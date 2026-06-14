# MicroBot First Prototype

MicroBot First Prototype is the first real bench-oriented prototype baseline for the MicroBot project.

The goal of this repository is to move from idea and documentation to a real, testable engineering workflow: software boot, safety logic, hardware bring-up, MuJoCo simulation, evidence reports, and eventually a small physical prototype.

## Current Status

Current status: `validated-offline / simulation-validated`

The repository now contains a working offline simulation pipeline. The MuJoCo model loads correctly, remains upright, passes a safe nudge test, passes a stability sweep test, and completes a repeated gait preview pattern while generating JSON, Markdown and CSV evidence reports.

This does not mean that the physical robot has been validated. Hardware movement, real servo behavior, real power delivery, real IMU readings, real camera capture, real LED behavior and real battery behavior must still be tested on physical hardware.

## What Works

- software configuration loading
- runtime directory creation
- logging system
- self-check report generation
- safety-layer self-check
- battery threshold simulation
- distance threshold simulation
- hello MicroBot software boot
- MuJoCo XML model loading
- stable initial simulated body pose
- safe nudge simulation
- stability sweep simulation
- gait preview simulation
- evidence report generation

## Main Areas

- `docs/` - project documentation
- `hardware/` - BOM, pinout, wiring and power notes
- `setup/microbot/` - Python support modules
- `setup/scripts/` - bring-up and test scripts
- `simulation/` - MuJoCo model and simulation scripts
- `evidence/reports/` - generated validation reports
- `logs/` - local runtime logs

## Simulation Commands

Activate the MuJoCo environment:

```bash
source /opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh
conda activate microbot312
```

Run the current simulation validation scripts:

```bash
python simulation/run_safe_nudge.py
python simulation/run_stability_sweep.py
python simulation/run_gait_preview.py
```

## Correct Claim

This repository can currently claim:

```text
MicroBot First Prototype has a working offline MuJoCo simulation validation pipeline.
```

It should not yet claim:

- the real robot walks
- the real hardware is validated
- the physical robot is autonomous
- the robot is finished

## Next Milestone

Next milestone: `M2 - physical hardware bring-up without movement`

The next phase is to run tests on Raspberry Pi hardware without enabling physical movement:

- Raspberry Pi boot
- dependency setup
- self-check on Pi
- camera test
- IMU test
- LED test
- audio test
- servo scan only
- hardware evidence photos
- hardware evidence reports

Only after that should physical safe servo movement be attempted.
