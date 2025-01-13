shape_first_dimension = 9

save_Freq = 50
max_Rounds = 2000
start_Round= 119
learning_rate = 2e-4


mcts_pure_simulations =5000
check_freq = 0
evaluate_games=10
simulations=400
factor=5
train_exploration = 1e-1
dir = 0.1

trainDataPoolSize = 10000  # 用以存储训练网络的数据
trainBatchSize = 256  # 每次从数据池(trainDataPool)中随机采样出的一批训练数据
epochs = 10  # 每次训练步数


UseBorderStrengthen = False
UseDropArea = False
FirstStepSelectBorderDot = False
SelfCompeteVisual = False