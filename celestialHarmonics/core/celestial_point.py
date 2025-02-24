from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np


@dataclass
class CelestialPoint:
    """no cap this is just a fancy coordinate holder fr fr"""

    name: str
    ra_hours: float
    dec_degrees: float
    ecliptic_lon: float
    distance_au: float

    # optional drip
    proper_motion_ra: Optional[float] = None  # mas/yr
    proper_motion_dec: Optional[float] = None  # mas/yr
    radial_velocity: Optional[float] = None  # km/s

    @property
    def ra_degrees(self) -> float:
        """convert that ra to degrees bc STANDARDS"""
        return (self.ra_hours % 24) * 15

    @property
    def position_vector(self) -> np.ndarray:
        """get that 3d position vector EXPEDITIOUSLY"""
        ra_rad = np.radians(self.ra_degrees)
        dec_rad = np.radians(self.dec_degrees)

        return np.array(
            [
                self.distance_au * np.cos(dec_rad) * np.cos(ra_rad),
                self.distance_au * np.cos(dec_rad) * np.sin(ra_rad),
                self.distance_au * np.sin(dec_rad),
            ]
        )

    def angular_separation(self, other: "CelestialPoint") -> float:
        """calculate angular separation RIGOROUSLY"""
        # use quaternion rotation to avoid gimbal lock NO CAP
        v1 = self.position_vector / np.linalg.norm(self.position_vector)
        v2 = other.position_vector / np.linalg.norm(other.position_vector)

        dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
        return np.degrees(np.arccos(dot))

    def phase_space_state(self) -> Tuple[np.ndarray, np.ndarray]:
        """get that full phase space state vector EXPEDITIOUSLY
        returns position and momentum vectors"""
        pos = self.position_vector

        # if we got proper motion data use it
        if self.proper_motion_ra and self.proper_motion_dec:
            pm_ra = np.radians(
                self.proper_motion_ra / (3600 * 1000)
            )  # convert mas to rad
            pm_dec = np.radians(self.proper_motion_dec / (3600 * 1000))

            # construct velocity vector from proper motion
            vel = np.array(
                [
                    -self.distance_au * pm_ra * np.sin(np.radians(self.ra_degrees)),
                    self.distance_au * pm_ra * np.cos(np.radians(self.ra_degrees)),
                    self.distance_au * pm_dec,
                ]
            )

            # add radial component if we got it
            if self.radial_velocity:
                vel += self.radial_velocity * pos / np.linalg.norm(pos)
        else:
            # no proper motion? just approximate orbital velocity
            v = 2 * np.pi * self.distance_au / 365.25  # AU/day
            vel = np.cross(np.array([0, 0, 1]), pos) * v / np.linalg.norm(pos)

        return pos, vel

    def geometric_invariants(self) -> dict:
        """compute them geometric invariants ALGEBRAICALLY"""
        pos, vel = self.phase_space_state()

        # angular momentum vector
        L = np.cross(pos, vel)

        # energy (approximation assuming circular orbit)
        E = 0.5 * np.dot(vel, vel) - 1 / np.linalg.norm(pos)

        # laplace-runge-lenz vector (perihelion direction)
        LRL = np.cross(vel, L) - pos / np.linalg.norm(pos)

        return {
            "angular_momentum": L,
            "energy": E,
            "LRL_vector": LRL,
            "LRL_magnitude": np.linalg.norm(LRL),
        }

    def __repr__(self) -> str:
        return f"CelestialPoint(name='{self.name}', ra={self.ra_degrees:.2f}°, dec={self.dec_degrees:.2f}°)"
