# Design Requirements

## 1. Purpose of This Document

This document defines the mechanical design requirements for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this file is to translate the mechanical idea into clear requirements before creating, modifying, printing or validating CAD/STL files.

MicroBot Round V0 should be a small rounded robot body with internal electronics, visible feedback, forward sensing, two simple leg or rocker-style movement elements, safe cable routing, a reachable power switch and enough internal access for debugging.

This document does not describe a final industrial product. It describes the first physical prototype requirements.

The design goal is:

```text
Build a rounded, openable, testable and safe MicroBot body that can hold the electronics, support two servos, expose sensors, move slightly within safe limits and be documented through real evidence.
```

---

## 2. Design Status

Current design status:

```text
Mechanical requirements: prepared
Final CAD: planned
Upper shell design: planned
Lower base design: planned
Leg design: planned
Servo mount design: planned
Sensor openings: planned
Internal layout: planned
Print validation: not completed yet
Movement validation: not completed yet
```

These requirements should be updated after the first printed and assembled version.

---

## 3. Mechanical Design Philosophy

MicroBot Round V0 follows a prototype-first mechanical philosophy.

The first version must be:

```text
simple
rounded
openable
repairable
safe
printable
testable
easy to modify
compatible with real electronics
```

The first version does not need to be:

```text
perfectly miniaturized
commercially polished
fully sealed
waterproof
production-ready
fully autonomous
fully walking
mechanically final
```

The mechanical design should make real testing possible. A beautiful shell that cannot be opened, cannot route wires safely, blocks sensors or prevents servo movement is not acceptable for V0.

---

## 4. Global Design Requirements

The complete mechanical design must satisfy these global requirements:

```text
The robot must have a rounded body identity.
The robot must be able to stand on a flat surface.
The robot must contain the selected controller and sensors.
The robot must provide a safe location for the battery.
The robot must expose the camera view.
The robot must expose the distance sensor if installed.
The robot must make the LED status visible.
The robot must provide space for speaker output if audio is installed.
The robot must provide space for microphone input if audio input is installed.
The robot must support two small servos.
The robot must support two simple legs or rocker-style feet.
The legs must not collide with the shell in the safe movement range.
The wires must not interfere with moving parts.
The power switch must be reachable.
The shell must be openable for maintenance.
The design must be printable with accessible 3D printing methods.
```

If any of these requirements cannot be satisfied in the first version, the limitation must be documented.

---

## 5. Target Mechanical Architecture

The target mechanical architecture is:

```text
upper_shell
lower_base
front_sensor_area
internal_electronics_area
battery_area
left_servo_mount
right_servo_mount
left_leg_or_rocker_foot
right_leg_or_rocker_foot
LED_window_or_ring_area
camera_mount
distance_sensor_mount
speaker_opening
microphone_opening
power_switch_access
cable_routing_area
```

The robot should feel like a compact rounded MicroBot prototype, not a random exposed electronics platform.

However, early exposed or semi-open layouts are acceptable during bench testing.

---

## 6. Size Requirements

The exact size depends on the selected electronics and servos.

V0 should be large enough to fit real components without unsafe compression.

Recommended design target:

```text
small enough to look like a compact robot
large enough to fit modular electronics
large enough to keep battery safe
large enough to route wires without crushing them
large enough to mount two servos securely
```

Avoid designing the shell too small at first.

A slightly larger working prototype is better than a tiny design that cannot be assembled.

Initial size category:

```text
bench prototype size
not final miniaturized size
```

The project should not claim final miniaturization in V0.

---

## 7. Upper Shell Requirements

The upper shell defines the external identity of MicroBot Round V0.

It should satisfy:

```text
rounded external shape
smooth visual profile
no sharp external edges
enough internal clearance
front camera opening
visible LED area
possible speaker opening
possible microphone opening
easy removal from lower base
no pressure on internal boards
no pressure on camera ribbon
no pressure on battery
```

The upper shell should not be permanently glued shut during V0.

Recommended upper shell features:

```text
small screw points or alignment tabs
front sensor window
LED diffuser area
internal clearance ribs only if needed
rounded top profile
safe wall thickness
```

Avoid:

```text
very thin fragile walls
unreachable internal screws
tight pressure on electronics
blocked camera view
decorative shapes that interfere with testing
```

---

## 8. Lower Base Requirements

The lower base is the structural foundation.

It should support:

```text
main controller mounting
battery placement
power module placement
servo mounting area
wire routing
switch access
leg clearance
standing stability
shell alignment
```

The lower base must be strong enough to hold the servos during small movements.

Recommended lower base features:

```text
flat internal mounting zones
low battery area
left and right servo mounting points
front sensor support if not in upper shell
rear or side switch access
holes or channels for cable routing
screw points for shell closure
```

Avoid:

```text
thin servo walls
no cable routing space
battery area near moving legs
base shape that tips easily
shell closure that crushes wires
```

---

## 9. Body Shape Requirements

MicroBot Round V0 should have a rounded visual identity.

Shape requirements:

```text
rounded body silhouette
compact and friendly appearance
front-facing sensor direction
clear top/front orientation
stable base geometry
compatible with two side or lower legs
```

The body should make it clear where the robot is facing.

Possible design cues:

```text
camera at front
distance sensor at front
LED ring around camera or on front/top
power switch on rear or side
legs on left and right lower sides
```

The robot should not be visually ambiguous during demo.

---

## 10. Internal Layout Requirements

Internal layout must prioritize safety and maintenance.

Recommended layout:

```text
battery low and central
main controller central or rear-central
IMU near center and fixed
camera front-facing
distance sensor front-facing
LED ring visible
servos left and right
power switch reachable
power modules accessible before final closure
wires routed along shell walls
```

The internal layout must avoid:

```text
battery pressing against shell
battery pressing against controller
boost converter touching exposed conductive surfaces
servo wires crossing leg path
camera ribbon folded sharply
IMU dangling on wires
loose boards moving inside shell
unreachable power switch
```

---

## 11. Battery Placement Requirements

Battery placement is safety-critical.

The battery must be:

```text
secured
removable during early testing
low in the body
near the center of mass
protected from sharp edges
away from moving legs
not compressed by shell
not placed under high mechanical stress
```

The battery compartment or mounting area should allow:

```text
visual inspection
wire exit without pinching
safe removal
future replacement
```

Do not design a fully enclosed battery area until the battery size and thermal behavior have been validated.

---

## 12. Power Switch Requirements

The power switch must be externally reachable.

Requirements:

```text
reachable without opening the shell
not hidden below the robot
not blocked by legs
not blocked by cables
securely mounted
easy to identify during testing
usable as a quick physical stop
```

For early versions, the power switch is one of the most important safety elements.

The robot should not require software access to cut power during early movement tests.

---

## 13. Camera Requirements

The camera must have a clear forward view.

Camera opening requirements:

```text
front-facing
not blocked by shell
not blocked by LED ring
not blocked by distance sensor
large enough for lens view
small enough to protect the camera board
aligned with body front
```

Camera mount requirements:

```text
camera fixed in place
ribbon not sharply bent
ribbon not crushed by shell
camera can be removed if needed
camera angle documented
```

The first camera goal is image capture, not advanced object recognition.

---

## 14. Distance Sensor Requirements

If a distance sensor is installed, it must face forward.

Distance sensor requirements:

```text
clear line of sight
front-facing
not recessed too deeply
not blocked by shell
not blocked by wires
aligned with movement direction
fixed firmly
```

If the distance sensor is used for obstacle safety, its physical placement becomes safety-relevant.

Poor placement can cause false readings or missed obstacles.

The design must allow distance threshold testing with real objects.

---

## 15. LED Requirements

The LED system should communicate robot state clearly.

LED placement requirements:

```text
visible during demo
not hidden under shell
not blocked by camera module
not blocked by wires
safe cable route
possible diffuser if needed
```

The LED area may be:

```text
front ring
top status window
front status window
translucent shell area
```

LED design should support state feedback:

```text
boot
idle
OK
warning
safe mode
decision cycle
obstacle
error
```

The LED ring is not only decoration. It is part of the robot’s status interface.

---

## 16. Speaker Requirements

If audio output is installed, the shell should provide a sound path.

Speaker requirements:

```text
speaker not fully enclosed without opening
speaker wires secured
speaker not pressing against battery
speaker not pressing against moving parts
sound opening or grille if possible
```

Speaker output is useful for demo, but not safety-critical.

If speaker placement is difficult, audio can remain optional in V0.

---

## 17. Microphone Requirements

If a microphone is installed, it should not be fully blocked.

Microphone requirements:

```text
small opening or sound path
not placed directly against speaker if avoidable
not loose inside shell
not blocked by mounting tape
wires secured
```

Voice recognition is not required for V0.

A microphone level test is enough for early validation.

---

## 18. IMU Mounting Requirements

The IMU is safety-critical.

IMU requirements:

```text
firmly mounted
not loose
near center of body if possible
orientation documented
not attached to flexible wires only
not placed on a moving part
not under mechanical stress
```

The IMU must move with the robot body, not independently from it.

If the IMU is loose, tilt detection is invalid.

The design should reserve a flat mounting area for the IMU.

---

## 19. Servo Mount Requirements

The servo mounts must resist small movement loads.

Servo mount requirements:

```text
left and right symmetrical placement
servo body fixed firmly
screws accessible
servo horn accessible
servo wires not strained
servo can be removed for repair
mount does not flex excessively
servo axis documented
```

The mount must support:

```text
servo scan
position read
safe nudge
return to neutral
small turn attempt
small forward attempt
```

The mount does not need to support aggressive walking in V0.

---

## 20. Leg and Foot Requirements

The legs or rocker feet are the first physical movement interface.

Requirements:

```text
simple geometry
rounded contact surface
left and right symmetry
compatible with servo horn
strong enough for repeated small motion
not too thin near servo connection
safe edge profile
clear movement range
```

The first leg design should support small movement only.

Initial safe movements:

```text
small left nudge
small right nudge
both legs return to neutral
small forward attempt
small turn attempt
stop
```

The design should not assume full walking before testing.

---

## 21. Leg Clearance Requirements

Legs must not collide with:

```text
upper shell
lower base
wires
battery
sensor boards
servo cables
mounting tape
table surface in unintended ways
```

Clearance must be tested:

```text
with power off
with legs attached
with shell open
with shell partially closed
with shell fully closed
during safe servo nudge
```

If clearance fails, reduce servo range or modify the mechanical design.

---

## 22. Standing Stability Requirements

The robot must stand on a flat surface before movement.

Stability requirements:

```text
robot does not tip immediately
left and right sides balanced
battery does not make robot front-heavy
legs contact surface predictably
center of mass not too high
robot stable enough for small movements
```

Standing stability should be tested on:

```text
desk surface
mat surface
floor surface if safe
```

Avoid testing near table edges.

---

## 23. Surface Contact Requirements

Foot surface contact affects movement.

The design should consider:

```text
friction
slipping
rocking behavior
contact patch
layer line direction
surface material
```

Possible improvements:

```text
rubber pads
TPU inserts
slightly flattened contact area
textured foot surface
different print orientation
```

Do not overcomplicate the first foot design. Test simple versions first.

---

## 24. Cable Routing Requirements

Mechanical design must reserve space for wiring.

Cable routing requirements:

```text
wires do not cross leg path
battery wires not pinched
camera ribbon gently curved
servo cables strain-relieved
sensor wires short but not tight
shell can open without tearing wires
connectors remain reachable
```

Design should include one or more of:

```text
wire channels
open internal wall areas
small tie points
mounting zones
space behind controller
space along shell wall
```

If wiring cannot be routed safely, the shell design must change.

---

## 25. Shell Closure Requirements

The shell must close without damaging components.

Closure requirements:

```text
no pressure on battery
no pressure on camera ribbon
no pressure on GPIO header
no pressure on servo wires
no pressure on boost converter
no wires crushed between shell halves
alignment points fit
screw holes accessible if used
```

The first shell should be easy to reopen.

Permanent closure is not allowed in V0 until validation is complete.

---

## 26. 3D Printing Requirements

The design should be printable with common 3D printers.

Printing requirements:

```text
reasonable wall thickness
not too many fragile thin features
limited impossible overhangs
support strategy considered
holes sized with tolerance
servo mount strength considered
flat surfaces for mounting if needed
parts not too large for printer bed
```

Recommended materials:

```text
PLA for first fit tests
PETG for more durable later version
TPU only for feet/grip experiments
```

The first print may require sanding, drilling or minor cleanup.

This is acceptable if documented.

---

## 27. Tolerance Requirements

The design must account for real-world tolerances.

Tolerances needed for:

```text
servo fit
screw holes
board fit
camera opening
LED opening
battery clearance
shell closure
leg clearance
wire space
```

Do not design holes and slots at exact theoretical dimensions without clearance.

Prototype recommendation:

```text
leave extra clearance for electronics
test fit before finalizing CAD
document every tight area
```

---

## 28. Fastener Requirements

The design may use screws, standoffs, tape or printed clips.

Recommended V0 approach:

```text
screws for servos
tape or standoffs for electronics
removable shell screws if possible
temporary mounting for early layout
```

Avoid:

```text
permanent glue on critical electronics
clips that break after one opening
hidden screws impossible to reach
servo mounts that require breaking the shell
```

Servos must be mounted more securely than lightweight sensors.

---

## 29. Maintenance Requirements

The robot must be serviceable.

Maintenance requirements:

```text
open shell without destroying robot
remove battery
access power switch wiring
access controller
access camera ribbon
access servo connectors
replace a servo
adjust cable routing
inspect wires after movement
```

A V0 prototype that cannot be repaired is not acceptable.

---

## 30. Safety Requirements

Mechanical safety requirements:

```text
no sharp edges near wires
no battery compression
no moving parts catching wires
no loose internal boards
no unstable standing position
no leg movement near exposed fragile parts
no hidden power switch
no table-edge testing
```

The design must support safe mode physically.

Safe mode means:

```text
robot can stop movement
servos can hold or release safely
robot does not trap wires
robot does not fall because of shell imbalance
```

---

## 31. Evidence Requirements

Every mechanical validation should produce evidence.

Required evidence for mechanical progress:

```text
printed part photos
fit test photos
internal layout photos
servo mount photos
leg clearance video
safe nudge video
standing stability photo
notes about failures
notes about modifications
```

Evidence should be stored in:

```text
mechanical/photos/
evidence/photos/
evidence/videos/
mechanical/print_notes.md
hardware/assembly_notes.md
```

---

## 32. Mechanical Validation Checklist

### Body

```text
[ ] rounded body shape exists
[ ] upper shell printed or modeled
[ ] lower base printed or modeled
[ ] shell can open
[ ] shell can close without crushing wires
[ ] body stands on flat surface
```

### Electronics Fit

```text
[ ] controller fits
[ ] battery fits
[ ] IMU fits
[ ] camera fits
[ ] LED ring fits
[ ] distance sensor fits
[ ] speaker fits if used
[ ] microphone fits if used
```

### Servo and Legs

```text
[ ] left servo fits
[ ] right servo fits
[ ] servo horns fit
[ ] left leg attaches
[ ] right leg attaches
[ ] legs clear shell
[ ] legs clear wires
[ ] safe movement range exists
```

### Sensor Exposure

```text
[ ] camera view clear
[ ] distance sensor clear
[ ] LED visible
[ ] speaker opening available if needed
[ ] microphone opening available if needed
```

### Safety

```text
[ ] battery not compressed
[ ] power switch reachable
[ ] no sharp edges near wires
[ ] no loose internal boards
[ ] robot stable enough for testing
```

---

## 33. Mechanical Validation Tests

### M-TEST-001 — Empty Shell Fit

Goal:

```text
verify upper shell and lower base fit together
```

Pass criteria:

```text
shell aligns
no major warping
can open and close
```

### M-TEST-002 — Electronics Fit

Goal:

```text
verify electronics fit inside body
```

Pass criteria:

```text
components fit without force
battery is not compressed
controller is not stressed
```

### M-TEST-003 — Sensor Exposure

Goal:

```text
verify camera, distance sensor and LED are visible/usable
```

Pass criteria:

```text
camera image not blocked
distance sensor line of sight clear
LED visible during demo
```

### M-TEST-004 — Servo Fit

Goal:

```text
verify servo mounts hold servos securely
```

Pass criteria:

```text
servos do not shift during manual inspection
servo screws accessible
wires not strained
```

### M-TEST-005 — Leg Clearance

Goal:

```text
verify legs can move without collision
```

Pass criteria:

```text
manual clearance passes
safe servo nudge passes
no wire interference
```

### M-TEST-006 — Standing Stability

Goal:

```text
verify robot can stand safely
```

Pass criteria:

```text
robot stands on flat surface
does not tip easily
center of mass acceptable
```

---

## 34. Known Design Risks

Known risks:

```text
body too small for electronics
battery too large
servo mounts too weak
legs collide with shell
robot too top-heavy
camera ribbon too short
LED ring not visible enough
distance sensor blocked by shell
wires interfere with legs
shell cannot close after wiring
feet slip on smooth surfaces
```

These risks must be checked during the first physical build.

---

## 35. Design Change Rules

Whenever the mechanical design changes, update:

```text
mechanical/design_requirements.md
mechanical/print_notes.md
mechanical/README.md if structure changes
hardware/assembly_notes.md
hardware/wiring.md if cable routing changes
hardware/power_budget.md if battery position or power modules change
docs/current_status.md
docs/limitations.md
CHANGELOG.md
```

No major physical design change should remain undocumented.

---

## 36. Public Claim Rules

Do not claim:

```text
final mechanical design
validated walking
production-ready shell
fully miniaturized body
commercial enclosure
reliable locomotion
```

unless real evidence exists.

Correct early claim:

```text
MicroBot Round V0 defines mechanical requirements for a rounded, openable and testable bench robot body with sensor openings, internal electronics space, servo mounts and simple leg movement.
```

Correct later claim after validation:

```text
MicroBot Round V0 printed body was fit-tested with electronics and validated for limited safe leg movement without mechanical collision.
```

---

## 37. Final Design Requirement Statement

The mechanical design of MicroBot Round V0 must make the robot real without making it untestable.

The design must support:

```text
a rounded identity
safe internal electronics
visible feedback
basic perception
two-servo movement
stable standing
safe cable routing
easy maintenance
evidence collection
future iteration
```

The first body does not need to be perfect.

It needs to be the first physical structure that allows MicroBot to wake up, sense, move carefully, stop safely and be improved.

That is the correct design requirement for MicroBot Round V0.
