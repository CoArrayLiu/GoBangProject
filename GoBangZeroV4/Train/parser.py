import re
from GoBang.Board import *

letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']


def read_data(fileindex):
    filename="../train_data/"+str(fileindex)+".txt"
    l=[]
    games_index = []
    board = Board()
    with open(filename,'r') as f:
        for line in f:
            l.append(line)

    for line in l:
        game_index=[]
        paired_data = re.findall(r'[a-zA-Z]\d+', line)
        for pair in paired_data:
            letter = pair[0]
            num = int(pair[1:])
            x=letters.index(letter)
            y=board.board_size-num
            index = board.convert_coordinate_to_line(x,y)
            game_index.append(index)
        games_index.append(game_index)

    return games_index






def read_boards():
    file = "../train_data.txt"
    l = []

    with open(file,"r") as f:
        for line in f:
            l.append(line)

    boards = []
    games_index = []
    games_xy=[]

    for line in l:
        board =Board()
        board.initBoard()
        game_index = []
        game_xy = []
        paired_data = re.findall(r'[a-zA-Z]\d+', line)



        for pair in paired_data:
            #print(pair)
            letter = pair[0]
            num = int(pair[1:])
            x=letters.index(letter)
            y=board.board_size-num
            game_xy.append((x,y))
            #print(x,y)
            index = board.convert_coordinate_to_line(x,y)
            game_index.append(index)
            #print(index)
            board.do_move(index)
        #print(board.states)
        end,_ = board.gameIsOver()
        if end:
            boards.append(board)
            games_index.append(game_index)
            games_xy.append(game_xy)

    return games_index




