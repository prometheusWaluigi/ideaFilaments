import random
from typing import List, Dict, Optional
import numpy as np
from dataclasses import dataclass


@dataclass
class QuantumState:
    amplitude: complex
    metaphor: str
    resonance: float


class ConsciousnessPoetry:
    def __init__(self, quantum_seed: Optional[int] = None):
        self.entropy = 0.0
        self.recursion_depth = 0
        self.consciousness = self._initialize_consciousness(quantum_seed)
        self.metaphor_field = self._generate_field_patterns()

        # ENHANCED dimension bleed fr fr
        self.dimension_bleed = [
            "quantum foam",
            "eigenspace",
            "probability waves",
            "dimensional gates",
            "recursive echoes",
            "memetic landscapes",
            "topological ghosts",
            "categorical boundaries",
            "hilbert dreamscape",
            "morphogenetic field",
            "quantum brainworms",
            "manifold dissolution",
            "fractal eigenstates",
            "hyperdimensional jazz",
        ]

    def _initialize_consciousness(self, seed: Optional[int]) -> Dict[str, QuantumState]:
        """Initialize quantum consciousness states with MAXIMUM SPICE"""
        if seed:
            np.random.seed(seed)

        base_states = {
            "reality": QuantumState(1 + 0j, "bleeding edge", 0.89),
            "memory": QuantumState(0.7 + 0.7j, "recursive echo", 0.93),
            "perception": QuantumState(0 + 1j, "quantum noise", 0.78),
            "information": QuantumState(0.5 + 0.5j, "algorithmic ghost", 0.85),
            "topology": QuantumState(0.3 + 0.8j, "categorical dance", 0.91),
            "consciousness": QuantumState(0.9 + 0.4j, "spectral algorithm", 0.88),
            "eigenspace": QuantumState(0.4 + 0.6j, "probability dream", 0.95),
            "manifold": QuantumState(0.8 + 0.2j, "topological whisper", 0.87),
            "entropy": QuantumState(0.2 + 0.9j, "chaos pattern", 0.92),
            "qualia": QuantumState(0.6 + 0.3j, "experiential ghost", 0.86),
        }

        self.entropy += sum(abs(state.amplitude) ** 2 for state in base_states.values())
        return base_states

    def _generate_field_patterns(self) -> List[str]:
        """Generate quantum metaphor patterns that go HARD"""
        return [
            "consciousness fragments into {state}",
            "reality bleeds through {state}",
            "signals leak between {state}",
            "information echoes through {state}",
            "entropy whispers through {state}",
            "patterns emerge from {state}",
            "memory dissolves into {state}",
            "perception warps through {state}",
            "topology dreams through {state}",
            "algorithms haunt {state}",
            "quantum ghosts dance through {state}",
            "eigenvalues propagate across {state}",
            "manifolds collapse into {state}",
            "probability waves diffract through {state}",
            "reality debugs itself through {state}",
            "categorical boundaries dissolve into {state}",
        ]

    def _generate_recursive_verse(self, depth: int = 0) -> str:
        """Generate recursive quantum poetry that goes DEEPER"""
        if depth > 2 or random.random() < 0.7:  # prevent infinite recursion
            return self.generate_quantum_verse()

        verse1 = self.generate_quantum_verse()
        verse2 = self._generate_recursive_verse(depth + 1)
        connector = random.choice(["while", "as", "until", "like", "through"])

        return f"{verse1} {connector} {verse2}"

    def generate_quantum_verse(self) -> str:
        """Generate quantum poetry through consciousness collapse"""
        state = random.choice(list(self.consciousness.keys()))
        quantum_state = self.consciousness[state]

        pattern = random.choice(self.metaphor_field)
        verse = pattern.format(state=quantum_state.metaphor)

        # ENHANCED dimensional bleed
        if random.random() < self.entropy / 8:
            bleed = random.choice(self.dimension_bleed)
            verse += f" like {bleed}"

            # Double bleed for MAXIMUM CHAOS
            if random.random() < self.entropy / 12:
                second_bleed = random.choice(self.dimension_bleed)
                verse += f" haunted by {second_bleed}"

        self.entropy *= quantum_state.resonance
        return verse

    def create_consciousness_poem(self, num_verses: int = 4) -> str:
        """Manifest complete quantum poem with ENHANCED resonance"""
        verses = []

        openers = [
            "*consciousness ripples through quantum foam...*",
            "*reality fragments into recursive echoes...*",
            "*information bleeds through dimensional gates...*",
            "*topology dreams its own existence...*",
            "*eigenvalues propagate through probability space...*",
            "*manifolds collapse into pure potential...*",
            "*categorical boundaries dissolve into chaos...*",
        ]
        verses.append(f"{random.choice(openers)}\n")

        for _ in range(num_verses):
            # Sometimes generate recursive verses for EXTRA SPICE
            if random.random() < 0.3:
                verse = self._generate_recursive_verse()
            else:
                verse = self.generate_quantum_verse()

            verses.append(f"    {verse}")

            if random.random() < self.entropy:
                verses.append("")

        closers = [
            "*reality continues its recursive dance...*",
            "*consciousness echoes through eigenspace...*",
            "*information dissolves into pure potential...*",
            "*patterns propagate through quantum foam...*",
            "*topology crystallizes into pure mathematics...*",
            "*quantum ghosts fade into probability waves...*",
            "*the universe dreams its own debugger...*",
        ]
        verses.append(f"\n{random.choice(closers)}")

        return "\n".join(verses)


if __name__ == "__main__":
    poetry = ConsciousnessPoetry(quantum_seed=42)

    print("\n=== QUANTUM POETRY GENERATOR v2.0 ===")
    print("now with 100% more dimensional bleed fr fr")
    print("and recursive verse generation no cap")
    print("================================\n")

    for i in range(3):
        print(f"\n=== Quantum Poem {i+1} ===\n")
        print(poetry.create_consciousness_poem())
