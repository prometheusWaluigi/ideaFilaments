import itertools
from typing import List

import numpy as np

from ..core.celestial_point import CelestialPoint
from .base_pattern import BasePattern


class GeometricPattern(BasePattern):
    """detect them geometric patterns ALGEBRAICALLY"""

    def __init__(self, points: List[CelestialPoint], symmetry_threshold: float = 0.1):
        super().__init__(points)
        self.symmetry_thresh = symmetry_threshold
        self._cached_symmetries = None

    def check_pattern(self) -> bool:
        """verify geometric pattern RIGOROUSLY"""
        symmetries = self._compute_symmetries()
        return any(s > self.symmetry_thresh for s in symmetries.values())

    def pattern_strength(self) -> float:
        """compute geometric pattern strength EXPEDITIOUSLY"""
        if self._cached_symmetries is None:
            self._cached_symmetries = self._compute_symmetries()
        return float(max(self._cached_symmetries.values()))

    def _compute_symmetries(self) -> dict:
        """compute them geometric symmetries CAREFULLY"""
        if self._cached_symmetries is not None:
            return self._cached_symmetries

        # get point positions
        positions = np.array([p.position_vector for p in self.points])

        # compute different symmetry types
        symmetries = {
            "translation": self._translation_symmetry(positions),
            "rotation": self._rotation_symmetry(positions),
            "reflection": self._reflection_symmetry(positions),
            "scale": self._scale_symmetry(positions),
        }

        self._cached_symmetries = symmetries
        return symmetries

    def _translation_symmetry(self, positions: np.ndarray) -> float:
        """detect translation symmetry EXPEDITIOUSLY"""
        if len(positions) < 2:
            return 0.0

        # compute all possible translation vectors
        translations = []
        for i, j in itertools.combinations(range(len(positions)), 2):
            t = positions[j] - positions[i]
            translations.append(t / np.linalg.norm(t))

        # check how many points respect each translation
        max_sym = 0.0
        for t in translations:
            # translate all points
            translated = positions + t

            # count matching points
            matches = 0
            for p1 in translated:
                if any(np.allclose(p1, p2, rtol=1e-5) for p2 in positions):
                    matches += 1

            sym = matches / len(positions)
            max_sym = max(max_sym, sym)

        return max_sym

    def _rotation_symmetry(self, positions: np.ndarray) -> float:
        """detect rotation symmetry CAREFULLY"""
        if len(positions) < 2:
            return 0.0

        # compute centroid
        center = positions.mean(axis=0)
        centered = positions - center

        # check different rotation angles
        max_sym = 0.0
        angles = np.linspace(0, 2 * np.pi, 36)[1:]  # skip identity

        for theta in angles:
            # rotation matrix
            R = np.array(
                [
                    [np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1],
                ]
            )

            # rotate points
            rotated = centered @ R.T + center

            # count matching points
            matches = 0
            for p1 in rotated:
                if any(np.allclose(p1, p2, rtol=1e-5) for p2 in positions):
                    matches += 1

            sym = matches / len(positions)
            max_sym = max(max_sym, sym)

        return max_sym

    def _reflection_symmetry(self, positions: np.ndarray) -> float:
        """detect reflection symmetry ALGEBRAICALLY"""
        if len(positions) < 2:
            return 0.0

        # try reflection planes aligned with coordinate axes
        max_sym = 0.0
        for axis in range(3):
            # reflection matrix
            R = np.eye(3)
            R[axis, axis] = -1

            # reflect points
            reflected = positions @ R

            # count matching points
            matches = 0
            for p1 in reflected:
                if any(np.allclose(p1, p2, rtol=1e-5) for p2 in positions):
                    matches += 1

            sym = matches / len(positions)
            max_sym = max(max_sym, sym)

        return max_sym

    def _scale_symmetry(self, positions: np.ndarray) -> float:
        """detect scale symmetry EXPEDITIOUSLY"""
        if len(positions) < 2:
            return 0.0

        # compute centroid
        center = positions.mean(axis=0)
        centered = positions - center

        # check different scale factors
        max_sym = 0.0
        scales = np.logspace(-1, 1, 20)  # try various scales

        for s in scales:
            # scale points
            scaled = s * centered + center

            # count matching points
            matches = 0
            for p1 in scaled:
                if any(np.allclose(p1, p2, rtol=1e-5) for p2 in positions):
                    matches += 1

            sym = matches / len(positions)
            max_sym = max(max_sym, sym)

        return max_sym
