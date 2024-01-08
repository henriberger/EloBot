    

import chess
import chess.svg
import chess.engine
from datetime import datetime
import random

import move_ordering
import board_evaluation
import minimax


def run_opening(board):


    opening_move_list = ['e2e4','c7c5','g1f3','b8c6']

    for move in opening_move_list:
        board.push_uci(move)
    return


def play_chess(white_bot='minimax', black_bot='random'):
    board = chess.Board()

    run_opening(board)

    #print(board)
    #print()
    board_evaluation.evaluate_board(board, not board.turn, board.turn, debug=True)
    print()

    last_time = datetime.now()


    while not board.is_game_over():
        print()
        if board.turn == chess.WHITE:
            print('White Moves')
            if white_bot == 'minimax':
                move = minimax.find_best_move(board, depth=4)

            elif white_bot == 'random':
                move_list = list(board.legal_moves)
                random.shuffle(move_list)
                move = move_list[0]

            else:
                move_list = list(board.legal_moves)
                random.shuffle(move_list)
                move = move_list[0]

        else:
            print('Black Moves')
            #move = find_best_move(board, depth=4)
            print('White Moves')

            if black_bot == 'minimax':
                move = minimax.find_best_move(board, depth=4)

            elif black_bot == 'random':
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
        print('Total Move Time: ', new_time - last_time)
        last_time = new_time

        #print(board)
        #print()
        board_evaluation.evaluate_board(board, not board.turn, board.turn, debug=True)
        print()

    print("Game Over")
    print("Result:", board.result())


if __name__ == "__main__":
    play_chess()


