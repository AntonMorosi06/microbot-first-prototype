# Architecture

## 1. Purpose of This Document

This document defines the architecture of **MicroBot Round V0**, the first physical bench prototype of a small rounded autonomous robot.

MicroBot Round V0 is not designed to claim full artificial intelligence, artificial consciousness, or advanced swarm behavior in its first version. Its purpose is more concrete and technically defensible: to create a real robotic platform that can power on, check its own subsystems, read sensors, move slowly, react to unsafe conditions, save evidence, and demonstrate a first layer of autonomous behavior.

The architecture is organized to keep the project clear, testable and expandable. Every subsystem is separated into layers so that hardware, drivers, safety, movement, perception, autonomy, dashboard control, logging and simulation can evolve without becoming a confused single script.

The first target is a stable physical robot that can perform the following demonstration:

* Power on from battery or bench supply.
* Run a visible LED boot sequence.
* Speak a short startup phrase.
* Run a self-check of the main subsystems.
* Read IMU orientation.
* Capture a camera frame.
* Read obstacle distance.
* Move the legs slowly and safely.
* Stop immediately if tilted, lifted, blocked or unstable.
* Choose between a limited set of safe movements.
* Save a structured session log.
* Present itself as MicroBot Round V0.

This is the architectural foundation for later versions involving stronger autonomy, external dashboard control, richer perception, machine learning, drone-observer integration, docking behavior, multi-node communication and the broader MicroBot ecosystem.

---

## 2. Design Philosophy

MicroBot Round V0 follows a simple principle: **build the smallest real robot that can prove the architecture physically**.

The goal is not to make the final MicroBot immediately. The goal is to build a physical platform that can be tested, documented, filmed, improved and extended.

The project is based on seven design principles.

### 2.1 Real Before Complex

A simple robot that actually powers on, moves, detects unsafe conditions and saves logs is more valuable than a large theoretical system that cannot be tested.

For this reason, V0 focuses on a bench prototype with limited movement, limited autonomy and strong safety boundaries.

### 2.2 Safety Before Autonomy

The robot must never execute uncontrolled motion. All movement commands must pass through a safety layer. The autonomy system is not allowed to directly control servos without validation.

The robot must stop if:

* The body is tilted beyond a safe threshold.
* The robot is lifted from the surface.
* An obstacle is too close.
* The battery is below a safe operating level.
* A servo does not respond.
* A movement produces instability.
* The system enters an unknown or invalid state.

### 2.3 Small Actions, Clear Feedback

The robot should not begin with aggressive walking. V0 movement must be based on small, slow, measurable actions:

* Small leg nudge.
* Return to neutral.
* Small left turn.
* Small right turn.
* Small forward attempt.
* Stop.

Every action must produce feedback through logs, LED state, optional voice output and sensor readings.

### 2.4 State-Based Intelligence

The first version of MicroBot intelligence is a state machine, not a free-form AI agent.

The robot does not “understand everything.” Instead, it evaluates a limited internal state and selects a safe action from a small list.

This is technically stronger than pretending to have general intelligence. The system can later connect to an LLM or learning policy, but V0 must remain deterministic, inspectable and safe.

### 2.5 Evidence-Oriented Development

Every important demo must produce evidence.

Evidence includes:

* Session logs.
* Sensor readings.
* Camera snapshots.
* Safety events.
* Movement attempts.
* Movement outcomes.
* Final session report.
* Photos and videos stored in the `evidence/` folder.

The project must be demonstrable from both the physical robot and the repository.

### 2.6 Modular Expansion

Each subsystem must be replaceable.

For example:

* The first distance sensor may be replaced by a better ToF sensor.
* The Raspberry Pi camera may be replaced by another camera module.
* A simple state machine may later be replaced by a learned policy.
* A local dashboard may later connect to a larger MicroBot telemetry system.
* Manual control may later be extended with gesture control, drone observation or multi-robot coordination.

### 2.7 Honest Status Vocabulary

Every feature must be described using realistic status labels.

The project uses the following vocabulary:

* **planned**: documented idea, not implemented yet.
* **prepared**: folder structure or file exists, but implementation is incomplete.
* **mocked**: simulated or placeholder behavior.
* **validated-offline**: tested locally without real robot hardware.
* **bench-tested**: tested on physical bench hardware.
* **hardware-validated**: tested on the assembled robot.
* **integrated**: connected with other subsystems.
* **demo-ready**: safe, repeatable and suitable for public demonstration.

---

## 3. High-Level System Overview

MicroBot Round V0 is divided into eight main layers:

1. Physical body.
2. Hardware electronics.
3. Low-level hardware drivers.
4. Safety layer.
5. Behavior layer.
6. Autonomy layer.
7. Dashboard and control layer.
8. Logging, evidence and simulation layer.

The architecture can be summarized as follows:

```text
User / Demo Operator
        |
        v
Dashboard / Manual Controls / Demo Script
        |
        v
Autonomy Layer
        |
        v
Action Safety Layer
        |
        v
Hardware Drivers
        |
        v
Physical Hardware
        |
        v
Sensors and Feedback
        |
        v
Logger / Dashboard / Autonomy State
```

No high-level decision is allowed to bypass the safety layer.

The autonomy system can propose an action, but the safety layer decides whether that action is allowed.

---

## 4. Physical Architecture

The physical body is the visible and mechanical foundation of the robot.

MicroBot Round V0 is designed as a small rounded robot with a compact body, internal electronics and two rounded legs. The shape should feel like a small autonomous creature, but the internal structure must remain practical for testing and repair.

### 4.1 Main Physical Components

The first physical prototype should include:

* Rounded upper shell.
* Lower base shell.
* Internal mounting area.
* Two side-mounted legs.
* Rounded or rocker-style feet.
* Camera opening.
* LED ring opening or visible LED window.
* Speaker opening.
* Cable routing area.
* Battery compartment.
* Access area for power switch and charging.
* Optional mounting area for distance sensor.

### 4.2 Shell Requirements

The shell must be:

* Small enough for a bench prototype.
* Large enough to contain the electronics safely.
* Openable for debugging.
* Printable with common 3D printers.
* Strong enough to survive repeated handling.
* Designed with simple tolerances.
* Not dependent on perfect miniaturization in V0.

The first shell does not need to be final or beautiful. It must be functional, accessible and repeatable.

### 4.3 Leg Requirements

The legs should be simple and robust.

The first version should avoid complex knee or ankle mechanisms. Instead, it should use two small servo-driven rounded legs or rocker-style feet.

The leg system should support:

* Small forward attempts.
* Small turning movements.
* Slow test movements.
* Return-to-neutral movement.
* Safe stopping.
* Mechanical tolerance for imperfect surfaces.

### 4.4 Mechanical Status

The mechanical layer starts as **prepared** until the robot is printed, assembled and physically tested.

A mechanical component becomes **bench-tested** only after it has been printed and manually checked.

A mechanical component becomes **hardware-validated** only after it works correctly on the assembled robot during movement tests.

---

## 5. Hardware Architecture

The hardware layer contains the electronic components needed for sensing, movement, feedback, power and control.

The first target is not a custom PCB. The first target is a working prototype using development boards and modules.

### 5.1 Main Controller

The main controller is responsible for:

* Running the Python software.
* Reading sensors.
* Controlling LEDs.
* Playing audio.
* Capturing camera frames.
* Communicating with servos.
* Running the safety layer.
* Saving logs.
* Serving the dashboard if enabled.

Possible controller:

* Raspberry Pi Zero 2 W.

Alternative future controllers may include:

* Raspberry Pi 5.
* ESP32-S3.
* Raspberry Pi Zero 2 W plus ESP32 co-controller.
* Custom PCB.

For V0, the architecture assumes a Raspberry Pi-class board because it simplifies camera, audio, Python and local dashboard development.

### 5.2 Actuation

The movement system should use two small servos.

Preferred servo type:

* Serial bus servo with position feedback.

The servo layer should support:

* Servo discovery.
* Servo ID scan.
* Torque enable/disable.
* Read current position.
* Read load or feedback if available.
* Move to target position.
* Clamp target inside safe range.
* Move both servos together.
* Return to neutral.
* Stop or disable torque during safe mode.

The first movement demo must use very small movements.

### 5.3 Sensors

The first sensor set should include:

* IMU for orientation and tilt detection.
* Camera for visual snapshots and basic perception.
* Distance sensor for obstacle detection.
* Microphone for basic audio input or future wake detection.
* Optional battery measurement.
* Optional CPU temperature or internal temperature monitoring.

The IMU is required for safety.

The distance sensor is strongly recommended because it makes obstacle detection much easier and more reliable than camera-only perception in V0.

### 5.4 Feedback Components

The robot should communicate its state through:

* LED ring.
* Speaker.
* Dashboard.
* Logs.

The LED ring is especially important because it gives immediate visual feedback during demonstrations.

Recommended LED states:

* White: boot or self-check.
* Blue: idle.
* Green: system OK.
* Yellow: warning or obstacle.
* Red: error or safe mode.
* Purple: decision or autonomy cycle.
* Cyan: listening or perception mode.
* Orange: movement blocked.

### 5.5 Power System

The power system must be treated carefully.

The architecture should support:

* Battery input.
* Charging module.
* Voltage boost or regulation.
* Stable 5 V rail for controller.
* Servo power rail.
* Common ground.
* Main switch.
* Fuse or protection where possible.
* Large capacitor near servo power input.
* Battery-low detection if available.

The robot must not move if the power level is unstable.

If servo movement causes voltage drops, the movement must be reduced or blocked.

### 5.6 Hardware Documentation Files

The hardware layer is documented in:

* `hardware/BOM.md`
* `hardware/wiring.md`
* `hardware/pinout.md`
* `hardware/power_budget.md`
* `hardware/assembly_notes.md`

These files must be updated whenever hardware changes.

---

## 6. Software Architecture

The software layer is organized into multiple folders to keep hardware tests, reusable modules, autonomy logic and dashboard code separated.

The main software areas are:

```text
setup/
autonomy/
dashboard/
simulation/
logs/
evidence/
```

### 6.1 Setup Package

The `setup/microbot/` package contains reusable low-level modules.

Expected modules:

```text
setup/microbot/
├── __init__.py
├── config.py
├── pins.py
├── servos.py
├── leds.py
├── imu.py
├── camera.py
├── audio.py
├── distance.py
├── battery.py
├── logger.py
└── safety.py
```

Each file has a specific responsibility.

### 6.2 Configuration Module

`config.py` stores general system configuration.

It should define:

* Robot name.
* Software version.
* Log folder.
* Evidence folder.
* Demo mode settings.
* Safety thresholds.
* Movement amplitude.
* Movement speed.
* Enabled or disabled subsystems.

No secret key or credential should be stored in this file.

### 6.3 Pin Mapping Module

`pins.py` stores hardware-specific pin definitions and addresses.

It should include:

* Serial port for servos.
* Servo baudrate.
* Servo IDs.
* LED GPIO pin.
* IMU I2C address.
* Distance sensor address or trigger/echo pins.
* Audio device names if needed.
* Camera settings if needed.

All hardware mapping should be centralized here so that the rest of the code does not contain scattered pin numbers.

### 6.4 Servo Module

`servos.py` controls the leg servos.

It should provide:

* Servo scan.
* Position read.
* Safe move.
* Neutral position.
* Small nudge.
* Turn left.
* Turn right.
* Small forward movement.
* Torque off.
* Emergency stop.

The servo module must not expose dangerous raw movement as the normal interface.

Raw low-level functions may exist internally, but public functions should be safe by default.

### 6.5 LED Module

`leds.py` controls the robot LED ring.

It should provide:

* Boot animation.
* Idle color.
* Error color.
* Warning color.
* Thinking animation.
* Movement animation.
* Safe mode animation.
* Shutdown animation.

The LED system is part of the user interface and should reflect real robot state.

### 6.6 IMU Module

`imu.py` reads orientation and motion data.

It should provide:

* Accelerometer readings.
* Gyroscope readings.
* Estimated tilt.
* Stability check.
* Lift detection if possible.
* Fall or sudden motion detection if possible.

The safety layer depends heavily on IMU data.

### 6.7 Camera Module

`camera.py` captures image frames.

It should provide:

* Single frame capture.
* Save image to evidence folder.
* Return image metadata.
* Basic brightness analysis.
* Optional simple color analysis.
* Optional face or motion detection in future versions.

V0 does not require advanced computer vision.

### 6.8 Audio Module

`audio.py` manages speech and microphone behavior.

It should provide:

* Speak text.
* Play simple tone or sound.
* Record short audio sample.
* Estimate microphone level.
* Optional wake sound detection in future versions.

Speech must be short and functional.

### 6.9 Distance Module

`distance.py` reads obstacle distance.

It should provide:

* Distance reading in centimeters.
* Obstacle threshold check.
* Sensor availability check.
* Invalid reading handling.

If the sensor fails, the robot should not continue moving forward blindly.

### 6.10 Battery Module

`battery.py` monitors power status if hardware support exists.

It should provide:

* Battery voltage if available.
* Low battery warning.
* Critical battery stop condition.
* CPU temperature fallback if battery measurement is not available.

If battery monitoring is not implemented yet, the file should clearly return a placeholder status and be marked as prepared or mocked.

### 6.11 Logger Module

`logger.py` creates structured logs for every session.

It should provide:

* Session ID creation.
* Event logging.
* Sensor logging.
* Action logging.
* Safety event logging.
* Final report generation.
* JSON or CSV output.

Logging is part of the core architecture, not an optional feature.

### 6.12 Safety Module

`safety.py` evaluates whether an action is allowed.

It should check:

* Tilt status.
* Lift status.
* Obstacle distance.
* Servo availability.
* Battery state.
* CPU temperature.
* Last movement result.
* Emergency stop flag.
* Manual stop flag.

The safety module returns either:

* Action allowed.
* Action blocked with reason.
* Safe mode required.

---

## 7. Script Architecture

The `setup/scripts/` folder contains executable scripts for testing and demonstration.

Expected scripts:

```text
setup/scripts/
├── scan_servos.py
├── test_servos_safe.py
├── test_leds.py
├── test_imu.py
├── test_camera.py
├── test_audio.py
├── test_distance.py
├── test_battery.py
├── self_check.py
└── hello_microbot.py
```

### 7.1 Hardware Test Scripts

Each hardware component must have its own test script.

This avoids debugging everything at once.

The correct testing order is:

1. LED test.
2. IMU test.
3. Camera test.
4. Distance sensor test.
5. Audio test.
6. Servo scan.
7. Safe servo nudge.
8. Self-check.
9. Hello MicroBot demo.

### 7.2 Self-Check Script

`self_check.py` runs a complete system check.

It should test:

* LED availability.
* Speaker availability.
* Camera availability.
* IMU availability.
* Distance sensor availability.
* Servo bus availability.
* Battery or power status.
* Log folder write access.

It should produce:

* Console output.
* LED feedback.
* Optional spoken output.
* Session log entry.
* Final status: OK, WARNING or FAILED.

### 7.3 Hello MicroBot Demo

`hello_microbot.py` is the first integrated demo.

It should:

1. Create a new session log.
2. Run boot LED animation.
3. Speak startup phrase.
4. Run self-check.
5. Read IMU.
6. Capture camera frame.
7. Read distance sensor.
8. Run safe servo nudge.
9. Choose one safe action.
10. Save final session report.
11. Present itself as MicroBot Round V0.

This script is the first public proof that the robot exists as an integrated system.

---

## 8. Safety Architecture

Safety is a mandatory layer between autonomy and hardware.

The robot must never execute a movement just because a high-level module requested it.

### 8.1 Safety Inputs

The safety layer receives:

* Requested action.
* Current robot state.
* IMU readings.
* Distance readings.
* Battery status.
* Servo status.
* Last action result.
* Manual emergency stop.
* Internal error flags.

### 8.2 Safety Outputs

The safety layer returns:

* `ALLOW`
* `BLOCK`
* `SAFE_MODE`

If blocked, it must return a reason.

Example reasons:

* `tilt_threshold_exceeded`
* `obstacle_too_close`
* `battery_low`
* `servo_not_responding`
* `movement_failed_recently`
* `manual_stop_active`
* `unknown_state`

### 8.3 Safe Mode

Safe mode is the protective state of the robot.

When safe mode is active:

* Movement is stopped.
* Servo torque is reduced or disabled when appropriate.
* LED state becomes red.
* A message is written to the session log.
* Optional speech announces the safety reason.
* Autonomy is paused.
* Manual reset may be required.

Safe mode is not a failure of the project. It is proof that the robot can protect itself.

### 8.4 Movement Boundaries

All movement must be bounded by:

* Maximum servo range.
* Maximum speed.
* Maximum action duration.
* Maximum movement amplitude.
* Maximum number of repeated attempts.
* Minimum delay between movements.
* Stability check before and after movement.

No movement should be infinite, blocking or uncontrolled.

---

## 9. Behavior Architecture

The behavior layer defines named actions that the robot can perform.

V0 behaviors should remain simple.

Recommended behaviors:

* `IDLE`
* `BOOT_ANIMATION`
* `SELF_CHECK`
* `SPEAK_STATUS`
* `CAPTURE_FRAME`
* `READ_SENSORS`
* `MOVE_FORWARD_SMALL`
* `TURN_LEFT_SMALL`
* `TURN_RIGHT_SMALL`
* `STOP`
* `SAFE_MODE`
* `SHUTDOWN`

Each behavior must be small and testable.

A behavior is not allowed to directly ignore safety constraints.

### 9.1 Action Set

The initial autonomous action set should include only:

* `STOP`
* `MOVE_FORWARD_SMALL`
* `TURN_LEFT_SMALL`
* `TURN_RIGHT_SMALL`

This keeps autonomy safe and understandable.

Future versions may add:

* `LOOK_AROUND`
* `APPROACH_LIGHT`
* `AVOID_DARK_AREA`
* `FOLLOW_OBJECT`
* `RETURN_TO_DOCK`
* `RESPOND_TO_GESTURE`
* `INTERACT_WITH_DRONE_OBSERVER`

---

## 10. Autonomy Architecture

The autonomy layer is responsible for deciding what the robot should do next.

In V0, autonomy should be a deterministic state machine.

### 10.1 State Machine

Possible states:

* `BOOT`
* `SELF_CHECK`
* `IDLE`
* `PERCEPTION`
* `DECISION`
* `MOVEMENT`
* `SAFE_MODE`
* `ERROR`
* `SHUTDOWN`

### 10.2 State Flow

Typical flow:

```text
BOOT
  -> SELF_CHECK
  -> IDLE
  -> PERCEPTION
  -> DECISION
  -> SAFETY_CHECK
  -> MOVEMENT
  -> PERCEPTION
  -> DECISION
```

If unsafe:

```text
ANY_STATE
  -> SAFE_MODE
```

If critical failure:

```text
ANY_STATE
  -> ERROR
  -> SHUTDOWN
```

### 10.3 Decision Logic

The first decision logic can be rule-based.

Example:

* If tilted, stop.
* If obstacle is close, turn left or right.
* If stable and clear, move forward small.
* If last movement failed, reduce amplitude.
* If repeated failures occur, enter safe mode.
* If battery is low, stop and report.

This is enough for a first autonomous demonstration.

### 10.4 Future AI Agent

A future LLM or AI agent may suggest actions, but it must only choose from safe predefined actions.

The AI agent must not send raw servo positions.

Allowed AI output example:

```text
TURN_LEFT_SMALL
```

Disallowed AI output example:

```text
move left servo to 983 and right servo to 112 at full speed
```

The safety layer remains mandatory even when AI is added.

---

## 11. Dashboard Architecture

The dashboard is the human control and observation interface.

It should allow the operator to see robot status and trigger safe commands.

### 11.1 Dashboard Responsibilities

The dashboard should display:

* Robot status.
* Current state.
* Last action.
* Last safety event.
* IMU orientation.
* Obstacle distance.
* Battery or power status.
* Camera snapshot.
* Servo status.
* Log session ID.

The dashboard should provide buttons for:

* Start demo.
* Stop.
* Safe mode.
* Take photo.
* Run self-check.
* Move forward small.
* Turn left small.
* Turn right small.
* Return to idle.

### 11.2 Manual Mode

Manual mode allows the user to request safe actions from the dashboard.

Manual mode still passes through the safety layer.

### 11.3 Autonomous Mode

Autonomous mode allows the robot to select actions by itself.

Autonomous mode must be easy to stop.

A visible emergency stop control must always be available.

### 11.4 Dashboard Status

The dashboard starts as **prepared**.

It becomes **validated-offline** when it can run locally and display mock robot data.

It becomes **bench-tested** when it displays real sensor data from hardware.

It becomes **integrated** when it can control the assembled robot safely.

---

## 12. Logging and Evidence Architecture

Logging is central to MicroBot Round V0.

Every demo must leave evidence.

### 12.1 Session Logs

Each session should create a unique folder or file.

Example:

```text
logs/session_2026-06-13_001.json
```

The log should include:

* Session ID.
* Timestamp.
* Robot version.
* Hardware status.
* Sensor readings.
* Selected actions.
* Safety decisions.
* Movement results.
* Errors.
* Final status.

### 12.2 Evidence Files

The `evidence/` folder stores material that can be used for documentation, portfolio and public demonstration.

Expected folders:

```text
evidence/
├── photos/
├── videos/
└── reports/
```

Examples:

```text
evidence/photos/boot_frame_001.jpg
evidence/photos/obstacle_detected_001.jpg
evidence/reports/session_report_001.md
```

### 12.3 Final Session Report

At the end of a demo, the robot should generate a report.

Example content:

```text
MicroBot Round V0 Session Report

Boot: OK
LED: OK
Speaker: OK
Camera: OK
IMU: OK
Distance Sensor: OK
Servo Bus: OK
Movements Attempted: 3
Movements Successful: 2
Movements Blocked: 1
Safety Events: obstacle_too_close
Final State: SAFE_IDLE
```

This report is important because it transforms the robot from a visual demo into a documented technical system.

---

## 13. Simulation Architecture

The simulation layer provides a simplified model of the robot.

The goal is not photorealism. The goal is to represent the body, joints, legs, basic contact behavior and sensor-like data in a simplified physics environment.

### 13.1 Simulation Goals

The simulation should help with:

* Understanding leg geometry.
* Testing movement patterns.
* Estimating stability.
* Testing basic action sequences.
* Preparing future control policies.
* Comparing simulated behavior with real robot behavior.

### 13.2 Simulation Boundaries

The simulation does not replace hardware testing.

A movement that works in simulation is not automatically hardware-validated.

Simulation status should be described as:

* mocked
* validated-offline
* simulation-only

It becomes useful evidence only when compared with physical test results.

### 13.3 Simulation Files

The simulation layer is stored in:

```text
simulation/
├── README.md
├── microbot_round_body.xml
└── notes.md
```

Future simulation files may include:

* MuJoCo XML.
* URDF.
* Blender model.
* Python controller.
* Recorded movement traces.
* Comparison reports.

---

## 14. Data Flow

The standard data flow is:

```text
Sensors
  -> Driver Modules
  -> Robot State
  -> Autonomy Layer
  -> Proposed Action
  -> Safety Layer
  -> Approved Action
  -> Hardware Driver
  -> Physical Movement
  -> Sensor Feedback
  -> Logger
  -> Dashboard
```

The safety layer is the gate between proposed action and physical movement.

The logger observes all major transitions.

The dashboard can observe and request actions, but not bypass safety.

---

## 15. First Integrated Demo Flow

The first integrated demo should follow this sequence:

1. Power on robot.
2. Start `hello_microbot.py`.
3. Create session log.
4. Run LED boot animation.
5. Speak startup phrase.
6. Run self-check.
7. Read IMU orientation.
8. Capture initial camera frame.
9. Read obstacle distance.
10. Check safety state.
11. Move left leg slightly.
12. Return left leg to neutral.
13. Move right leg slightly.
14. Return right leg to neutral.
15. Choose one safe action.
16. Execute action only if allowed.
17. Log result.
18. Generate final report.
19. Announce completion.
20. Return to idle or shutdown.

Expected final phrase:

```text
MicroBot Round V0. Autonomous safety demo completed.
```

---

## 16. Repository Architecture

The repository is organized as follows:

```text
microbot-round-v0/
├── README.md
├── CHANGELOG.md
├── LICENSE.md
├── .gitignore
│
├── docs/
│   ├── architecture.md
│   ├── current_status.md
│   ├── build_plan.md
│   ├── test_plan.md
│   ├── safety.md
│   ├── limitations.md
│   ├── demo_script.md
│   └── portfolio_note.md
│
├── hardware/
│   ├── BOM.md
│   ├── wiring.md
│   ├── pinout.md
│   ├── power_budget.md
│   └── assembly_notes.md
│
├── mechanical/
│   ├── README.md
│   ├── stl_reference/
│   ├── cad_custom/
│   ├── print_notes.md
│   └── design_requirements.md
│
├── setup/
│   ├── requirements.txt
│   ├── microbot/
│   └── scripts/
│
├── autonomy/
│   ├── README.md
│   ├── state_machine.py
│   ├── behaviors.py
│   ├── action_selector.py
│   ├── action_safety_layer.py
│   ├── memory_log.py
│   └── llm_agent_placeholder.py
│
├── dashboard/
│   ├── README.md
│   ├── app.py
│   ├── static/
│   └── templates/
│
├── simulation/
│   ├── README.md
│   ├── microbot_round_body.xml
│   └── notes.md
│
├── demos/
│   ├── README.md
│   ├── demo_sequence_v0.md
│   └── video_shot_list.md
│
├── evidence/
│   ├── README.md
│   ├── photos/
│   ├── videos/
│   └── reports/
│
├── logs/
│   └── .gitkeep
│
└── references/
    ├── README.md
    └── growbot_reference_notes.md
```

Each folder has a clear role.

No folder should become a random dump.

---

## 17. Current Architectural Status

The architecture is currently in the **prepared** stage.

The structure is ready to support:

* Hardware documentation.
* Mechanical design.
* Sensor test scripts.
* Servo test scripts.
* Safety logic.
* Basic autonomy.
* Dashboard integration.
* Simulation.
* Evidence collection.

The next step is to populate the documentation files and then implement the hardware bring-up scripts one by one.

---

## 18. Development Roadmap

### V0.1 — Repository and Documentation Baseline

Status target: prepared.

Goals:

* Create repository structure.
* Write architecture document.
* Write current status document.
* Write BOM.
* Write safety document.
* Write build plan.
* Write test plan.

### V0.2 — Hardware Bring-Up

Status target: bench-tested.

Goals:

* Test LED ring.
* Test IMU.
* Test camera.
* Test audio.
* Test distance sensor.
* Scan servos.
* Run safe servo nudge.

### V0.3 — Integrated Self-Check

Status target: bench-tested.

Goals:

* Implement `self_check.py`.
* Produce structured logs.
* Report subsystem status.
* Block movement if a critical subsystem fails.

### V0.4 — First Movement Demo

Status target: hardware-validated.

Goals:

* Move left leg safely.
* Move right leg safely.
* Return legs to neutral.
* Stop on tilt.
* Stop on obstacle.
* Save action results.

### V0.5 — First Autonomous Demo

Status target: demo-ready.

Goals:

* Select between three safe actions.
* Execute only approved actions.
* React to unsafe conditions.
* Generate session report.
* Record demo video.

### V0.6 — Dashboard Integration

Status target: integrated.

Goals:

* Display robot state.
* Display sensor values.
* Show last camera frame.
* Provide safe manual controls.
* Start/stop autonomous demo.

### V0.7 — Extended Perception

Status target: planned.

Goals:

* Basic object or face detection.
* Light-level behavior.
* Color response.
* Gesture placeholder.

### V0.8 — AI Agent Placeholder

Status target: planned / mocked.

Goals:

* Allow an LLM or simple agent to suggest actions.
* Restrict output to safe action names.
* Keep safety layer mandatory.
* Log every AI decision.

### V1.0 — Public Demonstration

Status target: demo-ready.

Goals:

* Repeatable demo.
* Clean documentation.
* Wiring documented.
* Logs and evidence included.
* Video demonstration published.
* Clear limitations stated.

---

## 19. Known Architectural Limitations

MicroBot Round V0 has intentional limitations.

It is not:

* A fully autonomous general-purpose robot.
* A complete humanoid or walking robot.
* A commercial product.
* A swarm robot yet.
* A proven AI learning platform yet.
* A fully miniaturized MicroBot module yet.
* A hardware-validated docking system yet.
* A drone-integrated robot yet.

It is:

* A first physical bench prototype.
* A rounded robot body experiment.
* A safe movement platform.
* A sensor and logging platform.
* A first autonomous behavior demonstrator.
* A foundation for later MicroBot development.

These limitations are not weaknesses. They make the project honest and technically credible.

---

## 20. Future Expansion Paths

MicroBot Round V0 can evolve into several directions.

### 20.1 Better Mechanical Design

Future versions may include:

* More rounded shell.
* Better internal mounting.
* Magnetic access panel.
* Improved leg mechanism.
* Better feet material.
* Charging contacts.
* Docking alignment geometry.

### 20.2 Better Electronics

Future versions may include:

* Dedicated power board.
* Separate servo power rail.
* Battery voltage monitoring.
* Custom PCB.
* Better camera.
* Better IMU.
* ToF sensor array.
* Thermal monitoring.

### 20.3 Better Autonomy

Future versions may include:

* Behavior memory.
* Local navigation.
* Learning from movement logs.
* Sim-to-real movement tuning.
* Basic reinforcement learning experiments.
* LLM-based action planning with strict safety boundaries.

### 20.4 MicroBot Ecosystem Integration

Future versions may connect to:

* MicroBot dashboard.
* MicroBot telemetry system.
* MicroBot simulation engine.
* Drone observer.
* Docking station.
* Multi-node MicroBot experiments.
* GitHub evidence pipeline.
* Portfolio website.

---

## 21. Final Architecture Statement

MicroBot Round V0 is a layered, safety-first robotic prototype.

Its purpose is to transform the MicroBot concept from a broad idea into a real physical system that can be powered, tested, observed, moved, stopped, logged and improved.

The robot does not need to be perfect in V0.

It needs to be real.

A successful V0 is a robot that can wake up, check itself, sense the environment, make a small safe decision, move carefully, stop when unsafe, save evidence and clearly communicate its state.

That is the foundation for every future MicroBot version.
