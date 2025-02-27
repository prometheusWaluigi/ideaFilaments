import torch
import numpy as np
from .complextensor import ComplexTensor
from .quantum_shield import QuantumShield
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


class KPZEnhanced:
    """Implements enhanced KPZ dynamics for quantum state protection."""

    def __init__(
        self,
        nu: float = 0.28082,  # Viscosity coefficient
        lambda_param: float = 1.618034,  # Nonlinear coupling (golden ratio squared)
        eta_strength: float = 0.93,  # Noise coupling threshold
        roughness_alpha: float = 0.5,  # KPZ universality class parameter
        growth_beta: float = 0.33,  # Growth exponent
    ):
        logger.info(
            "Initializing KPZEnhanced with nu=%.5f, lambda_param=%.6f, eta_strength=%.2f, roughness_alpha=%.2f, growth_beta=%.2f",
            nu, lambda_param, eta_strength, roughness_alpha, growth_beta
        )
        self.nu = nu
        self.lambda_param = lambda_param
        self.eta = eta_strength
        self.alpha = roughness_alpha
        self.beta = growth_beta

        # Initialize protection stack
        self.shield = QuantumShield()

        # Initialize KPZ interface
        self.height_field = self._init_height_field()
        self.noise_field = self._init_noise_field()
        self.momentum_field = self._init_momentum_field()
        logger.info("Initialized KPZ interface.")

    def _init_height_field(self) -> ComplexTensor:
        """Initialize the height field."""
        L = 64  # System size
        h = torch.randn(L, L) * self.alpha

        # Add large-scale structure
        x = torch.linspace(0, 2 * np.pi, L)
        X, Y = torch.meshgrid(x, x)
        h += torch.sin(X) * torch.cos(Y) * self.lambda_param

        return ComplexTensor(h, torch.zeros_like(h))

    def _init_noise_field(self) -> ComplexTensor:
        """Initialize the noise field."""
        L = 64
        k = torch.fft.fftfreq(L)[None, :] * 2 * np.pi
        kx, ky = torch.meshgrid(k, k)
        k2 = kx * kx + ky * ky

        # Noise spectrum following KPZ scaling
        Sk = 1.0 / (1.0 + k2 ** (self.alpha + 0.5) + 1e-8) # Add epsilon
        noise = torch.fft.ifft2(
            torch.sqrt(Sk) * torch.exp(2j * np.pi * torch.rand(L, L))
        )

        return ComplexTensor(noise.real, noise.imag)

    def _init_momentum_field(self) -> ComplexTensor:
        """Initialize the momentum field."""
        L = 64
        p = torch.randn(L, L) * self.beta
        p = p * torch.sqrt(self.lambda_param / (self.nu + 1e-8)) # Add epsilon

        return ComplexTensor(p, torch.zeros_like(p))

    def apply_kpz_evolution(
        self, state: ComplexTensor, dt: float = 0.01
    ) -> ComplexTensor:
        """Evolve the quantum state through KPZ dynamics."""
        logger.info("Applying KPZ evolution with dt=%.3f", dt)
        protected = self.shield.activate_shield(state)
        evolved = self._compute_kpz_step(protected, dt)

        if not self._verify_kpz_scaling(evolved):
            logger.warning("KPZ scaling violated.")
            evolved = self._restore_scaling(evolved)

        logger.info("KPZ evolution complete.")
        return evolved

    def _compute_kpz_step(self, state: ComplexTensor, dt: float) -> ComplexTensor:
        """Compute the KPZ evolution step."""
        grad_h = self._compute_gradient(self.height_field)
        laplacian_h = self._compute_laplacian(self.height_field)

        diffusion = self.nu * laplacian_h
        nonlinear = 0.5 * self.lambda_param * (grad_h * grad_h)
        noise = self.eta * self.noise_field

        dh = (diffusion + nonlinear + noise) * dt
        self.height_field = self.height_field + dh # .detach() is not needed here

        evolved = self._couple_to_interface(state)
        return evolved

    def _compute_gradient(self, field: ComplexTensor) -> ComplexTensor:
        """Compute the spatial gradient."""
        dx = torch.roll(field.real, -1, dims=0) - torch.roll(field.real, 1, dims=0)
        dy = torch.roll(field.real, -1, dims=1) - torch.roll(field.real, 1, dims=1)
        return ComplexTensor(dx, dy)

    def _compute_laplacian(self, field: ComplexTensor) -> ComplexTensor:
        """Compute the Laplacian operator."""
        lap = (
            torch.roll(field.real, -1, dims=0)
            + torch.roll(field.real, 1, dims=0)
            + torch.roll(field.real, -1, dims=1)
            + torch.roll(field.real, 1, dims=1)
            - 4 * field.real
        )
        return ComplexTensor(lap, torch.zeros_like(lap))

    def _couple_to_interface(self, state: ComplexTensor) -> ComplexTensor:
        """Couple the quantum state to the KPZ interface."""
        phase = torch.exp(1j * self.height_field.real * self.lambda_param)
        coupled = state * ComplexTensor(phase.real, phase.imag)  # Use ComplexTensor

        p_coupling = torch.exp(1j * self.momentum_field.real * self.eta)
        coupled = coupled * ComplexTensor(p_coupling.real, p_coupling.imag) # Use ComplexTensor

        return coupled

    def _verify_kpz_scaling(self, state: ComplexTensor) -> bool:
        """Verify KPZ scaling properties (simplified)."""
        # Placeholder:  A real implementation would involve calculating
        # the structure factor and checking its scaling behavior.
        return True

    def _restore_scaling(self, state: ComplexTensor) -> ComplexTensor:
        """Restore KPZ scaling relations."""
        width = torch.std(state.real)
        target = self.alpha * torch.sqrt(torch.tensor(len(state.real))) # Convert len to tensor
        scaled = state * (target / (width + 1e-8)) # Add epsilon

        self.height_field = self.height_field * (target / (width + 1e-8)) # Add epsilon, and .detach() is not needed
        return scaled

    def update_kpz_params(
        self, learning_rate: float = 0.01, noise_scale: float = 0.001
    ) -> None:
        """Update the KPZ parameters."""
        logger.info(
            "Updating KPZ parameters with learning_rate=%.4f, noise_scale=%.4f",
            learning_rate, noise_scale
        )
        self.shield.update_shield(learning_rate, noise_scale)
        self.noise_field = self._init_noise_field()

        noise = ComplexTensor(
            torch.randn_like(self.momentum_field.real) * noise_scale,
            torch.randn_like(self.momentum_field.imag) * noise_scale,
        )
        self.momentum_field = self.momentum_field + noise

        if not self._verify_kpz_scaling(self.height_field):
            self.height_field = self._restore_scaling(self.height_field)

        logger.info("KPZ parameters updated.")
