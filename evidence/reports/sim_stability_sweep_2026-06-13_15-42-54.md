# MicroBot Round V0 - Stability Sweep Report

Session ID: `sim_stability_sweep_2026-06-13_15-42-54`
XML model: `/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/simulation/microbot_round_body.xml`

## Summary

- Overall status: `OK`
- Tested amplitudes: `12`
- Stable amplitudes: `12`
- Failed amplitudes: `0`
- Maximum stable amplitude: `0.3`
- Recommended conservative control: `0.225`

## Results Table

| Amplitude | Status | Max tilt | Min height | Max XY drift | Message |
|---:|---|---:|---:|---:|---|
| 0.0200 | OK | 17.16 deg | 0.0757 m | 0.0026 m | Stable. |
| 0.0400 | OK | 17.07 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.0600 | OK | 16.98 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.0800 | OK | 16.89 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.1000 | OK | 16.79 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.1200 | OK | 16.70 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.1400 | OK | 16.60 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.1600 | OK | 16.51 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.1800 | OK | 16.41 deg | 0.0757 m | 0.0025 m | Stable. |
| 0.2000 | OK | 16.32 deg | 0.0757 m | 0.0024 m | Stable. |
| 0.2500 | OK | 16.08 deg | 0.0757 m | 0.0024 m | Stable. |
| 0.3000 | OK | 15.84 deg | 0.0757 m | 0.0024 m | Stable. |

## Interpretation

The model remained stable for at least one tested control amplitude. The recommended conservative control is intentionally lower than the maximum stable value.

## Important Limitation

This is simulation evidence only. It does not validate the real physical robot. The physical safe nudge must still be performed with hardware movement disabled by default, servo scan validation, supervised power testing, and the safety layer.
