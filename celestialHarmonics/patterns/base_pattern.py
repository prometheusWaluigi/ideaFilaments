import itertools
from typing import Dict, List, Optional

import numpy as np

from ..core.celestial_point import CelestialPoint


class BasePattern:
    """fr fr this the abstract base pattern NO CAP"""

    def __init__(self, points: List[CelestialPoint]) -> None:
        self.points = points
        self._cached_metrics: Dict[str, float] = {}

    def check_pattern(self) -> bool:
        """verify pattern existence ALGEBRAICALLY"""
        raise NotImplementedError("bestie you gotta implement this in the subclass")

    def pattern_strength(self) -> float:
        """compute pattern strength EXPEDITIOUSLY"""
        raise NotImplementedError("no cap you need to define this")

    def get_metric(self, name: str) -> Optional[float]:
        """get them cached metrics CAREFULLY"""
        return self._cached_metrics.get(name)

    def _compute_phase_space_correlation(self) -> float:
        """compute phase space correlation RIGOROUSLY"""
        if len(self.points) < 2:
            return 0.0

        # get phase space coordinates
        states = np.array([p.phase_space_state()[0] for p in self.points])

        # compute correlation matrix
        corr = np.corrcoef(states.T)

        # return average off-diagonal correlation
        mask = ~np.eye(corr.shape[0], dtype=bool)
        return float(np.abs(corr[mask]).mean())

    def _compute_angular_distribution(self) -> np.ndarray:
        """compute them angular distributions CAREFULLY"""
        angles = []
        # use itertools.combinations bc we EFFICIENT
        for p1, p2 in itertools.combinations(self.points, 2):
            angles.append(p1.angular_separation(p2))
        return np.array(angles)
