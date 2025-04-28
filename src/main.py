from machine import Pin, I2C
from time import sleep
from buzzer import Buzzer
from stepper import Stepper
from ultrasonic import HCSR04
from motor import MotorController
from oled import SSD1306_I2C

# I2C setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# OLED setup
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

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
    wait_button_press()
    print("Button pressed")
    
    distance_cm = ultrasonic.get_distance_cm()
    print(distance_cm)
    
    steps_to_move = get_steps_from_distance(distance_cm)

    motor_controller.move_cm(steps_to_move, 0.005)

if __name__ == "__main__":
  main()