#!/usr/bin/env python3
"""
Quantum Signal Processing Demo

This script demonstrates the application of quantum spectral weaving techniques
for signal processing tasks like denoising, compression, and analysis.
"""

import argparse
import logging
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("quantum_signal_demo")

# Import modules
from processor import QuantumSignalProcessor
from signal_generator import (
    generate_test_signal,
    generate_chirp_signal,
    generate_amplitude_modulated_signal,
    generate_pulsed_signal,
    generate_multiband_signal
)
from visualizer import (
    plot_signal_comparison,
    plot_coefficient_spectrum,
    plot_processing_results,
    plot_spectral_statistics
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Quantum Signal Processing Demo")
    
    # Basic parameters
    parser.add_argument(
        "--length", type=int, default=1000,
        help="Signal length (default: 1000)"
    )
    parser.add_argument(
        "--zeros", type=int, default=50,
        help="Number of Riemann zeros (default: 50)"
    )
    parser.add_argument(
        "--eigenvalues", type=int, default=50,
        help="Number of eigenvalues (default: 50)"
    )
    
    # Signal generation parameters
    parser.add_argument(
        "--signal-type", type=str, default="multi",
        choices=["multi", "chirp", "am", "pulse", "band"],
        help="Signal type to generate (default: multi)"
    )
    parser.add_argument(
        "--noise", type=float, default=0.2,
        help="Noise level (default: 0.2)"
    )
    parser.add_argument(
        "--components", type=int, default=5,
        help="Number of signal components (default: 5)"
    )
    
    # Processing parameters
    parser.add_argument(
        "--no-reduction", action="store_true",
        help="Disable quantum noise reduction"
    )
    parser.add_argument(
        "--compress", type=float, default=0.2,
        help="Compression ratio (default: 0.2)"
    )
    parser.add_argument(
        "--threshold", type=float, default=0.05,
        help="Denoising threshold (default: 0.05)"
    )
    
    # Output parameters
    parser.add_argument(
        "--output-dir", type=str, default="./results",
        help="Output directory for results (default: ./results)"
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save output plots"
    )
    parser.add_argument(
        "--show", action="store_true",
        help="Show plots (default if --save not specified)"
    )
    
    args = parser.parse_args()
    
    # If neither --save nor --show is specified, default to --show
    if not args.save and not args.show:
        args.show = True
    
    return args


def generate_signal(args: argparse.Namespace) -> np.ndarray:
    """Generate a test signal based on command-line arguments."""
    logger.info(f"Generating {args.signal_type} signal")
    
    if args.signal_type == "multi":
        return generate_test_signal(
            length=args.length,
            num_components=args.components,
            noise_level=args.noise
        )
    elif args.signal_type == "chirp":
        return generate_chirp_signal(
            length=args.length,
            start_freq=5.0,
            end_freq=50.0,
            noise_level=args.noise
        )
    elif args.signal_type == "am":
        return generate_amplitude_modulated_signal(
            length=args.length,
            carrier_freq=40.0,
            modulation_freq=5.0,
            noise_level=args.noise
        )
    elif args.signal_type == "pulse":
        return generate_pulsed_signal(
            length=args.length,
            num_pulses=args.components,
            noise_level=args.noise
        )
    elif args.signal_type == "band":
        return generate_multiband_signal(
            length=args.length,
            noise_level=args.noise
        )
    else:
        raise ValueError(f"Unknown signal type: {args.signal_type}")


def save_results(
    stats: Dict[str, float],
    output_dir: str,
    prefix: str = "quantum_signal"
) -> None:
    """Save processing results to text file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save statistics
    stats_file = os.path.join(output_dir, f"{prefix}_stats.txt")
    with open(stats_file, "w") as f:
        f.write("Quantum Spectral Analysis:\n")
        for key, value in stats.items():
            f.write(f"{key}: {value:.6f}\n")
    
    logger.info(f"Statistics saved to {stats_file}")


def main() -> None:
    """Main demo function."""
    args = parse_args()
    
    # Create output directory if saving
    if args.save and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Generate test signal
    signal = generate_signal(args)
    
    # Create time values
    time_values = np.linspace(0, 1, args.length)
    
    # Initialize quantum signal processor
    processor = QuantumSignalProcessor(
        signal_length=args.length,
        num_zeros=args.zeros,
        num_eigenvalues=args.eigenvalues,
        noise_reduction=not args.no_reduction
    )
    
    # Process signal
    logger.info("Processing signal")
    
    # Denoise signal
    denoised_signal = processor.denoise_signal(signal, threshold=args.threshold)
    
    # Compress and decompress signal
    compressed_coefficients, indices = processor.compress_signal(
        signal, compression_ratio=args.compress
    )
    compressed_signal = processor.decompress_signal(compressed_coefficients)
    
    # Get coefficients for visualization
    coefficients = processor.decompose_signal(signal)
    
    # Analyze spectrum
    stats = processor.analyze_spectrum(signal)
    
    # Plot results
    logger.info("Generating visualizations")
    
    # Create comprehensive plot
    fig = plot_processing_results(
        original_signal=signal,
        denoised_signal=denoised_signal,
        compressed_signal=compressed_signal,
        coefficients=coefficients,
        time_values=time_values,
        title=f"Quantum Signal Processing: {args.signal_type.upper()} Signal",
        save_path=os.path.join(args.output_dir, "processing_results.png") if args.save else None
    )
    
    # Create statistics plot
    stats_fig = plot_spectral_statistics(
        stats=stats,
        title="Quantum Spectral Analysis",
        save_path=os.path.join(args.output_dir, "spectral_stats.png") if args.save else None
    )
    
    # Print statistics to console
    print("\nQuantum Spectral Analysis:")
    for key, value in stats.items():
        print(f"  {key}: {value:.6f}")
    
    # Save results
    if args.save:
        save_results(stats, args.output_dir)
        logger.info(f"Results saved to {args.output_dir}")
    
    # Show plots if requested
    if args.show:
        plt.show()
    

if __name__ == "__main__":
    print("\nQuantum Signal Processing Demo")
    print("-----------------------------")
    print("Using quantum spectral weaving for signal processing")
    print()
    
    try:
        main()
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
