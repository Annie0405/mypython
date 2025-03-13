import os


def read_all_files(dir_path, has_subdir=False):
    file_list = []
    if has_subdir:
        for root, _, files in os.walk(dir_path):  # os.walk 使用 scandir 进行高效遍历
            for file_name in files:
                file_list.append(os.path.join(root, file_name))
    else:
        for entry in os.scandir(dir_path):
            if entry.is_file():
                file_list.append(entry.path)
    return file_list
