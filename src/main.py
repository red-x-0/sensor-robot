from machine import Pin
from buzzer import Buzzer

led = Pin(12, Pin.OUT)

button = Pin(27, Pin.IN, Pin.PULL_UP)

buzzerPin = 15
buzzer = Buzzer(buzzerPin)

def main():
  led.value(0)
  while True:
    pass

if __name__ == "__main__":
  main()