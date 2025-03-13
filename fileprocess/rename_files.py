import os
from stream.read import read_all_files


def rename_files(dir_path, prefix, suffix_digits, file_num):
    # 类型转换
    suffix_digits = int(suffix_digits)
    file_num = int(file_num)

    # 获取所有文件路径
    all_files = read_all_files(dir_path, has_subdir=False)

    # 遍历文件（限制数量）
    for idx, file_path in enumerate(all_files[:file_num]):
        file_name = os.path.basename(file_path)
        # 构造新的文件名
        new_file_name = prefix + str(idx).zfill(suffix_digits) + os.path.splitext(file_name)[1]
        # 新文件路径
        dst_file_path = os.path.join(dir_path, new_file_name)
        # 重命名文件
        os.rename(file_path, dst_file_path)

    # 打印信息
    print(f"已成功将 {dir_path} 下的 {file_num} 个文件重命名")
