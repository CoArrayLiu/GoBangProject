from AIPlayer import  *
from GoBang.Board import *
import Train.parser as TP
import Train.config as TCF
import random
import threading
import multiprocessing


if TCF.SelfCompeteVisual:
    from GoBang.VisualGoBang import *

class AIPlay:
    def __init__(self,policy_NN):
        self.policy_NN = policy_NN
        self.player = AIPlayer(policy_NN)
        self.board = Board()
        self.board.initBoard()
        if TCF.SelfCompeteVisual:
            self.visualer = VisualAiCompete()



    def resetBoard(self):
        self.board.initBoard()

    def random_coordinate(self):
        range_choice = random.choice([(0, 2), (12, 14)])
        x = random.randint(range_choice[0], range_choice[1])
        y = random.randint(range_choice[0], range_choice[1])
        return x,y

    def getMove(self,board):
        move, move_probs = self.player.getAction(board,flag_is_train=False)
        return move

    def get_action(self,board):
        move, move_probs = self.player.getAction(board,flag_is_train= False)
        return move

    def getNetMove(self,board):
        act_probs,_ = self.policy_NN(board)


        max_prob = -np.inf
        best_move = None

        for move, prob in act_probs:
            if prob > max_prob:
                max_prob = prob
                best_move = move

        return best_move


    def GenerateTrainData(self):
        if TCF.SelfCompeteVisual:
            self.visualer.reset()

        boards, probs, currentPlayer = [], [], []
        self.board.initBoard()

        if TCF.FirstStepSelectBorderDot:
            x,y = self.random_coordinate()
            move = self.board.convert_coordinate_to_line(x,y)
            print(f"1:{move}")
            self.board.do_move(move)
            self.board.update_new_drop_area(move)
            if TCF.SelfCompeteVisual:
                self.visualer.set_move(move)

        one_game = ""
        while True:
            move, move_probs = self.player.getAction(self.board,flag_is_train=True)
            #move, move_probs = self.player.get_move(self.board)
            boards.append(self.board.current_state())
            probs.append(move_probs)
            currentPlayer.append(self.board.current_player)



            line = self.board.convert_index_to_standard(move)
            print(f'{self.board.current_player}: {move}  /  {line}')
            one_game += line
            self.board.do_move(move)
            self.board.update_new_drop_area(move)

            if TCF.SelfCompeteVisual:
                self.visualer.set_move(move)


            gameOver, winner = self.board.gameIsOver()

            if gameOver:
                # 根据最终游戏的结果，构造用于训练神经网络的《标签》Z
                winners_z = np.zeros(len(currentPlayer))
                print(f"本轮游戏长度:{len(currentPlayer)}")
                print("本轮游戏进度:"+one_game)

                with open("../record/record.txt", 'a', encoding='utf-8') as file:
                    file.write(line+'\n')
                    print("对局已记录")

                if winner != -1:
                    winners_z[np.array(currentPlayer) == winner] = 1.0
                    winners_z[np.array(currentPlayer) != winner] = -1.0

                # 重新设置MCTS，初始化了整棵树
                self.player.resetMCTS()

                return winner, zip(boards, probs, winners_z)


class DataReader:

    def read_batch_data(self,fileIndex):
        games_index = TP.read_data(fileIndex)
        train_set = []
        first = True
        for game in games_index:
            boards, probs, current_player = [],[],[]
            board = Board()
            board.initBoard()
            for move in game:
                boards.append(board.current_state())
                prob = np.zeros(board.board_size*board.board_size)
                prob[move] = 1.0
                probs.append(prob)
                current_player.append(board.current_player)
                board.do_move(move)

            rounds = len(game)
            if rounds%2==0:
                winner = board.white
            else:
                winner = board.black

            winners_z = np.zeros(len(game))
            if winner != -1:
                winners_z[np.array(current_player) == winner] = 1.0
                winners_z[np.array(current_player) != winner] = -1.0


            if first :
                train_set.append([boards, probs, winners_z])
                first = False
                continue

            train_set[0][0].extend(boards)
            train_set[0][1].extend(probs)
            #print(len(train_set[0][2]),len(winners_z))
            train_set[0][2]=np.append(train_set[0][2], winners_z)


        return train_set


    def read_extended_batch_data(self,fileIndex):
        games_index = TP.read_data(fileIndex)
        train_set = []
        first = True
        for game in games_index:
            print(game)
            boards, probs, current_player = [],[],[]
            board = Board()
            board.initBoard()
            for move in game:
                boards.append(board.current_state())
                prob = np.zeros(board.board_size*board.board_size)
                prob[move] = 1.0
                probs.append(prob)
                current_player.append(board.current_player)
                board.do_move(move)

            rounds = len(game)
            if rounds%2==0:
                winner = board.white
            else:
                winner = board.black

            winners_z = np.zeros(len(game))
            if winner != -1:
                winners_z[np.array(current_player) == winner] = 1.0
                winners_z[np.array(current_player) != winner] = -1.0


            if first :
                train_set.append([boards, probs, winners_z])
                first = False
                continue

            train_set[0][0].extend(boards)
            train_set[0][1].extend(probs)
            #print(len(train_set[0][2]),len(winners_z))
            train_set[0][2]=np.append(train_set[0][2], winners_z)


        return zip(train_set[0][0], train_set[0][1], train_set[0][2])




    def read_data(self):
        train_set = []
        #board,prob,winners_z
        games_index = TP.read_boards()
        for game in games_index:
            boards, probs, current_player = [], [], []

            board = Board()
            board.initBoard()

            for move in game:
                boards.append(board.current_state())
                prob = np.zeros(board.board_size*board.board_size)
                prob[move] = 1.0
                probs.append(prob)
                current_player.append(board.current_player)
                board.do_move(move)

            gameOver, winner = board.gameIsOver()

            if gameOver:
                winners_z = np.zeros(len(game))
                if winner != -1:
                    winners_z[np.array(current_player) == winner] = 1.0
                    winners_z[np.array(current_player) != winner] = -1.0

            train_set.append((boards, probs, winners_z))

        return train_set


class SpecificDataGenerator:
    #生成特定类型的训练数据



    def EnemyFourPiecesConnectedInBorder(self):
        #生成左上象限的数据
        pass

    def EnemyThreePiecesConnectedBeforeUs(self):
        pass