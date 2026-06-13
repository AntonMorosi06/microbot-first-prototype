# Safety

## 1. Purpose of This Document

This document defines the safety strategy for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

MicroBot Round V0 is a small robotics prototype, but it still contains moving parts, electrical power, battery components, sensors, software control and autonomous decision logic. For this reason, safety must be treated as a core architectural layer, not as an optional feature added at the end.

The purpose of this document is to define:

```text
electrical safety rules
battery safety rules
mechanical safety rules
servo movement limits
sensor-based safety checks
software safety boundaries
autonomy restrictions
safe mode behavior
emergency stop behavior
test procedures
demo safety requirements
evidence requirements
```

The safety system must ensure that MicroBot Round V0 can move only within controlled limits and must stop when unstable, blocked, tilted, lifted, underpowered or in an unknown state.

The central rule of the project is:

```text
No movement command is allowed to reach the physical servos without passing through the safety layer.
```

---

## 2. Safety Philosophy

MicroBot Round V0 follows a safety-first development approach.

The robot should be built as a controlled engineering prototype, not as an uncontrolled toy. Every physical movement must be small, bounded, reversible and logged. Every demo must be repeatable and supervised.

Safety is based on five main principles.

### 2.1 Small Movement First

The first movement must not be walking.

The first movement must be:

```text
small
slow
bounded
reversible
supervised
logged
```

The correct first actuator test is a safe servo nudge, not a full gait.

### 2.2 Sensors Before Autonomy

The robot must read its safety-relevant sensors before attempting autonomous movement.

At minimum, the robot should check:

```text
IMU stability
servo availability
obstacle distance if available
battery or power status if available
log write access
current system state
```

If a critical sensor is unavailable, movement must be blocked.

### 2.3 Safety Layer Before Behavior Layer

The behavior layer may request an action, but the safety layer must approve it.

Example:

```text
Autonomy selects: MOVE_FORWARD_SMALL
Safety checks: stable body, no obstacle, servo bus OK, power OK
Safety result: ALLOW
Servo movement: executed
```

If safety blocks the action:

```text
Autonomy selects: MOVE_FORWARD_SMALL
Safety checks: obstacle too close
Safety result: BLOCK
Servo movement: not executed
Robot action: STOP
```

### 2.4 Safe Failure

If the system does not know what is happening, the robot must stop.

Unknown state must never produce movement.

Correct behavior:

```text
unknown state -> stop
sensor failure -> stop or reduced mode
servo failure -> movement disabled
power instability -> movement disabled
tilt detected -> safe mode
```

### 2.5 Evidence for Safety Claims

A safety feature should not be considered validated until evidence exists.

Evidence may include:

```text
test output
session log
video
photo
final report
hardware note
failure note
```

If the repository claims that tilt stop works, there must be a log or video showing that tilt stop was tested.

---

## 3. Safety Scope

This document covers the safety requirements for the V0 prototype.

Included safety areas:

```text
power safety
battery safety
servo safety
movement safety
tilt detection
obstacle detection
mechanical safety
software safety
autonomy safety
dashboard safety
logging safety
demo safety
operator safety
```

Excluded from V0:

```text
certified product safety
industrial robot compliance
commercial safety certification
medical safety
outdoor autonomous navigation safety
multi-robot swarm safety
drone flight safety
magnetic docking safety certification
```

MicroBot Round V0 is a supervised bench prototype. It must not be operated as an unsupervised autonomous robot.

---

## 4. Global Safety Rule

The global safety rule is:

```text
If the robot is not clearly safe, it must not move.
```

This rule applies to all layers.

The robot must not move if:

```text
the IMU is unavailable
the robot is tilted beyond threshold
the robot appears lifted or unstable
an obstacle is too close
the servo bus is unavailable
a servo does not respond
the battery or power state is unsafe
the previous movement failed repeatedly
the emergency stop flag is active
the dashboard requested stop
the system is in an unknown state
the log system cannot record safety-critical events
```

Movement is allowed only when the system has enough information to make a safe decision.

---

## 5. Safety Architecture

The safety architecture sits between high-level commands and low-level hardware drivers.

```text
User / Dashboard / Autonomy
        |
        v
Requested Action
        |
        v
Safety Layer
        |
        +--> ALLOW -----> Hardware Driver -----> Physical Movement
        |
        +--> BLOCK -----> STOP / Warning / Log
        |
        +--> SAFE_MODE -> Stop Movement / LED Red / Log / Optional Speech
```

The safety layer must be used by:

```text
manual dashboard commands
autonomous action selection
demo scripts
test scripts that move servos
future AI agent suggestions
```

No module should bypass safety to move the robot during normal operation.

---

## 6. Safety States

MicroBot Round V0 should use explicit safety states.

Recommended safety states:

```text
SAFE_IDLE
SELF_CHECK
MOVEMENT_ALLOWED
MOVEMENT_BLOCKED
WARNING
SAFE_MODE
CRITICAL_ERROR
SHUTDOWN
```

### 6.1 SAFE_IDLE

The robot is powered, stable and not moving.

Allowed actions:

```text
self-check
read sensors
capture photo
speak status
safe movement request
shutdown
```

### 6.2 SELF_CHECK

The robot is checking its subsystems.

Allowed actions:

```text
read sensors
test LEDs
test camera
test audio
check servo bus without large movement
write logs
```

Movement should remain disabled until self-check is complete.

### 6.3 MOVEMENT_ALLOWED

The robot has passed safety checks and may execute a small approved action.

Movement is still limited by:

```text
servo range
speed limit
duration limit
amplitude limit
stability check
obstacle check
```

### 6.4 MOVEMENT_BLOCKED

The robot received a movement request, but safety blocked it.

The reason must be logged.

Example reasons:

```text
tilt_threshold_exceeded
obstacle_too_close
servo_bus_unavailable
battery_low
unknown_state
manual_stop_active
```

### 6.5 WARNING

A non-critical issue exists, but the robot may continue in reduced mode.

Examples:

```text
speaker unavailable
camera unavailable if not required for movement
battery monitor not implemented
microphone unavailable
dashboard disconnected
```

### 6.6 SAFE_MODE

Safe mode is active when the robot must stop physical movement.

In safe mode:

```text
movement is disabled
servo torque may be disabled or reduced
LED should indicate warning or error
reason is logged
autonomy is paused
manual reset may be required
```

### 6.7 CRITICAL_ERROR

Critical error means the robot cannot continue safely.

Examples:

```text
power instability detected
servo runaway risk
unhandled hardware failure
repeated safety failures
software exception during movement
```

The system should stop movement and require operator intervention.

### 6.8 SHUTDOWN

The robot enters shutdown when the demo ends, battery is low, or the operator stops the session.

Shutdown should:

```text
stop movement
return servos to neutral if safe
disable torque if appropriate
save final report
set LED final state
exit software cleanly
```

---

## 7. Safety Inputs

The safety layer should evaluate multiple inputs before allowing movement.

Required inputs:

```text
requested action
current robot state
IMU stability status
obstacle status
servo bus status
servo position status
battery or power status
last movement result
emergency stop flag
manual stop flag
system error flag
```

Optional future inputs:

```text
CPU temperature
internal temperature
motor load
camera-based obstacle confidence
foot contact detection
current sensor
charging dock status
external dashboard heartbeat
drone observer status
```

V0 can start with a limited input set, but the architecture must allow future expansion.

---

## 8. Safety Outputs

The safety layer must return a structured result.

Recommended safety result format:

```text
result: ALLOW | BLOCK | SAFE_MODE | CRITICAL_ERROR
reason: text code
message: human-readable explanation
recommended_action: STOP | SAFE_MODE | CONTINUE | SHUTDOWN
```

Example:

```text
result: BLOCK
reason: obstacle_too_close
message: Forward movement blocked because obstacle distance is below threshold.
recommended_action: STOP
```

Example:

```text
result: SAFE_MODE
reason: tilt_threshold_exceeded
message: Robot is tilted beyond safe operating range.
recommended_action: SAFE_MODE
```

---

## 9. Action Safety Rules

MicroBot Round V0 must use a limited action set.

Allowed V0 actions:

```text
STOP
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
TAKE_PHOTO
SPEAK_STATUS
RUN_SELF_CHECK
RETURN_TO_IDLE
SAFE_MODE
SHUTDOWN
```

Movement actions:

```text
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
```

Non-movement actions:

```text
STOP
TAKE_PHOTO
SPEAK_STATUS
RUN_SELF_CHECK
RETURN_TO_IDLE
SAFE_MODE
SHUTDOWN
```

The autonomy system and dashboard must not send raw servo target values as normal commands.

Disallowed normal commands:

```text
move left servo to arbitrary position
move right servo to arbitrary position
set maximum torque without safety check
run infinite movement loop
disable safety layer
ignore obstacle check
ignore tilt check
override safe mode
```

Raw servo commands may exist only in controlled low-level test scripts and must be clearly marked as hardware bring-up tools.

---

## 10. Servo Safety

Servos are one of the highest-risk components in MicroBot Round V0 because they can move unexpectedly, draw high current and damage mechanical parts.

### 10.1 Servo Movement Rules

Every servo movement must be:

```text
bounded
slow
short-duration
within safe range
logged
interruptible
approved by safety layer
```

### 10.2 Servo Range

The project must define:

```text
left_servo_min
left_servo_max
left_servo_neutral
right_servo_min
right_servo_max
right_servo_neutral
movement_step_small
movement_speed_safe
movement_timeout
```

Until real calibration is complete, conservative default values must be used.

### 10.3 First Servo Test

The first servo test must be:

```text
scan servo bus
read servo ID
read current position
enable torque briefly
move a very small amount
return to original position
disable torque
log result
```

The first servo test must not attempt walking.

### 10.4 Servo Failure Conditions

Movement must be blocked if:

```text
servo ID is not detected
servo position cannot be read
servo reports invalid position
servo does not reach expected position
servo stalls
servo overheats if temperature is available
servo load is too high if load feedback is available
servo rail voltage drops during movement
```

### 10.5 Servo Emergency Behavior

If servo behavior is unsafe:

```text
stop movement immediately
disable torque if appropriate
enter safe mode
log reason
notify through LED and terminal
require operator check
```

---

## 11. Movement Safety

Movement safety controls how the robot physically moves.

### 11.1 Movement Boundaries

Each movement must have:

```text
maximum amplitude
maximum speed
maximum duration
maximum repetitions
minimum delay between actions
pre-movement safety check
post-movement safety check
```

### 11.2 Movement Before Check Is Forbidden

The robot must not move before:

```text
self-check has completed
IMU status is valid
servo status is valid
movement range is known
obstacle status is acceptable
emergency stop is inactive
```

### 11.3 Post-Movement Check

After every movement, the robot must check:

```text
stability
tilt
obstacle distance
servo response
movement result
system errors
```

If instability appears after movement, the robot must enter safe mode or block further movement.

### 11.4 Repeated Failure Rule

If movement fails repeatedly, the robot must stop.

Example rule:

```text
if failed_movements >= 3:
    enter SAFE_MODE
```

The exact threshold can be adjusted, but repeated failure must never produce more aggressive movement.

---

## 12. Tilt and Stability Safety

The IMU is the main safety sensor for orientation and stability.

### 12.1 Tilt Detection

The safety layer should define tilt thresholds.

Example placeholders:

```text
safe_tilt_degrees = 15
warning_tilt_degrees = 20
critical_tilt_degrees = 30
```

These values must be calibrated on real hardware before final use.

### 12.2 Tilt Safety Rules

Movement must be blocked if:

```text
tilt exceeds safe threshold
tilt reading is invalid
IMU is not responding
robot is unstable after movement
robot appears to be falling
```

### 12.3 Lift Detection

If possible, the robot should detect being lifted.

Possible signals:

```text
abnormal acceleration
low contact stability
sudden orientation change
unexpected movement result
```

Lift detection may be unreliable in V0 and should be marked as planned or experimental until validated.

### 12.4 Tilt Stop Test

The tilt stop test should verify:

```text
robot is stable on flat surface
movement is allowed
operator tilts robot beyond threshold
movement is blocked
safe mode activates
event is logged
LED changes state
optional speech announces warning
```

---

## 13. Obstacle Safety

Obstacle detection prevents forward movement into nearby objects.

### 13.1 Distance Sensor Use

A forward-facing distance sensor is recommended for V0.

The distance sensor should provide:

```text
distance_cm
valid_reading
obstacle_detected
timestamp
```

### 13.2 Obstacle Thresholds

Example placeholder thresholds:

```text
warning_distance_cm = 25
stop_distance_cm = 15
critical_distance_cm = 8
```

These must be calibrated with the real sensor and real body.

### 13.3 Obstacle Safety Rules

Forward movement must be blocked if:

```text
distance is below stop threshold
distance reading is invalid and forward motion requires obstacle awareness
sensor is unavailable and no fallback mode is defined
```

If an obstacle is detected, allowed actions may include:

```text
STOP
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
SPEAK_STATUS
TAKE_PHOTO
```

Forward movement should not be allowed.

### 13.4 Obstacle Stop Test

The obstacle stop test should verify:

```text
robot reads clear distance
forward movement is allowed
object is placed in front of robot
distance falls below threshold
forward movement is blocked
event is logged
LED changes state
optional speech announces obstacle
```

---

## 14. Power and Battery Safety

Power instability can cause unpredictable behavior.

### 14.1 Power Safety Rules

The robot must not move if:

```text
controller voltage is unstable
battery is critically low
servo rail voltage drops under load
power monitor reports unsafe state
controller repeatedly resets
```

### 14.2 Battery Handling Rules

If using LiPo or lithium-ion cells:

```text
do not use damaged batteries
do not short battery terminals
do not leave charging unattended during early tests
do not charge swollen batteries
do not place battery where it can be punctured
secure the battery inside the robot
avoid crushing battery wires when closing shell
```

### 14.3 Bench Power Testing

Before battery operation, it is recommended to test:

```text
controller power
sensor power
servo power
voltage stability
current draw if possible
```

The voltage must be measured before connecting sensitive electronics.

### 14.4 Power Failure Behavior

If power is unsafe:

```text
block movement
log power warning
set LED warning/error state
announce warning if speaker available
enter safe mode or shutdown
```

---

## 15. Electrical Safety

The robot contains low-voltage electronics, but short circuits and wrong wiring can still damage components.

### 15.1 Wiring Rules

Before powering the robot:

```text
check polarity
check ground connection
check voltage rail
check loose wires
check exposed conductors
check servo power
check I2C wiring
check serial wiring
check battery connection
```

### 15.2 Common Ground

All communication between controller and modules requires common ground.

The project must document:

```text
controller ground
servo ground
sensor ground
battery ground
power module ground
```

### 15.3 Short Circuit Prevention

To reduce risk:

```text
insulate exposed wires
avoid loose jumper wires during movement
avoid metal objects near powered boards
secure modules before moving robot
use proper connectors when possible
do not close the shell if wires are being crushed
```

### 15.4 Electrical Validation

Electrical validation should include:

```text
voltage measurement
idle power test
sensor power test
servo idle test
servo movement power test
temperature observation
reset observation
```

---

## 16. Mechanical Safety

Mechanical safety prevents the robot from damaging itself or nearby objects.

### 16.1 Mechanical Rules

Before movement:

```text
legs must move freely
shell must not collide with legs
wires must not touch moving parts
servo horns must be secured
body must stand stably
battery must be secured
camera and sensors must be mounted
```

### 16.2 Surface Requirements

Early movement tests should use:

```text
flat surface
clean surface
low-risk area
no table edge
no fragile objects nearby
good lighting
operator supervision
```

Avoid:

```text
stairs
outdoor ground
high surfaces
slippery glass
crowded spaces
near pets
near children
near liquids
```

### 16.3 Tip-Over Handling

If the robot tips over:

```text
stop movement
disable torque if appropriate
enter safe mode
log event
operator resets robot manually
```

The robot should not attempt complex self-righting in V0.

---

## 17. Software Safety

Software must fail safely.

### 17.1 Software Safety Rules

The software should:

```text
handle missing hardware
handle sensor read errors
handle invalid values
handle servo communication errors
handle file write errors
handle keyboard interrupt
avoid infinite movement loops
avoid blocking servo commands
log safety-critical exceptions
stop movement on crash when possible
```

### 17.2 Exception Handling

Movement scripts should use safe cleanup logic.

Expected behavior on exception:

```text
stop movement
disable torque if appropriate
write error log if possible
set LED error state if possible
exit with clear message
```

### 17.3 Configuration Safety

Unsafe values must not be hardcoded randomly.

Configuration should define:

```text
movement limits
servo ranges
tilt thresholds
distance thresholds
battery thresholds
timeouts
enabled subsystems
```

### 17.4 Default Behavior

Default behavior should be conservative.

If a value is missing:

```text
movement should be blocked
warning should be logged
operator should configure the missing value
```

---

## 18. Autonomy Safety

The autonomy layer must be constrained.

### 18.1 Allowed Autonomy Output

The autonomy layer may output only predefined action names.

Allowed examples:

```text
STOP
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
TAKE_PHOTO
SPEAK_STATUS
```

### 18.2 Disallowed Autonomy Output

The autonomy layer must not output:

```text
raw servo positions
unbounded speeds
direct torque override
safety bypass requests
infinite loops
unsafe movement sequences
```

### 18.3 AI Agent Safety

If a future LLM or AI agent is added, it must only suggest actions from the safe action set.

Correct future architecture:

```text
LLM suggestion -> action name -> safety layer -> approved movement
```

Incorrect architecture:

```text
LLM output -> raw motor command
```

### 18.4 Autonomy Stop Conditions

Autonomy must stop if:

```text
safe mode is active
emergency stop is active
critical sensor fails
movement fails repeatedly
battery is low
operator requests stop
```

---

## 19. Dashboard Safety

The dashboard must not bypass internal safety.

### 19.1 Dashboard Commands

Allowed dashboard commands:

```text
START_DEMO
STOP
SAFE_MODE
RUN_SELF_CHECK
TAKE_PHOTO
MOVE_FORWARD_SMALL
TURN_LEFT_SMALL
TURN_RIGHT_SMALL
RETURN_TO_IDLE
SHUTDOWN
```

Disallowed dashboard commands:

```text
raw servo control
disable safety
ignore tilt
ignore obstacle
increase torque beyond configured limits
run unlimited movement
```

### 19.2 Dashboard Failure

If the dashboard disconnects:

```text
robot should continue safe local behavior
manual physical stop remains available
autonomous mode should not depend on dashboard connection
critical safety must remain onboard
```

### 19.3 Manual Stop

The dashboard should include a visible stop control, but physical power-off must remain available during early tests.

---

## 20. Logging Safety

Logs are part of the safety system.

### 20.1 Required Safety Log Events

The logger should record:

```text
session started
self-check started
self-check completed
movement requested
safety check result
movement allowed
movement blocked
safe mode entered
safe mode cleared
emergency stop
servo error
sensor error
power warning
tilt detected
obstacle detected
final status
```

### 20.2 Log Failure

If logs cannot be written:

```text
non-critical demo actions may continue
movement should be blocked if safety events cannot be recorded
operator should be notified
```

This rule can be adjusted later, but during development it is better to be conservative.

### 20.3 Evidence Link

Safety events should be connected to evidence when possible.

Example:

```text
tilt_detected -> log entry + video clip
obstacle_detected -> log entry + camera snapshot
servo_error -> log entry + terminal output
```

---

## 21. Emergency Stop

MicroBot Round V0 must have an emergency stop strategy.

### 21.1 Emergency Stop Methods

Possible emergency stop methods:

```text
physical power switch
keyboard interrupt
dashboard stop button
software STOP command
safe mode trigger
battery disconnect in extreme case
```

The physical power switch is the most reliable early-stage stop method.

### 21.2 Emergency Stop Behavior

When emergency stop is triggered:

```text
movement stops
servo torque is disabled if safe
autonomy pauses
LED turns red if possible
event is logged if possible
operator intervention required
```

### 21.3 Emergency Stop Test

Emergency stop should be tested before public demo.

Test:

```text
start safe movement
trigger stop
verify movement stops
verify event is logged
verify robot does not resume movement automatically
```

---

## 22. Testing Safety Procedure

Every new feature should follow this testing order.

### 22.1 Test Order

```text
offline code review
mock test
single component bench test
low-power test if applicable
no-load actuator test
small movement test
integrated bench test
assembled robot test
repeatability test
evidence capture
documentation update
```

### 22.2 Movement Test Order

```text
servo scan
read position
torque enable
tiny nudge
return to neutral
torque disable
repeat on second servo
both servos no load
legs mounted
manual clearance check
tiny movement with robot lifted or supported
tiny movement on flat surface
post-movement stability check
```

### 22.3 Repeatability

A safety feature should be tested multiple times.

Recommended minimum:

```text
3 successful repeated tests
```

A feature should not be marked demo-ready after one lucky success.

---

## 23. Demo Safety Checklist

Before a recorded demo:

```text
robot is on flat surface
operator can reach power switch
battery is safe
voltage is checked
legs are not blocked
wires are secured
servos are tested
IMU is working
obstacle sensor is working or disabled clearly
safe mode is working
stop command is working
log folder is writable
evidence folder exists
camera or phone is recording
no fragile objects nearby
```

During demo:

```text
do not leave robot unattended
do not run aggressive movement
do not place robot near edge
do not block legs by hand
do not ignore warnings
stop immediately if movement is abnormal
```

After demo:

```text
stop script
disable torque if needed
power down safely
check battery temperature
check servo temperature
save logs
save video
update current status
document failures
```

---

## 24. Public Claim Safety

The repository must not claim safety features before validation.

Incorrect claims:

```text
MicroBot is fully safe.
MicroBot can operate unsupervised.
MicroBot can navigate any room safely.
MicroBot can avoid all obstacles.
MicroBot can recover from any fall.
```

Correct claims:

```text
MicroBot Round V0 includes a planned safety layer.
MicroBot Round V0 blocks movement under defined unsafe conditions after validation.
MicroBot Round V0 is designed for supervised bench testing.
MicroBot Round V0 uses limited safe actions in its first demo.
```

After real tests, stronger claims may be used only with evidence.

---

## 25. Safety Validation Matrix

The following matrix defines when a safety feature can be considered validated.

```text
Feature: Tilt stop
Required evidence: IMU readings + blocked movement + log event + video or report
Status after evidence: hardware-validated

Feature: Obstacle stop
Required evidence: distance reading + blocked forward movement + log event + photo or video
Status after evidence: hardware-validated

Feature: Servo bus failure stop
Required evidence: simulated or real servo failure + blocked movement + log event
Status after evidence: bench-tested or hardware-validated

Feature: Emergency stop
Required evidence: stop command during movement + movement stops + log event
Status after evidence: hardware-validated

Feature: Battery low stop
Required evidence: low-power condition or mocked threshold + movement blocked + log event
Status after evidence: mocked, bench-tested or hardware-validated depending on test

Feature: Dashboard stop
Required evidence: dashboard command + movement blocked/stopped + log event
Status after evidence: integrated
```

---

## 26. Known Safety Limitations

Current safety limitations:

```text
safety layer is not fully implemented yet
tilt thresholds are not calibrated yet
obstacle thresholds are not calibrated yet
battery monitoring may be unavailable at first
servo current may not be directly measured
lift detection may be unreliable
dashboard stop may not exist at first
physical emergency stop may initially be the power switch
safe mode behavior must be tested on real hardware
```

These limitations are expected at the V0 stage.

They must remain documented until solved.

---

## 27. Safety Roadmap

### V0.1 — Safety Documentation

Goals:

```text
define safety architecture
define safe states
define action limits
define stop conditions
define demo safety rules
```

### V0.2 — Sensor Safety Bring-Up

Goals:

```text
IMU read test
tilt threshold test
distance reading test
obstacle threshold test
logging of safety events
```

### V0.3 — Servo Safety Bring-Up

Goals:

```text
servo scan
safe nudge
neutral return
torque disable
movement timeout
servo failure handling
```

### V0.4 — Integrated Safety Layer

Goals:

```text
self-check blocks unsafe movement
movement actions pass through safety layer
safe mode implemented
emergency stop implemented
safety events logged
```

### V0.5 — Demo Safety Validation

Goals:

```text
tilt stop video
obstacle stop video
safe movement video
session report
repeatable demo
documentation update
```

---

## 28. Final Safety Statement

MicroBot Round V0 must always prefer stopping over guessing.

The robot should move only when the system has enough information to consider the action safe.

The first version does not need advanced movement. It needs controlled movement.

The first version does not need full intelligence. It needs reliable safety boundaries.

The first version does not need to be perfect. It needs to be testable, inspectable and honest.

A successful safety system means that MicroBot Round V0 can:

```text
wake up
check itself
read safety sensors
refuse unsafe movement
move carefully when allowed
stop when unstable
log what happened
return to a safe state
```

That is the correct safety foundation for the MicroBot project.
