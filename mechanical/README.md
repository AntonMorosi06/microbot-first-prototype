# Mechanical System

## 1. Purpose of This Folder

This folder contains the mechanical documentation and future mechanical assets for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of the mechanical system is to transform the MicroBot concept into a real physical body that can contain electronics, expose sensors, support controlled leg movement, remain stable on a flat surface, protect wiring and allow repeated testing.

MicroBot Round V0 is not intended to be a final industrial design. It is a first physical prototype designed for assembly, inspection, debugging, safe movement and evidence collection.

The mechanical system must support the first integrated demo:

```text
power on
LED boot animation
self-check
IMU reading
camera frame capture
distance reading
servo scan
safe leg nudge
limited safe movement
safety stop
session log
final report
```

The mechanical design must therefore be practical, openable, testable and safe.

---

## 2. Mechanical Status

Current mechanical status:

```text
Mechanical concept: prepared
Rounded body design: planned
Upper shell: planned
Lower base shell: planned
Legs / rocker feet: planned
Servo mounts: planned
Internal layout: planned
3D printed parts: not confirmed
Fit test: not completed yet
Leg clearance test: not completed yet
Movement validation: not completed yet
```

The mechanical system should remain marked as **planned** or **prepared** until real printed parts are tested.

---

## 3. Design Philosophy

The mechanical design of MicroBot Round V0 follows a prototype-first approach.

The first version should prioritize:

```text
easy assembly
safe wiring
openable shell
component access
stable sensor placement
servo clearance
battery safety
repeatable testing
clear documentation
```

The first version should not prioritize:

```text
perfect miniaturization
cosmetic perfection
permanent closed shell
fully hidden wiring
complex leg mechanics
advanced walking gait
final manufacturing quality
```

A good V0 robot is not the most beautiful robot.

A good V0 robot is a robot that can be opened, inspected, tested, repaired and improved.

---

## 4. Target Mechanical Concept

MicroBot Round V0 is intended to be a small rounded robot with a compact body and two simple leg or rocker-style movement elements.

The target physical structure is:

```text
rounded upper shell
lower base shell
front sensor area
visible LED area
internal electronics space
battery compartment
left servo mount
right servo mount
left rounded leg / foot
right rounded leg / foot
accessible power switch
safe cable routing
```

The body should look like a small rounded MicroBot prototype, but the internal structure must remain practical.

The visual goal is:

```text
small
rounded
compact
robotic
friendly
technical
not overcomplicated
```

The engineering goal is:

```text
stable
openable
testable
safe
easy to modify
```

---

## 5. Main Mechanical Components

The planned mechanical system includes:

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
speaker_opening
microphone_opening
battery_area
power_switch_access
cable_routing_area
```

Each component should eventually have either a CAD file, STL file, drawing, photograph or assembly note.

---

## 6. Folder Structure

Recommended structure for this folder:

```text
mechanical/
├── README.md
├── design_requirements.md
├── print_notes.md
├── stl_reference/
│   └── .gitkeep
├── cad_custom/
│   └── .gitkeep
├── exports/
│   └── .gitkeep
├── photos/
│   └── .gitkeep
└── notes/
    └── .gitkeep
```

### `mechanical/README.md`

This file explains the mechanical purpose, concept, structure, status and validation strategy.

### `mechanical/design_requirements.md`

This file defines the physical design requirements for the body, legs, shell, mounts, sensor openings, stability and safe movement.

### `mechanical/print_notes.md`

This file records 3D printing settings, print results, fit issues, material notes and modifications.

### `mechanical/stl_reference/`

This folder may contain reference STL files or notes about external mechanical inspiration.

If external STL files are used, their license must be checked before committing or publishing them.

### `mechanical/cad_custom/`

This folder is for original MicroBot CAD files created specifically for this project.

Possible file types:

```text
.blend
.step
.f3d
.obj
.stl
.glb
```

### `mechanical/exports/`

This folder is for generated export files, such as STL or GLB files derived from original custom CAD.

### `mechanical/photos/`

This folder can contain selected mechanical photos, such as printed shell photos, internal fit photos or leg clearance photos.

Large image sets should be handled carefully and should not make the repository unnecessarily heavy.

### `mechanical/notes/`

This folder can contain extra mechanical notes, sketches, version notes or failure reports.

---

## 7. External Reference Policy

MicroBot Round V0 may be inspired by external open-source robotics projects, rounded robot bodies or simple two-servo movement concepts.

However, the mechanical design must remain documented honestly.

The repository should distinguish between:

```text
original MicroBot mechanical files
external reference files
modified external files
inspiration only
planned future CAD
```

If an external STL, CAD file or model is copied, modified or included, the license must be checked first.

If an external design is only used for study or inspiration, it should be documented in:

```text
references/
mechanical/stl_reference/
```

The project must not present external mechanical files as original work.

---

## 8. GrowBot-Style Reference Note

MicroBot Round V0 may use lessons from GrowBot-style rounded prototypes:

```text
small rounded body
simple physical shell
two-servo movement
rounded legs or rocker feet
camera opening
sensor support
compact bench robot layout
```

However, MicroBot Round V0 should remain its own project.

Correct statement:

```text
MicroBot Round V0 uses a rounded two-leg bench robot architecture inspired by small open robotics prototypes, but its mechanical files, documentation and validation process are developed as part of the MicroBot project.
```

Incorrect statement:

```text
MicroBot Round V0 is a finished copy of an existing robot.
```

If any external mechanical file is reused, attribution and license compatibility must be handled before public release.

---

## 9. Upper Shell Requirements

The upper shell should provide the visible identity of the robot.

It should support:

```text
rounded external shape
front camera opening
front or top LED visibility
possible speaker opening
possible microphone opening
access to internal components during testing
safe clearance above electronics
no pressure on camera ribbon
no pressure on battery
no sharp internal edges
```

The shell should not be permanently closed during early development.

The upper shell should allow repeated opening and closing during testing.

---

## 10. Lower Base Requirements

The lower base should support the internal structure.

It should provide:

```text
stable lower body
mounting area for controller
mounting area for battery
mounting area for power module
left servo support
right servo support
wire routing channels or space
access to switch and charging port
clearance for leg movement
flat or stable contact geometry
```

The lower base must be strong enough to hold the robot during servo movement.

If the lower base flexes too much, movement may become unreliable.

---

## 11. Leg and Foot Requirements

The legs or rocker-style feet are the first movement interface of MicroBot Round V0.

They should be:

```text
simple
rounded
symmetrical
easy to print
easy to attach
safe to test
compatible with selected servo horns
not too thin
not too fragile
not too aggressive in movement
```

The first leg design does not need to produce perfect walking.

The first leg design must support:

```text
safe nudge
small forward attempt
small turn attempt
return to neutral
clearance from shell
repeatable testing
```

If the robot only rocks slightly or moves a few centimeters in V0, that is acceptable.

The first goal is controlled movement, not advanced locomotion.

---

## 12. Servo Mount Requirements

Servo mounts must hold the servos firmly.

Requirements:

```text
servo body does not shift during movement
servo horn remains aligned
servo screws are reachable
servo wires are not strained
servo can be removed for repair
left and right sides are symmetrical
servo axis is documented
movement range is mechanically limited or known
```

Servo mounts should not require destructive disassembly.

If the servo cannot be removed without breaking the shell, the design is not good for V0.

---

## 13. Sensor Opening Requirements

The front sensor area should support:

```text
camera
distance sensor
optional microphone
optional LED status area
```

The camera must have a clear view.

The distance sensor must not be recessed too deeply or blocked by the shell.

The LED ring must be visible during demo.

The microphone opening should not be blocked if microphone testing is planned.

---

## 14. Battery Placement Requirements

Battery placement affects safety and balance.

The battery should be:

```text
low
central
secured
removable
protected from puncture
away from moving legs
away from sharp edges
not compressed by shell
```

The battery should not be placed high in the robot unless there is a strong reason.

A high battery may raise the center of mass and make the robot unstable.

---

## 15. Center of Mass Requirements

MicroBot Round V0 should remain stable on a flat surface.

The center of mass should be:

```text
low
close to the center
not too far forward
not too far backward
not too far left or right
```

Possible balance problems:

```text
robot tips forward because camera and battery are too far forward
robot tips backward because cables or battery are too far rearward
robot leans left or right because servos are not symmetrical
robot slips because feet have low friction
robot rocks unpredictably because rounded feet are too smooth
```

Balance must be tested before movement.

---

## 16. Cable Routing Requirements

The mechanical design must reserve space for cables.

Cable routing should:

```text
avoid moving legs
avoid sharp bends
avoid crushing camera ribbon
avoid pulling sensor connectors
avoid crossing servo horns
avoid pressure on battery wires
allow shell opening
allow maintenance
```

Good mechanical design includes wire space.

A shell that fits electronics but crushes wires is not acceptable.

---

## 17. Power Switch and Charging Access

The power switch must be reachable from outside the shell.

Requirements:

```text
easy to access
not hidden under the robot
not blocked by legs
not accidentally pressed during movement
physically secure
```

If charging access is included, it should also be reachable.

However, V0 does not need perfect integrated charging.

For early tests, it is acceptable to remove the battery or use external bench power.

---

## 18. Mechanical Safety Requirements

Mechanical safety requirements:

```text
no sharp internal edges near wires
no moving part touching wires
no shell pressure on battery
no loose servo mount
no loose IMU
no loose camera
no exposed rotating part that can catch wires
no movement near table edge
no full movement before clearance test
```

If mechanical clearance is uncertain, movement must remain disabled.

---

## 19. Mechanical Test Sequence

Recommended mechanical test sequence:

```text
1. Inspect printed parts.
2. Clean printed parts.
3. Test shell fit without electronics.
4. Place electronics without wiring.
5. Check battery fit.
6. Check camera alignment.
7. Check LED visibility.
8. Check distance sensor line of sight.
9. Mount servos without legs.
10. Attach legs without powered movement.
11. Move legs manually if possible.
12. Check clearance from shell.
13. Check cable routing.
14. Run servo scan without movement.
15. Run safe nudge.
16. Check post-movement stability.
17. Partially close shell.
18. Repeat tests.
19. Fully close shell only after tests pass.
```

Do not jump from printing parts directly to full demo.

---

## 20. Mechanical Validation Levels

The mechanical system should use clear validation labels.

```text
planned = mechanical concept exists
prepared = design requirements and layout are documented
printed = physical parts have been printed
fit-tested = components physically fit inside the body
bench-tested = parts support component tests
movement-tested = legs move safely in limited range
hardware-validated = assembled robot performs safe movement
demo-ready = repeated demo works without mechanical failure
```

Do not mark the mechanical system as hardware-validated until the assembled robot works during real movement tests.

---

## 21. Required Mechanical Evidence

Mechanical progress should be supported by evidence.

Recommended evidence:

```text
photos of printed parts
photos of internal layout
photos of camera opening
photos of LED placement
photos of battery placement
photos of servo mounts
video of manual leg clearance
video of safe servo nudge
notes about print settings
notes about failed prints
notes about fit problems
```

Recommended locations:

```text
mechanical/photos/
evidence/photos/
evidence/videos/
mechanical/print_notes.md
hardware/assembly_notes.md
```

---

## 22. Mechanical Known Limitations

Current known limitations:

```text
final CAD is not completed yet
printed parts are not validated yet
internal layout is not physically tested yet
servo mount geometry is not validated yet
leg movement range is not validated yet
center of mass is not measured yet
shell closure is not validated yet
camera opening is not validated yet
distance sensor alignment is not validated yet
battery fit is not validated yet
```

These limitations must remain documented until real assembly tests are completed.

---

## 23. First Mechanical Milestone

The first mechanical milestone is:

```text
A rounded shell and base can physically hold the main controller, IMU, camera, LED ring and battery without forcing the shell closed.
```

Required evidence:

```text
photo of empty shell
photo of internal component layout
photo of front sensor area
photo of battery placement
notes about fit issues
```

Expected status:

```text
mechanical layout: fit-tested
movement: not tested yet
```

---

## 24. Second Mechanical Milestone

The second mechanical milestone is:

```text
Both servos can be mounted and both legs can move through the planned safe range without hitting the shell or wires.
```

Required evidence:

```text
photo of servo mounts
photo of left leg attached
photo of right leg attached
manual clearance video
safe servo nudge video
```

Expected status:

```text
servo mounting: bench-tested
leg clearance: bench-tested
walking: not validated yet
```

---

## 25. Third Mechanical Milestone

The third mechanical milestone is:

```text
The assembled robot can stand on a flat surface with stable center of mass.
```

Required evidence:

```text
front photo
side photo
top photo
standing stability note
center of mass observation
surface test note
```

Expected status:

```text
standing stability: bench-tested
movement: prepared
```

---

## 26. Fourth Mechanical Milestone

The fourth mechanical milestone is:

```text
The assembled robot can perform a safe leg nudge without mechanical collision, uncontrolled tipping or cable interference.
```

Required evidence:

```text
safe nudge video
session log
post-test inspection note
servo temperature note if available
wire clearance photo
```

Expected status:

```text
limited movement: hardware-validated
full walking: still planned
```

---

## 27. Mechanical Design Rules

The mechanical design should follow these rules:

```text
keep the robot openable
keep the battery accessible
keep the power switch reachable
keep the camera view clear
keep the IMU fixed
keep wires away from legs
keep servo mounts strong
keep leg movement small at first
keep all mechanical changes documented
```

The robot should not be glued shut.

The shell should not be treated as final until multiple test cycles have passed.

---

## 28. Mechanical Failure Notes

Mechanical failures should be documented, not hidden.

Examples of useful failure notes:

```text
left leg collides with lower shell
battery makes robot front-heavy
camera ribbon is too short
distance sensor is blocked by front shell
servo horn slips during movement
shell cannot close with current wiring
printed part cracked near servo mount
LED ring is not visible enough
robot slips on smooth table
```

Each failure should include:

```text
what happened
why it matters
what was changed
what test should be repeated
```

Failure documentation makes the project stronger.

---

## 29. Public Claim Rules

Do not claim:

```text
the mechanical design is final
the robot walks reliably
the shell is validated
the legs are validated
the robot is fully miniaturized
the robot is ready for production
```

unless real evidence exists.

Correct early claim:

```text
MicroBot Round V0 includes a planned rounded mechanical architecture with shell, base, sensors, servo mounts and simple leg movement. The mechanical system must be printed, assembled and validated before movement claims are made.
```

Correct later claim after tests:

```text
MicroBot Round V0 completed a limited safe leg nudge inside the assembled rounded body without mechanical collision or cable interference.
```

---

## 30. Relationship With Other Files

This mechanical README is connected to:

```text
hardware/assembly_notes.md
hardware/wiring.md
hardware/pinout.md
hardware/power_budget.md
docs/safety.md
docs/test_plan.md
docs/current_status.md
docs/limitations.md
demos/demo_sequence_v0.md
```

If the mechanical design changes, update the relevant hardware and documentation files.

Examples:

```text
if servo position changes -> update pinout, wiring and assembly notes if wiring route changes
if battery position changes -> update power budget and assembly notes
if camera opening changes -> update assembly notes and demo camera evidence
if leg geometry changes -> update design requirements and print notes
```

---

## 31. Final Mechanical Statement

The mechanical system is the physical foundation of MicroBot Round V0.

The first mechanical version does not need to be perfect.

It needs to be:

```text
rounded
openable
safe
testable
stable
repairable
documented
compatible with sensors
compatible with servos
ready for small controlled movement
```

A successful mechanical V0 means that MicroBot can become a real physical robot instead of only a concept.

The correct mechanical mindset is:

```text
print
inspect
fit
wire
test
record
modify
repeat
```

That is how MicroBot Round V0 becomes physically real.
