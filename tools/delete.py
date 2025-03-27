import os

# 定义根文件夹路径
root_folder = '../data/ucf101/rawframes_rgb+flow_sparse'

# 遍历目录树
for root, dirs, files in os.walk(root_folder):
    for filename in files:
        if filename.startswith('img_') and filename.endswith('.jpg'):
            # 提取文件名中的数字部分
            number_part = filename.split('_')[-1].split('.')[0]
            try:
                number = int(number_part)
                # 判断是否满足条件 (a-3)%4=0
                if (number - 3) % 4 == 0:
                    file_path = os.path.join(root, filename)
                    # 删除文件
                    os.remove(file_path)
                    print(f"已删除文件: {file_path}")
            except ValueError:
                # 如果无法转换为整数，跳过这个文件
                pass
