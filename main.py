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
       The function follows a hierarchy of searching for winning moves, blocking the players winning moves, then
       placing a random marker"""

    print("Computer turn (O):")
    time.sleep(1)
    # Search for winning moves
    for lst in search_pattern:  # Loop through search patterns
        count = 0
        for square in lst:  # Find if patterns can win
            if board[square] == "O":
                count += 1
        if count == 2:  # If patterns can win, check to see if remaining square is empty and mark
            for square in lst:
                if board[square] == " ":
                    board[square] = "O"
                    draw_grid()
                    return

    # If no winning moves are found, block opponent
    for lst in search_pattern:  # Loop through search patterns
        count = 0
        for square in lst:  # Find if patterns can win
            if board[square] == "X":
                count += 1
        if count == 2:  # If patterns can win, mark the remaining square if it's empty
            for square in lst:
                if board[square] == " ":
                    board[square] = "O"
                    draw_grid()
                    return

    # No critical moves - place random square
    if board[4] == " ":  # Maybe remove if it's too predictable
        board[4] = "O"
    else:
        available_squares = [i for i in range(0, 8) if board[i] == " "]
        board[random.choice(available_squares)] = "O"
    draw_grid()


def is_win():
    """Check for a winning line"""
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
        elif len([i for i in range(0, 8) if board[i] == " "]) == 0:
            print(draw)
            game_is_on = False
        else:
            ai_turn()
            if is_win():
                print(computer_win)
                game_is_on = False
            elif len([i for i in range(0, 8) if board[i] == " "]) == 0:
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
