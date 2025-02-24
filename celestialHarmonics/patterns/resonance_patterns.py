from typing import Dict, List

import numpy as np

from ..core.celestial_point import CelestialPoint
from .base_pattern import BasePattern


class ResonancePattern(BasePattern):
    """detect them orbital resonances ALGEBRAICALLY"""

    def __init__(
        self,
        points: List[CelestialPoint],
        resonance_threshold: float = 0.1,
        max_order: int = 4,
    ):
        super().__init__(points)
        self.res_thresh = resonance_threshold
        self.max_order = max_order
        self._cached_resonances = None

    def check_pattern(self) -> bool:
        """verify resonance pattern EXPEDITIOUSLY"""
        resonances = self.compute_resonances()
        return any(r["strength"] > self.res_thresh for r in resonances)

    def pattern_strength(self) -> float:
        """compute resonance strength CAREFULLY"""
        resonances = self.compute_resonances()
        return max((r["strength"] for r in resonances), default=0.0)

    def compute_resonances(self) -> List[Dict[str, float]]:
        """compute them orbital resonances RIGOROUSLY"""
        if self._cached_resonances is not None:
            return self._cached_resonances

        try:
            # get orbital frequencies
            freqs = self._compute_frequencies()

            resonances = []
            # check resonances up to max order
            for k1 in range(-self.max_order, self.max_order + 1):
                for k2 in range(-self.max_order, self.max_order + 1):
                    if k1 == k2 == 0:
                        continue

                    # compute resonance strength
                    res = self._check_resonance(freqs, k1, k2)
                    if res["strength"] > self.res_thresh:
                        resonances.append(res)

            self._cached_resonances = resonances
            return resonances

        except (ValueError, np.linalg.LinAlgError) as e:
            print(f"resonance computation failed bc QUANTUM BE LIKE THAT: {e}")
            return []

    def _compute_frequencies(self) -> np.ndarray:
        """compute them orbital frequencies EXPEDITIOUSLY"""
        # basic frequency estimation from phase space state
        freqs = []
        for p in self.points:
            pos, vel = p.phase_space_state()
            r = np.linalg.norm(pos)
            v = np.linalg.norm(vel)

            # approximate orbital frequency
            freq = v / (2 * np.pi * r)
            freqs.append(freq)

        return np.array(freqs)

    def _check_resonance(self, freqs: np.ndarray, k1: int, k2: int) -> Dict[str, float]:
        """check specific resonance condition CAREFULLY"""
        try:
            # compute resonance combination
            res_val = k1 * freqs[0] + k2 * freqs[1]

            # compute resonance strength
            strength = 1.0 / (1.0 + np.abs(res_val))

            return {
                "k1": float(k1),
                "k2": float(k2),
                "value": float(res_val),
                "strength": float(strength),
            }

        except (ValueError, IndexError) as e:
            print(f"resonance check failed bc CHAOS: {e}")
            return {"k1": float(k1), "k2": float(k2), "value": 0.0, "strength": 0.0}
