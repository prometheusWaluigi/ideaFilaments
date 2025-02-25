import torch
import numpy as np
from .complextensor import ComplexTensor
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(ch)


class SU2Protection:
    """Implements SU(2) gauge field protection for quantum states."""

    def __init__(
        self,
        coupling_strength: float = 0.28082,
        gauge_field_dim: int = 3,
        protection_threshold: float = 0.93,
    ):
        logger.info(
            "Initializing SU2Protection with coupling_strength=%.4f, gauge_field_dim=%d, protection_threshold=%.2f",
            coupling_strength, gauge_field_dim, protection_threshold
        )
        self.coupling = coupling_strength
        self.dim = gauge_field_dim
        self.threshold = protection_threshold

        self.sigma_x = ComplexTensor(
            torch.tensor([[0.0, 1.0], [1.0, 0.0]]), torch.tensor([[0.0, 0.0], [0.0, 0.0]])
        )
        self.sigma_y = ComplexTensor(
            torch.tensor([[0.0, 0.0], [0.0, 0.0]]), torch.tensor([[0.0, -1.0], [1.0, 0.0]])
        )
        self.sigma_z = ComplexTensor(
            torch.tensor([[1.0, 0.0], [0.0, -1.0]]), torch.tensor([[0.0, 0.0], [0.0, 0.0]])
        )

        self.gauge_field = self._init_gauge_field()
        logger.info("Initialized SU(2) gauge field.")

    def _init_gauge_field(self) -> ComplexTensor:
        """Initialize the SU(2) gauge field."""
        field = ComplexTensor(
            torch.randn(self.dim, self.dim, requires_grad=True),
            torch.randn(self.dim, self.dim, requires_grad=True),
        )
        projected = self._project_to_lie_algebra(field)
        return projected * self.coupling

    def protect_quantum_state(self, state: ComplexTensor) -> ComplexTensor:
        """Protect the quantum state using the SU(2) gauge field."""
        logger.info("Applying SU(2) gauge field protection.")
        U = self._compute_gauge_transformation()
        protected_state = U * state

        if self._check_coherence(protected_state) < self.threshold:
            logger.warning("Coherence below threshold. Restoring.")
            protected_state = self._restore_coherence(protected_state)

        logger.info("SU(2) protection applied.")
        return protected_state

    def _compute_gauge_transformation(self) -> ComplexTensor:
        """Compute the SU(2) gauge transformation."""
        exponent = (
            self.gauge_field * self.sigma_x
            + self.gauge_field * self.sigma_y
            + self.gauge_field * self.sigma_z
        )
        U = exponent.expm()  # Use expm for matrix exponential
        return U

    def update_gauge_field(
        self, grad_scale: float = 0.01, noise_scale: float = 0.001
    ) -> None:
        """Update the gauge field."""
        logger.info(
            "Updating gauge field with grad_scale=%.4f, noise_scale=%.4f",
            grad_scale, noise_scale
        )
        noise = ComplexTensor(
            torch.randn_like(self.gauge_field.real) * noise_scale,
            torch.randn_like(self.gauge_field.imag) * noise_scale,
        )

        self.gauge_field = self.gauge_field + noise
        self.gauge_field = self._project_to_lie_algebra(self.gauge_field)
        self.gauge_field = self.gauge_field * grad_scale
        logger.info("Gauge field updated.")

    def _project_to_lie_algebra(self, field: ComplexTensor) -> ComplexTensor:
        """Project the gauge field back to the Lie algebra."""
        anti_hermitian_part = (field - field.conj()) / 2
        return anti_hermitian_part

    def _check_coherence(self, state: ComplexTensor) -> float:
        """Check the coherence of the quantum state (simplified)."""
        coherence = state.abs().mean()
        return float(coherence.item())

    def _restore_coherence(self, state: ComplexTensor) -> ComplexTensor:
        """Restore coherence if it falls below the threshold."""
        return state / (state.abs().mean() + 1e-8) # Add epsilon
