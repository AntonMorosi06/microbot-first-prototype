# MicroBot First Prototype - Current Status

## Status Label

Current status: `validated-offline / simulation-validated`

MicroBot First Prototype has passed the first offline simulation validation stage. The project is no longer only a prepared repository or a static documentation baseline. The current repository contains a working software boot sequence, a self-check pipeline, a MuJoCo model, and automated simulation tests for stability and repeated controlled motion.

This status does not mean that the physical robot has been validated. Hardware movement, real servo behavior, real power delivery, real IMU readings, real camera capture, real LED behavior and real battery behavior must still be tested on physical hardware.

## Simulation Validation Completed

Completed simulation files:

- `simulation/microbot_round_body.xml`
- `simulation/run_safe_nudge.py`
- `simulation/run_stability_sweep.py`
- `simulation/run_gait_preview.py`

The model loads correctly, remains upright in its patched initial pose, executes a small safe nudge, completes a stability sweep across multiple control amplitudes, and completes a repeated gait preview pattern.

This is meaningful because it proves that the simulated body, hinge joints, actuators, contact geometry, mass approximation and basic safety thresholds are coherent enough for early offline testing.

## Correct Public Claim

The correct public claim is:

```text
MicroBot First Prototype includes a working offline MuJoCo simulation pipeline. The model loads, remains upright, passes safe-nudge testing, passes stability-sweep testing, and completes a repeated gait-preview pattern while generating evidence reports.
```

## Incorrect Claims To Avoid

Do not claim:

- the real robot walks
- the hardware has been validated
- the real servos have been tested
- the real power system is safe
- the robot is autonomous
- the physical robot balances
- the simulated results prove real-world movement
- the MuJoCo model is an exact CAD replica

These claims are not yet supported by physical evidence.

## Hardware Status

Hardware status: `not hardware-validated`

Physical tests still required:

- power rail measurement
- Raspberry Pi boot check
- I2C bus check
- MPU-6050 IMU test
- Pi camera capture test
- WS2812 LED ring test
- audio output test
- microphone input test
- servo bus scan
- safe servo nudge with hardware movement explicitly enabled
- battery measurement or battery monitor validation
- distance sensor validation if installed

## Current Technical Milestone

Completed milestone:

```text
M1 - offline simulation motion validation
```

Next milestone:

```text
M2 - physical hardware bring-up without movement
```

M2 should include:

- Raspberry Pi setup
- dependencies installed on Pi
- self_check.py run on Pi
- camera test if camera is connected
- IMU test if MPU-6050 is connected
- LED test if ring is connected
- audio test if speaker/mic are connected
- servo scan only, no movement
- hardware evidence photos
- hardware evidence reports

Only after M2 should the project move toward:

```text
M3 - physical safe servo nudge
```

## Development Rule

Keep strict distinction between:

- prepared
- validated-offline
- hardware-ready
- hardware-validated
- integrated
- released

The current repository is:

```text
validated-offline
```

It is not yet:

- hardware-validated
- integrated
- released
