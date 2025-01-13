BOARD_SIZE = 15
BLACK = 1
WHITE = 2
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def find_six_consecutive_empty(board):
    empty_positions = []

    # 检查横向
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - 5):  # 只需检查到第 10 列
            if all(board[r][c + i] == 0 for i in range(6)):  # 检查六个连续空位
                empty_positions.append([(r, c + i) for i in range(6)])

    # 检查纵向
    for r in range(BOARD_SIZE - 5):
        for c in range(BOARD_SIZE):
            if all(board[r + i][c] == 0 for i in range(6)):  # 检查六个连续空位
                empty_positions.append([(r + i, c) for i in range(6)])

    # 检查斜向（左上到右下）
    for r in range(BOARD_SIZE - 5):
        for c in range(BOARD_SIZE - 5):
            if all(board[r + i][c + i] == 0 for i in range(6)):  # 检查六个连续空位
                empty_positions.append([(r + i, c + i) for i in range(6)])

    # 检查斜向（右上到左下）
    for r in range(BOARD_SIZE - 5):
        for c in range(5, BOARD_SIZE):
            if all(board[r + i][c - i] == 0 for i in range(6)):  # 检查六个连续空位
                empty_positions.append([(r + i, c - i) for i in range(6)])

    return empty_positions

def check_four():
    pass


def find_four_consecutive_empty(board):
    empty_positions = []

    # 检查横向
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - 3):  # 只需检查到第 12 列
            if all(board[r][c + i] == 0 for i in range(4)):  # 检查四个连续空位
                empty_positions.append([(r, c + i) for i in range(4)])

    # 检查纵向
    for r in range(BOARD_SIZE - 3):
        for c in range(BOARD_SIZE):
            if all(board[r + i][c] == 0 for i in range(4)):  # 检查四个连续空位
                empty_positions.append([(r + i, c) for i in range(4)])

    # 检查斜向（左上到右下）
    for r in range(BOARD_SIZE - 3):
        for c in range(BOARD_SIZE - 3):
            if all(board[r + i][c + i] == 0 for i in range(4)):  # 检查四个连续空位
                empty_positions.append([(r + i, c + i) for i in range(4)])

    # 检查斜向（右上到左下）
    for r in range(BOARD_SIZE - 3):
        for c in range(3, BOARD_SIZE):
            if all(board[r + i][c - i] == 0 for i in range(4)):  # 检查四个连续空位
                empty_positions.append([(r + i, c - i) for i in range(4)])

    return empty_positions

def generate_win():
    six_positions = find_six_consecutive_empty(board)
    moves
    for six_pos in six_positions:
        for pos in six_pos:
            y,x = six_pos[0],six_pos[1]
