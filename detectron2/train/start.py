import os
from detectron2.config import get_cfg
from detectron2 import model_zoo
from train_app import TrainApp

# 字符串常量
TRAIN_SET = "train_set"
VAL_SET = "val_set"
TEST_SET = "test_set"

# 变量，在这里配置类别数、路径、启用项
NUM_CLASSES = 2
ROOT_DIR = "train_data/train1"
DATASET_DIR = os.path.join(ROOT_DIR, "2_labels")
OUTPUT_DIR = os.path.join(ROOT_DIR, "3_output")
INFER_DIR = os.path.join(ROOT_DIR, "4_infer")
ENABLE = {
    # "visualize": True,
    # "train": True,
    # "test": True,
    "infer": True,
}
INFER_VISUALIZE = False
# 处理 ENABLE 字典
keys = ["visualize", "train", "test", "infer"]
for key in keys:
    if key not in ENABLE:
        ENABLE[key] = False


def get_train_cfg():
    cfg = get_cfg()
    # 模型文件和权重配置
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    # 训练集配置
    cfg.DATASETS.TRAIN = (TRAIN_SET,)
    cfg.DATASETS.TEST = (VAL_SET,)  # 验证集用于评估
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = NUM_CLASSES
    # 模型输出目录配置
    cfg.OUTPUT_DIR = os.path.join(OUTPUT_DIR, "models")
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    # 图片加载进程数、批次大小、迭代次数配置
    cfg.DATALOADER.NUM_WORKERS = 4
    cfg.SOLVER.IMS_PER_BATCH = 8
    cfg.SOLVER.MAX_ITER = 100
    # 每张图像上 ROI 分类器处理的最小 ROI 数量
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 32
    # 学习率配置
    cfg.SOLVER.BASE_LR = 0.001
    cfg.SOLVER.GAMMA = 0.1
    cfg.SOLVER.WARMUP_ITERS = 5000
    cfg.SOLVER.STEPS = (10000, 15000)
    # 评估间隔配置
    cfg.TEST.EVAL_PERIOD = 1000
    # 训练阶段图像尺寸配置
    cfg.INPUT.MIN_SIZE_TRAIN = 2000  # 训练时随机从800到1000之间选择图像的短边
    cfg.INPUT.MAX_SIZE_TRAIN = 2000  # 图像长边最大为1333
    # 启用 OHEM (关注难例)
    cfg.MODEL.ROI_HEADS.OHEM = True
    # 调整 anchor 的 aspect ratio
    cfg.MODEL.ANCHOR_GENERATOR.ASPECT_RATIOS = [[0.1, 0.2, 0.5]]  # 针对细长目标设置更适合的比例
    cfg.MODEL.ANCHOR_GENERATOR.SIZES = [[32, 64, 128, 256, 512]]  # 可调整 anchor 的尺寸
    # 调整 ROI Align 的采样分辨率
    cfg.MODEL.ROI_BOX_HEAD.POOLER_RESOLUTION = 14  # 默认是 7，可以调整为 14 或更高
    cfg.MODEL.ROI_BOX_HEAD.POOLER_SAMPLING_RATIO = 2  # 增加采样率以提高精度
    # 调整 Mask 分支的 ROI Align 参数
    cfg.MODEL.ROI_MASK_HEAD.POOLER_RESOLUTION = 14
    cfg.MODEL.ROI_MASK_HEAD.POOLER_SAMPLING_RATIO = 2

    return cfg


def get_test_cfg():
    cfg = get_train_cfg()

    # 权重文件配置
    cfg.MODEL.WEIGHTS = os.path.join(OUTPUT_DIR, "models", "model_final.pth")
    # 测试集配置
    cfg.DATASETS.TEST = (TEST_SET,)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = NUM_CLASSES
    # # 推理阶段检测阈值配置
    # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # 设置检测阈值
    # cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = 0.3  # 设置NMS阈值，较高的值会去除重叠框
    # 推理阶段图像尺寸配置
    cfg.INPUT.MIN_SIZE_TEST = 2000  # 测试时图像的短边固定为1000
    cfg.INPUT.MAX_SIZE_TEST = 2000  # 图像长边最大为1333

    return cfg


TrainApp(
    register={
        "dataset_dir": DATASET_DIR,
        "name": {"train": TRAIN_SET, "val": VAL_SET, "test": TEST_SET},
        "json_file": {
            "train": os.path.join(DATASET_DIR, "annotations", "train_labels.json"),
            "val": os.path.join(DATASET_DIR, "annotations", "val_labels.json"),
            "test": os.path.join(DATASET_DIR, "annotations", "test_labels.json"),
        },
        "image_root": {
            "train": os.path.join(DATASET_DIR, "train_images"),
            "val": os.path.join(DATASET_DIR, "val_images"),
            "test": os.path.join(DATASET_DIR, "test_images"),
        }
    },
    visualize={
        "visualize": ENABLE["visualize"],
        "output_dir": os.path.join(OUTPUT_DIR, "visualizations"),
        "metadata": VAL_SET,
        "dataset": VAL_SET,
        "num_samples": 200
    },
    train={
        "train": ENABLE["train"],
        "cfg": get_train_cfg(),
    },
    test={
        "test": ENABLE["test"],
        "output_dir": os.path.join(OUTPUT_DIR, "test"),
        "cfg": get_test_cfg(),
    },
    infer={
        "infer": ENABLE["infer"],
        "images_dir": os.path.join(INFER_DIR, "infer_images"),
        "output_dir": os.path.join(INFER_DIR, "infer_results"),
        "cfg": get_test_cfg(),
    }
)
