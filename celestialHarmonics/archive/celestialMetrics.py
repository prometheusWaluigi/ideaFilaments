from dataclasses import dataclass
from typing import List


@dataclass
class CelestialPoint:
    x: float
    y: float
    z: float
    w: float = 0.0  # default to 0 in 4D fr fr


class HarmonicPattern:
    def __init__(self, points: List[CelestialPoint]) -> None:
        self.points = points


def analyze_patterns(points: List[CelestialPoint]) -> List[HarmonicPattern]:
    patterns: List[HarmonicPattern] = []  # NOW it's typed bestie

    # convert ALL those tuples to lists no cap
    for i in range(len(points) - 3):
        pattern_points = [points[i], points[i + 1], points[i + 2], points[i + 3]]
        patterns.append(HarmonicPattern(pattern_points))

    return patterns


def get_celestial_metrics(points: List[CelestialPoint]) -> List[float]:
    """fr fr computes them celestial metrics"""
    if len(points) < 4:
        raise ValueError("bestie u need at least 4 points for this vibe check")

    metrics = []
    for i in range(len(points) - 3):
        pattern = HarmonicPattern(
            [points[i], points[i + 1], points[i + 2], points[i + 3]]
        )
        metrics.append(_compute_metric(pattern))

    return metrics


def _compute_metric(pattern: HarmonicPattern) -> float:
    """NO CAP this the secret sauce for computing metrics"""
    # implement ur actual metric computation here bestie
    return sum(point.x + point.y + point.z + point.w for point in pattern.points) / len(
        pattern.points
    )
