# Wiring

## 1. Purpose of This Document

This document defines the wiring plan for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The goal of this document is to describe how the main controller, sensors, servos, LED ring, audio modules, power system and safety-related components should be connected during the V0 build.

This is not a final PCB design. It is a prototype wiring plan for a modular bench robot. The first version may use jumper wires, small breakout boards, temporary mounting and hand-routed cables. However, even a prototype must be wired carefully because incorrect voltage, weak ground, reversed polarity or loose wires can damage components or cause unsafe servo behavior.

The wiring plan follows four rules:

```text
1. Measure voltage before connecting electronics.
2. Share common ground between all modules.
3. Test one subsystem at a time.
4. Do not move servos before power and safety checks are complete.
```

---

## 2. Wiring Status

Current wiring status:

```text
Wiring plan: prepared
Physical wiring: not completed yet
Controller wiring: planned
Sensor wiring: planned
Servo wiring: planned
Power wiring: planned
Battery wiring: planned
Audio wiring: planned
LED wiring: planned
Safety validation: not completed yet
```

This document defines the intended V0 wiring. Actual pin assignments and voltage choices must be confirmed after the final hardware is selected.

---

## 3. Target Hardware Architecture

The target hardware architecture for MicroBot Round V0 is:

```text
Battery / Bench Power
        |
        v
Power Regulation
        |
        +---------------------> Raspberry Pi / Main Controller
        |
        +---------------------> Servo Power Rail
        |
        +---------------------> Sensors / LED / Audio Modules
        |
        v
Common Ground Shared by All Modules
```

The main controller communicates with:

```text
IMU through I2C
Distance sensor through I2C
LED ring through one GPIO data pin
Servos through UART or serial bus
Camera through CSI ribbon connector
Speaker amplifier through I2S
Microphone through I2S
Battery monitor through ADC or dedicated module if available
Dashboard through Wi-Fi or local network
```

---

## 4. Central Wiring Rule: Common Ground

All electronic modules that exchange signals must share a common ground.

This includes:

```text
main controller ground
servo ground
LED ring ground
IMU ground
distance sensor ground
audio amplifier ground
microphone ground
battery/power module ground
boost converter ground
```

Without common ground, signal lines may behave unpredictably.

Common ground does not mean every module must use the same voltage rail. It means all reference grounds are connected.

Example:

```text
Raspberry Pi 5 V rail -> controller power
Servo 5 V rail        -> servo power
Both GND rails        -> connected together
```

This allows the controller to send valid signals to the servos while keeping servo current spikes more isolated.

---

## 5. Voltage Domains

MicroBot Round V0 may contain multiple voltage domains.

Typical voltage domains:

```text
Battery voltage: around 3.7 V nominal for 1S LiPo / Li-ion
Controller voltage: 5 V input
Servo voltage: commonly around 5 V depending on selected servo
Logic voltage: 3.3 V for Raspberry Pi GPIO
I2C sensor voltage: often 3.3 V or 5 V depending on breakout board
LED voltage: often 5 V for WS2812B / NeoPixel-type LEDs
Audio amplifier voltage: often 3.3 V or 5 V depending on module
```

Important rule:

```text
Raspberry Pi GPIO is 3.3 V logic and is not 5 V tolerant.
```

This means that any signal going into the Raspberry Pi GPIO must be safe for 3.3 V logic.

If a module outputs 5 V logic, a level shifter or voltage divider may be required.

---

## 6. Recommended V0 Power Strategy

The safest V0 strategy is to separate controller power and servo power while keeping ground common.

Recommended prototype strategy:

```text
5 V controller rail:
    Raspberry Pi / main controller
    sensors where compatible
    audio modules where compatible

5 V servo rail:
    left servo
    right servo
    capacitor near servo power input

Common ground:
    controller ground connected to servo ground
```

This reduces the chance that servo current spikes reset the controller.

If using one shared 5 V rail, mark it clearly as a prototype limitation and test voltage drop during movement.

---

## 7. Power Wiring Overview

### 7.1 Bench Testing Power

Before battery operation, use a stable USB power supply or bench supply.

Bench testing order:

```text
1. Power main controller only.
2. Power controller + LED.
3. Power controller + IMU.
4. Power controller + camera.
5. Power controller + distance sensor.
6. Power servo rail without movement.
7. Power one servo and scan only.
8. Power two servos and scan only.
9. Perform safe servo nudge.
10. Move to battery operation only after stable bench tests.
```

### 7.2 Battery Power Path

Recommended battery path:

```text
Battery
  -> charger/protection module
  -> main power switch
  -> boost converter/regulator
  -> 5 V output rail
```

If separate rails are used:

```text
Battery
  -> charger/protection module
  -> main power switch
  -> boost converter A -> controller 5 V rail
  -> boost converter B -> servo 5 V rail
```

Ground must remain common.

### 7.3 Capacitor Placement

Place a capacitor near the servo power input.

Recommended capacitor:

```text
470 µF to 1000 µF
10 V or higher rating
electrolytic capacitor
```

Purpose:

```text
reduce voltage dips
absorb short current spikes
improve servo rail stability
reduce controller reset risk
```

Polarity must be correct:

```text
capacitor positive leg -> 5 V servo rail
capacitor negative leg -> GND
```

Incorrect capacitor polarity can damage the capacitor and circuit.

---

## 8. Main Controller Wiring

Recommended controller:

```text
Raspberry Pi Zero 2 W
```

The main controller should connect to:

```text
power input
ground
I2C sensors
UART servo bus
LED data pin
I2S audio output
I2S microphone input
CSI camera ribbon
optional stop button
optional battery monitor
```

The exact pins must be confirmed in `hardware/pinout.md`.

This document describes the logical wiring, not final pin assignment.

---

## 9. Camera Wiring

The camera should connect through the Raspberry Pi CSI camera connector.

Wiring type:

```text
CSI ribbon cable
```

Important notes:

```text
Use a Pi Zero compatible camera ribbon.
Insert the ribbon in the correct orientation.
Do not bend the ribbon sharply.
Do not crush the ribbon when closing the shell.
Keep the camera opening clear.
Secure the camera before movement tests.
```

Camera validation:

```text
capture one frame
save to evidence/photos/
confirm file size is greater than zero
open image after capture
log camera status
```

The camera should not be used as a safety-critical obstacle detector in V0 unless its behavior is validated.

---

## 10. I2C Sensor Wiring

The IMU and distance sensor may share the I2C bus if their addresses do not conflict.

Typical I2C connections:

```text
controller 3.3 V or module-compatible VCC -> sensor VCC
controller GND -> sensor GND
controller SDA -> sensor SDA
controller SCL -> sensor SCL
```

I2C modules:

```text
IMU: MPU-6050 or similar
Distance sensor: VL53L0X / VL53L1X or similar
Optional light sensor: BH1750 or similar
```

Important notes:

```text
Check whether the breakout board supports 3.3 V.
Do not connect 5 V logic directly to Raspberry Pi GPIO.
Avoid very long I2C wires inside the robot.
Keep I2C wires away from servo power wires if possible.
If readings are unstable, shorten wires and check pull-ups.
```

I2C validation:

```text
detect device address
read sensor values
move or tilt sensor and observe changing values
log sensor status
```

---

## 11. IMU Wiring

The IMU is a safety-relevant sensor.

Logical wiring:

```text
IMU VCC -> controller 3.3 V or compatible sensor supply
IMU GND -> common ground
IMU SDA -> controller I2C SDA
IMU SCL -> controller I2C SCL
```

Optional pins such as interrupt pins can remain unused in V0 unless needed.

IMU placement:

```text
mount near the center of the robot body if possible
keep orientation consistent
secure the module so it does not move independently
document physical orientation
avoid loose mounting
```

IMU validation:

```text
read acceleration
read gyro values
detect flat state
detect forward tilt
detect side tilt
trigger movement block if tilt threshold is exceeded
```

The robot must not perform autonomous movement if the IMU is unavailable or returns invalid values.

---

## 12. Distance Sensor Wiring

A distance sensor is strongly recommended for obstacle detection.

Logical wiring for an I2C ToF sensor:

```text
Distance sensor VCC -> compatible 3.3 V or 5 V supply depending on module
Distance sensor GND -> common ground
Distance sensor SDA -> controller I2C SDA
Distance sensor SCL -> controller I2C SCL
```

Placement:

```text
front-facing
clear line of sight
not blocked by shell
not blocked by cables
aligned with expected movement direction
```

Obstacle safety logic:

```text
if distance < stop threshold:
    block MOVE_FORWARD_SMALL
    allow STOP
    optionally allow TURN_LEFT_SMALL or TURN_RIGHT_SMALL
```

Distance sensor validation:

```text
read distance with no object nearby
place object at known distance
verify reading changes
define warning threshold
define stop threshold
log obstacle event
```

---

## 13. LED Ring Wiring

The LED ring gives visual state feedback.

Typical LED wiring:

```text
LED VCC -> 5 V rail or compatible LED supply
LED GND -> common ground
LED DIN -> controller GPIO data pin
```

Recommended additional component:

```text
small series resistor on LED data line if needed
capacitor across LED power rail if using many LEDs
```

Important notes:

```text
LED rings such as WS2812B often use 5 V power.
Data signal compatibility must be checked.
Keep LED brightness low during early testing to reduce current draw.
Do not power many LEDs at full white brightness from a weak rail.
```

Recommended LED states:

```text
white = boot / self-check
blue = idle
green = OK
yellow = warning
red = safe mode / error
purple = decision cycle
orange = obstacle detected
cyan = listening / perception
```

LED validation:

```text
show red
show green
show blue
show white
show idle blue
show safe mode red
```

---

## 14. Servo Bus Wiring

The servos control the legs and are safety-critical.

Preferred actuator type:

```text
small serial bus servo with position feedback
```

Logical wiring:

```text
Servo VCC -> servo 5 V power rail
Servo GND -> common ground
Servo DATA -> controller UART / serial bus data line through required wiring interface
```

Some serial bus servos use half-duplex UART, where transmit and receive may share one data line. The exact wiring depends on the selected servo model and adapter circuit.

Important rules:

```text
Do not connect servo power before checking voltage.
Do not move servo before scanning ID.
Do not run full movement before safe nudge.
Do not allow raw servo commands from autonomy.
Do not let servo wires touch moving legs.
Keep servo power wires thicker or shorter when possible.
```

Servo validation sequence:

```text
1. Check servo rail voltage.
2. Connect one servo.
3. Run servo scan without movement.
4. Read current position.
5. Enable torque briefly.
6. Move a very small amount.
7. Return to original or neutral position.
8. Disable torque.
9. Repeat with second servo.
10. Test both servos together.
```

The first servo test must not be walking.

---

## 15. Servo Rail Wiring

Recommended servo rail:

```text
5 V regulated rail sized for servo current
common ground with controller
capacitor near servo input
short wires when possible
secure connectors
```

Servo rail should be tested for:

```text
idle voltage
voltage during small movement
controller reset during movement
servo overheating
wire heating
unstable communication
```

If servo movement resets the controller, possible causes include:

```text
weak power supply
shared rail voltage drop
missing capacitor
thin wires
poor ground
servo stall
movement too aggressive
```

Mitigation:

```text
separate servo power rail
add capacitor
reduce movement amplitude
reduce speed
check mechanical binding
use stronger regulator
shorten wires
```

---

## 16. Audio Output Wiring

Audio output may use an I2S amplifier and small speaker.

Typical I2S amplifier wiring:

```text
Amplifier VIN -> 5 V or 3.3 V depending on module
Amplifier GND -> common ground
Amplifier BCLK -> controller I2S bit clock
Amplifier LRCLK / WS -> controller I2S word select
Amplifier DIN -> controller I2S data output
Speaker + -> amplifier output +
Speaker - -> amplifier output -
```

Important notes:

```text
Do not connect speaker directly to GPIO.
Use amplifier output for speaker.
Keep speaker wires away from IMU if possible.
Mount speaker opening so sound is not fully blocked.
```

Audio validation:

```text
play test phrase
play test tone
confirm volume
log audio status
```

If audio fails, the robot can still use LED and terminal output.

---

## 17. Microphone Wiring

The microphone may use an I2S digital microphone.

Typical I2S microphone wiring:

```text
Microphone VCC -> 3.3 V or module-compatible supply
Microphone GND -> common ground
Microphone BCLK -> controller I2S bit clock
Microphone LRCLK / WS -> controller I2S word select
Microphone DOUT -> controller I2S data input
```

Important notes:

```text
I2S microphone and I2S amplifier may share clock lines.
Data input and data output must be assigned correctly.
Microphone placement affects sound quality.
Avoid placing microphone directly against speaker to reduce feedback.
```

Microphone validation:

```text
record short sample
measure RMS or input level
produce sound near microphone
verify level changes
log microphone status
```

Voice command recognition is not required for V0.

---

## 18. Optional Button Wiring

A physical button may be used for manual start, mode selection or stop.

Recommended button uses:

```text
manual safe stop
start demo
switch between idle and demo mode
```

Typical button wiring:

```text
one side -> GPIO input
other side -> GND
internal pull-up enabled in software
```

Important notes:

```text
software debounce is required
button must be physically reachable
button should not replace main power switch
for early tests, physical power switch remains the most reliable stop
```

---

## 19. Optional Battery Monitor Wiring

Battery monitoring may require an ADC because Raspberry Pi GPIO does not provide analog input.

Possible options:

```text
external ADC module
battery fuel gauge module
safe voltage divider into ADC
power bank status if using USB power bank
mocked battery status in software
```

Important warning:

```text
Do not connect battery voltage directly to Raspberry Pi GPIO.
```

If battery monitoring is not implemented, software should clearly report:

```text
Battery monitor: unavailable or mocked
```

Movement may still be tested on bench power if voltage is stable and documented.

---

## 20. Wiring Order

The recommended wiring order is:

```text
1. Controller power only
2. LED ring
3. IMU
4. Camera
5. Distance sensor
6. Audio output
7. Microphone
8. Servo rail without movement
9. One servo scan
10. Two servo scan
11. Safe servo nudge
12. Battery power
13. Internal shell integration
14. Full self-check
15. Hello MicroBot demo
```

This order avoids debugging too many unknowns at once.

Do not wire every module at once and then attempt the full demo.

---

## 21. Pre-Power Checklist

Before powering the robot, check:

```text
polarity
voltage
ground
loose wires
exposed conductors
battery condition
switch position
boost converter output
servo rail voltage
controller power input
sensor voltage compatibility
```

Required measurement:

```text
measure regulator output before connecting controller
measure servo rail before connecting servos
```

The multimeter is mandatory.

---

## 22. Pre-Movement Checklist

Before moving servos, check:

```text
servo rail voltage measured
servo ground connected to controller ground
servo ID detected
servo position readable
movement amplitude configured
movement timeout configured
emergency stop method available
legs not mounted yet or movement clearance checked
robot not near table edge
operator supervising
```

Movement must remain disabled by default until servo validation is complete.

---

## 23. Internal Cable Routing

Inside the rounded shell, cables must be routed so they do not interfere with movement.

Cable routing rules:

```text
keep power wires away from moving legs
keep camera ribbon uncrushed
keep IMU fixed and stable
keep servo wires secured
keep battery wires protected
avoid sharp bends
avoid cables crossing the leg path
leave slack for opening the shell
avoid excessive slack near moving parts
```

Use:

```text
small zip ties
heat-shrink tubing
mounting tape
printed cable channels if available
labels for important wires
```

Do not close the shell if wires are being crushed.

---

## 24. Wiring Documentation Requirements

Every physical wiring change must be documented.

Update:

```text
hardware/wiring.md
hardware/pinout.md
hardware/power_budget.md
hardware/assembly_notes.md
docs/current_status.md
CHANGELOG.md
```

If a pin changes, update `hardware/pinout.md`.

If a voltage or rail changes, update `hardware/power_budget.md`.

If cable routing or mounting changes, update `hardware/assembly_notes.md`.

---

## 25. First Wiring Milestone

The first wiring milestone is:

```text
Controller powers on, LED ring works, IMU returns values and a session log can be created.
```

Required components:

```text
main controller
microSD card
stable power
LED ring
IMU
wires
common ground
Python environment
```

Expected status after milestone:

```text
controller: bench-tested
LED ring: bench-tested
IMU: bench-tested
logging: validated-offline or bench-tested
movement: still disabled
```

---

## 26. Second Wiring Milestone

The second wiring milestone is:

```text
Camera captures a frame and saves it to evidence/photos/.
```

Required components:

```text
camera module
Pi Zero compatible camera ribbon
camera software
evidence folder
```

Expected status after milestone:

```text
camera: bench-tested
visual evidence: available
```

---

## 27. Third Wiring Milestone

The third wiring milestone is:

```text
Servo bus detects both servos without movement.
```

Required components:

```text
two serial bus servos
servo power rail
servo data wiring
common ground
servo scan script
```

Expected status after milestone:

```text
servo bus: bench-tested
movement: still disabled
```

---

## 28. Fourth Wiring Milestone

The fourth wiring milestone is:

```text
Each servo performs a safe nudge and returns to neutral without resetting the controller.
```

Required components:

```text
validated servo power
safe movement script
servo position read
movement timeout
operator supervision
```

Expected status after milestone:

```text
servo movement: bench-tested
safe nudge: bench-tested
walking: still planned
```

---

## 29. Fifth Wiring Milestone

The fifth wiring milestone is:

```text
Distance sensor blocks forward movement when an obstacle is too close.
```

Required components:

```text
distance sensor
safety layer
obstacle threshold
action selector
logging
```

Expected status after milestone:

```text
obstacle detection: bench-tested
obstacle stop: bench-tested
forward movement safety: prepared
```

---

## 30. Common Wiring Errors

Common errors to avoid:

```text
connecting 5 V signal directly into 3.3 V GPIO
forgetting common ground
reversing battery polarity
boost converter output not measured
servo rail too weak
servo current resetting controller
camera ribbon inserted backward
I2C SDA and SCL swapped
wrong GPIO pin in software
LED brightness too high
servo data line wired incorrectly
loose jumper disconnecting during movement
wires blocking legs
closing shell on battery wires
```

Each error should be documented if encountered.

Failure notes are useful evidence.

---

## 31. Wiring Safety Matrix

| Subsystem       | Main Risk              | Required Check            | Movement Allowed If Fails?  |
| --------------- | ---------------------- | ------------------------- | --------------------------- |
| Main power      | wrong voltage or reset | measure voltage           | no                          |
| Servo power     | current spike or stall | voltage under movement    | no                          |
| Common ground   | invalid signals        | continuity / wiring check | no                          |
| IMU             | no tilt detection      | read valid values         | no                          |
| Distance sensor | obstacle missed        | threshold test            | depends on mode             |
| Camera          | no visual evidence     | capture frame             | yes, if not safety-critical |
| LED ring        | no visual feedback     | color test                | yes, with terminal warning  |
| Speaker         | no voice output        | audio test                | yes                         |
| Microphone      | no audio input         | input level test          | yes                         |
| Dashboard       | control unavailable    | local safety active       | yes, if local script works  |

---

## 32. Wiring Validation Checklist

### Power

```text
[ ] battery or bench power identified
[ ] regulator output measured
[ ] controller voltage safe
[ ] servo rail voltage safe
[ ] common ground connected
[ ] power switch works
[ ] no overheating at idle
```

### Controller

```text
[ ] controller boots
[ ] Python runs
[ ] repository exists on controller
[ ] required interfaces enabled
[ ] GPIO header available
```

### Sensors

```text
[ ] IMU wired
[ ] IMU detected
[ ] IMU values change when tilted
[ ] camera ribbon connected
[ ] camera captures frame
[ ] distance sensor wired
[ ] distance changes with object position
```

### Feedback

```text
[ ] LED ring wired
[ ] LED ring shows colors
[ ] speaker amplifier wired
[ ] speaker plays test phrase
[ ] microphone wired
[ ] microphone detects level or records sample
```

### Servos

```text
[ ] servo power measured
[ ] servo ground common with controller
[ ] servo data wired
[ ] servo ID detected
[ ] servo position readable
[ ] safe nudge works
[ ] torque off works
[ ] no controller reset during nudge
```

### Mechanical Integration

```text
[ ] wires do not block legs
[ ] battery secured
[ ] camera opening clear
[ ] LED visible
[ ] shell can close
[ ] switch reachable
[ ] charging access reachable
```

---

## 33. Recommended Wiring Evidence

Save evidence during wiring.

Recommended evidence:

```text
photo of power wiring
photo of controller wiring
photo of I2C sensor wiring
photo of servo wiring
photo of internal cable routing
photo of assembled robot before closing shell
video of LED test
terminal output of IMU test
camera snapshot
terminal output of servo scan
video of safe servo nudge
```

Recommended evidence locations:

```text
evidence/photos/
evidence/videos/
evidence/reports/
logs/
```

---

## 34. Wiring Change Log Template

Use this template when wiring changes.

```text
Date:
Subsystem:
Old wiring:
New wiring:
Reason for change:
Test performed:
Result:
Evidence:
Next action:
```

Example:

```text
Date: 2026-06-13
Subsystem: IMU
Old wiring: temporary jumper wires
New wiring: shorter female-female wires
Reason for change: unstable I2C readings
Test performed: test_imu.py
Result: readings stable after wire reduction
Evidence: terminal output saved
Next action: update pinout.md
```

---

## 35. V0 Prototype Wiring Statement

MicroBot Round V0 wiring is intentionally modular.

The first version may not be beautiful internally, but it must be safe, documented and testable.

A successful V0 wiring setup means:

```text
the controller powers on reliably
all grounds are common
sensors return valid readings
LED status works
camera saves frames
servos can be detected before movement
servo movement does not reset the controller
wires do not block mechanical movement
battery and power wiring are safe
all changes are documented
```

The wiring is ready for integrated testing only when power, sensors, feedback and servos have each passed their own basic tests.

---

## 36. Final Wiring Statement

The wiring layer connects the MicroBot idea to physical reality.

Bad wiring can make good software fail.

Good wiring makes the robot testable, repairable and safe.

The first MicroBot Round V0 wiring goal is not a perfect internal layout. The first goal is a reliable prototype that can be powered, inspected, measured, tested and improved.

No autonomous behavior should be trusted until the wiring is stable.

No movement should be trusted until power and ground are correct.

No public demo should be recorded until the wiring has been checked, tested and documented.
