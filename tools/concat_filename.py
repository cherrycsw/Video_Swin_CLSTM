import os

# 根文件夹路径
root_folder = '../data/ucf101/rawframes_concat'

def rename_jpg_files(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if filenames:
            jpg_files = [file for file in filenames if file.lower().endswith('.jpg')]
            total_count = len(jpg_files)

            # 计算 "xxx" 的位数
            max_total_count = max(total_count, 1)  # 避免零除错误
            num_digits = len(str(max_total_count))

            for i, file in enumerate(jpg_files):
                _, ext = os.path.splitext(file)
                file_name_parts = file.split('_')
                last_digit = int(file_name_parts[-1].split('.')[0])
                
                if last_digit % 2 == 0:
                    new_number = (total_count + 1) // 2 + last_digit // 2
                    new_name = f'img_{new_number:0{num_digits}d}{ext}'
                else:
                    new_number = (last_digit + 1) // 2
                    new_name = f'img_{new_number:0{num_digits}d}{ext}'
                
                old_path = os.path.join(dirpath, file)
                new_path = os.path.join(dirpath, new_name)
                
                # 检查新文件名是否已存在，避免覆盖已经改好的文件
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)

# 调用函数开始重命名
rename_jpg_files(root_folder)

