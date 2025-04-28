"""
Sensor Robot Project
--------------------
A MicroPython project using ESP32 that integrates ultrasonic sensing, 
stepper motor control, tilt detection via accelerometer, and OLED feedback.

Modules Used:
- Pin, I2C (machine)
- time
- buzzer, stepper, ultrasonic, oled, mpu6050 (custom classes)

Main Features:
- Start by button press
- Measure distance and move accordingly
- Detect tilt and handle emergency stop
- Provide visual and audio feedback
"""

from machine import Pin, I2C
from time import sleep
from buzzer import Buzzer
from stepper import Stepper
from ultrasonic import HCSR04
import oled
import mpu6050

# --- I2C setup for OLED and Accelerometer ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# --- Initialize I2C devices ---
mpu = mpu6050.accel(i2c)  # MPU6050 Accelerometer instance
oled_width = 128
oled_height = 64
oled = oled.SSD1306_I2C(oled_width, oled_height, i2c)  # OLED Display instance

# --- Initialize non-I2C devices ---
trigger_pin = 5
echo_pin = 18
ultrasonic = HCSR04(trigger_pin, echo_pin)  # Ultrasonic Distance Sensor

left_motor = Stepper([13])   # Left stepper motor (STEP pin D13)
right_motor = Stepper([19])  # Right stepper motor (STEP pin D19)

led = Pin(12, Pin.OUT)               # Status LED
button = Pin(27, Pin.IN, Pin.PULL_UP) # Start button with pull-up resistor
buzzer = Buzzer(15)                  # Buzzer for audio feedback

# --- Utility Functions ---
def wait_button_press():
    """Block execution until the button is pressed."""
    while button.value() == 1:
        pass  # Busy-wait loop

def get_steps_from_distance(distance_cm):
    """Convert distance in centimeters to number of steps."""
    steps_per_cm = 200 / (2 * 3.1416 * 3)  # Steps per cm based on motor configuration
    steps = int(distance_cm * steps_per_cm)
    return steps

# --- Main Robot Behavior ---
def main():
    while True:
        led.value(0)  # Turn LED off at the start of each cycle

        # Display initial message prompting for button press
        oled.fill(0)
        oled.text("Press button", 15, 20)
        oled.text("to start", 27, 35)
        oled.show()

        wait_button_press()  # Block until user presses the button

        led.value(1)  # Turn LED on to indicate activity

        buzzer.beep_once()  # Single beep after button press

        # Read distance from ultrasonic sensor
        distance_cm = ultrasonic.get_distance_cm()

        # Calculate equivalent steps based on distance
        steps = get_steps_from_distance(distance_cm)

        # Display distance and calculated steps on OLED
        oled.fill(0)
        oled.text("{:.2f}cm".format(distance_cm), 10, 20)
        oled.text("{} steps".format(steps), 10, 40)
        oled.show()
        sleep(1)  # Small delay for user to read

        reached = True  # Assume target will be reached unless tilt occurs

        # Move both motors the calculated number of steps
        for _ in range(steps):
            left_motor.move_one_step()
            right_motor.move_one_step()
            sleep(0.005)  # Small delay for motor stability

            # Check tilt after each step using accelerometer
            values = mpu.get_values()
            y_axis = values["AcY"]

            # If tilt exceeds threshold, stop movement
            if y_axis > 12000 or y_axis < -12000:
                reached = False  # Mark as not reaching the goal
                break  # Exit the motor movement loop early

        # Display appropriate message based on whether tilt was detected
        if reached:
            oled.fill(0)
            oled.text("REACHED", 30, 30)
            oled.show()
            buzzer.beep_once()  # Confirm success with one beep
        else:
            led.value(1)  # Ensure LED is ON to indicate error
            oled.fill(0)
            oled.text("TILTED", 30, 30)
            oled.show()
            # Beep three times to indicate error
            for _ in range(3):
                buzzer.beep_once()
                sleep(0.2)

        sleep(2)  # Pause to allow user to read final status

# --- Run the Main Program ---
if __name__ == "__main__":
    main()
