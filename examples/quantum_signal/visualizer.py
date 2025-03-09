"""
Visualization Module

Provides functions for visualizing quantum signal processing results.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, List, Tuple, Optional
import os


def plot_signal_comparison(
    original_signal: np.ndarray,
    processed_signal: np.ndarray,
    time_values: Optional[np.ndarray] = None,
    title: str = "Signal Comparison",
    labels: Tuple[str, str] = ("Original", "Processed"),
    fig_size: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> Figure:
    """
    Plot a comparison between original and processed signals.
    
    Args:
        original_signal: Original signal array
        processed_signal: Processed signal array
        time_values: Time values for x-axis (default: None, uses indices)
        title: Plot title
        labels: Tuple of (original_label, processed_label)
        fig_size: Figure size in inches
        save_path: Path to save figure (default: None, display only)
    
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=fig_size)
    
    # Create x-axis values
    if time_values is None:
        time_values = np.arange(len(original_signal))
    
    # Plot signals
    ax.plot(time_values, original_signal, 'b-', alpha=0.6, label=labels[0])
    ax.plot(time_values, processed_signal, 'r-', label=labels[1])
    
    # Add labels and title
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Save or show
    if save_path:
        plt.savefig(save_path)
    
    return fig


def plot_coefficient_spectrum(
    coefficients: np.ndarray,
    title: str = "Quantum Basis Coefficients",
    fig_size: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> Figure:
    """
    Plot the spectrum of quantum basis coefficients.
    
    Args:
        coefficients: Array of complex coefficients
        title: Plot title
        fig_size: Figure size in inches
        save_path: Path to save figure (default: None, display only)
    
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=fig_size)
    
    # Get coefficient magnitudes
    magnitudes = np.abs(coefficients)
    
    # Plot as bar chart
    ax.bar(range(len(coefficients)), magnitudes, alpha=0.7)
    
    # Add labels and title
    ax.set_title(title)
    ax.set_xlabel('Basis Function Index')
    ax.set_ylabel('Coefficient Magnitude')
    ax.grid(True, alpha=0.3)
    
    # Save or show
    if save_path:
        plt.savefig(save_path)
    
    return fig


def plot_processing_results(
    original_signal: np.ndarray,
    denoised_signal: np.ndarray,
    compressed_signal: np.ndarray,
    coefficients: np.ndarray,
    time_values: Optional[np.ndarray] = None,
    title: str = "Quantum Signal Processing Results",
    fig_size: Tuple[int, int] = (12, 10),
    save_path: Optional[str] = None
) -> Figure:
    """
    Plot comprehensive quantum signal processing results.
    
    Args:
        original_signal: Original signal array
        denoised_signal: Denoised signal array
        compressed_signal: Compressed/decompressed signal array
        coefficients: Array of quantum basis coefficients
        time_values: Time values for x-axis (default: None, uses indices)
        title: Plot title
        fig_size: Figure size in inches
        save_path: Path to save figure (default: None, display only)
    
    Returns:
        matplotlib Figure object
    """
    fig = plt.figure(figsize=fig_size)
    fig.suptitle(title, fontsize=16)
    
    # Create x-axis values
    if time_values is None:
        time_values = np.arange(len(original_signal))
    
    # Original and denoised signals
    ax1 = fig.add_subplot(3, 1, 1)
    ax1.plot(time_values, original_signal, 'b-', alpha=0.6, label='Original')
    ax1.plot(time_values, denoised_signal, 'r-', label='Denoised')
    ax1.set_title('Signal Denoising')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Compressed signal
    ax2 = fig.add_subplot(3, 1, 2)
    ax2.plot(time_values, original_signal, 'b-', alpha=0.6, label='Original')
    ax2.plot(time_values, compressed_signal, 'g-', label='Compressed/Decompressed')
    ax2.set_title('Signal Compression')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Amplitude')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Quantum coefficients
    ax3 = fig.add_subplot(3, 1, 3)
    ax3.bar(range(len(coefficients)), np.abs(coefficients), alpha=0.7)
    ax3.set_title('Quantum Basis Coefficients')
    ax3.set_xlabel('Basis Function Index')
    ax3.set_ylabel('Coefficient Magnitude')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust for suptitle
    
    # Save or show
    if save_path:
        plt.savefig(save_path)
    
    return fig


def plot_spectral_statistics(
    stats: Dict[str, float],
    title: str = "Quantum Spectral Statistics",
    fig_size: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> Figure:
    """
    Plot quantum spectral statistics.
    
    Args:
        stats: Dictionary of spectral statistics
        title: Plot title
        fig_size: Figure size in inches
        save_path: Path to save figure (default: None, display only)
    
    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=fig_size)
    
    # Extract keys and values
    keys = list(stats.keys())
    values = [stats[key] for key in keys]
    
    # Create horizontal bar chart
    y_pos = np.arange(len(keys))
    ax.barh(y_pos, values, alpha=0.7)
    
    # Add labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(keys)
    ax.invert_yaxis()  # Labels read top-to-bottom
    
    # Add title and labels
    ax.set_title(title)
    ax.set_xlabel('Value')
    
    # Add value labels
    for i, v in enumerate(values):
        ax.text(v + 0.01, i, f"{v:.4f}", va='center')
    
    # Save or show
    if save_path:
        plt.savefig(save_path)
    
    return fig
