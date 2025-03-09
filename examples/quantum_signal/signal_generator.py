"""
Signal Generator Module

Provides functions for generating test signals for quantum signal processing demos.
"""

import numpy as np
from typing import Tuple, List, Optional


def generate_test_signal(
    length: int = 1000, 
    num_components: int = 5,
    noise_level: float = 0.1
) -> np.ndarray:
    """
    Generate a test signal with multiple frequency components and noise.
    
    Args:
        length: Signal length
        num_components: Number of frequency components
        noise_level: Amplitude of noise relative to signal
    
    Returns:
        Test signal array
    """
    t = np.linspace(0, 1, length)
    signal = np.zeros(length)
    
    # Add frequency components
    for i in range(num_components):
        freq = (i + 1) * 5
        amp = 1.0 / (i + 1)
        signal += amp * np.sin(2 * np.pi * freq * t)
    
    # Normalize
    signal /= np.max(np.abs(signal))
    
    # Add noise
    noise = np.random.normal(0, noise_level, length)
    noisy_signal = signal + noise
    
    return noisy_signal


def generate_chirp_signal(
    length: int = 1000,
    start_freq: float = 5.0,
    end_freq: float = 50.0,
    noise_level: float = 0.1
) -> np.ndarray:
    """
    Generate a chirp signal with increasing frequency.
    
    Args:
        length: Signal length
        start_freq: Starting frequency
        end_freq: Ending frequency
        noise_level: Amplitude of noise relative to signal
    
    Returns:
        Chirp signal array
    """
    t = np.linspace(0, 1, length)
    
    # Linear frequency sweep
    freq = start_freq + (end_freq - start_freq) * t
    
    # Generate chirp
    signal = np.sin(2 * np.pi * freq * t)
    
    # Normalize
    signal /= np.max(np.abs(signal))
    
    # Add noise
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, length)
        signal += noise
    
    return signal


def generate_amplitude_modulated_signal(
    length: int = 1000,
    carrier_freq: float = 40.0,
    modulation_freq: float = 5.0,
    modulation_index: float = 0.8,
    noise_level: float = 0.1
) -> np.ndarray:
    """
    Generate an amplitude-modulated signal.
    
    Args:
        length: Signal length
        carrier_freq: Carrier frequency
        modulation_freq: Modulation frequency
        modulation_index: Modulation index (0-1)
        noise_level: Amplitude of noise relative to signal
    
    Returns:
        AM signal array
    """
    t = np.linspace(0, 1, length)
    
    # Generate modulation
    modulation = 1 + modulation_index * np.sin(2 * np.pi * modulation_freq * t)
    
    # Generate carrier
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    
    # Multiply to get AM signal
    signal = modulation * carrier
    
    # Normalize
    signal /= np.max(np.abs(signal))
    
    # Add noise
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, length)
        signal += noise
    
    return signal


def generate_pulsed_signal(
    length: int = 1000,
    num_pulses: int = 5,
    pulse_width: int = 50,
    base_freq: float = 20.0,
    noise_level: float = 0.1
) -> np.ndarray:
    """
    Generate a signal with multiple pulses.
    
    Args:
        length: Signal length
        num_pulses: Number of pulses
        pulse_width: Width of each pulse
        base_freq: Base frequency for pulse content
        noise_level: Amplitude of noise relative to signal
    
    Returns:
        Pulsed signal array
    """
    t = np.linspace(0, 1, length)
    signal = np.zeros(length)
    
    # Create pulses
    for i in range(num_pulses):
        # Pulse center position
        pos = int((i + 0.5) * length / num_pulses)
        
        # Pulse start and end
        start = max(0, pos - pulse_width // 2)
        end = min(length, pos + pulse_width // 2)
        
        # Create window (smooth edges)
        window = np.zeros(length)
        window[start:end] = np.hanning(end - start)
        
        # Create pulse content
        freq = base_freq * (i + 1) / num_pulses
        pulse_content = np.sin(2 * np.pi * freq * t)
        
        # Add windowed pulse to signal
        signal += window * pulse_content
    
    # Normalize
    signal /= np.max(np.abs(signal))
    
    # Add noise
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, length)
        signal += noise
    
    return signal


def generate_multiband_signal(
    length: int = 1000,
    bands: List[Tuple[float, float, float]] = None,  # (center_freq, bandwidth, amplitude)
    noise_level: float = 0.1
) -> np.ndarray:
    """
    Generate a signal with multiple frequency bands.
    
    Args:
        length: Signal length
        bands: List of (center_freq, bandwidth, amplitude) tuples
        noise_level: Amplitude of noise relative to signal
    
    Returns:
        Multiband signal array
    """
    if bands is None:
        # Default bands: (center_freq, bandwidth, amplitude)
        bands = [
            (10.0, 5.0, 1.0),    # Low frequency band
            (30.0, 10.0, 0.7),   # Mid frequency band
            (70.0, 20.0, 0.4)    # High frequency band
        ]
    
    t = np.linspace(0, 1, length)
    signal = np.zeros(length)
    
    # Generate each band
    for center_freq, bandwidth, amplitude in bands:
        # Generate band-limited signal
        num_components = int(bandwidth)
        band_signal = np.zeros(length)
        
        for i in range(num_components):
            freq = center_freq - bandwidth/2 + i * bandwidth / (num_components-1)
            phase = np.random.uniform(0, 2*np.pi)
            band_signal += np.sin(2 * np.pi * freq * t + phase)
        
        # Normalize and scale by amplitude
        band_signal *= amplitude / np.max(np.abs(band_signal))
        
        # Add to total signal
        signal += band_signal
    
    # Normalize
    signal /= np.max(np.abs(signal))
    
    # Add noise
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, length)
        signal += noise
    
    return signal
