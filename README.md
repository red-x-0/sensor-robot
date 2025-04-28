# 🚀 Sensor Robot Project

<p align="center">
  <img src="https://img.shields.io/badge/MicroPython-Enabled-blue.svg" alt="MicroPython Badge">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License Badge">
  <img src="https://img.shields.io/badge/Platform-Wokwi-ff69b4.svg" alt="Wokwi Badge">
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen.svg" alt="Project Status Badge">
</p>

---

## 📖 Overview
This project is a **sensor-driven robot** built using an **ESP32** and **MicroPython**.  
It integrates **distance sensing**, **stepper motor movement**, **tilt detection**, and **user feedback** via a **buzzer, LED, and OLED display**.

---

## 🛠 Hardware Components

| Component         | Pin Connections                 |
| ----------------- | -------------------------------- |
| LED               | D12 (Output)                     |
| Button            | D27 (Input, Pull-Up enabled)      |
| Buzzer            | D15 (Output via Buzzer class)     |
| Ultrasonic Sensor | Trigger: D5, Echo: D18            |
| Left Stepper      | STEP Pin: D13 (A4988 Driver)      |
| Right Stepper     | STEP Pin: D19 (A4988 Driver)      |
| OLED Display      | I2C (SCL: D22, SDA: D21)          |
| Accelerometer     | I2C (SCL: D22, SDA: D21)          |

---

## 🧠 Project Behavior

| Action                             | Result |
| ----------------------------------- | ------ |
| Startup                            | Displays "Press button to start" |
| Button Press                       | Buzzer beeps once, starts distance measurement |
| Measures Distance                  | OLED displays distance and calculated steps |
| Drives Motors                      | Moves robot corresponding to the measured distance |
| Tilt Detected While Driving        | Stops immediately, lights LED, beeps 3 times, displays "TILTED" |
| Successfully Reached Destination   | Buzzer beeps once, displays "REACHED" |

---

## 🧩 Software Organization

| File            | Purpose |
| --------------- | ------- |
| `main.py`       | Main control logic for the robot |
| `buzzer.py`     | Handles buzzer beeping functions |
| `ultrasonic.py` | Reads distance from ultrasonic sensor |
| `stepper.py`    | Controls stepper motor movement |
| `oled.py`       | Manages text display on the OLED screen |
| `mpu6050.py`    | Reads accelerometer values (AcY axis) |

---

## 📦 Getting Started

> ⚡ **How to run this project:**

1. Go to [Wokwi Simulator](https://wokwi.com/).
2. Create a new ESP32 project.
3. **Upload all source files** (`main.py`, `buzzer.py`, `ultrasonic.py`, `stepper.py`, `oled.py`, `mpu6050.py`) into the Wokwi project.
4. Set up the virtual components according to the **Hardware Components** table above.
5. Click **Start Simulation** — and you're good to go!

> **Note:**  
Make sure the filenames match exactly! Wokwi depends on proper file naming for imports to work correctly.

---

## 🎥 Demo

### 📸 Image Preview
 
![Sensor Robot Preview](image.png)

### 🎮 Wokwi Simulation
  
[🔗 Click here to view the live simulation](https://wokwi.com/projects/429302038745236481)

---

## 🔗 Useful Links

- [ESP32 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)
- [HC-SR04 Ultrasonic Sensor Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [A4988 Stepper Motor Driver Datasheet](https://www.pololu.com/file/download/a4988_DMOS_microstepping_driver_with_translator.pdf?file_id=0J450)
- [MPU6050 Accelerometer Datasheet](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
- [MicroPython Documentation](https://docs.micropython.org/)

---

## 📈 Technical Details

- **Microcontroller**: ESP32 Dev Module
- **Programming Language**: MicroPython
- **Distance Calculation**: Based on ultrasonic pulse timing
- **Step Calibration**: 10 steps ≈ 1 cm
- **Tilt Detection Threshold**: Accelerometer AcY axis > 12000 or < -12000
- **Buzzer Notifications**:
  - 1 short beep on start
  - 3 short beeps on tilt detection
  - 1 short beep on successful movement

---

## 👨‍💻 Author

| Field       | Details |
| ----------- | ------- |
| **Name**    | Sief Ali Sayed Said |
| **GitHub**  | [github.com/red-x-0](https://github.com/red-x-0) |
| **Email**   | 463688431@cairo5.moe.edu.eg |

---

## 📜 License

### MIT License

