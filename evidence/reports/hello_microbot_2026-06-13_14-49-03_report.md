# MicroBot Round V0 Hello Demo

Session ID: `hello_microbot_2026-06-13_14-49-03`
Started: 2026-06-13 14:49:03
Generated: 2026-06-13 14:49:03
Duration: 0.00 seconds
Event count: 13

## Summary

- DEBUG: 0
- INFO: 10
- WARNING: 2
- ERROR: 1
- CRITICAL: 0

## Events

### 1. INFO — logger — info

Time: 2026-06-13 14:49:03

Message: MicroBot logging session started.

Data:

```json
{
  "jsonl_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/logs/hello_microbot_2026-06-13_14-49-03.jsonl",
  "report_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/evidence/reports/hello_microbot_2026-06-13_14-49-03_report.md",
  "session_id": "hello_microbot_2026-06-13_14-49-03",
  "session_name": "MicroBot Round V0 Hello Demo"
}
```

### 2. INFO — system — info

Time: 2026-06-13 14:49:03

Message: Hello demo started.

Data:

```json
{
  "enable_movement": false,
  "safe_nudge_requested": false,
  "session_id": "hello_microbot_2026-06-13_14-49-03"
}
```

### 3. INFO — safety — info

Time: 2026-06-13 14:49:03

Message: Movement is disabled. Servo scan may run, but no movement will be performed.

### 4. INFO — leds — info

Time: 2026-06-13 14:49:03

Message: LED boot skipped by configuration.

### 5. INFO — audio — info

Time: 2026-06-13 14:49:03

Message: Audio startup skipped by configuration.

### 6. INFO — camera — info

Time: 2026-06-13 14:49:03

Message: Camera boot capture skipped by configuration.

### 7. WARNING — imu — self_check

Time: 2026-06-13 14:49:03

Message: IMU self-check skipped by configuration.

Data:

```json
{
  "message": "IMU self-check skipped by configuration.",
  "status": "UNAVAILABLE"
}
```

### 8. WARNING — servos — scan

Time: 2026-06-13 14:49:03

Message: Servo scan skipped by configuration.

Data:

```json
{
  "found_ids": [],
  "message": "Servo scan skipped by configuration.",
  "status": "UNAVAILABLE"
}
```

### 9. INFO — audio — info

Time: 2026-06-13 14:49:03

Message: Microphone test skipped.

### 10. INFO — servos — info

Time: 2026-06-13 14:49:03

Message: Safe nudge not requested. No movement will be performed.

### 11. ERROR — leds — status

Time: 2026-06-13 14:49:03

Message: Could not set LED status: RuntimeError: rpi_ws281x is not installed. Run: pip install rpi_ws281x

Data:

```json
{
  "message": "Could not set LED status: RuntimeError: rpi_ws281x is not installed. Run: pip install rpi_ws281x",
  "status": "FAILED",
  "timestamp": 1781354943.911568
}
```

### 12. INFO — system — info

Time: 2026-06-13 14:49:03

Message: Hello demo completed.

Data:

```json
{
  "audio_startup_ok": false,
  "camera_ok": false,
  "final_audio_ok": false,
  "imu_status": "UNAVAILABLE",
  "led_ok": false,
  "microphone_ok": false,
  "movement_enabled": false,
  "movement_ok": false,
  "movement_requested": false,
  "servo_scan_status": "UNAVAILABLE",
  "session_id": "hello_microbot_2026-06-13_14-49-03",
  "status": "OK"
}
```

### 13. INFO — logger — info

Time: 2026-06-13 14:49:03

Message: MicroBot logging session completed.

Data:

```json
{
  "event_count": 12,
  "session_id": "hello_microbot_2026-06-13_14-49-03"
}
```

## Notes

This report records software and hardware bring-up evidence for MicroBot Round V0. Hardware validation claims should only be made when the corresponding real test has been executed and documented.
