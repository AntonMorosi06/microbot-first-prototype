# Build Plan

## 1. Purpose of This Document

This document defines the build plan for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The goal of this build is to transform the MicroBot concept into a real, testable and documented robot that can power on, check its own subsystems, read sensors, move slowly, react to unsafe conditions, save logs and present itself as a working prototype.

MicroBot Round V0 is not intended to be the final MicroBot system. It is the first physical foundation. Its purpose is to prove that a small rounded robot can be assembled, powered, tested, controlled and documented in a technically credible way.

The build plan follows a progressive strategy:

1. Prepare the repository and documentation.
2. Select and document the hardware.
3. Assemble and test each electronic subsystem separately.
4. Build the rounded physical body.
5. Integrate the electronics inside the body.
6. Validate safe movement.
7. Implement self-check and logging.
8. Implement the first autonomous decision cycle.
9. Record evidence and prepare a public demo.

The project must not skip steps. A small validated prototype is more valuable than a complex robot that cannot be tested safely.

---

## 2. Build Philosophy

MicroBot Round V0 follows a safety-first and evidence-first build strategy.

The robot must be developed like a real engineering prototype, not like a random collection of parts. Every phase must produce a clear result, a test outcome and, when possible, evidence in the form of logs, photos, videos or reports.

The build philosophy is based on five principles.

### 2.1 Build One Layer at a Time

The robot must not be assembled completely before testing the individual parts.

The correct order is:

1. Test power.
2. Test controller.
3. Test LEDs.
4. Test IMU.
5. Test camera.
6. Test speaker and microphone.
7. Test distance sensor.
8. Test servos without load.
9. Test servos mounted on legs.
10. Test full robot movement.

This avoids the worst problem in robotics: not knowing which subsystem is failing.

### 2.2 Do Not Move Before Safety Exists

Servo movement must not be tested aggressively before the safety limits are defined.

Before meaningful movement, the project must define:

* Servo neutral positions.
* Servo safe range.
* Maximum movement amplitude.
* Maximum movement speed.
* Emergency stop behavior.
* Tilt threshold.
* Obstacle threshold.
* Battery or power instability behavior.
* Safe mode behavior.

### 2.3 Keep V0 Mechanically Simple

The first robot does not need a perfect shell or final miniaturization.

The first mechanical version must be:

* Printable.
* Openable.
* Strong enough for bench testing.
* Large enough to contain components.
* Simple enough to modify.
* Safe enough to move slowly.

A functional rough body is better than a beautiful body that cannot be repaired.

### 2.4 Every Demo Must Produce Evidence

Each integrated test should create evidence.

Evidence may include:

* Session logs.
* Sensor readings.
* Camera frames.
* Photos of the physical build.
* Video clips.
* Final reports.
* Build notes.
* Failure notes.

If a feature works but no evidence exists, it should not be considered fully validated.

### 2.5 Honest Status Labels

Every phase must use realistic status labels.

The project uses the following vocabulary:

* **planned**: described but not implemented.
* **prepared**: structure or documentation exists.
* **mocked**: simulated or placeholder behavior.
* **validated-offline**: tested without real robot hardware.
* **bench-tested**: tested on physical components outside the complete robot.
* **hardware-validated**: tested on the assembled robot.
* **integrated**: connected with other subsystems.
* **demo-ready**: safe, repeatable and suitable for public demonstration.

---

## 3. Target V0 Demonstration

The first complete demonstration of MicroBot Round V0 should show the robot performing a controlled startup and safety-aware behavior sequence.

The target demo is:

1. MicroBot powers on.
2. The LED ring performs a boot animation.
3. The robot speaks an initial phrase.
4. The robot creates a new session log.
5. The robot runs a self-check.
6. The robot reads IMU orientation.
7. The robot captures an initial camera frame.
8. The robot reads obstacle distance.
9. The robot checks servo availability.
10. The robot moves the legs slowly and safely.
11. The robot stops if tilted.
12. The robot stops if lifted.
13. The robot stops if an obstacle is too close.
14. The robot chooses one safe action from a limited action set.
15. The robot saves action results to the session log.
16. The robot generates a final session report.
17. The robot announces that the autonomous safety demo is complete.

The final demo phrase should be:

```text id="yl2sel"
MicroBot Round V0. Autonomous safety demo completed.
```

This demonstration is intentionally limited. Its value is that it is real, safe, repeatable and documentable.

---

## 4. Build Phases Overview

The build is divided into ten major phases.

```text id="9zg21n"
Phase 0  - Repository and documentation baseline
Phase 1  - Hardware selection and procurement
Phase 2  - Power system preparation
Phase 3  - Controller setup
Phase 4  - Sensor bring-up
Phase 5  - Actuator bring-up
Phase 6  - Mechanical body build
Phase 7  - Internal integration
Phase 8  - Safety and self-check
Phase 9  - First autonomous demo
Phase 10 - Evidence, documentation and release preparation
```

Each phase has a goal, required files, build actions, validation criteria and output evidence.

---

## 5. Phase 0 — Repository and Documentation Baseline

### 5.1 Goal

Create the repository structure and prepare the first documentation baseline before hardware implementation begins.

This phase ensures that the project is understandable from the beginning.

### 5.2 Required Repository Files

The repository should contain:

```text id="4ogqne"
README.md
CHANGELOG.md
LICENSE.md
.gitignore

docs/
hardware/
mechanical/
setup/
autonomy/
dashboard/
simulation/
demos/
evidence/
logs/
references/
```

### 5.3 Required Documentation Files

The first documentation files are:

```text id="mqeook"
docs/architecture.md
docs/current_status.md
docs/build_plan.md
docs/test_plan.md
docs/safety.md
docs/limitations.md
docs/demo_script.md
docs/portfolio_note.md
```

### 5.4 Build Actions

Actions:

1. Create the repository structure.
2. Create empty placeholder files.
3. Write `README.md`.
4. Write `docs/architecture.md`.
5. Write `docs/current_status.md`.
6. Write `docs/build_plan.md`.
7. Define status vocabulary.
8. Define the first target demo.
9. Commit the documentation baseline.

### 5.5 Validation Criteria

This phase is complete when:

* The repository structure exists.
* The main documentation files exist.
* The project goal is clearly described.
* The current status is not exaggerated.
* The first demo target is defined.
* The repository can be opened by another person and understood.

### 5.6 Expected Status

At the end of this phase:

```text id="5tkz1p"
Repository: prepared
Documentation: prepared
Hardware: planned
Software: planned
Mechanical body: planned
Autonomy: planned
Dashboard: planned
```

---

## 6. Phase 1 — Hardware Selection and Procurement

### 6.1 Goal

Select the first hardware components and document them clearly before assembly.

The hardware should support the first demo without unnecessary complexity.

### 6.2 Required Components

The first build should include:

* Main controller.
* MicroSD card.
* Power system.
* Battery.
* Power switch.
* LED ring.
* Two serial bus servos.
* IMU.
* Camera.
* Speaker.
* Microphone.
* Distance sensor.
* Wires and connectors.
* Mounting material.
* 3D printed body parts.
* Basic tools.

### 6.3 Recommended Main Controller

The recommended controller for V0 is:

```text id="ifti3h"
Raspberry Pi Zero 2 W
```

Reason:

* Small form factor.
* Linux support.
* Python support.
* Camera support.
* Audio support.
* Wi-Fi support.
* Suitable for dashboard and logging.
* Enough computing power for V0 behavior.

### 6.4 Recommended Actuators

The recommended actuator type is:

```text id="om8f3y"
Two small serial bus servos with position feedback
```

Reason:

* Better feedback than simple PWM servos.
* Better for robotic experiments.
* Supports bus communication.
* Allows position reading.
* Allows safer movement validation.

### 6.5 Recommended Sensors

The first sensor set should include:

* IMU for tilt and stability.
* Camera for snapshots and simple perception.
* Distance sensor for obstacle detection.
* Microphone for simple audio input or future wake detection.
* Battery or power monitoring if possible.

### 6.6 Documentation Files to Update

Update:

```text id="m621tx"
hardware/BOM.md
hardware/wiring.md
hardware/pinout.md
hardware/power_budget.md
hardware/assembly_notes.md
```

### 6.7 Validation Criteria

This phase is complete when:

* Every selected component is listed in `hardware/BOM.md`.
* The role of each component is clear.
* The voltage requirement of each component is documented.
* The pinout plan is documented.
* The expected power budget is estimated.
* Missing components are clearly marked.

### 6.8 Expected Status

At the end of this phase:

```text id="uy5f7y"
Hardware selection: prepared
BOM: prepared
Wiring plan: prepared
Power budget: prepared
Physical assembly: planned
```

---

## 7. Phase 2 — Power System Preparation

### 7.1 Goal

Prepare a safe and stable power system before connecting expensive electronics or moving parts.

The power system is one of the highest-risk parts of the robot.

### 7.2 Power Requirements

The power system must provide:

* Stable 5 V for the controller.
* Stable servo power.
* Common ground.
* Battery charging path.
* Power switch.
* Protection where possible.
* Enough current for servo peaks.
* Voltage stability during movement.

### 7.3 Build Actions

Actions:

1. Prepare battery or bench supply.
2. Prepare charging module if using battery.
3. Prepare boost converter or regulator.
4. Measure output voltage with a multimeter.
5. Adjust voltage before connecting the controller.
6. Add main switch.
7. Add capacitor near servo power input.
8. Verify common ground.
9. Test power without servos moving.
10. Document wiring.

### 7.4 Critical Safety Rules

Do not connect the controller before measuring voltage.

Do not connect servos before confirming power stability.

Do not move servos from the same weak rail without checking voltage drop.

Do not leave battery-powered electronics unattended during early tests.

Do not charge damaged batteries.

### 7.5 Validation Criteria

This phase is complete when:

* Output voltage is measured and documented.
* Controller can power on safely.
* Servo rail voltage is measured.
* Common ground is confirmed.
* Switch works.
* No component overheats during idle.
* The power system is documented in `hardware/power_budget.md`.

### 7.6 Expected Status

At the end of this phase:

```text id="mtespw"
Power system: bench-tested
Controller power: bench-tested
Servo power: prepared or bench-tested
Battery operation: prepared
```

---

## 8. Phase 3 — Controller Setup

### 8.1 Goal

Set up the main controller operating system, Python environment and base project files.

### 8.2 Build Actions

Actions:

1. Install operating system on microSD.
2. Enable SSH if needed.
3. Connect to Wi-Fi.
4. Update packages.
5. Enable required interfaces.
6. Create project folder on the controller.
7. Copy or clone the repository.
8. Create Python virtual environment.
9. Install requirements.
10. Run a basic Python startup test.

### 8.3 Required Interfaces

Depending on selected hardware, enable:

* I2C.
* Serial UART.
* Camera interface.
* Audio output.
* Audio input.
* GPIO access.

### 8.4 Required Files

Populate:

```text id="0tzxm8"
setup/requirements.txt
setup/microbot/config.py
setup/microbot/pins.py
```

### 8.5 Validation Criteria

This phase is complete when:

* The controller boots.
* The repository exists on the controller.
* Python runs correctly.
* Required Python packages install.
* Interfaces are enabled.
* A simple startup script can print robot version and configuration.

### 8.6 Expected Status

At the end of this phase:

```text id="vvxfbw"
Controller setup: bench-tested
Python environment: bench-tested
Repository on controller: prepared
Hardware interfaces: prepared
```

---

## 9. Phase 4 — Sensor Bring-Up

### 9.1 Goal

Test every sensor and feedback component individually before full robot integration.

### 9.2 Components to Test

Components:

* LED ring.
* IMU.
* Camera.
* Speaker.
* Microphone.
* Distance sensor.
* Battery or power monitor if available.

### 9.3 Testing Order

Recommended order:

1. LED ring.
2. IMU.
3. Camera.
4. Speaker.
5. Microphone.
6. Distance sensor.
7. Battery or CPU temperature monitoring.

### 9.4 Required Scripts

Populate and test:

```text id="lgjf7x"
setup/scripts/test_leds.py
setup/scripts/test_imu.py
setup/scripts/test_camera.py
setup/scripts/test_audio.py
setup/scripts/test_distance.py
setup/scripts/test_battery.py
```

### 9.5 Required Driver Modules

Populate:

```text id="y3dhs9"
setup/microbot/leds.py
setup/microbot/imu.py
setup/microbot/camera.py
setup/microbot/audio.py
setup/microbot/distance.py
setup/microbot/battery.py
```

### 9.6 Validation Criteria

This phase is complete when:

* LED ring can display at least three colors.
* IMU returns readable acceleration data.
* IMU tilt changes when the body is tilted.
* Camera captures and saves a frame.
* Speaker can play a phrase or tone.
* Microphone can record or measure input level.
* Distance sensor returns a reasonable distance.
* Sensor failures produce clear error messages.
* Test results are documented.

### 9.7 Evidence to Save

Save:

* Screenshot or terminal output of each successful test.
* At least one camera frame.
* Photo of wiring.
* Notes about failures.
* Notes about pin changes.

### 9.8 Expected Status

At the end of this phase:

```text id="ryxbla"
LED: bench-tested
IMU: bench-tested
Camera: bench-tested
Audio output: bench-tested
Microphone: bench-tested or prepared
Distance sensor: bench-tested
Battery monitoring: prepared or mocked
```

---

## 10. Phase 5 — Actuator Bring-Up

### 10.1 Goal

Test the servos safely before attaching them to the robot legs.

Actuators are risky because they can draw high current, move unexpectedly or damage the mechanism.

### 10.2 Build Actions

Actions:

1. Connect one servo only.
2. Confirm voltage.
3. Confirm ground.
4. Run servo scan.
5. Read servo ID.
6. Read current position.
7. Enable torque briefly.
8. Move only a very small amount.
9. Return to neutral.
10. Disable torque.
11. Repeat for second servo.
12. Test both servos together without legs.
13. Mount servos mechanically.
14. Repeat safe nudge after mounting.

### 10.3 Required Scripts

Populate and test:

```text id="o4d88h"
setup/scripts/scan_servos.py
setup/scripts/test_servos_safe.py
```

### 10.4 Required Driver Module

Populate:

```text id="kisv7f"
setup/microbot/servos.py
```

### 10.5 Servo Safety Rules

All servo movements must be:

* Small.
* Slow.
* Bounded.
* Reversible.
* Logged.
* Blockable by safety layer.

The first servo movement must not be a walking gait.

The first movement must be a small nudge around the current position.

### 10.6 Validation Criteria

This phase is complete when:

* Servo bus works.
* Both servo IDs are detected.
* Current positions can be read.
* Each servo can move slightly and return.
* Torque can be disabled.
* Movement does not reset the controller.
* Power does not drop dangerously during movement.
* No servo overheats.
* Movement range is documented.

### 10.7 Evidence to Save

Save:

* Terminal output of servo scan.
* Notes about servo IDs.
* Notes about neutral position.
* Notes about safe range.
* Short video of safe nudge.
* Voltage readings during movement if possible.

### 10.8 Expected Status

At the end of this phase:

```text id="4186iv"
Servo bus: bench-tested
Servo scan: bench-tested
Safe servo nudge: bench-tested
Leg movement: prepared
Walking behavior: planned
```

---

## 11. Phase 6 — Mechanical Body Build

### 11.1 Goal

Create and assemble the rounded physical body.

The body must support the electronics and movement system while remaining easy to open and modify.

### 11.2 Mechanical Components

Mechanical components:

* Rounded top shell.
* Bottom base shell.
* Internal mounting area.
* Left leg.
* Right leg.
* Rounded feet.
* Camera opening.
* LED visibility area.
* Speaker opening.
* Sensor opening.
* Power switch access.
* Charging access.
* Cable routing.

### 11.3 Build Actions

Actions:

1. Review design requirements.
2. Choose first printable shell.
3. Print body parts.
4. Clean supports and edges.
5. Check component fit.
6. Check servo mounting.
7. Check leg clearance.
8. Check cable routing.
9. Check shell access.
10. Assemble body without electronics first.
11. Mount electronics temporarily.
12. Adjust design notes.
13. Document mechanical issues.

### 11.4 Required Files

Update:

```text id="bg5wml"
mechanical/README.md
mechanical/print_notes.md
mechanical/design_requirements.md
```

### 11.5 Mechanical Validation Criteria

This phase is complete when:

* Body can be assembled.
* Shell can be opened.
* Controller fits.
* Battery fits.
* Servo mounting is stable.
* Legs move without colliding with shell.
* Camera has a clear opening.
* Wires can be routed without being crushed.
* Robot can stand on the surface.
* Robot can be handled safely.

### 11.6 Evidence to Save

Save:

* Photos of printed parts.
* Photos of assembly.
* Notes about print settings.
* Notes about fit issues.
* Notes about design changes.
* Short video of manual leg movement.

### 11.7 Expected Status

At the end of this phase:

```text id="45ilxf"
Mechanical body: bench-tested
Shell: bench-tested
Legs: bench-tested
Internal mounting: prepared
Full assembled robot: prepared
```

---

## 12. Phase 7 — Internal Integration

### 12.1 Goal

Install the tested electronics into the mechanical body and verify that the robot still works when assembled.

This phase connects the physical shell with the electronics.

### 12.2 Build Actions

Actions:

1. Mount controller.
2. Mount battery.
3. Mount switch.
4. Mount power module.
5. Mount LED ring.
6. Mount camera.
7. Mount IMU.
8. Mount speaker.
9. Mount microphone.
10. Mount distance sensor.
11. Mount servos.
12. Route cables.
13. Close shell partially.
14. Run sensor tests again.
15. Run servo scan again.
16. Check heat and voltage.
17. Close shell fully if safe.
18. Run self-check.

### 12.3 Cable Management Rules

Cables must not:

* Block the legs.
* Touch moving parts.
* Pull on connectors.
* Press directly against the camera.
* Press against the battery.
* Short exposed pins.
* Prevent the shell from closing.

### 12.4 Validation Criteria

This phase is complete when:

* All major electronics are inside or attached to the body.
* Sensor tests still work.
* Servo tests still work.
* The robot can stand.
* The robot can be powered safely.
* The shell can close.
* No cable interferes with movement.
* The robot can be carried without loose parts falling out.

### 12.5 Evidence to Save

Save:

* Internal wiring photo.
* Final assembled photo.
* Terminal output of self-check.
* Notes about mounting decisions.
* Notes about unstable or temporary mounting.

### 12.6 Expected Status

At the end of this phase:

```text id="09om3m"
Physical integration: bench-tested
Internal wiring: bench-tested
Assembled robot: bench-tested
Full movement: prepared
```

---

## 13. Phase 8 — Safety and Self-Check

### 13.1 Goal

Implement and validate a safety layer before running autonomous movement.

The robot must be able to refuse unsafe actions.

### 13.2 Required Files

Populate:

```text id="2ddow5"
setup/microbot/safety.py
setup/microbot/logger.py
setup/scripts/self_check.py
```

### 13.3 Self-Check Requirements

`self_check.py` must check:

* Log write access.
* LED status.
* Speaker status.
* IMU status.
* Camera status.
* Distance sensor status.
* Servo bus status.
* Battery or power status if available.
* Robot stability.
* Obstacle clearance.

### 13.4 Safety Conditions

Movement must be blocked if:

* Tilt threshold is exceeded.
* Robot appears lifted or unstable.
* Obstacle is too close.
* Servo bus is unavailable.
* Battery is too low.
* CPU temperature is too high.
* Previous movement failed repeatedly.
* Emergency stop is active.
* System state is unknown.

### 13.5 Safe Mode Behavior

When safe mode activates:

* Movement stops.
* Servo torque is disabled or reduced if appropriate.
* LED turns red or pulses red.
* The reason is logged.
* Optional speech announces safe mode.
* Autonomy pauses.
* Manual reset may be required.

### 13.6 Validation Criteria

This phase is complete when:

* Self-check runs from start to finish.
* Failed components are reported clearly.
* Movement is blocked when the robot is tilted.
* Movement is blocked when obstacle is close.
* Movement is blocked when servo bus fails.
* Safety events are logged.
* Safe mode can be triggered intentionally.
* Safe mode can be cleared only under safe conditions.

### 13.7 Evidence to Save

Save:

* Successful self-check output.
* Failed self-check output.
* Safe mode log.
* Tilt test result.
* Obstacle test result.
* Short video of safety stop.

### 13.8 Expected Status

At the end of this phase:

```text id="6e0b9h"
Self-check: bench-tested
Safety layer: bench-tested
Safe mode: bench-tested
Autonomous movement: prepared
```

---

## 14. Phase 9 — First Autonomous Demo

### 14.1 Goal

Implement the first limited autonomous behavior.

The robot should read sensors, evaluate safety and choose one action from a small safe action set.

### 14.2 Required Files

Populate:

```text id="s1zfaj"
autonomy/state_machine.py
autonomy/behaviors.py
autonomy/action_selector.py
autonomy/action_safety_layer.py
autonomy/memory_log.py
setup/scripts/hello_microbot.py
```

### 14.3 Allowed V0 Actions

The allowed V0 action set is:

```text id="caufkt"
STOP
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
```

No raw servo command should be selected by autonomy.

### 14.4 Decision Rules

Initial decision logic:

* If unsafe, choose `STOP`.
* If tilted, enter `SAFE_MODE`.
* If obstacle is close, choose `TURN_LEFT_SMALL` or `TURN_RIGHT_SMALL`.
* If stable and clear, choose `MOVE_FORWARD_SMALL`.
* If last movement failed, reduce movement amplitude.
* If repeated movements fail, enter `SAFE_MODE`.
* If power is low, stop and report.

### 14.5 Demo Flow

The first autonomous demo flow is:

1. Create session log.
2. Run boot LED animation.
3. Speak startup phrase.
4. Run self-check.
5. Read sensors.
6. Capture camera frame.
7. Evaluate safety.
8. Select one safe action.
9. Execute action if allowed.
10. Read sensors again.
11. Compare before and after state.
12. Save movement result.
13. Generate final report.
14. Announce completion.

### 14.6 Validation Criteria

This phase is complete when:

* Robot can start the demo.
* Robot can run self-check.
* Robot can read sensors.
* Robot can select one action.
* Robot can execute only safe actions.
* Robot stops when unsafe.
* Robot logs every decision.
* Robot generates a final report.
* Demo can be repeated at least three times.

### 14.7 Evidence to Save

Save:

* Video of full demo.
* Session log.
* Final report.
* Camera snapshots.
* Photo of setup.
* Notes about failures.
* Updated README demo section.

### 14.8 Expected Status

At the end of this phase:

```text id="qmz5ld"
First autonomous demo: hardware-validated
Safe action selection: hardware-validated
Movement logging: hardware-validated
Demo repeatability: bench-tested or demo-ready
```

---

## 15. Phase 10 — Evidence, Documentation and Release Preparation

### 15.1 Goal

Prepare the project for public presentation, portfolio use and future development.

This phase turns the build into a documented technical artifact.

### 15.2 Required Updates

Update:

```text id="s5943d"
README.md
CHANGELOG.md
docs/current_status.md
docs/test_plan.md
docs/safety.md
docs/limitations.md
docs/demo_script.md
docs/portfolio_note.md
hardware/BOM.md
hardware/wiring.md
hardware/pinout.md
hardware/power_budget.md
mechanical/print_notes.md
evidence/README.md
```

### 15.3 Evidence Package

The evidence package should include:

* At least one full demo video.
* At least one internal wiring photo.
* At least one assembled robot photo.
* At least one camera snapshot from the robot.
* At least one successful session log.
* At least one final session report.
* Notes about failed tests.
* Notes about limitations.

### 15.4 Release Criteria

A V0 demo can be considered public-demo-ready only when:

* The robot can run without uncontrolled movement.
* The safety layer works.
* Logs are generated.
* The demo can be repeated.
* Documentation explains the real status.
* Limitations are clearly stated.
* No private credentials or sensitive files are included.
* The repository does not claim more than has been validated.

### 15.5 Expected Status

At the end of this phase:

```text id="7upftr"
Repository: portfolio-ready
Documentation: portfolio-ready
First demo: demo-ready
Hardware: hardware-validated
Autonomy: limited but validated
Safety: hardware-validated
```

---

## 16. Build Checklist

### 16.1 Documentation Checklist

* [ ] Repository structure created.
* [ ] `README.md` written.
* [ ] `docs/architecture.md` written.
* [ ] `docs/build_plan.md` written.
* [ ] `docs/current_status.md` written.
* [ ] `docs/safety.md` written.
* [ ] `docs/test_plan.md` written.
* [ ] `docs/limitations.md` written.
* [ ] `docs/demo_script.md` written.
* [ ] `docs/portfolio_note.md` written.

### 16.2 Hardware Checklist

* [ ] Main controller selected.
* [ ] Power module selected.
* [ ] Battery selected.
* [ ] Switch selected.
* [ ] LED ring selected.
* [ ] IMU selected.
* [ ] Camera selected.
* [ ] Speaker selected.
* [ ] Microphone selected.
* [ ] Distance sensor selected.
* [ ] Servos selected.
* [ ] Wiring documented.
* [ ] Power budget estimated.

### 16.3 Mechanical Checklist

* [ ] Body design selected.
* [ ] Shell requirements written.
* [ ] Leg requirements written.
* [ ] First parts printed.
* [ ] Fit checked.
* [ ] Servo mounting checked.
* [ ] Camera opening checked.
* [ ] Cable routing checked.
* [ ] Assembly photographed.

### 16.4 Software Checklist

* [ ] Python environment prepared.
* [ ] Requirements file written.
* [ ] Config module created.
* [ ] Pin module created.
* [ ] LED module created.
* [ ] IMU module created.
* [ ] Camera module created.
* [ ] Audio module created.
* [ ] Distance module created.
* [ ] Servo module created.
* [ ] Logger module created.
* [ ] Safety module created.

### 16.5 Test Checklist

* [ ] LED test passed.
* [ ] IMU test passed.
* [ ] Camera test passed.
* [ ] Audio test passed.
* [ ] Distance test passed.
* [ ] Servo scan passed.
* [ ] Safe servo nudge passed.
* [ ] Self-check passed.
* [ ] Safe mode tested.
* [ ] Tilt stop tested.
* [ ] Obstacle stop tested.
* [ ] Hello MicroBot demo tested.

### 16.6 Evidence Checklist

* [ ] Photos saved.
* [ ] Videos saved.
* [ ] Logs saved.
* [ ] Reports saved.
* [ ] Failed tests documented.
* [ ] Current status updated.
* [ ] README updated.
* [ ] Changelog updated.

---

## 17. Risk Management

### 17.1 Electrical Risks

Main risks:

* Overvoltage to controller.
* Servo current spikes.
* Battery damage.
* Short circuit.
* Weak ground connection.
* Unstable power rail.

Mitigation:

* Measure voltage before connection.
* Use common ground.
* Use capacitor near servo rail.
* Test one component at a time.
* Avoid unattended battery charging.
* Document wiring carefully.

### 17.2 Mechanical Risks

Main risks:

* Legs collide with shell.
* Servo mount is weak.
* Shell cannot close.
* Wires interfere with movement.
* Robot tips over.
* Feet have poor traction.

Mitigation:

* Test leg movement manually.
* Keep shell accessible.
* Use temporary mounting in V0.
* Record fit issues.
* Iterate mechanical design.
* Keep movement slow.

### 17.3 Software Risks

Main risks:

* Raw movement commands bypass safety.
* Script crashes during movement.
* Sensor failure not handled.
* Logs not saved.
* Autonomy selects unsafe actions.
* Dashboard command bypasses safety.

Mitigation:

* Centralize safety layer.
* Use safe movement wrappers.
* Handle exceptions.
* Log all actions.
* Keep action set small.
* Never allow direct raw servo control from autonomy.

### 17.4 Demonstration Risks

Main risks:

* Robot fails during demo.
* Battery too low.
* Wi-Fi unavailable.
* Camera fails.
* Servo bus fails.
* Movement unstable.

Mitigation:

* Prepare manual mode.
* Prepare fallback demo.
* Record evidence before public presentation.
* Keep movement small.
* Test demo multiple times.
* Have safe shutdown procedure.

---

## 18. Definition of Done for MicroBot Round V0

MicroBot Round V0 is considered complete only when the following conditions are met:

* The robot powers on safely.
* The LED ring works.
* The robot can speak a phrase or play audio.
* The IMU works.
* The camera captures a frame.
* The distance sensor detects obstacles.
* Servo scan works.
* Safe servo movement works.
* Self-check works.
* Safety layer blocks unsafe movement.
* Tilt stop works.
* Obstacle stop works.
* A limited autonomous action is selected.
* A movement attempt is logged.
* A final session report is generated.
* The demo is repeatable.
* Documentation is updated.
* Evidence is saved.

If any critical condition is missing, the project should not be marked as demo-ready.

---

## 19. Immediate Next Steps

The immediate next steps are:

1. Complete `hardware/BOM.md`.
2. Complete `hardware/wiring.md`.
3. Complete `hardware/pinout.md`.
4. Complete `docs/safety.md`.
5. Complete `docs/test_plan.md`.
6. Populate `setup/requirements.txt`.
7. Implement `setup/microbot/config.py`.
8. Implement `setup/microbot/pins.py`.
9. Implement `setup/scripts/test_leds.py`.
10. Implement `setup/scripts/self_check.py`.

The first real technical milestone is not movement.

The first real technical milestone is:

```text id="co25d6"
MicroBot powers on, runs a self-check, shows LED state, reads at least one sensor and writes a session log.
```

Only after that should servo movement be tested.

---

## 20. Final Build Statement

MicroBot Round V0 must be built as a real engineering prototype.

The goal is not to impress through exaggerated claims. The goal is to impress through a working physical system that is small, documented, safe, inspectable and expandable.

A successful first build is a robot that can wake up, check itself, sense the environment, move carefully, stop when unsafe and save evidence.

That is the foundation for future MicroBot versions.
