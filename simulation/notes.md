# MicroBot Round V0 Simulation Notes

## Purpose

This folder contains the first simulation model for MicroBot Round V0.

The simulation is not intended to be a perfect CAD replica of the physical robot. It is a simplified physics model used to reason about the robot body, center of mass, leg placement, contact points, approximate movement, orientation, and basic sensor placement.

The physical robot remains the source of truth. A successful simulation does not prove that the real robot walks, balances, sees, hears, or moves safely. Real hardware validation requires physical tests, logs, photos, videos, and measured evidence.

## Current Simulation File

The current model file is:

```text
simulation/microbot_round_body.xml
```

It defines a simplified MuJoCo body for MicroBot Round V0 using primitive shapes such as boxes, spheres, ellipsoids, cylinders, and capsules.

The model includes:

```text
main rounded body
upper shell approximation
lower shell approximation
two side servo bodies
two hinged leg assemblies
rounded foot contact pads
Raspberry Pi Zero 2 W block
battery block
IMU block
camera module
speaker disk
microphone block
LED ring visual markers
basic floor contact
joint position sensors
joint velocity sensors
body accelerometer
body gyro
simple motor actuators
```

## Design Philosophy

The simulation follows the same philosophy as the physical prototype:

```text
build it large enough first
make it real before making it small
test one subsystem at a time
separate simulation from hardware validation
avoid exaggerated claims
use the model to learn, not to pretend the robot is finished
```

MicroBot Round V0 is a bench prototype. The goal is not to simulate a perfect autonomous creature. The goal is to create a useful engineering model that supports the real build.

## What the Simulation Represents

The simulation represents the first physical concept of a rounded MicroBot body with two actuated side legs.

The body shape is approximated as a compact rounded shell. The internal components are represented as simple blocks so their approximate mass and position can be reasoned about. The two legs use hinge joints and simple foot geometries so that basic contact and movement experiments can be performed.

The visual LED ring, camera, speaker, microphone, IMU and internal boards are included to keep the model conceptually aligned with the real hardware layout.

## What the Simulation Does Not Represent

The simulation does not currently represent:

```text
exact STL geometry
real printed plastic flexibility
real servo torque curves
real SCS0009 gearbox backlash
real battery cable routing
real wire stiffness
real friction of the final printed feet
real IMU noise
real camera image processing
real audio behavior
real power rail voltage drops
real servo stalls
real balance recovery
real walking controller
real autonomous intelligence
```

These limitations are intentional. The model starts simple so that it can be understood, tested, and improved.

## Relationship With the Physical Build

The physical build uses real hardware modules. The planned reference architecture includes:

```text
Raspberry Pi Zero 2 W
SCS0009 / SC09 serial bus servos
MPU-6050 IMU
Pi-compatible camera
WS2812B LED ring
MAX98357A I2S amplifier
INMP441 I2S microphone
1S battery
TP4056 charger/protection module
MT3608 boost converter
shared 5 V rail for early V0 testing
common ground
```

The simulation does not replace these tests:

```text
power rail measurement
servo scan
servo position read
safe servo nudge
LED test
IMU test
camera capture
audio test
battery status check
distance sensor check
self-check script
integrated hello demo
```

If the simulation behaves well but the hardware fails, the hardware result wins.

If the hardware works but the simulation is inaccurate, the simulation must be updated.

## Coordinate System

The model uses the MuJoCo world coordinate system.

The robot is placed above the floor with a free joint at the root body. The simplified convention is:

```text
X axis: front/back direction
Y axis: left/right direction
Z axis: vertical direction
```

The front camera is placed toward the positive X direction.

The two legs are placed on the left and right sides of the body along the Y direction.

## Body Model

The main body is represented as a rounded compact shell.

Instead of importing exact STL files, the body uses a combination of:

```text
central box
front sphere
rear sphere
upper ellipsoid
lower ellipsoid
```

This is not exact manufacturing geometry. It is a lightweight approximation for simulation and layout reasoning.

The body is intentionally large enough to represent a bench prototype rather than a final miniaturized robot.

## Leg Model

Each leg is represented as:

```text
servo case
hinge joint
capsule leg link
side pad
rounded foot
flat contact pad
```

The hinge joints are limited to a conservative angular range.

The goal is to simulate small leg motions first, not aggressive walking.

The first useful simulated movement should be equivalent to the physical safe nudge:

```text
read current state
move one leg a small amount
return to neutral
observe body response
avoid unrealistic large motions
```

## Actuator Model

The current actuators are simple MuJoCo motors connected to the left and right leg hinge joints.

They are not calibrated to real SCS0009 torque, speed, acceleration, temperature, load, or stall behavior.

The current motor model should be treated as a placeholder until physical servo behavior is measured.

Future actuator improvements may include:

```text
approximate torque limits
velocity limits
position control
servo delay
gear backlash approximation
stall risk modeling
energy cost approximation
```

## Sensor Model

The simulation includes basic sensors:

```text
joint position sensors
joint velocity sensors
body accelerometer
body gyro
```

These sensors are useful for early control experiments and for comparing simulated state with IMU-style physical readings.

The simulated accelerometer and gyro are not currently calibrated against the real MPU-6050 module.

Future work may include:

```text
noise injection
bias drift
tilt classification
fall detection
motion event detection
comparison with real IMU logs
```

## Camera Representation

The front camera is represented with a MuJoCo camera object.

This is useful for visual inspection of the simulated robot, but it is not equivalent to the real Pi camera module.

The real camera test remains:

```text
python setup/scripts/test_camera.py
```

The simulation camera may later support:

```text
synthetic frame capture
obstacle preview
dataset generation
visual debugging
dashboard preview
```

## LED Representation

The LED ring is represented visually with small colored spheres on the top shell.

These are not simulated light-emitting electronic components. They are visual markers.

The real LED test remains:

```text
sudo -E python setup/scripts/test_leds.py
```

The simulation may later show state colors matching the real robot:

```text
blue: boot / idle
green: OK
yellow: warning
red: safe mode / error
purple: decision
orange: obstacle
white: self-check
```

## Safety Interpretation

The simulation may help identify unsafe geometry, poor leg placement, or unstable mass distribution. However, it must not be used to bypass physical safety checks.

Before moving the real robot, the software must still use:

```text
setup/microbot/safety.py
setup/scripts/scan_servos.py
setup/scripts/test_servos_safe.py
```

The real robot should not move unless:

```text
servo scan passed
servo positions are readable
movement is explicitly enabled
safe nudge is requested
safety layer allows movement
operator is supervising the robot
power has been checked
fingers are clear of joints
torque can be released on exit
```

## Recommended Simulation Workflow

Use this workflow for the first simulation phase:

```text
1. Open the XML model in MuJoCo.
2. Confirm that the model loads without XML errors.
3. Confirm that the body starts above the floor.
4. Confirm that the feet contact the floor correctly.
5. Move one hinge joint slightly.
6. Observe whether the body rotates, tips, slides, or falls.
7. Reduce movement amplitude if the model becomes unstable.
8. Adjust foot shape and mass distribution.
9. Compare with the physical robot after safe nudge tests.
10. Update the model based on real evidence.
```

## Suggested Commands

Exact commands depend on the local MuJoCo installation.

Example Python-style launch command:

```bash
python -m mujoco.viewer --mjcf simulation/microbot_round_body.xml
```

If using a custom Python viewer script, keep it outside the XML file and document it separately.

A future script may be added as:

```text
simulation/view_model.py
simulation/run_idle_test.py
simulation/run_leg_nudge_test.py
```

## Validation Checklist

A simulation update is considered acceptable when:

```text
the XML loads without errors
the robot starts in a stable pose
both leg joints are visible and controllable
the body does not explode due to invalid contacts
feet contact the floor correctly
joint limits are conservative
the model includes meaningful names for bodies, geoms, joints and sensors
the simulation notes are updated if assumptions change
```

A simulation update is not considered hardware validation unless the corresponding physical test has also been run.

## Current Status

Current simulation status:

```text
prepared
```

Meaning:

```text
the first XML model exists
the model is designed as a simplified approximation
the model is not yet calibrated against real hardware
movement behavior is not yet validated
real robot build remains separate from simulation
```

The correct public claim is:

```text
MicroBot Round V0 includes an initial simplified MuJoCo model for studying the body layout, leg placement and sensor positions before and during physical prototyping.
```

Incorrect claims:

```text
The simulation proves the robot walks.
The simulation proves the real robot is stable.
The simulation proves autonomous behavior.
The simulation is an exact replica of the printed body.
The simulated sensors are equivalent to real sensors.
The simulated actuator model matches the real SCS0009 servos.
```

## Future Improvements

Future simulation improvements may include:

```text
more accurate shell dimensions
STL mesh import for visual geometry
separate collision and visual geometry
realistic foot friction measurements
estimated battery and board masses
servo torque and speed limits
safe nudge controller
small gait experiments
fall detection
IMU log replay
comparison between real and simulated tilt
camera preview
dashboard integration
simple obstacle environment
simulation evidence reports
```

## Evidence To Collect

When simulation is tested, save evidence in:

```text
evidence/reports/
evidence/videos/
evidence/photos/
```

Useful evidence includes:

```text
screenshot of loaded model
short video of idle stability
short video of small left leg nudge
short video of small right leg nudge
simulation log
notes about instability or contact problems
comparison with real physical nudge behavior
```

## Engineering Rule

The simulation is useful only if it remains honest.

The correct development loop is:

```text
simulate
build
measure
compare
correct
document
repeat
```

The final goal is not to make a beautiful simulation. The final goal is to make a real robot that can be tested safely and improved step by step.
