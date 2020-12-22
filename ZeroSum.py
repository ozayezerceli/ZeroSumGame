import numpy as np
import math
import time
from pandas import *


class Node:

    def __init__(self, data, key):
        self.north = None
        self.east = None
        self.data = data  # to hold Pawn (P)
        self.key = key  # to hold the value of node
        self.comingBranch = None


def get_grid_number():
    user_input = input("Please enter the number of grid:\n")
    user_input = int(user_input)
    return user_input


def construct_game_table(gridValue):
    game_table = np.empty((gridValue, gridValue), dtype=object)
    for i in range(gridValue):
        for j in range(gridValue):
            game_table[i][j] = Node(None, None)

    for i in range(gridValue):
        game_table[i:i + 1, gridValue - 1] = Node(None, np.random.randint(-2, 2))
        game_table[0, i:i + 1] = Node(None, np.random.randint(-2, 2))

    game_table[0, gridValue - 1] = Node(None, None)
    game_table[gridValue - 1, 0] = Node("P", None)
    return game_table


def connect_nodes(game_table, gridValue):
    for i in range(gridValue - 1):
        for j in range(gridValue - 1):
            game_table[i + 1][j].north = game_table[i][j]
            game_table[i + 1][j].east = game_table[i + 1][j + 1]


def draw_table(game_table):
    for i in range(int(math.sqrt(game_table.size))):
        for j in range(int(math.sqrt(game_table.size))):
            node = game_table[i][j]
            if node.key is not None:
                print(node.key, " \t", end=" ")
            elif node.data == "P":
                print(node.data, " \t", end=" ")
            else:
                print(node.data, " \t", end=" ")
        print(" ")


def is_end_state(game_table, gridValue):
    for i in range(gridValue):
        for j in range(gridValue):
            node = game_table[i][j]
            if node.data == "P" and node.key is not None:
                return node.key

def height(root):
    if root is None:
        return 0
    else:
        return max(height(root.north), height(root.east)) + 1


def get_children(root):
    return [root.north, root.east]


def find_Pawn(game_table, gridValue):
    for i in range(gridValue):
        for j in range(gridValue):
            if game_table[i][j].data == "P":
                return game_table[i][j]


def alphabeta(node, depth, alpha, beta, maxTurn, comingBrach):
    if depth == 0 or node.key is not None:
        return node.key, " "

    if maxTurn:
        value = float("-inf")
        for each in range(len(get_children(node))):  # to put break in each if, I have created loop
            if each == 1:
                comingBrach = "N"
                value = max(value, alphabeta(node.north, depth - 1, alpha, beta, False, comingBrach)[0])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            elif each == 2:
                comingBrach = "E"
                value = max(value, alphabeta(node.east, depth - 1, alpha, beta, False, comingBrach)[0])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return value, comingBrach

    else:
        value = float("inf")
        if alphabeta(node.east, depth - 1, alpha, beta, True, comingBrach)[0] > \
                alphabeta(node.north, depth - 1, alpha, beta, True, comingBrach)[0]:
            comingBrach = "N"
            value = min(value, alphabeta(node.north, depth - 1, alpha, beta, True, comingBrach)[0])
            beta = min(beta, value)
            if beta <= alpha:
                return
        else:
            comingBrach = "E"
            value = min(value, alphabeta(node.east, depth - 1, alpha, beta, True, comingBrach)[0])
            beta = min(beta, value)
            if beta <= alpha:
                return

        return value, comingBrach


def minimax(node, depth, maxTurn, comingBrach):
    if depth == 0 or node.key is not None:
        return node.key, " "

    if maxTurn:  # maximizing player
        value = float("-inf")
        if minimax(node.north, depth - 1, False, comingBrach)[0] > minimax(node.east, depth - 1, False, comingBrach)[0]:
            comingBrach = "N"
            value = max(value, minimax(node.north, depth - 1, False, comingBrach)[0])
        else:
            comingBrach = "E"
            value = max(value, minimax(node.east, depth - 1, False, comingBrach)[0])

        return value, comingBrach
    else:  # minimizing player
        value = float("inf")
        if minimax(node.east, depth - 1, True, comingBrach)[0] > minimax(node.north, depth - 1, True, comingBrach)[0]:
            comingBrach = "N"
            value = min(value, minimax(node.north, depth - 1, True, comingBrach)[0])
        else:
            comingBrach = "E"
            value = min(value, minimax(node.east, depth - 1, True, comingBrach)[0])

        return value, comingBrach


def play_game(search_type):
    grid_n = get_grid_number()
    game_table = construct_game_table(grid_n)
    connect_nodes(game_table, grid_n)
    player_turn = "P1"
    while True:
        result = is_end_state(game_table, grid_n)
        if result is not None:
            if result > 0:
                print("The winner is Player 1!")
            elif result < 0:
                print("The winner is Player 2!")
            else:
                print("It's a tie!")

            again_opt = input("Would you like to play again?\n:Yes(Y) or No(N)")
            if again_opt == "Y":
                play_game(search_type)
            else:
                print("Thanks for playing! See you later!")
                break
        draw_table(game_table)
        if player_turn == "P1":
            start = time.time()
            current_node = find_Pawn(game_table, grid_n)
            if search_type == "1":
                optimal_move = minimax(current_node, height(current_node), True, " ")  # minimax alg.
            else:
                optimal_move = alphabeta(current_node, height(current_node), float("-inf"), float("inf"), True,
                                         " ")  # alpha beta pruning alg.
            end = time.time()
            print('Evaluation time: {}s'.format(round(end - start, 7)))
            print('Recommended move: ', optimal_move, "\n")
            player_option = input("North(N), East(E), Pass(P) and Exit(X). Please choose one:\n ")
            if player_option == "N":
                current_node.data = None
                current_node.north.data = "P"
            elif player_option == "E":
                current_node.data = None
                current_node.east.data = "P"

            elif player_option == "P":
                print("Pawn stays same!")

            elif player_option == "X":
                print("Thanks for playing! See you later!")
                break
            else:
                print("Please enter a valid option!")

            player_turn = "P2"

        else:
            start = time.time()
            current_node = find_Pawn(game_table, grid_n)
            if search_type == "1":
                optimal_move = minimax(current_node, height(current_node), False, " ")  # minimax alg.
            else:
                optimal_move = alphabeta(current_node, height(current_node), float("-inf"), float("inf"), False,
                                         " ")  # alpha beta pruning alg.
            end = time.time()
            print('Evaluation time: {}s'.format(round(end - start, 7)))
            print('Recommended move: ', optimal_move, "\n")
            if optimal_move[1] == "N":
                current_node.data = None
                current_node.north.data = "P"

            elif optimal_move[1] == "E":
                current_node.data = None
                current_node.east.data = "P"

            else:
                print("Pawn stays same!")

            player_turn = "P1"


def ai_vs_ai(search_type):
    grid_n = get_grid_number()
    game_table = construct_game_table(grid_n)
    connect_nodes(game_table, grid_n)
    player_turn = "P1"
    while True:
        result = is_end_state(game_table, grid_n)
        if result is not None:
            if result > 0:
                print("The winner is Player 1!")
            elif result < 0:
                print("The winner is Player 2!")
            else:
                print("It's a tie!")

            again_opt = input("Would you like to play again?\n:Yes(Y) or No(N)")
            if again_opt == "Y":
                ai_vs_ai(search_type)
            else:
                print("Going back to the main menu...")
                break
        draw_table(game_table)
        if player_turn == "P1":
            start = time.time()
            current_node = find_Pawn(game_table, grid_n)
            if search_type == "1":
                optimal_move = minimax(current_node, height(current_node), True, " ")  # minimax alg.
            else:
                optimal_move = alphabeta(current_node, height(current_node), float("-inf"), float("inf"), True,
                                         " ")  # alpha beta pruning alg.
            end = time.time()
            print('Evaluation time: {}s'.format(round(end - start, 7)))
            print('Recommended move: ', optimal_move, "\n")
            if optimal_move[1] == "N":
                current_node.data = None
                current_node.north.data = "P"

            elif optimal_move[1] == "E":
                current_node.data = None
                current_node.east.data = "P"

            else:
                print("Pawn stays same!")

            player_turn = "P2"

        else:
            start = time.time()
            current_node = find_Pawn(game_table, grid_n)
            if search_type == "1":
                optimal_move = minimax(current_node, height(current_node), False, " ")  # minimax alg.
            else:
                optimal_move = alphabeta(current_node, height(current_node), float("-inf"), float("inf"), False,
                                         " ")  # alpha beta pruning alg.
            end = time.time()
            print('Evaluation time: {}s'.format(round(end - start, 7)))
            print('Recommended move: ', optimal_move, "\n")
            if optimal_move[1] == "N":
                current_node.data = None
                current_node.north.data = "P"

            elif optimal_move[1] == "E":
                current_node.data = None
                current_node.east.data = "P"

            else:
                print("Pawn stays same!")

            player_turn = "P1"


def pick_search_alg():
    valid_type = False
    while valid_type is not True:
        search_alg_type = input(
            "Please select the type of search algorithm: \n (1) Minimax Alg. \n (2) Alpha-Beta Alg. \n")
        if search_alg_type == "1" or search_alg_type == "2":
            valid_type = True
            return search_alg_type
        else:
            print("Please select a valid search algorithm!")


def main():
    play = True
    while play:
        game_mode = input("Please select game mode: \n (1) User-AI \n (2) AI-AI \n (3) Exit \n")
        if game_mode == "1":
            search_alg_type = pick_search_alg()
            play_game(search_alg_type)
        elif game_mode == "2":
            search_alg_type = pick_search_alg()
            ai_vs_ai(search_alg_type)
        elif game_mode == "3":
            print("Thanks for playing!")
            play = False
        else:
            print("Please select a valid option!!")


if __name__ == "__main__":
    main()
