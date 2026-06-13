# Demo Script

## 1. Purpose of This Document

This document defines the official demonstration script for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this demo is to show a real, safe and technically defensible robotic system. The demo does not claim that MicroBot Round V0 has full artificial intelligence, full environmental understanding, advanced locomotion or completed swarm behavior.

The goal of the demo is to prove the first physical foundation:

* The robot can power on.
* The robot can run a visible boot sequence.
* The robot can communicate its state through LEDs and speech.
* The robot can read basic sensors.
* The robot can capture visual evidence.
* The robot can test its legs with safe movement.
* The robot can stop when unsafe.
* The robot can choose a limited action from a safe action set.
* The robot can save logs and evidence.
* The robot can present itself as a working MicroBot Round V0 prototype.

The demonstration must be repeatable, safe, documented and honest.

---

## 2. Demo Name

The official name of the first integrated demo is:

```text
MicroBot Round V0 — First Autonomous Safety Demo
```

Alternative short name:

```text
MicroBot Round V0 Awakening Demo
```

The name “Awakening Demo” can be used for video presentation, but the repository should use the more technical name “First Autonomous Safety Demo”.

---

## 3. Demo Objective

The objective of the demo is to show MicroBot Round V0 waking up, checking itself, sensing the environment, moving carefully, reacting to unsafe conditions and saving evidence.

The demo should communicate one clear idea:

```text
MicroBot Round V0 is not a final autonomous robot yet, but it is a real physical platform that can sense, react, move safely and document its own behavior.
```

The strongest part of the demo is not the size of the movement. The strongest part is the complete system loop:

```text
power -> self-check -> perception -> safety -> action -> feedback -> log -> report
```

This is the first proof that MicroBot can become a real robotic platform instead of remaining only a concept.

---

## 4. Demo Status

Current demo status:

```text
Demo concept: defined
Demo script: prepared
Hardware implementation: planned
Sensor implementation: planned
Servo implementation: planned
Safety implementation: planned
Logging implementation: planned
Autonomy implementation: planned
Video evidence: planned
```

This script describes the target demonstration. The demo becomes valid only after it has been implemented, tested and recorded on physical hardware.

---

## 5. Demo Scope

This demo includes:

* Boot animation.
* Startup voice phrase.
* Session log creation.
* System self-check.
* LED status feedback.
* IMU orientation reading.
* Camera frame capture.
* Distance or obstacle reading.
* Servo availability check.
* Safe leg nudge.
* Tilt safety stop.
* Obstacle safety stop.
* Limited autonomous action selection.
* Final session report.
* Final spoken presentation.

This demo does not include:

* Full walking.
* Full mapping.
* Full object recognition.
* Full AI learning.
* Swarm coordination.
* Drone observer integration.
* Magnetic docking.
* Charging station behavior.
* Advanced gesture control.
* Real-time language conversation.
* Reinforcement learning on the physical robot.

Those features belong to future versions.

---

## 6. Required Hardware for the Demo

The ideal demo setup includes:

```text
Main controller
LED ring
Speaker
IMU
Camera
Distance sensor
Two leg servos
Battery or stable bench power
Power switch
Rounded robot shell
Two rounded legs or rocker-style feet
MicroSD card
Wiring
Mounting material
```

The minimum acceptable demo setup is:

```text
Main controller
LED ring
IMU
Camera
Two servos
Stable power
Session logging
Safety logic
```

If the speaker is unavailable, the demo can still run with text output and LED feedback.

If the distance sensor is unavailable, obstacle detection must be clearly marked as mocked, simulated or not available.

---

## 7. Required Software for the Demo

Required scripts and modules:

```text
setup/scripts/hello_microbot.py
setup/scripts/self_check.py
setup/scripts/test_leds.py
setup/scripts/test_imu.py
setup/scripts/test_camera.py
setup/scripts/test_distance.py
setup/scripts/scan_servos.py
setup/scripts/test_servos_safe.py

setup/microbot/config.py
setup/microbot/pins.py
setup/microbot/leds.py
setup/microbot/imu.py
setup/microbot/camera.py
setup/microbot/audio.py
setup/microbot/distance.py
setup/microbot/servos.py
setup/microbot/logger.py
setup/microbot/safety.py

autonomy/state_machine.py
autonomy/behaviors.py
autonomy/action_selector.py
autonomy/action_safety_layer.py
autonomy/memory_log.py
```

The first public demo should be launched through:

```text
python setup/scripts/hello_microbot.py
```

If some hardware requires elevated permissions, the command may become:

```text
sudo python setup/scripts/hello_microbot.py
```

This must be documented clearly in the final README after real testing.

---

## 8. Safety Requirements Before Running the Demo

Before running the demo, the operator must verify:

* The power system is stable.
* The battery is not damaged.
* The output voltage has been measured.
* The robot is placed on a flat surface.
* The legs are not blocked.
* The shell does not interfere with movement.
* The wires are not touching moving parts.
* The servos have been tested with small movements.
* The IMU returns valid data.
* The emergency stop method is known.
* The first movement amplitude is small.
* The robot is not near table edges.
* The robot is not near fragile objects.
* The operator can physically stop the robot if needed.

The demo must not begin with aggressive movement.

The robot should start with a small nudge movement only.

---

## 9. Demo Environment

The first demo should be recorded in a controlled indoor environment.

Recommended environment:

* Clean desk or floor.
* Good lighting.
* Flat surface.
* No loose cables in front of the robot.
* No fragile objects nearby.
* Camera or phone positioned to capture the robot clearly.
* Laptop nearby showing terminal output or dashboard.
* Optional second camera angle for close-up.

Avoid:

* Table edges.
* Reflective surfaces.
* Dark environments.
* Crowded areas.
* Unstable surfaces.
* Long cables across the movement area.
* Testing near water, metal clutter or battery hazards.

---

## 10. Demo Pre-Flight Checklist

Before starting the demo, complete this checklist.

### 10.1 Physical Checklist

* [ ] Robot body is assembled.
* [ ] Shell is stable.
* [ ] Legs are attached.
* [ ] Legs can move freely.
* [ ] Camera opening is clear.
* [ ] LED ring is visible.
* [ ] Speaker opening is not blocked.
* [ ] Distance sensor is facing forward.
* [ ] Battery is secured.
* [ ] Cables are routed safely.
* [ ] Power switch is reachable.
* [ ] Robot is placed on a flat surface.

### 10.2 Electrical Checklist

* [ ] Power voltage measured.
* [ ] Controller powers on.
* [ ] Servo rail is stable.
* [ ] Common ground confirmed.
* [ ] No overheating during idle.
* [ ] Battery level acceptable.
* [ ] Charging circuit disconnected if not needed.
* [ ] No exposed short-circuit risk.
* [ ] Emergency power-off method available.

### 10.3 Software Checklist

* [ ] Repository is copied to the robot.
* [ ] Python environment is active.
* [ ] Requirements are installed.
* [ ] Pin configuration is correct.
* [ ] Log folder exists.
* [ ] Evidence folder exists.
* [ ] Camera permissions are correct.
* [ ] Serial port is configured.
* [ ] I2C is enabled.
* [ ] LED library works.
* [ ] Self-check script runs.

### 10.4 Demo Checklist

* [ ] Camera for recording is ready.
* [ ] Terminal or dashboard is visible.
* [ ] Robot is centered in the frame.
* [ ] Lighting is acceptable.
* [ ] Demo command is ready.
* [ ] Fallback plan is ready.
* [ ] Operator knows how to stop the robot.

---

## 11. Demo Sequence Overview

The full demo sequence is:

```text
1. Power on MicroBot.
2. Start demo script.
3. Create session log.
4. Run LED boot animation.
5. Speak startup phrase.
6. Run system self-check.
7. Read IMU orientation.
8. Capture camera frame.
9. Read obstacle distance.
10. Check servo bus.
11. Test safe leg movement.
12. Enter perception cycle.
13. Evaluate safety.
14. Select one safe action.
15. Execute action if allowed.
16. Stop if tilted or blocked.
17. Save movement result.
18. Generate final report.
19. Speak completion phrase.
20. Return to idle.
```

The expected behavior is not large movement. The expected behavior is controlled, safe, readable behavior.

---

## 12. Detailed Demo Script

### Step 1 — Power On

Operator action:

```text
Turn on MicroBot using the main power switch.
```

Expected robot behavior:

```text
Controller boots.
LED ring may remain off until software starts.
No servo movement occurs automatically.
```

Expected operator narration:

```text
This is MicroBot Round V0, the first rounded physical bench prototype of the MicroBot project. The goal of this demo is to show a real safety-aware robotic startup sequence.
```

Validation:

* Robot receives power.
* Controller boots.
* No uncontrolled motion occurs.

Evidence:

* Video of power-on.
* Optional photo of setup.

---

### Step 2 — Start Demo Script

Operator action:

```text
Run the demo script from terminal.
```

Expected command:

```text
python setup/scripts/hello_microbot.py
```

Expected robot behavior:

```text
The robot creates a new session log.
The robot initializes configuration.
The robot initializes LEDs if available.
The robot prepares self-check.
```

Expected terminal output:

```text
MicroBot Round V0
Session created: session_YYYY-MM-DD_HH-MM-SS
Boot sequence started.
```

Validation:

* Script starts.
* No import errors.
* Session log is created.

Evidence:

* Terminal output.
* Created log file.

---

### Step 3 — LED Boot Animation

Robot action:

```text
Run LED boot animation.
```

Expected LED behavior:

```text
White pulse.
Blue idle flash.
Green confirmation.
Purple thinking animation.
```

Alternative simple LED sequence:

```text
Red -> Green -> Blue -> White -> Idle Blue
```

Expected spoken phrase, if speaker is available:

```text
MicroBot Round V0 online. System check started.
```

Expected terminal output:

```text
LED check: OK
Startup phrase: OK
```

Validation:

* LED ring responds.
* Speaker works if available.
* If speaker fails, demo continues with warning.

Evidence:

* Video of LED sequence.
* Log event: `boot_led_animation_completed`.

---

### Step 4 — Session Log Initialization

Robot action:

```text
Create or open a structured session log.
```

Expected log fields:

```text
session_id
timestamp
robot_name
software_version
demo_name
initial_state
hardware_status
events
sensor_readings
actions
safety_events
final_status
```

Expected terminal output:

```text
Session log initialized.
```

Validation:

* Log file exists.
* Log file is writable.
* First event is saved.

Evidence:

* `logs/session_*.json`
* Optional final report.

---

### Step 5 — System Self-Check

Robot action:

```text
Run self-check of core subsystems.
```

Subsystems checked:

```text
LED ring
Speaker
Camera
IMU
Distance sensor
Servo bus
Battery or power status
Log folder
Evidence folder
```

Expected terminal output:

```text
Self-check started.
LED: OK
Speaker: OK or WARNING
Camera: OK
IMU: OK
Distance sensor: OK or WARNING
Servo bus: OK
Log write access: OK
Evidence folder: OK
Self-check result: OK
```

Expected LED behavior:

```text
White or purple during check.
Green if check passes.
Yellow if non-critical warning.
Red if critical failure.
```

Expected robot speech:

```text
System check complete.
```

Validation:

* All critical components report valid status.
* Non-critical failure does not crash the demo.
* Critical failure blocks movement.

Evidence:

* Log event: `self_check_completed`
* Terminal output.
* Optional final report entry.

---

### Step 6 — IMU Orientation Reading

Robot action:

```text
Read IMU orientation and stability status.
```

Expected output:

```text
IMU: OK
Tilt X: value
Tilt Y: value
Stable: true
```

Expected behavior:

```text
If stable, continue.
If tilted beyond threshold, block movement and enter safe mode.
```

Operator test option:

```text
Slightly tilt the robot to show that the system detects instability.
```

Expected safety behavior:

```text
Movement blocked.
LED turns red or yellow.
Safety event is logged.
```

Expected speech:

```text
Unstable orientation detected. Movement blocked.
```

Validation:

* IMU readings change when robot is tilted.
* Tilt threshold triggers safety block.
* Safety event is logged.

Evidence:

* Terminal output.
* Log event: `tilt_detected`.
* Optional video of tilt stop.

---

### Step 7 — Camera Frame Capture

Robot action:

```text
Capture an initial camera frame.
```

Expected output:

```text
Camera: OK
Frame saved: evidence/photos/boot_frame_001.jpg
```

Expected behavior:

```text
The robot captures a frame and saves it with a clear filename.
```

Recommended filename:

```text
evidence/photos/session_<id>_boot_frame.jpg
```

Validation:

* Image file exists.
* File size is greater than zero.
* Image can be opened after demo.

Evidence:

* Saved camera snapshot.
* Log event: `camera_frame_captured`.

---

### Step 8 — Distance or Obstacle Reading

Robot action:

```text
Read obstacle distance.
```

Expected output:

```text
Distance sensor: OK
Distance: value_cm
Obstacle: false
```

If obstacle is close:

```text
Obstacle: true
Forward movement blocked.
```

Expected LED behavior:

```text
Green if path is clear.
Yellow or orange if obstacle is detected.
```

Expected speech:

```text
Obstacle detected. Forward movement blocked.
```

Validation:

* Distance value changes when an object is placed in front.
* Obstacle threshold blocks forward movement.
* Safety event is logged.

Evidence:

* Log event: `obstacle_detected`.
* Optional camera frame: `obstacle_detected_001.jpg`.

---

### Step 9 — Servo Bus Check

Robot action:

```text
Scan or verify servo bus.
```

Expected output:

```text
Servo bus: OK
Left servo ID: detected
Right servo ID: detected
Servo positions: readable
```

Important rule:

```text
The servo bus check should not perform large movement.
```

Validation:

* Both servos are detected.
* Current positions can be read.
* Servo failures are reported clearly.
* Movement remains blocked if servo bus fails.

Evidence:

* Terminal output.
* Log event: `servo_bus_checked`.

---

### Step 10 — Safe Leg Nudge

Robot action:

```text
Move each leg slightly and return to neutral.
```

Expected behavior:

```text
Left leg moves slightly.
Left leg returns to neutral.
Right leg moves slightly.
Right leg returns to neutral.
Both servos remain inside safe range.
```

Expected output:

```text
Safe leg nudge started.
Left servo nudge: OK
Right servo nudge: OK
Neutral position restored.
```

Expected LED behavior:

```text
Purple during movement.
Green after successful movement.
```

Expected speech:

```text
Movement test complete.
```

Validation:

* Movement is small.
* Movement does not cause instability.
* Servos do not stall.
* Controller does not reset.
* Movement result is logged.

Evidence:

* Video of leg nudge.
* Log event: `safe_leg_nudge_completed`.

---

### Step 11 — Perception Cycle

Robot action:

```text
Read current sensor state.
```

Inputs:

```text
IMU stability
Obstacle distance
Last movement result
Servo status
Battery or power status
Camera snapshot status
```

Expected output:

```text
Perception cycle started.
Stable: true
Obstacle: false
Servo status: OK
Last movement: OK
```

Validation:

* Sensor state is collected.
* Missing non-critical sensor does not crash the demo.
* Missing critical sensor blocks movement if needed.

Evidence:

* Log event: `perception_cycle_completed`.

---

### Step 12 — Autonomous Action Selection

Robot action:

```text
Select one action from the safe V0 action set.
```

Allowed actions:

```text
STOP
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
```

Example decision rules:

```text
If unstable -> STOP
If obstacle close -> TURN_LEFT_SMALL or TURN_RIGHT_SMALL
If stable and clear -> MOVE_FORWARD_SMALL
If previous movement failed -> STOP or reduce movement amplitude
```

Expected output:

```text
Autonomous decision cycle started.
Selected action: MOVE_FORWARD_SMALL
Reason: stable_body_and_clear_path
```

Expected LED behavior:

```text
Purple while deciding.
Blue or green after decision.
```

Expected speech:

```text
Selecting safe movement.
```

Validation:

* Action is one of the allowed actions.
* Raw servo commands are not generated by autonomy.
* Safety layer checks selected action before execution.

Evidence:

* Log event: `action_selected`.
* Selected action and reason saved.

---

### Step 13 — Safety Validation Before Action

Robot action:

```text
Pass selected action through safety layer.
```

Expected output if safe:

```text
Safety check: ALLOW
Action approved: MOVE_FORWARD_SMALL
```

Expected output if unsafe:

```text
Safety check: BLOCK
Reason: obstacle_too_close
Action replaced with: STOP
```

Validation:

* Safety layer can allow, block or force safe mode.
* Blocked action is logged.
* Robot does not move if unsafe.

Evidence:

* Log event: `safety_check_completed`.

---

### Step 14 — Execute Safe Action

Robot action:

```text
Execute approved action.
```

Expected behavior:

```text
If MOVE_FORWARD_SMALL is approved, the robot attempts a very small forward motion.
If TURN_LEFT_SMALL is approved, the robot rotates slightly left.
If TURN_RIGHT_SMALL is approved, the robot rotates slightly right.
If STOP is selected, the robot remains still.
```

Expected output:

```text
Executing action: MOVE_FORWARD_SMALL
Action completed.
```

Validation:

* Action is small and controlled.
* Movement stays within safe limits.
* Robot does not fall.
* Robot logs result.

Evidence:

* Video of movement.
* Log event: `action_executed`.
* Movement result entry.

---

### Step 15 — Post-Movement Sensor Check

Robot action:

```text
Read sensors again after movement.
```

Expected output:

```text
Post-movement check started.
Stable: true
Obstacle: false
Movement result: successful
```

If unstable:

```text
Post-movement instability detected.
Entering safe mode.
```

Validation:

* The robot compares before and after state.
* Failed movement is detected.
* Safe mode is triggered if needed.

Evidence:

* Log event: `post_movement_check_completed`.
* Optional camera frame after movement.

---

### Step 16 — Safe Mode Demonstration

The demo may optionally include an intentional safety test.

Operator action:

```text
Tilt the robot slightly or place an object in front of it.
```

Expected robot behavior:

```text
Robot stops.
Movement is blocked.
LED turns red, yellow or orange.
Safety reason is logged.
```

Expected speech:

```text
Safe mode active.
```

Expected output:

```text
Safety event: tilt_threshold_exceeded
Movement blocked.
Safe mode active.
```

Validation:

* Safe mode triggers correctly.
* Robot does not continue moving.
* Safety event is saved.

Evidence:

* Video of safety stop.
* Log event: `safe_mode_triggered`.

---

### Step 17 — Final Report Generation

Robot action:

```text
Generate a final session report.
```

Expected report content:

```text
MicroBot Round V0 Session Report

Session ID: <id>
Demo: First Autonomous Safety Demo
Boot: OK
LED: OK
Speaker: OK or WARNING
Camera: OK
IMU: OK
Distance Sensor: OK or WARNING
Servo Bus: OK
Movements Attempted: <number>
Movements Successful: <number>
Movements Blocked: <number>
Safety Events: <list>
Final State: SAFE_IDLE
```

Expected file location:

```text
evidence/reports/session_<id>_report.md
```

Validation:

* Report is generated.
* Report matches log data.
* Final state is clear.

Evidence:

* Final report file.
* Session log file.

---

### Step 18 — Final Presentation Phrase

Robot action:

```text
Speak or print final status.
```

Expected phrase:

```text
MicroBot Round V0. Autonomous safety demo completed.
```

Alternative if safe mode was triggered:

```text
MicroBot Round V0. Demo completed with safety intervention.
```

Expected LED behavior:

```text
Green if successful.
Yellow if completed with warnings.
Red if ended in safe mode.
Blue if returned to idle.
```

Validation:

* Final phrase or terminal output occurs.
* Final LED state matches status.
* Demo ends without uncontrolled motion.

Evidence:

* Video clip.
* Final log entry.

---

## 13. Full Operator Narration Script

This is the narration that can be spoken during a recorded video.

```text
This is MicroBot Round V0, the first rounded physical bench prototype of the MicroBot project.

The goal of this version is not to claim full artificial intelligence, but to prove a real safety-aware robotic platform.

In this demo, MicroBot will power on, run a visible boot sequence, check its core subsystems, read its IMU, capture a camera frame, check for obstacles, verify the servo bus, move its legs slowly, select one limited safe action and save a session log.

The most important part of this demo is the safety layer. MicroBot is not allowed to move directly from a high-level command. Every action must pass through a safety check.

If the robot is tilted, blocked, unstable or unable to read a critical subsystem, movement is stopped.

Now I will start the first autonomous safety demo.

MicroBot is creating a new session log.

The LED ring shows the boot sequence.

The robot is now running its self-check.

The IMU is active and the robot is checking its orientation.

The camera captures an initial frame and saves it as evidence.

The distance sensor checks whether there is an obstacle in front of the robot.

The servo bus is checked before any movement.

Now MicroBot performs a very small safe leg movement. This is not full walking yet. It is a controlled hardware validation step.

The robot now enters a limited autonomous decision cycle. It can only choose between safe predefined actions: stop, move forward slightly, turn left slightly or turn right slightly.

The selected action is checked by the safety layer before execution.

If the action is safe, MicroBot executes it slowly. If the action is unsafe, the robot stops and logs the reason.

At the end of the demo, MicroBot generates a session report containing subsystem status, movement results, safety events and final state.

This is the first physical foundation for the larger MicroBot ecosystem: a small robot that can wake up, sense, move carefully, stop when unsafe and document what happened.
```

---

## 14. Short Video Narration Script

This shorter version can be used for a one-minute video.

```text
This is MicroBot Round V0, my first rounded physical bench prototype.

The goal of this demo is simple but important: the robot must wake up, check itself, read sensors, move safely and stop when something is wrong.

It starts with an LED boot sequence and a spoken startup phrase.

Then it creates a session log and checks the main subsystems: IMU, camera, distance sensor, servo bus, audio and logging.

Before moving, MicroBot verifies that its body is stable and that the path is clear.

The leg movement is intentionally small. This is not full walking yet. It is a safe hardware validation step.

After reading the environment, the robot chooses one action from a limited safe set: stop, move forward slightly, turn left slightly or turn right slightly.

Every action passes through the safety layer.

If the robot is tilted or blocked, it stops immediately and logs the reason.

At the end, it saves a final report.

This is MicroBot Round V0: a real first step toward a small autonomous robotic platform.
```

---

## 15. Terminal Demo Script

Expected terminal flow:

```text
$ python setup/scripts/hello_microbot.py

MicroBot Round V0
Demo: First Autonomous Safety Demo
Software version: 0.1.0

[BOOT] Creating session log...
[OK] Session created: session_2026-06-13_001

[BOOT] LED animation started...
[OK] LED ring ready

[AUDIO] Startup phrase...
[OK] Speech output ready

[SELF_CHECK] Running system check...
[OK] Log write access
[OK] Evidence folder
[OK] IMU detected
[OK] Camera available
[OK] Distance sensor ready
[OK] Servo bus available
[WARNING] Battery monitor not implemented
[OK] Self-check completed with warnings

[IMU] Reading orientation...
[OK] Stable orientation detected

[CAMERA] Capturing initial frame...
[OK] Saved evidence/photos/session_2026-06-13_001_boot_frame.jpg

[DISTANCE] Reading obstacle distance...
[OK] Distance: 42.5 cm
[OK] Path clear

[SERVO] Running safe leg nudge...
[OK] Left leg nudge completed
[OK] Right leg nudge completed
[OK] Neutral position restored

[AUTONOMY] Starting decision cycle...
[OK] Selected action: MOVE_FORWARD_SMALL
[OK] Reason: stable_body_and_clear_path

[SAFETY] Validating action...
[OK] Action approved

[ACTION] Executing MOVE_FORWARD_SMALL...
[OK] Action completed

[POST_CHECK] Reading sensors after movement...
[OK] Robot stable
[OK] Movement result: successful

[REPORT] Generating final session report...
[OK] Report saved: evidence/reports/session_2026-06-13_001_report.md

[DONE] MicroBot Round V0. Autonomous safety demo completed.
```

---

## 16. Demo Failure Cases

The demo must handle failures clearly.

### 16.1 Camera Failure

Expected behavior:

```text
Camera: FAILED
Warning saved to log.
Demo continues only if camera is not critical.
```

Robot phrase:

```text
Camera unavailable. Continuing in reduced mode.
```

### 16.2 IMU Failure

Expected behavior:

```text
IMU: FAILED
Movement blocked.
Demo stops before servo action.
```

Robot phrase:

```text
IMU unavailable. Movement blocked.
```

### 16.3 Servo Failure

Expected behavior:

```text
Servo bus: FAILED
Movement blocked.
Demo continues only as sensor demo.
```

Robot phrase:

```text
Servo bus unavailable. Movement disabled.
```

### 16.4 Obstacle Detected

Expected behavior:

```text
Obstacle too close.
Forward movement blocked.
Robot selects STOP or TURN action.
```

Robot phrase:

```text
Obstacle detected. Forward movement blocked.
```

### 16.5 Tilt Detected

Expected behavior:

```text
Tilt threshold exceeded.
Safe mode active.
Movement stopped.
```

Robot phrase:

```text
Unstable orientation detected. Safe mode active.
```

### 16.6 Power Warning

Expected behavior:

```text
Battery low or power unstable.
Movement blocked.
Demo ends safely.
```

Robot phrase:

```text
Power warning. Movement disabled.
```

---

## 17. Fallback Demo Modes

If the full demo is not ready, use one of these fallback modes.

### 17.1 Fallback Demo A — Sensor Demo

Use when servos are not ready.

Includes:

* LED boot.
* Speech.
* IMU reading.
* Camera frame.
* Distance reading.
* Session log.
* Final report.

Does not include:

* Leg movement.
* Autonomous action execution.

Claim:

```text
This is a sensor and self-check demo. Movement is disabled until servo validation is complete.
```

### 17.2 Fallback Demo B — Movement Demo

Use when camera or audio is not ready.

Includes:

* LED boot.
* IMU reading.
* Servo scan.
* Safe leg nudge.
* Tilt stop.
* Log.

Does not include:

* Camera snapshot.
* Speech.
* Advanced perception.

Claim:

```text
This is a safe movement validation demo. Some perception modules are not connected yet.
```

### 17.3 Fallback Demo C — Offline Simulation Demo

Use when hardware is not ready.

Includes:

* Mock sensor data.
* State machine.
* Action selection.
* Safety block.
* Mock log.
* Mock report.

Claim:

```text
This is an offline software simulation of the MicroBot Round V0 decision and safety flow. It is not hardware validation.
```

---

## 18. Demo Evidence Requirements

Every completed demo should save evidence.

Required evidence:

```text
logs/session_<id>.json
evidence/photos/session_<id>_boot_frame.jpg
evidence/reports/session_<id>_report.md
```

Recommended evidence:

```text
evidence/photos/session_<id>_setup.jpg
evidence/photos/session_<id>_internal_wiring.jpg
evidence/photos/session_<id>_obstacle_test.jpg
evidence/videos/session_<id>_full_demo.mp4
evidence/videos/session_<id>_tilt_stop.mp4
evidence/videos/session_<id>_safe_leg_nudge.mp4
```

The README should link to selected evidence after validation.

Large videos should not necessarily be committed directly to Git if they are too large. They can be linked from releases, external storage or portfolio pages.

---

## 19. Demo Success Criteria

The full demo is successful only if:

* Robot powers on safely.
* Demo script starts.
* Session log is created.
* LED boot sequence works.
* Self-check runs.
* IMU reading works.
* Camera frame is saved.
* Distance reading works or is clearly marked unavailable.
* Servo bus is detected.
* Safe leg nudge works.
* Safety layer validates movement.
* Robot stops on unsafe condition.
* One safe autonomous action is selected.
* Final report is generated.
* Demo ends without uncontrolled motion.
* Evidence is saved.

The demo is not successful if:

* Robot moves before safety check.
* Robot executes raw servo movement from autonomy.
* Robot falls because movement was too aggressive.
* Unsafe condition is ignored.
* Log is not generated.
* Final status is unclear.
* The repository claims more than the hardware proves.

---

## 20. Definition of Demo-Ready

The demo can be marked as **demo-ready** only after it has been successfully repeated at least three times.

Required repeated validation:

```text
Run 1: successful
Run 2: successful
Run 3: successful
```

Each run must produce:

```text
Session log
Final report
No uncontrolled movement
No critical safety failure
```

Optional but recommended:

```text
At least one recorded full demo video
At least one recorded safety stop video
At least one photo of the assembled robot
```

Until then, the demo status should remain:

```text
prepared
bench-tested
hardware-validated
```

depending on the real test level.

---

## 21. Public Demo Description

This text can be used in the repository or video description after real validation.

```text
MicroBot Round V0 is the first rounded physical bench prototype of the MicroBot project.

This demo shows the robot powering on, running a boot animation, checking its core subsystems, reading IMU orientation, capturing a camera frame, detecting obstacle status, verifying its servo bus, performing a small safe leg movement, selecting a limited autonomous action and generating a session report.

The robot does not claim full artificial intelligence or full autonomous navigation in this version. The purpose of V0 is to validate the first physical platform, safety layer, sensor loop, controlled movement and evidence logging system.
```

---

## 22. What Not to Claim

Do not claim:

```text
MicroBot fully understands its environment.
MicroBot can walk autonomously in any space.
MicroBot has complete AI learning.
MicroBot is swarm-ready.
MicroBot has solved autonomous robotics.
MicroBot can safely navigate real environments without supervision.
MicroBot has validated docking behavior.
MicroBot has validated drone integration.
```

Correct claims:

```text
MicroBot Round V0 can run a structured self-check.
MicroBot Round V0 can read basic sensors.
MicroBot Round V0 can perform limited safe movement.
MicroBot Round V0 can block movement under unsafe conditions.
MicroBot Round V0 can save logs and evidence.
MicroBot Round V0 is a first physical foundation for future autonomous behavior.
```

---

## 23. Final Demo Statement

The final message of the demo should be:

```text
MicroBot Round V0. Autonomous safety demo completed.
```

The final repository statement should be:

```text
This demo validates the first safety-aware startup, sensing, movement and evidence loop of MicroBot Round V0. It is a limited but real foundation for future MicroBot autonomy.
```

The most important result is not that MicroBot moves far.

The most important result is that MicroBot behaves like a controlled robotic system:

```text
It wakes up.
It checks itself.
It senses.
It decides within limits.
It moves carefully.
It stops when unsafe.
It saves evidence.
```

That is the first real MicroBot Round V0 demonstration.
