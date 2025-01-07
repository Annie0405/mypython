"""
随机从文件夹A中移动N张图片到文件夹B
"""
import os
import random
import shutil


def rand_move_files(path_src: str, path_dst: str, num: int):
    # 遍历源文件夹中的所有文件
    file_list = [f for f in os.listdir(path_src)]

    # 如果目标文件夹不存在，则创建
    os.makedirs(path_dst, exist_ok=True)

    # 确保源文件夹中的文件数大于等于 num
    if len(file_list) < num:
        raise ValueError(f"源文件夹中只有{len(file_list)}个文件，不足{num}张！")

    # 随机选择 num 个文件
    selected_files = random.sample(file_list, num)

    # 把文件移动到目标文件夹
    for file_name in selected_files:
        src_file = os.path.join(path_src, file_name)
        dst_file = os.path.join(path_dst, file_name)
        shutil.move(src_file, dst_file)

    print(f"已成功从{path_src}随机移动{num}张图片到{path_dst}")


if __name__ == '__main__':
    path_src = r"/path/to/source"
    path_dst = r"/path/to/destination"
    n = 10
    rand_move_files(path_src, path_dst, n)
