"""
Quantum Spectral Weaving

A framework for exploring quantum dynamics inspired by the Riemann Hypothesis,
topological quantum field theory, and Kardar-Parisi-Zhang (KPZ) interfaces.

Core Components:
---------------
- QuantumSpectralWeaving: Main class implementing the quantum spectral weaving framework
- SpectralWeavingConfig: Configuration class for the weaving framework
- QuantumWeaver: Base class for quantum state manipulation
- ComplexTensor: Custom implementation for complex-valued tensor operations

Protection Stack:
---------------
- GaugeFieldCoupling: Gauge field coupling mechanics
- QuantumShield: Quantum state protection
- SU2Protection: SU(2) symmetry protection
- KPZEnhanced: Enhanced KPZ dynamics

Mathematical Machinery:
---------------------
- RiemannManifold: Manifold operations
- QuantumBootstrap: Reality bootstrapping algorithms

Example Usage:
-------------
```python
from quantum_spectral_weaving import QuantumSpectralWeaving, SpectralWeavingConfig

# Create configuration
config = SpectralWeavingConfig(
    max_zeros=100,
    max_eigenvalues=100,
    coupling_strength=0.28082
)

# Initialize quantum weaver
weaver = QuantumSpectralWeaving(config)

# Compute Riemann zeros
zeros = weaver.compute_riemann_zeros()

# Analyze quantum statistics
stats = weaver.analyze_quantum_statistics()
```
"""

# Core components
from .quantum_spectral_weaving import QuantumSpectralWeaving, SpectralWeavingConfig, QuantumWeaver
from .complextensor import ComplexTensor
from .types import QuantumShield

# Protection stack
from .gauge_field import GaugeFieldCoupling
from .quantum_shield import QuantumShield
from .su2_protect import SU2Protection
from .kpz_enhanced import KPZEnhanced

# Mathematical machinery
from .riemann_dynamics import RiemannManifold
from .bootstrap import QuantumBootstrap

__all__ = [
    'QuantumSpectralWeaving',
    'SpectralWeavingConfig',
    'QuantumWeaver',
    'ComplexTensor',
    'QuantumShield',
    'GaugeFieldCoupling',
    'SU2Protection',
    'KPZEnhanced',
    'RiemannManifold',
    'QuantumBootstrap'
]

__version__ = '0.1.0'
