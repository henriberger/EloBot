import random
from datetime import datetime

import board_evaluation
import chess
import chess.engine
import chess.svg
import minimax
import move_ordering


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
    elif piece.piece_type == chess.KING:
        return 1000  # High value to prioritize checkmating


def mvv_lva_ordering(capture_moves, board):
    scores = []
    for move in capture_moves:
        # MVV/LVA score: (captured piece value - attacker piece value)
        captured_piece = board.piece_at(move.to_square)
        attacker_piece = board.piece_at(move.from_square)
        if captured_piece is not None and attacker_piece is not None:
            score = ordering_value(captured_piece) - ordering_value(attacker_piece)
            scores.append((move, score))

    # Sort moves in descending order based on MVV/LVA score
    scores.sort(key=lambda x: x[1], reverse=True)
    return [move for move, _ in scores]


def get_ordered_moves(board):
    # Get all legal moves
    legal_moves = list(board.legal_moves)

    # Separate capture moves and non-capture moves
    capture_moves = [move for move in legal_moves if board.is_capture(move)]
    non_capture_moves = [move for move in legal_moves if not board.is_capture(move)]

    # Order capture moves using MVV/LVA ordering
    ordered_capture_moves = mvv_lva_ordering(capture_moves, board)

    # Combine ordered capture moves and non-capture moves
    ordered_moves = ordered_capture_moves + non_capture_moves

    return ordered_moves
