# save as simple_test.py
import sys
import os

# direct src import - no package bullshit
sys.path.insert(0, os.path.abspath('./src'))

# create mock types.py since that seems to be missing
with open('src/types.py', 'w') as f:
    f.write("""
# mock types module EXPEDITIOUSLY
from complextensor import ComplexTensor
from quantum_shield import QuantumShield
""")

# test if we can import stuff now
try:
    import spectral_weaving
    print("YO SPECTRAL WEAVING IMPORTED fr fr")
    
    # try to create the basic objects
    config = spectral_weaving.SpectralWeavingConfig(
        max_zeros=3,      # tiny af for test
        max_eigenvalues=3,
        coupling_strength=0.28082
    )
    
    # make the weaver EXPEDITIOUSLY
    print("creating quantum weaver...")
    weaver = spectral_weaving.QuantumSpectralWeaving(config)
    print("WEAVER CREATED no cap")
    
    # try a basic function
    print("computing quantum stats...")
    stats = weaver.analyze_quantum_statistics()
    print(f"QUANTUM STATS: {stats}")

except Exception as e:
    print(f"quantum FAILURE: {e}")
    import traceback
    traceback.print_exc()