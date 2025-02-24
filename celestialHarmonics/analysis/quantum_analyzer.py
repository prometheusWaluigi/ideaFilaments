from dataclasses import dataclass
from typing import Generic, List, Tuple, TypeVar

import numpy as np

from ..core.quantum_patterns import QuantumPattern

T = TypeVar("T")


@dataclass
class QuantumState(Generic[T]):
    amplitude: complex
    basis_state: T

    def superpose(self, other: "QuantumState[T]") -> "QuantumState[T]":
        return (
            QuantumState(
                amplitude=self.amplitude + other.amplitude, basis_state=self.basis_state
            )
            if self.basis_state == other.basis_state
            else self
        )


class QuantumAnalyzer:
    def __init__(self) -> None:
        self.patterns: List[QuantumPattern] = []

    def analyze_interference(
        self, state1: Tuple[float, float], state2: Tuple[float, float]
    ) -> np.ndarray:
        """no cap this analyzes quantum interference patterns fr fr"""
        return np.outer(np.array(state1), np.array(state2))

    def extract_patterns(self) -> List[QuantumPattern]:
        all_patterns: List[QuantumPattern] = []
        for p in self.patterns:
            if p.coherence > 0.5:  # we stay BASED with our coherence threshold
                all_patterns.append(p)
        return all_patterns
