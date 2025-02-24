from typing import List, Optional

import networkx as nx
import numpy as np

from ..core.celestial_point import CelestialPoint  # ADDED THIS IMPORT FR FR
from .base_pattern import BasePattern


class ArnoldWebPattern(BasePattern):
    """arnold diffusion but make it ASTRONOMICAL NO CAP"""

    def __init__(
        self, points: List[CelestialPoint], epsilon: float = 1e-3
    ):  # perturbation strength bc we CAREFUL
        super().__init__(points)
        self.eps = epsilon
        self._cached_web = None
        self._cached_whiskers = None  # heteroclinic tangle GANG

    def check_pattern(self) -> bool:
        """verify arnold web existence EXPEDITIOUSLY"""
        web = self.compute_arnold_web()
        return web is not None and self._check_web_connectivity(web)

    def pattern_strength(self) -> float:
        """compute pattern strength via HOMOCLINIC SPLITTING"""
        if self._cached_whiskers is None:
            return 0.0

        # measure splitting angle of invariant manifolds
        angles = self._compute_splitting_angles()
        return float(np.mean(np.exp(-angles)))  # exponential decay bc we ASYMPTOTIC

    def compute_arnold_web(self) -> Optional[nx.Graph]:
        """compute that arnold web CAREFULLY"""
        if self._cached_web is not None:
            return self._cached_web

        try:
            # construct phase space graph
            G = nx.Graph()

            # compute resonance lines (basic af rn)
            for i, p1 in enumerate(self.points):
                pos1 = p1.phase_space_state()[0]
                G.add_node(i, pos=pos1)

                for j, p2 in enumerate(self.points[i + 1 :], i + 1):
                    pos2 = p2.phase_space_state()[0]

                    # check resonance condition
                    if self._check_resonance(pos1, pos2):
                        G.add_edge(i, j)

            # verify web properties
            if self._verify_web_topology(G):
                self._cached_web = G
                return G
            return None

        except (ValueError, np.linalg.LinAlgError) as e:
            print(f"web computation failed bc CHAOS: {e}")
            return None

    def _check_resonance(self, p1: np.ndarray, p2: np.ndarray) -> bool:
        """check resonance condition RIGOROUSLY"""
        # compute frequency vectors
        omega1 = self._get_frequency(p1)
        omega2 = self._get_frequency(p2)

        # check near-resonance condition
        k_max = 3  # resonance order (keep it REASONABLE)
        for k1 in range(-k_max, k_max + 1):
            for k2 in range(-k_max, k_max + 1):
                if k1 == k2 == 0:
                    continue

                # resonance measure
                res = abs(k1 * omega1 + k2 * omega2)
                if res < self.eps:
                    return True

        return False

    def _get_frequency(self, p: np.ndarray) -> float:
        """compute frequency vector EXPEDITIOUSLY"""
        # basic frequency approximation
        return np.linalg.norm(p) + self.eps * np.sin(np.sum(p))

    def _verify_web_topology(self, G: nx.Graph) -> bool:
        """verify web has correct topology fr fr"""
        # check connectedness
        if not nx.is_connected(G):
            return False

        # compute some basic homology (SUPER basic rn)
        cycles = nx.cycle_basis(G)
        if len(cycles) < 1:  # need some complexity NO CAP
            return False

        return True

    def compute_melnikov_potential(self) -> np.ndarray:
        """compute that melnikov potential CAREFULLY"""
        if len(self.points) < 2:
            return np.array([])

        # get phase space coordinates
        positions = np.array([p.phase_space_state()[0] for p in self.points])

        # compute melnikov integral (BASIC VERSION RN)
        t = np.linspace(0, 10, 1000)  # integration time
        potential = np.zeros_like(positions)

        for i, pos in enumerate(positions):
            # separatrix solution (simplified)
            q = 2 * np.arctan(np.sinh(t))
            p = 2 / np.cosh(t)

            # perturbation
            H1 = self.eps * np.cos(q + pos[0])

            # melnikov integral
            potential[i] = np.trapz(H1 * p, t)

        return potential

    def _compute_splitting_angles(self) -> np.ndarray:
        """compute splitting angles EXPEDITIOUSLY"""
        if self._cached_whiskers is None:
            return np.array([])

        angles = []
        for p in self.points:
            # compute stable/unstable directions
            try:
                stable = self._compute_stable_manifold(p)
                unstable = self._compute_unstable_manifold(p)

                if stable is not None and unstable is not None:
                    # compute angle between manifolds
                    angle = np.arccos(np.clip(np.dot(stable, unstable), -1.0, 1.0))
                    angles.append(angle)
            except (ValueError, np.linalg.LinAlgError) as e:
                print(f"manifold computation failed bc INSTABILITY: {e}")
                continue

        return np.array(angles)

    def _compute_stable_manifold(self, p: CelestialPoint) -> Optional[np.ndarray]:
        """compute stable manifold CAREFULLY"""
        try:
            # basic linear approximation rn
            pos, vel = p.phase_space_state()

            # linearized dynamics
            A = self._linearized_dynamics(pos)

            # find stable direction (eigenvector w/ negative eigenvalue)
            eigenvals, eigenvecs = np.linalg.eig(A)
            stable_idx = np.argmin(np.real(eigenvals))

            return eigenvecs[:, stable_idx]

        except (ValueError, np.linalg.LinAlgError) as e:
            print(f"stable manifold computation failed bc CHAOS BE LIKE THAT: {e}")
            return None

    def _compute_unstable_manifold(self, p: CelestialPoint) -> Optional[np.ndarray]:
        """compute unstable manifold EXPEDITIOUSLY"""
        try:
            # same as stable but time-reversed
            stable = self._compute_stable_manifold(p)
            return -stable if stable is not None else None
        except (ValueError, np.linalg.LinAlgError) as e:
            print(f"unstable manifold computation failed bc CHAOS DO BE CHAOTIC: {e}")
            return None

    def _linearized_dynamics(self, pos: np.ndarray) -> np.ndarray:
        """compute linearized dynamics RIGOROUSLY"""
        # basic hamiltonian matrix
        n = len(pos)
        A = np.zeros((2 * n, 2 * n))

        # kinetic terms
        A[:n, n:] = np.eye(n)

        # potential terms (basic approximation)
        A[n:, :n] = -np.eye(n) - self.eps * np.cos(pos)

        return A


class ChaoticTransportPattern(BasePattern):
    """chaotic transport but make it COSMIC"""

    def __init__(self, points: List[CelestialPoint], diffusion_threshold: float = 0.1):
        super().__init__(points)
        self.D_thresh = diffusion_threshold
        self._cached_transport = None

    def check_pattern(self) -> bool:
        """verify chaotic transport EXPEDITIOUSLY"""
        # compute transport coefficients
        D = self._compute_diffusion()
        return np.any(D > self.D_thresh)

    def pattern_strength(self) -> float:
        """compute transport strength via DIFFUSION TENSOR"""
        if self._cached_transport is None:
            return 0.0

        # use largest transport coefficient
        return float(np.max(self._cached_transport))

    def _compute_diffusion(self) -> np.ndarray:
        """compute them diffusion coefficients CAREFULLY"""
        if self._cached_transport is not None:
            return self._cached_transport

        try:
            # get phase space trajectories
            positions = np.array([p.phase_space_state()[0] for p in self.points])

            # compute mean square displacement
            msd = np.zeros((len(positions), len(positions)))

            for i, pos1 in enumerate(positions):
                for j, pos2 in enumerate(positions):
                    dr = pos2 - pos1
                    msd[i, j] = np.dot(dr, dr)

            # estimate diffusion coefficients
            D = np.mean(msd, axis=1) / 2  # einstein relation fr fr

            self._cached_transport = D
            return D

        except (ValueError, AttributeError, np.linalg.LinAlgError) as e:
            print(f"diffusion computation failed bc we IMPERFECT: {e}")
            return np.array([])

    def compute_transport_network(self) -> Optional[nx.Graph]:
        """construct transport network EXPEDITIOUSLY"""
        if len(self.points) < 2:
            return None

        # make network of transport channels
        G = nx.Graph()

        # add nodes
        for i, p in enumerate(self.points):
            pos = p.phase_space_state()[0]
            G.add_node(i, pos=pos)

        # add edges where transport occurs
        D = self._compute_diffusion()
        if len(D) == len(self.points):
            for i in range(len(self.points)):
                for j in range(i + 1, len(self.points)):
                    # edge weight = geometric mean of coefficients
                    weight = np.sqrt(D[i] * D[j])
                    if weight > self.D_thresh:
                        G.add_edge(i, j, weight=float(weight))

        return G if G.number_of_edges() > 0 else None
