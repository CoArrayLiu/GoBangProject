from PolicyNN import *
import Train.config as TCF
from GenerateTrainData import *
import tensorflow as tf
import os
import copy
from mcts_pure import MCTSPlayer as mctsPlayer
os.environ["CUDA_VISIBLE_DEVICES"] = '0'   #指定第一块GPU可用


class SelfCompete:
    def __init__(self):
        self.board_size = GBC.BOARD_SIZE
        self.playerNet = PolicyValueNet((4,self.board_size, self.board_size))
        self.player = AIPlay(self.playerNet.policy_NN)
        self.targetNet = None
        self.targetPlayer = None
        #每进行gamesPerRound局自我对弈就进行一次模型评估
        self.gamesPerRound = 10
        #模型评估让targetNet与playerNet对局evaluateGames次
        self.evaluateGames = 10
        #在evaluateGames对局中，胜率大于等于0.6更新playerNet
        self.updateModelRate = 0.6
        #记录自我对弈的数据进行训练
        self.playDataPool = []
        #如果超过gamesThrowExceptionNum局仍未更新，则进行异常处理
        self.gamesUntilLastUpdate = 0
        self.gamesThrowExceptionNum =100
        self.gamesSum =0

    def getMove(self, board, modelNet):
        act_probs, _ = modelNet.policy_NN(board)

        max_prob = -np.inf
        best_move = None

        for move, prob in act_probs:
            if prob > max_prob:
                max_prob = prob
                best_move = move

        return best_move

    def loadModel(self, modelFile):
        print(f'Loading model----{modelFile}')
        self.playerNet.load_model(modelFile)

    def saveModel(self, modelFile, which):
        print(f'Saving model----{modelFile}')
        if which == 1:
            self.playerNet.save_model(modelFile)
        if which == 2:
            self.targetNet.save_model(modelFile)

    def selfCompete(self):
        for game in range(self.gamesPerRound):
            self.gamesUntilLastUpdate += 1
            self.gamesSum += 1
            print(f"开始进行第{self.gamesUntilLastUpdate}轮对弈")
            self.player.resetBoard()
            winner, play_data = self.player.GenerateTrainData()
            print(f"本轮对弈胜者:{winner}")
            self.playDataPool.extend(self.playerNet.get_DataAugmentation(play_data))

    def trainTargetModel(self):
        print(f"开始训练TargetNet,训练数据数量{len(self.playDataPool)}")
        self.targetNet.update_net_extended(self.playDataPool)

    def evaluateTargetModel(self,mode):
        print("开始评估target模型")
        board = Board()
        win_num = 0
        movess=[]
        for game in range(self.evaluateGames):
            moves=[]
            board.initBoard()
            if game < 5:
                while True:
                    if mode ==1:
                        move = self.player.getMove(board)
                    else:
                        move = self.player.getNetMove(board)

                    board.do_move(move)
                    moves.append(move)
                    end, winner = board.has_a_winner()
                    if end:
                        print("winner:", winner)
                        break

                    if mode ==1:
                        move = self.targetPlayer.getMove(board)
                    else:
                        move = self.targetPlayer.getNetMove(board)
                    board.do_move(move)
                    moves.append(move)
                    end, winner = board.has_a_winner()
                    if end:
                        print("winner:", winner)
                        win_num += 1
                        break

            if game >= 5:
                while True:
                    if mode ==1:
                        move = self.targetPlayer.getMove(board)
                    else:
                        move = self.targetPlayer.getNetMove(board)
                    board.do_move(move)
                    moves.append(move)
                    end, winner = board.has_a_winner()
                    if end:
                        print("winner:", winner)
                        win_num += 1
                        break

                    if mode ==1:
                        move = self.player.getMove(board)
                    else:
                        move = self.player.getNetMove(board)
                    board.do_move(move)
                    moves.append(move)
                    end, winner = board.has_a_winner()
                    if end:
                        print("winner:", winner)
                        break
            movess.append(moves)
        print(movess)
        winRate = win_num / self.evaluateGames
        print(f"winRate:{str(winRate)}")
        return winRate

    def copyNet(self, Net):
        newNet = PolicyValueNet((4,self.board_size, self.board_size))
        newNet.model.set_weights(Net.model.get_weights())
        return newNet

    def eliminateOne(self):
        self.targetNet = self.copyNet(self.playerNet)
        self.trainTargetModel()
        self.targetPlayer = AIPlay(self.targetNet.policy_NN)
        win_rate = self.evaluateTargetModel()
        print("胜率:" + str(win_rate))
        if win_rate >= self.updateModelRate:
            self.playerNet = self.copyNet(self.targetNet)
            print("playerNet采用targetNet")
            self.playDataPool = []
            self.gamesUntilLastUpdate = 0
            return True
        else:
            if win_rate>=0.0:
                self.saveModel(f"../model/15/targetcopy/{str(self.gamesSum)}+{str(win_rate)}.model", 2)
            print("不更新")
            return False

    def mainRound(self, modelFile=None):
        if modelFile is not None:
            self.loadModel(modelFile)
        while self.gamesUntilLastUpdate < self.gamesThrowExceptionNum:
            self.selfCompete()
            self.eliminateOne()
        print("多次未更新model,异常退出")




class Train:
    save_freq = TCF.save_Freq
    max_rounds = TCF.max_Rounds
    start_round = TCF.start_Round
    board_size = GBC.BOARD_SIZE


    def __init__(self):
        self.Net = PolicyValueNet((4,self.board_size, self.board_size))
        self.ai = AIPlay(self.Net.policy_NN)
        self.data_reader = DataReader()
        if self.start_round != 0:
            self.Net.load_model(f"../model/self-{str(self.board_size)}/{str(self.start_round)}.model")
            print(f"../model/self-{str(self.board_size)}/{str(self.start_round)}.model")
            print("load model")


    def train(self):
        Loss=[]

        for game in range(self.max_rounds):
            if game<self.start_round:
                continue
            print(f"开始进行第{game+1}轮对弈")
            self.ai.resetBoard()
            winner, play_data = self.ai.GenerateTrainData()

            if TCF.SelfCompeteVisual:
                self.ai.visualer.ai_vs_ai()

            print("winner ："+str(winner))

            self.Net.memory(play_data)

            if len(self.Net.trainDataPool) > self.Net.trainBatchSize:
                loss = self.Net.update()
                print("loss: "+str(loss))
                self.Net.save_model(f"../model/self-{str(self.board_size)}/{str(game+1)}.model")
                print("保存模型")
            else:
                print("len(trainDataPool):"+str(len(self.Net.trainDataPool)))
                print("trainBatchSize:"+str(self.Net.trainBatchSize))
                print("收集训练数据: %d%%" % (len(self.Net.trainDataPool) / self.Net.trainBatchSize * 100))

            if (game+1) % self.save_freq == 0:
                self.Net.save_model(f"../model/self-{str(self.board_size)}/{str(game+1)}.model")
                print("保存模型")


class Train_of_data:
    board_size = GBC.BOARD_SIZE

    def __init__(self):
        self.Net = PolicyValueNet((4,self.board_size, self.board_size))
        self.data_reader = DataReader()


    def train_of_batch(self,fileIndex):
        train_set = self.data_reader.read_batch_data(fileIndex)
        batch_size = TCF.trainBatchSize
        data_num = len(train_set[0][0])

        print(data_num)
        print(len(train_set[0][1]))
        print(len(train_set[0][2]))

        batches = data_num // batch_size
        Loss=[]
        print(f"本次学习数据量:{data_num}，划分{batches}批次，每批次数量:{batch_size}。")


        for index in range(1,batches+1):
            print(f"开始学习第{index}/{batches}批次")
            slice_train_set = [[lst[(index-1)*batch_size:index*batch_size] for lst in t] for t in train_set]
            slice_train_set = slice_train_set[0]
            loss = self.Net.update_of_board(slice_train_set)
            Loss.append(loss)
            print("本批次loss:"+str(loss))
            self.Net.save_model(f"../model/{str(self.board_size)}/9.model")

    def train_of_extended_batch(self,fileIndex):
        if os.path.getsize(f"../train_data/{str(fileIndex)}.txt") == 0:
            return

        train_set = self.data_reader.read_extended_batch_data(fileIndex)
        train_set = self.Net.get_DataAugmentation(train_set)


        batch_size = TCF.trainBatchSize
        data_num = len(train_set)

        print(data_num)

        batches = data_num // batch_size
        Loss=[]
        print(f"本次学习数据量:{data_num}，划分{batches}批次，每批次数量:{batch_size}。")


        for index in range(1,batches+1):
            print(f"开始学习第{index}/{batches}批次")
            loss = self.Net.update_net_extended(train_set[(index-1)*batch_size:index*batch_size])
            Loss.append(loss)
            print("本批次loss:"+str(loss))

        self.Net.save_model(f"../model/{str(self.board_size)}/{fileIndex}.model")



    def train_of_boards(self,rounds):
        train_set = self.data_reader.read_data()
        batch_size = len(train_set)
        start = TCF.start_Round
        Loss = []
        for i in range(rounds+start):
            if i<start:
                continue
            print(f"第{i+1}/{rounds+start}轮训练")
            for data in train_set:
                loss=self.Net.update_of_board(data)
                Loss.append(loss)

        self.Net.save_model(f"../model/{str(self.board_size)}/{str(rounds+start)}.model")


if __name__ == '__main__':
    # trainer = Train()
    # trainer.train()

    trainer = Train_of_data()
    trainer.Net.load_model("../model/15/127.model")
    for index in range(128,366,1):
        trainer.train_of_extended_batch(index)

    # SC = SelfCompete()
    # SC.playerNet.load_model("../model/15/181.model")
    # SC.targetNet = PolicyValueNet((4,SC.board_size,SC.board_size))
    # SC.targetNet.load_model("../model/self-15/500.model")
    # SC.targetPlayer = AIPlay(SC.targetNet.policy_NN)
    # SC.evaluateTargetModel(2)

