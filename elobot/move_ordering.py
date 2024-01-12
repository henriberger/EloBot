import random
from datetime import datetime

import board_evaluation
import chess
import chess.engine
import chess.svg
import minimax
import move_ordering

from setup.constants import CENTER_SQUARES


def ordering_value(piece):
    # print(piece, piece.piece_type, chess.PAWN)
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    # high value to prioritize checkmating
    elif piece.piece_type == chess.KING:
        return float("inf")


def mvv_lva_ordering(capture_moves, board):
    scores = []
    for move in capture_moves:
        # MVV/LVA score: (captured piece value - attacker piece value)
        captured_piece = board.piece_at(move.to_square)
        attacker_piece = board.piece_at(move.from_square)
        if captured_piece is not None and attacker_piece is not None:
            score = ordering_value(captured_piece) - ordering_value(attacker_piece)
            scores.append((score, move))

    # Sort moves in descending order based on MVV/LVA score
    scores.sort(key=lambda x: x[0], reverse=True)
    return [move for _, move in scores]


# def order_non_capture_moves(non_capture_moves, board):
#     moves = {
#         "is_center": [],
#         "is_castling": [],
#         "is_development": [],
#         "is_pawn_structure": [],
#         "is_active_piece": [],
#         "is_coordination": [],
#         "is_safe": [],
#     }

#     for move in non_capture_moves:
#         if board.is_center(move):
#             moves["is_center"].append(move)
#         elif board.is_castling(move):
#             moves["is_castling"].append(move)
#         elif board.is_development(move):
#             moves["is_development"].append(move)
#         elif board.is_pawn_structure(move):
#             moves["is_pawn_structure"].append(move)
#         elif board.is_active_piece(move):
#             moves["is_active_piece"].append(move)
#         elif board.is_coordination(move):
#             moves["is_coordination"].append(move)
#         elif board.is_safe(move):
#             moves["is_safe"].append(move)

#     ordered_moves = moves["is_center"] + moves["is_development"] + moves["is_pawn_structure"]
#     return ordered_moves


def evaluate_move(move, board):
    score = 0
    piece = board.piece_at(move.from_square)
    if move.to_square in CENTER_SQUARES:
        score += 1
    elif board.is_castling(move):
        score += 2
    elif piece and piece.piece_type in [chess.PAWN, chess.KNIGHT]:
        score += 1

    return score


def order_non_capture_moves(non_capture_moves, board):
    ordered_moves = sorted(non_capture_moves, key=lambda move: evaluate_move(move, board), reverse=True)
    return ordered_moves


def get_ordered_moves(board):
    # Get all legal moves
    legal_moves = list(board.legal_moves)

    # Separate capture moves and non-capture moves
    capture_moves, non_capture_moves = [], []
    for move in legal_moves:
        if board.is_capture(move):
            capture_moves.append(move)
        else:
            non_capture_moves.append(move)

    # capture_moves = [move for move in legal_moves if board.is_capture(move)]
    # non_capture_moves = [move for move in legal_moves if not board.is_capture(move)]

    # Order capture moves using MVV/LVA ordering
    ordered_capture_moves = mvv_lva_ordering(capture_moves, board)
    ordered_non_capture_moves = order_non_capture_moves(non_capture_moves, board)

    # Combine ordered capture moves and non-capture moves
    ordered_moves = ordered_capture_moves + ordered_non_capture_moves

    return ordered_moves
