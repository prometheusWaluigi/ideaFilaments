"""
fr fr this generates KPZ dynamics for quantum biological computing no cap
implements nature's middleware for coherence management
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class KPZParams:
    """parameters for that KPZ gaming fr fr"""
    nu: float = 0.1        # smoothing coefficient (real)
    lambda_: float = 0.5   # nonlinearity throwing it back
    noise_strength: float = 1.0  # quantum chaos amplitude
    dt: float = 0.01      # time step (based)

class KPZCoherenceManager:
    """
    implements KPZ dynamics for quantum biological middleware
    manages coherence through controlled chaos no cap
    """
    def __init__(self, size: int = 100, params: KPZParams = KPZParams()):
        self.size = size
        self.params = params
        self.height = np.zeros(size)
        self.time_series = []

    def compute_gradients(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        calculates spatial derivatives for KPZ gaming
        returns: gradient and laplacian fr fr
        """
        grad = np.gradient(self.height)
        laplacian = np.gradient(grad)[0]
        return grad[0], laplacian

    def generate_noise(self) -> np.ndarray:
        """spawns quantum noise fr fr"""
        return self.params.noise_strength * np.random.randn(self.size)

    def evolve(self) -> None:
        """
        evolves KPZ dynamics for one time step no cap
        implements that middleware coherence management
        """
        grad, laplacian = self.compute_gradients()
        noise = self.generate_noise()

        # KPZ equation throwing it back:
        # ∂h/∂t = ν∇²h + λ(∇h)² + η
        dh_dt = (
            self.params.nu * laplacian +
            self.params.lambda_ * grad**2 +
            noise
        )

        self.height += dh_dt * self.params.dt
        self.time_series.append(self.height.copy())

    def run_simulation(self, steps: int = 1000) -> np.ndarray:
        """
        runs the whole KPZ protocol fr fr
        returns: height evolution through quantum chaos
        """
        print("initiating KPZ dynamics no cap")
        for step in range(steps):
            self.evolve()
            if step % 100 == 0:
                print(f"step {step}: quantum chaos amplitude = {np.std(self.height):.3f}")
        
        return np.array(self.time_series)

    def visualize_evolution(self) -> None:
        """
        shows KPZ dynamics in real time no cap
        plots that quantum biological gaming
        """
        evolution = np.array(self.time_series)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(
            evolution.T,
            aspect='auto',
            cmap='plasma',  # absolutely based colormap fr fr
            extent=[0, len(evolution), 0, self.size]
        )
        plt.colorbar(label='Height (quantum units)')
        plt.xlabel('Time Steps')
        plt.ylabel('Spatial Position')
        plt.title('KPZ Quantum Coherence Evolution (real)')
        plt.show()

        # plot final height profile
        plt.figure(figsize=(10, 4))
        plt.plot(self.height, label='Final Height Profile')
        plt.xlabel('Position')
        plt.ylabel('Height')
        plt.title('Final KPZ Quantum State (no cap)')
        plt.grid(True)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    # init that KPZ middleware fr fr
    params = KPZParams(
        nu=0.1,
        lambda_=0.5,
        noise_strength=1.0,
        dt=0.01
    )
    
    kpz = KPZCoherenceManager(size=100, params=params)
    
    # run quantum biological simulation (real)
    kpz.run_simulation(steps=1000)
    
    # visualize that quantum chaos
    kpz.visualize_evolution()
    
    print("KPZ coherence successfully managed fr fr")
    print(f"final roughness: {np.std(kpz.height):.3f}")
    print(f"quantum chaos level: {np.max(np.abs(np.gradient(kpz.height))):.3f}")
