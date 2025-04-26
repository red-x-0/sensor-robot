from machine import Pin
from time import sleep
from buzzer import Buzzer

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