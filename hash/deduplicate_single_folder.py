"""
通过比较哈希值去除重复的文件
"""
import os
import hashlib
from stream.read import read_all_files


def calculate_file_hash(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def deduplicate_single_folder(folder_path):
    """
    比较文件夹内文件哈希值，相同哈希值的文件只保留一个，其余删除
    """
    # 用于记录哈希值与文件路径的映射
    seen_hashes = {}
    # 遍历文件夹中的所有文件
    file_paths = read_all_files(folder_path, has_subdir=False)
    for file_path in file_paths:
        file_hash = calculate_file_hash(file_path)
        if file_hash in seen_hashes:
            # 如果哈希值已存在，删除重复文件
            print(f"删除重复文件: {file_path}")
            os.remove(file_path)
        else:
            # 否则记录哈希值与文件路径
            seen_hashes[file_hash] = file_path
    print("去重完毕")


if __name__ == "__main__":

    # 输入文件夹路径
    folder = r"/path/to/folder"

    deduplicate_single_folder(folder)
