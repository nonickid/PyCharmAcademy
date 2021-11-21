from random import choice


def get_num_of_friends():
    print('Enter the number of friends joining (including you):')
    return int(input())


def get_friends(num):
    print('Enter the name of every friend (including you), each on a new line:')
    f_dict = dict()
    while num:
        f_dict[input('')] = 0
        num -= 1
    return f_dict


def get_bill():
    print('Enter the total bill:')
    return int(input())


def split_bill(bill, no_of_split):
    return round(bill / no_of_split, 2)


def update_dict(f_dict, lucky, bill):
    for key in f_dict.keys():
        if key != lucky:
            f_dict[key] = bill


def get_lucky(f_list):
    print('Do you want to use the "Who is lucky?" feature? Write Yes/No')
    opt = input()
    if opt == 'Yes':
        lucky = choice(list(f_list.keys()))
        print(lucky, 'is the lucky one!')
        return lucky
    else:
        print('No one is going to be lucky')
    return None


try:
    no_of_friends = get_num_of_friends()
    assert no_of_friends > 0
    friends = get_friends(no_of_friends)
    total_bill = get_bill()
    lucky_friend = get_lucky(friends)
    no_of_friends = no_of_friends - 1 if lucky_friend else no_of_friends
    bill_split = split_bill(total_bill, no_of_friends)
    update_dict(friends, lucky_friend, bill_split)
    print(friends)
except ValueError:
    print('Wrong input value')
except AssertionError:
    print('No one is joining for the party')

