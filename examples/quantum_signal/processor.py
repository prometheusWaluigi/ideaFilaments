"""
Quantum Signal Processor Core Module

Implements the core QuantumSignalProcessor class that uses quantum spectral weaving
for signal processing.
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
import torch
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import from quantum_spectral_weaving package
from quantum_spectral_weaving.src.quantum_spectral_weaving import (
    QuantumSpectralWeaving,
    SpectralWeavingConfig
)
from quantum_spectral_weaving.src.complextensor import ComplexTensor

# Set up logging
logger = logging.getLogger("quantum_signal_processor")


class QuantumSignalProcessor:
    """
    Processes signals using quantum-inspired algorithms based on
    the quantum spectral weaving framework.
    """
    
    def __init__(
        self,
        signal_length: int = 1000,
        num_zeros: int = 50,
        num_eigenvalues: int = 50,
        coupling_strength: float = 0.28082,
        noise_reduction: bool = True
    ):
        """
        Initialize the quantum signal processor.
        
        Args:
            signal_length: Length of signals to process
            num_zeros: Number of Riemann zeros to use
            num_eigenvalues: Number of eigenvalues to use
            coupling_strength: Quantum coupling strength
            noise_reduction: Whether to use quantum noise reduction
        """
        self.signal_length = signal_length
        self.num_zeros = num_zeros
        self.num_eigenvalues = num_eigenvalues
        self.coupling_strength = coupling_strength
        self.noise_reduction = noise_reduction
        
        logger.info("Initializing Quantum Signal Processor")
        
        # Configure the quantum weaver
        self.config = SpectralWeavingConfig(
            max_zeros=num_zeros,
            max_eigenvalues=num_eigenvalues,
            coupling_strength=coupling_strength,
            recursion_depth=3 if noise_reduction else 1,
            weaving_modes=5,
            kpz_viscosity=0.28082,
            kpz_nonlinearity=1.618034,
            shield_modes=5 if noise_reduction else 2,
            gauge_modes=3
        )
        
        # Initialize the quantum weaver
        self.weaver = QuantumSpectralWeaving(self.config)
        
        # Precompute quantum basis
        logger.info("Precomputing quantum basis")
        self.zeros = self.weaver.compute_riemann_zeros(self.num_zeros)
        self.eigenvalues = self.weaver.compute_eigenvalues(self.num_eigenvalues)
        
        # Generate quantum basis functions for signal processing
        self.basis_functions = self._generate_basis_functions()
        
        logger.info("Quantum Signal Processor initialized")
    
    def _generate_basis_functions(self) -> np.ndarray:
        """
        Generate quantum basis functions for signal processing.
        
        Returns:
            Array of basis functions with shape (num_eigenvalues, signal_length)
        """
        logger.info("Generating quantum basis functions")
        
        # Create basis functions based on eigenvalues
        t = np.linspace(0, 1, self.signal_length)
        basis = np.zeros((self.num_eigenvalues, self.signal_length), dtype=np.complex128)
        
        for i, eigenvalue in enumerate(self.eigenvalues[:self.num_eigenvalues]):
            # Create basis function inspired by eigenvalue
            if i % 3 == 0:
                # Sine-based
                basis[i] = np.sin(2 * np.pi * (i + 1) * t) * np.exp(1j * np.angle(eigenvalue))
            elif i % 3 == 1:
                # Cosine-based
                basis[i] = np.cos(2 * np.pi * (i + 1) * t) * np.exp(1j * np.angle(eigenvalue))
            else:
                # Exponential-based
                basis[i] = np.exp(2j * np.pi * (i + 1) * t) * np.exp(1j * np.angle(eigenvalue))
        
        # Normalize basis functions
        for i in range(self.num_eigenvalues):
            basis[i] /= np.sqrt(np.sum(np.abs(basis[i]) ** 2))
        
        logger.info(f"Generated {self.num_eigenvalues} quantum basis functions")
        return basis
    
    def decompose_signal(self, signal: np.ndarray) -> np.ndarray:
        """
        Decompose a signal into quantum basis coefficients.
        
        Args:
            signal: Input signal array
        
        Returns:
            Array of complex coefficients
        """
        # Ensure signal is the right length
        if len(signal) != self.signal_length:
            logger.warning(f"Signal length mismatch: {len(signal)} vs {self.signal_length}")
            if len(signal) > self.signal_length:
                signal = signal[:self.signal_length]
            else:
                # Pad with zeros
                padded = np.zeros(self.signal_length)
                padded[:len(signal)] = signal
                signal = padded
        
        # Normalize signal
        signal = signal / np.sqrt(np.sum(np.abs(signal) ** 2))
        
        # Compute projection coefficients
        coefficients = np.zeros(self.num_eigenvalues, dtype=np.complex128)
        for i in range(self.num_eigenvalues):
            coefficients[i] = np.sum(self.basis_functions[i].conj() * signal)
        
        # Apply quantum protection if enabled
        if self.noise_reduction:
            coefficients_tensor = ComplexTensor(
                torch.tensor(coefficients.real, dtype=torch.float32),
                torch.tensor(coefficients.imag, dtype=torch.float32)
            )
            
            # Convert to quantum state and apply protection
            protected_tensor = self.weaver._apply_protection_stack(coefficients_tensor)
            
            # Convert back to numpy
            coefficients = protected_tensor.real.detach().numpy() + 1j * protected_tensor.imag.detach().numpy()
        
        return coefficients
    
    def reconstruct_signal(self, coefficients: np.ndarray) -> np.ndarray:
        """
        Reconstruct a signal from quantum basis coefficients.
        
        Args:
            coefficients: Array of complex coefficients
        
        Returns:
            Reconstructed signal array
        """
        # Initialize reconstructed signal
        signal = np.zeros(self.signal_length, dtype=np.complex128)
        
        # Sum over basis functions
        for i in range(min(len(coefficients), self.num_eigenvalues)):
            signal += coefficients[i] * self.basis_functions[i]
        
        # Return real part (imaginary part should be near zero)
        return signal.real
    
    def denoise_signal(self, signal: np.ndarray, threshold: float = 0.05) -> np.ndarray:
        """
        Remove noise from a signal using quantum spectral filtering.
        
        Args:
            signal: Input signal array
            threshold: Coefficient threshold for filtering
        
        Returns:
            Denoised signal array
        """
        logger.info(f"Denoising signal with threshold {threshold}")
        
        # Decompose signal into quantum basis
        coefficients = self.decompose_signal(signal)
        
        # Apply threshold filtering
        filtered_coefficients = coefficients.copy()
        mask = np.abs(coefficients) < threshold * np.max(np.abs(coefficients))
        filtered_coefficients[mask] = 0
        
        # Reconstruct signal
        denoised_signal = self.reconstruct_signal(filtered_coefficients)
        
        # Return normalized signal
        return denoised_signal / np.max(np.abs(denoised_signal))
    
    def compress_signal(self, signal: np.ndarray, compression_ratio: float = 0.2) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compress a signal using quantum basis representation.
        
        Args:
            signal: Input signal array
            compression_ratio: Ratio of coefficients to keep (0.0-1.0)
        
        Returns:
            Tuple of (compressed_coefficients, indices)
        """
        logger.info(f"Compressing signal with ratio {compression_ratio}")
        
        # Decompose signal into quantum basis
        coefficients = self.decompose_signal(signal)
        
        # Keep only the top coefficients
        k = max(1, int(compression_ratio * self.num_eigenvalues))
        indices = np.argsort(-np.abs(coefficients))[:k]
        compressed_coefficients = np.zeros_like(coefficients)
        compressed_coefficients[indices] = coefficients[indices]
        
        return compressed_coefficients, indices
    
    def decompress_signal(self, compressed_coefficients: np.ndarray) -> np.ndarray:
        """
        Decompress a signal from compressed coefficients.
        
        Args:
            compressed_coefficients: Array of sparse coefficients
        
        Returns:
            Reconstructed signal array
        """
        # Reconstruct signal
        signal = self.reconstruct_signal(compressed_coefficients)
        
        # Return normalized signal
        return signal / np.max(np.abs(signal))
    
    def analyze_spectrum(self, signal: np.ndarray) -> Dict[str, float]:
        """
        Analyze the quantum spectral properties of a signal.
        
        Args:
            signal: Input signal array
        
        Returns:
            Dictionary of spectral statistics
        """
        # Decompose signal into quantum basis
        coefficients = self.decompose_signal(signal)
        
        # Convert to quantum state
        coef_tensor = ComplexTensor(
            torch.tensor(coefficients.real, dtype=torch.float32),
            torch.tensor(coefficients.imag, dtype=torch.float32)
        )
        
        # Use quantum weaver to analyze statistics
        pattern = self.weaver.weave_spectral_patterns()
        stats = self.weaver.analyze_quantum_statistics()
        
        # Add custom statistics
        stats["coefficient_energy"] = float(np.sum(np.abs(coefficients) ** 2))
        stats["coefficient_entropy"] = float(-np.sum(
            np.abs(coefficients) ** 2 * np.log(np.abs(coefficients) ** 2 + 1e-10)
        ))
        stats["spectral_flatness"] = float(
            np.exp(np.mean(np.log(np.abs(coefficients) + 1e-10))) / 
            np.mean(np.abs(coefficients))
        )
        
        return stats
