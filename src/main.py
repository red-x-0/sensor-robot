from machine import Pin, I2C
from time import sleep
from buzzer import Buzzer
from stepper import Stepper
from ultrasonic import HCSR04
from motor import MotorController
import oled

# I2C setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# OLED setup
oled_width = 128
oled_height = 64
oled = oled.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text("loading...", 22, 20)
oled.show()

trigger_pin=5
echo_pin=18

ultrasonic = HCSR04(trigger_pin, echo_pin)

left_motor = Stepper([13])
right_motor = Stepper([19])
motor_controller = MotorController(left_motor, right_motor)

led = Pin(12, Pin.OUT)

button = Pin(27, Pin.IN, Pin.PULL_UP)

buzzerPin = 15
buzzer = Buzzer(buzzerPin)

def wait_button_press():
  while button.value() == 1:
    pass
  
def get_steps_from_distance(distance_cm):
  steps_per_cm = 200 / (2 * 3.1416 * 3)  # precalculate for fast access
  steps = int(distance_cm * steps_per_cm)
  return steps

def main():
  led.value(0)
  while True:
    oled.fill(0)
    oled.text("Press button", 15, 20)
    oled.text("to start", 27, 35)
    oled.show()

    wait_button_press()
    print("Button pressed")

    buzzer.beep_once()

    distance_cm = ultrasonic.get_distance_cm()
    print(distance_cm)
    
    oled.fill(0)
    oled.text("Moving {:.2f}cm".format(distance_cm), 7, 20)
    oled.show()

    steps_to_move = get_steps_from_distance(distance_cm)

    motor_controller.move_steps(steps_to_move, 0.005)

    buzzer.beep_once()

    oled.fill(0)
    oled.text("Reached", 20, 20)
    oled.show()
    sleep(0.5)

if __name__ == "__main__":
  main()