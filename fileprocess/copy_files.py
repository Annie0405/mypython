import os
import shutil
from stream.read import read_all_files


def copy_files(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)

    # 使用 read_all_files 获取所有文件路径
    for src_file in read_all_files(src_dir, has_subdir=False):
        dst_file = os.path.join(dst_dir, os.path.basename(src_file))
        shutil.copy(src_file, dst_file)

    print("复制完成！")
