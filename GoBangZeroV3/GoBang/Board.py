import GoBang.config as GBC
#from __future__ import print_function
import numpy as np
from collections import deque
import Train.config as TCF
'''
Board类
方便进行训练创建的线性存储棋盘的数据结构
包含的数据: 
1、board_size 2、current_player 3、states {line-position:player} 4、availables (line-position...)
方法:
1、init_board() 清空棋盘信息
2、do_move(move:line-position)  放置棋子，在availables中删除位置，更换棋手
3、gameIsOver()  返回是否结束(bool)以及胜者(player\-1)
4、current_state()  
    返回四层棋盘 
    第一层记录当前玩家所有落子
    第二层记录对手玩家所有落子
    第三层记录最后一次落子 (落子位置为1，其他位置都为0)
    第四层当前玩家的行棋顺序(先手都设为1，后手都设为0)
'''

class Board:
    """
    棋盘
    """

    def __init__(self, n_in_row=5):
        # 设置棋盘的长宽
        self.board_size = GBC.BOARD_SIZE
        self.black = GBC.BLACK
        self.white = GBC.WHITE
        self.n_in_row=5
        # 棋盘状态《states》存储在dict中
        # key: 棋盘上的落子行为 value: 玩家
        # {38: 1, 23: 2, 24: 1, 36: 2, ··· }
        # 玩家1 落子 38 位置
        # 玩家2 落子 23 位置 ···
        self.states = {}
        self.drop_area=[]
        self.border=GBC.BORDER
        self.drop_deque = deque(maxlen=3)



    def initBoard(self, start_player=0):
        """
        初始化棋盘
        start_player: 先手玩家
        """

        # 当前玩家设置
        #   默认先手的是玩家1
        self.current_player = self.black

        # 在列表中保留还没有落子的位置
        self.availables = list(range(self.board_size*self.board_size))
        self.states = {}

        # 刚刚落子的情况
        self.last_move = -1
        self.drop_area = []
        self.drop_deque.clear()
        self.board = np.zeros((self.board_size, self.board_size))

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

    def update_drop_area(self,index):
        '''
        在棋盘上柚子区域周围border格进行搜索
        '''
        x,y = self.convert_line_to_coordinate(index)
        if(index in self.drop_area):
            self.drop_area.remove(index)
        for i in range(x-self.border,x+self.border+1):
            for j in range(y-self.border,y+self.border+1):
                if i<0 or i>=self.board_size or j<0 or j>=self.board_size:
                    continue
                else:
                    new_index = self.convert_coordinate_to_line(i, j)
                    if new_index in self.availables and new_index not in self.drop_area :
                        self.drop_area.append(new_index)




    def current_state(self):
        """
        以当前 玩家player 角度返回当前棋盘
        """
        # 使用 9*board_size*board_size 存储棋盘的状态
        square_state = np.zeros((TCF.shape_first_dimension, self.board_size, self.board_size))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            # moves 数组记录着两个玩家交错的落子位置

            move_curr = moves[players == self.current_player]  # 当前玩家落子的位置
            move_oppo = moves[players != self.current_player]  # 对手玩家落子的位置

            square_state[0][move_curr // self.board_size, move_curr % self.board_size] = 1.0  # 当前玩家所有落子棋盘
            square_state[1][move_oppo // self.board_size, move_oppo % self.board_size] = 1.0  # 对手玩家所有落子棋盘

            # 标记最近三次落子位置
            square_state[2][self.last_move // self.board_size, self.last_move % self.board_size] = 1.0

            if len(self.drop_deque)>=2:
                square_state[3][self.drop_deque[-2] // self.board_size, self.drop_deque[-2] % self.board_size] = 1.0

                if len(self.drop_deque)>=3:
                    square_state[4][self.drop_deque[-3] // self.board_size, self.drop_deque[-3] % self.board_size] = 1.0

        if len(self.states) % 2 == 0:
            square_state[5][:, :] = 1.0

        # 标记我方连子
        l_3,s_4,l_4 = self.find_patterns()
        square_state[6] = l_3
        square_state[7] = s_4
        square_state[8] = l_4


        return square_state[:, ::-1, :]

    def do_move(self, move):
        """
        落子
        move：落子的位置 一个整数 0 ~ H*W-1
        """

        self.states[move] = self.current_player
        self.availables.remove(move)  # 减少一个可以落子的位置
        self.update_drop_area(move)
        self.drop_deque.append(move)
        x,y = self.convert_line_to_coordinate(move)
        self.board[y][x] = self.current_player
        # 切换玩家角色
        self.current_player = 3-self.current_player
        self.last_move = move  # 记录上一次落子的位置



    def has_a_winner(self):
        """
        判断是否比出输赢
        """
        width = self.board_size
        height = self.board_size
        states = self.states
        n = self.n_in_row

        moved = list(set(range(width * height)) - set(self.availables))
        if len(moved) < self.n_in_row * 2 - 1:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player

            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player

            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player

            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def gameIsOver(self):
        """
        判断游戏是否结束
        """
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.availables):
            return True, -1
        return False, -1

    def end(self):
        win, winner = self.has_a_winner()
        return win


    def getCurrentPlayer(self):
        return self.current_player

    def reversePlayer(self):
        self.current_player = 3 - self.current_player


    def convert_index_to_standard(self,move):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
        line = ""
        x, y = self.convert_line_to_coordinate(move)
        line += letters[x]
        line += str(15 - y)
        return line

    def find_patterns(self):
        BOARD_SIZE = 15
        board = self.board

        # 新建三个标记棋盘，初始为0
        live_three_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        semi_live_four_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        live_four_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        def check_pattern(start_x, start_y, dx, dy):
            x, y = start_x, start_y
            count = 0
            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == self.current_player:
                count += 1
                x += dx
                y += dy

            if count < 3 or count > 4:
                return None, []

            if count == 3:
                # 检查两端是否有足够的空位
                x, y = start_x - dx, start_y - dy
                left_empty = right_empty = 0

                while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == 0:
                    left_empty += 1
                    x -= dx
                    y -= dy

                x, y = start_x + count * dx, start_y + count * dy
                while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == 0:
                    right_empty += 1
                    x += dx
                    y += dy

                if left_empty >= 2 and right_empty >= 1:
                    return 'live_three', [(start_x + step * dx, start_y + step * dy) for step in range(count)]

                if left_empty >= 1 and right_empty >= 2:
                    return 'live_three', [(start_x + step * dx, start_y + step * dy) for step in range(count)]

            elif count == 4:
                # 检查两端是否有足够的空位
                x, y = start_x - dx, start_y - dy
                left_empty = 0
                while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == 0:
                    left_empty += 1
                    x -= dx
                    y -= dy

                x, y = start_x + count * dx, start_y + count * dy
                right_empty = 0
                while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == 0:
                    right_empty += 1
                    x += dx
                    y += dy

                if left_empty >= 1 and right_empty >= 1:
                    return 'live_four', [(start_x + step * dx, start_y + step * dy) for step in range(count)]
                elif left_empty >= 1 or right_empty >= 1:
                    return 'semi_live_four', [(start_x + step * dx, start_y + step * dy) for step in range(count)]

            return None, []

        # 记录所有连珠
        all_patterns = {
            'live_three': set(),
            'semi_live_four': set(),
            'live_four': set()
        }

        # 搜索所有可能的方向
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == self.current_player:
                    for dx, dy in directions:
                        pattern_type, positions = check_pattern(x, y, dx, dy)
                        if pattern_type is not None:
                            all_patterns[pattern_type].update(positions)

        # 根据记录的信息标记连珠
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if (x, y) in all_patterns['live_four']:
                    live_four_board[x][y] = 3
                if (x, y) in all_patterns['live_three']:
                    live_three_board[x][y] = 1
                if (x, y) in all_patterns['semi_live_four']:
                    semi_live_four_board[x][y] = 2

        return live_three_board, semi_live_four_board, live_four_board
