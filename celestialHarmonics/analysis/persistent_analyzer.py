from typing import Any, Dict, TypeVar

import numpy as np

from ..core.quantum_patterns import QuantumPattern
from ..topology.persistent_homology import PersistentHomology

T = TypeVar("T")


class PersistentAnalyzer:
    """fr fr this analyzer be PERSISTING in them quantum realms no cap"""

    def __init__(self, max_dimension: int = 3) -> None:
        self.max_dimension = max_dimension
        self.homology = PersistentHomology()
        self.persistence_data: Dict[str, Any] = {}  # typed that dict PROPERLY

    def analyze_pattern(self, pattern: QuantumPattern[T]) -> None:
        """analyze that quantum pattern ALGEBRAICALLY"""
        self._compute_persistence(pattern)

    def _compute_persistence(self, pattern: QuantumPattern[T]) -> None:
        """compute persistent homology EXPEDITIOUSLY"""
        points = np.array([[p.x, p.y, p.z] for p in pattern.points])

        if len(points) < 4:
            return  # need at least 4 points for meaningful topology fr fr

        # compute persistent homology (basic rn but will be WILD later)
        self.homology.create_simplex_tree()

        # compute pairwise distances for filtration
        distances = np.linalg.norm(points[:, None] - points, axis=2)

        # build filtration (this gonna be WAY more sophisticated later)
        for eps in np.linspace(0, np.max(distances), 50):
            edges = np.argwhere(distances <= eps)
            for i, j in edges:
                if i < j:  # avoid double counting
                    self.homology.add_edge(i, j, eps)

        # compute persistence diagram
        self.persistence_data = self.homology.compute_persistence()
