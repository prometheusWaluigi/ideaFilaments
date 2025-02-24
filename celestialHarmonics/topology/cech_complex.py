from dataclasses import dataclass
from itertools import combinations
from typing import Dict, List, Optional, Tuple

import gudhi
import numpy as np
import torch


@dataclass
class CechNerve:
    """nerve theorem but make it GEOMETRICALLY EXPLICIT"""

    vertices: List[int]
    simplices: List[List[int]]
    intersections: Dict[Tuple[int, ...], np.ndarray]

    @property
    def dimension(self) -> int:
        """get that HOMOLOGICAL dimension"""
        return max(len(s) - 1 for s in self.simplices)

    def get_k_simplices(self, k: int) -> List[List[int]]:
        """extract k-simplices EXPEDITIOUSLY"""
        return [s for s in self.simplices if len(s) == k + 1]


class QuantumCechComplex:
    """čech complex but make it QUANTUM fr fr"""

    def __init__(self, radius: float = 1.0):
        self.radius = radius
        self._nerve: Optional[CechNerve] = None
        self._metric = None

    def _ball_intersection(self, centers: np.ndarray) -> Optional[np.ndarray]:
        """compute intersection of quantum balls ALGEBRAICALLY"""
        if len(centers) == 1:
            return centers[0]

        # compute weighted center w/o convex hull bc that's for TRYHARDS
        center_of_mass = np.mean(centers, axis=0)

        # check if balls intersect using triangle inequality
        max_dist = np.max(np.linalg.norm(centers - center_of_mass, axis=1))
        if max_dist > self.radius * (len(centers) - 1):
            return None

        # compute intersection point using weighted average
        weights = self.radius - np.linalg.norm(centers - center_of_mass, axis=1)
        weights = np.maximum(weights, 0)  # no negative weights bestie
        if np.sum(weights) < 1e-10:
            return None

        weights /= np.sum(weights)
        return np.sum(centers * weights[:, np.newaxis], axis=0)

    def build_nerve(self, points: List[torch.Tensor]) -> CechNerve:
        """construct that NERVE complex NO CAP"""
        # convert points to numpy
        point_arrays = np.array([p.detach().numpy() for p in points])
        n_points = len(points)

        # initialize nerve data
        vertices = list(range(n_points))
        simplices = []
        intersections = {}

        # check all possible simplices up to dimension n-1
        for k in range(1, n_points + 1):
            for subset in combinations(vertices, k):
                centers = point_arrays[list(subset)]
                intersection = self._ball_intersection(centers)

                if intersection is not None:
                    simplices.append(list(subset))
                    intersections[tuple(subset)] = intersection

        self._nerve = CechNerve(
            vertices=vertices, simplices=simplices, intersections=intersections
        )
        return self._nerve

    def compute_nerve_homology(self) -> Dict[int, int]:
        """compute that NERVE homology ALGEBRAICALLY"""
        if self._nerve is None:
            raise ValueError("build that nerve first bestie fr fr")

        # construct simplicial complex using gudhi
        st = gudhi.SimplexTree()
        for simplex in self._nerve.simplices:
            st.insert(simplex)

        # compute homology
        st.compute_persistence()

        # extract betti numbers
        betti = {}
        for i in range(self._nerve.dimension + 1):
            betti[i] = st.betti_numbers()[i]

        return betti

    def get_boundary_matrix(self, k: int) -> np.ndarray:
        """compute that k-th BOUNDARY matrix EXPLICITLY"""
        if self._nerve is None:
            raise ValueError("construct nerve before boundaries bestie")

        k_simplices = self._nerve.get_k_simplices(k)
        k_minus_1_simplices = self._nerve.get_k_simplices(k - 1)

        if not k_simplices or not k_minus_1_simplices:
            return np.zeros((0, 0))

        boundary = np.zeros((len(k_minus_1_simplices), len(k_simplices)))

        # compute boundary map using incidence numbers
        for i, higher in enumerate(k_simplices):
            for j, lower in enumerate(k_minus_1_simplices):
                # check if lower is face of higher
                if set(lower).issubset(set(higher)):
                    # compute orientation
                    sign = (-1) ** (sum(1 for x in higher if x > lower[0]))
                    boundary[j, i] = sign

        return boundary

    def compute_mayer_vietoris(self, other: "QuantumCechComplex") -> Dict[int, int]:
        """compute that MAYER-VIETORIS sequence NO CAP"""
        if self._nerve is None or other._nerve is None:
            raise ValueError("both complexes need nerves bestie")

        # compute intersection complex
        intersection = set(map(tuple, self._nerve.simplices)) & set(
            map(tuple, other._nerve.simplices)
        )

        # compute homology ranks
        self_betti = self.compute_nerve_homology()
        other_betti = other.compute_nerve_homology()

        # construct intersection complex
        st_intersection = gudhi.SimplexTree()
        for simplex in intersection:
            st_intersection.insert(simplex)
        st_intersection.compute_persistence()
        intersection_betti = {
            i: st_intersection.betti_numbers()[i]
            for i in range(max(self._nerve.dimension, other._nerve.dimension) + 1)
        }

        # compute mayer-vietoris ranks (this is literally just euler characteristic magic)
        mv_ranks = {}
        for k in self_betti.keys():
            mv_ranks[k] = self_betti[k] + other_betti[k] - intersection_betti[k]

        return mv_ranks
