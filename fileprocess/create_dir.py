import os


def create_dir(path, prefix, number, count):
    start = int(number)
    length = len(number)
    count = int(count)
    for i in range(count):
        dir_name = prefix + str(start + i).zfill(length)
        dir_path = os.path.join(path, dir_name)
        os.makedirs(dir_path, exist_ok=True)
    print("目录创建完毕！")
