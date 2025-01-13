import os
import shutil

source_folder = "./train_data_with_end"
target_folder = "./OrderedData"


def order(source_folder, target_folder):
    index = 185
    for root, dirs,files in os.walk(source_folder):
        for file in files:
            if file.endswith(".txt"):
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_folder,f"{str(index)}.txt")
                shutil.copyfile(source_path,target_path)
                index+=1

order(source_folder, target_folder)