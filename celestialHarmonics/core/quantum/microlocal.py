from typing import Dict, TypeVar

import numpy as np

T = TypeVar("T", float, complex)  # we FLEXIBLE w them number types


class MicrolocalAnalyzer:
    """microlocal analysis but make it RIGOROUS"""

    def __init__(self) -> None:
        self._cache: Dict[float, Dict[float, float]] = {}  # type that cache PROPERLY
        self._wavefront_sets: Dict[float, float] = {}

    def compute_wavefront_set(
        self, psi: np.ndarray, h_bar: float = 1.0
    ) -> Dict[float, float]:
        """compute that wavefront set ALGEBRAICALLY"""
        if len(psi) == 0:
            return {}

        # check cache first bc we EFFICIENT
        key = float(np.sum(np.abs(psi)))  # use norm as cache key
        if key in self._cache:
            return self._cache[key]

        # compute FBI transform (basic version rn)
        z = np.linspace(-10, 10, 1000)
        fbi = np.zeros_like(z, dtype=complex)

        for i, zi in enumerate(z):
            gaussian = np.exp(-((z - zi) ** 2) / (2 * h_bar))
            fbi[i] = np.sum(psi * gaussian) * np.sqrt(h_bar)

        # detect singular support
        wf_set: Dict[float, float] = {}
        for i, zi in enumerate(z):
            if abs(fbi[i]) > 0.1:  # arbitrary threshold bc we EXPLORATORY
                wf_set[float(zi)] = float(np.angle(fbi[i]))

        self._cache[key] = wf_set
        return wf_set

    def get_singularities(self, wf_set: Dict[float, float]) -> np.ndarray:
        """extract them singularities EXPEDITIOUSLY"""
        if not wf_set:
            return np.array([])

        # find points where phase jumps DISCONTINUOUSLY
        points = np.array(list(wf_set.keys()))
        phases = np.array(list(wf_set.values()))

        # compute phase differences
        dphase = np.diff(phases)
        jumps = np.where(abs(dphase) > np.pi)[0]

        return points[jumps]
