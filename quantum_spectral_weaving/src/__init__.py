import logging
from .complextensor import ComplexTensor
from .quantum_spectral_weaving import QuantumSpectralWeaving, RiemannQuantumDynamics

__all__ = ["ComplexTensor", "QuantumSpectralWeaving", "RiemannQuantumDynamics"]

# Configure the logger (Simplified)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Default to INFO, DEBUG can be set via environment variable

# Create console handler (if not already configured)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

logger.info("quantum_spectral_weaving package initialized.")
