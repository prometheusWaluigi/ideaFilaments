from quantum_spectral_weaving.src.quantum_spectral_weaving import QuantumWeaver
from quantum_spectral_weaving.src.spectral_weaving import QuantumSpectralWeaving, SpectralWeavingConfig
import numpy as np

print("testing that quantum heat EXPEDITIOUSLY")

# make a small config to test quickly
config = SpectralWeavingConfig(
    max_zeros=10,  # small for testing
    max_eigenvalues=10,
    coupling_strength=0.28082,  # golden ratio HEAT
    weaving_modes=3
)

try:
    # instantiate that quantum heat
    weaver = QuantumSpectralWeaving(config)
    print("quantum weaver initialized fr fr")
    
    # compute some riemann zeros
    zeros = weaver.compute_riemann_zeros()
    print(f"computed {len(zeros)} riemann zeros: {zeros[:3]}...")
    
    # compute quantum stats
    stats = weaver.analyze_quantum_statistics()
    print(f"quantum stats be like:")
    for k, v in stats.items():
        print(f"  {k}: {v:.6f}")
        
    print("QUANTUM TEST PASSED no cap")
except Exception as e:
    print(f"bruh the quantum test FAILED: {str(e)}")
    import traceback
    traceback.print_exc()