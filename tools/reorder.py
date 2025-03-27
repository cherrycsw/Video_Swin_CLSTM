import os

# 定义根文件夹路径
root_folder = '../data/ucf101/rawframes_rgb+flow_sparse'

# 遍历目录树
for root, dirs, files in os.walk(root_folder):
    file_list = [filename for filename in files if filename.startswith('img_') and filename.endswith('.jpg')]
    if file_list:
        # 根据文件名中的数字部分对文件列表进行排序
        file_list.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

        # 重新编号并重命名文件
        for i, filename in enumerate(file_list, start=1):
            old_file_path = os.path.join(root, filename)
            new_filename = f"img_{i:05d}.jpg"
            new_file_path = os.path.join(root, new_filename)

            os.rename(old_file_path, new_file_path)
            print(f"重命名文件: {filename} -> {new_filename}")