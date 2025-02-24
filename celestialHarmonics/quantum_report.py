from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from complex_tensor.viz import plot_wigner_function

from .core.quantum_patterns import QuantumPoint


@dataclass
class QuantumReport:
    """report generator that goes ABSOLUTELY WILD"""

    points: List[QuantumPoint]
    patterns: Dict[str, List[Dict]]
    timestamp: datetime = datetime.now()

    def generate_markdown(self) -> str:
        return f"""# Quantum Pattern Analysis Report
Generated: {self.timestamp}

## Quantum Patterns Detected

### Entangled Pairs
{self._format_entangled_pairs()}

### Coherent Clusters
{self._format_coherent_clusters()}

### Ergodic Regions
{self._format_ergodic_regions()}

### Berry Phases
{self._format_berry_phases()}

## Quantum State Analysis
{self._format_state_analysis()}
"""

    def _format_entangled_pairs(self) -> str:
        pairs = self.patterns.get("entangled_pairs", [])
        if not pairs:
            return "No significant entangled pairs detected."

        formatted = []
        for pair in pairs:
            formatted.append(
                f"- Points: {pair['points'][0]} ↔️ {pair['points'][1]}\n"
                f"  - Entanglement: {pair['entanglement']:.3f}"
            )
        return "\n".join(formatted)

    def _format_coherent_clusters(self) -> str:
        clusters = self.patterns.get("coherent_clusters", [])
        if not clusters:
            return "No coherent clusters detected."

        formatted = []
        for i, cluster in enumerate(clusters):
            formatted.append(
                f"- Cluster {i+1}\n" f"  - Coherence: {cluster['strength']:.3f}"
            )
        return "\n".join(formatted)

    def _format_ergodic_regions(self) -> str:
        regions = self.patterns.get("ergodic_regions", [])
        if not regions:
            return "No ergodic regions detected."

        formatted = []
        for region in regions:
            formatted.append(
                f"- Region measure: {region['measure']:.3f}\n"
                f"  - Points: {', '.join(region['points'])}"
            )
        return "\n".join(formatted)

    def _format_berry_phases(self) -> str:
        phases = self.patterns.get("berry_phases", [])
        if not phases:
            return "No significant geometric phases detected."

        formatted = []
        for phase in phases:
            formatted.append(
                f"- Geometric phase: {phase['phase']:.3f}π\n"
                f"  - Type: {phase['type']}"
            )
        return "\n".join(formatted)

    def _format_state_analysis(self) -> str:
        # compute average quantities over all points
        entropies = [p.state.von_neumann_entropy() for p in self.points]
        purities = [p.state.purity() for p in self.points]

        return f"""
### Statistical Analysis
- Mean von Neumann entropy: {np.mean(entropies):.3f}
- Mean state purity: {np.mean(purities):.3f}
- Number of quantum points: {len(self.points)}
"""

    def generate_visualizations(self, output_dir: str = "."):
        """make them plots go CRAZY"""
        # plot wigner functions for each point
        for i, point in enumerate(self.points):
            fig, ax = plt.subplots(figsize=(8, 6))
            plot_wigner_function(point.state, ax=ax)
            ax.set_title(f"Wigner Function - {point.name}")
            plt.savefig(f"{output_dir}/wigner_{i}.png")
            plt.close()

        # plot entanglement network
        fig, ax = plt.subplots(figsize=(10, 8))
        self._plot_entanglement_network(ax)
        plt.savefig(f"{output_dir}/entanglement_network.png")
        plt.close()

        # plot quantum ergodicity measures
        fig, ax = plt.subplots(figsize=(8, 6))
        self._plot_ergodicity_measures(ax)
        plt.savefig(f"{output_dir}/ergodicity.png")
        plt.close()

    def _plot_entanglement_network(self, ax):
        """visualize that entanglement TOPOLOGY"""
        pairs = self.patterns.get("entangled_pairs", [])

        # create network layout
        pos = {}
        for i, point in enumerate(self.points):
            angle = 2 * np.pi * i / len(self.points)
            pos[point.name] = np.array([np.cos(angle), np.sin(angle)])

        # plot points
        for name, position in pos.items():
            ax.scatter(*position, s=100, label=name)

        # plot entanglement edges
        for pair in pairs:
            p1, p2 = pair["points"]
            strength = pair["entanglement"]
            ax.plot(
                [pos[p1][0], pos[p2][0]],
                [pos[p1][1], pos[p2][1]],
                "-",
                alpha=strength,
                linewidth=2 * strength,
            )

        ax.set_title("Quantum Entanglement Network")
        ax.axis("equal")
        ax.legend()

    def _plot_ergodicity_measures(self, ax):
        """visualize that QUANTUM CHAOS"""
        regions = self.patterns.get("ergodic_regions", [])

        if not regions:
            ax.text(0.5, 0.5, "No ergodic regions detected", ha="center", va="center")
            return

        measures = [r["measure"] for r in regions]
        ax.hist(measures, bins="auto", density=True)
        ax.set_xlabel("Ergodicity Measure")
        ax.set_ylabel("Density")
        ax.set_title("Distribution of Quantum Ergodicity")
