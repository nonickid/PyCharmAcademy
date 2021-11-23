messages = dict({
    0: "Enter an equation",
    1: "Do you even know what numbers are? Stay focused!",
    2: "Yes ... an interesting math operation. You've slept through all classes, haven't you?",
    3: "Yeah... division by zero. Smart move...",
    4: "Do you want to store the result? (y / n):",
    5: "Do you want to continue calculations? (y / n):",
    6: " ... lazy",
    7: " ... very lazy",
    8: " ... very, very lazy",
    9: "You are",
    10: "Are you sure? It is only one digit! (y / n)",
    11: "Don't be silly! It's just one number! Add to the memory? (y / n)",
    12: "Last chance! Do you really want to embarrass yourself? (y / n)"
})

operators = dict({
    "+": "add", "-": "sub", "*": "mul", "/": "div"
})

operations = dict(
    add=lambda a, b: a + b,
    sub=lambda a, b: a - b,
    mul=lambda a, b: a * b,
    div=lambda a, b: a / b
)

memory = 0.0


def read_calc():
    print_msg(0)
    data_input = input()
    return data_input.split()


def store_result():
    print_msg(4)
    answer = input()
    return check_answer(answer)


def continue_calculation():
    print_msg(5)
    answer = input()
    return check_answer(answer)


def check(v1, v2, v3):
    msg = ""
    if is_one_digit(v1) and is_one_digit(v2):
        msg += messages.get(6)
    if (v1 == 1 or v2 == 1) and v3 == "*":
        msg += messages.get(7)
    if (v1 == 0 or v2 == 0) and v3 in "*+-":
        msg += messages.get(8)
    if msg:
        msg = messages.get(9) + msg
        print(msg)


def print_msg(index):
    print(messages.get(index))


def check_answer(answer):
    if answer == "y":
        return True
    return False


def confirm_is_digit(res, mem):
    msg_index = 10

    while True:
        print_msg(msg_index)
        answer = input()
        if check_answer(answer):
            if msg_index < 12:
                msg_index += 1
            else:
                return res
        else:
            return mem


def is_one_digit(v):
    return v.is_integer() and -10 < v < 10


while True:
    x, operator, y = read_calc()
    try:
        x = memory if x == 'M' else float(x)
        y = memory if y == 'M' else float(y)
        assert operator in list(operators.keys())
        check(x, y, operator)
        result = operations.get(operators.get(operator))(x, y)
        print(result)
        if store_result():
            if is_one_digit(result):
                memory = confirm_is_digit(result, memory)
            else:
                memory = result
        if not continue_calculation():
            break
    except ValueError:
        print(messages.get(1))
    except AssertionError:
        print(messages.get(2))
    except ZeroDivisionError:
        print(messages.get(3))
