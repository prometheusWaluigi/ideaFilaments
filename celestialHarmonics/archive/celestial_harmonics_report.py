import json
from datetime import datetime

import matplotlib.pyplot as plt


class CelestialHarmonicsReport:
    def __init__(self, points, patterns, phase_metrics):
        self.points = points
        self.patterns = patterns
        self.phase_metrics = phase_metrics
        self.timestamp = datetime.now()

    def generate_markdown_report(self):
        report = f"""# Celestial Harmonics Analysis Report
## Generated: {self.timestamp}

### Detected Patterns
{self._format_patterns()}

### Phase Space Metrics
{self._format_phase_metrics()}

### Detailed Point Observations
{self._format_points()}
"""
        return report

    def _format_patterns(self):
        pattern_sections = []
        for pattern_type, pattern_list in self.patterns.items():
            if pattern_list:
                pattern_sections.append(
                    f"#### {pattern_type.replace('_', ' ').title()} Patterns"
                )
                for pattern in pattern_list:
                    pattern_sections.append(
                        f"- **Resonance**: {pattern.get('resonance', 'N/A')}"
                    )
                    pattern_sections.append(
                        f"  - **Points**: {', '.join(pattern.get('points_involved', []))}"
                    )
        return (
            "\n".join(pattern_sections)
            if pattern_sections
            else "No significant patterns detected."
        )

    def _format_phase_metrics(self):
        return "\n".join(
            [
                f"- **{k.replace('_', ' ').title()}**: {v}"
                for k, v in self.phase_metrics.items()
            ]
        )

    def _format_points(self):
        return "\n".join(
            [
                f"#### {point.name}\n"
                f"- RA: {point.ra_degrees:.2f}°\n"
                f"- Dec: {point.dec_degrees:.2f}°\n"
                f"- Ecliptic Longitude: {point.ecliptic_lon:.2f}°\n"
                f"- Distance: {point.distance_au:.4f} AU"
                for point in self.points
            ]
        )

    def generate_visualization(self, output_path="celestial_harmonics_plot.png"):
        plt.figure(figsize=(12, 8))

        ra_coords = [p.ra_degrees for p in self.points]
        dec_coords = [p.dec_degrees for p in self.points]
        plt.scatter(ra_coords, dec_coords, s=100, alpha=0.7)

        for p in self.points:
            plt.annotate(
                p.name,
                (p.ra_degrees, p.dec_degrees),
                xytext=(5, 5),
                textcoords="offset points",
            )

        plt.title("Celestial Harmonics Point Distribution")
        plt.xlabel("Right Ascension (degrees)")
        plt.ylabel("Declination (degrees)")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def export_json(self, output_path="celestial_harmonics_report.json"):
        report_data = {
            "timestamp": self.timestamp.isoformat(),
            "points": [
                {
                    "name": p.name,
                    "ra_degrees": p.ra_degrees,
                    "dec_degrees": p.dec_degrees,
                    "ecliptic_lon": p.ecliptic_lon,
                    "distance_au": p.distance_au,
                }
                for p in self.points
            ],
            "patterns": self.patterns,
            "phase_metrics": self.phase_metrics,
        }

        with open(output_path, "w") as f:
            json.dump(report_data, f, indent=2)
