import multiprocessing as mp
import time

import board_evaluation
import chess
import minimax
import move_ordering
from tqdm import tqdm


class EloBot:
    def __init__(self, color, depth=3, breadth=0.9, decay=0.9, multiprocess=False, cores=8):
        self.color = color
        self.depth = depth
        self.breadth = breadth
        self.decay = decay
        self.multiprocess = multiprocess
        self.cores = cores
        self.best_move = None
        self.best_board = None
        self.moves = 0
        self.plies = 0

    def cheat_runtime(self):
        return self.opponent_best_follow_up_move

    def prepend_best_follow_up_moves(self, ordered_moves):
        if self.best_board:
            if len(self.best_board.move_stack) > self.plies:
                best_follow_up_move1 = list(self.best_board.move_stack)[self.plies]
                if best_follow_up_move1 in board.legal_moves:
                    if best_follow_up_move1 in ordered_moves:
                        ordered_moves.remove(best_follow_up_move1)
                ordered_moves.insert(0, best_follow_up_move1)
                if len(self.best_board.move_stack) > self.plies + 2:
                    best_follow_up_move2 = list(self.best_board.move_stack)[self.plies + 2]
                    if best_follow_up_move2 in board.legal_moves:
                        if best_follow_up_move2 in ordered_moves:
                            ordered_moves.remove(best_follow_up_move2)
                    ordered_moves.insert(1, best_follow_up_move2)

        return ordered_moves

    def narrow_move_search(self, depth, ordered_moves, n=4):
        plies_ahead = self.depth - depth
        if plies_ahead > n:
            scaling = self.breadth * (self.decay ** (plies_ahead - n + 1))
            n_moves = max(1, int(len(ordered_moves) * scaling))
            ordered_moves = ordered_moves[:n_moves]

        return ordered_moves

    def minimax(self, board, depth, alpha, beta, best_board):
        if depth == 0 or board.is_game_over():
            return board_evaluation.evaluate_board(board), board.copy()

        ordered_moves = move_ordering.get_ordered_moves(board)
        ordered_moves = self.narrow_move_search(depth, ordered_moves)

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

    def find_best_move_mp(self, board, best_board, results):
        score, last_board = self.minimax(board, self.depth - 1, float("-inf"), float("inf"), best_board)
        if results.get(score):
            while results.get(score):
                if self.color:
                    score -= 1e-6
                else:
                    score += 1e-6
            results[score] = last_board

        else:
            results[score] = last_board

    def make_best_move(self, board, meta=False, top_n=3):
        self.plies = len(board.move_stack)
        self.moves = int(self.plies / 2) + (1 if not board.turn else 0)
        best_move = None
        best_odd_depth_score = float("-inf")
        best_even_depth_score = float("inf")
        legal_moves = list(board.legal_moves)

        ordered_moves = move_ordering.get_ordered_moves(board)
        ordered_moves = self.prepend_best_follow_up_moves(ordered_moves)

        best_board = board.copy()

        if self.multiprocess:
            manager = mp.Manager()
            results = manager.dict()
            for i in range(0, len(ordered_moves), self.cores):
                jobs = []
                for move in ordered_moves[i : min(i + self.cores, len(ordered_moves))]:
                    board.push(move)

                    p = mp.Process(target=self.find_best_move_mp, args=(board.copy(), best_board, results))
                    board.pop()
                    p.start()
                    jobs.append(p)

                for p in jobs:
                    p.join()

            if self.color:
                best_score = max(results.keys())
                best_board = results[best_score]
                best_move = best_board.move_stack[self.plies]
            else:
                best_score = min(results.keys())
                best_board = results[best_score]
                best_move = best_board.move_stack[self.plies]

        else:
            for move in ordered_moves:
                board.push(move)

                score, last_board = self.minimax(board, self.depth - 1, float("-inf"), float("inf"), best_board)

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

        if meta:
            if self.color:
                results = dict(sorted(results.items(), reverse=True))
                keys = list(results.keys())
            else:
                results = dict(sorted(results.items(), reverse=False))

            keys = list(results.keys())
            return [results[keys[i]].move_stack[self.plies] for i in range(top_n)]

        self.best_move = best_move
        self.best_board = best_board
        board.push(self.best_move)

        try:
            self.opponent_best_follow_up_move = list(self.best_board.move_stack)[self.plies + 1]
        except:
            pass

        # print(best_move, self.opponent_best_follow_up_move)

        return board

    def meta_search(self):
        pass


if __name__ in "__main__":
    white_bot = EloBot(color=True, depth=6, multiprocess=True)
    black_bot = EloBot(color=False, depth=4)

    board = chess.Board()
    print(board)
    moves = 0
    while not board.is_game_over():
        start = time.time()
        board = white_bot.make_best_move(board)
        if not board.is_game_over():
            # board = black_bot.find_best_move(board)
            board.push(white_bot.cheat_runtime())
        end = time.time()
        moves += 1
        print(f"Move {moves}: {round((end - start) / 1, 1)} sec")
        print(board)
    #     break
    # print(white_bot.best_board)
    # print(white_bot.best_board.move_stack)

    print("Game Over")
    print("Result:", board.result())
