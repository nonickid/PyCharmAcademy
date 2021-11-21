class CoffeeMachine(object):
    def __init__(self):
        self.amount = 550
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9

        self.action_choices = {"buy": self.buy_coffee, "fill": self.update_fill,
                               "take": self.take_money, "exit": self.exit_program,
                               "remaining": self.status}

    def _change_amount(self, amount):
        self.amount = amount

    def status(self):
        return f'''
The coffee machine has:
{self.water} of water
{self.milk} of milk
{self.beans} of coffee beans
{self.cups} of coffee cups
{self.amount} of money
'''

    @staticmethod
    def print_coffee_menu():
        print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        coffee_type = input('> ')
        coffee_type = coffee_type.strip('> ')
        return coffee_type

    def buy_coffee(self, coffee_type):
        if coffee_type == 'back':
            return

        coffee_type = int(coffee_type)
        resources = self.check_resources(coffee_type)
        if resources >= 1:
            msg = 'I have enough resources, making you a coffee!'
        else:
            return 'Sorry, not enough resources'
        if coffee_type == 1:
            self.update_buy(water=250, beans=16, cups=1, cost=4)
        if coffee_type == 2:
            self.update_buy(water=350, milk=75, beans=20, cups=1, cost=7)
        if coffee_type == 3:
            self.update_buy(water=200, milk=100, beans=12, cups=1, cost=6)

        return msg

    def check_resources(self, coffee_type):
        if coffee_type == 1:
            return int(min(self.water // 250, self.beans // 16, self.cups // 1))
        if coffee_type == 2:
            return int(min(self.water // 350, self.milk // 75, self.beans // 20, self.cups // 1))
        if coffee_type == 3:
            return int(min(self.water // 200, self.milk // 100, self.beans // 12, self.cups // 1))

    def update_buy(self, water=0, milk=0, beans=0, cups=0, cost=0):
        self.water -= water
        self.milk -= milk
        self.beans -= beans
        self.cups -= cups
        self.amount += cost

    @staticmethod
    def print_fill_menu():
        print('Write how many ml of water do you want to add: ')
        water = int(input('> ').strip('> '))
        print('Write how many ml of milk do you want to add: ')
        milk = int(input('> ').strip('> '))
        print('Write how many grams of coffee beans do you want to add: ')
        beans = int(input('> ').strip('> '))
        print('Write how many disposable cups of coffee do you want to add: ')
        cups = int(input('> ').strip('> '))

        return water, milk, beans, cups

    def update_fill(self, water=0, milk=0, beans=0, cups=0):
        self.water += water
        self.milk += milk
        self.beans += beans
        self.cups += cups

    def take_money(self):
        msg = f'I gave you ${self.amount}'
        self._change_amount(0)
        return msg

    @staticmethod
    def exit_program():
        return 'exit'

    def commands(self, cmd):
        if cmd == 'remaining':
            return self.status()
        elif cmd == 'buy':
            coffee_type = self.print_coffee_menu()
            return self.action_choices[cmd](coffee_type)
        elif cmd == 'fill':
            water, milk, beans, cups = self.print_fill_menu()
            self.action_choices[cmd](water=water, milk=milk, beans=beans, cups=cups)
        elif cmd == 'take':
            return self.action_choices[cmd]()
        elif cmd == 'exit':
            return self.action_choices[cmd]()

    def start(self):
        while True:
            print('Write action (buy, fill, take, remaining, exit):')
            cmd = input('> ')
            cmd = cmd.strip('> ')

            if cmd in self.action_choices:
                result = self.commands(cmd)
            else:
                print('Wrong choose!')
                continue

            if result == 'exit':
                break
            if result is not None:
                print(result)


coffee = CoffeeMachine()
coffee.start()
