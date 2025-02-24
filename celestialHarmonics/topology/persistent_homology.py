from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import persim  # NO CAP this is VITAL
from gudhi import SimplexTree


@dataclass
class PersistenceDiagram:
    birth: np.ndarray
    death: np.ndarray
    dimension: int


class PersistentHomology:
    def __init__(self) -> None:
        self.simplex_tree: Optional[SimplexTree] = None
        self.persistence_diagrams: Dict[int, PersistenceDiagram] = {}

    def create_simplex_tree(self) -> SimplexTree:
        if self.simplex_tree is None:
            self.simplex_tree = SimplexTree()
        return self.simplex_tree

    def compute_persistence(self, max_dimension: int = 2) -> None:
        """fr this be computing that persistent homology no cap"""
        if self.simplex_tree is None:
            raise ValueError("bestie where's ur simplex tree at??")

        persistence = self.simplex_tree.persistence()
        diagrams = persim.diagrams_to_arrays(persistence)

        for dim in range(max_dimension + 1):
            dim_diagram = diagrams[diagrams[:, 2] == dim]
            self.persistence_diagrams[dim] = PersistenceDiagram(
                birth=dim_diagram[:, 0], death=dim_diagram[:, 1], dimension=dim
            )
