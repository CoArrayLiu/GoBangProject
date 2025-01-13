import os
import shutil

def process_files(source_folder, target_folder):
    index = 0
    # 创建目标文件夹，如果不存在的话
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        if filename.endswith('.txt'):
            source_path = os.path.join(source_folder, filename)
            file_size = os.path.getsize(source_path)

            # 检查文件大小
            if file_size == 0:
                # 删除大小为0的文件
                #os.remove(source_path)
                print(f"Deleted empty file: {source_path}")
            else:
                index+=1
                # 复制文件到目标文件夹
                target_path = os.path.join(target_folder, f"{index}.txt")
                shutil.copy2(source_path, target_path)
                #print(f"Copied non-empty file: {source_path} -> {target_path}")

# 使用示例
source_folder = './train_data_1'
target_folder = './train_data'

def count_data(source_folder):
    line_count = 0
    for filename in os.listdir(source_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(source_folder,filename)) as f:
                for line in f:
                    line_count += 1
    print(line_count)

#process_files(source_folder,target_folder)
count_data(target_folder)