import os

# 根文件夹路径
root_folder = '../data/ucf101/rawframes_concat'

def rename_files_recursively(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.startswith("img_") and filename.endswith(".jpg"):
                try:
                    # 提取文件名中的数字部分
                    name_parts = filename.split("_")
                    number_part = name_parts[-1].split(".")[0]

                    # 将数字部分转换为整数
                    number = int(number_part)

                    # 生成新的文件名，将数字部分填充到 5 位
                    new_number_part = f'{number:05d}'
                    new_filename = f'img_{new_number_part}.jpg'

                    # 旧路径和新路径
                    old_path = os.path.join(dirpath, filename)
                    new_path = os.path.join(dirpath, new_filename)

                    # 重命名文件
                    os.rename(old_path, new_path)
                except (ValueError, IndexError):
                    # 出现错误时跳过文件
                    pass

# 调用函数开始重命名
rename_files_recursively(root_folder)

