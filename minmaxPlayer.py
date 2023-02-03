from game import Player
from game import Board
from copy import deepcopy
from random import shuffle

class AIPlayer(Player):
    # inheriting from Player class
    def __init__(self, move, depth):
        super().__init__(move)
        self.depth = depth
    def __repr__(self):
        return "AIPlayer({})".format(self.move)
    # getting the next move from the given board
    def next_move(self, board):
        column = self.minimax(board, self.depth, self.move)
        if board.add_move(self.move, column):
            return column
    # getting the move of the opponent
    def opponent_move(self, move):
        if move == 'X':
            return 'O'
        return 'X'
    # implmenting minmax algorithm to get the best move
    def minimax(self, board, depth, move):
        # all the possible moves
        movesPossible = board.getMoves()
        bestMove = movesPossible[0]
        bestScore = -1e9
        # setting thresholds for alphabet pruning
        alpha = -1e9
        beta = 1e9
        shuffle(movesPossible)
        for turn in movesPossible:
            tempBoard = deepcopy(board)
            tempBoard.add_move(move, turn)
            # traversing up the tree
            score = self.betaFunction(tempBoard, depth - 1, alpha, beta, move)
            if score > bestScore:
                bestScore = score
                bestMove = turn
        return bestMove

    # finding the score on differnt configurations
    def evaluate(self, board, move):
        current_move_fours = self.countSequence(board, move, 4)
        current_move_threes = self.countSequence(board, move, 3)
        current_move_twos = self.countSequence(board, move, 2)
        current_move_ones = self.countSequence(board, move, 1)

        opponent_move_fours = self.countSequence(board, self.opponent_move(move), 4)
        opponent_move_threes = self.countSequence(board, self.opponent_move(move), 3)
        opponent_move_twos = self.countSequence(board, self.opponent_move(move), 2)
        opponent_move_ones = self.countSequence(board, self.opponent_move(move), 1)

        current_player_score = current_move_fours * 1000000 + current_move_threes * 1000 + current_move_twos * 100 + current_move_ones * 10
        opponent_score = opponent_move_fours * 1000000 + opponent_move_threes * 1000 + opponent_move_twos * 100 + opponent_move_ones * 10

        if opponent_move_fours > 0:
            return -1e9
        else:
            return current_player_score - opponent_score

    def countSequence(self, board, move, sequence):
        rowCount = 0
        colCount = 0
        diagCount = 0
        antiDiagCount = 0
        # counting the sequence on row
        for row in range(board.height):
            count = 0
            for col in range(board.width):
                if board.slots[row][col] == move:
                    count += 1
                else:
                    count = 0
                if count == sequence:
                    rowCount += 1
        # counting the sequence on column
        for col in range(board.width):
            count = 0
            for row in range(board.height):
                if board.slots[row][col] == move:
                    count += 1
                else:
                    count = 0
                if count == sequence:
                    colCount += 1
        # counting the sequence on diagonal
        for row in range(board.height - sequence + 1):
            for col in range(board.width - sequence + 1):
                count = 0
                for i in range(sequence):
                    if board.slots[row + i][col + i] == move:
                        count += 1
                    else:
                        count = 0
                    if count == sequence:
                        diagCount += 1
        # counting the sequence on other diagonal
        for row in range(board.height - sequence + 1):
            for col in range(board.width - sequence + 1):
                count = 0
                for i in range(sequence):
                    if board.slots[row + i][col - i] == move:
                        count += 1
                    else:
                        count = 0
                    if count == sequence:
                        antiDiagCount += 1
        
        return rowCount + colCount + diagCount + antiDiagCount
        

    def betaFunction(self, board, depth, alpha, beta, move):
        
        # initializing an empty array
        validMoves = []

        # appending all possible moves
        for col in range(1, board.width + 1):
            if board.can_add_to(col):
                validMoves.append(col)
                
        # checking an special case
        if depth == 0 or len(validMoves) == 0 or board.check_win(self.move, board.last_move_board) or board.check_win(self.opponent_move, board.last_move_board):
            score = self.evaluate(board, self.move)
            return score
        
        validMoves = board.getMoves()

        for turn in validMoves:
            score = 1e9
        # calculating the value for beta by minimizing it
            if alpha < beta:
                tempBoard = deepcopy(board)
                tempBoard.add_move(self.opponent_move(move), turn)
                score = self.alphaFunction(tempBoard, depth - 1, alpha, beta, move)
            beta = min(beta, score)
        return beta
    
    def alphaFunction(self, board, depth, alpha, beta, move):
        
        # initializing an empty array
        validMoves = []

        # appending all possible moves
        for col in range(1, board.width + 1):
            if board.can_add_to(col):
                validMoves.append(col)
        
        # checking an special case
        if depth == 0 or len(validMoves) == 0 or board.check_win(self.move, board.last_move_board) or board.check_win(self.opponent_move(move), board.last_move_board):
            return self.evaluate(board, self.move)
        
        # calculating the value for alpha by maximizing it
        validMoves = board.getMoves()
        for turn in validMoves:
            score = -1e9

            if alpha < beta:
                tempBoard = deepcopy(board)
                tempBoard.add_move(move, turn)
                score = self.betaFunction(tempBoard, depth - 1, alpha, beta, move)
            alpha = max(alpha, score)
        return alpha