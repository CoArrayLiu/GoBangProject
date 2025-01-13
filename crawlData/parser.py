import re
from  Board import *
import copy
import sys


letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
board_size = 15
max_depth = 2




def revise_data(fileindex):
    filename="./train_data/"+str(fileindex)+".txt"
    l=[]
    board = Board()
    with open(filename,'r') as f:
        for line in f:
            l.append(line)

    new_line = []

    for line in l:
        game_index = []
        paired_data = re.findall(r'[a-zA-Z]\d+', line)
        for pair in paired_data:
            letter = pair[0]
            num = int(pair[1:])
            x=letters.index(letter)
            y=board.board_size-num
            index = board.convert_coordinate_to_line(x,y)
            #print(index,end=" ")
            game_index.append(index)
        #print(" ")
        win_moves = StrgthenData(game_index)
        if win_moves==None:
            print("已经结束哩")
            new_line.append(line)
            continue
        if len(win_moves)==0:
            print("没找到赢法")
            continue
        else:
            print(win_moves)
            line = line.strip()
            for move in win_moves:
                x,y = Board().convert_line_to_coordinate(move)
                line += letters[x]
                line += str(15-y)
            print(line)
            new_line.append(line)

    new_file = f"./train_data_1/"+str(fileindex)+".txt"
    with open(new_file,'w') as f:
        f.write("\n".join(line for line in new_line))

def StrgthenData(game_moves):
    #board = [[0 for _ in range(board_size)] for _ in range(board_size)]

    line_board = Board()
    line_board.initBoard()

    for index in game_moves:
        line_board.do_move(index)

    if line_board.end():
        return None

    win_moves = []

    def find_end(board,depth,win_moves):
        if depth > max_depth:
            return False
        for move in board.drop_area:
            board_next = copy.deepcopy(board)
            board_next.do_move(move)
            win_moves.append(move)
            if board_next.end():
                return True
            else:
                result = find_end(board_next,depth+1,win_moves)
                if result:
                    return True
                win_moves.remove(move)

        return False

    have_end = find_end(line_board,1,win_moves)

    return win_moves



if __name__ == '__main__':
    start = sys.argv[1]
    end = sys.argv[2]
    for i in range(int(start),int(end)+1):
        revise_data(i)