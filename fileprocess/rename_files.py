import os


def rename_files(dir_path, prefix, suffix_digits, file_num):
    # 类型转换
    suffix_digits = int(suffix_digits)
    file_num = int(file_num)
    # 遍历文件夹
    for idx, file_name in enumerate(os.listdir(dir_path)):
        # 遍历指定文件数量后就停止遍历
        if idx == file_num:
            break
        # 源文件路径
        src_file_path = os.path.join(dir_path, file_name)
        # 构造新的文件名
        new_file_name = prefix + str(idx).zfill(suffix_digits) + os.path.splitext(file_name)[1]
        # 新文件路径
        dst_file_path = os.path.join(dir_path, new_file_name)
        # 重命名文件
        os.rename(src_file_path, dst_file_path)
    # 打印信息
    print(f"已成功将 {dir_path} 下的 {file_num} 张图片重命名")
