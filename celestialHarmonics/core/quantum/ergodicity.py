from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import eigs

from core.celestial_point import CelestialPoint  # ADDED THIS IMPORT FR FR


class QuantumErgodicity:
    """quantum ergodicity metrics going ABSOLUTELY BUCKWILD"""

    def __init__(self, hbar: float = 1.0, energy_cutoff: float = 10.0):
        self.hbar = hbar
        self.energy_cutoff = energy_cutoff
        self._cached_eigenstates = None

    def quantum_variance(
        self, observable: np.ndarray, eigenstates: np.ndarray
    ) -> float:
        """compute that quantum variance EXPEDITIOUSLY
        this measures how ergodic the quantum system is fr fr"""

        # compute expectation values
        expectations = np.array(
            [np.abs(np.vdot(state, observable @ state)) for state in eigenstates]
        )

        # compute variance of matrix elements
        return np.var(expectations)

    def rate_of_eigenstate_thermalization(self, hamiltonian: np.ndarray) -> float:
        """check how fast them eigenstates thermalize NO CAP"""

        # get eigenstates below energy cutoff
        energies, states = self._get_eigenstates(hamiltonian)
        if states is None:
            return 0.0

        # compute overlaps between nearby eigenstates
        overlaps = np.array(
            [
                np.abs(np.vdot(states[i], states[i + 1])) ** 2
                for i in range(len(states) - 1)
            ]
        )

        # fit exponential decay
        log_overlaps = np.log(overlaps + 1e-10)
        thermalization_rate = -np.polyfit(range(len(log_overlaps)), log_overlaps, 1)[0]

        return max(thermalization_rate, 0.0)

    def level_spacing_statistics(self, hamiltonian: np.ndarray) -> Dict[str, float]:
        """analyze them energy level spacings RIGOROUSLY
        GOE statistics = quantum chaos fr fr"""

        # get energy levels
        energies, _ = self._get_eigenstates(hamiltonian)
        if energies is None:
            return {"r_mean": 0.0, "level_variance": 0.0}

        # compute nearest neighbor spacings
        spacings = np.diff(energies)

        # compute ratio of consecutive spacings
        r = np.minimum(spacings[:-1], spacings[1:]) / np.maximum(
            spacings[:-1], spacings[1:]
        )

        return {
            "r_mean": float(np.mean(r)),  # should be ~0.53 for GOE
            "level_variance": float(np.var(spacings)),  # should be small for chaos
        }

    def scarring_measure(
        self, eigenstates: np.ndarray, periodic_orbit: np.ndarray
    ) -> float:
        """compute how much them eigenstates SCAR on periodic orbits"""

        # project eigenstates onto periodic orbit
        projections = np.array(
            [np.abs(np.vdot(state, periodic_orbit)) ** 2 for state in eigenstates]
        )

        # high projections = scarring
        return float(np.max(projections))

    def _get_eigenstates(
        self, hamiltonian: np.ndarray
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """get them eigenstates EFFICIENTLY using sparse matrices"""
        if self._cached_eigenstates is not None:
            return self._cached_eigenstates

        try:
            # convert to sparse and find eigenstates below cutoff
            sparse_h = csc_matrix(hamiltonian)
            energies, states = eigs(sparse_h, k=min(100, len(hamiltonian) - 2))

            # sort by energy
            idx = np.argsort(np.real(energies))
            energies = np.real(energies[idx])
            states = states[:, idx].T

            # filter by energy cutoff
            mask = energies < self.energy_cutoff
            self._cached_eigenstates = (energies[mask], states[mask])
            return self._cached_eigenstates

        except (ValueError, np.linalg.LinAlgError) as e:
            print(
                f"eigenstate computation failed bc quantum mechanics be like that: {e}"
            )
            return None, None


def compute_ergodicity_metrics(
    points: List[CelestialPoint], hbar: float = 1.0
) -> Dict[str, float]:
    """compute them ergodicity metrics for celestial configurations"""

    # construct hamiltonian from point positions
    N = len(points)
    H = np.zeros((N, N))

    for i in range(N):
        for j in range(i + 1, N):
            # coupling strength falls off with angular separation
            angle = points[i].angular_separation(points[j])
            H[i, j] = H[j, i] = 1.0 / (1.0 + angle)

    # add kinetic energy terms
    for i in range(N):
        H[i, i] = points[i].distance_au

    # analyze quantum ergodicity
    analyzer = QuantumErgodicity(hbar=hbar)

    # position observable
    X = np.diag([p.ra_degrees for p in points])

    # get eigenstates
    energies, states = analyzer._get_eigenstates(H)
    if states is None:
        return {"quantum_variance": 0.0, "thermalization_rate": 0.0}

    # compute metrics
    metrics = {
        "quantum_variance": float(analyzer.quantum_variance(X, states)),
        "thermalization_rate": float(analyzer.rate_of_eigenstate_thermalization(H)),
    }

    # add level statistics
    metrics.update(analyzer.level_spacing_statistics(H))

    return metrics
