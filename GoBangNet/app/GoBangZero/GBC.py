BOARD_SIZE = 15
BLACK = 1
WHITE = 2
BORDER = 3



shape_first_dimension = 11
learning_rate = 2e-4

save_Freq = 50
max_Rounds = 2000
start_Round= 1



mcts_pure_simulations =5000
check_freq = 0
evaluate_games=10
simulations=400
factor=5
train_exploration = 1.e-1
dir = 0.1  #dir_noise 随机噪声

trainDataPoolSize = 10000  # 用以存储训练网络的数据
trainBatchSize = 512  # 每次从数据池(trainDataPool)中随机采样出的一批训练数据
epochs = 10  # 每次训练步数


UseBorderStrengthen = False
UseDropArea = False  #禁用
FirstStepSelectBorderDot = False
SelfCompeteVisual = False