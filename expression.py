# Defines the Expression class, an expression 
# being one side of a mathematical equation.

class Expression:

    def __init__(self, expr: str, *variables):
        self.expr = expr
        self.variables = variables
