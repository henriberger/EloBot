

import chess
import chess.svg
import chess.engine
from datetime import datetime
import random


import move_ordering 
import board_evaluation 
import minimax

def piece_value(piece, current_turn):
    if current_turn:
        multiplier = int((current_turn-0.5)*2)
    else:
        multiplier = int(-(current_turn-0.5)*2)

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
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_score += piece_value(piece, final_turn)
    return piece_score

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
        return float('inf')
    elif board.turn == final_turn and board.is_checkmate():
        return float('-inf')
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
        #display(board)
        print(board)
    return evaluation



