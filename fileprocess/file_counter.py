from stream.read import read_all_files


def count_files(dir_path):
    file_list = read_all_files(dir_path, has_subdir=True)
    print(len(file_list))
