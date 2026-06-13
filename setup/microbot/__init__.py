"""
MicroBot Round V0 package.

This package contains the first hardware bring-up modules for MicroBot Round V0:
configuration, pin mapping, logging, LEDs, IMU, camera, audio, distance sensing,
servo control and safety logic.

The project is intentionally developed in small validated layers. Early modules
should remain simple, readable and safe. Hardware movement must always be routed
through the safety layer before reaching physical actuators.
"""

__project_name__ = "MicroBot Round V0"
__version__ = "0.1.0"
__status__ = "prepared"

__all__ = [
    "__project_name__",
    "__version__",
    "__status__",
]