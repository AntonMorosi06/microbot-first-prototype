# Limitations

## 1. Purpose of This Document

This document defines the current limitations of **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this file is to keep the project technically honest, credible and safe. MicroBot Round V0 is an early prototype, not a finished autonomous robot. Its purpose is to validate the first physical, electronic, software and safety foundations of a small rounded robotic platform.

This document explains what the project can reasonably claim, what it cannot claim yet, what remains planned, and what must be validated before future claims are made.

Clear limitations are not a weakness. They are part of serious engineering documentation.

---

## 2. Current Project Limitation Summary

MicroBot Round V0 is currently in the **prepared** stage.

The repository structure and documentation baseline are being created, but the physical robot has not yet been fully assembled, tested or validated.

Current global limitations:

```text
The physical robot is not fully built yet.
The hardware has not been fully validated yet.
The power system has not been tested under real load yet.
The sensors have not been tested as an integrated system yet.
The servo movement has not been hardware-validated yet.
The safety layer is planned but not fully implemented yet.
The autonomy layer is planned but not fully implemented yet.
The dashboard is planned but not fully implemented yet.
The simulation is planned but not validated against hardware yet.
The robot does not yet perform full autonomous navigation.
The robot does not yet perform full learning behavior.
The robot does not yet support swarm behavior.
The robot does not yet support validated docking behavior.
The robot does not yet support drone observer integration.
```

These limitations must remain visible until the corresponding features are implemented and tested.

---

## 3. What MicroBot Round V0 Is

MicroBot Round V0 is intended to be:

```text
A first rounded physical bench prototype.
A small robot body and hardware integration experiment.
A safety-aware startup and sensing platform.
A limited movement validation platform.
A basic perception and logging platform.
A foundation for future autonomous behavior.
A physical proof-of-work for the MicroBot ecosystem.
```

The project is valid even if the first version moves only slightly.

The main success criterion is not advanced locomotion. The main success criterion is a real robot that can wake up, check itself, sense basic conditions, move safely within limits, stop when unsafe and save evidence.

---

## 4. What MicroBot Round V0 Is Not Yet

MicroBot Round V0 is not yet:

```text
A complete autonomous robot.
A general-purpose AI robot.
A fully self-learning robot.
A fully validated walking robot.
A commercial robotic product.
A swarm robotics platform.
A docking robot.
A magnetic aggregation system.
A drone-integrated robotic platform.
A fully miniaturized MicroBot module.
A validated AI embodiment platform.
A replacement for professional robotics hardware.
```

These may be future directions, but they are not current validated capabilities.

The repository must not describe them as completed features.

---

## 5. Hardware Limitations

The hardware layer is expected to use small development boards and modular components.

This makes the robot easier to build, test and repair, but it also creates several limitations.

### 5.1 Prototype-Level Electronics

MicroBot Round V0 is not expected to use a custom PCB in its first version.

This means:

```text
Wiring may be less compact.
Connections may be more fragile.
Internal space may be inefficient.
Cable routing may be difficult.
Electrical noise may be higher.
Power distribution may be less clean.
Assembly may require manual adjustment.
```

This is acceptable for V0 as long as the limitations are documented and the system remains safe.

### 5.2 Power System Limitations

The power system may be one of the weakest parts of the first prototype.

Possible limitations:

```text
Servo current spikes may cause voltage drops.
Battery capacity may be limited.
Runtime may be short.
Power rails may require adjustment.
A shared power rail may be unstable under load.
Battery voltage monitoring may not exist in the first build.
Charging may require manual supervision.
```

The robot must not be marked as hardware-validated until the power system has been tested under realistic load.

### 5.3 Battery Limitations

If MicroBot Round V0 uses a LiPo or lithium-ion battery, the battery introduces safety and reliability limitations.

Possible limitations:

```text
Battery charging requires care.
Battery protection must be verified.
Battery voltage may drop during servo movement.
Battery state may not be accurately measured.
Low battery conditions may cause unstable behavior.
Battery placement affects weight distribution.
```

Movement should be blocked or reduced when power instability is detected.

### 5.4 Sensor Limitations

The first sensor set is expected to be simple.

Possible sensor limitations:

```text
The IMU may drift.
The IMU may require calibration.
Camera-only obstacle detection may be unreliable.
A single distance sensor only sees one direction.
Microphone input may be noisy.
Battery monitoring may be missing.
CPU temperature may only approximate internal thermal state.
```

V0 perception should be described as basic sensing, not full environmental understanding.

### 5.5 Servo Limitations

The first movement system is expected to use two small servos.

Possible limitations:

```text
Movement range is limited.
Torque is limited.
Speed is limited.
Leg motion may be unstable.
Servo feedback may be noisy or incomplete.
Servos may draw high current during load.
Repeated movement may heat the servos.
A two-servo robot cannot perform complex locomotion.
```

The first movement demo should be a safe nudge or small movement, not full walking.

---

## 6. Mechanical Limitations

The first physical body is expected to be a 3D printed prototype.

This creates several mechanical limitations.

### 6.1 Shell Limitations

The first shell may not be final.

Possible shell limitations:

```text
The body may be larger than the final target.
The shell may require manual sanding or adjustment.
The shell may not close perfectly.
The mounting points may not align perfectly.
The internal layout may be crowded.
The camera opening may need adjustment.
The LED ring may not be perfectly centered.
The speaker opening may reduce sound quality.
```

A rough but functional shell is acceptable for V0.

### 6.2 Leg and Foot Limitations

The rounded leg or rocker-style foot design may produce only limited movement.

Possible limitations:

```text
The robot may rock instead of walking cleanly.
The robot may move only a small distance.
Movement may depend heavily on surface friction.
Feet may slip on smooth surfaces.
Feet may catch on rough surfaces.
Leg clearance may be limited by the shell.
Servo alignment may affect movement quality.
```

The first movement goal should be controlled motion, not perfect locomotion.

### 6.3 Weight Distribution Limitations

The robot may be sensitive to internal component placement.

Possible limitations:

```text
Battery position may shift the center of mass.
Cable placement may affect balance.
Camera placement may affect front weight.
Servo placement may affect turning behavior.
Uneven weight may cause one leg to behave differently.
```

Mechanical validation must include balance and stability checks.

### 6.4 Material Limitations

If the body is printed in PLA, PETG or similar materials, each material has limitations.

Possible limitations:

```text
PLA may deform with heat.
PLA may crack under repeated stress.
PETG may flex more than expected.
Layer lines may affect rounded foot smoothness.
Printed parts may vary between printers.
Small holes may require drilling or cleanup.
```

Mechanical parts should be treated as prototype parts, not final manufacturing-ready parts.

---

## 7. Software Limitations

The first software version is expected to be simple and modular.

This creates deliberate limitations.

### 7.1 Driver Limitations

The first hardware drivers may be minimal.

Possible limitations:

```text
Drivers may only support the exact hardware selected for V0.
Error handling may be incomplete at first.
Sensor calibration may be basic.
Servo control may support only safe movement presets.
Camera code may support only still images.
Audio code may support only simple speech or tones.
```

This is acceptable as long as each driver is tested and documented.

### 7.2 Logging Limitations

The first logging system may not be perfect.

Possible limitations:

```text
Logs may be local only.
Logs may not yet stream to dashboard.
Logs may not include every sensor field.
Log timestamps may depend on controller clock accuracy.
Large logs may not be automatically compressed.
Video evidence may not be stored directly in Git.
```

The first requirement is that logs exist and are readable.

### 7.3 Error Handling Limitations

The first version may not handle every possible failure.

Known possible failure cases:

```text
Sensor unplugged during runtime.
Servo disconnect during movement.
Camera unavailable after boot.
Distance sensor returns invalid values.
Battery voltage drops suddenly.
Python script crashes during demo.
Filesystem becomes read-only or full.
```

The project should progressively add error handling after each real failure is observed.

### 7.4 Dashboard Limitations

The dashboard is planned, but it may not exist in the first hardware bring-up.

Possible limitations:

```text
Dashboard may initially show mock data only.
Manual control may not be implemented at first.
Live camera preview may not be available.
Real-time telemetry may be delayed.
Dashboard commands may be limited to safe actions only.
Emergency stop must not rely only on the dashboard.
```

The robot must remain safe even if the dashboard fails.

---

## 8. Safety Limitations

The safety layer is essential, but V0 safety is still limited.

### 8.1 Safety Is Not Absolute

The safety layer can reduce risk, but it cannot eliminate all risk.

Possible remaining risks:

```text
Servo movement may still surprise the operator.
A cable may disconnect during movement.
A sensor may report incorrect data.
A battery issue may occur unexpectedly.
A mechanical part may fail.
The robot may tip over despite safety checks.
```

For this reason, early testing must be supervised.

### 8.2 Tilt Detection Limitations

Tilt detection depends on IMU readings and thresholds.

Possible limitations:

```text
Thresholds may require tuning.
IMU noise may cause false positives.
Fast movement may temporarily look like tilt.
Slow tilt may be detected later than expected.
Lift detection may be unreliable without additional sensors.
```

Tilt stop should be tested repeatedly before public demo.

### 8.3 Obstacle Detection Limitations

Obstacle detection may use one forward-facing distance sensor.

Possible limitations:

```text
Only objects in front of the sensor are detected.
Transparent or reflective objects may be detected poorly.
Small objects may be missed.
Side obstacles may not be detected.
Camera-based obstacle detection may be unreliable in V0.
```

Obstacle detection should be described as basic proximity sensing.

### 8.4 Emergency Stop Limitations

The emergency stop system may initially be manual or software-based.

Possible limitations:

```text
Software stop may fail if the process crashes.
Dashboard stop may fail if Wi-Fi disconnects.
Physical power switch may be the most reliable stop method.
A real hardware emergency stop may be added later.
```

During early testing, the operator must always be able to cut power physically.

---

## 9. Autonomy Limitations

MicroBot Round V0 will use limited autonomy.

This is intentional.

### 9.1 No General Understanding

The robot does not truly understand the full environment.

It may read:

```text
orientation
distance
camera frame
last movement result
system status
```

But these readings do not mean the robot has full spatial understanding.

Correct description:

```text
MicroBot Round V0 uses basic sensor readings to select limited safe actions.
```

Incorrect description:

```text
MicroBot Round V0 fully understands its environment.
```

### 9.2 Limited Action Set

The first autonomous action set is intentionally small.

Allowed V0 actions:

```text
STOP
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
```

The robot should not attempt complex behavior in V0.

Not included yet:

```text
full walking
mapping
path planning
object manipulation
docking
multi-agent coordination
gesture-based control
self-directed learning
```

### 9.3 Rule-Based Behavior

The first autonomy layer is expected to be a state machine or rule-based action selector.

This means:

```text
The robot follows predefined logic.
The robot does not invent new movement strategies.
The robot does not learn complex behavior by itself.
The robot does not optimize movement through reinforcement learning yet.
```

Rule-based autonomy is still valid because it creates a safe and inspectable foundation.

### 9.4 AI Agent Limitations

A future LLM or AI agent may suggest actions, but it must not directly control servos.

Limitations:

```text
The AI agent can only suggest predefined safe actions.
The safety layer must approve every action.
The AI agent cannot bypass hardware limits.
The AI agent cannot receive unrestricted control over motors.
The AI agent cannot be treated as proof of real understanding.
```

The correct architecture is:

```text
AI suggestion -> predefined action -> safety check -> hardware execution
```

Not:

```text
AI output -> raw servo movement
```

---

## 10. Movement and Locomotion Limitations

MicroBot Round V0 should not be described as a fully walking robot until movement is validated.

### 10.1 Movement Scope

The first movement scope is:

```text
small leg nudge
return to neutral
small turn
small forward attempt
stop
```

The first version may only move a few centimeters or less.

That is acceptable.

### 10.2 Walking Limitations

Full walking may not be possible or reliable in V0.

Possible issues:

```text
Two-servo locomotion is mechanically limited.
Rounded feet may slip.
Surface friction affects movement.
Center of mass may be too high.
Battery placement may affect balance.
Movement may require tuning.
Servo torque may be insufficient.
```

The repository should use the term “limited safe movement” until real walking is demonstrated repeatedly.

### 10.3 Movement Validation Requirements

A movement should not be marked as validated unless:

```text
It is repeated successfully.
It stays within safe servo limits.
It does not reset the controller.
It does not cause dangerous instability.
It is logged.
It is captured as evidence.
```

A single successful movement is not enough for demo-ready status.

---

## 11. Perception Limitations

MicroBot Round V0 perception is basic.

### 11.1 Camera Limitations

The camera may initially be used only for snapshots.

Possible limitations:

```text
No real-time vision at first.
No reliable object recognition at first.
No depth perception from a single camera.
Lighting affects image quality.
Motion blur may affect captured frames.
Camera processing may be slow.
```

The correct claim is:

```text
MicroBot captures camera frames as visual evidence and future perception input.
```

Not:

```text
MicroBot sees and understands everything around it.
```

### 11.2 Audio Limitations

Audio may initially support only basic speech or simple microphone level reading.

Possible limitations:

```text
Speech may sound robotic.
Microphone input may be noisy.
Voice command recognition may not exist yet.
Wake word detection may not exist yet.
Audio latency may exist.
```

The robot may speak status messages before it can understand spoken commands.

### 11.3 Distance Sensor Limitations

Distance sensing may be narrow and local.

Possible limitations:

```text
Only one direction may be measured.
Certain materials may be detected poorly.
Readings may fluctuate.
Sensor range may be limited.
Sensor placement affects results.
```

Distance sensing should be used as a safety helper, not as a full navigation system.

---

## 12. Simulation Limitations

The simulation layer is useful but limited.

### 12.1 Simulation Is Not Hardware Validation

A movement that works in simulation is not automatically valid on the real robot.

Simulation may ignore or simplify:

```text
servo backlash
battery voltage drops
wire interference
surface texture
material flex
sensor noise
assembly imperfections
weight distribution errors
friction variation
```

Simulation results must be marked as simulation-only until compared with real hardware.

### 12.2 Simplified Body Model

The first simulation may use simplified geometry.

Possible limitations:

```text
Body may be represented by boxes or simple shapes.
Feet may be approximated.
Mass distribution may be estimated.
Joint friction may be simplified.
Contact behavior may not match real surfaces.
```

This is acceptable if clearly documented.

### 12.3 No Sim-to-Real Claim Yet

The project should not claim sim-to-real transfer until:

```text
The real robot movement is measured.
The simulation movement is compared.
Parameters are tuned.
Results are documented.
```

Until then, simulation is a design and testing aid, not proof.

---

## 13. Dashboard Limitations

The dashboard is planned as a control and monitoring layer, but it has limitations.

### 13.1 Dashboard Is Not a Safety Replacement

The dashboard may help monitor and control MicroBot, but it must not replace internal safety.

Possible dashboard failures:

```text
Wi-Fi disconnects.
Browser freezes.
Backend crashes.
Command latency occurs.
Camera stream fails.
```

The robot must still stop safely without dashboard access.

### 13.2 Manual Control Limitations

Manual control should only send safe high-level actions.

Allowed manual commands:

```text
STOP
SAFE_MODE
SELF_CHECK
TAKE_PHOTO
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
RETURN_TO_IDLE
```

Disallowed manual commands:

```text
unbounded servo movement
direct raw motor control
unsafe speed override
safety bypass
```

---

## 14. Evidence Limitations

Evidence collection is necessary, but evidence can still be incomplete.

### 14.1 Logs May Not Prove Everything

A log can show what the software recorded, but it may not prove the complete physical behavior.

For strong evidence, combine:

```text
session log
terminal output
photo
video
camera snapshot
final report
```

### 14.2 Photos and Videos May Be Large

Large videos should not necessarily be committed directly to Git.

Possible alternatives:

```text
GitHub Releases
external portfolio page
compressed demo clip
linked video
selected screenshots
```

### 14.3 Evidence Must Match Claims

If the README claims a feature works, evidence should exist.

Example:

```text
Claim: tilt stop works.
Required evidence: log event + video or test report.
```

Without evidence, the feature should remain prepared, planned or bench-tested depending on actual state.

---

## 15. Repository and Publication Limitations

The repository must remain clean and safe to publish.

### 15.1 No Private Information

The repository should not include:

```text
Wi-Fi passwords
API keys
personal addresses
private images
private documents
unreviewed certificates
raw credentials
hardware serial numbers if sensitive
large personal files
```

### 15.2 No Exaggerated Claims

The repository should not claim:

```text
completed AI robot
human-like understanding
full autonomous navigation
real swarm behavior
validated docking
validated drone integration
commercial readiness
```

unless these are actually implemented and tested.

### 15.3 License Compatibility

If external designs, code, STL files or references are used, their licenses must be checked.

If a project is used only as inspiration, that should be stated clearly.

If any external file is copied or modified, attribution and license terms must be respected.

---

## 16. GrowBot Reference Limitation

MicroBot Round V0 may be inspired by GrowBot-style ideas such as a small rounded body, two-leg movement, basic sensors, startup demo and safety-aware behavior.

However:

```text
MicroBot Round V0 must remain its own project.
External STL files should not be reused without checking license terms.
External code should not be copied without license compatibility.
References should be documented in references/growbot_reference_notes.md.
The public repository should make clear what is original, what is inspired and what is externally referenced.
```

If an external design uses a non-commercial license, MicroBot must not reuse it in a commercial context unless the license allows it or permission is obtained.

---

## 17. Ethical and Safety Limitations

MicroBot Round V0 is a small robotics prototype, but safety and ethics still matter.

The project should not be used for:

```text
surveillance of people without consent
unsafe autonomous movement near people or animals
operation near stairs, roads or dangerous areas
battery experiments without supervision
bypassing safety limits
claiming capabilities that are not real
```

Camera and microphone features should be used responsibly.

If recording people, consent should be considered.

---

## 18. Current Public Claim

The current correct public claim is:

```text
MicroBot Round V0 is a prepared robotics repository for the first rounded physical bench prototype of the MicroBot project. It defines the architecture, build plan, safety strategy and implementation structure for a small robot that will power on, run self-checks, read sensors, move safely, react to unsafe conditions and save evidence.
```

The current incorrect public claim is:

```text
MicroBot Round V0 is already a complete autonomous AI robot.
```

The project should always use the correct claim until real hardware evidence supports stronger statements.

---

## 19. Future Capabilities Not Yet Validated

The following capabilities are future directions, not current validated features:

```text
full walking
environment mapping
object recognition
gesture control
voice command recognition
LLM-based action planning
reinforcement learning
self-improving movement
magnetic docking
charging dock
drone observer
multi-robot communication
swarm robotics
MicroBot OS integration
cloud telemetry
mobile app control
custom PCB
miniaturized final body
```

Each future capability must go through:

```text
planned -> prepared -> mocked -> validated-offline -> bench-tested -> hardware-validated -> integrated -> demo-ready
```

depending on its nature.

---

## 20. Definition of Limitation Removal

A limitation can be removed only when there is evidence.

Example:

```text
Limitation: The robot does not yet stop on tilt.
```

This limitation can be removed only after:

```text
IMU tilt readings are implemented.
Safety threshold is defined.
Movement is blocked when tilted.
The behavior is tested on hardware.
A log event is generated.
Evidence is saved.
The documentation is updated.
```

Until then, the limitation remains.

This rule applies to every major feature.

---

## 21. Final Limitation Statement

MicroBot Round V0 is an early but serious robotic prototype.

Its current limitations are intentional. They keep the project safe, honest and buildable.

The first version does not need to be a complete autonomous robot. It needs to become a real physical foundation that can be powered, tested, observed, moved carefully, stopped safely and documented.

The project becomes stronger when its limits are clear.

A credible V0 does not say:

```text
I solved robotics.
```

A credible V0 says:

```text
I built the first real layer, tested it, documented it and know exactly what still needs to be improved.
```

That is the correct foundation for MicroBot Round V0.
