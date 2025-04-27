class MotorController:
    def __init__(self, left_motor, right_motor):
        self.left = left_motor
        self.right = right_motor
        self.steps_per_cm = 200 / (2 * 3.1416 * 3)  # precalculate for fast access

    def move_cm(self, distance_cm, delay=0.001):
        """Move the robot forward or backward by a distance in cm."""
        steps = int(distance_cm * self.steps_per_cm)

        for _ in range(abs(steps)):
            self.left.move_one_step(delay)
            self.right.move_one_step(delay)
