# Bill of Materials

## 1. Purpose of This Document

This document defines the first Bill of Materials for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this BOM is to define the hardware required to build a small safety-aware robotic platform able to power on, run self-checks, read sensors, move slowly, stop when unsafe and save evidence.

This document is not a final manufacturing BOM. It is a V0 prototype BOM designed for bench testing, learning, debugging and progressive validation.

MicroBot Round V0 should be built with accessible modular components before moving toward custom PCBs, miniaturized electronics or final industrial design.

---

## 2. BOM Status

Current BOM status:

```text
BOM status: prepared
Hardware purchased: not confirmed
Hardware assembled: not confirmed
Hardware validated: not yet
Power system validated: not yet
Servo system validated: not yet
Sensor system validated: not yet
```

This BOM defines the recommended component set. A component should not be marked as validated until it has been physically tested.

---

## 3. Build Philosophy

The hardware for MicroBot Round V0 follows six principles.

### 3.1 Build a Real Robot Before a Perfect Robot

The first version must be real, testable and repairable.

It does not need to be fully miniaturized.

It does not need a custom PCB.

It does not need perfect walking.

It needs to power on, sense, move carefully, stop safely and log what happened.

### 3.2 Use Modular Components First

Development boards and breakout modules are acceptable for V0.

They make it easier to:

```text
debug wiring
replace broken parts
test one subsystem at a time
change the design
document the build
avoid expensive PCB mistakes
```

### 3.3 Separate Required and Optional Components

The BOM is divided into:

```text
required for first hardware bring-up
required for first movement demo
recommended for safety
optional for improved interaction
future expansion
tools and consumables
```

This avoids buying unnecessary parts too early.

### 3.4 Safety Before Movement

Power, IMU, servo scan and emergency stop strategy must be validated before full movement.

The robot should not attempt walking before:

```text
power is stable
servos are detected
servo positions are readable
small servo movement is tested
IMU tilt detection works
safety layer blocks movement when unsafe
```

### 3.5 Evidence-Oriented Hardware

Every major component should eventually produce evidence.

Examples:

```text
LED ring -> boot animation video
IMU -> tilt reading terminal output
Camera -> saved frame
Distance sensor -> obstacle reading log
Servos -> safe nudge video
Battery/power -> voltage measurement photo
```

### 3.6 Keep Alternatives Documented

If a component is unavailable, an alternative can be used.

However, alternatives must be documented because they may change:

```text
pinout
voltage
libraries
mechanical fit
power consumption
software driver
```

---

## 4. Hardware Priority Levels

Each component is assigned a priority.

```text
P0 = required for repository and planning
P1 = required for first electronics bring-up
P2 = required for first sensor demo
P3 = required for first safe movement demo
P4 = recommended for complete V0 demo
P5 = optional or future expansion
```

The first purchase should focus on P1, P2 and P3 items.

---

## 5. High-Level Component Summary

The recommended MicroBot Round V0 hardware system includes:

```text
main controller
microSD storage
power input and battery system
LED ring
IMU
camera
distance sensor
two small serial bus servos
speaker
microphone
audio amplifier
wiring and connectors
3D printed rounded body
mounting material
basic tools
```

Minimum first working demo:

```text
main controller
microSD card
stable 5 V power
LED ring
IMU
camera
two servos
safe logging
basic wiring
```

Recommended first complete demo:

```text
main controller
microSD card
battery and power switch
LED ring
IMU
camera
distance sensor
two serial servos
speaker
microphone
audio amplifier
rounded printed shell
logs and evidence
```

---

## 6. Core Electronics BOM

| ID    |                  Component | Qty | Priority | Recommended Type                          | Purpose                                                                   | Status   |
| ----- | -------------------------: | --: | -------: | ----------------------------------------- | ------------------------------------------------------------------------- | -------- |
| E-001 |            Main controller |   1 |       P1 | Raspberry Pi Zero 2 W                     | Main robot brain, Python runtime, camera, logging, dashboard, sensor loop | planned  |
| E-002 |               microSD card |   1 |       P1 | 16 GB or 32 GB, Class 10 / A1 preferred   | Operating system and project storage                                      | planned  |
| E-003 |                GPIO header |   1 |       P1 | 2x20 40-pin male header                   | GPIO access for sensors, LED, audio and servo bus                         | planned  |
| E-004 |            USB power cable |   1 |       P1 | Micro USB power cable for Pi Zero 2 W     | Power and setup                                                           | planned  |
| E-005 |            USB OTG adapter |   1 |       P2 | Micro USB OTG adapter                     | Keyboard, USB serial or peripheral connection during setup                | planned  |
| E-006 | Mini HDMI adapter or cable |   1 |       P2 | Mini HDMI to HDMI                         | Optional local display during setup                                       | optional |
| E-007 |      Pi Zero camera ribbon |   1 |       P2 | Narrow CSI ribbon compatible with Pi Zero | Required for Pi camera connection                                         | planned  |

### Notes

The Raspberry Pi Zero 2 W is recommended because it can run Linux and Python, supports a camera connector, provides GPIO access and is small enough for a compact rounded robot.

A Raspberry Pi with pre-soldered headers is easier for the first build. If the board has no header, soldering is required before using GPIO.

---

## 7. Actuation BOM

| ID    |           Component | Qty | Priority | Recommended Type                              | Purpose                                              | Status      |
| ----- | ------------------: | --: | -------: | --------------------------------------------- | ---------------------------------------------------- | ----------- |
| A-001 |      Left leg servo |   1 |       P3 | Small serial bus servo with position feedback | Left leg movement                                    | planned     |
| A-002 |     Right leg servo |   1 |       P3 | Small serial bus servo with position feedback | Right leg movement                                   | planned     |
| A-003 | Servo data resistor | 1-2 |       P3 | 1 kΩ resistor                                 | Half-duplex serial data line protection / bus wiring | planned     |
| A-004 |    Servo horn / arm |   2 |       P3 | Compatible with selected servo                | Mechanical connection to legs                        | planned     |
| A-005 |        Servo screws | set |       P3 | Compatible with servo                         | Mounting servo horn and servo body                   | planned     |
| A-006 |         Spare servo |   1 |       P4 | Same model as main servo                      | Replacement during debugging                         | recommended |

### Recommended Servo Type

The recommended actuator type for V0 is a small serial bus servo with feedback.

Preferred characteristics:

```text
small form factor
4 V to 6 V operating range
position feedback
bus communication
ID-based control
safe torque limiting if supported
suitable for slow small movements
```

### Why Not Simple PWM Servos?

Simple PWM servos are cheaper and easier, but they usually do not provide useful feedback. For a safety-aware robot, feedback is valuable because the robot should know whether the actuator exists and whether its position can be read.

### Servo Safety Notes

The first servo test must not be walking.

Correct first servo test:

```text
detect servo ID
read current position
move slightly
return to neutral
disable torque
log result
```

The robot must not execute large servo movements before calibration.

---

## 8. Sensor BOM

| ID    |                       Component | Qty | Priority | Recommended Type                                  | Purpose                                          | Status      |
| ----- | ------------------------------: | --: | -------: | ------------------------------------------------- | ------------------------------------------------ | ----------- |
| S-001 |                             IMU |   1 |       P2 | MPU-6050 or similar 6-DoF IMU                     | Tilt detection, stability check, motion feedback | planned     |
| S-002 |                          Camera |   1 |       P2 | Raspberry Pi compatible camera, Pi Zero ribbon    | Visual snapshots and future perception           | planned     |
| S-003 |                 Distance sensor |   1 |       P4 | VL53L0X or VL53L1X ToF sensor                     | Obstacle detection and forward safety            | planned     |
| S-004 |                      Microphone |   1 |       P4 | INMP441 I2S microphone or similar                 | Audio input, future wake/sound detection         | planned     |
| S-005 |           Optional light sensor |   1 |       P5 | BH1750 or similar                                 | Light-seeking / light-level behavior             | optional    |
| S-006 | Optional battery voltage sensor |   1 |       P4 | ADC module or voltage divider with safe interface | Battery monitoring                               | recommended |

### IMU Requirement

The IMU is required for safety.

It should support:

```text
acceleration reading
gyro reading
orientation estimation
tilt detection
stability check
```

The IMU must be tested before movement.

### Camera Requirement

The camera is required for the first visual evidence loop.

Initial camera use:

```text
capture one frame at boot
save image to evidence/photos/
log filename
optionally calculate brightness
```

Advanced vision is not required for V0.

### Distance Sensor Requirement

The distance sensor is strongly recommended because camera-only obstacle detection is too complex for a first prototype.

Initial distance use:

```text
read forward distance
compare with stop threshold
block forward movement if obstacle is too close
log obstacle event
```

---

## 9. Feedback and Interaction BOM

| ID    |            Component | Qty | Priority | Recommended Type                      | Purpose                                   | Status      |
| ----- | -------------------: | --: | -------: | ------------------------------------- | ----------------------------------------- | ----------- |
| F-001 |             LED ring |   1 |       P2 | WS2812B / NeoPixel ring, 7 to 12 LEDs | Boot animation and robot status feedback  | planned     |
| F-002 |      Audio amplifier |   1 |       P4 | MAX98357A I2S mono amplifier          | Speaker output                            | planned     |
| F-003 |              Speaker |   1 |       P4 | 8 Ω small speaker, 0.5 W to 3 W       | Spoken status messages / sounds           | planned     |
| F-004 |      Optional buzzer |   1 |       P5 | Active buzzer                         | Simple warning tones if speaker not ready | optional    |
| F-005 | Optional push button | 1-2 |       P4 | Momentary button                      | Manual start, mode select or local stop   | recommended |

### LED State Mapping

Recommended LED mapping:

```text
white = boot / self-check
blue = idle
green = system OK
yellow = warning
red = safe mode / error
purple = decision cycle
orange = obstacle detected
cyan = listening / perception
```

### Audio Output

Audio is useful but not required for the first electronics test.

If audio is unavailable, terminal output and LED state can replace spoken messages.

Recommended startup phrase:

```text
MicroBot Round V0 online. System check started.
```

Recommended final phrase:

```text
MicroBot Round V0. Autonomous safety demo completed.
```

---

## 10. Power System BOM

| ID    |                         Component | Qty | Priority | Recommended Type                                      | Purpose                               | Status   |
| ----- | --------------------------------: | --: | -------: | ----------------------------------------------------- | ------------------------------------- | -------- |
| P-001 |                           Battery |   1 |       P4 | 1S LiPo or protected 18650 cell                       | Portable power                        | planned  |
| P-002 | Battery charger/protection module |   1 |       P4 | TP4056 USB-C with protection, OUT+ and OUT- preferred | Safe charging and battery output      | planned  |
| P-003 |                   Boost converter | 1-2 |       P3 | MT3608 or better 5 V boost module                     | Step battery voltage up to 5 V        | planned  |
| P-004 |                 Main power switch |   1 |       P3 | SPST switch                                           | Physical power control                | planned  |
| P-005 |            Electrolytic capacitor | 1-2 |       P3 | 470 µF to 1000 µF, 10 V or higher                     | Reduce voltage dips near servo rail   | planned  |
| P-006 |                  USB power supply |   1 |       P1 | Stable 5 V supply                                     | Bench testing and safe development    | planned  |
| P-007 |          Optional USB power meter |   1 |       P5 | USB voltage/current meter                             | Measure current draw and voltage drop | optional |
| P-008 |          Optional fuse/protection |   1 |       P5 | Small inline fuse or protected power board            | Added electrical protection           | optional |

### Power Strategy

For the first bench tests, use a stable USB power supply before relying on battery operation.

Recommended progression:

```text
bench power for controller
bench power for sensors
servo rail idle test
single servo movement test
two-servo safe nudge
battery operation only after stable bench tests
```

### Power Warning

Do not connect the Raspberry Pi or servos to a boost converter before measuring the output voltage with a multimeter.

Some adjustable boost modules may arrive set to unsafe output voltages.

### Rail Strategy

V0 may use one shared 5 V rail, but this is not ideal.

Preferred safer strategy:

```text
5 V rail for Raspberry Pi and logic
separate 5 V rail for servos
common ground between all rails
capacitor near servo power input
```

If using one shared 5 V rail, the design must be marked as prototype-only and tested carefully under servo load.

---

## 11. Wiring and Connectors BOM

| ID    |               Component | Qty | Priority | Recommended Type                      | Purpose                       | Status      |
| ----- | ----------------------: | --: | -------: | ------------------------------------- | ----------------------------- | ----------- |
| W-001 |            Jumper wires | set |       P1 | Male-male, male-female, female-female | Breadboard/prototype wiring   | planned     |
| W-002 |             Hookup wire | set |       P2 | 22-26 AWG stranded wire               | Internal robot wiring         | planned     |
| W-003 |          JST connectors | set |       P4 | JST PH or JST SH depending modules    | More reliable internal wiring | recommended |
| W-004 |      Heat-shrink tubing | set |       P3 | Assorted sizes                        | Insulation and strain relief  | recommended |
| W-005 |         Electrical tape |   1 |       P2 | Standard electrical tape              | Temporary insulation          | planned     |
| W-006 | Breadboard or perfboard |   1 |       P2 | Small breadboard or perfboard         | Early wiring/prototyping      | planned     |
| W-007 |    Screw terminal board |   1 |       P4 | Small terminal block board            | Cleaner power distribution    | optional    |
| W-008 |              Cable ties | set |       P3 | Small zip ties                        | Cable routing                 | recommended |

### Wiring Rules

All wiring must follow these rules:

```text
common ground must be shared
servo power must be checked before movement
I2C devices must use correct voltage
wires must not touch moving legs
battery wires must not be crushed by shell
exposed conductors must be insulated
```

---

## 12. Mechanical BOM

| ID    |                Component | Qty | Priority | Recommended Type                      | Purpose                                 | Status      |
| ----- | -----------------------: | --: | -------: | ------------------------------------- | --------------------------------------- | ----------- |
| M-001 |      Rounded upper shell |   1 |       P3 | 3D printed PLA/PETG                   | Main visual body                        | planned     |
| M-002 |         Lower base shell |   1 |       P3 | 3D printed PLA/PETG                   | Electronics support and lower structure | planned     |
| M-003 |         Left rounded leg |   1 |       P3 | 3D printed PLA/PETG                   | Left movement element                   | planned     |
| M-004 |        Right rounded leg |   1 |       P3 | 3D printed PLA/PETG                   | Right movement element                  | planned     |
| M-005 |             Servo mounts |   2 |       P3 | Printed or bracket-based              | Servo fixation                          | planned     |
| M-006 |         Mounting squares | set |       P3 | Strong double-sided mounting squares  | Temporary board mounting                | recommended |
| M-007 |     Screws and standoffs | set |       P4 | M2/M2.5/M3 assorted                   | Cleaner internal mounting               | recommended |
| M-008 | Rubber feet or grip pads | set |       P4 | Rubber pads / TPU pads                | Improve traction and stability          | optional    |
| M-009 |   Transparent LED window |   1 |       P5 | Diffuser plastic or translucent print | Better LED visual effect                | optional    |
| M-010 |             Camera mount |   1 |       P4 | Printed mount                         | Camera alignment                        | recommended |

### Mechanical Material Recommendation

For first prints:

```text
PLA = easier to print, good for early fit tests
PETG = more durable, better for repeated handling
TPU = useful for feet/grip only, not ideal for full shell
```

### Mechanical First Goal

The first mechanical goal is not beauty.

The first goal is:

```text
body opens
electronics fit
legs move freely
camera has a clear view
LED is visible
battery is secured
wires do not block movement
```

---

## 13. Tools BOM

| ID    |                  Tool | Qty | Priority | Purpose                                       | Status      |
| ----- | --------------------: | --: | -------: | --------------------------------------------- | ----------- |
| T-001 |            Multimeter |   1 |       P1 | Measure voltage before connecting electronics | required    |
| T-002 |        Soldering iron |   1 |       P2 | Headers, wires, connectors                    | recommended |
| T-003 |                Solder |   1 |       P2 | Electrical connections                        | recommended |
| T-004 |         Wire stripper |   1 |       P2 | Prepare wires                                 | recommended |
| T-005 | Small screwdriver set |   1 |       P2 | Servo and shell assembly                      | recommended |
| T-006 |              Tweezers |   1 |       P3 | Small connector handling                      | recommended |
| T-007 |         Flush cutters |   1 |       P3 | Cut wires, supports, cable ties               | recommended |
| T-008 |              Calipers |   1 |       P4 | Measure printed parts and clearances          | optional    |
| T-009 |          Hot glue gun |   1 |       P4 | Temporary mounting and strain relief          | optional    |
| T-010 |          Camera/phone |   1 |       P1 | Evidence photos and demo video                | required    |

### Most Important Tool

The multimeter is mandatory.

Do not power the robot from an adjustable boost converter without measuring voltage first.

---

## 14. Consumables BOM

| ID    |                 Consumable | Qty | Priority | Purpose                  | Status      |
| ----- | -------------------------: | --: | -------: | ------------------------ | ----------- |
| C-001 |               PLA filament |   1 |       P3 | First body prints        | planned     |
| C-002 |              PETG filament |   1 |       P4 | Stronger later prints    | optional    |
| C-003 | Double-sided mounting tape |   1 |       P3 | Temporary board mounting | recommended |
| C-004 |         Heat-shrink tubing | set |       P3 | Insulation               | recommended |
| C-005 |                   Zip ties | set |       P3 | Cable routing            | recommended |
| C-006 |          M2/M2.5/M3 screws | set |       P4 | Mounting                 | recommended |
| C-007 |             Label stickers | set |       P5 | Label wires and modules  | optional    |

---

## 15. Minimum Purchase Set

This is the smallest useful purchase set for the first real electronics bring-up.

```text
Raspberry Pi Zero 2 W
microSD card
GPIO header
stable 5 V power supply
LED ring
MPU-6050 IMU
Pi-compatible camera with Pi Zero ribbon
jumper wires
multimeter
```

This minimum set allows:

```text
controller boot
Python setup
LED test
IMU test
camera capture
session log creation
```

It does not yet validate movement.

---

## 16. First Movement Purchase Set

To validate movement, add:

```text
2 small serial bus servos with feedback
servo-compatible cables
1 kΩ resistor
servo horns
servo screws
boost converter or safe 5 V servo rail
470 µF to 1000 µF capacitor
main switch
basic mounting material
```

This allows:

```text
servo bus scan
position read
safe servo nudge
neutral return
power drop observation
```

It does not yet prove reliable walking.

---

## 17. Complete V0 Demo Purchase Set

For the full MicroBot Round V0 demo, add:

```text
distance sensor
speaker
I2S amplifier
I2S microphone
battery
charger/protection module
power switch
3D printed shell
3D printed legs
mounting material
wiring insulation
camera recording setup for evidence
```

This allows the target demo:

```text
boot
LED animation
speech
self-check
IMU read
camera frame
distance check
servo check
safe movement
safety stop
autonomous action selection
session log
final report
```

---

## 18. Optional Expansion Components

These components are not required for V0, but may be useful later.

| Component               | Purpose                                | Priority |
| ----------------------- | -------------------------------------- | -------: |
| BNO055 or better IMU    | Easier orientation estimation          |       P5 |
| VL53L1X distance sensor | Longer range ToF sensing               |       P5 |
| OLED display            | Local status display                   |       P5 |
| ESP32 co-controller     | Real-time low-level control            |       P5 |
| Battery fuel gauge      | Better battery measurement             |       P5 |
| Charging dock contacts  | Future docking                         |       P5 |
| Magnets                 | Future docking / alignment experiments |       P5 |
| Small fan or heatsink   | Thermal management                     |       P5 |
| Custom PCB              | Future clean electronics               |       P5 |
| Drone camera system     | Future external observer               |       P5 |

---

## 19. Do Not Buy Yet

These items should not be bought until the V0 platform is working.

```text
custom PCB parts
large quantity of servos
expensive batteries
advanced LiDAR
expensive camera modules
complex docking hardware
magnetic aggregation hardware
multiple robot copies
drone integration hardware
custom machined shell
professional manufacturing parts
```

Reason:

```text
The first robot must validate the architecture before scaling.
```

---

## 20. Estimated Budget Categories

Exact prices change by country, supplier and availability. The following budget categories are only planning estimates.

### Minimal Bring-Up Budget

Includes:

```text
controller
microSD
LED
IMU
camera
wires
power supply basics
```

Estimated category:

```text
low to medium
```

Purpose:

```text
boot, LED, IMU, camera, logging
```

### First Movement Budget

Includes:

```text
minimal bring-up
two servos
servo wiring
capacitor
boost converter
switch
basic mounting
```

Estimated category:

```text
medium
```

Purpose:

```text
servo scan and safe nudge
```

### Complete V0 Demo Budget

Includes:

```text
first movement build
distance sensor
audio
microphone
battery system
printed body
mounting material
tools and consumables
```

Estimated category:

```text
medium to high for a first build
```

Purpose:

```text
complete safety-aware autonomous startup demo
```

### Budget Note

The first build usually costs more than the pure electronics list because of:

```text
shipping
duplicate parts
wrong cables
adapters
tools
mounting material
failed prints
spare components
```

The BOM should be updated with real purchase prices after ordering.

---

## 21. Component Status Tracker

| Component Group | Current Status    | Next Action                      |
| --------------- | ----------------- | -------------------------------- |
| Main controller | planned           | select and purchase              |
| Power system    | planned           | define safe rail strategy        |
| LED ring        | planned           | select model and pin             |
| IMU             | planned           | select I2C module                |
| Camera          | planned           | select Pi Zero compatible camera |
| Distance sensor | planned           | choose ToF sensor                |
| Servos          | planned           | choose serial bus servo model    |
| Audio output    | planned           | select amp and speaker           |
| Microphone      | planned           | select I2S microphone            |
| Mechanical body | planned           | select or design first shell     |
| Wiring          | planned           | prepare wiring diagram           |
| Tools           | partially planned | verify available tools           |

---

## 22. Hardware Validation Requirements

A component becomes **bench-tested** only when it has been tested physically.

Examples:

```text
LED ring bench-tested = LED script displays colors on real hardware
IMU bench-tested = real IMU returns changing values
Camera bench-tested = real camera saves image
Servo bench-tested = servo scan and safe nudge pass
Power bench-tested = measured voltage is stable under load
```

A component becomes **hardware-validated** only when it works inside the assembled MicroBot Round V0 body.

---

## 23. Safety-Critical Components

The following components are safety-critical:

```text
power regulator
battery
main switch
servos
servo power rail
IMU
distance sensor if used for obstacle stop
wiring
mounting of moving parts
```

Failure of these components may block movement.

The following components are useful but non-critical for first movement:

```text
speaker
microphone
camera if not used for movement safety
dashboard
LED ring if terminal output is available
```

However, the LED ring is strongly recommended because it gives immediate visible status feedback.

---

## 24. BOM Change Rules

Whenever a component changes, update:

```text
hardware/BOM.md
hardware/wiring.md
hardware/pinout.md
hardware/power_budget.md
docs/current_status.md
docs/limitations.md if needed
CHANGELOG.md
```

Examples:

```text
changing IMU model changes driver and wiring
changing servo model changes voltage and protocol
changing controller changes pinout and software
changing battery changes power budget and runtime
changing shell changes mechanical fit
```

No hardware change should remain undocumented.

---

## 25. First Recommended Build Order

Recommended hardware build order:

```text
1. Main controller + microSD
2. Python environment
3. LED ring
4. IMU
5. Camera
6. Session logging
7. Distance sensor
8. Servo bus without movement
9. Safe servo nudge
10. Speaker and microphone
11. Battery and switch
12. Mechanical shell
13. Internal integration
14. Self-check
15. Hello MicroBot demo
```

This order avoids debugging too many unknowns at the same time.

---

## 26. First Hardware Milestones

### Milestone H0.1 — Controller Alive

Criteria:

```text
controller boots
repository copied or cloned
Python runs
logs folder writable
```

### Milestone H0.2 — First Feedback

Criteria:

```text
LED ring works
boot animation works
terminal output works
```

### Milestone H0.3 — First Sensor

Criteria:

```text
IMU returns values
tilt changes values
camera saves first frame
```

### Milestone H0.4 — First Safety Input

Criteria:

```text
distance sensor returns value
obstacle threshold can be tested
tilt threshold can be tested
```

### Milestone H0.5 — First Actuator

Criteria:

```text
servos detected
positions readable
safe nudge works
neutral return works
torque off works
```

### Milestone H0.6 — First Integrated Hardware Demo

Criteria:

```text
self-check runs
LED shows state
IMU read works
camera frame saved
distance read works
servo check works
safe nudge works
session log saved
```

---

## 27. Hardware Risks

### Electrical Risks

```text
wrong voltage
wrong polarity
servo current spike
weak ground
battery short
boost converter set too high
loose wire during movement
```

Mitigation:

```text
measure voltage first
use common ground
test one component at a time
use capacitor near servo rail
secure wires
use physical power switch
```

### Mechanical Risks

```text
legs collide with shell
wires block movement
servo mount bends
battery shifts
robot tips over
camera opening blocked
```

Mitigation:

```text
manual clearance test
temporary mounting first
small movement only
photos of internal layout
update mechanical notes
```

### Software-Hardware Risks

```text
wrong pin mapping
wrong serial port
wrong I2C address
raw servo movement too large
LED library requiring root
camera not enabled
audio device mismatch
```

Mitigation:

```text
centralize pins in setup/microbot/pins.py
test scripts individually
write clear errors
keep movement disabled by default
```

---

## 28. Final BOM Statement

This BOM defines the first hardware foundation for MicroBot Round V0.

The objective is not to buy the most advanced components. The objective is to build the smallest credible robot that can be tested safely and documented clearly.

A successful V0 hardware build includes:

```text
stable power
working controller
visible LED state
IMU stability sensing
camera evidence capture
basic obstacle sensing
two safe leg servos
bounded movement
session logs
clear documentation
```

Once these elements are working, MicroBot Round V0 can move from a prepared repository to a real physical robotics prototype.
