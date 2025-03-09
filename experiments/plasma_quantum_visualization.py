#!/usr/bin/env python3
"""
Plasma Quantum Visualization

This script creates a visualization of plasma-based quantum fields,
demonstrating the concepts discussed in the quantum ghost manuscripts.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as colors
from scipy.ndimage import gaussian_filter
import argparse

class PlasmaQuantumVisualization:
    """
    Visualizes plasma-based quantum fields using KPZ dynamics and
    quantum resonance patterns.
    """
    
    def __init__(self, size=100, kpz_lambda=1.0, kpz_nu=0.3, noise_scale=0.02):
        """
        Initialize the plasma quantum visualization.
        
        Args:
            size: Grid size (default: 100)
            kpz_lambda: KPZ nonlinearity parameter (default: 1.0)
            kpz_nu: KPZ viscosity parameter (default: 0.3)
            noise_scale: Scale of quantum noise (default: 0.02)
        """
        self.size = size
        self.kpz_lambda = kpz_lambda
        self.kpz_nu = kpz_nu
        self.noise_scale = noise_scale
        
        # Initialize quantum field
        self.quantum_field = np.random.randn(size, size) * 0.1
        
        # Initialize plasma vortex centers
        self.vortex_centers = []
        self.add_vortices(5)
        
        # Initialize figure and axes
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.suptitle('Plasma Quantum Consciousness Visualization', fontsize=16)
        
        # Custom colormap
        colors_list = [(0, 'darkblue'), (0.4, 'blue'), 
                       (0.6, 'purple'), (0.8, 'red'), (1, 'yellow')]
        self.cmap = colors.LinearSegmentedColormap.from_list('plasma_quantum', colors_list)
        
        # Setup plot
        self.img = self.ax.imshow(
            self.quantum_field, 
            cmap=self.cmap,
            interpolation='bicubic',
            vmin=-1, vmax=1
        )
        self.cbar = self.fig.colorbar(self.img, ax=self.ax)
        self.cbar.set_label('Quantum Field Intensity')
        self.ax.set_title('Iteration: 0')
        self.ax.axis('off')
        
        # Parameter display
        self.param_text = self.fig.text(
            0.02, 0.02, 
            f"λ: {self.kpz_lambda:.3f}, ν: {self.kpz_nu:.3f}, Noise: {self.noise_scale:.3f}",
            ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.7)
        )
        
        # Iteration counter
        self.iteration = 0
    
    def add_vortices(self, num_vortices):
        """Add plasma vortex centers to the field."""
        for _ in range(num_vortices):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            strength = np.random.uniform(0.5, 1.5)
            rotation = np.random.choice([-1, 1])
            self.vortex_centers.append((x, y, strength, rotation))
    
    def apply_vortex_field(self):
        """Apply plasma vortex dynamics to the quantum field."""
        vortex_field = np.zeros((self.size, self.size))
        x_grid, y_grid = np.meshgrid(range(self.size), range(self.size))
        
        for x, y, strength, rotation in self.vortex_centers:
            # Distance from vortex center
            r = np.sqrt((x_grid - x)**2 + (y_grid - y)**2)
            # Avoid division by zero
            r = np.maximum(r, 0.1)
            # Vortex field (decreases with distance)
            vortex = strength * np.exp(-r / 20) * np.sin(r / 2) * rotation
            vortex_field += vortex
        
        # Apply vortex field
        self.quantum_field += vortex_field * 0.05
    
    def apply_kpz_dynamics(self):
        """Apply KPZ dynamics to the quantum field."""
        # Compute spatial derivatives
        dx = np.roll(self.quantum_field, -1, axis=1) - self.quantum_field
        dy = np.roll(self.quantum_field, -1, axis=0) - self.quantum_field
        
        # Nonlinear term: (∇h)²
        nonlinear_term = self.kpz_lambda * (dx**2 + dy**2)
        
        # Diffusion term: ∇²h
        laplacian = (
            np.roll(self.quantum_field, 1, axis=0) +
            np.roll(self.quantum_field, -1, axis=0) +
            np.roll(self.quantum_field, 1, axis=1) +
            np.roll(self.quantum_field, -1, axis=1) -
            4 * self.quantum_field
        )
        diffusion_term = self.kpz_nu * laplacian
        
        # Quantum noise
        eta = np.random.normal(0, self.noise_scale, (self.size, self.size))
        
        # Update field
        self.quantum_field += diffusion_term + nonlinear_term + eta
        
        # Apply coherence-preserving smoothing
        self.quantum_field = gaussian_filter(self.quantum_field, sigma=0.5)
        
        # Enforce boundary conditions
        self.quantum_field = np.clip(self.quantum_field, -2, 2)
    
    def update_plot(self, frame):
        """Update the visualization for animation."""
        # Move vortex centers
        for i, (x, y, strength, rotation) in enumerate(self.vortex_centers):
            dx = np.random.randint(-1, 2)
            dy = np.random.randint(-1, 2)
            new_x = (x + dx) % self.size
            new_y = (y + dy) % self.size
            self.vortex_centers[i] = (new_x, new_y, strength, rotation)
        
        # Apply dynamics
        self.apply_vortex_field()
        self.apply_kpz_dynamics()
        
        # Occasionally add or remove vortices
        if np.random.random() < 0.02:  # 2% chance
            if np.random.random() < 0.5 and len(self.vortex_centers) > 3:
                # Remove a vortex
                idx = np.random.randint(0, len(self.vortex_centers))
                self.vortex_centers.pop(idx)
            else:
                # Add a vortex
                self.add_vortices(1)
        
        # Occasionally adjust parameters
        if np.random.random() < 0.05:  # 5% chance
            self.kpz_lambda += np.random.normal(0, 0.05)
            self.kpz_lambda = np.clip(self.kpz_lambda, 0.1, 2.0)
            
            self.kpz_nu += np.random.normal(0, 0.02)
            self.kpz_nu = np.clip(self.kpz_nu, 0.1, 0.5)
            
            self.noise_scale += np.random.normal(0, 0.002)
            self.noise_scale = np.clip(self.noise_scale, 0.001, 0.05)
            
            # Update parameter display
            self.param_text.set_text(
                f"λ: {self.kpz_lambda:.3f}, ν: {self.kpz_nu:.3f}, Noise: {self.noise_scale:.3f}"
            )
        
        # Update plot
        self.img.set_array(self.quantum_field)
        self.ax.set_title(f'Iteration: {self.iteration}')
        self.iteration += 1
        
        return [self.img]

    def animate(self, frames=200, interval=50):
        """Animate the plasma quantum visualization."""
        self.anim = FuncAnimation(
            self.fig, self.update_plot, frames=frames,
            interval=interval, blit=True
        )
        plt.tight_layout()
        plt.show()
    
    def save_animation(self, filename='plasma_quantum.mp4', fps=20):
        """Save the animation to a file."""
        print(f"Saving animation to {filename}...")
        self.anim = FuncAnimation(
            self.fig, self.update_plot, frames=100,
            interval=50, blit=True
        )
        self.anim.save(filename, fps=fps, extra_args=['-vcodec', 'libx264'])
        print(f"Animation saved to {filename}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Plasma Quantum Visualization")
    parser.add_argument(
        "--size", type=int, default=100,
        help="Grid size (default: 100)"
    )
    parser.add_argument(
        "--lambda", dest="kpz_lambda", type=float, default=1.0,
        help="KPZ nonlinearity parameter (default: 1.0)"
    )
    parser.add_argument(
        "--nu", type=float, default=0.3,
        help="KPZ viscosity parameter (default: 0.3)"
    )
    parser.add_argument(
        "--noise", type=float, default=0.02,
        help="Quantum noise scale (default: 0.02)"
    )
    parser.add_argument(
        "--frames", type=int, default=200,
        help="Number of animation frames (default: 200)"
    )
    parser.add_argument(
        "--interval", type=int, default=50,
        help="Animation interval in milliseconds (default: 50)"
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save animation to file"
    )
    parser.add_argument(
        "--output", type=str, default="plasma_quantum.mp4",
        help="Output filename (default: plasma_quantum.mp4)"
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    print("Initializing Plasma Quantum Visualization...")
    viz = PlasmaQuantumVisualization(
        size=args.size,
        kpz_lambda=args.kpz_lambda,
        kpz_nu=args.nu,
        noise_scale=args.noise
    )
    
    if args.save:
        viz.save_animation(filename=args.output)
    else:
        print(f"Starting animation with {args.frames} frames...")
        viz.animate(frames=args.frames, interval=args.interval)


if __name__ == "__main__":
    print("Plasma Quantum Consciousness Visualization")
    print("------------------------------------------")
    print("This visualization demonstrates plasma-based quantum fields")
    print("with KPZ dynamics and quantum resonance patterns.")
    print()
    main()
