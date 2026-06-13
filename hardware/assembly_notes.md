# Assembly Notes

## 1. Purpose of This Document

This document defines the assembly notes for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this file is to document how the physical robot should be assembled, checked, modified and prepared for testing. MicroBot Round V0 is a prototype, not a finished manufactured robot, so the assembly process must remain flexible, inspectable and easy to update.

The first assembly goal is not to build a perfect final product. The first goal is to build a safe, testable and repairable robot that can contain the electronics, support the servos, expose the sensors, route the cables, move the legs slowly and produce evidence.

Assembly must follow one central rule:

```text
Do not close the robot permanently until every internal subsystem has been tested and the wiring has been photographed.
```

---

## 2. Assembly Status

Current assembly status:

```text
Assembly plan: prepared
Mechanical parts printed: not confirmed
Electronics mounted: not confirmed
Internal wiring completed: not confirmed
Servo mounting completed: not confirmed
Shell closed: not confirmed
Physical movement tested: not yet
Hardware validation: not yet
```

This document describes the intended assembly process. Every real assembly change must be documented after it happens.

---

## 3. Assembly Philosophy

MicroBot Round V0 follows a prototype-first assembly philosophy.

The robot should be assembled in a way that allows testing, opening, modification and repair.

The first build should prioritize:

```text
accessibility
safe wiring
component visibility
easy debugging
mechanical clearance
stable mounting
repeatable tests
evidence collection
```

The first build should not prioritize:

```text
perfect miniaturization
permanent glue everywhere
fully hidden wiring
cosmetic perfection
complex internal brackets
unreachable components
irreversible assembly
```

A rough but testable robot is better than a beautiful robot that cannot be opened or debugged.

---

## 4. Assembly Order Overview

The recommended assembly order is:

```text
1. Inspect all printed parts.
2. Clean printed parts.
3. Test component fit without wiring.
4. Test leg and servo clearance.
5. Mount controller temporarily.
6. Mount sensors temporarily.
7. Mount LED ring temporarily.
8. Mount camera temporarily.
9. Mount power components temporarily.
10. Route wires without closing the shell.
11. Run individual hardware tests.
12. Mount servos and legs.
13. Run servo scan without movement.
14. Run safe servo nudge.
15. Check cable interference.
16. Close shell partially.
17. Run self-check.
18. Close shell fully only after tests pass.
19. Record evidence.
20. Update documentation.
```

The robot should not be fully closed before power, sensors and servo clearance have been tested.

---

## 5. Required Assembly Materials

Recommended assembly materials:

```text
3D printed upper shell
3D printed lower base shell
3D printed left leg
3D printed right leg
servo horns
servo screws
main controller
IMU
camera
LED ring
distance sensor
speaker
microphone
power switch
battery
power modules
wires
mounting tape
small screws
standoffs
zip ties
heat-shrink tubing
electrical tape
multimeter
small screwdriver
phone or camera for evidence
```

Optional materials:

```text
hot glue
rubber pads
foam pads
cable labels
threaded inserts
small printed cable guides
transparent LED diffuser
small terminal block
```

Temporary mounting is acceptable in V0 if it is safe and documented.

---

## 6. Printed Part Inspection

Before mounting electronics, inspect all printed parts.

Check:

```text
shell cracks
warping
sharp edges
poor layer adhesion
blocked holes
support residue
servo opening accuracy
camera opening accuracy
LED opening accuracy
switch access
charging access
leg clearance
base flatness
```

If a printed part has defects, document them in `mechanical/print_notes.md`.

Do not mount electronics inside a shell that has sharp edges or areas that can cut wires.

---

## 7. Cleaning Printed Parts

After printing, clean the parts carefully.

Recommended actions:

```text
remove supports
trim loose filament
sand sharp edges lightly
check holes with small screwdriver or drill bit
remove plastic dust
test-fit parts before electronics
```

Important caution:

```text
Do not force electronic boards into tight printed slots.
```

If a component does not fit, modify the shell or mounting method instead of bending the board.

---

## 8. Mechanical Fit Test

Before wiring, place each component inside the shell without powering anything.

Check fit for:

```text
main controller
battery
power module
boost converter
LED ring
camera
IMU
distance sensor
speaker
microphone
servo bodies
servo horns
legs
switch
charging port
wires
```

The purpose of this test is to identify space problems before electronics are connected.

A component fit test passes when:

```text
the component fits without force
the shell can still close or partially close
the component does not block moving parts
the component does not press against battery cells
the component can be removed for repair
```

---

## 9. Internal Layout Strategy

The internal layout should support stability, safety and access.

Recommended layout principles:

```text
battery low and central
controller accessible
IMU fixed and near center if possible
camera facing forward
distance sensor facing forward
LED ring visible from outside
speaker opening not blocked
servo wires routed away from legs
power switch reachable
charging port reachable
```

Avoid:

```text
battery high in shell
loose IMU
camera ribbon sharply bent
wires crossing leg path
power module touching metal
boost converter hidden under battery
servo wires under mechanical stress
shell pressing on connectors
```

The center of mass matters. If the battery is too high or too far forward, the robot may tip or move poorly.

---

## 10. Component Mounting Strategy

V0 may use temporary mounting.

Acceptable V0 mounting methods:

```text
double-sided mounting tape
small screws
standoffs
zip ties
printed brackets
light hot glue for strain relief
foam pads
```

Avoid permanent mounting until the layout is proven.

Do not permanently glue:

```text
battery
main controller
camera ribbon
boost converter adjustment area
servo connectors
power switch wires
```

Components that may need replacement or debugging should remain accessible.

---

## 11. Main Controller Mounting

The main controller should be mounted where it is protected but still reachable.

Requirements:

```text
USB or power access if needed
GPIO header accessible
camera connector accessible
airflow not completely blocked
no direct pressure on microSD card
no metal contact with shell screws
no loose board movement
```

Recommended mounting:

```text
standoffs if available
mounting tape for early prototype
printed board tray in later version
```

The controller should not touch the battery directly.

If the controller heats noticeably, improve airflow or add spacing.

---

## 12. Battery Mounting

The battery is one of the most important and sensitive components.

Battery placement should be:

```text
low
central
secured
protected from puncture
away from moving legs
away from sharp printed edges
not crushed by shell
easy to disconnect if needed
```

Do not place battery wires where they can be pinched by the shell.

Do not close the robot if the battery is being compressed.

If using LiPo, inspect before installation:

```text
no swelling
no puncture
no exposed conductor
no damaged connector
no overheating during charge
```

Battery mounting should allow manual removal during early tests.

---

## 13. Power Module Mounting

Power modules include charger/protection board, boost converter and power distribution.

Mounting requirements:

```text
accessible adjustment screw if using adjustable boost converter
no short circuit risk
no loose exposed underside contacts
enough spacing from battery
wires strain-relieved
power switch connected clearly
```

Before mounting permanently:

```text
measure output voltage
document voltage
test controller power
test servo rail power
```

Do not hide an adjustable boost converter in a place that cannot be reached.

---

## 14. Power Switch Placement

The main power switch must be reachable from outside the robot.

Requirements:

```text
easy to access
not accidentally pressed by movement
clearly marked on/off if possible
securely mounted
wires strain-relieved
```

The power switch is the most reliable emergency stop during early testing.

Do not rely only on software stop before the robot is fully validated.

---

## 15. IMU Mounting

The IMU must be mounted firmly.

Requirements:

```text
fixed to the body
not dangling on wires
not moving independently from shell
orientation documented
near center of body if possible
away from strong vibration if possible
```

If the IMU moves independently, tilt readings become meaningless.

Document IMU orientation:

```text
which side is forward
which side is up
where the module is mounted
```

This information will be needed for tilt detection and safety thresholds.

---

## 16. Camera Mounting

The camera should face forward and have a clear view.

Requirements:

```text
lens not blocked
ribbon not sharply bent
module fixed in place
camera opening aligned
no pressure on lens
no loose movement during walking
```

The camera ribbon is fragile. Avoid repeated sharp bending.

The first camera mount can be temporary, but it must not allow the camera to fall into the shell.

After mounting, capture a test image and verify that:

```text
image is not black
image is not blocked by shell
image is correctly oriented or documented
image is saved to evidence/photos/
```

---

## 17. Distance Sensor Mounting

The distance sensor should face forward.

Requirements:

```text
clear line of sight
not recessed too deeply
not blocked by shell
aligned with movement direction
fixed firmly
wires not strained
```

If the sensor is angled incorrectly, obstacle detection may be unreliable.

After mounting, test distance readings with:

```text
no obstacle
object at 30 cm
object at 15 cm
object very close
```

Document the approximate useful range.

---

## 18. LED Ring Mounting

The LED ring should be visible from outside.

Possible placements:

```text
front face
top shell
around camera
inside translucent window
central status window
```

Requirements:

```text
visible during demo
not hidden by shell
wires secured
brightness configurable
not drawing excessive current
```

Avoid running all LEDs at full white brightness during early tests because current draw may be high.

LEDs should communicate real robot state, not random decoration.

---

## 19. Speaker Mounting

The speaker should be mounted near an opening or sound path.

Requirements:

```text
sound not fully blocked
speaker wires secured
speaker cone not pressed against shell
amplifier connected correctly
speaker not placed directly against IMU if avoidable
```

If speaker quality is poor, it is acceptable for V0 as long as the startup phrase is audible or terminal output replaces speech.

---

## 20. Microphone Mounting

The microphone should be placed where it can receive sound.

Requirements:

```text
microphone port not blocked
not directly pressed against shell
not placed too close to speaker if feedback occurs
wires secured
orientation documented if module is directional
```

Voice command recognition is not required for V0.

A simple microphone level test is enough for early validation.

---

## 21. Servo Mounting

The servos are safety-critical and mechanically important.

Requirements:

```text
servo body fixed firmly
servo horn secured
leg attached correctly
no shell collision
no cable strain
servo wires protected
servo orientation documented
```

Before attaching legs:

```text
scan servo ID
read current position
identify neutral position
test very small no-load movement
disable torque
```

After attaching legs:

```text
move manually with power off if possible
check clearance
run small nudge only
return to neutral
watch for binding
```

Do not start with a full gait.

---

## 22. Leg Mounting

The legs should be mounted symmetrically.

Check:

```text
left and right leg orientation
servo horn alignment
neutral angle
foot contact
clearance from shell
clearance from wires
ground contact
surface friction
```

Legs should not scrape the shell during the safe movement range.

If legs collide with the shell, reduce range or modify the mechanical part before testing movement.

If the robot slips too much, test rubber pads or different surface material.

---

## 23. Rounded Foot Notes

Rounded or rocker-style feet may help the robot shift contact points during movement.

However, they introduce surface sensitivity.

Possible issues:

```text
feet slip on smooth surfaces
feet catch on rough surfaces
movement depends on friction
left and right feet behave differently
layer lines affect smoothness
```

Test surfaces:

```text
desk mat
wood table
paper
smooth floor
rubber mat
```

Document the best surface for the first demo.

---

## 24. Cable Routing

Cable routing must be checked before closing the shell.

Good routing:

```text
wires follow shell walls
wires are tied or taped
servo wires have enough slack
camera ribbon has gentle curve
battery wires are protected
power wires are not under tension
sensor wires do not cross leg path
```

Bad routing:

```text
wire crosses moving leg path
wire is pinched by shell
wire pulls on small connector
battery wire bends sharply
camera ribbon folded sharply
servo connector loose
wire touches hot component
```

Use small zip ties, mounting tape or printed guides where possible.

Do not over-tighten zip ties on fragile wires.

---

## 25. Shell Closing Procedure

Do not close the shell fully until all basic tests have passed.

Before closing:

```text
take photo of internal wiring
check power switch access
check battery position
check camera view
check LED visibility
check leg clearance
check wire clearance
check no connector is loose
check no metal part can short exposed pins
```

Close shell partially first.

Run:

```text
LED test
IMU test
camera test
distance test
servo scan
safe nudge if clearance is confirmed
```

Only then close shell fully.

If closing the shell changes sensor readings or causes failures, reopen and inspect cable pressure.

---

## 26. First Assembly Milestone

The first assembly milestone is:

```text
MicroBot body can hold the controller, LED ring, IMU and camera without closing pressure or cable damage.
```

Required evidence:

```text
photo of internal layout
photo of front view
camera test image
IMU test output
LED test video
```

Expected status:

```text
physical layout: bench-tested
movement: still disabled
```

---

## 27. Second Assembly Milestone

The second assembly milestone is:

```text
Servo bodies and legs are mounted, and the legs can move through the safe range without collision.
```

Required evidence:

```text
photo of servo mounting
photo of leg neutral position
manual clearance video
safe nudge video
servo scan output
```

Expected status:

```text
servo mounting: bench-tested
safe nudge: bench-tested
walking: still planned
```

---

## 28. Third Assembly Milestone

The third assembly milestone is:

```text
The robot can run self-check while partially or fully assembled.
```

Required evidence:

```text
terminal output of self-check
session log
photo of assembled robot
camera snapshot from mounted camera
```

Expected status:

```text
assembly: bench-tested
self-check: bench-tested
integrated demo: prepared
```

---

## 29. Fourth Assembly Milestone

The fourth assembly milestone is:

```text
The robot can perform the first safe integrated demo without uncontrolled movement.
```

Required evidence:

```text
video of demo
session log
final report
camera snapshot
safety event if tested
```

Expected status:

```text
integrated demo: hardware-validated
public demo: not yet demo-ready until repeated
```

---

## 30. Assembly Evidence Requirements

Save evidence at every major step.

Recommended evidence:

```text
evidence/photos/internal_layout_v0.jpg
evidence/photos/front_view_v0.jpg
evidence/photos/servo_mount_left_v0.jpg
evidence/photos/servo_mount_right_v0.jpg
evidence/photos/wiring_before_closing_v0.jpg
evidence/videos/leg_clearance_test_v0.mp4
evidence/videos/safe_nudge_test_v0.mp4
evidence/reports/assembly_report_v0.md
```

Large videos may be stored outside Git if needed.

Photos should be clear enough to understand wiring and component placement.

---

## 31. Assembly Report Template

Use this template after each assembly session.

```text
# Assembly Report

Date:
Operator:
Robot version:
Mechanical revision:
Hardware revision:
Software version:

## Assembly Actions Completed

- 

## Components Installed

- 

## Wiring Changes

- 

## Mechanical Issues Found

- 

## Electrical Issues Found

- 

## Tests Performed

- 

## Test Results

- 

## Evidence Saved

- 

## Next Actions

- 
```

---

## 32. Assembly Change Log Template

Use this template whenever a physical layout changes.

```text
Date:
Changed component:
Previous position:
New position:
Reason:
Effect on wiring:
Effect on balance:
Effect on testing:
Evidence:
Next action:
```

Example:

```text
Date: 2026-06-13
Changed component: battery
Previous position: front upper shell
New position: lower center base
Reason: reduce front-heavy tipping
Effect on wiring: battery wires shortened
Effect on balance: improved standing stability
Effect on testing: repeat standing stability test
Evidence: evidence/photos/battery_layout_update.jpg
Next action: update power_budget.md and run movement clearance test
```

---

## 33. Common Assembly Problems

Common problems:

```text
shell does not close
wires block legs
camera ribbon is too short or twisted
battery is too large
servo horn alignment is wrong
left and right legs are not symmetrical
IMU is loose
LED ring not visible
distance sensor blocked by shell
speaker too quiet because opening is blocked
power switch unreachable
servo cable disconnects during movement
robot tips forward or backward
```

Each problem should be documented with a note and, if possible, a photo.

Problems are not failures. They are part of the prototype process.

---

## 34. Assembly Risk Matrix

| Area            | Risk                            | Impact                  | Mitigation                                    |
| --------------- | ------------------------------- | ----------------------- | --------------------------------------------- |
| Battery         | crushed or punctured            | high                    | mount low, protected and removable            |
| Servo legs      | collision with shell            | high                    | manual clearance test before powered movement |
| Wires           | caught by moving leg            | high                    | route along shell walls and secure            |
| Camera ribbon   | sharp bend or pressure          | medium                  | gentle routing and camera test after closing  |
| IMU             | loose mounting                  | high                    | fixed to body, orientation documented         |
| LED ring        | high current at full brightness | medium                  | reduce brightness during tests                |
| Power module    | inaccessible voltage adjustment | high                    | test and document before mounting             |
| Shell           | cannot close                    | medium                  | temporary layout, update mechanical notes     |
| Speaker         | blocked output                  | low                     | provide opening or fallback terminal output   |
| Distance sensor | blocked view                    | high if used for safety | front-facing and tested                       |

---

## 35. Assembly Safety Checklist

Before powering:

```text
[ ] battery is not damaged
[ ] output voltage measured
[ ] boost converter adjusted
[ ] no exposed short circuit risk
[ ] common ground planned
[ ] switch works
[ ] wires are not crushed
[ ] controller is mounted safely
```

Before moving servos:

```text
[ ] servo rail measured
[ ] servo ID detected
[ ] servo position readable
[ ] legs clear shell
[ ] wires clear legs
[ ] robot is on safe flat surface
[ ] operator can cut power
[ ] movement amplitude is small
```

Before closing shell:

```text
[ ] internal wiring photographed
[ ] camera ribbon safe
[ ] battery secured
[ ] power switch reachable
[ ] charging port reachable if used
[ ] LED visible
[ ] distance sensor view clear
[ ] shell does not press on boards
```

Before demo:

```text
[ ] self-check passes
[ ] safe mode tested
[ ] emergency stop method available
[ ] robot not near edge
[ ] evidence recording ready
[ ] logs folder writable
[ ] final report generation ready
```

---

## 36. Assembly Status Labels

Use these labels when documenting physical assembly.

```text
planned = assembly idea documented
prepared = parts and layout selected
partially assembled = some components mounted
bench-tested = assembly works in basic component tests
hardware-validated = assembly works during movement tests
integrated = assembly works with sensors, servos, safety and logging
demo-ready = assembly supports repeated public demo
```

Do not mark the robot as hardware-validated until it works as an assembled system.

---

## 37. Recommended First Physical Layout

A recommended first layout is:

```text
front:
    camera
    distance sensor
    LED visible area

center:
    IMU
    main controller

lower center:
    battery

sides:
    left servo
    right servo

rear or side:
    power switch
    charging access

top or front:
    LED ring / status window

inside wall:
    power module and cable routing
```

This layout is only a starting point. It should be changed if the real parts do not fit well.

---

## 38. Do Not Do These During V0 Assembly

Avoid:

```text
permanently gluing everything before tests
closing shell before taking internal photos
testing full walking immediately
placing robot near table edge
using long loose wires near legs
hiding the power switch
ignoring battery placement
mounting IMU loosely
letting camera ribbon fold sharply
running servos from unmeasured power
claiming hardware validation without evidence
```

---

## 39. Assembly Definition of Done

Assembly can be considered complete for V0 only when:

```text
body is assembled
electronics are mounted
battery is secured
power switch is reachable
camera has clear view
LED is visible
IMU is fixed
distance sensor is aligned if installed
servos are mounted securely
legs move without collision
wires do not block movement
self-check runs
safe servo nudge works
movement stops when unsafe
evidence is saved
documentation is updated
```

If any critical item is missing, assembly should remain partially assembled or bench-tested, not demo-ready.

---

## 40. Final Assembly Statement

MicroBot Round V0 assembly must be practical, safe and inspectable.

The first assembled robot does not need to look perfect. It needs to be real, accessible and testable.

A successful V0 assembly means that the robot can hold its components, protect its wiring, expose its sensors, move its legs within safe limits, stop when unsafe and be opened again for repairs or improvements.

The correct assembly mindset is:

```text
build
inspect
photograph
test
log
fix
repeat
```

That is how MicroBot Round V0 becomes a real physical robotics prototype.
