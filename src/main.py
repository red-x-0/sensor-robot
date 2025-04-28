from machine import Pin, I2C
from time import sleep
from buzzer import Buzzer
from stepper import Stepper
from ultrasonic import HCSR04
import oled
import mpu6050

# I2C setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Initialize devices
mpu = mpu6050.accel(i2c)
oled_width = 128
oled_height = 64
oled = oled.SSD1306_I2C(oled_width, oled_height, i2c)

trigger_pin = 5
echo_pin = 18
ultrasonic = HCSR04(trigger_pin, echo_pin)

left_motor = Stepper([13])
right_motor = Stepper([19])

led = Pin(12, Pin.OUT)
button = Pin(27, Pin.IN, Pin.PULL_UP)
buzzer = Buzzer(15)

# --- Utility functions ---
def wait_button_press():
    while button.value() == 1:
        pass  # Block until button is pressed

def get_steps_from_distance(distance_cm):
    steps_per_cm = 200 / (2 * 3.1416 * 3)  # Precalculate steps per cm
    steps = int(distance_cm * steps_per_cm)
    return steps

# --- Main program ---
def main():
    while True:
        led.value(0)  # 2. Start by turning LED off

        oled.fill(0)  # 3. Clear OLED and show message
        oled.text("Press button", 15, 20)
        oled.text("to start", 27, 35)
        oled.show()

        wait_button_press()  # 4. Wait for button press

        led.value(1)  # Turn LED ON after button press

        buzzer.beep_once()  # 5. Beep once after press

        distance_cm = ultrasonic.get_distance_cm()  # 6. Read ultrasonic distance

        steps = get_steps_from_distance(distance_cm)  # 7. Convert distance to steps

        # 8. Show distance and steps on OLED
        oled.fill(0)
        oled.text("{:.2f}cm".format(distance_cm), 10, 20)
        oled.text("{} steps".format(steps), 10, 40)
        oled.show()
        sleep(1)

        reached = True  # 9. Assume we will reach

        # 10. Move steps
        for _ in range(steps):
            left_motor.move_one_step()
            right_motor.move_one_step()
            sleep(0.005)  # Small delay for stability

            # 12. After each step, read accelerometer
            values = mpu.get_values()
            y_axis = values["AcY"]

            # 13. Check tilt conditions
            if y_axis > 12000 or y_axis < -12000:
                reached = False  # 14. Mark not reached
                break  # Exit movement immediately

        if reached:
            # 15. Reached successfully
            oled.fill(0)
            oled.text("REACHED", 30, 30)
            oled.show()
            buzzer.beep_once()
        else:
            # 15. Tilt detected
            led.value(1)
            oled.fill(0)
            oled.text("TILTED", 30, 30)
            oled.show()
            for _ in range(3):
                buzzer.beep_once()
                sleep(0.2)

        sleep(2)  # 16. Wait 2 seconds for user to read

if __name__ == "__main__":
    main()
