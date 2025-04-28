from machine import Pin  # type: ignore
from time import sleep

class Stepper:
    def __init__(self, pins, microstep_mode=1):
        """
        Initialize the Stepper object.
        :param pins: List of pins. First pin = STEP, second (optional) = DIR,
                     next three (optional) = MS1, MS2, MS3.
        :param microstep_mode: Microstepping mode (1 = full-step, 16 = sixteenth-step, etc.)
        """
        self.step_pin = Pin(pins[0], Pin.OUT)  # STEP pin
        self.dir_pin = Pin(pins[1], Pin.OUT) if len(pins) > 1 else None  # DIR pin (optional)
        
        # MS1, MS2, MS3 pins are optional
        self.ms_pins = [Pin(pin, Pin.OUT) for pin in pins[2:5]] if len(pins) > 4 else []

        # Set microstepping mode
        self.set_microstepping(microstep_mode)
        
        # Default steps per revolution for a full-step motor
        self.steps_per_revolution = 200

    def set_microstepping(self, microstep_mode):
        """
        Configure microstepping mode based on MS1, MS2, MS3 settings.
        """
        if not self.ms_pins:
            # No microstepping control available
            return
        
        microstep_map = {
            1: [0, 0, 0],   # Full-step
            2: [1, 0, 0],   # Half-step
            4: [0, 1, 0],   # Quarter-step
            8: [1, 1, 0],   # Eighth-step
            16: [1, 1, 1]   # Sixteenth-step
        }

        if microstep_mode not in microstep_map:
            raise ValueError("Invalid microstep mode. Must be 1, 2, 4, 8, or 16.")
        
        ms_values = microstep_map[microstep_mode]
        for ms_pin, value in zip(self.ms_pins, ms_values):
            ms_pin.value(value)

        self.steps_per_revolution = 200 * (16 // microstep_mode)

    def move_one_step(self, delay=0.001):
        """
        Move the motor exactly one step.
        :param delay: Time between ON and OFF phases.
        """
        self.step_pin.on()
        sleep(delay / 2)
        self.step_pin.off()
        sleep(delay / 2)

    def step(self, steps, delay=0.001):
        """
        Move the motor a given number of steps.
        Positive for one direction, negative for the other.
        :param steps: Number of steps (can be negative).
        :param delay: Delay between steps.
        """
        if self.dir_pin:
            # Set direction only if dir_pin exists
            direction = 1 if steps > 0 else 0
            self.dir_pin.value(direction)

        for _ in range(abs(steps)):
            self.move_one_step(delay)

    def rotate(self, revolutions, delay=0.001):
        """
        Rotate motor a given number of revolutions.
        :param revolutions: Number of revolutions (can be negative).
        :param delay: Delay between steps.
        """
        steps = int(revolutions * self.steps_per_revolution)
        self.step(steps, delay)
    
    def stop(self):
        """
        Stop motor
        """
        self.step_pin.off()