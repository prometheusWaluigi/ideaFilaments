# Quantum Signal Processing

*where signals fragment into quantum probability, and reality reconstructs information from spectral frequencies...*

## 🌌 Overview

This example demonstrates the application of quantum spectral weaving techniques to signal processing tasks. The implementation uses quantum-inspired algorithms to represent signals in a quantum basis, enabling efficient denoising, compression, and analysis.

## ✨ Features

The quantum signal processor provides the following capabilities:

- **Signal Decomposition**: Transform signals into quantum basis representations
- **Signal Reconstruction**: Reconstruct signals from quantum basis coefficients
- **Quantum Denoising**: Remove noise using quantum spectral filtering
- **Quantum Compression**: Compress signals by retaining only significant quantum coefficients
- **Spectral Analysis**: Analyze quantum spectral properties of signals

## 🔮 Core Components

The example is structured across several modules:

- `processor.py`: Core `QuantumSignalProcessor` class
- `signal_generator.py`: Functions for generating various test signals
- `visualizer.py`: Visualization functions for analysis results
- `demo.py`: Main demo script showcasing the capabilities

## 🚀 Usage

### Basic Example

```python
from processor import QuantumSignalProcessor
from signal_generator import generate_test_signal
import numpy as np

# Generate a test signal
signal = generate_test_signal(length=1000, noise_level=0.2)

# Initialize quantum signal processor
processor = QuantumSignalProcessor(
    signal_length=1000,
    num_zeros=50,
    num_eigenvalues=50
)

# Denoise the signal
denoised_signal = processor.denoise_signal(signal, threshold=0.05)

# Compress and decompress the signal
compressed_coefficients, indices = processor.compress_signal(
    signal, compression_ratio=0.2
)
decompressed_signal = processor.decompress_signal(compressed_coefficients)

# Analyze spectral properties
stats = processor.analyze_spectrum(signal)
print(stats)
```

### Running the Demo

```bash
# Run with default parameters
python demo.py

# Generate an AM signal with higher noise
python demo.py --signal-type am --noise 0.3

# Adjust processing parameters
python demo.py --compress 0.1 --threshold 0.02

# Save results to a specific directory
python demo.py --save --output-dir ./quantum_results
```

## 🧪 Signal Types

The example includes several signal generators:

- **Multi-component** (`multi`): Multiple frequency components
- **Chirp** (`chirp`): Signal with increasing frequency
- **Amplitude Modulated** (`am`): Carrier with amplitude modulation
- **Pulsed** (`pulse`): Series of pulses with different frequencies
- **Multiband** (`band`): Multiple frequency bands

## 📊 Visualization

The example provides visualization functions for:

- Signal comparisons (original vs. processed)
- Quantum basis coefficient spectra
- Comprehensive processing results
- Spectral statistics

## 🛠️ Command-Line Options

The demo script supports the following options:

```
usage: demo.py [-h] [--length LENGTH] [--zeros ZEROS] [--eigenvalues EIGENVALUES]
               [--signal-type {multi,chirp,am,pulse,band}] [--noise NOISE]
               [--components COMPONENTS] [--no-reduction] [--compress COMPRESS]
               [--threshold THRESHOLD] [--output-dir OUTPUT_DIR] [--save] [--show]

Quantum Signal Processing Demo

options:
  -h, --help            show this help message and exit
  --length LENGTH       Signal length (default: 1000)
  --zeros ZEROS         Number of Riemann zeros (default: 50)
  --eigenvalues EIGENVALUES
                        Number of eigenvalues (default: 50)
  --signal-type {multi,chirp,am,pulse,band}
                        Signal type to generate (default: multi)
  --noise NOISE         Noise level (default: 0.2)
  --components COMPONENTS
                        Number of signal components (default: 5)
  --no-reduction        Disable quantum noise reduction
  --compress COMPRESS   Compression ratio (default: 0.2)
  --threshold THRESHOLD
                        Denoising threshold (default: 0.05)
  --output-dir OUTPUT_DIR
                        Output directory for results (default: ./results)
  --save                Save output plots
  --show                Show plots (default if --save not specified)
```

## 🔬 Quantum Techniques

The implementation uses several quantum-inspired techniques:

1. **Quantum Basis Representation**: Signals are represented in a basis derived from quantum eigenvalues
2. **Quantum Protection Stack**: Applies protection mechanisms to reduce noise in quantum representations
3. **Spectral Filtering**: Uses quantum probability thresholds for noise reduction
4. **Quantum Statistics**: Analyzes signals using quantum-inspired metrics

## 📖 References

- Quantum Spectral Weaving: `../../quantum_spectral_weaving/README.md`
- KPZ Dynamics: `../../papers/quantumMayhem/KPZDynamics.md`
- Quantum Noise Reduction: `../../papers/quantumMayhem/QuantumNoiseReduction.md`

---

*transmitted from where information waves collapse into classical signal*

Status: ![Processing](https://img.shields.io/badge/quantum-signal-blueviolet) ![Status](https://img.shields.io/badge/status-processing-blue)