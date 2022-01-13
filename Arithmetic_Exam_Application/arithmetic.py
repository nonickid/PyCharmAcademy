import random

math = dict(
    {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '**': lambda x: x ** 2

    }
)

levels = dict(
    {
        1: '1 - simple operations with numbers 2-9',
        2: '2 - integral squares of 11-29'
    }
)


def generate_math_task(x, y):
    return random.randint(x, y),\
            random.randint(x, y), \
            random.choice('+-*')


def generate_square_task(x, y):
    return random.randint(x, y)


def print_msg():
    print('Which level do you want? Enter a number:')
    print(levels.get(1))
    print(levels.get(2))


def save_result(student, level, correct, tasks):
    try:
        with open('results.txt', 'a') as fn:
            record = f'{student}: {correct}/{tasks} in level {level} {levels.get(level)}.'
            fn.write(record)
    except IOError:
        print('Cannot save result in file results.txt')
    else:
        print('The results are saved in "results.txt".')


while True:
    print_msg()
    try:
        difficult = int(input(''))
        assert 1 <= difficult <= 2
    except (ValueError, AssertionError):
        print('Incorrect format.')
    else:
        break


num_of_task = 5
correct_answer = 0
attempt = 0

while num_of_task != attempt:
    if difficult == 1:
        a, b, operator = generate_math_task(2, 9)
        print(f'{a} {operator} {b}')
    else:
        a = generate_square_task(11, 29)
        print(a)

    while True:
        try:
            result = int(input(''))
            break
        except ValueError:
            print('Incorrect format')

    if difficult == 1 and result == math[operator](a, b):
        print('Right!')
        correct_answer += 1
    elif difficult == 2 and result == math['**'](a):
        print('Right!')
        correct_answer += 1
    else:
        print('Wrong')
    attempt += 1

print(f'Your mark is {correct_answer}/{num_of_task}. Would you like to save the result? Enter yes or no.')
save = input()

if save in 'Yy' or save.lower() == 'yes':
    name = input('What is your name?')
    save_result(name, difficult, correct_answer, num_of_task)


