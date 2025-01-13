data_folder = "../train_data"
from Train.parser import read_data
from GoBang.Board import Board
import GoBang.config as GBC
board_size = GBC.BOARD_SIZE
border = 1
import copy
max_depth = 2


def StrengthenFile(FileIndex):
    games_index = read_data(FileIndex)
    Sum = len(games_index)
    find_num=0
    for game_moves in games_index:
        win_moves = StrgthenData(game_moves)
        if len(win_moves) == 0:
            print("没找到赢法")
        else:
            find_num+=1
            #print(game_moves)
            print(win_moves)

    print(f"{find_num}/{Sum}")


def StrgthenData(game_moves):
    #board = [[0 for _ in range(board_size)] for _ in range(board_size)]

    line_board = Board()
    line_board.initBoard()

    for index in game_moves:
        line_board.do_move(index)

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






StrengthenFile(1)



