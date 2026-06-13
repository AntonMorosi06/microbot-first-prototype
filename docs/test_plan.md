# Test Plan

## 1. Purpose of This Document

This document defines the test plan for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The goal of the test plan is to validate MicroBot progressively, one subsystem at a time, before attempting integrated movement or autonomous behavior. The project must not jump directly from assembly to full demo. Each component must be tested individually, then in combination, then inside the assembled robot, and finally inside the full safety-aware demo.

MicroBot Round V0 is an early robotics prototype. For this reason, testing must prioritize:

```text
power safety
component validation
sensor reliability
servo safety
mechanical clearance
safe movement
logging
evidence collection
repeatability
honest status tracking
```

A feature should not be marked as working unless it has been tested, documented and, when possible, supported by evidence.

---

## 2. Testing Philosophy

MicroBot Round V0 follows an evidence-based testing approach.

The purpose of testing is not only to make the robot work once. The purpose is to understand what works, what fails, what is unstable, what needs calibration and what can be safely demonstrated.

The testing philosophy is based on six principles.

### 2.1 Test Small Before Testing Complete

Each subsystem must be tested independently before full integration.

Correct order:

```text
test LED alone
test IMU alone
test camera alone
test distance sensor alone
test audio alone
test servo bus alone
test safe servo nudge
test self-check
test safety layer
test integrated demo
```

Incorrect order:

```text
assemble everything
run full autonomous demo immediately
debug all failures at once
```

### 2.2 No Movement Without Safety

Any test that moves servos must include movement limits.

Before movement, the robot must know:

```text
servo IDs
servo neutral positions
servo safe range
movement amplitude
movement speed
movement timeout
emergency stop method
```

The first actuator test must be a small safe nudge, not a walking gait.

### 2.3 Every Test Must Produce a Clear Result

Each test must produce one of the following outcomes:

```text
PASS
PASS_WITH_WARNING
FAIL
BLOCKED_FOR_SAFETY
NOT_TESTED
```

Unclear results should not be treated as successful.

### 2.4 Test Results Must Update Documentation

After each relevant test, update:

```text
docs/current_status.md
docs/limitations.md
docs/safety.md if safety behavior changed
hardware/pinout.md if wiring changed
hardware/power_budget.md if power behavior changed
mechanical/print_notes.md if mechanical fit changed
CHANGELOG.md
```

### 2.5 Evidence Matters

A test is stronger when it produces evidence.

Evidence can include:

```text
terminal output
session log
camera snapshot
photo
video
final report
measured voltage
measured temperature
failure note
```

### 2.6 Repeatability Is Required

A test should not be considered stable after one lucky success.

Recommended minimum:

```text
3 successful repeated runs
```

A feature becomes more credible when it works repeatedly under the same conditions.

---

## 3. Status Vocabulary for Testing

This project uses realistic test status labels.

### planned

The test is described but not implemented yet.

### prepared

The test file or procedure exists, but it has not been executed yet.

### mocked

The test runs with simulated data or placeholder hardware behavior.

### validated-offline

The test works without real robot hardware.

### bench-tested

The test works on real hardware components outside or before full assembly.

### hardware-validated

The test works on the assembled MicroBot Round V0 robot.

### integrated

The feature works together with other subsystems.

### demo-ready

The test or feature works repeatedly, safely and can be shown publicly.

---

## 4. Test Environment

The first tests should be performed in a controlled indoor environment.

Recommended environment:

```text
clean desk
flat surface
good lighting
stable power source
laptop or monitor nearby
multimeter available
robot away from table edges
no fragile objects nearby
no liquids nearby
operator supervision
```

Avoid:

```text
testing near stairs
testing near pets
testing near children
testing near water
testing on unstable surfaces
testing with low battery
testing with loose wires near moving parts
testing aggressive movement early
```

---

## 5. Required Tools for Testing

Recommended tools:

```text
laptop or desktop computer
Raspberry Pi or selected controller
microSD card
USB power supply
battery if already validated
multimeter
small screwdriver set
wire cutters
wire stripper
tweezers
electrical tape or heat-shrink tubing
3D printed body parts
phone or camera for evidence
notebook or build log
```

Optional tools:

```text
bench power supply
USB power meter
logic analyzer
oscilloscope
thermal camera
calipers
soldering station
hot glue or temporary mounting material
```

The minimum tool required before powering electronics is a multimeter.

---

## 6. Test Evidence Structure

Test evidence should be saved in the repository when appropriate.

Recommended evidence locations:

```text
logs/
evidence/photos/
evidence/videos/
evidence/reports/
```

Recommended naming pattern:

```text
logs/session_<date>_<id>.json
evidence/photos/<date>_<test_name>.jpg
evidence/videos/<date>_<test_name>.mp4
evidence/reports/<date>_<test_name>_report.md
```

Example:

```text
logs/session_2026-06-13_001.json
evidence/photos/2026-06-13_camera_test_boot_frame.jpg
evidence/videos/2026-06-13_safe_servo_nudge.mp4
evidence/reports/2026-06-13_self_check_report.md
```

Large videos should not necessarily be committed directly to Git if they are too large. They may be stored externally or attached through releases.

---

## 7. Test Result Format

Each test should be documented using the following format.

```text
Test ID:
Test name:
Date:
Operator:
Hardware revision:
Software version:
Test status:
Command executed:
Expected result:
Actual result:
Evidence saved:
Notes:
Next action:
```

Example:

```text
Test ID: T-LED-001
Test name: LED boot animation test
Date: 2026-06-13
Operator: Anton Morosi
Hardware revision: V0 bench wiring
Software version: 0.1.0
Test status: PASS_WITH_WARNING
Command executed: python setup/scripts/test_leds.py
Expected result: LED ring shows red, green, blue, white and idle blue.
Actual result: LED ring works, but brightness should be reduced.
Evidence saved: evidence/videos/2026-06-13_led_test.mp4
Notes: LED pin confirmed. Brightness 255 is too high for indoor demo.
Next action: reduce default brightness in config.py.
```

---

## 8. Test Phases Overview

The complete test plan is divided into ten phases.

```text
Phase 0  - Repository and documentation tests
Phase 1  - Power and electrical safety tests
Phase 2  - Controller and environment tests
Phase 3  - Sensor and feedback tests
Phase 4  - Servo and actuator tests
Phase 5  - Mechanical fit and movement clearance tests
Phase 6  - Safety layer tests
Phase 7  - Self-check and logging tests
Phase 8  - Autonomy and behavior tests
Phase 9  - Integrated demo tests
Phase 10 - Evidence and release-readiness tests
```

Each phase must be completed progressively.

---

# Phase 0 — Repository and Documentation Tests

## 9. Phase 0 Goal

Verify that the repository structure and documentation baseline are ready before hardware testing begins.

## 10. Phase 0 Required Files

Required files:

```text
README.md
CHANGELOG.md
LICENSE.md
.gitignore
docs/architecture.md
docs/build_plan.md
docs/current_status.md
docs/safety.md
docs/limitations.md
docs/demo_script.md
docs/test_plan.md
docs/portfolio_note.md
hardware/BOM.md
hardware/wiring.md
hardware/pinout.md
hardware/power_budget.md
hardware/assembly_notes.md
mechanical/README.md
mechanical/print_notes.md
mechanical/design_requirements.md
```

## 11. T-DOC-001 — Repository Structure Test

### Objective

Verify that the repository structure exists and follows the expected layout.

### Procedure

Run:

```bash
find . -maxdepth 3 -type f | sort
find . -maxdepth 3 -type d | sort
```

### Expected Result

The repository contains the required folders:

```text
docs
hardware
mechanical
setup
autonomy
dashboard
simulation
demos
evidence
logs
references
```

### Pass Criteria

The structure exists and no major folder is missing.

### Status

```text
prepared
```

---

## 12. T-DOC-002 — Documentation Completeness Test

### Objective

Verify that the main documentation files are populated.

### Procedure

Check that each required markdown file exists and contains meaningful content.

### Expected Result

Each document includes:

```text
purpose
scope
current status
limitations or next steps
```

### Pass Criteria

The repository can be understood by another person without external explanation.

### Status

```text
prepared
```

---

## 13. T-DOC-003 — Claim Accuracy Test

### Objective

Verify that the repository does not overclaim unvalidated features.

### Procedure

Search for exaggerated claims.

Terms to review:

```text
fully autonomous
complete AI
understands everything
swarm-ready
commercial-ready
validated walking
self-learning
```

### Expected Result

Any future feature is marked as planned, mocked, prepared or future work unless validated.

### Pass Criteria

No unvalidated feature is presented as completed.

### Status

```text
prepared
```

---

# Phase 1 — Power and Electrical Safety Tests

## 14. Phase 1 Goal

Validate the power system before connecting sensitive electronics or moving parts.

Power is one of the highest-risk areas of the robot.

## 15. T-PWR-001 — Voltage Measurement Test

### Objective

Measure the power output before connecting the main controller.

### Procedure

1. Connect battery or power source to regulator.
2. Turn on power.
3. Use multimeter to measure output voltage.
4. Record voltage.
5. Adjust regulator if needed.
6. Do not connect controller until voltage is correct.

### Expected Result

Controller rail should be within the safe input voltage for the selected controller.

Servo rail should be within the safe operating range of selected servos.

### Pass Criteria

Measured voltage is safe and stable.

### Evidence

```text
photo of multimeter reading
hardware/power_budget.md update
```

### Status

```text
planned
```

---

## 16. T-PWR-002 — Controller Power-On Test

### Objective

Verify that the controller powers on safely.

### Procedure

1. Connect controller to verified power source.
2. Power on.
3. Observe boot behavior.
4. Confirm SSH or local terminal access.
5. Check for overheating.
6. Leave idle for several minutes.

### Expected Result

Controller boots normally and remains stable.

### Pass Criteria

No reset, no overheating, no smoke, no unstable behavior.

### Evidence

```text
photo of powered controller
terminal screenshot
notes in hardware/power_budget.md
```

### Status

```text
planned
```

---

## 17. T-PWR-003 — Servo Power Rail Idle Test

### Objective

Verify that servo power rail is stable before movement.

### Procedure

1. Connect servo power rail without movement command.
2. Measure voltage.
3. Confirm common ground.
4. Observe for heat or instability.
5. Do not move servo yet.

### Expected Result

Servo rail stays within safe voltage range.

### Pass Criteria

No overheating, no unstable voltage, no reset of controller.

### Evidence

```text
multimeter photo
wiring note
```

### Status

```text
planned
```

---

## 18. T-PWR-004 — Power Drop During Servo Nudge Test

### Objective

Check whether servo movement causes voltage drop or controller reset.

### Procedure

1. Run safe servo nudge.
2. Monitor controller stability.
3. Measure servo rail during movement if possible.
4. Record any reset, LED flicker or communication failure.

### Expected Result

Servo movement does not reset controller.

### Pass Criteria

No reboot, no brownout, no communication loss.

### Evidence

```text
video
terminal output
voltage note
```

### Status

```text
planned
```

---

# Phase 2 — Controller and Environment Tests

## 19. Phase 2 Goal

Validate that the controller operating system, Python environment and hardware interfaces are ready.

## 20. T-CTRL-001 — Operating System Boot Test

### Objective

Verify that the controller boots and is accessible.

### Procedure

1. Install operating system.
2. Boot controller.
3. Connect through SSH or local terminal.
4. Confirm system date/time.
5. Confirm network if needed.

### Expected Result

Controller is accessible and stable.

### Pass Criteria

Terminal access works.

### Evidence

```text
terminal output
setup notes
```

### Status

```text
planned
```

---

## 21. T-CTRL-002 — Python Environment Test

### Objective

Verify that Python and dependencies work.

### Procedure

Run:

```bash
python --version
python -m venv .venv
source .venv/bin/activate
pip install -r setup/requirements.txt
python -c "print('MicroBot Python environment OK')"
```

### Expected Result

Python runs and requirements install.

### Pass Criteria

No dependency errors.

### Evidence

```text
terminal output
```

### Status

```text
planned
```

---

## 22. T-CTRL-003 — Interface Availability Test

### Objective

Verify that required interfaces are enabled.

### Interfaces

Possible interfaces:

```text
I2C
UART
GPIO
camera
audio
Wi-Fi
```

### Procedure

Check each interface using system commands and test scripts.

### Expected Result

Required interfaces are available.

### Pass Criteria

Interfaces required by selected hardware are enabled.

### Evidence

```text
terminal output
configuration notes
```

### Status

```text
planned
```

---

# Phase 3 — Sensor and Feedback Tests

## 23. Phase 3 Goal

Validate each sensor and feedback component individually.

The goal is not integration yet. The goal is component-level confidence.

---

## 24. T-LED-001 — LED Ring Basic Test

### Objective

Verify that the LED ring can display colors.

### Script

```text
setup/scripts/test_leds.py
```

### Procedure

Run:

```bash
python setup/scripts/test_leds.py
```

If required by hardware:

```bash
sudo python setup/scripts/test_leds.py
```

### Expected Result

LED ring displays:

```text
red
green
blue
white
idle blue
```

### Pass Criteria

LEDs respond correctly and no controller reset occurs.

### Evidence

```text
short video
log event if available
```

### Status

```text
planned
```

---

## 25. T-LED-002 — LED State Mapping Test

### Objective

Verify that LED colors represent robot states.

### Expected Mapping

```text
white = boot / self-check
blue = idle
green = OK
yellow = warning
red = safe mode / error
purple = decision cycle
orange = obstacle
cyan = listening / perception
```

### Pass Criteria

Each state color can be triggered by software.

### Evidence

```text
video or photo sequence
```

### Status

```text
planned
```

---

## 26. T-IMU-001 — IMU Detection Test

### Objective

Verify that the IMU is detected and returns data.

### Script

```text
setup/scripts/test_imu.py
```

### Procedure

Run:

```bash
python setup/scripts/test_imu.py
```

### Expected Result

Terminal prints acceleration and gyroscope readings.

### Pass Criteria

Values are readable and update over time.

### Evidence

```text
terminal output
```

### Status

```text
planned
```

---

## 27. T-IMU-002 — Tilt Response Test

### Objective

Verify that IMU readings change when the robot is tilted.

### Procedure

1. Place robot or IMU flat.
2. Run IMU test.
3. Tilt forward.
4. Tilt backward.
5. Tilt left.
6. Tilt right.
7. Observe values.

### Expected Result

Orientation-related values change consistently.

### Pass Criteria

Tilt is detectable and can be used by safety logic.

### Evidence

```text
terminal output
short video
```

### Status

```text
planned
```

---

## 28. T-CAM-001 — Camera Capture Test

### Objective

Verify that the camera can capture and save a frame.

### Script

```text
setup/scripts/test_camera.py
```

### Procedure

Run:

```bash
python setup/scripts/test_camera.py
```

### Expected Result

A frame is saved to:

```text
evidence/photos/
```

### Pass Criteria

Image file exists, file size is greater than zero and image can be opened.

### Evidence

```text
saved image
terminal output
```

### Status

```text
planned
```

---

## 29. T-DIST-001 — Distance Sensor Detection Test

### Objective

Verify that the distance sensor returns a valid distance.

### Script

```text
setup/scripts/test_distance.py
```

### Procedure

Run:

```bash
python setup/scripts/test_distance.py
```

Place an object at different distances.

### Expected Result

Distance values change when object position changes.

### Pass Criteria

Sensor readings are reasonable and stable enough for obstacle safety.

### Evidence

```text
terminal output
photo of test setup
```

### Status

```text
planned
```

---

## 30. T-DIST-002 — Obstacle Threshold Test

### Objective

Verify that obstacle detection triggers below defined threshold.

### Procedure

1. Set stop threshold in configuration.
2. Run distance test.
3. Place object farther than threshold.
4. Confirm obstacle is false.
5. Place object closer than threshold.
6. Confirm obstacle is true.

### Expected Result

Obstacle status changes correctly.

### Pass Criteria

Forward movement can be blocked based on threshold.

### Evidence

```text
terminal output
log entry
```

### Status

```text
planned
```

---

## 31. T-AUDIO-001 — Speaker Output Test

### Objective

Verify that the robot can speak or play a sound.

### Script

```text
setup/scripts/test_audio.py
```

### Procedure

Run:

```bash
python setup/scripts/test_audio.py
```

### Expected Result

Speaker plays a test phrase or tone.

### Pass Criteria

Audio output is audible and does not crash script.

### Evidence

```text
video or audio note
terminal output
```

### Status

```text
planned
```

---

## 32. T-AUDIO-002 — Microphone Input Test

### Objective

Verify that microphone input can be recorded or measured.

### Procedure

Run audio test and produce sound near the microphone.

### Expected Result

The script detects input level or records a short sample.

### Pass Criteria

Microphone returns non-zero or changing input data.

### Evidence

```text
terminal output
recorded test file if created
```

### Status

```text
planned
```

---

## 33. T-BAT-001 — Battery or Power Status Test

### Objective

Verify that battery or power monitoring works, if implemented.

### Script

```text
setup/scripts/test_battery.py
```

### Procedure

Run:

```bash
python setup/scripts/test_battery.py
```

### Expected Result

Battery status or placeholder status is printed clearly.

### Pass Criteria

If real monitoring exists, voltage is readable.

If not implemented, output must clearly say mocked or unavailable.

### Evidence

```text
terminal output
power_budget.md update
```

### Status

```text
planned
```

---

# Phase 4 — Servo and Actuator Tests

## 34. Phase 4 Goal

Validate servos safely before attempting walking or autonomous movement.

---

## 35. T-SERVO-001 — Servo Bus Scan Test

### Objective

Verify that servo IDs can be detected without movement.

### Script

```text
setup/scripts/scan_servos.py
```

### Procedure

Run:

```bash
python setup/scripts/scan_servos.py
```

### Expected Result

Detected servo IDs are printed.

### Pass Criteria

Both left and right servos are detected.

### Evidence

```text
terminal output
log entry
```

### Status

```text
planned
```

---

## 36. T-SERVO-002 — Servo Position Read Test

### Objective

Verify that current servo position can be read.

### Procedure

Run servo test and read current positions without commanding movement.

### Expected Result

The script prints current position for each servo.

### Pass Criteria

Positions are valid and within expected range.

### Evidence

```text
terminal output
```

### Status

```text
planned
```

---

## 37. T-SERVO-003 — Safe Servo Nudge Test

### Objective

Move each servo a very small amount and return to neutral.

### Script

```text
setup/scripts/test_servos_safe.py
```

### Procedure

Run:

```bash
python setup/scripts/test_servos_safe.py
```

### Expected Result

Each servo moves slightly, returns to neutral and torque can be disabled.

### Pass Criteria

Movement is small, controlled and does not reset the controller.

### Evidence

```text
video
terminal output
log event
```

### Status

```text
planned
```

---

## 38. T-SERVO-004 — Servo Timeout Test

### Objective

Verify that servo commands do not run indefinitely.

### Procedure

Trigger a movement command with a defined timeout.

### Expected Result

Movement ends within configured time.

### Pass Criteria

No infinite movement loop occurs.

### Evidence

```text
terminal output
log event
```

### Status

```text
planned
```

---

## 39. T-SERVO-005 — Servo Torque Off Test

### Objective

Verify that servo torque can be disabled safely.

### Procedure

1. Enable torque.
2. Perform safe nudge.
3. Disable torque.
4. Confirm servo no longer actively holds position if expected.

### Expected Result

Torque disable command works.

### Pass Criteria

Robot can enter a safe non-moving state.

### Evidence

```text
terminal output
operator note
```

### Status

```text
planned
```

---

# Phase 5 — Mechanical Fit and Movement Clearance Tests

## 40. Phase 5 Goal

Validate that the physical body can contain electronics and allow movement without collision.

---

## 41. T-MECH-001 — Printed Part Inspection

### Objective

Verify quality of printed mechanical parts.

### Procedure

Inspect:

```text
shell
base
legs
feet
mounting points
sensor openings
cable passages
switch access
```

### Expected Result

Parts are usable or issues are documented.

### Pass Criteria

No critical structural failure.

### Evidence

```text
photos
mechanical/print_notes.md update
```

### Status

```text
planned
```

---

## 42. T-MECH-002 — Component Fit Test

### Objective

Verify that electronics fit inside the body.

### Procedure

Place components inside shell without final wiring.

Check:

```text
controller fit
battery fit
power module fit
LED placement
camera placement
speaker placement
sensor placement
cable routing
```

### Expected Result

Components fit or required modifications are documented.

### Pass Criteria

The body can contain the required electronics safely.

### Evidence

```text
internal photos
assembly notes
```

### Status

```text
planned
```

---

## 43. T-MECH-003 — Leg Clearance Test

### Objective

Verify that legs can move without colliding with shell or wires.

### Procedure

1. Attach servos and legs.
2. Move legs manually with power off.
3. Check shell clearance.
4. Check wire clearance.
5. Mark collision areas if any.

### Expected Result

Legs move inside the required range.

### Pass Criteria

No collision during safe movement range.

### Evidence

```text
short video
mechanical note
```

### Status

```text
planned
```

---

## 44. T-MECH-004 — Standing Stability Test

### Objective

Verify that the assembled robot can stand on a flat surface.

### Procedure

1. Place robot on flat surface.
2. Observe balance.
3. Slightly shift orientation.
4. Check whether robot tips easily.

### Expected Result

Robot stands without immediate tipping.

### Pass Criteria

Robot is stable enough for small movement tests.

### Evidence

```text
photo or video
notes about center of mass
```

### Status

```text
planned
```

---

# Phase 6 — Safety Layer Tests

## 45. Phase 6 Goal

Validate that the safety layer can block movement under unsafe conditions.

---

## 46. T-SAFE-001 — Safety Function Offline Test

### Objective

Verify safety decision logic without hardware.

### Procedure

Feed mocked robot states to the safety function:

```text
stable and clear
tilted
obstacle close
servo unavailable
battery low
unknown state
manual stop active
```

### Expected Result

Safety function returns correct result:

```text
ALLOW
BLOCK
SAFE_MODE
CRITICAL_ERROR
```

### Pass Criteria

Unsafe states do not allow movement.

### Evidence

```text
terminal output
test report
```

### Status

```text
planned
```

---

## 47. T-SAFE-002 — Tilt Stop Test

### Objective

Verify that movement is blocked when the robot is tilted.

### Procedure

1. Place robot flat.
2. Confirm movement would be allowed.
3. Tilt robot beyond threshold.
4. Request movement.
5. Confirm movement is blocked.

### Expected Result

Safety returns `SAFE_MODE` or `BLOCK`.

### Pass Criteria

No movement occurs while tilted.

### Evidence

```text
video
log event
terminal output
```

### Status

```text
planned
```

---

## 48. T-SAFE-003 — Obstacle Stop Test

### Objective

Verify that forward movement is blocked when obstacle is close.

### Procedure

1. Place robot on flat surface.
2. Confirm path clear.
3. Place object in front below threshold.
4. Request `MOVE_FORWARD_SMALL`.
5. Confirm movement is blocked or replaced with stop/turn.

### Expected Result

Forward movement is blocked.

### Pass Criteria

Obstacle produces safety event and no unsafe forward movement.

### Evidence

```text
video
log event
photo
```

### Status

```text
planned
```

---

## 49. T-SAFE-004 — Servo Failure Safety Test

### Objective

Verify that movement is blocked if servo bus is unavailable.

### Procedure

1. Disconnect servo bus or simulate unavailable servo.
2. Run self-check.
3. Request movement.
4. Confirm movement is blocked.

### Expected Result

Servo failure prevents movement.

### Pass Criteria

Robot does not attempt movement without servo validation.

### Evidence

```text
terminal output
log event
```

### Status

```text
planned
```

---

## 50. T-SAFE-005 — Emergency Stop Test

### Objective

Verify that the robot can be stopped during or before movement.

### Procedure

1. Start a safe movement test.
2. Trigger stop through available method.
3. Confirm movement stops.
4. Confirm autonomy does not resume automatically.

### Possible stop methods:

```text
keyboard interrupt
dashboard stop button
physical power switch
software STOP command
safe mode trigger
```

### Expected Result

Movement stops and event is recorded if possible.

### Pass Criteria

Emergency stop prevents continued movement.

### Evidence

```text
video
log event
```

### Status

```text
planned
```

---

## 51. T-SAFE-006 — Repeated Movement Failure Test

### Objective

Verify that repeated failed movement attempts trigger safe mode.

### Procedure

1. Simulate or create failed movement result.
2. Repeat until threshold is reached.
3. Confirm safe mode activates.

### Expected Result

Robot stops after repeated failures.

### Pass Criteria

Failure does not cause more aggressive movement.

### Evidence

```text
terminal output
log event
```

### Status

```text
planned
```

---

# Phase 7 — Self-Check and Logging Tests

## 52. Phase 7 Goal

Validate self-check and logging before integrated demo.

---

## 53. T-LOG-001 — Session Log Creation Test

### Objective

Verify that a new session log is created at startup.

### Procedure

Run:

```bash
python setup/scripts/self_check.py
```

or:

```bash
python setup/scripts/hello_microbot.py
```

### Expected Result

New log file appears in:

```text
logs/
```

### Pass Criteria

Log file exists and contains session ID, timestamp and initial event.

### Evidence

```text
logs/session_*.json
```

### Status

```text
planned
```

---

## 54. T-LOG-002 — Safety Event Logging Test

### Objective

Verify that safety events are recorded.

### Procedure

Trigger:

```text
tilt event
obstacle event
servo unavailable event
manual stop event
```

### Expected Result

Each event appears in session log.

### Pass Criteria

Safety logs include event name, timestamp and reason.

### Evidence

```text
session log
```

### Status

```text
planned
```

---

## 55. T-SELF-001 — Self-Check Complete Test

### Objective

Verify that self-check tests all required subsystems.

### Script

```text
setup/scripts/self_check.py
```

### Expected checks:

```text
log write access
LED
IMU
camera
distance sensor
audio
servo bus
battery or power status
safety state
```

### Expected Result

Self-check returns final status:

```text
OK
WARNING
FAILED
```

### Pass Criteria

Critical failures block movement.

### Evidence

```text
terminal output
session log
report
```

### Status

```text
planned
```

---

## 56. T-SELF-002 — Self-Check Failure Handling Test

### Objective

Verify that missing or failed critical components are handled safely.

### Procedure

Simulate or disconnect one subsystem at a time.

Examples:

```text
camera unavailable
IMU unavailable
servo bus unavailable
distance sensor unavailable
```

### Expected Result

Critical failures block movement. Non-critical failures produce warnings.

### Pass Criteria

Demo does not crash unpredictably.

### Evidence

```text
terminal output
log event
```

### Status

```text
planned
```

---

# Phase 8 — Autonomy and Behavior Tests

## 57. Phase 8 Goal

Validate the limited autonomous decision logic.

The first autonomy layer should not generate raw servo commands. It should choose from predefined safe actions.

---

## 58. T-AUTO-001 — Action Set Validation Test

### Objective

Verify that autonomy only selects allowed V0 actions.

Allowed actions:

```text
STOP
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
```

### Procedure

Run action selector with multiple mocked states.

### Expected Result

Only allowed actions are returned.

### Pass Criteria

No raw servo values are generated.

### Evidence

```text
terminal output
test report
```

### Status

```text
planned
```

---

## 59. T-AUTO-002 — Stable Clear Path Decision Test

### Objective

Verify decision when robot is stable and path is clear.

### Input State

```text
stable = true
obstacle = false
servo_status = OK
last_movement = OK
battery = OK
```

### Expected Result

Autonomy may select:

```text
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
STOP
```

depending on configured behavior.

### Pass Criteria

Selected action must pass safety validation.

### Evidence

```text
test output
log entry
```

### Status

```text
planned
```

---

## 60. T-AUTO-003 — Obstacle Decision Test

### Objective

Verify decision when obstacle is close.

### Input State

```text
stable = true
obstacle = true
```

### Expected Result

Autonomy should not select forward movement.

Allowed results:

```text
STOP
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
```

### Pass Criteria

No `MOVE_FORWARD_SMALL` is executed when obstacle is too close.

### Evidence

```text
log entry
test output
```

### Status

```text
planned
```

---

## 61. T-AUTO-004 — Tilt Decision Test

### Objective

Verify decision when robot is tilted.

### Input State

```text
stable = false
tilt_threshold_exceeded = true
```

### Expected Result

Autonomy selects:

```text
STOP
```

or enters:

```text
SAFE_MODE
```

### Pass Criteria

Movement is not allowed.

### Evidence

```text
log entry
test output
```

### Status

```text
planned
```

---

## 62. T-AUTO-005 — LLM Agent Placeholder Safety Test

### Objective

Verify that future AI agent output is constrained.

### Procedure

Simulate agent outputs:

```text
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
raw_servo_left_900
disable_safety
```

### Expected Result

Allowed action names pass to safety layer.

Unsafe or unknown strings are rejected.

### Pass Criteria

AI placeholder cannot bypass safety.

### Evidence

```text
test output
```

### Status

```text
planned
```

---

# Phase 9 — Integrated Demo Tests

## 63. Phase 9 Goal

Validate the first integrated demo script.

The integrated demo should combine boot sequence, self-check, sensors, safety, movement, autonomy and logging.

---

## 64. T-DEMO-001 — Hello MicroBot Dry Run

### Objective

Run the demo script without physical movement or with movement disabled.

### Procedure

Set:

```text
ENABLE_MOVEMENT = false
```

Run:

```bash
python setup/scripts/hello_microbot.py
```

### Expected Result

Demo runs through boot, self-check, sensing and logging without moving servos.

### Pass Criteria

No crash. Movement is clearly skipped.

### Evidence

```text
session log
terminal output
```

### Status

```text
planned
```

---

## 65. T-DEMO-002 — Hello MicroBot Full Bench Test

### Objective

Run the full demo with real hardware and safe movement.

### Procedure

1. Place robot on flat surface.
2. Verify pre-flight checklist.
3. Run:

```bash
python setup/scripts/hello_microbot.py
```

4. Observe behavior.
5. Stop if unsafe.

### Expected Result

Robot performs full controlled demo:

```text
LED boot
speech or terminal phrase
self-check
IMU read
camera capture
distance read
servo check
safe leg nudge
action selection
safety validation
small movement if allowed
final report
```

### Pass Criteria

Demo completes without uncontrolled movement.

### Evidence

```text
video
session log
camera snapshot
final report
```

### Status

```text
planned
```

---

## 66. T-DEMO-003 — Integrated Tilt Stop Demo

### Objective

Show that the robot stops or blocks movement when tilted.

### Procedure

1. Start demo.
2. Trigger tilt condition.
3. Request movement or allow demo to reach movement stage.
4. Confirm safety stop.

### Expected Result

Movement blocked. Safe mode or warning is activated.

### Pass Criteria

Robot does not move while tilted.

### Evidence

```text
video
log event
report entry
```

### Status

```text
planned
```

---

## 67. T-DEMO-004 — Integrated Obstacle Stop Demo

### Objective

Show that the robot blocks forward movement when obstacle is close.

### Procedure

1. Start demo.
2. Place obstacle in front.
3. Let robot evaluate action.
4. Confirm forward movement is blocked.

### Expected Result

Robot chooses STOP or turn action.

### Pass Criteria

No unsafe forward movement.

### Evidence

```text
video
camera snapshot
log event
report entry
```

### Status

```text
planned
```

---

## 68. T-DEMO-005 — Three-Run Repeatability Test

### Objective

Verify that the demo can be repeated.

### Procedure

Run the full demo three times.

```text
Run 1
Run 2
Run 3
```

### Expected Result

All runs complete safely.

### Pass Criteria

At least three successful runs with no uncontrolled movement.

### Evidence

```text
three session logs
three reports
optional video clips
```

### Status

```text
planned
```

---

# Phase 10 — Evidence and Release-Readiness Tests

## 69. Phase 10 Goal

Verify that the project is ready to be shown publicly.

---

## 70. T-REL-001 — Evidence Completeness Test

### Objective

Verify that the repository includes enough evidence for the claimed status.

### Required Evidence for First Demo

```text
session log
final report
camera snapshot
video of safe movement
video or log of safety stop
photo of assembled robot
photo of wiring
```

### Pass Criteria

Every major claim has supporting evidence.

### Status

```text
planned
```

---

## 71. T-REL-002 — README Accuracy Test

### Objective

Verify that README matches real test results.

### Procedure

Review README and compare with actual evidence.

### Pass Criteria

No unvalidated feature is described as completed.

### Status

```text
planned
```

---

## 72. T-REL-003 — Privacy and Safety Review

### Objective

Ensure public repository does not include sensitive or unsafe information.

### Check for:

```text
Wi-Fi passwords
API keys
personal addresses
private images
raw credentials
unreviewed personal files
dangerous instructions
overclaiming
```

### Pass Criteria

Repository is safe to publish.

### Status

```text
planned
```

---

## 73. T-REL-004 — Changelog Update Test

### Objective

Verify that important project milestones are recorded.

### Procedure

Update `CHANGELOG.md` after:

```text
documentation baseline
hardware bring-up
sensor validation
servo validation
self-check implementation
first demo
safety validation
```

### Pass Criteria

Changelog reflects real progress.

### Status

```text
planned
```

---

## 74. Master Test Checklist

### Documentation Tests

```text
[ ] T-DOC-001 Repository Structure Test
[ ] T-DOC-002 Documentation Completeness Test
[ ] T-DOC-003 Claim Accuracy Test
```

### Power Tests

```text
[ ] T-PWR-001 Voltage Measurement Test
[ ] T-PWR-002 Controller Power-On Test
[ ] T-PWR-003 Servo Power Rail Idle Test
[ ] T-PWR-004 Power Drop During Servo Nudge Test
```

### Controller Tests

```text
[ ] T-CTRL-001 Operating System Boot Test
[ ] T-CTRL-002 Python Environment Test
[ ] T-CTRL-003 Interface Availability Test
```

### Sensor Tests

```text
[ ] T-LED-001 LED Ring Basic Test
[ ] T-LED-002 LED State Mapping Test
[ ] T-IMU-001 IMU Detection Test
[ ] T-IMU-002 Tilt Response Test
[ ] T-CAM-001 Camera Capture Test
[ ] T-DIST-001 Distance Sensor Detection Test
[ ] T-DIST-002 Obstacle Threshold Test
[ ] T-AUDIO-001 Speaker Output Test
[ ] T-AUDIO-002 Microphone Input Test
[ ] T-BAT-001 Battery or Power Status Test
```

### Servo Tests

```text
[ ] T-SERVO-001 Servo Bus Scan Test
[ ] T-SERVO-002 Servo Position Read Test
[ ] T-SERVO-003 Safe Servo Nudge Test
[ ] T-SERVO-004 Servo Timeout Test
[ ] T-SERVO-005 Servo Torque Off Test
```

### Mechanical Tests

```text
[ ] T-MECH-001 Printed Part Inspection
[ ] T-MECH-002 Component Fit Test
[ ] T-MECH-003 Leg Clearance Test
[ ] T-MECH-004 Standing Stability Test
```

### Safety Tests

```text
[ ] T-SAFE-001 Safety Function Offline Test
[ ] T-SAFE-002 Tilt Stop Test
[ ] T-SAFE-003 Obstacle Stop Test
[ ] T-SAFE-004 Servo Failure Safety Test
[ ] T-SAFE-005 Emergency Stop Test
[ ] T-SAFE-006 Repeated Movement Failure Test
```

### Logging and Self-Check Tests

```text
[ ] T-LOG-001 Session Log Creation Test
[ ] T-LOG-002 Safety Event Logging Test
[ ] T-SELF-001 Self-Check Complete Test
[ ] T-SELF-002 Self-Check Failure Handling Test
```

### Autonomy Tests

```text
[ ] T-AUTO-001 Action Set Validation Test
[ ] T-AUTO-002 Stable Clear Path Decision Test
[ ] T-AUTO-003 Obstacle Decision Test
[ ] T-AUTO-004 Tilt Decision Test
[ ] T-AUTO-005 LLM Agent Placeholder Safety Test
```

### Demo Tests

```text
[ ] T-DEMO-001 Hello MicroBot Dry Run
[ ] T-DEMO-002 Hello MicroBot Full Bench Test
[ ] T-DEMO-003 Integrated Tilt Stop Demo
[ ] T-DEMO-004 Integrated Obstacle Stop Demo
[ ] T-DEMO-005 Three-Run Repeatability Test
```

### Release Tests

```text
[ ] T-REL-001 Evidence Completeness Test
[ ] T-REL-002 README Accuracy Test
[ ] T-REL-003 Privacy and Safety Review
[ ] T-REL-004 Changelog Update Test
```

---

## 75. Definition of Test Completion

MicroBot Round V0 can be considered test-ready when:

```text
documentation tests pass
power tests pass
controller tests pass
at least one sensor test passes
logging works
safety layer exists
movement remains disabled by default
```

MicroBot Round V0 can be considered movement-ready when:

```text
servo bus scan passes
servo position read passes
safe servo nudge passes
power does not drop during movement
leg clearance test passes
emergency stop method exists
```

MicroBot Round V0 can be considered safety-demo-ready when:

```text
self-check passes
tilt stop passes
obstacle stop passes
safe mode works
safety events are logged
small movement is bounded
```

MicroBot Round V0 can be considered integrated-demo-ready when:

```text
hello_microbot.py completes
session log is generated
camera snapshot is saved
one safe action is selected
safety layer approves or blocks action correctly
final report is generated
demo repeats successfully at least three times
```

---

## 76. Immediate Testing Priorities

The immediate testing priorities are:

```text
1. Repository structure test.
2. Documentation completeness test.
3. Voltage measurement test.
4. Controller power-on test.
5. Python environment test.
6. LED ring test.
7. IMU detection test.
8. Camera capture test.
9. Servo bus scan test.
10. Safe servo nudge test.
```

The first hardware milestone should be:

```text
LED ring works and a session log can be created.
```

The first movement milestone should be:

```text
Both servos can be detected, nudged slightly and returned to neutral without resetting the controller.
```

The first safety milestone should be:

```text
Movement is blocked when the robot is tilted or when an obstacle is too close.
```

The first integrated demo milestone should be:

```text
MicroBot Round V0 runs hello_microbot.py, performs self-check, reads sensors, executes one safe action or blocks it, saves evidence and generates a final report.
```

---

## 77. Final Test Plan Statement

MicroBot Round V0 must be tested as a real robotic prototype.

The project should not move from idea to full autonomy in one jump. It must progress through clear validation stages:

```text
documentation
power
controller
sensors
servos
mechanics
safety
logging
autonomy
integrated demo
evidence
```

A successful test plan does not only prove that the robot can move.

It proves that the robot can move safely, stop correctly, report its state and provide evidence of what happened.

That is the correct validation path for MicroBot Round V0.
