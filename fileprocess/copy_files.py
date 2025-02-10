import os
import shutil


def copy_files(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for file_name in os.listdir(src_dir):
        src_file = os.path.join(src_dir, file_name)
        dst_file = os.path.join(dst_dir, file_name)
        shutil.copy(src_file, dst_file)
    print("复制完成！")
