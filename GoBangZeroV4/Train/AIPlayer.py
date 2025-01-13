from Train.MCTS import *
import Train.config as config
from GoBang import config as GBC
import copy

class AIPlayer():
    def __init__(self,policy_NN):
        self.simulations = config.simulations
        self.factor = config.factor
        self.board_size = GBC.BOARD_SIZE
        self.policy_NN = policy_NN

        self.MCTS = MCTS(policy_NN,self.factor,self.simulations)

    def resetMCTS(self):
        self.MCTS.updateMCTS(-1)

    def getAction(self,board,flag_is_train):
        emptySpacesBoard = board.availables

        kill_move = None
        killed_move = None
        end = False

        for pos in emptySpacesBoard:
            new_board = copy.deepcopy(board)
            new_board.do_move(pos)
            end, b = new_board.has_a_winner()
            if end:
                kill_move = pos
                print(f"发现杀棋:{kill_move}")
                break

        if not end:
            for pos in emptySpacesBoard:
                new_board = copy.deepcopy(board)
                new_board.reversePlayer()
                new_board.do_move(pos)
                end,b = new_board.has_a_winner()
                if end:
                    killed_move = pos
                    print(f"发现被杀棋:{pos}")
                    break
        move_probs = np.zeros(self.board_size*self.board_size)


        if end:
            if kill_move !=None:
                move_probs[kill_move] = 1.0
                self.MCTS.updateMCTS(kill_move)
                return kill_move, move_probs
            else:
                move_probs[killed_move] = 1.0
                self.MCTS.updateMCTS(killed_move)
                return killed_move, move_probs


        if len(emptySpacesBoard) > 0:
            acts,probs = self.MCTS.getMoveProbs(board,flag_is_train)
            move_probs[list(acts)] = probs

            if len(board.new_drop_area)!=0:
                if flag_is_train:
                    valid_acts = [act for act in acts if act in board.new_drop_area]
                    valid_probs = [probs[i] for i, act in enumerate(acts) if act in valid_acts]
                    valid_probs = np.array(valid_probs)
                    valid_probs = valid_probs / valid_probs.sum()
                    dirichlet_dist = np.random.dirichlet(TCF.dir * np.ones(len(valid_probs)))
                    move = np.random.choice(
                        valid_acts,
                        p=0.75 * valid_probs + 0.25 * dirichlet_dist
                    )
                    self.MCTS.updateMCTS(move)
                else:
                    move = np.random.choice(acts, p=probs)
                    # 重置 MCTS
                    self.MCTS.updateMCTS(-1)

            else:
                if flag_is_train:
                    move = np.random.choice( # 随机抽取
                        acts, # 落子行为
                        p=0.75*probs + 0.25*np.random.dirichlet(TCF.dir*np.ones(len(probs)))
                    )
                    self.MCTS.updateMCTS(move)
                else:
                    # 非训练
                    # ------------------------------------
                    # 更新根节点并使用默认的temp=1e-3重用搜索树
                    # 这几乎等同于选择prob最高的移动
                    move = np.random.choice(acts, p=probs)
                    # 重置 MCTS
                    self.MCTS.updateMCTS(-1)

            return move,move_probs

        else:
            print("Board is full")

    def get_move(self,board):
        act_probs,_ = self.policy_NN(board)

        max_prob = -np.inf
        best_move = None

        for move, prob in act_probs:
            if prob > max_prob:
                max_prob = prob
                best_move = move

        return best_move,act_probs

    def getMove(self,board):
        act_probs,_ = self.policy_NN(board)


        max_prob = -np.inf
        best_move = None

        for move, prob in act_probs:
            if prob > max_prob:
                max_prob = prob
                best_move = move

        return best_move