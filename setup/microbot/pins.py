"""
MicroBot Round V0 pin and hardware constants.

This file centralizes the first hardware mapping for MicroBot Round V0.

Target controller:

- Raspberry Pi Zero 2 W
- Raspberry Pi OS Lite / Bookworm
- 40-pin GPIO header

Reference V0 hardware pattern:

- SCS0009 / SC09 serial bus servos on /dev/serial0
- MPU-6050 IMU on I2C address 0x68
- WS2812B / NeoPixel LED ring on GPIO12
- MAX98357A I2S amplifier
- INMP441 I2S microphone
- Pi-compatible CSI camera
- shared 5 V rail for early V0 testing
- common ground across all modules

Important rule:
This file should contain constants only. Hardware logic belongs in the subsystem
modules such as servos.py, imu.py, leds.py, audio.py and camera.py.
"""

from __future__ import annotations


# =============================================================================
# Project identity
# =============================================================================

PROJECT_NAME = "MicroBot Round V0"
PROJECT_SLUG = "microbot-round-v0"
HARDWARE_VERSION = "v0"
PINOUT_VERSION = "0.1.0"


# =============================================================================
# Raspberry Pi board reference
# =============================================================================

CONTROLLER_BOARD = "Raspberry Pi Zero 2 W"
GPIO_NUMBERING = "BCM"
GPIO_HEADER = "40-pin"


# =============================================================================
# Power rails
# =============================================================================

# Physical 5 V pins on the Raspberry Pi 40-pin header.
PI_5V_PHYSICAL_PINS = (2, 4)

# Physical 3.3 V pins on the Raspberry Pi 40-pin header.
PI_3V3_PHYSICAL_PINS = (1, 17)

# Recommended ground pins for common ground.
PI_GND_PHYSICAL_PINS = (6, 9, 14, 20, 25, 30, 34, 39)

# V0 power architecture.
POWER_ARCHITECTURE = "shared_5v_rail_v0"

# V0 warning:
# The first bench prototype may share one 5 V rail for Pi, servos, LEDs and amp.
# This must be treated as an early prototype choice, not as the final power design.
SHARED_5V_RAIL = True

# Recommended capacitor across the 5 V rail near the servos.
SERVO_RAIL_CAPACITOR_UF_MIN = 470
SERVO_RAIL_CAPACITOR_UF_RECOMMENDED = 1000
SERVO_RAIL_CAPACITOR_VOLTAGE_MIN = 10

# Recommended boost converter output for early V0 testing.
BOOST_OUTPUT_VOLTAGE = 5.1


# =============================================================================
# I2C bus
# =============================================================================

I2C_BUS = 1

I2C_SDA_GPIO = 2
I2C_SCL_GPIO = 3

I2C_SDA_PHYSICAL_PIN = 3
I2C_SCL_PHYSICAL_PIN = 5

# MPU-6050 / GY-521 IMU.
IMU_I2C_ADDR = 0x68
IMU_ALT_I2C_ADDR = 0x69

# Optional future VL53L0X / VL53L1X time-of-flight distance sensor.
DISTANCE_I2C_ADDR = 0x29


# =============================================================================
# Serial bus servos: Feetech SCS0009 / Waveshare SC09
# =============================================================================

# On Raspberry Pi Zero 2 W, /dev/serial0 should point to the usable PL011 UART
# after serial console is disabled and Bluetooth is detached when needed.
SERVO_PORT = "/dev/serial0"
SERVO_BAUD = 1_000_000
SERVO_TIMEOUT_SECONDS = 0.05

# UART pins, BCM numbering.
SERVO_TX_GPIO = 14
SERVO_RX_GPIO = 15

# UART pins, physical header numbering.
SERVO_TX_PHYSICAL_PIN = 8
SERVO_RX_PHYSICAL_PIN = 10

# Half-duplex servo data line:
# TX goes through a 1 kΩ resistor to the DATA bus.
# RX connects directly to the same DATA bus.
SERVO_HALF_DUPLEX = True
SERVO_TX_SERIES_RESISTOR_OHMS = 1_000

# Servo IDs expected in the first two-leg MicroBot Round V0 build.
# Do not assume left/right mechanically until the real horn mounting is verified.
SERVO_IDS = (1, 2)

# Optional mapping placeholders.
# Keep these as None until the physical robot confirms which ID is left/right.
LEFT_LEG_ID: int | None = None
RIGHT_LEG_ID: int | None = None

# Encoder range for SCS0009.
# The servo reports 0-1023 over roughly 300 degrees.
# The usable lower range may be higher on real units, so V0 clamps conservatively.
ENCODER_MIN = 255
ENCODER_MAX = 1023
ENCODER_CENTER = 512

# Safe nudge for smoke tests.
# Around 30 encoder units is a small visible movement.
SAFE_NUDGE = 30

# Movement timing defaults.
SAFE_NUDGE_STEP = 5
SAFE_NUDGE_DWELL_SECONDS = 0.02
SERVO_SETTLE_SECONDS = 0.20
TORQUE_RELEASE_ON_EXIT = True

# SCS0009 / SC09 register map.
# Important: 2-byte values are BIG-ENDIAN for this servo family.
REG_ID = 0x03
REG_TORQUE_ENABLE = 0x28
REG_GOAL_POS = 0x2A
REG_EEPROM_LOCK = 0x30
REG_PRESENT_POS = 0x38

# Instruction codes used by the serial bus driver.
INST_PING = 0x01
INST_READ = 0x02
INST_WRITE = 0x03
INST_SYNC_WRITE = 0x83
BROADCAST_ID = 0xFE

# Servo status values.
TORQUE_OFF = 0
TORQUE_ON = 1

# The SCS0009 uses big-endian word order for two-byte registers.
SERVO_WORD_ENDIANNESS = "big"


# =============================================================================
# WS2812B / NeoPixel LED ring
# =============================================================================

# LED ring data pin.
LED_PIN = 12
LED_PHYSICAL_PIN = 32

# 7-pixel ring, matching the reference V0 style.
LED_COUNT = 7

# Keep brightness conservative for early power tests.
LED_BRIGHTNESS = 40

# rpi_ws281x timing defaults.
LED_FREQ_HZ = 800_000
LED_DMA = 10
LED_CHANNEL = 0
LED_INVERT = False

# LED status colors in RGB order.
LED_COLOR_OFF = (0, 0, 0)
LED_COLOR_BOOT = (0, 80, 255)
LED_COLOR_OK = (0, 255, 0)
LED_COLOR_WARNING = (255, 180, 0)
LED_COLOR_ERROR = (255, 0, 0)
LED_COLOR_DECISION = (150, 0, 255)
LED_COLOR_OBSTACLE = (255, 80, 0)
LED_COLOR_SELF_CHECK = (255, 255, 255)


# =============================================================================
# I2S audio: MAX98357A amplifier + INMP441 microphone
# =============================================================================

# Shared I2S clock pins.
I2S_BCLK_GPIO = 18
I2S_LRCLK_GPIO = 19

I2S_BCLK_PHYSICAL_PIN = 12
I2S_LRCLK_PHYSICAL_PIN = 35

# Microphone input: INMP441 SD / DOUT.
I2S_MIC_DATA_GPIO = 20
I2S_MIC_DATA_PHYSICAL_PIN = 38

# Amplifier output: MAX98357A DIN.
I2S_AMP_DATA_GPIO = 21
I2S_AMP_DATA_PHYSICAL_PIN = 40

# INMP441 L/R pin.
# Tying L/R to GND usually selects the left channel.
MIC_CHANNEL_SELECT = "left"
MIC_LR_TO_GND = True

# MAX98357A configuration notes.
AMP_SD_TIE_TO_3V3 = True
AMP_GAIN_FLOATING_DB = 9

# ALSA device hint.
# On some Raspberry Pi audio overlays this may be different.
AUDIO_DEVICE = "plughw:CARD=sndrpigooglevoi"

# Default speech phrases.
HELLO_PHRASE = "Hello. I am MicroBot Round V0."
STARTUP_PHRASE = "MicroBot Round V0 online. System check started."
COMPLETE_PHRASE = "MicroBot Round V0. Autonomous safety demo completed."
WARNING_PHRASE = "Warning. Safe mode active."


# =============================================================================
# Camera
# =============================================================================

# Raspberry Pi camera uses CSI ribbon, not GPIO pins.
CAMERA_INTERFACE = "CSI"
CAMERA_DEFAULT_WIDTH = 640
CAMERA_DEFAULT_HEIGHT = 480
CAMERA_DEFAULT_TIMEOUT_MS = 800

# Pi Zero camera ribbon reference.
CAMERA_RIBBON = "22-pin to 15-pin Pi Zero CSI ribbon"


# =============================================================================
# Optional buttons / emergency stop
# =============================================================================

# These are optional for MicroBot Round V0.
# If physical buttons are not installed yet, leave the feature disabled in config.py.
BUTTON_1_GPIO = 17
BUTTON_1_PHYSICAL_PIN = 11

BUTTON_2_GPIO = 27
BUTTON_2_PHYSICAL_PIN = 13

EMERGENCY_STOP_GPIO: int | None = None
EMERGENCY_STOP_PHYSICAL_PIN: int | None = None


# =============================================================================
# Optional battery / voltage monitoring
# =============================================================================

# Raspberry Pi has no analog input.
# Real battery voltage monitoring requires an ADC or fuel gauge module.
BATTERY_MONITOR_AVAILABLE = False
BATTERY_ADC_I2C_ADDR: int | None = None

BATTERY_WARNING_VOLTAGE = 3.65
BATTERY_LOW_VOLTAGE = 3.50
BATTERY_MOVEMENT_BLOCK_VOLTAGE = 3.45
BATTERY_CRITICAL_VOLTAGE = 3.30


# =============================================================================
# Optional distance sensor
# =============================================================================

DISTANCE_SENSOR_AVAILABLE = False
DISTANCE_SENSOR_TYPE = "VL53L0X_or_VL53L1X_optional"
DISTANCE_WARNING_CM = 25.0
DISTANCE_STOP_CM = 15.0
DISTANCE_CRITICAL_CM = 8.0


# =============================================================================
# Safety defaults
# =============================================================================

MOVEMENT_ENABLED_BY_DEFAULT = False
REQUIRE_SERVO_SCAN_BEFORE_MOVE = True
REQUIRE_POSITION_READ_BEFORE_MOVE = True
REQUIRE_IMU_BEFORE_MOVE = True
REQUIRE_SAFE_POWER_BEFORE_MOVE = True

TILT_WARNING_DEGREES = 20.0
TILT_CRITICAL_DEGREES = 30.0

MAX_FAILED_MOVEMENTS_BEFORE_SAFE_MODE = 3


# =============================================================================
# Human-readable pin tables
# =============================================================================

PINOUT_TABLE = {
    "5v_power": {
        "physical_pins": PI_5V_PHYSICAL_PINS,
        "description": "5 V rail input to Raspberry Pi and shared V0 power rail.",
    },
    "3v3_power": {
        "physical_pins": PI_3V3_PHYSICAL_PINS,
        "description": "3.3 V output from Raspberry Pi for IMU and microphone logic.",
    },
    "ground": {
        "physical_pins": PI_GND_PHYSICAL_PINS,
        "description": "Common ground for all modules.",
    },
    "i2c_sda": {
        "gpio": I2C_SDA_GPIO,
        "physical_pin": I2C_SDA_PHYSICAL_PIN,
        "description": "I2C SDA for MPU-6050 and optional distance sensor.",
    },
    "i2c_scl": {
        "gpio": I2C_SCL_GPIO,
        "physical_pin": I2C_SCL_PHYSICAL_PIN,
        "description": "I2C SCL for MPU-6050 and optional distance sensor.",
    },
    "servo_tx": {
        "gpio": SERVO_TX_GPIO,
        "physical_pin": SERVO_TX_PHYSICAL_PIN,
        "description": "UART TX through 1 kΩ resistor to servo DATA bus.",
    },
    "servo_rx": {
        "gpio": SERVO_RX_GPIO,
        "physical_pin": SERVO_RX_PHYSICAL_PIN,
        "description": "UART RX directly from servo DATA bus.",
    },
    "led_ring": {
        "gpio": LED_PIN,
        "physical_pin": LED_PHYSICAL_PIN,
        "description": "WS2812B / NeoPixel ring data pin.",
    },
    "i2s_bclk": {
        "gpio": I2S_BCLK_GPIO,
        "physical_pin": I2S_BCLK_PHYSICAL_PIN,
        "description": "I2S bit clock for amp and mic.",
    },
    "i2s_lrclk": {
        "gpio": I2S_LRCLK_GPIO,
        "physical_pin": I2S_LRCLK_PHYSICAL_PIN,
        "description": "I2S word select / left-right clock for amp and mic.",
    },
    "i2s_mic_data": {
        "gpio": I2S_MIC_DATA_GPIO,
        "physical_pin": I2S_MIC_DATA_PHYSICAL_PIN,
        "description": "I2S microphone data input.",
    },
    "i2s_amp_data": {
        "gpio": I2S_AMP_DATA_GPIO,
        "physical_pin": I2S_AMP_DATA_PHYSICAL_PIN,
        "description": "I2S amplifier data output.",
    },
    "button_1": {
        "gpio": BUTTON_1_GPIO,
        "physical_pin": BUTTON_1_PHYSICAL_PIN,
        "description": "Optional user button.",
    },
    "button_2": {
        "gpio": BUTTON_2_GPIO,
        "physical_pin": BUTTON_2_PHYSICAL_PIN,
        "description": "Optional user button.",
    },
}


I2C_DEVICES = {
    "imu_mpu6050": {
        "address": IMU_I2C_ADDR,
        "address_hex": hex(IMU_I2C_ADDR),
        "description": "MPU-6050 / GY-521 inertial measurement unit.",
    },
    "distance_vl53l0x": {
        "address": DISTANCE_I2C_ADDR,
        "address_hex": hex(DISTANCE_I2C_ADDR),
        "description": "Optional VL53L0X / VL53L1X distance sensor.",
    },
}


SERVO_DEVICES = {
    "servo_bus": {
        "port": SERVO_PORT,
        "baud": SERVO_BAUD,
        "ids": SERVO_IDS,
        "endianness": SERVO_WORD_ENDIANNESS,
        "description": "SCS0009 / SC09 half-duplex serial servo bus.",
    },
    "servo_1": {
        "id": 1,
        "role": "unmapped_leg_servo",
        "description": "First detected leg servo. Physical side must be verified.",
    },
    "servo_2": {
        "id": 2,
        "role": "unmapped_leg_servo",
        "description": "Second detected leg servo. Physical side must be verified.",
    },
}


def describe_pinout() -> str:
    """
    Return a human-readable pinout summary.
    """

    lines: list[str] = []

    lines.append(f"{PROJECT_NAME} pinout")
    lines.append("=" * (len(PROJECT_NAME) + 8))
    lines.append(f"Controller: {CONTROLLER_BOARD}")
    lines.append(f"GPIO numbering: {GPIO_NUMBERING}")
    lines.append(f"Pinout version: {PINOUT_VERSION}")
    lines.append("")

    lines.append("Power")
    lines.append("-----")
    lines.append(f"5 V physical pins: {PI_5V_PHYSICAL_PINS}")
    lines.append(f"3.3 V physical pins: {PI_3V3_PHYSICAL_PINS}")
    lines.append(f"GND physical pins: {PI_GND_PHYSICAL_PINS}")
    lines.append(f"Shared 5 V rail V0: {SHARED_5V_RAIL}")
    lines.append(f"Recommended boost output: {BOOST_OUTPUT_VOLTAGE} V")
    lines.append("")

    lines.append("I2C")
    lines.append("---")
    lines.append(f"SDA: GPIO{I2C_SDA_GPIO}, physical pin {I2C_SDA_PHYSICAL_PIN}")
    lines.append(f"SCL: GPIO{I2C_SCL_GPIO}, physical pin {I2C_SCL_PHYSICAL_PIN}")
    lines.append(f"IMU address: {hex(IMU_I2C_ADDR)}")
    lines.append(f"Optional distance address: {hex(DISTANCE_I2C_ADDR)}")
    lines.append("")

    lines.append("Servo bus")
    lines.append("---------")
    lines.append(f"Port: {SERVO_PORT}")
    lines.append(f"Baud: {SERVO_BAUD}")
    lines.append(f"TX: GPIO{SERVO_TX_GPIO}, physical pin {SERVO_TX_PHYSICAL_PIN}")
    lines.append(f"RX: GPIO{SERVO_RX_GPIO}, physical pin {SERVO_RX_PHYSICAL_PIN}")
    lines.append(f"Expected IDs: {SERVO_IDS}")
    lines.append(f"Encoder clamp: {ENCODER_MIN} to {ENCODER_MAX}")
    lines.append(f"Safe nudge: {SAFE_NUDGE}")
    lines.append(f"Word endianness: {SERVO_WORD_ENDIANNESS}")
    lines.append("")

    lines.append("LED ring")
    lines.append("--------")
    lines.append(f"Data: GPIO{LED_PIN}, physical pin {LED_PHYSICAL_PIN}")
    lines.append(f"Count: {LED_COUNT}")
    lines.append(f"Brightness: {LED_BRIGHTNESS}")
    lines.append("")

    lines.append("I2S audio")
    lines.append("---------")
    lines.append(f"BCLK: GPIO{I2S_BCLK_GPIO}, physical pin {I2S_BCLK_PHYSICAL_PIN}")
    lines.append(f"LRCLK: GPIO{I2S_LRCLK_GPIO}, physical pin {I2S_LRCLK_PHYSICAL_PIN}")
    lines.append(f"MIC data: GPIO{I2S_MIC_DATA_GPIO}, physical pin {I2S_MIC_DATA_PHYSICAL_PIN}")
    lines.append(f"AMP data: GPIO{I2S_AMP_DATA_GPIO}, physical pin {I2S_AMP_DATA_PHYSICAL_PIN}")
    lines.append(f"Audio device hint: {AUDIO_DEVICE}")
    lines.append("")

    lines.append("Camera")
    lines.append("------")
    lines.append(f"Interface: {CAMERA_INTERFACE}")
    lines.append(f"Ribbon: {CAMERA_RIBBON}")
    lines.append("")

    return "\n".join(lines)


def print_pinout() -> None:
    """
    Print the MicroBot Round V0 pinout summary.
    """

    print(describe_pinout())


if __name__ == "__main__":
    print_pinout()