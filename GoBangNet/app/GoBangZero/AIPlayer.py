import copy
from app.GoBangZero import GBC
import numpy as np
from app.GoBangZero import PolicyNN as PolicyNN
from app.GoBangZero import Board

class GoBangZeroV4():
    def __init__(self,model_file):
        self.model_file = model_file
        self.Net = PolicyNN.PolicyValueNet((GBC.shape_first_dimension,GBC.BOARD_SIZE,GBC.BOARD_SIZE))
        self.Net.load_model(model_file)
        self.policy_NN = self.Net.policy_NN

    def get_move(self,pieces):
        board = self.wrap(pieces)

        act_probs, _ = self.policy_NN(board)
        max_prob = -np.inf
        best_move = None

        for move, prob in act_probs:
            if prob > max_prob:
                max_prob = prob
                best_move = move

        return best_move

    def wrap(self,pieces):
        board = Board.Board()
        board.initBoard()
        for piece in pieces:
            board.do_move(piece)
        return board


# aiplayer = GoBangZeroV4(model_file='../model/15/314.model')
#
# print(aiplayer.get_move({}))
