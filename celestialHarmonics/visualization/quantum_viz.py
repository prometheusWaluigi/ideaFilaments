from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import torch

from ..analysis.quantum_analyzer import QuantumPatternAnalyzer
from ..core.quantum_patterns import QuantumPoint


def plot_wigner(
    wigner: torch.Tensor,
    x_range: Tuple[float, float],
    p_range: Tuple[float, float],
    ax=None,
) -> None:
    """plot that wigner function EXPEDITIOUSLY"""
    if ax is None:
        _, ax = plt.subplots()

    extent = [x_range[0], x_range[1], p_range[0], p_range[1]]
    im = ax.imshow(
        wigner.numpy(), extent=extent, origin="lower", cmap="RdBu_r", aspect="equal"
    )
    plt.colorbar(im, ax=ax)
    ax.set_xlabel("Position")
    ax.set_ylabel("Momentum")
    ax.set_title("Wigner Quasi-Probability Distribution")


def plot_entanglement_network(
    points: List[QuantumPoint], patterns: Dict[str, List[Dict]], ax=None
) -> None:
    """visualize them quantum correlations NO CAP"""
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

    # plot points
    positions = torch.stack([p.position.real for p in points])
    ax.scatter(
        positions[:, 0], positions[:, 1], positions[:, 2], c="blue", marker="o", s=100
    )

    # plot entanglement connections
    for pair in patterns["entangled_pairs"]:
        idx1 = next(i for i, p in enumerate(points) if p.name == pair["points"][0])
        idx2 = next(i for i, p in enumerate(points) if p.name == pair["points"][1])
        p1, p2 = positions[idx1], positions[idx2]

        # line color based on entanglement strength
        color = plt.cm.viridis(pair["entanglement"] / 4.0)  # normalize to max entropy
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            c=color,
            linewidth=2,
            alpha=0.5,
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Quantum Entanglement Network")


def plot_coherent_clusters(
    analyzer: QuantumPatternAnalyzer, patterns: Dict[str, List[Dict]], ax=None
) -> None:
    """visualize them coherent state clusters fr fr"""
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))

    # plot eigenvalue spectrum
    eigenvals, _ = analyzer.density_matrix.eigendecomposition()
    ax.bar(range(len(eigenvals)), eigenvals.numpy(), alpha=0.7)

    # highlight coherent clusters
    for cluster in patterns["coherent_clusters"]:
        ax.axhline(y=cluster["strength"], color="r", linestyle="--", alpha=0.5)

    ax.set_xlabel("Eigenvalue Index")
    ax.set_ylabel("Eigenvalue")
    ax.set_title("Density Matrix Spectrum (Coherent Clusters in Red)")


def plot_berry_phases(
    points: List[QuantumPoint], patterns: Dict[str, List[Dict]], ax=None
) -> None:
    """visualize them geometric phases NO CAP"""
    if ax is None:
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

    # plot points
    positions = torch.stack([p.position.real for p in points])
    ax.scatter(
        positions[:, 0], positions[:, 1], positions[:, 2], c="blue", marker="o", s=100
    )

    # plot berry phase loops
    for loop in patterns["berry_phases"]:
        indices = [
            next(i for i, p in enumerate(points) if p.name == name)
            for name in loop["points"]
        ]
        loop_points = positions[indices]

        # color based on phase
        color = plt.cm.hsv(loop["phase"] / (2 * np.pi))
        ax.plot(
            loop_points[:, 0],
            loop_points[:, 1],
            loop_points[:, 2],
            c=color,
            linewidth=2,
            alpha=0.7,
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Geometric Phase Loops")


def quantum_visualization_report(
    points: List[QuantumPoint],
    analyzer: QuantumPatternAnalyzer,
    patterns: Dict[str, List[Dict]],
) -> None:
    """generate that QUANTUM VISUALIZATION REPORT fr fr"""
    fig = plt.figure(figsize=(20, 15))

    # wigner function for first point
    ax1 = fig.add_subplot(221)
    wigner = analyzer.visualize_state(0)
    plot_wigner(wigner, (-5, 5), (-5, 5), ax1)

    # entanglement network
    ax2 = fig.add_subplot(222, projection="3d")
    plot_entanglement_network(points, patterns, ax2)

    # coherent clusters
    ax3 = fig.add_subplot(223)
    plot_coherent_clusters(analyzer, patterns, ax3)

    # berry phases
    ax4 = fig.add_subplot(224, projection="3d")
    plot_berry_phases(points, patterns, ax4)

    plt.tight_layout()
    plt.show()
