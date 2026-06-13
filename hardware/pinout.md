# Pinout

## 1. Purpose of This Document

This document defines the planned pinout for **MicroBot Round V0**, the first rounded physical bench prototype of the MicroBot project.

The purpose of this file is to define how the main controller pins are assigned to sensors, servos, LED ring, audio modules, optional buttons and future expansion ports.

This pinout is designed for a Raspberry Pi Zero 2 W style controller. It may be changed if the controller, sensors, servos or audio modules change.

The pinout must always remain synchronized with:

```text
hardware/wiring.md
hardware/power_budget.md
hardware/assembly_notes.md
setup/microbot/pins.py
setup/microbot/config.py
```

The central rule is:

```text
Do not wire hardware from memory. Always check this file, the wiring document and the real module datasheet before powering the robot.
```

---

## 2. Pinout Status

Current pinout status:

```text
Pinout plan: prepared
Physical wiring: not completed yet
Controller selected: Raspberry Pi Zero 2 W planned
Pin assignments validated: not yet
I2C validated: not yet
UART servo bus validated: not yet
LED pin validated: not yet
I2S audio validated: not yet
Camera connector validated: not yet
```

This file defines the intended V0 pinout. Actual wiring must be verified on the physical robot.

---

## 3. Controller Assumption

The planned controller for MicroBot Round V0 is:

```text
Raspberry Pi Zero 2 W
```

Reason:

```text
small form factor
Linux support
Python support
camera connector
40-pin GPIO header footprint
Wi-Fi
enough computing power for V0 behavior
suitable for logging and dashboard experiments
```

If a different controller is used, this pinout must be rewritten.

---

## 4. Pin Numbering Convention

This document uses two pin names:

```text
Physical pin number = actual position on the 40-pin header
GPIO / BCM number = Broadcom GPIO number used in software
```

Example:

```text
Physical pin 3 = GPIO2 = I2C SDA1
Physical pin 5 = GPIO3 = I2C SCL1
```

Software should use BCM/GPIO numbering unless a library requires a different convention.

---

## 5. Critical Voltage Warning

Raspberry Pi GPIO pins use **3.3 V logic**.

Important rule:

```text
Raspberry Pi GPIO pins are not 5 V tolerant.
```

This means:

```text
Do not connect a 5 V signal directly into a Raspberry Pi GPIO input.
Do not connect sensor output pins to GPIO unless voltage compatibility is known.
Use level shifting when needed.
Use 3.3 V-compatible modules where possible.
Measure and verify before connecting.
```

Power pins and signal pins are different.

A module may use 5 V power but still require 3.3 V-safe signal levels.

---

## 6. Planned V0 Pin Assignment Summary

| Subsystem            |     Signal |                 Physical Pin |    GPIO / BCM | Notes                                       |
| -------------------- | ---------: | ---------------------------: | ------------: | ------------------------------------------- |
| I2C bus              |        SDA |                            3 |         GPIO2 | IMU, distance sensor, optional light sensor |
| I2C bus              |        SCL |                            5 |         GPIO3 | Shared I2C clock                            |
| Servo bus            |    UART TX |                            8 | GPIO14 / TXD0 | Servo serial transmit                       |
| Servo bus            |    UART RX |                           10 | GPIO15 / RXD0 | Servo serial receive                        |
| LED ring             |    LED DIN |                           32 |        GPIO12 | WS2812B / NeoPixel data pin                 |
| I2S audio            |       BCLK |                           12 |        GPIO18 | Speaker amp / microphone clock              |
| I2S audio            | LRCLK / WS |                           35 |        GPIO19 | I2S word select                             |
| I2S microphone       |       DOUT |                           38 |        GPIO20 | Microphone data into controller             |
| I2S amplifier        |        DIN |                           40 |        GPIO21 | Audio data out to amplifier                 |
| Optional button      |   Button 1 |                           11 |        GPIO17 | Manual start / mode button                  |
| Optional stop button |   Button 2 |                           13 |        GPIO27 | Manual safe stop                            |
| Optional status      | Extra GPIO |                           15 |        GPIO22 | Reserved                                    |
| Optional expansion   | Extra GPIO |                           16 |        GPIO23 | Reserved                                    |
| Optional expansion   | Extra GPIO |                           18 |        GPIO24 | Reserved                                    |
| Optional expansion   | Extra GPIO |                           22 |        GPIO25 | Reserved                                    |
| Power                |      3.3 V |                      1 or 17 |           3V3 | For compatible sensors only                 |
| Power                |        5 V |                       2 or 4 |            5V | Controller rail / modules as appropriate    |
| Ground               |        GND | 6, 9, 14, 20, 25, 30, 34, 39 |           GND | Common ground                               |

This is the recommended initial assignment. It may change after real module testing.

---

## 7. I2C Bus Pinout

The I2C bus is used for sensors.

Planned I2C devices:

```text
IMU: MPU-6050 or similar
Distance sensor: VL53L0X / VL53L1X or similar
Optional light sensor: BH1750 or similar
Optional ADC / battery monitor if added
```

### I2C Pin Assignment

| Signal | Physical Pin | GPIO / BCM | Purpose                    |
| ------ | -----------: | ---------: | -------------------------- |
| SDA1   |            3 |      GPIO2 | I2C data                   |
| SCL1   |            5 |      GPIO3 | I2C clock                  |
| 3.3 V  |      1 or 17 |        3V3 | Sensor power if compatible |
| GND    | 6 or any GND |        GND | Common ground              |

### I2C Wiring

Logical wiring:

```text
Raspberry Pi GPIO2 / SDA -> sensor SDA
Raspberry Pi GPIO3 / SCL -> sensor SCL
Raspberry Pi 3.3 V       -> sensor VCC if module supports 3.3 V
Raspberry Pi GND         -> sensor GND
```

### I2C Safety Notes

```text
Check sensor voltage compatibility.
Avoid long I2C wires inside the robot.
If multiple I2C devices are used, confirm addresses do not conflict.
If readings are unstable, check pull-ups, wire length and ground.
```

### Expected Initial I2C Addresses

These are common addresses, not guaranteed.

| Device   | Common Address | Notes                      |
| -------- | -------------: | -------------------------- |
| MPU-6050 |   0x68 or 0x69 | Depends on AD0 pin         |
| VL53L0X  |           0x29 | Default ToF sensor address |
| BH1750   |   0x23 or 0x5C | Optional light sensor      |

Actual addresses must be verified with an I2C scan.

---

## 8. IMU Pinout

The IMU is safety-critical because it supports tilt and stability detection.

Recommended module:

```text
MPU-6050 or similar 6-DoF IMU
```

### IMU Wiring

| IMU Pin |    Raspberry Pi Pin | GPIO / Rail  | Notes                                                  |
| ------- | ------------------: | ------------ | ------------------------------------------------------ |
| VCC     |    Physical 1 or 17 | 3.3 V        | Use 3.3 V unless module explicitly supports 5 V safely |
| GND     |             Any GND | GND          | Common ground                                          |
| SDA     |          Physical 3 | GPIO2 / SDA1 | I2C data                                               |
| SCL     |          Physical 5 | GPIO3 / SCL1 | I2C clock                                              |
| INT     | not connected in V0 | optional     | Future interrupt support                               |

### IMU Placement Note

The IMU must be mounted firmly and its orientation must be documented in `hardware/assembly_notes.md`.

If the IMU is loose, tilt readings are not valid.

---

## 9. Distance Sensor Pinout

Recommended module:

```text
VL53L0X or VL53L1X ToF distance sensor
```

### Distance Sensor Wiring

| Sensor Pin  |                               Raspberry Pi Pin | GPIO / Rail                        | Notes                       |
| ----------- | ---------------------------------------------: | ---------------------------------- | --------------------------- |
| VIN / VCC   | Physical 1 or 17, or 2/4 if module supports it | 3.3 V or 5 V depending on breakout | Check breakout board        |
| GND         |                                        Any GND | GND                                | Common ground               |
| SDA         |                                     Physical 3 | GPIO2 / SDA1                       | Shared I2C data             |
| SCL         |                                     Physical 5 | GPIO3 / SCL1                       | Shared I2C clock            |
| XSHUT       |                                       optional | reserved GPIO                      | Future multi-sensor control |
| GPIO1 / INT |                                       optional | reserved GPIO                      | Future interrupt support    |

### Distance Sensor Safety Note

If the distance sensor is used for obstacle stop, it becomes safety-relevant.

If it is unavailable or invalid, forward movement should be blocked or the robot should run in reduced mode.

---

## 10. Servo Bus Pinout

The servos are used for leg movement.

Preferred actuator type:

```text
small serial bus servo with position feedback
```

The exact wiring depends on the selected servo model and adapter circuit.

### Planned UART Pins

| Signal    |        Physical Pin |      GPIO / BCM | Notes                                                 |
| --------- | ------------------: | --------------: | ----------------------------------------------------- |
| UART TXD0 |                   8 |          GPIO14 | Controller transmit                                   |
| UART RXD0 |                  10 |          GPIO15 | Controller receive                                    |
| GND       |             any GND |             GND | Common ground with servo rail                         |
| Servo VCC | external servo rail | 5 V servo power | Do not power high-current servos from weak logic rail |

### Full-Duplex UART Case

If the servo adapter supports separate TX and RX:

```text
Pi TXD0 -> servo adapter RX
Pi RXD0 -> servo adapter TX
Pi GND  -> servo adapter GND
Servo V+ -> servo power rail
Servo GND -> common ground
```

### Half-Duplex UART Case

Some serial bus servos use a single data line.

In that case, a half-duplex circuit, adapter or resistor-based wiring may be required.

Prototype concept:

```text
Pi UART TX/RX -> half-duplex interface -> servo DATA
Servo V+      -> servo power rail
Servo GND     -> common ground
```

The exact circuit must match the selected servo.

### Servo Safety Notes

```text
Do not connect servo power before measuring servo rail voltage.
Do not move servos before scanning ID.
Do not attempt walking as the first servo test.
Do not allow AI/autonomy to send raw servo target positions.
Keep servo power ground connected to controller ground.
Use a capacitor near the servo rail.
```

### Servo ID Plan

Recommended initial IDs:

| Servo       | Planned ID | Role      |
| ----------- | ---------: | --------- |
| Left servo  |          1 | Left leg  |
| Right servo |          2 | Right leg |

Actual IDs must be verified with `scan_servos.py`.

---

## 11. LED Ring Pinout

The LED ring provides visible robot status.

Recommended component:

```text
WS2812B / NeoPixel-compatible LED ring
```

### LED Pin Assignment

| LED Signal | Physical Pin | GPIO / BCM | Notes               |
| ---------- | -----------: | ---------: | ------------------- |
| DIN        |           32 |     GPIO12 | LED data            |
| VCC        |     5 V rail |        5 V | Depends on LED ring |
| GND        |      any GND |        GND | Common ground       |

### Why GPIO12?

GPIO12 is selected so that GPIO18 can remain available for I2S audio clock.

Some Raspberry Pi LED libraries commonly use PWM-capable pins. GPIO12 is suitable for this role, but actual library compatibility must be tested.

### LED Safety Notes

```text
Keep brightness low during early tests.
Do not run all LEDs at full white brightness from a weak power rail.
Use common ground between LED ring and controller.
Check whether data level is reliable at 3.3 V.
If LED behavior is unstable, consider a level shifter.
```

---

## 12. I2S Audio Pinout

The audio system may include:

```text
I2S audio amplifier for speaker output
I2S microphone for audio input
```

Recommended output module:

```text
MAX98357A I2S mono amplifier or similar
```

Recommended input module:

```text
INMP441 I2S microphone or similar
```

### I2S Pin Assignment

| I2S Signal           | Physical Pin | GPIO / BCM | Direction        | Purpose                           |
| -------------------- | -----------: | ---------: | ---------------- | --------------------------------- |
| BCLK                 |           12 |     GPIO18 | output           | I2S bit clock                     |
| LRCLK / WS           |           35 |     GPIO19 | output           | I2S word select                   |
| DIN to amplifier     |           40 |     GPIO21 | output           | Audio data from Pi to speaker amp |
| DOUT from microphone |           38 |     GPIO20 | input            | Audio data from microphone to Pi  |
| VCC                  | 3.3 V or 5 V |      power | module dependent | Check module requirements         |
| GND                  |      any GND |        GND | common           | Common ground                     |

### Audio Wiring Notes

```text
Do not connect a speaker directly to Raspberry Pi GPIO.
Use an amplifier module for speaker output.
Microphone and amplifier may share BCLK and LRCLK.
Data output and input must not be swapped.
Speaker output wires should connect to amplifier output, not GPIO.
```

### Audio Priority

Audio is useful for presentation but not required for first movement validation.

If audio fails, terminal output and LED states are acceptable fallbacks.

---

## 13. Camera Connector Pinout

The camera does not use normal GPIO pins.

It connects through:

```text
Raspberry Pi Zero CSI camera connector
```

### Camera Wiring

| Camera Signal | Connection            | Notes                                |
| ------------- | --------------------- | ------------------------------------ |
| Camera ribbon | Pi Zero CSI connector | Use compatible Pi Zero camera ribbon |
| Camera module | Forward-facing mount  | Lens must not be blocked             |

### Camera Notes

```text
Check ribbon orientation.
Do not sharply bend the ribbon.
Do not crush ribbon when closing shell.
Verify image after mounting.
```

Camera validation is performed by saving a frame to `evidence/photos/`.

---

## 14. Optional Button Pinout

Optional buttons may be added for local control.

Recommended buttons:

```text
Button 1: manual start / mode select
Button 2: manual safe stop
```

### Button Pin Assignment

| Button   | Physical Pin | GPIO / BCM | Wiring Style                  | Purpose      |
| -------- | -----------: | ---------: | ----------------------------- | ------------ |
| Button 1 |           11 |     GPIO17 | GPIO to GND, internal pull-up | Start / mode |
| Button 2 |           13 |     GPIO27 | GPIO to GND, internal pull-up | Safe stop    |

### Button Wiring

```text
GPIO input -> one side of button
GND        -> other side of button
software  -> internal pull-up enabled
```

### Button Safety Notes

```text
Button inputs need debounce.
Physical power switch remains the most reliable emergency stop in early tests.
Dashboard stop and software stop should not replace physical power access.
```

---

## 15. Optional Battery Monitor Pinout

Raspberry Pi does not have analog input.

Battery voltage monitoring requires:

```text
external ADC
battery fuel gauge module
safe voltage divider connected to ADC
```

Do not connect battery voltage directly to Raspberry Pi GPIO.

### Possible ADC Pinout

If an I2C ADC is added:

| ADC Signal |               Raspberry Pi Pin | GPIO / Rail         |
| ---------- | -----------------------------: | ------------------- |
| VCC        |               Physical 1 or 17 | 3.3 V               |
| GND        |                        any GND | GND                 |
| SDA        |                     Physical 3 | GPIO2 / SDA1        |
| SCL        |                     Physical 5 | GPIO3 / SCL1        |
| A0         | battery voltage divider output | analog input to ADC |

### Battery Monitor Status

Battery monitoring may initially be:

```text
mocked
unavailable
manual measurement only
```

If not implemented, software should clearly report:

```text
Battery monitor: unavailable
```

---

## 16. Reserved GPIO Pins

The following GPIO pins are reserved for future expansion.

| Physical Pin | GPIO / BCM | Possible Future Use                 |
| -----------: | ---------: | ----------------------------------- |
|           15 |     GPIO22 | extra status signal / sensor enable |
|           16 |     GPIO23 | expansion                           |
|           18 |     GPIO24 | expansion                           |
|           22 |     GPIO25 | expansion                           |
|           29 |      GPIO5 | future input                        |
|           31 |      GPIO6 | future input                        |
|           36 |     GPIO16 | future output                       |
|           37 |     GPIO26 | future output                       |

Reserved pins should not be used casually.

Any change must be documented here and in `setup/microbot/pins.py`.

---

## 17. Pins to Avoid or Treat Carefully

Some pins should be treated carefully.

| Physical Pin |    GPIO / BCM | Reason                                   |
| -----------: | ------------: | ---------------------------------------- |
|           27 | GPIO0 / ID_SD | HAT EEPROM / ID pin, avoid unless needed |
|           28 | GPIO1 / ID_SC | HAT EEPROM / ID pin, avoid unless needed |
|            3 |   GPIO2 / SDA | Has I2C pull-up behavior                 |
|            5 |   GPIO3 / SCL | Has I2C pull-up behavior                 |
|            8 |  GPIO14 / TXD | UART TX, used for servo bus              |
|           10 |  GPIO15 / RXD | UART RX, used for servo bus              |
|           12 |        GPIO18 | I2S / PWM, reserved for audio clock      |
|           32 |        GPIO12 | LED signal, timing-sensitive             |

Avoid using ID pins 27 and 28 unless there is a specific reason.

---

## 18. Full Raspberry Pi 40-Pin Reference

This table is included as a reference for the Raspberry Pi 40-pin header.

| Physical Pin | Function                |
| -----------: | ----------------------- |
|            1 | 3.3 V                   |
|            2 | 5 V                     |
|            3 | GPIO2 / SDA1            |
|            4 | 5 V                     |
|            5 | GPIO3 / SCL1            |
|            6 | GND                     |
|            7 | GPIO4                   |
|            8 | GPIO14 / TXD0           |
|            9 | GND                     |
|           10 | GPIO15 / RXD0           |
|           11 | GPIO17                  |
|           12 | GPIO18 / PCM_CLK / PWM0 |
|           13 | GPIO27                  |
|           14 | GND                     |
|           15 | GPIO22                  |
|           16 | GPIO23                  |
|           17 | 3.3 V                   |
|           18 | GPIO24                  |
|           19 | GPIO10 / SPI0 MOSI      |
|           20 | GND                     |
|           21 | GPIO9 / SPI0 MISO       |
|           22 | GPIO25                  |
|           23 | GPIO11 / SPI0 SCLK      |
|           24 | GPIO8 / SPI0 CE0        |
|           25 | GND                     |
|           26 | GPIO7 / SPI0 CE1        |
|           27 | GPIO0 / ID_SD           |
|           28 | GPIO1 / ID_SC           |
|           29 | GPIO5                   |
|           30 | GND                     |
|           31 | GPIO6                   |
|           32 | GPIO12 / PWM0           |
|           33 | GPIO13 / PWM1           |
|           34 | GND                     |
|           35 | GPIO19 / PCM_FS / PWM1  |
|           36 | GPIO16                  |
|           37 | GPIO26                  |
|           38 | GPIO20 / PCM_DIN        |
|           39 | GND                     |
|           40 | GPIO21 / PCM_DOUT       |

---

## 19. Software Mapping for `setup/microbot/pins.py`

The first `pins.py` file should reflect this document.

Planned constants:

```python
# Robot identity
ROBOT_NAME = "MicroBot Round V0"
SOFTWARE_VERSION = "0.1.0"

# I2C
I2C_SDA_GPIO = 2
I2C_SCL_GPIO = 3
IMU_I2C_ADDRESS = 0x68
DISTANCE_I2C_ADDRESS = 0x29

# Servo UART
SERVO_UART_TX_GPIO = 14
SERVO_UART_RX_GPIO = 15
SERVO_UART_DEVICE = "/dev/serial0"
SERVO_BAUDRATE = 1000000
LEFT_SERVO_ID = 1
RIGHT_SERVO_ID = 2

# LED
LED_GPIO = 12
LED_COUNT = 7
LED_BRIGHTNESS = 40

# I2S Audio
I2S_BCLK_GPIO = 18
I2S_LRCLK_GPIO = 19
I2S_MIC_DOUT_GPIO = 20
I2S_AMP_DIN_GPIO = 21

# Buttons
BUTTON_START_GPIO = 17
BUTTON_STOP_GPIO = 27

# Safety placeholders
TILT_WARNING_DEGREES = 20
TILT_CRITICAL_DEGREES = 30
OBSTACLE_WARNING_CM = 25
OBSTACLE_STOP_CM = 15
```

These values are placeholders until real hardware calibration.

---

## 20. Pinout Validation Tests

The following tests validate the pinout.

### P-TEST-001 — I2C Scan

Goal:

```text
verify IMU and distance sensor addresses
```

Expected:

```text
IMU visible at expected address
distance sensor visible at expected address
```

### P-TEST-002 — LED GPIO Test

Goal:

```text
verify GPIO12 controls LED ring
```

Expected:

```text
LED ring shows red, green, blue and idle blue
```

### P-TEST-003 — UART Servo Test

Goal:

```text
verify UART pins communicate with servo bus
```

Expected:

```text
servo IDs detected without movement
```

### P-TEST-004 — I2S Audio Test

Goal:

```text
verify speaker output and microphone input
```

Expected:

```text
speaker plays phrase
microphone level changes when sound is produced
```

### P-TEST-005 — Button Test

Goal:

```text
verify optional buttons read correctly
```

Expected:

```text
button press changes GPIO state
```

---

## 21. Pinout Change Rules

Whenever a pin assignment changes, update:

```text
hardware/pinout.md
hardware/wiring.md
setup/microbot/pins.py
docs/current_status.md
CHANGELOG.md
```

If the change affects power, also update:

```text
hardware/power_budget.md
```

If the change affects physical layout, also update:

```text
hardware/assembly_notes.md
```

No pin change should remain undocumented.

---

## 22. Pinout Change Log Template

Use this template when changing a pin.

```text
Date:
Changed signal:
Old pin:
New pin:
Reason:
Files updated:
Test performed:
Result:
Evidence:
Next action:
```

Example:

```text
Date: 2026-06-13
Changed signal: LED DIN
Old pin: GPIO18
New pin: GPIO12
Reason: reserve GPIO18 for I2S audio clock
Files updated: hardware/pinout.md, setup/microbot/pins.py
Test performed: test_leds.py
Result: pending
Evidence: none yet
Next action: validate LED ring on GPIO12
```

---

## 23. Pinout Safety Checklist

Before powering:

```text
[ ] voltage rails checked
[ ] common ground confirmed
[ ] GPIO inputs are not receiving 5 V
[ ] I2C wiring checked
[ ] UART wiring checked
[ ] LED data pin checked
[ ] camera ribbon orientation checked
[ ] audio wiring checked if installed
[ ] servo rail voltage measured
[ ] no loose wires touching power rails
```

Before movement:

```text
[ ] servo IDs detected
[ ] servo positions readable
[ ] servo power stable
[ ] IMU detected
[ ] safety thresholds configured
[ ] emergency stop method available
```

---

## 24. Final Pinout Statement

This pinout defines the first planned electrical interface for MicroBot Round V0.

The pinout is designed to support:

```text
I2C sensing
UART servo communication
LED status output
I2S audio input/output
CSI camera capture
optional local buttons
future expansion
```

The pinout is not considered validated until each assigned interface has been physically tested.

A successful pinout validation means:

```text
I2C sensors are detected
LED ring responds
camera captures frames
servo bus detects servos
audio works if installed
optional buttons work if installed
no GPIO receives unsafe voltage
all changes are documented
```

Only after pinout validation should the robot move toward full integrated testing.
