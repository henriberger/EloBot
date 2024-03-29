import random
from datetime import datetime

import board_evaluation
import chess
import chess.engine
import chess.svg
import minimax
import move_ordering
from tqdm import tqdm


def minimax(board, depth, final_player, current_player, alpha, beta, best_board):
    # print(depth)
    if depth == 0 or board.is_game_over():
        return board_evaluation.evaluate_board(board, final_player, current_player), board.copy()

    legal_moves = list(board.legal_moves)
    # random.shuffle(legal_moves)
    ordered_moves = move_ordering.get_ordered_moves(board)

    if len(ordered_moves) > 25:
        ordered_moves = ordered_moves[:25]

    if current_player == final_player:
        max_score = float("-inf")
        for move in ordered_moves:
            board.push(move)
            score, last_board = minimax(board, depth - 1, final_player, not current_player, alpha, beta, best_board)
            board.pop()
            # if depth == 1:
            # print(len(board.move_stack), board.move_stack)
            # print(len(last_board.move_stack), last_board.move_stack)
            # exit()

            if score > max_score:
                best_board = last_board

            max_score = max(max_score, score)
            alpha = max(alpha, score)

            if beta <= alpha:
                break
        return max_score, best_board

    else:  # Minimizing player
        min_score = float("inf")
        for move in ordered_moves:
            board.push(move)
            score, last_board = minimax(board, depth - 1, final_player, not current_player, alpha, beta, best_board)
            board.pop()

            if score < min_score:
                best_board = last_board

            min_score = min(min_score, score)
            beta = min(beta, score)

            if beta <= alpha:
                break
        return min_score, best_board


def find_best_move(board, depth):
    best_move = None
    best_score = float("-inf")
    legal_moves = list(board.legal_moves)
    score_list = []

    # last_time = datetime.now()
    ordered_moves = move_ordering.get_ordered_moves(board)
    last_board = board.copy()

    for i in tqdm(range(len(ordered_moves))):
        move = ordered_moves[i]

        board.push(move)

        score, last_board = minimax(
            board, depth - 1, not board.turn, board.turn, float("-inf"), float("inf"), last_board
        )

        score_list.append(score)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
            best_board = last_board

    print("BEST BOARD")
    print(best_move, best_score)
    print(best_board)

    return best_move, best_board
