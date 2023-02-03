class Board:
    def __init__(self):
        """
        empty *
        red X
        black O
        """
        self.height = 6
        self.width = 7
        self.slots = [['*'] * self.width for row in range(self.height)]
        self.last_move_board = None

    def __repr__(self):
        board = ''

        for row in range(self.height):
            for col in range(self.width):
                board += self.slots[row][col] + ' '
            board += '\n'

        for col in range(self.width):
            board += f"{col + 1} "
        return board

    def last_move(self):
        """
        return last move
        """
        return self.last_move_board

    def can_add_to(self, column):
        """
        check if column is full
        """
        if column < 1 or column > self.width:
            return False
        if self.slots[0][column - 1] != '*':
            return False
        return True

    def getMoves(self):
        """
        return list of columns available to move
        """
        moves = []
        for col in range(1, self.width + 1):
            if self.can_add_to(col):
                moves.append(col)
        return moves

    def add_move(self, move, column):
        """
        add move to column
        """
        if move != 'X' and move != 'O':
            return False
        if column < 1 or column > self.width:
            return False
        if self.slots[0][column - 1] != '*':
            return False
        for row in range(self.height):
            if row + 1 == self.height and self.slots[row][column - 1] == '*':
                self.slots[row][column - 1] = move
                self.last_move_board = column - 1
                break
            if self.slots[row][column - 1] == '*' and self.slots[row + 1][column - 1] != '*':
                self.slots[row][column - 1] = move
                self.last_move_board = column - 1
                break
        return True

    def is_full(self):
        """
        check if board is full
        """
        for row in range(self.height):
            for col in range(self.width):
                if self.slots[row][col] == '*':
                    return False
        return True

    def clear(self):
        """
        clear board
        """
        self.slots = [['*'] * self.width for row in range(self.height)]

    def check_win(self, move, column):
        """
        check if move is a win
        """
        if self.check_horizontal_win(move, column) or self.check_vertical_win(move, column) or self.is_up_diagonal_win(move) or self.is_down_diagonal_win(move):
            return True
        return False

    def check_horizontal_win(self, move, column):
        """
        check if move is a horizontal win
        """
        for row in range(self.height):
            if self.slots[row][column - 1] == move:
                for col in range(3, -1, -1):
                    if self.width < column + col or column + col - 4 < 0:
                        break
                    if self.slots[row][column + col - 1] == move and self.slots[row][column + col - 2] == move and self.slots[row][column + col - 3] == move and self.slots[row][column + col - 4] == move:
                        return True
                break
        return False

    def check_vertical_win(self, move, column):
        for row in range(self.height):
            if self.slots[row][column - 1] == move:
                for rows in range(3):
                    if row - rows < 0:
                        break
                    if self.slots[row - rows][column - 1] == move and self.slots[row - rows - 1][column - 1] == move and self.slots[row - rows - 2][column - 1] == move and self.slots[row - rows - 3][column - 1] == move:
                        return True
        return False

    def is_down_diagonal_win(self, move):
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.slots[row][col] == move and \
                   self.slots[row + 1][col + 1] == move and \
                   self.slots[row + 2][col + 2] == move and \
                   self.slots[row + 3][col + 3] == move:
                    return True
        return False

    def is_up_diagonal_win(self, move):
        for row in range(3, self.height):
            for col in range(self.width - 3):
                if self.slots[row][col] == move and \
                   self.slots[row - 1][col + 1] == move and \
                   self.slots[row - 2][col + 2] == move and \
                   self.slots[row - 3][col + 3] == move:
                    return True
        return False

class Player:
    def __init__(self, move):
        self.move = move

    def __repr__(self):
        return f"Player {self.move}"

    def next_move(self, board):
        """
        get next move
        """
        while True:
            try:
                column = int(input(f"Player {self.move}, enter a column: "))
                if board.add_move(self.move, column):
                    return column
            except ValueError:
                print("Please enter a valid column number.")
class RandomPlayer(Player):
    def __init__(self, move):
        super().__init__(move)

    def next_move(self, board):
        """
        get next move
        """
        import random
        while True:
            validMoves = board.getMoves()
            column = random.choice(validMoves)
            if board.add_move(self.move, column):
                return column
