import math
import random
from datetime import datetime

import board_evaluation
import chess
import chess.engine
import chess.svg
import minimax
import move_ordering

from setup.constants import CENTER_SQUARES


def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    # the king's value is not typically counted in basic evaluation
    elif piece.piece_type == chess.KING:
        return 0


def get_piece_score(board):
    piece_score = 0
    for piece in board.piece_map().values():
        if piece.color:
            piece_score += piece_value(piece)
        else:
            piece_score -= piece_value(piece)

    return piece_score


def get_center_score(board):
    center_score = 0
    for square in CENTER_SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color:
                center_score += math.log(piece_value(piece) + 1e-6)
            else:
                center_score -= math.log(piece_value(piece) + 1e-6)

    return center_score


def get_move_score(board):
    move_score = 0
    move_score -= len(list(board.legal_moves))
    move = board.pop()
    move_score += len(list(board.legal_moves))
    board.push(move)

    if move_score == 0:
        return 0
    elif not board.turn:
        return math.log(abs(move_score))
    else:
        return -math.log(abs(move_score))


def get_checkmate_score(board):
    if not board.turn and board.is_checkmate():
        return float("inf")
    elif board.turn and board.is_checkmate():
        return float("-inf")
    else:
        return 0


def evaluate_board(board, debug=False):
    # print(current_turn)
    # Simple evaluation function (count material)

    piece_score = get_piece_score(board)
    center_score = get_center_score(board)
    move_score = get_move_score(board)

    checkmate_score = get_checkmate_score(board)

    evaluation = piece_score + center_score + move_score / len(board.move_stack) + checkmate_score

    if debug == True:
        print("EVALUATION")
        print(final_turn, piece_score, move_score, checkmate_score)
        print()
        # display(board)
        print(board)
    return evaluation
