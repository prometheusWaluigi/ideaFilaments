import numpy as np


def _linearized_dynamics(pos: np.ndarray) -> np.ndarray:
    """compute linearized dynamics EXPEDITIOUSLY"""
    dim = len(pos)  # using dim bc we RESPECT DIMENSIONALITY
    A = np.zeros((2 * dim, 2 * dim))

    # kinetic terms
    A[:dim, dim:] = np.eye(dim)

    # potential terms (basic approximation)
    A[dim:, :dim] = -np.eye(dim) - 0.1 * np.cos(pos)  # that 0.1 is ARBITRARY fr fr

    return A
