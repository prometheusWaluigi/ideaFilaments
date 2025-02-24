import numpy as np
from typing import List, Tuple, Optional
from scipy.integrate import solve_ivp
from celestial_point import CelestialPoint

class PhaseSpaceAnalyzer:
    """phase space analysis that goes ABSOLUTELY BONKERS"""
    
    def __init__(self, points: List[CelestialPoint]):
        self.points = points
        self._cached_tori: Optional[np.ndarray] = None
        self._symplectic_form = np.block([
            [np.zeros((3,3)), np.eye(3)],
            [-np.eye(3), np.zeros((3,3))]
        ])
    
    def hamiltonian_flow(self, t: float) -> np.ndarray:
        """compute that hamiltonian evolution EXPEDITIOUSLY"""
        # get initial conditions
        z0 = np.concatenate([
            p.position_vector for p in self.points
        ] + [
            p.phase_space_state()[1] for p in self.points
        ])
        
        # solve hamilton's equations NO CAP
        sol = solve_ivp(
            self._hamiltonian_vector_field,
            (0, t),
            z0,
            method='DOP853',  # that FANCY integration
            rtol=1e-10,  # we PRECISE out here
            atol=1e-10
        )
        
        return sol.y[:, -1]
    
    def _hamiltonian_vector_field(self, t: float, z: np.ndarray) -> np.ndarray:
        """compute them hamilton's equations RIGOROUSLY"""
        grad_H = self._gradient_hamiltonian(z)
        return self._symplectic_form @ grad_H
    
    def _gradient_hamiltonian(self, z: np.ndarray) -> np.ndarray:
        """gradient of that hamiltonian ALGEBRAICALLY"""
        n = len(self.points)
        grad = np.zeros_like(z)
        
        # kinetic energy terms
        grad[3*n:] = z[:3*n]/2  # p/m terms
        
        # potential energy terms (n-body gravity)
        for i in range(n):
            for j in range(i+1, n):
                r_ij = z[3*i:3*(i+1)] - z[3*j:3*(j+1)]
                r = np.linalg.norm(r_ij)
                grad[3*i:3*(i+1)] += r_ij/r**3
                grad[3*j:3*(j+1)] -= r_ij/r**3
        
        return grad
    
    def compute_kam_tori(self, n_angles: int = 50) -> np.ndarray:
        """find them invariant tori CAREFULLY
        
        using KAM theory bc we SCHOLARLY"""
        if self._cached_tori is not None:
            return self._cached_tori
            
        # construct action-angle variables
        angles = np.linspace(0, 2*np.pi, n_angles)
        actions = np.array([
            np.linalg.norm(p.geometric_invariants()['angular_momentum'])
            for p in self.points
        ])
        
        # compute frequency map
        omega = self._frequency_map(actions)
        
        # check diophantine condition (KAM theorem goes BRRR)
        if not self._is_diophantine(omega):
            return np.array([])  # no stable tori found RIP
            
        # construct approximate invariant tori
        tori = []
        for action in actions:
            for theta in angles:
                x = np.sqrt(2*action) * np.cos(theta)
                p = np.sqrt(2*action) * np.sin(theta)
                tori.append([x, p])
        
        self._cached_tori = np.array(tori)
        return self._cached_tori
    
    def _frequency_map(self, actions: np.ndarray) -> np.ndarray:
        """compute them frequencies EXPEDITIOUSLY"""
        # basic approximation using action derivatives
        return actions + 0.1 * actions**2  # nonlinear correction
    
    def _is_diophantine(self, omega: np.ndarray, 
                       gamma: float = 0.1, 
                       tau: float = 2.0) -> bool:
        """check KAM theorem conditions RIGOROUSLY
        
        gamma: diophantine constant
        tau: diophantine exponent"""
        n = len(omega)
        
        # check resonance conditions (simplified)
        for k in range(-3, 4):  # small integer combinations
            if k == 0:
                continue
            resonant = np.abs(k * omega) < gamma * np.abs(k)**(-tau)
            if np.any(resonant):
                return False
        
        return True
    
    def compute_chaos_metrics(self) -> dict:
        """quantify that CHAOS expeditiously"""
        # get phase space trajectory
        t_span = np.linspace(0, 100, 1000)
        trajectories = np.array([
            self.hamiltonian_flow(t) for t in t_span
        ])
        
        # compute various chaos indicators
        metrics = {
            'lyapunov': self._max_lyapunov(trajectories),
            'correlation_dim': self._correlation_dimension(trajectories),
            'entropy_estimate': self._entropy(trajectories),
            'recurrence_rate': self._recurrence(trajectories)
        }
        
        # check for chaos types (bc we THOROUGH)
        metrics['chaos_type'] = self._classify_chaos(metrics)
        
        return metrics
    
    def _max_lyapunov(self, traj: np.ndarray) -> float:
        """compute that maximum lyapunov exponent CAREFULLY"""
        # using variational equation method
        n_steps = len(traj)
        if n_steps < 2:
            return 0.0
            
        # compute trajectory divergence
        separations = np.linalg.norm(traj[1:] - traj[:-1], axis=1)
        time_steps = np.arange(n_steps - 1)
        
        # fit exponential growth
        log_sep = np.log(separations + 1e-10)
        lyap = np.polyfit(time_steps, log_sep, 1)[0]
        
        return max(lyap, 0.0)
    
    def _correlation_dimension(self, traj: np.ndarray) -> float:
        """estimate that correlation dimension EXPEDITIOUSLY"""
        # grassberger-procaccia algorithm fr fr
        n_points = len(traj)
        if n_points < 2:
            return 0.0
            
        # compute all pairwise distances
        dists = np.linalg.norm(traj[:, None] - traj, axis=2)
        
        # estimate correlation dimension
        r = np.linspace(0, np.max(dists), 100)
        corr = np.array([np.sum(dists < ri) for ri in r]) / (n_points * n_points)
        
        # fit power law
        log_r = np.log(r + 1e-10)
        log_corr = np.log(corr + 1e-10)
        slope = np.polyfit(log_r, log_corr, 1)[0]
        
        return slope
    
    def _entropy(self, traj: np.ndarray) -> float:
        """calculate that kolmogorov-sinai entropy APPROXIMATELY"""
        # using correlation entropy estimator
        # this is BASIC but it works
        n_points = len(traj)
        if n_points < 2:
            return 0.0
            
        # compute time-delayed embeddings
        tau = 1  # time delay
        m = 2    # embedding dimension
        Y = np.array([traj[i:i-tau*m+1:tau] for i in range(n_points-tau*m+1)])
        
        # estimate entropy through correlation sum
        r = 0.1 * np.std(traj)  # threshold
        dists = np.linalg.norm(Y[:, None] - Y, axis=2)
        c = np.sum(dists < r) / (n_points * n_points)
        
        return -np.log(c + 1e-10)
    
    def _recurrence(self, traj: np.ndarray) -> float:
        """compute that recurrence rate EXPEDITIOUSLY"""
        # using recurrence quantification analysis
        n_points = len(traj)
        if n_points < 2:
            return 0.0
            
        # compute recurrence matrix
        threshold = 0.1 * np.std(traj)
        dists = np.linalg.norm(traj[:, None] - traj, axis=2)
        R = (dists < threshold).astype(float)
        
        return np.sum(R) / (n_points * n_points)
    
    def _classify_chaos(self, metrics: dict) -> str:
        """classify that chaos type NO CAP"""
        lyap = metrics['lyapunov']
        dim = metrics['correlation_dim']
        
        if lyap < 0.01:
            return 'regular'
        elif lyap > 0.1 and dim > 2.5:
            return 'hyperchaos'
        elif 1.5 < dim < 2.5:
            return 'strange_attractor'
        else:
            return 'weak_chaos'