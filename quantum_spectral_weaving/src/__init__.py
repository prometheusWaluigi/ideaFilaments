import logging
from .complextensor import ComplexTensor
from .quantum_spectral_weaving import QuantumSpectralWeaving, RiemannQuantumDynamics

__all__ = ['ComplexTensor', 'QuantumSpectralWeaving', 'RiemannQuantumDynamics']

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # Set to DEBUG to capture all debug messages

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

logger.info("quantum_spectral_weaving package initialized.")