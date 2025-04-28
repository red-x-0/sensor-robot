from time import sleep
from machine import PWM, Pin

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        self.buzzer = PWM(Pin(pin, Pin.OUT))
        self.buzzer.duty(0)

    def beep_once(self):
        self.buzzer.freq(1047)
        self.buzzer.duty(50)
        sleep(0.2)
        self.buzzer.duty(0)