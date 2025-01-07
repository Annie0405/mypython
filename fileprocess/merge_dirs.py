import os
import shutil
import time


def gen_dir_list(src_dir):
    for item in os.listdir(src_dir):
        if os.path.isdir(os.path.join(src_dir, item)):
            yield item


def merge_dirs(src_dir, dst_dir):
    # 生成源目录下的子目录列表
    sub_dirs = gen_dir_list(src_dir)
    for sub_dir in sub_dirs:
        sub_dir_path = os.path.join(src_dir, sub_dir)
        # 遍历子目录下的所有文件
        for file_name in os.listdir(sub_dir_path):
            src_path = os.path.join(sub_dir_path, file_name)
            dst_path = os.path.join(dst_dir, file_name)
            shutil.copy(src_path, dst_path)
    # 合并完成，打印信息
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{current_time}] 合并完成！")
