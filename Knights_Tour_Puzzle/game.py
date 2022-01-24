
class Knight:
    def __init__(self):
        self.board = []
        self.ROWS = 0
        self.COLS = 0
        self.X_row = 0
        self.X_col = 0
        self.X_position = None
        self.counter = None
        self.cell = None
        self.size = None
        self.visits = 1
        self.moves = dict()
        self.path = dict()

    def start(self):
        self.COLS, self.ROWS = self.get_position("Enter your board dimensions: ", board=True)
        self.create_board()
        self.X_col, self.X_row = self.get_position("Enter the knight's starting position: ")
        self.X_position = self.COLS * self.X_row + self.X_col
        answer = self.play_or_solution()
        if answer == 'y':
            if self.find_solution(self.X_position, 1):
                self.moves = dict()
                self.play()
            else:
                print('No solution exists!')
        else:
            if self.find_solution(self.X_position, 1):
                self.update_all_positions(self.path)
                print("Here's the solution!")
                self.print_board()
            else:
                print('No solution exists!')

    def play(self):
        self.make_update()
        while True:
            self.X_col, self.X_row = self.get_position("Enter your next move: ", next_move=True)
            next_move = self.COLS * self.X_row + self.X_col
            self.move_knight(next_move)
            self.make_update()
            if self.end_game():
                break

    def update_path(self, pos, num):
        self.path[pos] = num

    def find_solution(self, pos, step):
        if step == self.size:
            self.update_path(pos, step)
            return True
        moves = self.can_move(pos)
        if not moves:
            return False
        self.update_path(pos, step)
        self.update_position(pos, 'X')
        while moves:
            move = moves.pop()
            self.update_position(pos, '*')
            result = self.find_solution(move, step + 1)
            if result:
                self.board[pos] = ['_'] * self.cell
                return True
            self.board[move] = ['_'] * self.cell
            self.update_position(pos, 'X')
        return False

    def move_knight(self, move):
        self.update_position(self.X_position, '*')
        self.X_position = move
        self.clear_old_entries(self.moves)
        self.moves = dict()
        self.visits += 1

    @staticmethod
    def play_or_solution():
        while True:
            try:
                answer = input('Do you want to try the puzzles? (y/n): ')
                assert answer.lower() == 'y' or answer.lower() == 'n'
            except AssertionError:
                print('Invalid input!')
            else:
                return answer.lower()

    def valid_move(self, row, col):
        if self.COLS * row + col in self.moves and self.not_visit(self.COLS * row + col) and \
                self.COLS * row + col != self.X_position:
            return True
        return False

    def get_position(self, msg, board=False, next_move=False):
        while True:
            try:
                col, row = input(msg).split()
                col = int(col) if board else int(col) - 1
                row = int(row) if board else int(row) - 1
                if (col <= 0 or row <= 0) and board:
                    raise ValueError
                if (col < 0 or row < 0) and not board:
                    raise ValueError
                if not board:
                    assert 0 <= col < self.COLS and 0 <= row < self.ROWS,\
                        'Invalid position!'
                if next_move:
                    assert self.valid_move(row, col), 'Invalid move!'
            except ValueError:
                print('Invalid dimensions!')
            except AssertionError as e:
                print(e, end=' ')
            else:
                return [col, row]

    def create_board(self):
        self.size = self.COLS * self.ROWS
        self.cell = len(str(self.size))
        self.counter = [str(num) for num in range(1, self.COLS + 1)]
        self.board = [['_'] * self.cell for _ in range(0, self.size + 1)]

    def make_update(self):
        self.update_position(self.X_position, 'X')
        self.possible_moves(self.X_position)
        self.update_all_positions(self.moves)
        self.print_board()

    def end_game(self):
        if self.moves and self.visits < self.size:
            return False
        if self.visits == self.size:
            print('What a great tour! Congratulations!')
        else:
            print('No more possible moves!')
            print(f'Your knight visited {self.visits} squares!')
        return True

    def print_line(self, cols=False):
        print(' ' * (self.cell - 1) + '-' * (self.COLS * (self.cell + 1) + 3))
        if cols:
            print(' ' * (self.cell + 2), end='')
            for col in self.counter:
                print(col, ' ' * (self.cell - 1), end='')
            print()

    def print_row(self, row, col):
        row = [''.join(cell) for cell in self.board[row:col]]
        return ' '.join(row)

    def print_board(self):
        self.print_line()
        self.get_board(0, self.COLS, 1)
        self.print_line(cols=True)

    def get_board(self, row, col, counter):
        align = len(str(self.ROWS))
        if col > self.size + 1:
            return
        self.get_board(row + self.COLS, col + self.COLS, counter + 1)
        print('{0:>{1}}'.format(counter, align) + '| ' + self.print_row(row, col), '|')

    def update_position(self, pos, value):
        if len(value) == self.cell:
            self.board[pos] = [v for v in value]
        else:
            self.board[pos] = [' ' for _ in range(self.cell)]
            self.board[pos][self.cell - 1] = value

    def update_all_positions(self, values):
        for key, value in values.items():
            self.update_position(key, str(value - 1 if values is self.moves else value))

    def clear_old_entries(self, values):
        for key in values.keys():
            if key == self.X_position:
                continue
            self.board[key] = ['_'] * self.cell

    def update_moves(self, pos):
        if pos == self.X_position:
            return
        if self.moves.get(pos):
            self.moves[pos] += 1
        else:
            self.moves[pos] = 1

    def not_visit(self, pos):
        return self.board[pos][self.cell - 1] != '*'

    def can_move(self, pos):
        possible_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2)]
        positions = []
        for row, move in possible_moves:
            y_pos = pos + self.COLS * row
            if y_pos < 0 or y_pos >= self.size:
                continue
            edge = y_pos % self.COLS
            if y_pos - move >= y_pos - edge and self.not_visit(y_pos - move):
                positions.append(y_pos - move)
                self.update_moves(pos)
            if y_pos + move < y_pos + self.COLS - edge and self.not_visit(y_pos + move):
                positions.append(y_pos + move)
                self.update_moves(pos)
        return positions

    def possible_moves(self, pos, depth=2):
        moves = self.can_move(pos)
        if depth - 1 == 0:
            return
        while moves:
            self.possible_moves(moves.pop(), depth - 1)


knight = Knight()
knight.start()


