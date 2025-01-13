current_player = 2
def find_patterns(board):
    BOARD_SIZE = 15

    # 新建三个标记棋盘，初始为0
    live_three_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    semi_live_four_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    live_four_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def check_pattern(start_x, start_y, dx, dy):
        x, y = start_x, start_y
        count = 0
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[x][y] == current_player:
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
            if board[x][y] == current_player:
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


# 示例棋盘
board = [
    [0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
]
from GoBang import Board

aboard = Board.Board()
aboard.initBoard()
aboard.do_move(112)
aboard.do_move(118)
aboard.do_move(113)
aboard.do_move(119)
aboard.do_move(114)
aboard.do_move(120)
aboard.do_move(111)
aboard.do_move(121)
live_three_board, semi_live_four_board, live_four_board = aboard.find_patterns()
cr = aboard.current_state()
print(cr.shape)
for id,chess in enumerate(cr):
    print(f"layer{id+1}")
    print(chess)
print(cr)
print("Board:")
for row in aboard.board:
    print(row)


print("Live Three Board:")
for row in live_three_board:
    print(row)

print("\nSemi-Live Four Board:")
for row in semi_live_four_board:
    print(row)

print("\nLive Four Board:")
for row in live_four_board:
    print(row)