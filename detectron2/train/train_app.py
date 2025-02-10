import os
import cv2
import random
from detectron2.utils.logger import setup_logger
from detectron2.engine import DefaultTrainer, DefaultPredictor
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog, DatasetCatalog, build_detection_test_loader
from detectron2.data.datasets import register_coco_instances
from detectron2.evaluation import COCOEvaluator, inference_on_dataset


class TrainApp:
    def __init__(self, register: dict, visualize: dict, train: dict, test: dict, infer: dict):
        setup_logger()  # 配置日志

        # 注册数据集
        self.register = register
        self.register_datasets()
        # 可视化数据集样本
        if visualize["visualize"]:
            self.visualize = visualize
            self.visualize_samples()
        # 启动训练
        if train["train"]:
            self.train = train
            self.train_model()
        # 验证模型
        if test["test"]:
            self.test = test
            self.test_model()
        # 推理
        if infer["infer"]:
            self.infer = infer
            self.infer_model()

    def register_datasets(self,):
        train = self.register["name"]["train"]
        val = self.register["name"]["val"]
        test = self.register["name"]["test"]
        register_coco_instances(
            train, {}, self.register["json_file"]["train"], self.register["image_root"]["train"]
        )
        register_coco_instances(
            val, {}, self.register["json_file"]["val"], self.register["image_root"]["val"]
        )
        register_coco_instances(
            test, {}, self.register["json_file"]["test"], self.register["image_root"]["test"]
        )
        print(f"数据集注册完成：\n- 训练集: {train}\n- 验证集: {val}\n- 测试集: {test}")

    def visualize_samples(self):
        # 可视化样本存放路径
        output_dir = self.visualize["output_dir"]
        os.makedirs(output_dir, exist_ok=True)
        # 获取数据集的元数据
        metadata = MetadataCatalog.get(self.visualize["metadata"])
        dataset_dicts = DatasetCatalog.get(self.visualize["dataset"])
        # 随机选择 num_samples 个样本进行可视化
        for idx, data in enumerate(random.sample(dataset_dicts, self.visualize["num_samples"])):
            img = cv2.imread(data["file_name"])
            visualizer = Visualizer(img[:, :, ::-1], metadata=metadata, scale=0.8, instance_mode=ColorMode.IMAGE_BW)
            visiual_img = visualizer.draw_dataset_dict(data)
            save_path = os.path.join(output_dir, f"val_sample_{idx}.jpg")
            cv2.imwrite(save_path, visiual_img.get_image()[:, :, ::-1])
        # 打印信息
        print(f"可视化样本保存至: {output_dir}")

    def train_model(self):
        trainer = DefaultTrainer(self.train["cfg"])
        trainer.resume_or_load(resume=False)
        trainer.train()

    def test_model(self):
        # 模型配置
        cfg = self.test["cfg"]
        # 输出路径配置
        output_dir = self.test["output_dir"]
        os.makedirs(output_dir, exist_ok=True)
        # 推理器配置
        predictor = DefaultPredictor(cfg)
        # 测试集配置
        test_dataset_name = cfg.DATASETS.TEST[0]
        metadata = MetadataCatalog.get(test_dataset_name)
        dataset_dicts = DatasetCatalog.get(test_dataset_name)
        # 推理结果可视化
        for idx, d in enumerate(dataset_dicts):
            im = cv2.imread(d["file_name"])
            outputs = predictor(im)
            visualizer = Visualizer(im[:, :, ::-1], metadata=metadata, scale=1.0, instance_mode=ColorMode.IMAGE)
            out = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
            image_name = os.path.basename(d["file_name"])
            save_path = os.path.join(output_dir, image_name)
            cv2.imwrite(save_path, out.get_image()[:, :, ::-1])
        print(f"推理结果保存至: {output_dir}")
        # 使用 COCOEvaluator 评估训练集的 mAP
        evaluator = COCOEvaluator(test_dataset_name, cfg, False, output_dir=output_dir)
        test_loader = build_detection_test_loader(cfg, test_dataset_name)
        print("开始评估测试集表现...")
        metrics = inference_on_dataset(predictor.model, test_loader, evaluator)
        print("训练集评估结果:", metrics)

    def infer_model(self):
        # 模型配置
        cfg = self.infer["cfg"]
        # 输入路径配置
        images_dir = self.infer["images_dir"]
        # 输出路径配置
        output_dir = self.infer["output_dir"]
        os.makedirs(output_dir, exist_ok=True)
        # 推理器配置
        predictor = DefaultPredictor(cfg)  # 创建推理器
        # 元数据配置
        metadata = MetadataCatalog.get(cfg.DATASETS.TEST[0] if len(cfg.DATASETS.TEST) else "__unused")
        # 推理结果可视化
        for image_name in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_name)
            im = cv2.imread(image_path)
            outputs = predictor(im)
            visualizer = Visualizer(im[:, :, ::-1], metadata=metadata, scale=1.0, instance_mode=ColorMode.IMAGE)
            vis_output = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
            save_path = os.path.join(output_dir, image_name)
            cv2.imwrite(save_path, vis_output.get_image()[:, :, ::-1])
        print(f"推理结果已保存至: {output_dir}")
