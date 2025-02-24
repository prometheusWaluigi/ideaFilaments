from dataclasses import dataclass
from typing import Dict, Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class QuantumPattern(Generic[T]):
    """fr this pattern do be having that quantum coherence tho"""

    state: T
    coherence: float
    metadata: Optional[Dict[str, float]] = None

    def get_metadata_value(self, key: str, default: float = 0.0) -> float:
        """NO CAP we accessing that metadata SAFELY now"""
        return self.metadata.get(key, default) if self.metadata is not None else default

    def superpose(self, other: "QuantumPattern[T]") -> "QuantumPattern[T]":
        """fr fr quantum superposition BUSSIN"""
        return QuantumPattern(
            state=self.state,  # implement actual superposition logic here bestie
            coherence=(self.coherence + other.coherence) / 2,
            metadata={
                k: (self.get_metadata_value(k) + other.get_metadata_value(k)) / 2
                for k in (self.metadata or {}).keys() | (other.metadata or {}).keys()
            },
        )
