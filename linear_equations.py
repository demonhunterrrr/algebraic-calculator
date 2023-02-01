from sys import argv

class LinearEquation:
    def __init__(self, left_side, right_side):
        self.left_side = left_side
        self.right_side = right_side
        self.equation = f"{left_side} = {right_side}"