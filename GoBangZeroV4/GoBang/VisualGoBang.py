#pvp pvc
#GoBang传入相关数据
#对局回放
import time

import GoBang.config as GBC
import Train.AIPlayer as ai
import Train.PolicyNN as PolicyNN
import GoBang.GoBangGame as GoBangGame
import pygame
import sys
import numpy as np
from pygame.locals import QUIT,KEYDOWN
import Train.config as TCF

#locals
black = GBC.BLACK
white = GBC.WHITE
board_size = GBC.BOARD_SIZE
piece_radius = 20
middle_dot_radius = 8
piece_interval = 2
edge_blank = 27
edge_line_width = 4
line_width=2


line_interval = 2*piece_radius+piece_interval
window_size = edge_blank*2+(board_size-1)*line_interval
middle_dot_pos = edge_blank+line_interval*int(board_size/2)

#color locals
screen_color=[238,154,73]
line_color = [0,0,0]
color_black = [0,0,0]
color_white = [255,255,255]



pygame.init()
screen = pygame.display.set_mode((window_size,window_size))

def convert_accurate_window_coordinate(x,y):
    for i in range(edge_blank,window_size,line_interval):
        for j in range(edge_blank,window_size,line_interval):
            L1=i-22
            L2=i+22
            R1=j-22
            R2=j+22
            if x>=L1 and x<=L2 and y>=R1 and y<=R2:
                return i,j
    return x,y

def convert_window_to_coordinate(x,y):
    for i in range(edge_blank,window_size,line_interval):
        for j in range(edge_blank,window_size,line_interval):
            L1=i-22
            L2=i+22
            R1=j-22
            R2=j+22
            if x>=L1 and x<=L2 and y>=R1 and y<=R2:
                x=int((i-edge_blank)/line_interval)
                y=int((j-edge_blank)/line_interval)
                return x,y
    return -1,-1


def convert_coordinate_to_window(x,y):
    x=edge_blank+line_interval*x
    y=edge_blank+line_interval*y
    return x,y

def draw_board(screen):
    #画棋盘线
    for i in range(edge_blank,window_size,line_interval):
        #竖线
        if i == edge_blank or i == window_size-edge_blank:
            pygame.draw.line(screen,line_color,(i,edge_blank),(i,window_size-edge_blank),edge_line_width)
        else:
            pygame.draw.line(screen,line_color,(i,edge_blank),(i,window_size-edge_blank),line_width)

        #横线
        if i == edge_blank or i == window_size-edge_blank:
            pygame.draw.line(screen, line_color, (edge_blank,i), (window_size-edge_blank, i), edge_line_width)
        else:
            pygame.draw.line(screen, line_color, (edge_blank, i), (window_size - edge_blank, i), line_width)

        # 在棋盘中心画个小圆表示正中心位置
        pygame.draw.circle(screen, color_black, [middle_dot_pos, middle_dot_pos], middle_dot_radius, 0)

def draw_one_piece(screen,x,y,player):
    x,y=convert_coordinate_to_window(x,y)
    if player == black:
        pygame.draw.circle(screen,color_black,(x,y),piece_radius,0)
    elif player == white:
        pygame.draw.circle(screen,color_white,(x,y),piece_radius,0)

def draw_pieces(screen,board):

    for (x, y), value in np.ndenumerate(board):
        if board[x,y] !=0:
            draw_one_piece(screen,x,y,board[x,y])



def player_vs_player():
    is_end=False
    game = GoBangGame.GoBang()
    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

        screen.fill(screen_color)  # 清屏

        draw_board(screen)

        draw_pieces(screen,game.board)

        #在鼠标位置显示下棋的位置
        x, y = pygame.mouse.get_pos()
        x, y = convert_accurate_window_coordinate(x, y)
        pygame.draw.rect(screen, [0, 229, 238], [x - 22, y - 22, 44, 44], 2, 1)

        mouse_pressed_pos = pygame.mouse.get_pressed()
        if mouse_pressed_pos[0] and not is_end:
            board_x,board_y=convert_window_to_coordinate(x,y)
            if game.placeable(board_x,board_y):
                is_end=game.place(board_x,board_y)



        pygame.display.update()  # 刷新显示

def player_vs_ai():
    player = GBC.test_pva_start
    Net = PolicyNN.PolicyValueNet((TCF.shape_first_dimension,board_size,board_size))
    Net.load_model(GBC.model)
    aiplayer = ai.AIPlayer(Net.policy_NN)


    is_end=False
    game=GoBangGame.GoBang()
    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()

        screen.fill(screen_color)  # 清屏

        draw_board(screen)

        draw_pieces(screen,game.board)

        if game.cur_player==player and not is_end:
            #在鼠标位置显示下棋的位置
            x, y = pygame.mouse.get_pos()
            x, y = convert_accurate_window_coordinate(x, y)
            pygame.draw.rect(screen, [0, 229, 238], [x - 22, y - 22, 44, 44], 2, 1)

            mouse_pressed_pos = pygame.mouse.get_pressed()
            if mouse_pressed_pos[0] and not is_end:
                board_x,board_y=convert_window_to_coordinate(x,y)
                if game.placeable(board_x,board_y):
                    is_end=game.place(board_x,board_y)
                pygame.display.flip()  # 更新屏幕
                continue



        if game.cur_player!=player and not is_end:
            if GBC.test_pva_use_mcts:
                move, _= aiplayer.getAction(game.line_board,False)
            else:
                move = aiplayer.getMove(game.line_board)

            x,y = game.convert_line_to_coordinate(move)
            print(move)
            print(x)
            print(y)
            is_end = game.place(x,y)

        pygame.display.flip()  # 更新屏幕






class VisualGoBang:
    def __init__(self):
        pass

    def pvp(self):
        player_vs_player()

    def pve(self):
        player_vs_ai()

class VisualAiCompete:
    def __init__(self):
        self.wait_moves=[]
        self.game = GoBangGame.GoBang()

    def reset(self):
        self.wait_moves=[]
        self.game.restart()

    def set_move(self,move):
        self.wait_moves.append(move)

    def ai_vs_ai(self):
        is_end = False
        while True:
            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                    sys.exit()

            screen.fill(screen_color)  # 清屏

            draw_board(screen)

            draw_pieces(screen, self.game.board)

            # 在鼠标位置显示下棋的位置
            if len(self.wait_moves)!=0:
                move = self.wait_moves.pop(0)
                x,y = self.game.line_board.convert_line_to_coordinate(move)
                if self.game.placeable(x,y):
                    is_end = self.game.place(x,y)

            pygame.display.update()  # 刷新显示
            time.sleep(1)

            if is_end:
                break










