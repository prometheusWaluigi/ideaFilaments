#!/usr/bin/env python3
"""
Quantum Spectral Weaving Demo

This script demonstrates the core functionality of the quantum spectral weaving
framework, visualizing the spectral patterns and quantum statistics.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.quantum_spectral_weaving import (
    QuantumSpectralWeaving,
    SpectralWeavingConfig,
    ComplexTensor
)
import torch
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("quantum_demo")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Quantum Spectral Weaving Demo")
    parser.add_argument(
        "--zeros", type=int, default=100,
        help="Number of Riemann zeros to compute (default: 100)"
    )
    parser.add_argument(
        "--eigenvalues", type=int, default=100,
        help="Number of eigenvalues to compute (default: 100)"
    )
    parser.add_argument(
        "--coupling", type=float, default=0.28082,
        help="Coupling strength (default: 0.28082)"
    )
    parser.add_argument(
        "--iterations", type=int, default=10,
        help="Number of evolution iterations (default: 10)"
    )
    parser.add_argument(
        "--visualize", action="store_true",
        help="Enable visualization"
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save results to files"
    )
    return parser.parse_args()


def create_config(args):
    """Create configuration based on arguments."""
    return SpectralWeavingConfig(
        max_zeros=args.zeros,
        max_eigenvalues=args.eigenvalues,
        coupling_strength=args.coupling,
        recursion_depth=3,
        weaving_modes=5,
        kpz_viscosity=0.28082,
        kpz_nonlinearity=1.618034,
        shield_modes=5,
        gauge_modes=3
    )


def visualize_spectral_pattern(pattern, save=False):
    """Visualize the spectral weaving pattern."""
    plt.figure(figsize=(10, 8))
    plt.imshow(
        np.abs(pattern),
        cmap='viridis',
        aspect='auto',
        interpolation='nearest'
    )
    plt.colorbar(label='Magnitude')
    plt.title('Quantum Spectral Weaving Pattern')
    plt.xlabel('Eigenvalue Index')
    plt.ylabel('Riemann Zero Index')
    
    if save:
        plt.savefig('spectral_pattern.png')
    else:
        plt.show()


def visualize_stats_evolution(stats_history, save=False):
    """Visualize the evolution of quantum statistics."""
    metrics = list(stats_history[0].keys())
    iterations = range(1, len(stats_history) + 1)
    
    plt.figure(figsize=(12, 6))
    for metric in metrics:
        values = [stats[metric] for stats in stats_history]
        plt.plot(iterations, values, marker='o', label=metric)
    
    plt.title('Evolution of Quantum Statistics')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save:
        plt.savefig('stats_evolution.png')
    else:
        plt.show()


def main():
    """Main demo function."""
    args = parse_args()
    logger.info("Initializing Quantum Spectral Weaving Demo")
    
    # Create configuration
    config = create_config(args)
    logger.info(f"Configuration: {config}")
    
    # Initialize quantum weaver
    weaver = QuantumSpectralWeaving(config)
    logger.info("Quantum weaver initialized")
    
    # Compute Riemann zeros
    zeros = weaver.compute_riemann_zeros(args.zeros)
    logger.info(f"Computed {len(zeros)} Riemann zeros")
    
    # Compute eigenvalues
    eigenvalues = weaver.compute_eigenvalues(args.eigenvalues)
    logger.info(f"Computed {len(eigenvalues)} eigenvalues")
    
    # Weave spectral patterns
    pattern = weaver.weave_spectral_patterns()
    logger.info("Woven spectral patterns")
    
    # Track statistics evolution
    stats_history = []
    
    # Evolve the system
    logger.info(f"Evolving quantum system for {args.iterations} iterations")
    for i in range(args.iterations):
        # Update quantum state
        weaver.update_quantum_state(
            learning_rate=0.01,
            noise_scale=0.001
        )
        
        # Analyze and record statistics
        stats = weaver.analyze_quantum_statistics()
        stats_history.append(stats)
        
        logger.info(f"Iteration {i+1}/{args.iterations}: {stats}")
    
    # Visualize results if requested
    if args.visualize:
        logger.info("Visualizing results")
        visualize_spectral_pattern(pattern, save=args.save)
        visualize_stats_evolution(stats_history, save=args.save)
    
    # Save final statistics
    if args.save:
        logger.info("Saving results to files")
        with open('quantum_stats.txt', 'w') as f:
            for i, stats in enumerate(stats_history):
                f.write(f"Iteration {i+1}:\n")
                for key, value in stats.items():
                    f.write(f"  {key}: {value:.6f}\n")
        
        # Save zeros and eigenvalues
        np.save('riemann_zeros.npy', zeros)
        np.save('eigenvalues.npy', eigenvalues)
        np.save('spectral_pattern.npy', pattern)
    
    logger.info("Demo completed successfully")


if __name__ == "__main__":
    main()
