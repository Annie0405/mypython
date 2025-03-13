import os
import shutil
import time
from stream.read import read_all_files


def gen_dir_list(src_dir):
    """ 生成源目录下的子目录列表 """
    for entry in os.scandir(src_dir):  # 用 scandir 替换 listdir
        if entry.is_dir():
            yield entry.name


def merge_dirs(src_dir, dst_dir):
    """合并 src_dir 下所有子文件夹内的文件到 dst_dir"""
    # 直接获取所有文件路径（包含所有子目录内的文件）
    file_list = read_all_files(src_dir, has_subdir=True)

    for src_path in file_list:
        dst_path = os.path.join(dst_dir, os.path.basename(src_path))
        shutil.copy(src_path, dst_path)

    # 合并完成，打印信息
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{current_time}] 合并完成！")
