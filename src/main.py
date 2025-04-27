from machine import Pin
from time import sleep
from buzzer import Buzzer
from stepper import Stepper
from ultrasonic import HCSR04
from motor import MotorController

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

def main():
  led.value(0)
  while True:
    wait_button_press()
    print("Button pressed")
    sleep(1)

if __name__ == "__main__":
  main()