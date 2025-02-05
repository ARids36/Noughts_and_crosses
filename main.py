# Imports
import os
import random
import time
from ascii import title, player_win, computer_win, draw


# Functions
def draw_grid():
    """Draws the board in the terminal"""

    clear_screen()
    print(title)
    print(f"-------------\n"
          f"| {board[0]} | {board[1]} | {board[2]} |    0   1   2\n"
          f"-------------\n"
          f"| {board[3]} | {board[4]} | {board[5]} |    3   4   5\n"
          f"-------------\n"
          f"| {board[6]} | {board[7]} | {board[8]} |    6   7   8\n"
          f"-------------\n")


def player_turn():
    """Allows the player to place a marker"""

    print("Player turn (X) - Enter 0-8")
    try:
        choice = int(input("Enter a square: "))

        if board[choice] != " ":
            print("Square occupied - select again")
            player_turn()
            return

    except ValueError:
        print("Grid doesn't exist")
        player_turn()
    else:
        board[choice] = "X"
        draw_grid()


def ai_turn():
    """Allows the AI to place a marker
       The function scores each of the available squares based on the opportunities available from that square,
       with the scoring methods detailed below. The AI then places a marker in the highest scoring square """

    print("Computer turn (O):")
    time.sleep(1)

    '''
    If pattern = X O _  =   -1
    If pattern = _ _ _  =   1
    If pattern = X _ _  =   2
    If pattern = O _ _  =   3
    If pattern = X X _  =   10
    If pattern = O O _  =   15
    '''
    scores = []
    available_squares = [i for i in range(0, 9) if board[i] == " "]  # Check available squares
    for av_square in available_squares:  # Loop through all available squares
        av_square_score = 0
        for lst in search_pattern:  # Loop through all search pattern
            if av_square in lst:  # Check if nominated square is in search pattern
                pattern_markers = [board[i] for i in lst]
                if pattern_markers.count("X") == 1 and pattern_markers.count("O") == 1:
                    av_square_score -= 1
                elif pattern_markers.count("X") == 1:
                    av_square_score += 2
                elif pattern_markers.count("O") == 1:
                    av_square_score += 3
                elif pattern_markers.count("X") == 2:
                    av_square_score += 10
                elif pattern_markers.count("O") == 2:
                    av_square_score += 15
                else:
                    av_square_score += 1
        scores.append((av_square, av_square_score))

    scores.sort(key=lambda x: x[1], reverse=True)
    best_squares = [i for (i, j) in scores if j == scores[0][1]]
    board[random.choice(best_squares)] = "O"
    draw_grid()


def is_win():
    """Checks for a winning line"""

    for lst in search_pattern:  # Loop through search patterns
        x_count = 0
        o_count = 0
        for square in lst:  # Find if patterns can win
            if board[square] == "O":
                o_count += 1
            elif board[square] == "X":
                x_count += 1

            # Check for a winner
            if o_count == 3 or x_count == 3:
                return True

    return False


def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')

    # For macOS and Linux
    else:
        _ = os.system('clear')


# Set board
board = 9*[" "]

# Search pattern for AI turns
search_pattern = [[0, 4, 8],
                  [2, 4, 6],
                  [0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8],
                  [0, 3, 6],
                  [1, 4, 7],
                  [2, 5, 8]]

# -------- Play Game -------- #
running = True
game_is_on = True

while running:
    while game_is_on:
        if board == 9*[" "]:  # Check for new game
            draw_grid()
            print("Choosing starting player...")
            time.sleep(1)
            if random.randint(0, 1) == 1:
                ai_turn()
        player_turn()
        if is_win():
            print(player_win)
            game_is_on = False
        elif len([i for i in range(0, 9) if board[i] == " "]) == 0:
            print(draw)
            game_is_on = False
        else:
            ai_turn()
            if is_win():
                print(computer_win)
                game_is_on = False
            elif len([i for i in range(0, 9) if board[i] == " "]) == 0:
                print(draw)
                game_is_on = False

    rematch = input("Rematch? [Y/N]: ").upper()

    if rematch == "Y":
        game_is_on = True
        board = 9*[" "]
    elif rematch == "N":
        running = False
        print("Exiting")
    else:
        print("Unknown command. Please enter either 'Y' or 'N'")
