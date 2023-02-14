# this file contains functions having to do with
# basic numerical calculations and order of operations
import re
from numpy import prod

REGEXS = {
    "power": r"-?\d+\.?\d?\^-?\d+\.?\d?",
    "prod": r"-?\d+\.?\d?[*\/]-?\d+\.?\d?",
    "sum": r"-?\d+\.?\d?[+-]+-?\d+\.?\d?",
    "signs": r"(?<=\d)[+*\/^-]"
}

# removes unnecessary negative signs from a number
def check_for_double_negative(num): 
    num = num.replace("+","")
    if num.count("-") % 2 == 0:
        return num.replace("-","")
    return f'-{num.replace("-","")}'

# converts to float and then sums, finds product, or args[0] to the power of args[1]
def _operation(mode="sum", *args):
    args = [float(i) for i in args]
    if mode == "sum": return sum(args)
    elif mode == "prod": return prod(args)
    return args[0] ** args[1]

# returns the main operation of an expression and its index if u want
def get_symbol(expr: str, return_sign_index: bool):
    operation = re.findall(REGEXS["signs"], expr)[0]
    if not return_sign_index: return operation

    # this var is necessary because without it, this func might confuse a minus sign with a negative number
    first_digit_index = expr.index(re.findall(r"\d", expr)[0])

    operation_index = expr.index(operation, first_digit_index)
    return (operation,operation_index)

def _basic_operations(expr: str, mode="prod"):

    # basically, don't delete this variable. I'm too stupid to explain what it is, but don't delete it.
    mode_change = 0
    if mode != "sum": mode_change = 1

    # finding every operation in the entire expression
    operations = re.findall(REGEXS[mode], expr)

    # solving each operation one by one until there are no operations left, ie, the operations list is empty.
    while operations != []:
        operation = operations[0]
        symbol = get_symbol(operation, True)    # determines if the operation is addition, subtraction, multiplication, or division
        number_on_right = operation[:symbol[1]]
        number_on_left = check_for_double_negative(operation[symbol[1]+mode_change:])

        # this is just saying that if we're doing division, change the number on the left to its reciprocal.
        if symbol[0] == "/": number_on_left = 1 / float(number_on_left)

        simplified_value = _operation(
            mode,
            number_on_right,
            number_on_left)
        expr = expr.replace(operation, str(simplified_value))
        operations = re.findall(REGEXS[mode], expr)
    return expr    

def exponentiation(base, power):
    return base ** power

def calc(expr: str):
    expr = _basic_operations(expr, "power")
    expr = _basic_operations(expr, "prod")
    expr = _basic_operations(expr, "sum")
    if re.search(r"[()]", expr): expr = calc(expr.replace("(","").replace(")",""))
    return expr