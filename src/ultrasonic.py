from machine import Pin, time_pulse_us
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trig_pin = Pin(trigger_pin, Pin.OUT)
        self.echo_pin = Pin(echo_pin, Pin.IN)

        self.trig_pin.value(0)

    def trigger(self):
        self.trig_pin.value(0)
        time.sleep_us(2)

        self.trig_pin.value(1)
        time.sleep_us(10)

        self.trig_pin.value(0)

        # measure the duration of the echo pulse
        duration_us = time_pulse_us(self.echo_pin, 1)

        return duration_us

    def get_distance_mm(self):
        duration_us = self.trigger()
        # calculate the distance in millimeters
        distance_mm = duration_us / 5.8
        return distance_mm

    def get_distance_cm(self):
        duration_us = self.trigger()
        # calculate the distance based on the duration
        distance_cm = duration_us / 58.0
        return distance_cm