import numpy as np
from typing import List, Dict, Optional
from scipy.spatial.distance import pdist, squareform
import dionysus as d  # persistence homology GANG
import ripser
from patterns.base_pattern import BasePattern

class PersistentAnalyzer:
    """persistent homology but make it ASTRONOMICAL fr fr"""
    
    def __init__(self, max_dimension: int = 3):
        self.max_dim = max_dimension
        self._cached_diagrams = {}  # memoization bc we EFFICIENT
        
    def analyze_pattern(self, pattern: BasePattern) -> Dict[str, Any]:
        """analyze pattern topology EXPEDITIOUSLY"""
        # get point cloud data
        points = np.array([
            p.phase_space_state()[0] for p in pattern.points
        ])
        
        # compute persistent homology
        dgms = self._get_persistence_diagrams(points)
        
        # extract topological features NO CAP
        return {
            'betti_numbers': self._compute_betti_numbers(dgms),
            'persistence_entropy': self._compute_persistence_entropy(dgms),
            'wasserstein_stability': self._compute_wasserstein_stability(dgms),
            'zigzag_persistence': self._compute_zigzag_persistence(points)
        }
    
    def _get_persistence_diagrams(self, points: np.ndarray) -> List[np.ndarray]:
        """compute them persistence diagrams CAREFULLY"""
        # check cache first bc we SMART
        key = hash(points.tobytes())
        if key in self._cached_diagrams:
            return self._cached_diagrams[key]
        
        # compute distance matrix
        dists = squareform(pdist(points))
        
        # compute persistence (using ripser bc it's EXPEDITIOUS)
        diagrams = ripser.ripser(
            dists,
            distance_matrix=True,
            maxdim=self.max_dim,
            coeff=2  # Z/2Z coefficients bc we ALGEBRAIC
        )['dgms']
        
        self._cached_diagrams[key] = diagrams
        return diagrams
    
    def _compute_betti_numbers(self, dgms: List[np.ndarray]) -> List[int]:
        """compute them betti numbers RIGOROUSLY"""
        betti = []
        for k, dgm in enumerate(dgms):
            # count persistence pairs that exist at threshold
            threshold = np.median([p[1] for p in dgm if p[1] < np.inf])
            betti.append(np.sum(
                (dgm[:, 0] <= threshold) & (dgm[:, 1] > threshold)
            ))
        return betti
    
    def _compute_persistence_entropy(self, dgms: List[np.ndarray]) -> List[float]:
        """compute persistence entropy EXPEDITIOUSLY"""
        entropy = []
        for dgm in dgms:
            # get finite persistence pairs
            pairs = dgm[dgm[:, 1] < np.inf]
            if len(pairs) == 0:
                entropy.append(0.0)
                continue
                
            # compute persistence lengths
            lengths = pairs[:, 1] - pairs[:, 0]
            
            # normalize and compute entropy
            total_length = np.sum(lengths)
            if total_length > 0:
                p = lengths / total_length
                entropy.append(-np.sum(p * np.log(p + 1e-10)))
            else:
                entropy.append(0.0)
                
        return entropy
    
    def _compute_wasserstein_stability(self, dgms: List[np.ndarray]) -> List[float]:
        """compute wasserstein stability ALGEBRAICALLY"""
        stability = []
        for dgm in dgms:
            if len(dgm) < 2:
                stability.append(0.0)
                continue
                
            # compute pairwise distances between persistence pairs
            X = dgm[:, None, :]  # (n,1,2)
            Y = dgm[None, :, :]  # (1,n,2)
            dists = np.sqrt(np.sum((X - Y)**2, axis=2))  # (n,n)
            
            # compute bottleneck distance
            stability.append(np.min(dists[dists > 0]))
            
        return stability
    
    def _compute_zigzag_persistence(self, points: np.ndarray) -> Dict[str, Any]:
        """compute zigzag persistence CAREFULLY"""
        # construct zigzag filtration
        zz = self._build_zigzag_filtration(points)
        
        # compute zigzag persistence
        zz_dgms = d.zigzag_homology_persistence(zz)
        
        # extract features (BASIC af rn but it works)
        features = {
            'num_intervals': len(zz_dgms),
            'max_length': max(d.death - d.birth for d in zz_dgms),
            'total_persistence': sum(d.death - d.birth for d in zz_dgms)
        }
        
        return features
    
    def _build_zigzag_filtration(self, points: np.ndarray) -> d.Filtration:
        """build zigzag filtration EXPEDITIOUSLY"""
        # construct sequence of simplicial complexes
        filtration = d.Filtration()
        
        # add vertices
        for i in range(len(points)):
            filtration.append(d.Simplex([i], 0))
        
        # add edges based on distance threshold
        dists = squareform(pdist(points))
        threshold = np.median(dists)
        
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                if dists[i,j] <= threshold:
                    filtration.append(d.Simplex([i,j], dists[i,j]))
        
        # sort filtration
        filtration.sort()
        return filtration

    def visualize_persistence(self, dgms: List[np.ndarray]) -> Dict[str, Any]:
        """visualize persistence diagrams CAREFULLY"""
        viz_data = {}
        
        for k, dgm in enumerate(dgms):
            # get finite points
            finite = dgm[dgm[:, 1] < np.inf]
            
            # compute persistence landscape
            if len(finite) > 0:
                land = self._compute_persistence_landscape(finite)
                viz_data[f'dim_{k}_landscape'] = land
            
        return viz_data
    
    def _compute_persistence_landscape(self, dgm: np.ndarray) -> np.ndarray:
        """compute persistence landscape EXPEDITIOUSLY"""
        if len(dgm) == 0:
            return np.array([])
            
        # convert diagram to landscape functions
        n_points = 100
        x = np.linspace(np.min(dgm), np.max(dgm), n_points)
        
        landscapes = []
        for i in range(min(len(dgm), 5)):  # just compute first 5 levels
            land = np.zeros(n_points)
            
            for birth, death in dgm:
                # compute landscape function
                midpoint = (birth + death) / 2
                height = (death - birth) / 2
                
                # update landscape level
                mask = (x >= birth) & (x <= death)
                land[mask] = np.maximum(land[mask],
                    np.minimum(x[mask] - birth, death - x[mask]))
                
            landscapes.append(land)
            
        return np.array(landscapes)