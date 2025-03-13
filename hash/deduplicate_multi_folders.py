"""
通过比较哈希值
找到只存在于A而不存在于B中的文件
将其复制到C
即使文件名不同也没关系
"""
import os
import hashlib
import shutil
from stream.read import read_all_files


def calculate_file_hash(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_file_hashes(folder_path):
    """获取文件夹内所有文件的哈希值"""
    file_hashes = {}
    # 使用 read_all_files 获取所有文件路径
    file_paths = read_all_files(folder_path, has_subdir=False)
    for file_path in file_paths:
        file_hashes[calculate_file_hash(file_path)] = file_path  # 直接存完整路径
    return file_hashes


def find_unique_files(folder_a, folder_b):
    """找出文件夹A中有而文件夹B中没有的文件"""
    hashes_a = get_file_hashes(folder_a)
    hashes_b = get_file_hashes(folder_b)

    unique_files = [file_name for file_hash, file_name in hashes_a.items() if file_hash not in hashes_b]

    return unique_files


def deduplicate_multiple_folders(folder_a, folder_b, folder_c):
    unique_files = find_unique_files(folder_a, folder_b)

    for source_path in unique_files:
        file_name = os.path.basename(source_path)
        destination_path = os.path.join(folder_c, file_name)
        shutil.copy(source_path, destination_path)

    length = len(unique_files)
    print(f"去重完毕, 未重复文件有 {length} 个")


if __name__ == '__main__':

    # 输入文件夹
    folder_a = r'/path/to/A'
    # 从文件夹A中剔除文件夹B中的文件
    folder_b = r'/path/to/B'
    # 输出文件夹
    folder_c = r'/path/to/C'

    deduplicate_multiple_folders(folder_a, folder_b, folder_c)
