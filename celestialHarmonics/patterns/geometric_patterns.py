from typing import Dict, List, Optional

import numpy as np

from ..core.celestial_point import CelestialPoint
from .base_pattern import BasePattern


class GeometricPattern(BasePattern):
    """detect them geometric patterns ALGEBRAICALLY"""

    def __init__(self, points: List[CelestialPoint], symmetry_threshold: float = 0.1):
        super().__init__(points)
        self.symmetry_thresh = symmetry_threshold
        self._cached_symmetries: Optional[
            Dict[str, float]
        ] = None  # type that cache PROPERLY

    def check_pattern(self) -> bool:
        """verify geometric pattern RIGOROUSLY"""
        symmetries = self._compute_symmetries()
        return any(s > self.symmetry_thresh for s in symmetries.values())

    def pattern_strength(self) -> float:
        """compute geometric pattern strength EXPEDITIOUSLY"""
        if self._cached_symmetries is None:
            self._cached_symmetries = self._compute_symmetries()
        return float(
            max(self._cached_symmetries.values(), default=0.0)
        )  # handle empty dict case

    def _compute_symmetries(self) -> Dict[str, float]:
        """compute them geometric symmetries CAREFULLY"""
        if self._cached_symmetries is not None:
            return self._cached_symmetries

        # init empty dict for safety
        result: Dict[str, float] = {}

        # get point positions
        positions = np.array([p.position_vector for p in self.points])

        # compute different symmetry types
        result = {
            "translation": self._translation_symmetry(positions),
            "rotation": self._rotation_symmetry(positions),
            "reflection": self._reflection_symmetry(positions),
            "scale": self._scale_symmetry(positions),
        }

        self._cached_symmetries = result
        return result

    # rest of file stays the same bc it's CLEAN
