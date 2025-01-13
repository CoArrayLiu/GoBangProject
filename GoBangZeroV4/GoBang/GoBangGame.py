import GoBang.config as config
import numpy as np
import GoBang.Board as Board


#约定： 1代表黑棋 2代表白棋
class GoBang:
    def __init__(self):
        self.board_size = config.BOARD_SIZE
        self.cur_player = config.BLACK
        self.board = np.zeros((self.board_size, self.board_size),dtype = int)
        self.line_board=Board.Board()
        self.line_board.initBoard()


    def convert_line_to_coordinate(self,index):
        '''
        eg.0 - (10,0)  11 -(9,0) 15 - (9,4)
        '''

        x=self.board_size - index//self.board_size -1
        y=index%self.board_size
        x,y = y,x
        return x,y

    def convert_coordinate_to_line(self,x,y):
        '''

        '''
        x, y = y, x
        index = (self.board_size-x-1)*self.board_size+y
        return index

    def restart(self):
        self.line_board.initBoard()
        self.cur_player = config.BLACK
        self.board = np.zeros((self.board_size, self.board_size),dtype = int)


    def check_win(self,x,y,player):
        #约定左上角为(0,0) 横向为x轴 纵向为y轴
        length = self.board_size
        #横向
        for j in range (y-4,y+1):
            if j<0 or j+4>=length :
                continue
            if np.array_equal(self.board[x][j:j+5],np.full(5,player)) :
                return True
        #纵向
        for i in range(x-4,x+1):
            if i<0 or i+4>=length :
                continue
            if np.array_equal([self.board[i+index][y] for index in range(5)],np.full(5,player)):
                return True

        #左上到右下方向
        for i in range(-4,1):
            if x+i<0 or y+i<0 or x+i+4>=length or y+i+4>=length:
                continue
            if np.array_equal([self.board[x+i+j][y+i+j] for j in range(5)], np.full(5,player)):
                return True

        #右上到左下
        for i in range(-4,1):
            if x+i<0 or y-i>=length or x+i+4>=length or y-i-4<0:
                continue
            if np.array_equal([self.board[x+i+j][y-i-j] for j in range(5)],np.full(5,player)):
                return True

        return False

    def placeable(self,x,y):
        if(x>=0 and x<self.board_size and y>=0 and y<self.board_size):
            return self.board[x][y]==0
        else:
            return False

    def place(self,x,y):
        self.line_board.do_move(self.convert_coordinate_to_line(x,y))
        self.board[x][y] = self.cur_player
        is_end = self.check_win(x,y,self.cur_player)
        if is_end :
            return True
        else:
            self.cur_player = 3 - self.cur_player
            return False


    def remove(self,x,y):
        self.board[x][y] = 0
        self.line_board.states.pop()


    def AI_play(self):
        pass

