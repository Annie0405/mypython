import os
import random
import shutil


def split_train_val_test(root_dir, server_dir, train, val, test, filename):
    # 原始图片和标签存放路径
    ori_dir = os.path.join(root_dir, "0_original_data")
    # 原始标签路径
    file_path = os.path.join(ori_dir, filename)

    # 数据集划分后存放路径
    split_dir = os.path.join(root_dir, "1_labels")
    os.makedirs(split_dir, exist_ok=True)
    train_dir = os.path.join(split_dir, "train")
    os.makedirs(train_dir, exist_ok=True)
    train_txt_path = os.path.join(split_dir, "train.txt")
    val_dir = os.path.join(split_dir, "val")
    os.makedirs(val_dir, exist_ok=True)
    val_txt_path = os.path.join(split_dir, "val.txt")
    if test:
        test_dir = os.path.join(split_dir, "test")
        os.makedirs(test_dir, exist_ok=True)
        test_txt_path = os.path.join(split_dir, "test.txt")

    # 读入原始标签文件
    with open(file_path, 'r', encoding='utf-8') as f:
        total_label_list = [line.strip() for line in f.readlines()]

    # 10个一组划分标签列表
    group_num = 10
    group_list = [total_label_list[i:i + group_num] for i in range(0, len(total_label_list), group_num)]

    # 按 train : val : test 的比例划分训练集、验证集和测试集
    # 初始化训练集、验证集和测试集标签列表
    train_label_list = []
    val_label_list = []
    test_label_list = []

    # 分组遍历标签列表
    for group in group_list:

        # 随机划分
        random.shuffle(group)
        train_group = group[:train]
        val_group = group[train:train + val]
        if test:
            test_group = group[train + val:]

        # 划分训练集或验证集或测试集的方法
        def data_process(which_group, which_label_list, which_dir, method: str):
            for item in which_group:
                # 构造标签
                which_label = server_dir + '/' + method + '/' + item
                which_label_list.append(which_label)
                # 复制图片
                image_name = item.split("\t")[0]
                src_path = os.path.join(ori_dir, image_name)
                dst_path = os.path.join(which_dir, image_name)
                shutil.copy(src_path, dst_path)

        data_process(train_group, train_label_list, train_dir, "train")
        data_process(val_group, val_label_list, val_dir, "val")
        if test:
            data_process(test_group, test_label_list, test_dir, "test")

    # 写入训练集、验证集和测试集的标签
    with open(train_txt_path, 'w', encoding='utf-8') as f:
        for label in train_label_list:
            f.write(label + "\n")
    with open(val_txt_path, 'w', encoding='utf-8') as f:
        for label in val_label_list:
            f.write(label + "\n")
    if test:
        with open(test_txt_path, 'w', encoding='utf-8') as f:
            for label in test_label_list:
                f.write(label + "\n")
    print("划分完毕！")


def split(root_dir, server_dir, train, val, test, mode):
    train = int(train)
    val = int(val)
    if test:
        test = int(test)
    else:
        test = 0

    if mode == "det":
        split_train_val_test(root_dir, server_dir, train, val, test, "Label.txt")
    elif mode == "rec":
        split_train_val_test(root_dir, server_dir, train, val, test, "rec_gt.txt")


def split_rec(root_dir, server_dir, train: int, val: int, test: int):
    # 原始图片和标签存放路径
    ori_dir = os.path.join(root_dir, "0_original_data")
    # 原始标签路径
    rec_gt_path = os.path.join(ori_dir, "rec_gt.txt")

    # 数据集划分后存放路径
    split_dir = os.path.join(root_dir, "1_labels")
    os.makedirs(split_dir, exist_ok=True)
    train_dir = os.path.join(split_dir, "train")
    os.makedirs(train_dir, exist_ok=True)
    train_txt_path = os.path.join(split_dir, "train.txt")
    val_dir = os.path.join(split_dir, "val")
    os.makedirs(val_dir, exist_ok=True)
    val_txt_path = os.path.join(split_dir, "val.txt")
    if test:
        test_dir = os.path.join(split_dir, "test")
        os.makedirs(test_dir, exist_ok=True)
        test_txt_path = os.path.join(split_dir, "test.txt")

    # 读入原始标签文件
    with open(rec_gt_path, 'r', encoding='utf-8') as f:
        total_label_list = [line.strip() for line in f.readlines()]

    # 10个一组划分标签列表
    group_num = 10
    group_list = [total_label_list[i:i + group_num] for i in range(0, len(total_label_list), group_num)]

    # 按 train : val : test 的比例划分训练集、验证集和测试集
    # 初始化训练集、验证集和测试集标签列表
    train_label_list = []
    val_label_list = []
    test_label_list = []

    # 分组遍历标签列表
    for group in group_list:

        # 随机划分
        random.shuffle(group)
        train_group = group[:train]
        val_group = group[train:train + val]
        if test:
            test_group = group[train + val:]

        # 划分训练集或验证集或测试集的方法
        def data_process(which_group, which_label_list, which_dir, method: str):
            for item in which_group:
                # 构造标签
                which_label = server_dir + '/' + method + '/' + item
                which_label_list.append(which_label)
                # 复制图片
                image_name = item.split("\t")[0]
                src_path = os.path.join(ori_dir, image_name)
                dst_path = os.path.join(which_dir, image_name)
                shutil.copy(src_path, dst_path)

        data_process(train_group, train_label_list, train_dir, "train")
        data_process(val_group, val_label_list, val_dir, "val")
        if test:
            data_process(test_group, test_label_list, test_dir, "test")

    # 写入训练集、验证集和测试集的标签
    with open(train_txt_path, 'w', encoding='utf-8') as f:
        for label in train_label_list:
            f.write(label + "\n")
    with open(val_txt_path, 'w', encoding='utf-8') as f:
        for label in val_label_list:
            f.write(label + "\n")
    if test:
        with open(test_txt_path, 'w', encoding='utf-8') as f:
            for label in test_label_list:
                f.write(label + "\n")
    print("划分完毕！")
