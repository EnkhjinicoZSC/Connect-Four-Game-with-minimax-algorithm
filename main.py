import game
from minmaxPlayer import AIPlayer

wins = {'X': 0, 'O': 0, 'Tie': 0}

def parse_move(player, board):
    """
    parse move
    """
    column_num = player.next_move(board)
    print(board)
    if board.check_win(player.move, column_num):
        with open(f"random_games/games{wins['X'] + wins['O'] + wins['Tie']}.txt", 'w') as f:
            f.write(str(board))
            if player.move == 'X':
                f.write("X won")
            else:
                f.write("O won")
        wins[player.move] += 1
        print(player, "wins")
        print("Congratulations!")
        return True
    if board.is_full():
        with open(f"random_games/games{wins['X'] + wins['O'] + wins['Tie']}.txt", 'a') as f:
            f.write(str(board))
            f.write("Tie")
        print("It's a tie!")
        wins['Tie'] += 1
        return True
    return False

def main():
    for i in range(1, 1000):
        board = game.Board()
        player1 = game.RandomPlayer('X')
        player2 = AIPlayer('O', 5)
        while True:
            if parse_move(player1, board) == True:
                break
            if parse_move(player2, board) == True:
                break
        print("Game", i, "finished")
    print(wins)
if __name__ == '__main__':
    main()