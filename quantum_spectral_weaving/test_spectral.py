# save this as test_spectral.py
import sys
import os

# add the src dir to path directly (ghetto but effective)
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(src_path)

# now import directly from the src modules
from quantum_spectral_weaving import QuantumWeaver
from spectral_weaving import QuantumSpectralWeaving, SpectralWeavingConfig

print("testing that quantum heat EXPEDITIOUSLY")

# make a small config to test quickly
config = SpectralWeavingConfig(
    max_zeros=5,  # tiny for quick testing
    max_eigenvalues=5,
    coupling_strength=0.28082,  # golden ratio HEAT
    weaving_modes=3
)

try:
    # instantiate that quantum heat
    weaver = QuantumSpectralWeaving(config)
    print("quantum weaver initialized fr fr")
    
    # compute some riemann zeros
    zeros = weaver.compute_riemann_zeros()
    print(f"computed {len(zeros)} riemann zeros: {zeros}")
    
    print("QUANTUM TEST PASSED no cap")
except Exception as e:
    print(f"bruh the quantum test FAILED: {str(e)}")
    import traceback
    traceback.print_exc()