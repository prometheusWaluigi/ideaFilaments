# [previous test content]

import unittest
import torch
import numpy as np
from quantum_spectral_weaving.complextensor import ComplexTensor
from quantum_spectral_weaving.quantum_spectral_weaving import (
    QuantumSpectralWeaving,
)
from quantum_spectral_weaving.riemann_dynamics import (
    RiemannQuantumDynamics,
    RiemannDynamicsConfig,
)
from quantum_spectral_weaving.spectral_weaving import SpectralWeavingConfig
from quantum_spectral_weaving.gauge_field import GaugeFieldCoupling
from quantum_spectral_weaving.kpz_enhanced import KPZEnhanced
from quantum_spectral_weaving.quantum_shield import QuantumShield
from quantum_spectral_weaving.su2_protect import SU2Protection
from quantum_spectral_weaving.bootstrap import QuantumBootstrap


class TestComplexTensor(unittest.TestCase):
    def test_creation(self):
        real = torch.tensor([1.0, 2.0])
        imag = torch.tensor([3.0, 4.0])
        ct = ComplexTensor(real, imag)
        self.assertTrue(torch.equal(ct.real, real))
        self.assertTrue(torch.equal(ct.imag, imag))

    def test_addition(self):
        ct1 = ComplexTensor(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]))
        ct2 = ComplexTensor(torch.tensor([5.0, 6.0]), torch.tensor([7.0, 8.0]))
        ct3 = ct1 + ct2
        self.assertTrue(torch.equal(ct3.real, torch.tensor([6.0, 8.0])))
        self.assertTrue(torch.equal(ct3.imag, torch.tensor([10.0, 12.0])))

    def test_subtraction(self):
        ct1 = ComplexTensor(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]))
        ct2 = ComplexTensor(torch.tensor([5.0, 6.0]), torch.tensor([7.0, 8.0]))
        ct3 = ct1 - ct2
        self.assertTrue(torch.equal(ct3.real, torch.tensor([-4.0, -4.0])))
        self.assertTrue(torch.equal(ct3.imag, torch.tensor([-4.0, -4.0])))

    def test_multiplication(self):
        ct1 = ComplexTensor(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]))
        ct2 = ComplexTensor(torch.tensor([5.0, 6.0]), torch.tensor([7.0, 8.0]))
        ct3 = ct1 * ct2
        # (1+3j)*(5+7j) = 5 + 7j + 15j - 21 = -16 + 22j
        # (2+4j)*(6+8j) = 12 + 16j + 24j - 32 = -20 + 40j
        self.assertTrue(torch.equal(ct3.real, torch.tensor([-16.0, -20.0])))
        self.assertTrue(torch.equal(ct3.imag, torch.tensor([22.0, 40.0])))

    def test_conjugate(self):
        ct = ComplexTensor(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]))
        conj = ct.conj()
        self.assertTrue(torch.equal(conj.real, torch.tensor([1.0, 2.0])))
        self.assertTrue(torch.equal(conj.imag, torch.tensor([-3.0, -4.0])))

    def test_abs(self):
        ct = ComplexTensor(torch.tensor([3.0, 0.0]), torch.tensor([4.0, 5.0]))
        abs_val = ct.abs()
        self.assertTrue(torch.allclose(abs_val, torch.tensor([5.0, 5.0])))

    def test_division(self):
        ct1 = ComplexTensor(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]))
        ct2 = ComplexTensor(torch.tensor([5.0, 6.0]), torch.tensor([7.0, 8.0]))
        ct3 = ct1 / ct2
        # (1+3j)/(5+7j) = (5-7j+15j+21)/(25+49) = (26+8j)/74 = 13/37 + 4/37j
        # (2+4j)/(6+8j) = (12-16j+24j+32)/(36+64) = (44+8j)/100 = 11/25 + 2/25j
        expected_real = torch.tensor([13.0 / 37.0, 11.0 / 25.0])
        expected_imag = torch.tensor([4.0 / 37.0, 2.0 / 25.0])
        self.assertTrue(torch.allclose(ct3.real, expected_real))
        self.assertTrue(torch.allclose(ct3.imag, expected_imag))

    def test_division_by_zero(self):
        ct1 = ComplexTensor(torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]))
        ct2 = ComplexTensor(torch.tensor([0.0, 0.0]), torch.tensor([0.0, 0.0]))
        with self.assertRaises(ZeroDivisionError):
            ct3 = ct1 / ct2  # Expect ZeroDivisionError

    def test_from_polar(self):
        r = torch.tensor([1.0, 2.0])
        theta = torch.tensor([np.pi / 2, np.pi / 4])  # 90 and 45 degrees
        ct = ComplexTensor.from_polar(r, theta)
        expected_real = torch.tensor([0.0, 2.0 * np.cos(np.pi / 4)])
        expected_imag = torch.tensor([1.0, 2.0 * np.sin(np.pi / 4)])
        self.assertTrue(torch.allclose(ct.real, expected_real, atol=1e-7))
        self.assertTrue(torch.allclose(ct.imag, expected_imag, atol=1e-7))

    def test_matmul(self):
        ct1 = ComplexTensor(torch.eye(2), torch.zeros(2, 2))  # Identity matrix
        ct2 = ComplexTensor(
            torch.tensor([[1.0, 2.0], [3.0, 4.0]]),
            torch.tensor([[5.0, 6.0], [7.0, 8.0]]),
        )
        ct3 = ct1 @ ct2
        self.assertTrue(torch.equal(ct3.real, ct2.real))
        self.assertTrue(torch.equal(ct3.imag, ct2.imag))

        ct4 = ComplexTensor(
            torch.tensor([[1.0, 0.0], [0.0, 1.0]]),
            torch.tensor([[0.0, 1.0], [-1.0, 0.0]]),
        )  # i, -i on the diagonals
        ct5 = ct4 @ ct4  # Should be -I
        self.assertTrue(torch.allclose(ct5.real, -torch.eye(2)))
        self.assertTrue(torch.allclose(ct5.imag, torch.zeros(2, 2)))

    def test_expm(self):
        # Test with a simple case:  i * [[0, 1], [-1, 0]]
        ct = ComplexTensor(torch.zeros(2,2), torch.tensor([[0., 1.], [-1., 0.]]))
        ct_exp = ct.expm()
        # Expected:  cos(1) * I + sin(1) * [[0, 1], [-1, 0]]
        expected_real = torch.tensor([[np.cos(1), 0.], [0., np.cos(1)]])
        expected_imag = torch.tensor([[0., np.sin(1)], [-np.sin(1), 0.]])
        self.assertTrue(torch.allclose(ct_exp.real, expected_real, atol=1e-6))
        self.assertTrue(torch.allclose(ct_exp.imag, expected_imag, atol=1e-6))

    def test_angle(self):
        ct = ComplexTensor(torch.tensor([1.0, 0.0, -1.0, 0.0]), torch.tensor([0.0, 1.0, 0.0, -1.0]))
        angles = ct.angle()
        expected_angles = torch.tensor([0.0, np.pi/2, np.pi, -np.pi/2])
        self.assertTrue(torch.allclose(angles, expected_angles, atol=1e-7))

    def test_requires_grad(self):
        ct = ComplexTensor(torch.randn(2,2), torch.randn(2,2))
        self.assertTrue(ct.real.requires_grad)
        self.assertTrue(ct.imag.requires_grad)
        ct.requires_grad_(False)
        self.assertFalse(ct.real.requires_grad)
        self.assertFalse(ct.imag.requires_grad)
        ct.requires_grad_(True)
        self.assertTrue(ct.real.requires_grad)
        self.assertTrue(ct.imag.requires_grad)

    def test_to(self):
        ct = ComplexTensor(torch.randn(2,2), torch.randn(2,2))
        ct_double = ct.to(torch.float64)
        self.assertEqual(ct_double.real.dtype, torch.float64)
        self.assertEqual(ct_double.imag.dtype, torch.float64)

        if torch.cuda.is_available():
            ct_cuda = ct.to(torch.device('cuda'))
            self.assertTrue(ct_cuda.real.is_cuda)
            self.assertTrue(ct_cuda.imag.is_cuda)

    def test_apply_gradient_manipulation(self):
        ct = ComplexTensor(torch.randn(2,2), torch.randn(2,2), requires_grad=True)
        ct_manipulated = ct.apply_gradient_manipulation(grad_scale_real=2.0, grad_scale_imag=0.5)
        loss = ct_manipulated.real.sum() + ct_manipulated.imag.sum()
        loss.backward()
        self.assertTrue(torch.allclose(ct.real.grad, torch.ones(2,2) * 2.0))
        self.assertTrue(torch.allclose(ct.imag.grad, torch.ones(2,2) * 0.5))

    def test_fft(self):
        ct = ComplexTensor(torch.randn(4), torch.randn(4))
        ct_fft = ct.fft()
        ct_forward = ct.forward()
        expected_fft = torch.fft.fft(ct_forward)
        self.assertTrue(torch.allclose(ct_fft.real, expected_fft.real, atol=1e-7))
        self.assertTrue(torch.allclose(ct_fft.imag, expected_fft.imag, atol=1e-7))

    def test_ifft(self):
        ct = ComplexTensor(torch.randn(4), torch.randn(4))
        ct_ifft = ct.ifft()
        ct_forward = ct.forward()
        expected_ifft = torch.fft.ifft(ct_forward)
        self.assertTrue(torch.allclose(ct_ifft.real, expected_ifft.real, atol=1e-7))
        self.assertTrue(torch.allclose(ct_ifft.imag, expected_ifft.imag, atol=1e-7))

    def test_ternary_quantize(self):
        ct = ComplexTensor(torch.tensor([-0.2, 0.05, 0.3]), torch.tensor([0.1, -0.01, -0.4]))
        ct_quantized = ct.ternary_quantize(threshold=0.1)
        expected_real = torch.tensor([-1.0, 0.0, 1.0])
        expected_imag = torch.tensor([1.0, 0.0, -1.0])
        self.assertTrue(torch.equal(ct_quantized.real, expected_real))
        self.assertTrue(torch.equal(ct_quantized.imag, expected_imag))

    def test_forward(self):
        real = torch.randn(3, 3, requires_grad=True)
        imag = torch.randn(3, 3, requires_grad=True)
        ct = ComplexTensor(real, imag) # Create instance FIRST
        ct = ComplexTensor.forward(None, ct) # Then call forward
        self.assertTrue(ct.real.requires_grad)
        self.assertTrue(ct.imag.requires_grad)

    def test_backward(self):
        real = torch.randn(3, 3, requires_grad=True)
        imag = torch.randn(3, 3, requires_grad=True)
        ct = ComplexTensor(real, imag)
        ct = ComplexTensor.forward(None, ct) # Call forward
        grad_real = torch.randn(3, 3)
        grad_imag = torch.randn(3, 3)
        grad_real_in, grad_imag_in = ComplexTensor.backward(None, grad_real, grad_imag) # Call backward
        self.assertTrue(torch.equal(grad_real_in, grad_real))
        self.assertTrue(torch.equal(grad_imag_in, grad_imag))


class TestQuantumSpectralWeaving(unittest.TestCase):
    def test_initialization(self):
        config = SpectralWeavingConfig()
        qsw = QuantumSpectralWeaving(config)
        self.assertIsNotNone(qsw)

    def test_compute_riemann_zeros(self):
        config = SpectralWeavingConfig(max_zeros=5)
        qsw = QuantumSpectralWeaving(config)
        zeros = qsw.compute_riemann_zeros()
        self.assertEqual(len(zeros), 5)

    def test_compute_eigenvalues(self):
        config = SpectralWeavingConfig(max_eigenvalues=5)
        qsw = QuantumSpectralWeaving(config)
        eigenvalues = qsw.compute_eigenvalues()
        self.assertEqual(len(eigenvalues), 5)

    def test_weave_spectral_patterns(self):
        config = SpectralWeavingConfig(max_zeros=2, max_eigenvalues=2)
        qsw = QuantumSpectralWeaving(config)
        pattern = qsw.weave_spectral_patterns()
        self.assertEqual(pattern.shape, (2, 2))

    def test_analyze_quantum_statistics(self):
        config = SpectralWeavingConfig()
        qsw = QuantumSpectralWeaving(config)
        stats = qsw.analyze_quantum_statistics()
        self.assertIn("mean_spacing", stats)
        self.assertIn("spectral_alignment", stats)
        self.assertIn("quantum_correlation", stats)
        self.assertIn("weaving_coherence", stats)

    def test_update_quantum_state(self):
        config = SpectralWeavingConfig()
        qsw = QuantumSpectralWeaving(config)
        qsw.update_quantum_state()  # Just check that it runs without error


class TestRiemannQuantumDynamics(unittest.TestCase):
    def test_initialization(self):
        config = RiemannDynamicsConfig()
        rqd = RiemannQuantumDynamics(config)
        self.assertIsNotNone(rqd)

    def test_evolve(self):
        config = RiemannDynamicsConfig(time_steps=10)  # Shorter time for testing
        rqd = RiemannQuantumDynamics(config)
        rqd.evolve()  # Just check that it runs without error

    def test_analyze_evolution_metrics(self):
        config = RiemannDynamicsConfig(time_steps=10)
        rqd = RiemannQuantumDynamics(config)
        rqd.evolve()
        metrics = rqd.analyze_evolution_metrics()
        self.assertIn("alignment", metrics)
        self.assertIn("correlation", metrics)
        self.assertIn("coherence", metrics)

    def test_extract_convergence_stats(self):
        config = RiemannDynamicsConfig(time_steps=10)
        rqd = RiemannQuantumDynamics(config)
        rqd.evolve()
        stats = rqd.extract_convergence_stats()
        self.assertIn("final_alignment", stats)
        self.assertIn("max_correlation", stats)
        self.assertIn("mean_coherence", stats)
        self.assertIn("convergence_time", stats)


class TestGaugeFieldCoupling(unittest.TestCase):
    def test_initialization(self):
        gauge = GaugeFieldCoupling()
        self.assertIsNotNone(gauge)

    def test_couple_quantum_states(self):
        gauge = GaugeFieldCoupling()
        state1 = ComplexTensor(torch.randn(3, 3), torch.randn(3, 3))
        state2 = ComplexTensor(torch.randn(3, 3), torch.randn(3, 3))
        coupled_states = gauge.couple_quantum_states([state1, state2])
        self.assertEqual(len(coupled_states), 2)

    def test_update_coupling_field(self):
        gauge = GaugeFieldCoupling()
        initial_field = gauge.coupling_field.clone()
        gauge.update_coupling_field()
        self.assertFalse(torch.equal(gauge.coupling_field.real, initial_field.real))
        self.assertFalse(torch.equal(gauge.coupling_field.imag, initial_field.imag))


class TestKPZEnhanced(unittest.TestCase):
    def test_initialization(self):
        kpz = KPZEnhanced()
        self.assertIsNotNone(kpz)

    def test_update_kpz_params(self):
        kpz = KPZEnhanced()
        initial_height_field = kpz.height_field.clone()
        kpz.update_kpz_params()
        self.assertFalse(torch.equal(kpz.height_field.real, initial_height_field.real))
        # Note:  It's possible (though unlikely) for the height field to remain *exactly* the same
        # after an update due to the randomness.  More robust tests might involve checking
        # statistical properties rather than direct equality.

    def test_apply_kpz_evolution(self):
        kpz = KPZEnhanced()
        state = ComplexTensor(torch.randn(64, 64), torch.randn(64, 64))
        evolved_state = kpz.apply_kpz_evolution(state)
        self.assertEqual(evolved_state.shape, state.shape)
        self.assertFalse(torch.equal(evolved_state.real, state.real))
        self.assertFalse(torch.equal(evolved_state.imag, state.imag))


class TestQuantumShield(unittest.TestCase):
    def test_initialization(self):
        shield = QuantumShield()
        self.assertIsNotNone(shield)

    def test_update_shield(self):
        shield = QuantumShield()
        initial_berry_curvature = shield.berry_curvature.clone()
        shield.update_shield()
        self.assertFalse(torch.equal(shield.berry_curvature.real, initial_berry_curvature.real))
        self.assertFalse(torch.equal(shield.berry_curvature.imag, initial_berry_curvature.imag))

    def test_activate_shield(self):
        shield = QuantumShield()
        state = ComplexTensor(torch.randn(10, 10), torch.randn(10, 10))
        protected_state = shield.activate_shield(state)
        self.assertEqual(protected_state.shape, state.shape)


class TestSU2Protection(unittest.TestCase):
    def test_initialization(self):
        su2 = SU2Protection()
        self.assertIsNotNone(su2)

    def test_update_gauge_field(self):
        su2 = SU2Protection()
        initial_gauge_field = su2.gauge_field.clone()
        su2.update_gauge_field()
        self.assertFalse(torch.equal(su2.gauge_field.real, initial_gauge_field.real))
        self.assertFalse(torch.equal(su2.gauge_field.imag, initial_gauge_field.imag))

    def test_protect_quantum_state(self):
        su2 = SU2Protection()
        state = ComplexTensor(torch.randn(2, 2), torch.randn(2, 2))
        protected_state = su2.protect_quantum_state(state)
        self.assertEqual(protected_state.shape, state.shape)


class TestQuantumBootstrap(unittest.TestCase):
    def test_initialization(self):
        bootstrap = QuantumBootstrap()
        self.assertIsNotNone(bootstrap)

    def test_update_bootstrap(self):
        bootstrap = QuantumBootstrap()
        initial_probability_field = bootstrap.probability_field.clone()
        bootstrap.update_bootstrap()
        self.assertFalse(torch.equal(bootstrap.probability_field.real, initial_probability_field.real))
        self.assertFalse(torch.equal(bootstrap.probability_field.imag, initial_probability_field.imag))

    def test_bootstrap_reality(self):
        bootstrap = QuantumBootstrap()
        state = ComplexTensor(torch.randn(10, 10), torch.randn(10, 10))
        bootstrapped_state = bootstrap.bootstrap_reality(state)
        self.assertEqual(bootstrapped_state.shape, state.shape)

    def test_recursive_collapse(self):
        bootstrap = QuantumBootstrap()
        state = ComplexTensor(torch.randn(10, 10), torch.randn(10, 10))
        collapsed_state = bootstrap._recursive_collapse(state)
        self.assertEqual(collapsed_state.shape, state.shape)

    def test_verify_emergence(self):
        bootstrap = QuantumBootstrap()
        # Test case where emergence should be true
        metrics = {
            "coherence": [0.95] * 11,
            "emergence": [0.95] * 11,
            "stability": [0.95] * 11,
        }
        self.assertTrue(bootstrap._verify_emergence(metrics))

        # Test case where emergence should be false (coherence too low)
        metrics = {
            "coherence": [0.8] * 11,
            "emergence": [0.95] * 11,
            "stability": [0.95] * 11,
        }
        self.assertFalse(bootstrap._verify_emergence(metrics))


if __name__ == "__main__":
    unittest.main()
