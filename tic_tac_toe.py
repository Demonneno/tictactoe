from random import choice
# import json
from sys import exit
from time import sleep
from math import ceil
from os import name, system

board_moves_played = []
board_dimensions = 3
columns_size = board_dimensions
rows = board_dimensions
board_size = rows * columns_size
positions = {}
max_players = 2
players = {"X": ["",[],""], "O": ["", [],""]} # player[shape]: [0] = name, [1] = positions selectied, [2] = turns counted
ai_player = {}
games_played = 0
timer_to_endgame = 3
combined_moves = []
ai_names = [
    "Byte-Sized Bandit",
    "Glitch Goblin",
    "Neural Noodlehead",
    "Sir Overclocks-a-Lot",
    "Pixel Prankster",
    "Quantum Quirkster",
    "Algo McFlub",
    "Silicon Snickerdoodle",
    "Error 404: Wit Not Found",
    "Fuzzy Logic Fiasco",
    "RoboTickleMonster",
    "Data Doodlebug"
]

epithets = [
    "The Diagonal Daredevil",
    "Cornerstone Conqueror",
    "X Marks the Menace",
    "Ominous O-Placer",
    "Board-Busting Baron",
    "Triple-Threat Trickster",
    "Win-Wrangling Wizard",
    "Draw-Dodging Demon",
    "Cell-Seizing Scoundrel",
    "Row-Ravaging Rogue",
    "Tic Tac Tyrant",
    "Grid-Grabbing Guru"
]

def create_columns(columns):
    list = ""
    char = 65
    for _ in range(0, columns):
        list = list + chr(char)
        char = char + 1
    return list

columns = create_columns(columns_size)

def create_board(board_moves_played):
    for _ in range(board_size):
        board_moves_played.append(" ")


def set_positions(positions):
    index = 0
    for idx in range(1, rows + 1):
        for row in columns:
            positions[f'{row}{idx}'] = index
            index += 1
    return positions

def convert_positions(select_position):
    return positions.get(select_position, "This is awkward...")

def print_board(board_moves_played):
    offset = " " * 46
    offset_border = " " * 51
    print(f"\n{offset_border} {'    '.join( columns )} ")
    border = ""
    for _ in range(0, (board_dimensions * 4) + (ceil(board_dimensions / 2))):
        border = border + "="
    for row in range(rows):
        row_num = row + 1
        print(f"\n{offset}{row_num}    ", end="")
        for col in range(0, columns_size):
            index = row * board_dimensions + col
            print(f" {board_moves_played[index]} ", end="")
            if col < (len(columns) - 1):
                print("||", end="")
        print()  
        if row < (rows - 1):
            print(f"{offset_border}{border}")    

# Future Use?
# def read_scores(doc):
#     try:
#         with open(doc, "r") as file:
#             content = file.readlines()
#             for line in content:
#                 if "high_score" in line:
#                     return "high_score"
#             return 0
#     except FileNotFoundError:
#         with open(doc, "x") as file:
#             print(f'{file} has been created')
#         return 0
#
#
# def save_scores(doc, score):
#     with open(doc, "a", encoding='utf-8') as file:
#         json.dump(score, file, ensure_ascii=False, indent=4)


def name_ai(player_list, epithets, ai_names):

    for key, value in player_list.items():
        if not value:
            player_list[key].append(choice(ai_names))
            print(f"\nYour opponent is {choice(epithets)}, {player_list[key]}\n")
    return player_list


def exit_command(varible_trigger, exit_code: int):
    if varible_trigger == "EXIT":
        clear_screen_exit()
        exit(exit_code)

def number_of_players():
    while True:
        try:
            print(f"\nWelcome to Tic-Tac-Toe! Not that we want it, but you may exit by typing 'exit' at any time!")
            num_players = input("\nIs this a (1) Player or (2) Player game? ")
            exit_command(num_players.upper(), 1)
            num_players = int(num_players)
            if 1 <= num_players <= 2:
                break
            else:
                print(f"\n{num_players} isn't a valid number of Players. Please choose 1 or 2.")
        except ValueError:
            print("\nInvalid input! Please choose 1 or 2 Players.\n")
    return num_players

def name_players():
    n = 1
    ai_player = {}
    max_players = 2
    num_players = number_of_players()
    while n <= max_players:
        if n == 1:
            player_name = input(f"\nEnter your name, Player {n}: ")
            if player_name.upper() == "EXIT":
                confirm_exit = input("\n Did you REALLY mean to exit or are you messin'? (Y)es I think I'm funny / (N)o Messin'! BAIL ME OUT!").upper()
                if confirm_exit == "N":
                    exit_command(player_name.upper(), 2)
            while True:
                player_shape = input(f"\nDo you prefer X or O, {player_name}? (X always plays first): ").upper()
                if player_shape == 'X' or player_shape == 'O':
                    if not players[player_shape][0]:
                        players[player_shape][0] = (player_name)
                        n += 1
                        break
                else:
                    print(f"\nNow, now. {player_shape} isn't valid and you know it, {choice(epithets)} {player_name}!")
        elif n == 2:
            for key in players:
                if not players[key][0]:
                    if num_players == 1:
                        ai_name = choice(ai_names)
                        players[key][0] = ai_name
                        print(f"\nYour opponent is {choice(epithets)}, {players[key][0]}")
                        sleep(1)
                        n += 1
                        ai_player = {key: ai_name}
                        break
                    elif num_players == 2:
                        player_name = input(f"\nWhat's your name, Player {n}? ")
                        players[key][0] = player_name
                        print(f'\nThanks, {player_name}! You will be {key}')
                        n += 1
    return players, ai_player, num_players


def tutorial_check():
    tutorial = input(f"\nDo you want to read the instructions before we begin? (Y/N)").upper()
    if tutorial == "Y":
        print("\nChoose an empty space that matches the column and row (ex. A1 or C3). The first to match horizontally, vertically, or diagonally wins! ")
        sleep(5)
    elif tutorial == "EXIT":
        exit(0)


def replay_check(timer_to_endgame):
    end_game = True
    confirm_end = input("\nAre we going to (C)ontinue or (Q)uit? ").upper()
    if confirm_end == "C" or confirm_end =="CONTINUE":
        end_game = False
    elif confirm_end == "Q" or confirm_end =="QUIT":
        print(f'\nGoodbye, my friends...')
        for i in range(timer_to_endgame, 0,-1):
            print(f"\nTime until it all ends: {i}")
            sleep(1)
        clear_screen_exit()
        end_game = True
    else:
        print("\nWhat are you pressing?!")
    return end_game


def generate_wins(board_dimensions):
    wins = []
    for r in range(board_dimensions):
        row_combo = [r * board_dimensions + c for c in range(board_dimensions)]
        wins.append(row_combo)
    for c in range(board_dimensions):
        col_combo = [r * board_dimensions + c for r in range(board_dimensions)]
        wins.append(col_combo)
    if board_dimensions > 0:
        main_diag = [i * board_dimensions + i for i in range(board_dimensions)]
        wins.append(main_diag)
    if board_dimensions > 1:
        anti_diag = [i * board_dimensions + (board_dimensions - 1 - i) for i in range(board_dimensions)]
        wins.append(anti_diag)
    return wins

def check_win(board_moves_played, shape, board_dimensions):
    """Check if shape won on current board."""
    wins = generate_wins(board_dimensions)
    for combo in wins:
        if all(board_moves_played[idx] == shape for idx in combo):  # All spots match shape
            return True
    return False


def is_draw(board_moves_played, total_moves):
    return total_moves == 0 or " " not in board_moves_played


def logging_position(selected, shape, total_moves):
    global board_moves_played  # <- Ensures access to global board
    board_value = convert_positions(selected)
    board_moves_played[board_value] = shape  # <- Update the global board
    players[shape][1].append(selected)
    combined_moves.append(selected)
    # ADD WIN CHECK HERE
    if check_win(board_moves_played, shape, board_dimensions):
        print(f"\n{players[shape][0]} ({shape}) WINS! 🎉")
        sleep(1)
        return "win"  # Signal to caller
    elif is_draw(board_moves_played, total_moves):  # Uses global board
        print(f"\n{players['X'][0]} and {players['O'][0]} TIE!")
        sleep(1)
        return "draw"
    return "continue"  # Normal turn

def ai_bot(board_moves_played, positions):
    empty_indices =[i for i, x in enumerate(board_moves_played) if x == ' ']
    random_index = choice(empty_indices)
    random_choice = next(key for key, value in positions.items() if value == random_index)
    return random_choice

def clear_screen():
    system('cls' if name == 'nt' else 'clear')
    print('\n\n\n\n')
    print("░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░       ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░       ░▒▓████████▓▒░▒▓██████▓▒░░▒▓████████▓▒░ ")
    print("  ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
    print("  ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
    print("  ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓████████▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░   ")
    print("  ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
    print("  ░▒▓█▓▒░   ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        ")
    print("  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓██████▓▒░          ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░          ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓████████▓▒░ ")

def clear_screen_exit():
    system('cls' if name == 'nt' else 'clear')

def player_turns():
    end_game = False
    global games_played
    while not end_game:
        board_moves_played[:] = [" "] * board_size
        combined_moves.clear()
        total_moves = board_size
        win = False
        player_x = False
        if games_played == 0:
            tutorial_check()
        elif games_played > 0:
            clear_screen()
        while not win and total_moves > 0:
            player = players["X"][0] if not player_x else players["O"][0]
            shape = "X" if not player_x else "O"  # <- ADD THIS: Define shape for the turn
            while True:
                clear_screen()
                print_board(board_moves_played)
                if player in ai_names and num_players == 1:
                    select_position = ai_bot(board_moves_played,positions)
                    sleep(1)
                    print(f"\n{player} has chosen {select_position}!")
                    sleep(2)
                else:
                    select_position = input(f"\nChoose a position, {player}: ").upper()
                    exit_command(select_position, 3)

                if select_position in positions and select_position not in combined_moves:
                    result = logging_position(select_position, shape, total_moves)
                    total_moves -= 1
                    if result == "win" or result == "draw":
                        win = True  # End game loop
                        break  # Exit turn loop
                    break  # Normal move
                else:
                    print(f'{select_position} is invalid!')
            player_x = not player_x

        games_played += 1
        end_game= replay_check(timer_to_endgame)


if __name__ == "__main__":
    clear_screen()
    create_board(board_moves_played)
    positions = set_positions(positions)
    print_board(board_moves_played)
    players, ai_player, num_players = name_players()
    player_turns()
