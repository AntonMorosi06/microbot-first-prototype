# Print Notes

## 1. Purpose of This Document

This document records the 3D printing notes for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this file is to document how the mechanical parts are printed, inspected, modified and validated. MicroBot Round V0 is a prototype, so the first prints may not be perfect. That is acceptable as long as every issue is recorded and used to improve the next version.

This file should be updated after every print, test fit, mechanical failure, servo clearance test or shell modification.

The central rule is:

```text
Do not treat a printed part as validated until it has been physically inspected, assembled and tested with the real hardware.
```

---

## 2. Print Notes Status

Current status:

```text
Print notes: prepared
First print completed: not confirmed
Upper shell printed: not confirmed
Lower base printed: not confirmed
Left leg printed: not confirmed
Right leg printed: not confirmed
Servo mounts printed: not confirmed
Fit testing completed: not yet
Movement clearance completed: not yet
Mechanical validation completed: not yet
```

This document is prepared for future print records.

---

## 3. Mechanical Parts to Print

The planned MicroBot Round V0 mechanical parts are:

```text
upper_shell
lower_base
left_leg
right_leg
left_servo_mount
right_servo_mount
camera_mount
distance_sensor_mount
LED_mount_or_window
speaker_opening_or_grille
microphone_opening
battery_holder_or_battery_area
power_switch_holder
optional_cable_guides
```

Not every part must be printed separately. Some features may be integrated directly into the shell or base.

For V0, simplicity is preferred.

---

## 4. Print Philosophy

The first printed version should prioritize fit and testing.

The first prints should prove:

```text
the parts can be printed
the shell can open and close
electronics can fit
the camera is not blocked
the LED is visible
the IMU can be fixed
the battery can be secured
the servos can mount
the legs can move safely
wires can be routed without collision
```

The first prints do not need to prove:

```text
final aesthetics
perfect surface finish
commercial manufacturing quality
full miniaturization
reliable walking
final locomotion mechanics
```

A rough printed shell that can be opened and tested is better than a polished shell that cannot be debugged.

---

## 5. Recommended Materials

### PLA

PLA is recommended for the first fit tests.

Advantages:

```text
easy to print
low warping
good dimensional accuracy
cheap
good for checking shape and fit
```

Limitations:

```text
can crack under stress
can deform with heat
not ideal for long-term mechanical stress
not ideal near hot components
```

Recommended use:

```text
first upper shell
first lower base
first fit-test legs
camera mount
sensor mount
LED mount
```

### PETG

PETG is recommended after the design is more stable.

Advantages:

```text
more durable than PLA
better impact resistance
better heat resistance
slightly flexible
```

Limitations:

```text
can string more
may require slower printing
may have less crisp details
can be harder to tune
```

Recommended use:

```text
later shell versions
servo mounts
legs
parts under repeated handling
```

### TPU

TPU may be useful for feet or grip pads.

Advantages:

```text
flexible
good friction
useful for contact surfaces
```

Limitations:

```text
harder to print
not ideal for full structural shell
may deform under load
```

Recommended use:

```text
optional foot pads
rubber-like grip inserts
vibration damping pads
```

---

## 6. Recommended Initial Print Settings

These are starting values only. They should be adjusted based on the printer, material and part geometry.

### PLA Starting Settings

```text
Layer height: 0.20 mm
Wall count: 3
Top layers: 4 or more
Bottom layers: 4 or more
Infill: 15% to 25%
Nozzle temperature: according to filament
Bed temperature: according to filament
Supports: as needed
Cooling: enabled
Print speed: moderate
```

### PETG Starting Settings

```text
Layer height: 0.20 mm
Wall count: 3 or 4
Top layers: 4 or more
Bottom layers: 4 or more
Infill: 20% to 35%
Nozzle temperature: according to filament
Bed temperature: according to filament
Supports: as needed
Cooling: moderate
Print speed: slower than PLA if needed
```

### TPU Starting Settings

```text
Layer height: 0.20 mm
Wall count: 3
Infill: 15% to 30%
Speed: slow
Retraction: tuned carefully
Supports: avoid if possible
```

Exact temperatures should follow the filament manufacturer’s recommendations.

---

## 7. Wall Thickness Requirements

Recommended wall thickness depends on part function.

### Shell Parts

Recommended:

```text
minimum 2.0 mm wall thickness
prefer 2.4 mm to 3.0 mm in stress areas
avoid very thin decorative walls
```

### Servo Mount Areas

Recommended:

```text
stronger walls around servo screws
extra material around servo axis
avoid thin posts
avoid unsupported screw towers
```

### Legs and Feet

Recommended:

```text
thicker near servo horn connection
rounded contact surface
no fragile thin necks
enough infill for repeated movement
```

### Sensor Mounts

Recommended:

```text
lightweight but not fragile
holes with tolerance
no pressure on sensor board
```

---

## 8. Infill Notes

The first shell does not need extremely high infill.

Recommended approach:

```text
shell: 15% to 25% infill
base: 20% to 35% infill
servo mounts: 30% to 50% infill if separate
legs: 30% to 50% infill depending on strength
small brackets: 30% to 60% infill
```

More infill increases strength but also increases weight.

Weight affects center of mass and movement.

Do not make the shell unnecessarily heavy.

---

## 9. Support Strategy

Supports should be minimized where possible.

Design should avoid:

```text
deep unsupported overhangs
tiny unsupported tabs
internal supports that are hard to remove
supports inside cable channels
supports inside screw holes
supports inside camera opening
```

After printing, remove supports carefully.

Support damage should be documented.

If support removal damages the part, the CAD should be modified.

---

## 10. Print Orientation

Print orientation affects strength and surface quality.

General guidance:

```text
print shell to preserve rounded external surface if possible
print servo mounts so layer lines do not split under load
print legs so the servo horn connection is strong
print small brackets with screw holes cleanly oriented
```

Legs and servo mounts should be oriented for strength, not only appearance.

If a leg cracks near the servo connection, change print orientation or increase thickness.

---

## 11. Tolerance Notes

3D prints require clearance.

Areas requiring tolerance:

```text
servo body pocket
servo horn opening
screw holes
camera board slot
LED ring opening
distance sensor opening
battery compartment
controller mounting area
shell alignment tabs
power switch opening
wire channels
```

Recommended prototype clearances:

```text
small board fit: leave extra clearance
servo fit: do not make exact zero-clearance pocket
battery fit: leave safe clearance
wires: leave more room than expected
switch opening: allow manual adjustment
```

If a part requires force to fit, update the CAD.

Do not bend electronics to fit printed geometry.

---

## 12. Hole and Screw Notes

Printed holes may be smaller than expected.

Recommended approach:

```text
make screw holes slightly oversized or post-process them
use pilot holes for self-tapping screws
avoid very thin screw posts
use washers if needed
avoid over-tightening screws
```

Servo screws must be secure but not crack the mount.

If a screw post cracks, document it and reinforce the design.

---

## 13. Post-Processing

After printing:

```text
remove supports
remove loose filament
trim sharp edges
sand rough cable-contact areas
clear holes carefully
check shell alignment
check moving part clearance
clean plastic dust
```

Do not leave sharp internal edges near wires or battery.

If sanding changes a critical dimension, document it.

---

## 14. Print Inspection Checklist

After every print, check:

```text
[ ] no major warping
[ ] no cracks
[ ] no severe layer separation
[ ] no blocked camera opening
[ ] no blocked sensor opening
[ ] no blocked screw holes
[ ] no sharp internal edges
[ ] shell halves align
[ ] servo mounts are not fragile
[ ] legs are symmetrical
[ ] battery area is safe
[ ] wire paths are usable
```

If any critical issue is found, mark the part as not validated.

---

## 15. Upper Shell Print Notes

The upper shell should be inspected for:

```text
rounded external surface quality
front camera opening
LED visibility
speaker opening if used
microphone opening if used
internal clearance
shell alignment
edge quality
ribbon cable clearance
```

Common issues:

```text
camera opening too small
LED ring hidden
shell too thin
internal supports hard to remove
sharp internal edge near camera ribbon
shell does not align with base
```

Validation requirement:

```text
camera can capture an unblocked image
LED can be seen from outside
shell can be removed without damaging wires
```

---

## 16. Lower Base Print Notes

The lower base should be inspected for:

```text
flatness
servo mount strength
battery placement
controller placement
wire routing space
switch access
shell alignment
leg clearance
base stability
```

Common issues:

```text
base warped
servo mount too weak
battery area too tight
controller does not fit
wires have no routing path
legs collide with base
switch opening misaligned
```

Validation requirement:

```text
electronics fit without force
battery is not compressed
servos can be mounted securely
legs can move through safe range
```

---

## 17. Leg and Foot Print Notes

Legs or rocker-style feet should be inspected for:

```text
left/right symmetry
servo horn fit
strength near attachment point
rounded contact quality
surface smoothness
foot friction
clearance from shell
layer orientation
```

Common issues:

```text
servo horn fit too tight
servo horn fit too loose
leg cracks near horn
rounded foot too slippery
foot catches on surface
left and right legs not symmetrical
leg collides with shell
```

Validation requirement:

```text
leg attaches securely
leg clears shell
leg can perform safe nudge
leg returns to neutral
no cracking after test
```

---

## 18. Servo Mount Print Notes

Servo mounts should be inspected for:

```text
servo pocket fit
screw hole quality
mount wall thickness
axis alignment
left/right symmetry
wire exit clearance
access to screws
```

Common issues:

```text
servo does not fit
servo is loose
screw holes crack
servo axis misaligned
wire exit blocked
mount flexes during movement
```

Validation requirement:

```text
servo remains fixed during safe nudge
servo screws are reachable
servo can be removed for repair
```

---

## 19. Sensor Mount Print Notes

Sensor mounts should be inspected for:

```text
camera alignment
distance sensor alignment
LED ring alignment
microphone opening
speaker opening
wire clearance
```

Common issues:

```text
camera sees shell edge
distance sensor blocked
LED not visible
sensor board squeezed
mount too fragile
wires exit badly
```

Validation requirement:

```text
camera image is clear
distance reading changes correctly
LED status is visible
sensor can be removed if needed
```

---

## 20. Fit Test Procedure

After printing, perform a fit test before wiring.

Procedure:

```text
1. Place upper shell and lower base together.
2. Check shell alignment.
3. Place controller inside without wires.
4. Place battery inside without wires.
5. Place IMU.
6. Place camera.
7. Place LED ring.
8. Place distance sensor.
9. Place servos.
10. Place legs.
11. Check if shell can close loosely.
12. Mark tight areas.
13. Photograph internal layout.
14. Update assembly_notes.md.
```

Pass criteria:

```text
components fit without force
battery is not compressed
camera has view
LED is visible
servos can mount
legs have clearance
shell can open again
```

---

## 21. Leg Clearance Test Procedure

Before powered movement, perform a mechanical clearance test.

Procedure:

```text
1. Mount servos with power off.
2. Attach legs.
3. Move legs manually if possible.
4. Check shell clearance.
5. Check cable clearance.
6. Partially close shell.
7. Repeat clearance check.
8. Fully close shell only if safe.
9. Run servo scan without movement.
10. Run tiny safe nudge.
11. Inspect for collision.
```

Pass criteria:

```text
legs do not hit shell
legs do not touch wires
servo wires are not strained
robot does not tip immediately
safe nudge does not damage parts
```

If any collision occurs, stop and modify the design.

---

## 22. Standing Stability Test Procedure

The robot must stand before movement.

Procedure:

```text
1. Place robot on flat surface.
2. Observe from front.
3. Observe from side.
4. Lightly touch shell and observe tipping tendency.
5. Place battery in intended position.
6. Check whether center of mass is too high or too far forward.
7. Test on one or two safe surfaces.
8. Photograph standing position.
```

Pass criteria:

```text
robot stands without immediate tipping
left and right balance is acceptable
battery placement does not create severe instability
legs contact surface predictably
```

If the robot tips easily, do not run movement tests.

---

## 23. Surface Test Notes

Different surfaces may affect movement.

Surfaces to test:

```text
desk surface
paper sheet
desk mat
smooth floor
rubber mat
wood surface
```

Record:

```text
surface type
slipping observed
sticking observed
movement distance
turning behavior
stability
```

The first public demo should use the surface where MicroBot behaves most predictably.

---

## 24. Print Record Template

Use this template for each printed part.

```text
## Print Record

Date:
Part name:
Version:
File used:
Material:
Color:
Printer:
Nozzle size:
Layer height:
Wall count:
Infill:
Supports:
Print time:
Print result:

Inspection:
- 

Fit issues:
- 

Post-processing:
- 

Test performed:
- 

Evidence:
- 

Status:
Next action:
```

---

## 25. Example Print Record

```text
## Print Record

Date: 2026-06-13
Part name: upper_shell
Version: v0.1
File used: mechanical/cad_custom/upper_shell_v0_1.stl
Material: PLA
Color: black
Printer: not recorded
Nozzle size: 0.4 mm
Layer height: 0.20 mm
Wall count: 3
Infill: 20%
Supports: yes
Print time: not recorded
Print result: pending

Inspection:
- not inspected yet

Fit issues:
- not tested yet

Post-processing:
- not completed yet

Test performed:
- none

Evidence:
- none

Status: planned
Next action: print first shell and perform empty shell fit test
```

---

## 26. Modification Record Template

Use this template when a print is modified manually.

```text
## Modification Record

Date:
Part:
Version:
Modification:
Tool used:
Reason:
Effect:
Risk:
Test repeated:
Evidence:
Next action:
```

Example:

```text
## Modification Record

Date: 2026-06-13
Part: lower_base
Version: v0.1
Modification: enlarged power switch opening
Tool used: small file
Reason: switch did not fit
Effect: switch fits with light pressure
Risk: opening edge slightly rough
Test repeated: switch fit test
Evidence: mechanical/photos/lower_base_switch_mod.jpg
Next action: update CAD for v0.2
```

---

## 27. Failure Record Template

Use this template when a part fails.

```text
## Failure Record

Date:
Part:
Version:
Failure type:
When it happened:
Description:
Likely cause:
Immediate action:
Design change needed:
Evidence:
Status:
Next action:
```

Example:

```text
## Failure Record

Date: 2026-06-13
Part: left_leg
Version: v0.1
Failure type: crack near servo horn
When it happened: during safe nudge test
Description: small crack appeared near horn connection
Likely cause: wall too thin and layer orientation weak
Immediate action: stop movement test
Design change needed: thicken horn area and change print orientation
Evidence: evidence/photos/left_leg_crack_v0_1.jpg
Status: failed
Next action: design left_leg_v0_2
```

---

## 28. Version Naming

Recommended mechanical version naming:

```text
upper_shell_v0_1
upper_shell_v0_2
lower_base_v0_1
left_leg_v0_1
right_leg_v0_1
servo_mount_left_v0_1
servo_mount_right_v0_1
```

For exports:

```text
mechanical/exports/upper_shell_v0_1.stl
mechanical/exports/lower_base_v0_1.stl
mechanical/exports/left_leg_v0_1.stl
mechanical/exports/right_leg_v0_1.stl
```

Do not overwrite validated files without backup.

Keep old versions if they explain design evolution.

---

## 29. Mechanical Status Labels

Use these labels for printed parts.

```text
planned = part described but not printed
modeled = CAD exists
exported = STL/print file exists
printed = physical print exists
inspected = print inspected
fit-tested = component fit tested
modified = manually adjusted
failed = part failed or unusable
bench-tested = works in non-integrated test
movement-tested = works in safe movement test
hardware-validated = works inside assembled robot
demo-ready = works repeatedly in demo
```

A part should not be marked hardware-validated until it works inside the assembled robot.

---

## 30. Documentation Updates After Printing

After each print, update:

```text
mechanical/print_notes.md
hardware/assembly_notes.md
docs/current_status.md
docs/limitations.md if limitation changes
CHANGELOG.md
```

If the printed part changes wiring or component layout, update:

```text
hardware/wiring.md
hardware/pinout.md if relevant
hardware/power_budget.md if battery or power placement changes
```

If the CAD changes, update:

```text
mechanical/design_requirements.md if requirements changed
mechanical/README.md if structure changed
```

---

## 31. Public Claim Rules

Do not claim:

```text
printed shell is validated
robot can walk
mechanical design is final
servo mounts are reliable
legs work correctly
body is production-ready
```

unless real evidence exists.

Correct early claim:

```text
The mechanical system defines print requirements and validation notes for a rounded MicroBot Round V0 body, but printed parts still need fit testing and movement validation.
```

Correct later claim:

```text
The MicroBot Round V0 printed body was fit-tested with electronics and completed a limited safe servo nudge without shell collision.
```

---

## 32. First Print Checklist

Before printing:

```text
[ ] STL file exists
[ ] file version named clearly
[ ] material selected
[ ] orientation checked
[ ] supports checked
[ ] wall thickness checked
[ ] servo mount strength checked if relevant
[ ] camera opening checked
[ ] LED opening checked
[ ] battery clearance checked
[ ] print settings recorded
```

After printing:

```text
[ ] supports removed
[ ] sharp edges removed
[ ] holes checked
[ ] shell alignment checked
[ ] electronics fit checked
[ ] leg clearance checked
[ ] photos taken
[ ] print record added
[ ] status updated
```

---

## 33. Final Print Notes Statement

The first MicroBot Round V0 prints are part of the engineering process.

They are not expected to be perfect.

They are expected to teach what fits, what fails, what needs more clearance, what is too fragile, what blocks sensors and what prevents safe movement.

A successful print process means:

```text
print
inspect
fit
photograph
test
record
modify
repeat
```

That process is how MicroBot Round V0 becomes a real physical robot instead of only a digital concept.
