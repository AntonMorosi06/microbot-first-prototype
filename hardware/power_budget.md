# Power Budget

## 1. Purpose of This Document

This document defines the initial power budget for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this file is to estimate, document and validate the electrical power requirements of the robot before full assembly and movement testing.

MicroBot Round V0 contains a main controller, sensors, LEDs, camera, audio modules, servos and possibly a battery system. Even if the robot is small, poor power design can cause unstable behavior, controller resets, servo failures, corrupted logs, unsafe movement or damaged components.

The power budget must answer these questions:

```text
What components need power?
What voltage does each component need?
How much current may each component draw?
Which components can share a rail?
Which components should be separated?
What happens when servos move?
Can the battery support the robot?
Can the regulator support current spikes?
What should be tested before movement?
```

The central rule is:

```text
No movement test should be performed until the power rails have been measured and verified.
```

---

## 2. Power Budget Status

Current power budget status:

```text
Power budget plan: prepared
Final components selected: not confirmed
Exact current measurements: not available yet
Bench power validated: not yet
Battery power validated: not yet
Servo rail validated: not yet
Voltage drop under load validated: not yet
Movement power behavior validated: not yet
```

This document contains estimated values. Real values must be measured during hardware bring-up.

---

## 3. Power Design Philosophy

MicroBot Round V0 follows a conservative power design approach.

The first version should prioritize reliability and safety over compactness.

The power system should be:

```text
measurable
stable
documented
easy to disconnect
safe under servo load
easy to debug
not hidden inside the shell before validation
```

The first power system does not need to be elegant. It needs to be stable.

---

## 4. Main Power Risks

The most important power risks are:

```text
wrong voltage
wrong polarity
weak regulator
servo current spikes
controller brownout
battery voltage drop
poor common ground
thin power wires
loose connectors
boost converter set too high
boost converter overheating
LED current too high
battery damage
short circuit
```

The most dangerous early mistake is connecting electronics before measuring the regulator output.

The second most dangerous mistake is powering servos from a rail that cannot handle current spikes.

---

## 5. Planned Power Architecture

The recommended V0 architecture uses separate power rails for the controller and servos.

```text
Battery or bench supply
        |
        v
Power switch
        |
        +--------------------------+
        |                          |
        v                          v
Controller 5 V rail           Servo 5 V rail
        |                          |
        v                          v
Raspberry Pi / sensors        Left servo / right servo
LED / audio / camera          Capacitor near servo rail
        |                          |
        +----------- GND ----------+
```

The grounds must be connected.

The rails may be separate, but the reference ground must be common.

---

## 6. Recommended Rail Strategy

### 6.1 Controller Rail

The controller rail powers:

```text
Raspberry Pi Zero 2 W
camera
I2C sensors
LED ring if current is low
I2S audio modules if installed
microphone if installed
optional buttons
```

Recommended voltage:

```text
5 V input to Raspberry Pi
3.3 V provided by Raspberry Pi for compatible low-current sensors
```

### 6.2 Servo Rail

The servo rail powers:

```text
left leg servo
right leg servo
future actuator modules if added
```

Recommended voltage:

```text
5 V regulated rail, depending on selected servo specifications
```

The servo rail should have:

```text
common ground with controller
short power wires
sufficient current capacity
capacitor near servo input
movement current tested before assembly
```

### 6.3 Shared Rail Option

A single shared 5 V rail may work for early testing if it is strong enough.

However, it has limitations:

```text
servo spikes may reset the controller
LED brightness may reduce voltage stability
logs may corrupt if controller loses power
camera may fail during movement
```

If a shared rail is used, it must be documented as a prototype limitation.

---

## 7. Estimated Component Power Table

The following table contains rough planning estimates. These values must be replaced with measured values after testing.

| ID      |                     Component |            Voltage | Estimated Idle Current | Estimated Active Current |     Peak / Warning Current | Notes                              |
| ------- | ----------------------------: | -----------------: | ---------------------: | -----------------------: | -------------------------: | ---------------------------------- |
| PWR-001 |         Raspberry Pi Zero 2 W |                5 V |             150-300 mA |               300-700 mA |                    800 mA+ | Depends on CPU, Wi-Fi, camera, USB |
| PWR-002 |                 Camera module |         via Pi CSI |              50-100 mA |               100-250 mA |                     300 mA | Depends on camera model            |
| PWR-003 |                  MPU-6050 IMU | 3.3 V / 5 V module |                3-10 mA |                  5-15 mA |                        low | Small load                         |
| PWR-004 | VL53L0X / ToF distance sensor | 3.3 V / 5 V module |               10-20 mA |                 20-40 mA |                      50 mA | Small but safety-relevant          |
| PWR-005 |      WS2812B LED ring, 7 LEDs |                5 V |               10-50 mA |                50-250 mA | up to 420 mA at full white | Brightness must be limited         |
| PWR-006 |                I2S microphone |              3.3 V |                 1-5 mA |                  2-10 mA |                        low | Optional                           |
| PWR-007 |       I2S amplifier + speaker |        3.3 V / 5 V |                5-20 mA |                50-500 mA |          depends on volume | Optional, can spike                |
| PWR-008 |             Serial servo left |        5 V typical |              20-100 mA |               200-700 mA |              1 A+ possible | Depends on load/stall              |
| PWR-009 |            Serial servo right |        5 V typical |              20-100 mA |               200-700 mA |              1 A+ possible | Depends on load/stall              |
| PWR-010 |        Boost converter losses |     battery to 5 V |                 varies |                   varies |                  heat risk | Efficiency depends on current      |
| PWR-011 |      Optional battery monitor |             varies |                1-10 mA |                  1-10 mA |                        low | Optional                           |

These are planning values, not final measurements.

The servo values are the most uncertain and must be tested.

---

## 8. Estimated Current Scenarios

### 8.1 Idle Scenario

Robot is powered, Linux is running, no movement, LEDs low brightness.

Estimated loads:

```text
Raspberry Pi: 250-400 mA
Camera idle: 50-100 mA
IMU: 5-10 mA
Distance sensor: 10-25 mA
LED ring low brightness: 20-80 mA
Audio idle: 5-20 mA
Servos idle / torque off: 20-100 mA total
```

Estimated total:

```text
350-735 mA
```

Planning target:

```text
1 A available for idle operation
```

### 8.2 Self-Check Scenario

Robot runs LED animation, reads sensors, captures camera frame, may speak a phrase.

Estimated loads:

```text
Raspberry Pi: 400-700 mA
Camera capture: 100-250 mA
IMU and distance: 20-50 mA
LED animation: 50-250 mA
Audio phrase: 50-400 mA
Servos not moving: 20-100 mA
```

Estimated total:

```text
640 mA to 1.75 A
```

Planning target:

```text
2 A available for self-check and feedback
```

### 8.3 Safe Servo Nudge Scenario

Robot performs a small servo movement.

Estimated loads:

```text
Raspberry Pi + sensors: 500-900 mA
LED low brightness: 20-100 mA
One moving servo: 200-700 mA
Second servo idle or holding: 50-300 mA
Possible current spike: 1 A+ on servo rail
```

Estimated total:

```text
800 mA to 2 A+
```

Planning target:

```text
2.5 A available total
separate servo rail recommended
```

### 8.4 Two-Servo Movement Scenario

Robot moves both legs.

Estimated loads:

```text
Raspberry Pi + sensors: 500-900 mA
LED low brightness: 20-100 mA
Two moving servos: 400 mA to 1.4 A typical
Servo peak / stall risk: 2 A+ possible
```

Estimated total:

```text
1 A to 3 A+
```

Planning target:

```text
3 A available for early movement testing
```

### 8.5 Worst-Case Prototype Scenario

Robot runs camera, LEDs, audio and both servos at the same time.

Estimated loads:

```text
Raspberry Pi high activity: 700-900 mA
Camera active: 150-300 mA
LED ring bright: 200-420 mA or more
Audio active: 100-500 mA
Two servos under load: 1 A to 2 A+ possible
Sensors: 20-60 mA
```

Estimated total:

```text
2.2 A to 4 A+
```

Planning target:

```text
avoid this scenario in V0
limit LED brightness
avoid loud audio during servo movement
avoid aggressive servo movement
```

---

## 9. Recommended Power Capacity

For a stable V0 prototype, the power system should be planned with headroom.

Recommended minimum:

```text
Controller rail: 5 V, at least 2 A available
Servo rail: 5 V, at least 2 A available for two small servos
```

Better prototype target:

```text
Controller rail: 5 V, 2 A to 3 A
Servo rail: 5 V, 3 A or more if servos draw high current
```

If using a single rail:

```text
5 V, 3 A minimum
5 V, 4 A or more preferred
```

The actual requirement depends on the selected servos, regulator and motion load.

---

## 10. Battery Planning

### 10.1 Battery Options

Possible battery options:

```text
1S LiPo battery
protected 18650 cell
USB power bank
bench power supply during development
```

For early testing, bench power or a stable USB supply is safer than relying immediately on battery.

### 10.2 1S LiPo / Li-Ion Considerations

A 1S lithium cell has:

```text
nominal voltage around 3.7 V
full charge around 4.2 V
discharge voltage lower than 3.7 V
requires boost converter to provide 5 V
```

The boost converter must supply enough current at 5 V.

Current on the battery side can be higher than current on the 5 V side because voltage is boosted.

Example concept:

```text
5 V output at 2 A = 10 W output
Battery around 3.7 V
Input current may be around 3 A or more after efficiency losses
```

This is why battery, wires and boost converter must be selected carefully.

### 10.3 USB Power Bank Option

A USB power bank can simplify early testing.

Advantages:

```text
stable 5 V output
integrated charging
often includes protection
easy to replace
less custom battery wiring
```

Limitations:

```text
may shut off at low load
may not handle servo spikes well
may be physically large
may not expose battery level easily
may not fit inside final shell
```

A USB power bank is useful for bench testing but may not be ideal for final V0 assembly.

---

## 11. Estimated Runtime

Runtime depends on battery capacity, voltage, regulator efficiency and load.

Approximate formula:

```text
runtime_hours = usable_battery_energy_Wh / average_load_W
```

Example:

```text
Battery: 2000 mAh at 3.7 V
Energy: 2.0 Ah * 3.7 V = 7.4 Wh
Estimated usable after boost losses: around 5.5 Wh to 6.5 Wh
Average load: 5 W
Runtime: about 1.1 to 1.3 hours
```

If the robot uses servos often, audio and high LEDs, runtime may be much shorter.

For V0, runtime is not the main target.

The main target is stable operation during a short demo.

Recommended first demo runtime target:

```text
5 to 10 minutes stable operation
```

Recommended later V0 target:

```text
20 to 30 minutes supervised operation
```

---

## 12. LED Brightness Power Rules

WS2812B / NeoPixel-type LEDs can draw significant current at high brightness, especially full white.

Rule:

```text
Do not use full brightness full white during early testing.
```

Recommended initial brightness:

```text
10% to 25% brightness
```

Recommended startup animation:

```text
short duration
low brightness
avoid full white for long periods
```

LED safety rule:

```text
If voltage drops or controller resets during LED animation, reduce brightness and check power rail.
```

LEDs are status feedback, not a power stress test.

---

## 13. Servo Power Rules

Servos are the main source of current spikes.

Servo power rules:

```text
measure servo rail before connecting servos
scan servo ID before movement
start with torque off if supported
move one servo first
move only a tiny amount
return to neutral
watch voltage during movement
watch for controller reset
watch for servo heating
avoid stall
avoid mechanical binding
```

If the servo stalls, current can increase sharply.

A stalled servo may:

```text
heat up
draw high current
drop voltage
reset controller
damage gears
damage printed parts
```

The first movement must be a safe nudge, not walking.

---

## 14. Capacitor Requirement

A capacitor should be placed near the servo rail.

Recommended:

```text
470 µF to 1000 µF
10 V or higher
electrolytic capacitor
```

Purpose:

```text
reduce voltage dips
support short current spikes
improve servo rail stability
reduce reset risk
```

Polarity:

```text
capacitor positive -> 5 V servo rail
capacitor negative -> GND
```

Incorrect polarity can damage the capacitor.

The capacitor does not replace a good regulator. It only helps with short spikes.

---

## 15. Wire Gauge and Connector Notes

Power wires should be able to carry expected current.

Prototype warning:

```text
thin jumper wires may be acceptable for sensors
thin jumper wires are not ideal for servo power
battery wires should not be thin or loose
servo power wires should be short and secure
```

Recommended:

```text
use thicker wires for battery and servo power
use short power runs
avoid loose breadboard connections for high-current servo tests
secure connectors before movement
```

A loose servo power connector can cause sudden resets or erratic movement.

---

## 16. Grounding Strategy

All modules must share ground.

Common ground includes:

```text
controller ground
servo ground
sensor ground
LED ground
audio ground
battery / power module ground
```

Bad ground can cause:

```text
I2C failures
UART failures
LED flicker
servo communication errors
random resets
unreliable sensor readings
```

If strange behavior occurs, check ground first.

---

## 17. Power Test Sequence

The recommended power test sequence is:

```text
1. Inspect power wiring with power off.
2. Measure boost converter output with no load.
3. Adjust output to safe voltage.
4. Power controller alone.
5. Confirm controller boots.
6. Add sensors one by one.
7. Add LED ring at low brightness.
8. Add camera.
9. Add servo rail without servos moving.
10. Connect one servo and scan only.
11. Connect two servos and scan only.
12. Run one-servo safe nudge.
13. Run two-servo safe nudge.
14. Observe voltage drop.
15. Document results.
```

Do not skip directly to step 13.

---

## 18. Power Test Result Template

Use this template for each power test.

```text
Test ID:
Date:
Power source:
Regulator:
Output voltage no load:
Output voltage idle:
Output voltage during LED test:
Output voltage during camera capture:
Output voltage during servo scan:
Output voltage during safe nudge:
Controller reset observed:
Servo issue observed:
Temperature issue observed:
Result:
Evidence:
Next action:
```

Example:

```text
Test ID: PWR-TEST-001
Date: 2026-06-13
Power source: bench USB 5 V supply
Regulator: none
Output voltage no load: 5.10 V
Output voltage idle: 5.05 V
Output voltage during LED test: 5.00 V
Output voltage during camera capture: 4.95 V
Output voltage during servo scan: not tested
Output voltage during safe nudge: not tested
Controller reset observed: no
Servo issue observed: not tested
Temperature issue observed: no
Result: PASS_WITH_WARNING
Evidence: photo of multimeter and terminal output
Next action: test servo rail separately
```

---

## 19. Voltage Measurement Points

Measure voltage at multiple points.

Recommended measurement points:

```text
boost converter output
controller 5 V input
servo rail input
servo connector
LED ring VCC and GND
battery terminals
charger/protection output
```

A voltage can look correct at the regulator but drop at the servo connector due to wire resistance or bad connectors.

Measure where the load is connected.

---

## 20. Brownout and Reset Symptoms

Possible power instability symptoms:

```text
Raspberry Pi reboots
SSH disconnects
camera capture fails
LED freezes
servo communication fails
I2C device disappears
audio crackles
log file incomplete
terminal stops unexpectedly
robot behaves differently each run
```

If any of these occur during movement, stop testing and investigate power.

Do not solve brownout by increasing movement amplitude or retrying aggressively.

---

## 21. Heat Monitoring

During tests, check temperature manually and through software if possible.

Components to monitor:

```text
boost converter
battery
Raspberry Pi
servo body
audio amplifier
wires near servo power
```

Warning signs:

```text
component too hot to touch
battery warming unexpectedly
boost converter heating quickly
servo heating during idle
wire insulation softening
burning smell
```

If heat appears, stop testing.

---

## 22. Safe Operating Modes

MicroBot Round V0 should support different power-aware modes.

### 22.1 Low-Power Idle

Behavior:

```text
servos torque off if safe
LED low brightness blue
camera inactive
audio inactive
sensors read slowly
logging active
```

### 22.2 Self-Check Mode

Behavior:

```text
LED animation low brightness
sensors read
camera captures one frame
audio phrase optional
servos do not move yet
```

### 22.3 Movement Test Mode

Behavior:

```text
LED low brightness
audio disabled or minimal
camera not streaming continuously
one safe servo action at a time
voltage monitored
```

### 22.4 Safe Mode

Behavior:

```text
movement disabled
servos torque off or reduced if safe
LED red low brightness
audio warning optional
logs saved
```

### 22.5 Demo Mode

Behavior:

```text
short LED sequences
short audio phrases
one camera capture
limited movement
safety layer active
final report generated
```

---

## 23. Power-Aware Software Limits

Software should reduce power stress.

Recommended limits:

```text
LED brightness limited by default
audio volume moderate
camera capture not continuous in first demo
servo movement short and slow
minimum delay between movement actions
movement disabled if power warning exists
safe mode if repeated resets are detected
```

Configuration placeholders:

```text
LED_BRIGHTNESS = 40
ENABLE_AUDIO_DURING_MOVEMENT = False
ENABLE_CAMERA_STREAMING = False
MOVEMENT_MAX_DURATION_SEC = 1.0
MOVEMENT_COOLDOWN_SEC = 2.0
POWER_WARNING_ENABLED = True
```

---

## 24. Battery Safety Rules

If using a LiPo or lithium-ion battery:

```text
do not use swollen batteries
do not puncture battery
do not crush battery inside shell
do not short battery terminals
do not charge unattended during early tests
do not use damaged wires
do not place battery near sharp printed edges
do not allow battery to move inside the shell
```

Battery must be:

```text
secured
removable during early development
protected from mechanical stress
not overheated
documented in assembly notes
```

---

## 25. Charger and Protection Module Notes

If using a TP4056 or similar charger/protection board:

```text
verify that the board includes protection if battery safety depends on it
connect battery correctly
verify OUT+ and OUT- behavior if used
do not reverse polarity
do not charge and test movement without understanding current path
```

Charging while operating the robot may be possible with some circuits but should not be assumed.

For V0, charging and operation can remain separate.

---

## 26. Boost Converter Notes

Boost converter risks:

```text
output voltage set too high
insufficient current capacity
overheating under servo load
voltage sag during movement
electrical noise
```

Before connecting electronics:

```text
connect battery or input source
measure output with multimeter
adjust to required voltage
connect small load if possible
measure again
only then connect controller or servos
```

Do not trust the factory setting.

---

## 27. Power Budget Validation Matrix

| Test ID | Test Name                             | Required Before Movement | Evidence Required       | Status  |
| ------- | ------------------------------------- | -----------------------: | ----------------------- | ------- |
| PWR-001 | Regulator no-load voltage measurement |                      yes | multimeter photo / note | planned |
| PWR-002 | Controller power-on stability         |                      yes | terminal output         | planned |
| PWR-003 | Sensor rail stability                 |                      yes | terminal output         | planned |
| PWR-004 | LED low-brightness current behavior   |      no, but recommended | video / note            | planned |
| PWR-005 | Camera capture power behavior         |      no, but recommended | image + note            | planned |
| PWR-006 | Servo rail idle voltage               |                      yes | multimeter note         | planned |
| PWR-007 | One-servo scan power behavior         |                      yes | terminal output         | planned |
| PWR-008 | One-servo nudge voltage drop          |                      yes | video + voltage note    | planned |
| PWR-009 | Two-servo nudge voltage drop          |                      yes | video + voltage note    | planned |
| PWR-010 | Battery operation short demo          |    no, after bench tests | report                  | planned |
| PWR-011 | Heat observation after demo           |             yes for demo | operator note           | planned |

---

## 28. Power Budget Checklist

### Before Connecting Controller

```text
[ ] battery inspected
[ ] boost converter output measured
[ ] polarity checked
[ ] ground checked
[ ] no short circuit visible
[ ] power switch checked
[ ] voltage documented
```

### Before Connecting Sensors

```text
[ ] controller boots
[ ] 3.3 V rail not overloaded
[ ] module voltage compatibility checked
[ ] I2C wiring checked
[ ] ground common
```

### Before Connecting LED Ring

```text
[ ] LED voltage checked
[ ] brightness set low
[ ] LED ground common
[ ] data pin correct
[ ] no full-white stress test at first
```

### Before Connecting Servos

```text
[ ] servo rail voltage measured
[ ] servo ground common with controller
[ ] capacitor installed or planned
[ ] servo wiring checked
[ ] movement disabled by default
[ ] emergency stop method ready
```

### Before Battery Operation

```text
[ ] bench power tests passed
[ ] voltage drop tested
[ ] battery secured
[ ] battery wires protected
[ ] power switch reachable
[ ] charging method understood
[ ] no overheating observed
```

---

## 29. Power Budget Change Rules

Whenever a power component changes, update:

```text
hardware/power_budget.md
hardware/wiring.md
hardware/BOM.md
hardware/assembly_notes.md
docs/current_status.md
docs/limitations.md
CHANGELOG.md
```

Examples of changes that require documentation:

```text
new battery capacity
new boost converter
separate servo rail added
LED count changed
servo model changed
audio amplifier added
camera model changed
battery monitor added
```

Power changes can affect safety, movement and runtime. They must not remain undocumented.

---

## 30. Known Power Limitations

Current known limitations:

```text
exact current draw is not measured yet
final battery is not selected yet
servo current under real load is unknown
boost converter capacity is unknown
battery runtime is unknown
LED current depends on brightness
audio current depends on volume
controller reset behavior under servo load is unknown
power rail separation is planned but not validated
battery monitoring may not exist in V0
```

These limitations must remain visible until real tests are completed.

---

## 31. Recommended First Power Milestone

The first power milestone is:

```text
Controller boots reliably from verified 5 V power, LED ring works at low brightness, IMU returns values and no reset occurs.
```

Required evidence:

```text
voltage measurement note
terminal output
LED test video
IMU test output
```

Expected status:

```text
controller power: bench-tested
LED power: bench-tested
IMU power: bench-tested
servo power: not tested yet
movement: disabled
```

---

## 32. Recommended Second Power Milestone

The second power milestone is:

```text
Servo rail is measured, one servo is detected, and no movement occurs during scan.
```

Required evidence:

```text
servo rail voltage note
servo scan terminal output
photo of wiring
```

Expected status:

```text
servo rail idle: bench-tested
servo communication: bench-tested
movement: still disabled
```

---

## 33. Recommended Third Power Milestone

The third power milestone is:

```text
One servo performs a safe nudge and the controller does not reset.
```

Required evidence:

```text
video of safe nudge
terminal output
voltage note during or after movement
operator note about heat
```

Expected status:

```text
one-servo movement power: bench-tested
two-servo movement power: not yet
```

---

## 34. Recommended Fourth Power Milestone

The fourth power milestone is:

```text
Both servos perform a safe nudge and return to neutral without voltage instability.
```

Required evidence:

```text
video
session log
voltage note
heat observation
```

Expected status:

```text
servo power under small movement: bench-tested
safe integrated movement: prepared
```

---

## 35. Recommended Fifth Power Milestone

The fifth power milestone is:

```text
MicroBot Round V0 completes a short integrated demo on stable power.
```

Required evidence:

```text
full demo video
session log
final report
camera snapshot
post-demo heat observation
```

Expected status:

```text
power system: hardware-validated for short supervised demo
battery operation: separate validation if used
```

---

## 36. Public Claim Rules

Do not claim:

```text
MicroBot has validated battery runtime
MicroBot can operate for hours
MicroBot power system is fully safe
MicroBot can run all modules at full load
MicroBot can move continuously without power issues
```

unless there is real evidence.

Correct early claim:

```text
MicroBot Round V0 includes a planned power architecture with separate controller and servo rail strategy. Power stability must be validated through bench tests before movement and demo operation.
```

Correct later claim after tests:

```text
MicroBot Round V0 completed a short supervised demo on validated 5 V power without controller reset during safe movement.
```

---

## 37. Final Power Budget Statement

The power system is one of the most important parts of MicroBot Round V0.

A small robot can still fail if the power system is weak.

The first power goal is not long runtime. The first goal is stable, measurable, safe power during short controlled tests.

A successful V0 power system means:

```text
voltage is measured before connection
controller boots reliably
sensors read correctly
LEDs work at safe brightness
servos can be scanned safely
small servo movement does not reset the controller
battery is secured if used
power switch is reachable
heat is monitored
all results are documented
```

Only after this should MicroBot Round V0 move toward integrated autonomous demo testing.
