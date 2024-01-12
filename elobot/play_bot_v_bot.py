import random
from datetime import datetime

import board_evaluation
import chess
import chess.engine
import chess.svg
import minimax
import move_ordering


def run_opening(board):
    opening_move_list = ["e2e4", "c7c5", "g1f3", "b8c6"]

    for move in opening_move_list:
        board.push_uci(move)
    return


def play_chess(white_bot="minimax", black_bot="random"):
    board = chess.Board()

    run_opening(board)

    print(board)
    print(len(board.move_stack))
    print()
    # board_evaluation.evaluate_board(board, not board.turn, board.turn, debug=True)
    # print()

    last_time = datetime.now()

    while not board.is_game_over():
        print()
        if board.turn == chess.WHITE:
            print("White Moves")
            if white_bot == "minimax":
                move, best_board = minimax.find_best_move(board, depth=5)

            elif white_bot == "random":
                move_list = list(board.legal_moves)
                random.shuffle(move_list)
                move = move_list[0]

            else:
                move_list = list(board.legal_moves)
                random.shuffle(move_list)
                move = move_list[0]

        else:
            print("Black Moves")
            # move = find_best_move(board, depth=4)

            if black_bot == "minimax":
                move, best_board = minimax.find_best_move(board, depth=3)

            elif black_bot == "random":
                move_list = list(board.legal_moves)
                random.shuffle(move_list)
                move = move_list[0]

            else:
                move_list = list(board.legal_moves)
                random.shuffle(move_list)
                move = move_list[0]

        board.push(move)

        new_time = datetime.now()
        print(datetime.now())
        print("Total Move Time: ", new_time - last_time)
        last_time = new_time

        # print(board)
        # print()
        # board_evaluation.evaluate_board(board, not board.turn, board.turn, debug=True)
        print(len(board.move_stack), len(best_board.move_stack))
        print()
        break

    print("Game Over")
    print("Result:", board.result())


if __name__ == "__main__":
    play_chess()
