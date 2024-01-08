import random
from datetime import datetime

import board_evaluation
import chess
import chess.engine
import chess.svg
import minimax
import move_ordering


def piece_value(piece, current_turn):
    if current_turn:
        multiplier = 1
    else:
        multiplier = -1

    if piece.piece_type == chess.PAWN:
        return 1 * multiplier
    elif piece.piece_type == chess.KNIGHT:
        return 3 * multiplier
    elif piece.piece_type == chess.BISHOP:
        return 3 * multiplier
    elif piece.piece_type == chess.ROOK:
        return 5 * multiplier
    elif piece.piece_type == chess.QUEEN:
        return 9 * multiplier
    elif piece.piece_type == chess.KING:
        return 0  # The king's value is not typically counted in basic evaluation


def get_piece_score(board, final_turn):
    piece_score = 0
    piece_map = board.piece_map()
    for piece in piece_map:
        score += piece_value(piece, final_turn)
    # for square in chess.SQUARES:
    #     piece = board.piece_at(square)
    #     if piece is not None:
    #         piece_score += piece_value(piece, final_turn)
    return piece_score


def control_center_score(board):
    score = 0
    for square in CENTER_SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color:
                score += piece_value(piece, board.turn) ** 0.33
            else:
                score -= piece_value(piece, board.turn) ** 0.33

    return score


def get_move_score(board, final_turn, current_turn):
    move_score = 0
    if final_turn == current_turn:
        move_score += len(list(board.legal_moves))
        move = board.pop()
        move_score -= len(list(board.legal_moves))
        board.push(move)

    else:
        move_score -= len(list(board.legal_moves))
        move = board.pop()
        move_score += len(list(board.legal_moves))
        board.push(move)

    return move_score


def get_checkmate_score(board, final_turn, current_turn):
    if not board.turn == final_turn and board.is_checkmate():
        return float("inf")
    elif board.turn == final_turn and board.is_checkmate():
        return float("-inf")
    else:
        return 0


def evaluate_board(board, final_turn, current_turn, debug=False):
    # print(current_turn)
    # Simple evaluation function (count material)

    piece_score = get_piece_score(board, final_turn) * 3
    move_score = get_move_score(board, final_turn, current_turn)
    checkmate_score = get_checkmate_score(board, final_turn, current_turn)

    evaluation = piece_score + move_score + checkmate_score

    if debug == True:
        print("EVALUATION")
        print(final_turn, piece_score, move_score, checkmate_score)
        print()
        # display(board)
        print(board)
    return evaluation
