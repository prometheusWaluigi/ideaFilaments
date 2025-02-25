from typing import Optional, Tuple

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import eigs


class QuantumErgodicity:
    """quantum ergodicity metrics going ABSOLUTELY BUCKWILD"""

    def __init__(self, hbar: float = 1.0, energy_cutoff: float = 10.0):
        self.hbar = hbar
        self.energy_cutoff = energy_cutoff
        self._cached_eigenstates: Optional[
            Tuple[np.ndarray, np.ndarray]
        ] = None  # type that cache PROPERLY

    def _get_eigenstates(
        self, hamiltonian: np.ndarray
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """get them eigenstates EFFICIENTLY using sparse matrices"""
        if self._cached_eigenstates is not None:
            return self._cached_eigenstates

        try:
            # convert to sparse and find eigenstates below cutoff
            sparse_h = csc_matrix(hamiltonian)
            energies, states = eigs(sparse_h, k=min(100, len(hamiltonian) - 2))

            # sort by energy
            idx = np.argsort(np.real(energies))
            energies = np.real(energies[idx])
            states = states[:, idx].T

            # filter by energy cutoff
            mask = energies < self.energy_cutoff
            result = (energies[mask], states[mask])
            self._cached_eigenstates = result
            return result

        except (ValueError, np.linalg.LinAlgError) as e:
            print(
                f"eigenstate computation failed bc quantum mechanics be like that: {e}"
            )
            return None, None

    # rest of the file stays the same bc it's already CLEAN
