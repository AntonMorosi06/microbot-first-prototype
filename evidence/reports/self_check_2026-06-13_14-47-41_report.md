# MicroBot Round V0 Self-Check

Session ID: `self_check_2026-06-13_14-47-41`
Started: 2026-06-13 14:47:41
Generated: 2026-06-13 14:47:41
Duration: 0.00 seconds
Event count: 14

## Summary

- DEBUG: 0
- INFO: 11
- WARNING: 3
- ERROR: 0
- CRITICAL: 0

## Events

### 1. INFO — logger — info

Time: 2026-06-13 14:47:41

Message: MicroBot logging session started.

Data:

```json
{
  "jsonl_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/logs/self_check_2026-06-13_14-47-41.jsonl",
  "report_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/evidence/reports/self_check_2026-06-13_14-47-41_report.md",
  "session_id": "self_check_2026-06-13_14-47-41",
  "session_name": "MicroBot Round V0 Self-Check"
}
```

### 2. INFO — logger — info

Time: 2026-06-13 14:47:41

Message: Logger check event written from self_check.py.

Data:

```json
{
  "jsonl_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/logs/self_check_2026-06-13_14-47-41.jsonl",
  "report_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/evidence/reports/self_check_2026-06-13_14-47-41_report.md",
  "session_id": "self_check_2026-06-13_14-47-41"
}
```

### 3. INFO — config — self_check

Time: 2026-06-13 14:47:41

Message: Configuration loaded and runtime directories are available.

Data:

```json
{
  "hardware_version": "v0",
  "logs_dir": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/logs",
  "message": "Configuration loaded and runtime directories are available.",
  "movement_enabled": false,
  "photos_dir": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/evidence/photos",
  "project_name": "MicroBot Round V0",
  "project_root": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0",
  "project_slug": "microbot-round-v0",
  "reports_dir": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/evidence/reports",
  "software_version": "0.1.0",
  "status": "OK",
  "status_label": "prepared",
  "timestamp": 1781354861.0025249
}
```

### 4. INFO — logger — self_check

Time: 2026-06-13 14:47:41

Message: Logger is active and accepted a test event.

Data:

```json
{
  "jsonl_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/logs/self_check_2026-06-13_14-47-41.jsonl",
  "message": "Logger is active and accepted a test event.",
  "report_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/evidence/reports/self_check_2026-06-13_14-47-41_report.md",
  "session_id": "self_check_2026-06-13_14-47-41",
  "status": "OK",
  "timestamp": 1781354861.002592
}
```

### 5. INFO — safety — self_check

Time: 2026-06-13 14:47:41

Message: Safety self-check completed.

Data:

```json
{
  "allowed_decision": {
    "action": "SAFE_NUDGE",
    "allowed": true,
    "movement_allowed": true,
    "reasons": [
      "All configured safety checks passed."
    ],
    "severity": "INFO",
    "state": "MOVEMENT_ALLOWED",
    "timestamp": 1781354861.002625,
    "warnings": []
  },
  "blocked_decision": {
    "action": "SAFE_NUDGE",
    "allowed": false,
    "movement_allowed": false,
    "reasons": [
      "IMU status blocks movement: CRITICAL.",
      "Tilt is critical: 45.0 degrees >= 30.0 degrees.",
      "Battery voltage is critical: 3.30 V <= 3.30 V."
    ],
    "severity": "ERROR",
    "state": "MOVEMENT_BLOCKED",
    "timestamp": 1781354861.002646,
    "warnings": []
  },
  "disabled_decision": {
    "action": "SAFE_NUDGE",
    "allowed": false,
    "movement_allowed": false,
    "reasons": [
      "Hardware movement is disabled by configuration. Set hardware_movement_enabled=True only after real safety validation."
    ],
    "severity": "ERROR",
    "state": "MOVEMENT_BLOCKED",
    "timestamp": 1781354861.002636,
    "warnings": []
  },
  "message": "Safety self-check completed.",
  "photo_decision": {
    "action": "TAKE_PHOTO",
    "allowed": true,
    "movement_allowed": false,
    "reasons": [
      "TAKE_PHOTO is allowed as a non-movement action."
    ],
    "severity": "INFO",
    "state": "SAFE_IDLE",
    "timestamp": 1781354861.002652,
    "warnings": []
  },
  "status": "OK",
  "timestamp": 1781354861.002663
}
```

### 6. INFO — leds — self_check

Time: 2026-06-13 14:47:41

Message: LED check skipped by command-line flag.

Data:

```json
{
  "message": "LED check skipped by command-line flag.",
  "status": "SKIPPED",
  "timestamp": 1781354861.002665
}
```

### 7. INFO — audio — self_check

Time: 2026-06-13 14:47:41

Message: Audio check skipped by command-line flag.

Data:

```json
{
  "message": "Audio check skipped by command-line flag.",
  "status": "SKIPPED",
  "timestamp": 1781354861.002666
}
```

### 8. INFO — camera — self_check

Time: 2026-06-13 14:47:41

Message: Camera check skipped by command-line flag.

Data:

```json
{
  "message": "Camera check skipped by command-line flag.",
  "status": "SKIPPED",
  "timestamp": 1781354861.002666
}
```

### 9. INFO — imu — self_check

Time: 2026-06-13 14:47:41

Message: IMU check skipped by command-line flag.

Data:

```json
{
  "message": "IMU check skipped by command-line flag.",
  "status": "SKIPPED",
  "timestamp": 1781354861.002666
}
```

### 10. INFO — servos — self_check

Time: 2026-06-13 14:47:41

Message: Servo scan skipped by command-line flag.

Data:

```json
{
  "message": "Servo scan skipped by command-line flag.",
  "status": "SKIPPED",
  "timestamp": 1781354861.002667
}
```

### 11. WARNING — distance — self_check

Time: 2026-06-13 14:47:41

Message: Distance sensor is not implemented. Forward movement should be blocked or reduced.

Data:

```json
{
  "distance_cm": null,
  "forward_movement_allowed": false,
  "message": "Distance sensor is not implemented. Forward movement should be blocked or reduced.",
  "obstacle_detected": false,
  "source": "unavailable",
  "status": "UNAVAILABLE",
  "timestamp": 1781354861.002673
}
```

### 12. WARNING — battery — self_check

Time: 2026-06-13 14:47:41

Message: Battery monitoring is not implemented. Use bench power or manual measurement.

Data:

```json
{
  "message": "Battery monitoring is not implemented. Use bench power or manual measurement.",
  "movement_allowed": false,
  "percentage": null,
  "source": "unavailable",
  "status": "UNAVAILABLE",
  "timestamp": 1781354861.0026822,
  "voltage": null
}
```

### 13. WARNING — system — self_check_summary

Time: 2026-06-13 14:47:41

Message: Self-check completed with warnings or unavailable optional hardware.

Data:

```json
{
  "counts": {
    "FAILED": 0,
    "OK": 3,
    "SKIPPED": 5,
    "UNAVAILABLE": 2,
    "UNKNOWN": 0,
    "WARNING": 0
  },
  "failed_subsystems": [],
  "message": "Self-check completed with warnings or unavailable optional hardware.",
  "skipped_subsystems": [
    "leds",
    "audio",
    "camera",
    "imu",
    "servos"
  ],
  "status": "WARNING",
  "summary_json_path": "/Users/antonmorosi/Desktop/first real prototyope/microbot-round-v0/evidence/reports/self_check_2026-06-13_14-47-41_summary.json",
  "timestamp": 1781354861.002691,
  "unavailable_subsystems": [
    "distance",
    "battery"
  ],
  "warning_subsystems": []
}
```

### 14. INFO — logger — info

Time: 2026-06-13 14:47:41

Message: MicroBot logging session completed.

Data:

```json
{
  "event_count": 13,
  "session_id": "self_check_2026-06-13_14-47-41"
}
```

## Notes

This report records software and hardware bring-up evidence for MicroBot Round V0. Hardware validation claims should only be made when the corresponding real test has been executed and documented.
