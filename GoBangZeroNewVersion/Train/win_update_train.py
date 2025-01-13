from PolicyNN import *
import Train.config as TCF
from GenerateTrainData import *
import tensorflow as tf
import os
import copy
from mcts_pure import MCTSPlayer as mctsPlayer
os.environ["CUDA_VISIBLE_DEVICES"] = '0'   #指定第一块GPU可用


class selfCompete:
    def __init__(self):

        self.mcts_simulations = TCF.mcts_pure_simulations
        self.board_size = GBC.BOARD_SIZE
        self.current_net = PolicyValueNet((4,self.board_size,self.board_size))
        self.current_player = AIPlay(self.current_net.policy_NN)
        self.best_net = None
        self.mcts_player = mctsPlayer(n_playout=self.mcts_simulations)

        self.win_rate = 0
        self.evaluate_games = TCF.evaluate_games


        self.data_buffer = deque(maxlen = TCF.trainDataPoolSize)
        self.epochs = 5
        self.check_freq = TCF.check_freq

        self.current_net.load_model(f"../model/currentModel/current_model_{self.mcts_simulations}.model")

    def compete(self,n_games):
        for _ in range(n_games):
            print(f"第{_+1}轮自对弈")
            self.current_player.resetBoard()
            winner,play_data = self.current_player.GenerateTrainData()
            self.data_buffer.extend(self.current_net.get_DataAugmentation(play_data))
            self.current_player.resetBoard()


    def update_net(self):
        batch_size = TCF.trainBatchSize
        batches = int(len(self.data_buffer)/batch_size)

        for i in range(1,batches+1):
            self.current_net.update_net_extended(random.sample(self.data_buffer,batch_size))

    def compete_with_mcts(self):
        print("开始评估")
        num_win = 0

        for game_index in range(self.evaluate_games):
            print(f"第{game_index+1}轮评估")
            board = Board()
            board.initBoard()

            if game_index%2 == 0:
                players = [0,self.current_player,self.mcts_player]
            else:
                players = [0, self.mcts_player, self.current_player]

            while True:
                player_in_turn = board.getCurrentPlayer()
                move = players[player_in_turn].get_action(board)
                print(f"{player_in_turn}: {move}")
                board.do_move(move)

                end,winner = board.gameIsOver()
                if end:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                        if game_index%2 == 0 and winner == 1:
                            num_win+=1
                        if game_index%2 == 1 and winner == 2:
                            num_win+=1
                        break
                    else:
                        print("Game end. Tie")

        return num_win / self.evaluate_games


    def copyNet(self, Net):
        newNet = PolicyValueNet((4,self.board_size, self.board_size))
        newNet.model.set_weights(Net.model.get_weights())
        return newNet

    def run(self):
        while True:
            self.compete(self.check_freq)
            self.update_net()
            win_rate = self.compete_with_mcts()
            if win_rate > self.win_rate:
                self.win_rate = win_rate
                print("get new best net")
                print("win_rate:"+str(self.win_rate))
                self.best_net = self.copyNet(self.current_net)
                self.current_net.save_model(f"../model/currentModel/current_model_{self.mcts_simulations}.model")
                self.best_net.save_model(f"../model/bestModel/best_model_{self.mcts_simulations}_{self.win_rate}.model")
                if win_rate > 0.91:
                    self.mcts_simulations *= 1.3
                    print(f"新的mcts模拟次数{self.mcts_simulations}")

            else:
                self.current_net.save_model(f"../model/currentModel/current_model_{self.mcts_simulations}.model")
                print("not update")


trainer = selfCompete()
trainer.run()


