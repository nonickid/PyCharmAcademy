formats = ('plain', 'bold', 'italic', 'header', 'link', 'inline-code',
           'ordered-list', 'unordered-list', 'new-line')

commands = ('!help', '!done')


formatted_text = ''''''


def helper():
    print('Available formatters: ', ' '.join(formats))
    print('Special commands: ', ' '.join(commands))


def header():
    while True:
        try:
            level = int(input('Level: '))
            assert 1 <= level <= 6
            text = input('Text: ')
        except (ValueError, AssertionError):
            print('The level should be within the range of 1 to 6')
            continue
        else:
            break

    return '#' * level + ' ' + text + new_line()


def plain():
    text = input('Text: ')
    return text


def link():
    while True:
        try:
            label = input('Label: ')
            url = input('URL: ')
        except ValueError:
            pass
        else:
            break

    return f'[{label}]({url})'


def inline_code():
    text = input('Text: ')
    return f'`{text}`'


def bold():
    text = input('Text: ')
    return f'**{text}**'


def italic():
    text = input('Text: ')
    return f'*{text}*'


def new_line():
    return '\n'


def create_list(ordered=False):
    text = ''
    while True:
        try:
            num_of_rows = int(input('Number of rows:'))
            assert num_of_rows > 0
        except ValueError:
            print('Only numbers are allowed')
            continue
        except AssertionError:
            print('The number of rows should be greater than zero')
            continue
        else:
            break

    for num in range(num_of_rows):
        row = input(f'Row #{num + 1}: ')
        if ordered:
            text += f'{num + 1}. ' + row + new_line()
        else:
            text += '* ' + row + new_line()

    return text


def formatter(format_type, text):
    if format_type == 'ordered-list':
        text += format_funcs.get(format_type)(ordered=True)
    else:
        text += format_funcs.get(format_type)()
    return text


def save(text):
    with open('output.md', 'w') as fn:
        fn.write(text)


format_funcs = dict(
        {
            'header': header,
            'plain': plain,
            'link': link,
            'inline-code': inline_code,
            'bold': bold,
            'italic': italic,
            'new-line': new_line,
            'ordered-list': create_list,
            'unordered-list': create_list
        }
    )


while True:
    cmd = input('Choose a formatter: ')
    if cmd == '!help':
        helper()
    elif cmd == '!done':
        save(formatted_text)
        break
    elif cmd in formats:
        formatted_text = formatter(cmd, formatted_text)
        print(formatted_text)
    else:
        print('Unknown formatting type or command')


