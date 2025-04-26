from machine import Pin # type: ignore
from time import sleep

class Stepper:
    def __init__(self, pins, microstep_mode=1):
        """
        Initialize the Stepper object.
        :param pins: List of pins, where the first pin is for STEP, the second for DIR,
                     and the next three (optional) are for MS1, MS2, MS3.
        :param microstep_mode: Microstepping mode (1 = full-step, 16 = sixteenth-step, etc.)
        """
        self.step_pin = Pin(pins[0], Pin.OUT)  # STEP pin
        self.dir_pin = Pin(pins[1], Pin.OUT)   # DIR pin
        
        # MS1, MS2, MS3 pins are optional, so we check if they're provided
        self.ms_pins = [Pin(pin, Pin.OUT) for pin in pins[2:5]] if len(pins) > 2 else []

        # Set microstepping mode
        self.set_microstepping(microstep_mode)
        
        # Default steps per revolution for a full step motor
        self.steps_per_revolution = 200  # Adjust according to your motor's specifications

    def set_microstepping(self, microstep_mode):
        """
        Set the microstepping mode using a dictionary to map mode to MS1, MS2, MS3 pin values.
        :param microstep_mode: Microstepping setting (1 = full-step, 16 = sixteenth-step, etc.)
        """
        if len(self.ms_pins) == 0:
            # If no microstepping pins are provided, use full step (default)
            return
        
        # Dictionary to map microstep mode to corresponding MS1, MS2, MS3 pin values
        microstep_map = {
            1: [0, 0, 0],  # Full-step
            2: [1, 0, 0],  # Half-step
            4: [0, 1, 0],  # Quarter-step
            8: [1, 1, 0],  # Eighth-step
            16: [1, 1, 1]  # Sixteenth-step
        }

        if microstep_mode not in microstep_map:
            raise ValueError("Invalid microstep mode. Must be 1, 2, 4, 8, or 16.")
        
        # Set MS1, MS2, MS3 pins based on the microstep mode
        ms_values = microstep_map[microstep_mode]
        for ms_pin, value in zip(self.ms_pins, ms_values):
            ms_pin.value(value)

        # Update the steps per revolution based on microstepping
        self.steps_per_revolution = 200 * (16 // microstep_mode)

    def step(self, steps, delay=0.001):
        """
        Move the motor a given number of steps.
        Positive steps for clockwise, negative for counter-clockwise.
        :param steps: Number of steps to move (positive or negative).
        :param delay: Delay between steps (adjust for speed).
        """
        # Set direction
        direction = 1 if steps > 0 else 0
        self.dir_pin.value(direction)

        # Send pulses to STEP pin
        for _ in range(abs(steps)):
            self.step_pin.on()
            sleep(delay / 2)  # Half of the delay for HIGH
            self.step_pin.off()
            sleep(delay / 2)  # Half of the delay for LOW

    def rotate(self, revolutions, delay=0.001):
        """
        Rotate the motor a specified number of revolutions.
        :param revolutions: Number of revolutions (positive or negative).
        :param delay: Delay between steps.
        """
        steps = int(revolutions * self.steps_per_revolution)
        self.step(steps, delay)