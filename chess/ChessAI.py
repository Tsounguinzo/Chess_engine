import random
import numpy as np

class AI():

    def __init__(self):
        self.pawn_table = np.array([
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 5, 10, 10,-20,-20, 10, 10,  5],
            [ 5, -5,-10,  0,  0,-10, -5,  5],
            [ 0,  0,  0, 20, 20,  0,  0,  0],
            [ 5,  5, 10, 25, 25, 10,  5,  5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
        ])

        self.knight_table = np.array([
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,   0,   5,   5,   0, -20, -40],
            [-30,   5,  10,  15,  15,  10,   5, -30],
            [-30,   0,  15,  20,  20,  15,   0, -30],
            [-30,   5,  15,  20,  20,  15,   0, -30],
            [-30,   0,  10,  15,  15,  10,   0, -30],
            [-40, -20,   0,   0,   0,   0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ])

        self.bishop_table = np.array([
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,   5,   0,   0,   0,   0,   5, -10],
            [-10,  10,  10,  10,  10,  10,  10, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,   5,   5,  10,  10,   5,   5, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ])

        self.rook_table = np.array([
            [ 0,  0,  0,  5,  5,  0,  0,  0],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [ 5, 10, 10, 10, 10, 10, 10,  5],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
        ])

        self.queen_table = np.array([
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10,   0,   5,  0,  0,   0,   0, -10],
            [-10,   5,   5,  5,  5,   5,   0, -10],
            [  0,   0,   5,  5,  5,   5,   0,  -5],
            [ -5,   0,   5,  5,  5,   5,   0,  -5],
            [-10,   0,   5,  5,  5,   5,   0, -10],
            [-10,   0,   0,  0,  0,   0,   0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]
        ])

        self.king_table = np.array([
            [ 20,  30,  10,   0,   0,  10,  30,  20],
            [ 20,  20,   0,   0,   0,   0,  20,  20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30]
        ])

        self.piece_scores = {'p': 10, 'B': 30, 'N': 30,
                             'R': 50, 'Q': 90, 'K': 900}  # stores the weight of each piece in a dictionary

    # returns random valid move
    def generate_random_move(self, valid_moves):
        #random fct in python generates a number from a to b inclusive
        return valid_moves[random.randint(0, len(valid_moves) - 1)]

    # returns only material score
    def evaluate_simple(self, gs, board):
        # declaring check/stalemate
        if gs.check_mate:
            if gs.white_to_move:
                return -9999 #min player (black) wins
            else:
                return 9999 # max player (white) wins
        elif gs.stale_mate:
            return 0

        return self.get_material_score(board)

    # returns material score + piece position scores
    def evaluate_complex(self, gs, board):
        # declaring check/stalemate (terminal state)
        if gs.check_mate:
            if gs.white_to_move:
                return -9999  # min player (black) wins
            else:
                return 9999  # max player (white) wins
        elif gs.stale_mate:
            return 0

        # stores piece position scores for each piece
        material_score = self.get_material_score(board)
        pawns = self.get_position_score(board, 'p',self.pawn_table)
        knights = self.get_position_score(board, 'N', self.knight_table)
        bishops = self.get_position_score(board, 'B', self.bishop_table)
        rooks = self.get_position_score(board, 'R', self.rook_table)
        queens = self.get_position_score(board, 'Q', self.queen_table)
        kings = self.get_position_score(board, 'K', self.king_table)

        eval_score = material_score + pawns + bishops + knights + rooks + queens + kings

        # white is max / black is min
        if gs.white_to_move:
            return eval_score
        else:
            return -eval_score

    # returns the material score: weighted sum of w pieces on board - weighted sum of b pieces on board
    def get_material_score (self, board):
        white_material_score = 0
        black_material_score = 0
        for r in range (8):
            for c in range (8):
                piece = board[r][c]
                if piece != "**":
                    if piece[0] == 'w':
                        white_material_score += self.piece_scores[piece[1]]  # using the value for the piece key
                    elif piece[0] == 'b':
                        black_material_score += self.piece_scores[piece[1]]
        return white_material_score - black_material_score

    # returns the piece position score: sum of w position score per piece - sum of b position score per piece
    def get_position_score (self, board, piece_type, table):
        white_position_score = 0
        black_position_score = 0
        for r in range (0, 1, 8):
            for c in range (0, 1, 8):
                piece = board[r][c]
                if piece != "**":
                    if piece[1] == piece_type:
                        if piece[0] == 'w':
                            white_position_score += table[r][c]  # using values in 2d array tables
                        elif piece[0] == 'b':
                            black_position_score += table[7-r][c]
        return white_position_score - black_position_score

    # returns smart move with depth 2
    def generate_smart_move(self, gs, depth, difficulty):
        best_score = 9999
        valid_moves = gs.get_valid_moves()
        best_move = valid_moves[0]
        for move in valid_moves:
            gs.make_move(move)
            current_eval = self.minimax(gs, depth, -9999, 9999, True, difficulty)
            gs.undo_move()
            if (current_eval < best_score):
                best_score = current_eval
                best_move = move
        return best_move

    # returns the best move and the min/max evaluation function score (uses AB-pruning)
    def minimax(self, gs, depth, alpha, beta, max_player, difficulty):
        # using different evaluation functions depending on difficulty chosen by the user
        if depth == 0: # base case
            if difficulty == 1:
                return self.evaluate_simple(gs, gs.board)
            if difficulty == 2:
                return self.evaluate_complex(gs, gs.board)
        valid_moves = gs.get_valid_moves()

        if max_player: # aims to maximize score
            max_eval = -9999
            for move in valid_moves:
                gs.make_move(move)
                max_eval = max(max_eval, self.minimax(gs, depth-1, alpha, beta, False, difficulty))
                gs.undo_move()
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else: # aims to minimize score
            min_eval = 9999
            for move in valid_moves:
                gs.make_move(move)
                min_eval = min(min_eval, self.minimax(gs, depth - 1, alpha, beta, True, difficulty))
                gs.undo_move()
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval
