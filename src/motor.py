class MotorController:
    def __init__(self, left_motor, right_motor):
        self.left = left_motor
        self.right = right_motor

    def move_steps(self, steps, delay=0.001):
        """Move the robot forward."""

        for _ in range(abs(steps)):
            self.left.move_one_step(delay)
            self.right.move_one_step(delay)
