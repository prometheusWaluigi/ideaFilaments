# [previous test content]

import unittest
import torch
import numpy as np
from quantum_spectral_weaving.src.complextensor import ComplexTensor
from quantum_spectral_weaving.src.quantum_spectral_weaving import (
    QuantumSpectralWeaving,
    RiemannQuantumDynamics,
)
from quantum_spectral_weaving.src.spectral_weaving import SpectralWeavingConfig
from quantum_spectral_weaving.src.riemann_dynamics import RiemannDynamicsConfig
from quantum_spectral_weaving.src.gauge_field import GaugeFieldCoupling
from quantum_spectral_weaving.src.kpz_enhanced import KPZEnhanced
from quantum_spectral_weaving.src.quantum_shield import QuantumShield
from quantum_spectral_weaving.src.su2_protect import SU2Protection
from quantum_spectral_weaving.src.bootstrap import QuantumBootstrap


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
        # (1+3j)/(5+7j) = (5+7j-15j+21)/(25+49) = (26-8j)/74 = 13/37 - 4/37j
        # (2+4j)/(6+8j) = (12+16j-24j+32)/(36+64) = (44-8j)/100 = 11/25 - 2/25j
        expected_real = torch.tensor([13.0 / 37.0, 11.0 / 25.0])
        expected_imag = torch.tensor([-4.0 / 37.0, -2.0 / 25.0])
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
        ct2 = ComplexTensor(torch.tensor([[1.0, 2.0], [3.0, 4.0]]), torch.tensor([[5.0, 6.0], [7.0, 8.0]]))
        ct3 = ct1 @ ct2
        self.assertTrue(torch.equal(ct3.real, ct2.real))
        self.assertTrue(torch.equal(ct3.imag, ct2.imag))

        ct4 = ComplexTensor(torch.tensor([[1.0, 0.0], [0.0, 1.0]]), torch.tensor([[0.0, 1.0], [-1.0, 0.0]])) # i, -i on the diagonals
        ct5 = ct4 @ ct4 # Should be -I
        self.assertTrue(torch.allclose(ct5.real, -torch.eye(2)))
        self.assertTrue(torch.allclose(ct5.imag, torch.zeros(2,2)))

    def test_expm(self):
        # Test with a simple case:  i * [[0, 1], [-1, 0]]
        ct = ComplexTensor(torch.zeros(2,2), torch.tensor([[0., 1.], [-1., 0.]]))
        ct_exp = ct.expm()
        # Expected:  [[cos(1), sin(1)], [-sin(1), cos(1)]]
        expected_real = torch.tensor([[np.cos(1.), np.sin(1.)], [-np.sin(1.), np.cos(1.)]])
        expected_imag = torch.zeros(2,2)
        self.assertTrue(torch.allclose(ct_exp.real, expected_real, atol=1e-6))
        self.assertTrue(torch.allclose(ct_exp.imag, expected_imag, atol=1e-6))

    def test_forward(self):
        real = torch.randn(3, 3, requires_grad=True)
        imag = torch.randn(3, 3, requires_grad=True)
        ct = ComplexTensor.forward(real, imag)
        self.assertTrue(isinstance(ct, torch.Tensor))
        self.assertTrue(ct.requires_grad)

    def test_backward(self):
        real = torch.randn(3, 3, requires_grad=True)
        imag = torch.randn(3, 3, requires_grad=True)
        ct = ComplexTensor.forward(real, imag)
        ct.sum().backward()  # Sum to get a scalar for backward
        self.assertTrue(real.grad is not None)
        self.assertTrue(imag.grad is not None)

    def test_fft(self):
        ct = ComplexTensor(torch.randn(4, 4), torch.randn(4, 4))
        ct_fft = ct.fft()
        self.assertTrue(isinstance(ct_fft, ComplexTensor))
        self.assertEqual(ct_fft.shape, ct.shape)

    def test_ifft(self):
        ct = ComplexTensor(torch.randn(4, 4), torch.randn(4, 4))
        ct_ifft = ct.ifft()
        self.assertTrue(isinstance(ct_ifft, ComplexTensor))
        self.assertEqual(ct_ifft.shape, ct.shape)

    def test_ternary_quantize(self):
        ct = ComplexTensor(torch.randn(5,5), torch.randn(5,5))
        ct_ternary = ct.ternary_quantize(threshold=0.2)
        self.assertTrue(isinstance(ct_ternary, ComplexTensor))
        # Check that all values are -1, 0, or 1
        self.assertTrue(torch.all((ct_ternary.real >= -1) & (ct_ternary.real <= 1)))
        self.assertTrue(torch.all((ct_ternary.imag >= -1) & (ct_ternary.imag <= 1)))
        self.assertTrue(torch.all(torch.isin(ct_ternary.real, torch.tensor([-1., 0., 1.]))))
        self.assertTrue(torch.all(torch.isin(ct_ternary.imag, torch.tensor([-1., 0., 1.]))))


class TestQuantumSpectralWeaving(unittest.TestCase):
    def test_initialization(self):
        config = SpectralWeavingConfig()
        weaver = QuantumSpectralWeaving(config)
        self.assertIsNotNone(weaver)

    def test_compute_riemann_zeros(self):
        config = SpectralWeavingConfig(max_zeros=5)
        weaver = QuantumSpectralWeaving(config)
        zeros = weaver.compute_riemann_zeros()
        self.assertEqual(len(zeros), 5)
        self.assertTrue(np.iscomplexobj(zeros))

    def test_compute_eigenvalues(self):
        config = SpectralWeavingConfig(max_eigenvalues=5)
        weaver = QuantumSpectralWeaving(config)
        eigenvalues = weaver.compute_eigenvalues()
        self.assertEqual(len(eigenvalues), 5)
        self.assertTrue(np.iscomplexobj(eigenvalues))

    def test_weave_spectral_patterns(self):
        config = SpectralWeavingConfig(max_zeros=2, max_eigenvalues=3)
        weaver = QuantumSpectralWeaving(config)
        pattern = weaver.weave_spectral_patterns()
        self.assertEqual(pattern.shape, (2, 3))
        self.assertTrue(np.iscomplexobj(pattern))

    def test_analyze_quantum_statistics(self):
        config = SpectralWeavingConfig()
        weaver = QuantumSpectralWeaving(config)
        stats = weaver.analyze_quantum_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn("mean_spacing", stats)
        self.assertIn("spectral_alignment", stats)
        self.assertIn("quantum_correlation", stats)
        self.assertIn("weaving_coherence", stats)

    def test_update_quantum_state(self):
        config = SpectralWeavingConfig()
        weaver = QuantumSpectralWeaving(config)
        initial_riemann_state = weaver.riemann_state.clone()
        weaver.update_quantum_state()
        # Check that the state has been updated (not exactly equal to initial state)
        self.assertFalse(torch.equal(weaver.riemann_state.real, initial_riemann_state.real))
        self.assertFalse(torch.equal(weaver.riemann_state.imag, initial_riemann_state.imag))


class TestRiemannQuantumDynamics(unittest.TestCase):
    def test_initialization(self):
        config = RiemannDynamicsConfig()
        dynamics = RiemannQuantumDynamics(config)
        self.assertIsNotNone(dynamics)

    def test_evolve(self):
        config = RiemannDynamicsConfig(time_steps=10)  # Shorter time for testing
        dynamics = RiemannQuantumDynamics(config)
        dynamics.evolve()
        self.assertEqual(len(dynamics.quantum_states), 10)

    def test_analyze_evolution_metrics(self):
        config = RiemannDynamicsConfig(time_steps=5)
        dynamics = RiemannQuantumDynamics(config)
        dynamics.evolve()
        metrics = dynamics.analyze_evolution_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn("alignment", metrics)
        self.assertIn("correlation", metrics)
        self.assertIn("coherence", metrics)
        self.assertEqual(len(metrics["alignment"]), 5)

    def test_extract_convergence_stats(self):
        config = RiemannDynamicsConfig(time_steps=5)
        dynamics = RiemannQuantumDynamics(config)
        dynamics.evolve()
        stats = dynamics.extract_convergence_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("final_alignment", stats)
        self.assertIn("max_correlation", stats)
        self.assertIn("mean_coherence", stats)
        self.assertIn("convergence_time", stats)


class TestGaugeFieldCoupling(unittest.TestCase):
    def test_initialization(self):
        gauge = GaugeFieldCoupling()
        self.assertIsNotNone(gauge)

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
