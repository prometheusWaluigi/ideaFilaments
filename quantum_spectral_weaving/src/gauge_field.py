import torch
from typing import Optional, List
from .complextensor import ComplexTensor
from .su2_protect import SU2Protection
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class GaugeFieldCoupling:
    """Implements gauge field coupling for quantum state protection."""

    def __init__(
        self,
        field_strength: float = 0.28082,
        coupling_modes: int = 3,
        interaction_range: float = 2.0,
        quench_threshold: float = 0.93,
    ):
        logger.info(
            "Initializing GaugeFieldCoupling with field_strength=%.4f, coupling_modes=%d, interaction_range=%.2f, quench_threshold=%.2f",
            field_strength, coupling_modes, interaction_range, quench_threshold
        )
        self.field_strength = field_strength
        self.modes = coupling_modes
        self.range = interaction_range
        self.threshold = quench_threshold

        # Initialize SU2 protection
        self.su2 = SU2Protection(
            coupling_strength=field_strength,
            gauge_field_dim=coupling_modes,
            protection_threshold=quench_threshold,
        )

        # Initialize coupling tensors
        self.coupling_field = self._init_coupling_field()
        self.interaction_kernel = self._init_interaction_kernel()
        logger.info("Initialized coupling tensors.")

    def _init_coupling_field(self) -> ComplexTensor:
        """Initialize the coupling field."""
        field = ComplexTensor(
            torch.randn(self.modes, 3, 3, requires_grad=True),
            torch.randn(self.modes, 3, 3, requires_grad=True),
        )

        # Normalize field strength
        field = field * (self.field_strength / (field.abs().mean() + 1e-8)) # Add epsilon
        logger.debug("Initialized coupling field with shape %s", field.real.shape)
        return field

    def _init_interaction_kernel(self) -> torch.Tensor:
        """Initialize the interaction kernel."""
        r = torch.linspace(0, self.range, 100)
        kernel = torch.exp(-r) / (r + 1e-8) # Add epsilon to avoid division by zero
        kernel[0] = kernel[1]  # Avoid singularity
        logger.debug("Initialized interaction kernel with shape %s", kernel.shape)
        return kernel

    def couple_quantum_states(
        self, states: List[ComplexTensor], topology: Optional[torch.Tensor] = None
    ) -> List[ComplexTensor]:
        """Couple quantum states through the gauge field."""
        logger.info("Coupling %d quantum states.", len(states))
        num_states = len(states)
        coupled_states = []

        # Default to fully connected topology if none provided
        if topology is None:
            topology = torch.ones(num_states, num_states)

        for i in range(num_states):
            coupled = ComplexTensor(
                torch.zeros_like(states[i].real), torch.zeros_like(states[i].imag)
            )

            for j in range(num_states):
                if i != j and topology[i, j] > 0:
                    r_ij = self._compute_distance(states[i], states[j])
                    strength = self._get_interaction_strength(r_ij)
                    interaction = self._compute_interaction(
                        states[i], states[j], strength
                    )
                    coupled = coupled + interaction

            coupled = coupled * (1.0 / (num_states - 1 + 1e-8)) # Add epsilon
            coupled = self.su2.protect_quantum_state(coupled)
            coupled_states.append(coupled)

        logger.info("Quantum state coupling complete.")
        return coupled_states

    def _compute_distance(self, state1: ComplexTensor, state2: ComplexTensor) -> float:
        """Compute the quantum state distance metric."""
        overlap = (state1.conj() * state2).abs().mean()
        distance = torch.sqrt(1 - overlap**2 + 1e-8) # Add epsilon
        return float(distance.item())

    def _get_interaction_strength(self, distance: float) -> float:
        """Get the interaction strength based on distance."""
        idx = int(distance * 100 / self.range)
        if idx >= len(self.interaction_kernel):
            return 0.0
        return float(self.interaction_kernel[idx].item())

    def _compute_interaction(
        self, state1: ComplexTensor, state2: ComplexTensor, strength: float
    ) -> ComplexTensor:
        """Compute state interactions through the gauge field."""
        interaction = ComplexTensor(
            torch.zeros_like(state1.real), torch.zeros_like(state1.imag)
        )

        for m in range(self.modes):
            U = self._compute_mode_coupling(m)
            transformed1 = U * state1
            transformed2 = U * state2
            mode_interaction = (transformed1 * transformed2.conj()) * strength
            interaction = interaction + mode_interaction

        return interaction

    def _compute_mode_coupling(self, mode: int) -> ComplexTensor:
        """Compute the mode coupling transformation."""
        field = self.coupling_field[mode]
        U = field.exp()
        U = U * (1.0 / (U.abs().mean() + 1e-8))  # Add epsilon for normalization
        return U

    def update_coupling_field(
        self, learning_rate: float = 0.01, noise_scale: float = 0.001
    ) -> None:
        """Update the coupling field with quantum fluctuations."""
        logger.info(
            "Updating coupling field with learning_rate=%.4f, noise_scale=%.4f",
            learning_rate, noise_scale
        )
        noise = ComplexTensor(
            torch.randn_like(self.coupling_field.real) * noise_scale,
            torch.randn_like(self.coupling_field.imag) * noise_scale,
        )
        self.coupling_field = self.coupling_field + noise
        self.coupling_field = self.coupling_field * (
            self.field_strength / (self.coupling_field.abs().mean() + 1e-8) # Add epsilon
        )
        self.su2.update_gauge_field(grad_scale=learning_rate, noise_scale=noise_scale)
        logger.info("Coupling field updated.")

    def _compute_gauge_invariance(self, state: ComplexTensor) -> float:
        """Compute the gauge invariance metric (simplified)."""
        # Placeholder: Returns a constant value.  A real implementation
        # would involve calculating how much the state changes under
        # a small gauge transformation.
        return 0.99
