import board_evaluation
import chess
import minimax
import move_ordering
from tqdm import tqdm


class EloBot:
    def __init__(self, color, depth=3, breadth=1, decay=0.9):
        self.color = color
        self.depth = depth
        self.breadth = breadth
        self.decay = decay
        self.best_move = None
        self.best_board = None
        self.moves = 0
        self.plies = 0

    def cheat_runtime(self):
        return self.opponent_best_follow_up_move

    def minimax(self, board, depth, alpha, beta, best_board):
        if depth == 0 or board.is_game_over():
            return board_evaluation.evaluate_board(board), board.copy()

        ordered_moves = move_ordering.get_ordered_moves(board)

        if board.turn:
            max_score = float("-inf")
            for move in ordered_moves:
                board.push(move)
                score, last_board = self.minimax(board, depth - 1, alpha, beta, best_board)
                board.pop()

                if score > max_score:
                    best_board = last_board

                max_score = max(max_score, score)
                alpha = max(alpha, score)

                if beta <= alpha:
                    break

            return max_score, best_board

        else:
            min_score = float("inf")
            for move in ordered_moves:
                board.push(move)
                score, last_board = self.minimax(board, depth - 1, alpha, beta, best_board)
                board.pop()

                if score < min_score:
                    best_board = last_board

                min_score = min(min_score, score)
                beta = min(beta, score)

                if beta <= alpha:
                    break

            return min_score, best_board

    def find_best_move(self, board):
        self.plies = len(board.move_stack)
        self.moves = int(self.plies / 2)
        # self.best_move, self.best_board = minimax.find_best_move(board, self.depth)
        best_move = None
        best_odd_depth_score = float("-inf")
        best_even_depth_score = float("inf")
        legal_moves = list(board.legal_moves)

        # last_time = datetime.now()
        ordered_moves = move_ordering.get_ordered_moves(board)
        if self.best_board:
            if len(self.best_board.move_stack) > self.plies:
                best_follow_up_move1 = list(self.best_board.move_stack)[self.plies]
                if best_follow_up_move1 in board.legal_moves:
                    ordered_moves.insert(0, ordered_moves.pop(ordered_moves.index(best_follow_up_move1)))
                if len(self.best_board.move_stack) > self.plies + 2:
                    best_follow_up_move2 = list(self.best_board.move_stack)[self.plies + 2]
                    if best_follow_up_move2 in board.legal_moves:
                        #     ordered_moves.insert(0, best_follow_up_move)
                        # move best follow up to front
                        #     ordered_moves.insert(0, best_follow_up_move)
                        # move best follow up to front
                        ordered_moves.insert(1, ordered_moves.pop(ordered_moves.index(best_follow_up_move2)))

        # if len(ordered_moves) > 30:
        #     ordered_moves = ordered_moves[:30]

        last_board = board.copy()

        for move in ordered_moves:
            board.push(move)

            score, last_board = self.minimax(board, self.depth - 1, float("-inf"), float("inf"), last_board)

            board.pop()
            if self.color:
                if score > best_odd_depth_score:
                    best_odd_depth_score = score
                    best_move = move
                    best_board = last_board
            else:
                if score < best_even_depth_score:
                    best_even_depth_score = score
                    best_move = move
                    best_board = last_board

        self.best_move = best_move
        self.best_board = best_board
        board.push(self.best_move)
        print(best_board)

        try:
            self.opponent_best_follow_up_move = list(self.best_board.move_stack)[self.plies + 1]
        except:
            pass

        return board


white_bot = EloBot(color=True, depth=4)
black_bot = EloBot(color=False, depth=4)

board = chess.Board()
print(board)
moves = 0
while not board.is_game_over():
    board = white_bot.find_best_move(board)
    if not board.is_game_over():
        # board = black_bot.find_best_move(board)
        board.push(white_bot.cheat_runtime())
    moves += 1
    print(f"Move {moves}")
    print(board)
#     break
# print(white_bot.best_board)
# print(white_bot.best_board.move_stack)

print("Game Over")
print("Result:", board.result())
