import random
from collections import Counter


class DominoGame:
    def __init__(self):
        self.player = False
        self.computer = False
        self.domino_set = set()
        self.stock_pairs = set()
        self.player_pairs = set()
        self.computer_pairs = set()
        self.snake = None
        self.snake_lst = []

    def start(self):
        self._generate()
        self._update_snake(self.snake, 1)
        while True:
            self._print()
            if self._print_status():
                break
            num, pair = self._get_player_input()
            if num != 0:
                self._update_snake(pair, num)
                self._remove_pairs(pair)
            self._switch_player()

    def _print(self):
        print('=' * 70)
        print('Stock size:', self._get_size(self.stock_pairs))
        print('Computer pieces:', self._get_size(self.computer_pairs), end='\n\n')
        self._get_snake_status()
        print('Your pieces:')
        self._get_player_pairs()

    def _print_status(self):
        if not self._get_size(self.player_pairs):
            print('Status: The game is over. You won!')
            return True
        if not self._get_size(self.computer_pairs):
            print('Status: The game is over. The computer won!')
            return True
        if self.snake_lst[0][0] == self.snake_lst[-1][1] and self._get_snake_size() >= 8:
            if self._check_draw():
                print('Status: The game is over. It\'s a draw!')
                return True
        if self.computer:
            print('Status: Computer is about to make a move. Press Enter to continue...')
        else:
            print("Status: It's your turn to make a move. Enter your command.")
        return False

    def _validate_player_input(self, num):
        pairs = self.computer_pairs if self.computer else self.player_pairs
        if num == 0:
            if self._if_stock_empty():
                return 0
            pair = random.choice(list(self.stock_pairs))
            pairs.add(pair)
            self.stock_pairs.remove(pair)
        else:
            pair = tuple(pairs)[abs(num) - 1]

        return pair

    def _validate_match(self, pair, num):
        if num > 0:
            if pair[0] == self.snake_lst[-1][1]:
                return pair
            elif pair[1] == self.snake_lst[-1][1]:
                return pair[1], pair[0]
        else:
            if pair[1] == self.snake_lst[0][0]:
                return pair
            elif pair[0] == self.snake_lst[0][0]:
                return pair[1], pair[0]

        return False

    def _ai_move(self):
        pairs = list(self.computer_pairs) + self.snake_lst
        numbers_count = Counter(num for pair in pairs for num in pair)
        scores = dict()

        for pair in self.computer_pairs:
            scores[pair] = numbers_count[pair[0]] + numbers_count[pair[1]]

        for pair in sorted(scores, key=scores.get, reverse=True):
            swapped = self._validate_match(pair, -1)
            if swapped:
                self._is_pair_swapped(pair, swapped)
                return -1, swapped
            swapped = self._validate_match(pair, 1)
            if swapped:
                self._is_pair_swapped(pair, swapped)
                return 1, swapped

        pair = self._validate_player_input(0)
        return 0, pair

    def _get_player_input(self):
        if self.computer:
            input('')
            return self._ai_move()

        while True:
            try:
                choice = int(input('> '))
                assert abs(choice) <= len(self.player_pairs)
            except (ValueError, AssertionError):
                print('Invalid input. Please try again.')
                continue

            pair = self._validate_player_input(choice)
            if choice == 0:
                return 0, pair
            swapped = self._validate_match(pair, choice)
            if not swapped:
                print('Illegal move. Please try again')
                continue
            break

        self._is_pair_swapped(pair, swapped)
        return choice, swapped

    def _is_pair_swapped(self, pair, swapped):
        if pair != swapped:
            if self.computer:
                self.computer_pairs.remove(pair)
                self.computer_pairs.add(swapped)
            else:
                self.player_pairs.remove(pair)
                self.player_pairs.add(swapped)

    def _if_stock_empty(self):
        return not self.stock_pairs

    def _generate(self):
        self._get_domino_set()
        self._set_stock_pairs()
        self._set_computer_pairs()
        self._set_player_pairs()
        self.snake = self._get_snake()
        self._set_starting_player()

    def _get_domino_set(self):
        nums = []
        for n in range(0, 7):
            for m in range(0, 7):
                if m not in nums:
                    self.domino_set.add((n, m))
            nums.append(n)

    def _switch_player(self):
        if self.player:
            self.player = False
            self.computer = True
        else:
            self.computer = False
            self.player = True

    def _set_stock_pairs(self):
        self.stock_pairs = set(tuple(n) for n in random.sample(list(self.domino_set), 14))

    def _set_computer_pairs(self):
        pairs = self.domino_set - self.stock_pairs
        self.computer_pairs = set(tuple(n) for n in random.sample(list(pairs), 7))

    def _set_player_pairs(self):
        self.player_pairs = self.domino_set - self.stock_pairs - self.computer_pairs

    def _remove_pairs(self, pair):
        if self.computer:
            self.computer_pairs.remove(pair)
        else:
            self.player_pairs.remove(pair)

    def _update_snake(self, pair, index=None):
        if index > 0:
            self.snake_lst.append(list(pair))
        else:
            self.snake_lst.insert(0, list(pair))

    def _get_player_pairs(self):
        for i, pair in enumerate(self.player_pairs, start=1):
            print(f'{i}:{list(pair)}')
        print()

    def _get_snake(self):
        pairs = self.computer_pairs.union(self.player_pairs)
        return max(pair for pair in pairs if pair[0] == pair[1])

    def _set_starting_player(self):
        if self.snake in self.computer_pairs:
            self.computer = False
            self.player = True
            self.computer_pairs.remove(self.snake)
        else:
            self.player = False
            self.computer = True
            self.player_pairs.remove(self.snake)

    def _get_snake_status(self):
        if len(self.snake_lst) > 6:
            for pair in self.snake_lst[0:3]:
                print(pair, end='')
            print('...', end='')
            for pair in self.snake_lst[-3:]:
                print(pair, end='')
        else:
            for pair in self.snake_lst:
                print(pair, end='')
        print(end='\n\n')

    def _get_snake_size(self):
        return len(self.snake_lst)

    def _check_draw(self):
        counter = 0
        for pair in self.snake_lst:
            if self.snake_lst[0][0] == pair[0]:
                counter += 1
            if self.snake_lst[0][0] == pair[1]:
                counter += 1
        if counter >= 8:
            return True
        return False

    @staticmethod
    def _get_size(pairs):
        return len(pairs)


game = DominoGame()
game.start()
