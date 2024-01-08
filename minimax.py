
import chess
import chess.svg
import chess.engine
from datetime import datetime
import random

import move_ordering 
import board_evaluation 
import minimax 



def minimax(board, depth, final_player, current_player, alpha, beta):
    if depth == 0 or board.is_game_over():
        return board_evaluation.evaluate_board(board, final_player, current_player)

    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)
    ordered_moves = move_ordering.get_ordered_moves(board)
    
    if current_player == final_player:
        max_score = float('-inf')
        for move in ordered_moves:
            board.push(move)
            score = minimax(board, depth - 1, final_player, not current_player, alpha, beta)
            board.pop()

            max_score = max(max_score, score)
            alpha = max(alpha, score)

            if beta <= alpha:
                break  # Beta cutoff
        return max_score

    else:  # Minimizing player
        min_score = float('inf')
        for move in ordered_moves:
            board.push(move)
            score = minimax(board, depth - 1, final_player, not current_player, alpha, beta)
            board.pop()

            min_score = min(min_score, score)
            beta = min(beta, score)

            if beta <= alpha:
                break  # Alpha cutoff
        return min_score


def find_best_move(board, depth):
    best_move = None
    best_score = float('-inf')
    legal_moves = list(board.legal_moves)
    score_list = []

    #last_time = datetime.now()
    ordered_moves = move_ordering.get_ordered_moves(board)

    for move in ordered_moves:
        board.push(move)

        score = minimax(board, depth - 1, not board.turn, board.turn, float('-inf'), float('inf'))
        score_list.append(score)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move

    print(best_move, best_score)
    return best_move






