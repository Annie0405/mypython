import os
import cv2
import numpy as np
import onnxruntime as ort
from custom_det_process import (
    transform, create_operators, build_post_process,
    order_points_clockwise, clip_det_res
)

# =========================== 配置参数 ===========================
MODEL_PATH = r"/path/to/model.onnx"
IMAGE_PATH = r"/path/to/image"

USE_GPU = True
GPU_ID = 0

DETECTOR_CONFIG = {
    "box_type": "",
    "limit_side_len": 0,
    "limit_type": "",
    "thresh": 0.0,
    "box_thresh": 0.0,
    "use_dilation": False,
    "score_mode": "",
    "max_candidates": 0,
    "unclip_ratio": 2.5,    # 固定
}


# =========================== 加载 ONNX 模型 ===========================
def load_model(model_path, use_gpu=True, gpu_id=0):
    """ 加载 ONNX 模型 """
    if not os.path.exists(model_path):
        raise ValueError(f"Model file not found: {model_path}")

    providers = ["CPUExecutionProvider"]
    if use_gpu:
        providers = [
            (
                "CUDAExecutionProvider",
                {"device_id": gpu_id, "cudnn_conv_algo_search": "DEFAULT"}
            )
        ]

    return ort.InferenceSession(model_path, providers=providers)


# =========================== 预处理 ===========================
def preprocess_image(image, input_tensor_shape, config):
    """ 对输入图像进行预处理 """
    img_h, img_w = input_tensor_shape[2:]

    # 预处理算子列表
    pre_process_list = [
        {"DetResizeForTest": {"limit_side_len": config["limit_side_len"], "limit_type": config["limit_type"]}},
        {"NormalizeImage": {"std": [0.229, 0.224, 0.225], "mean": [0.485, 0.456, 0.406], "scale": "1./255.",
                            "order": "hwc"}},
        {"ToCHWImage": None},
        {"KeepKeys": {"keep_keys": ["image", "shape"]}}
    ]

    # 如果模型有固定输入尺寸，更新 resize 参数
    if isinstance(img_h, int) and isinstance(img_w, int) and img_h > 0 and img_w > 0:
        pre_process_list[0] = {"DetResizeForTest": {"image_shape": [img_h, img_w]}}

    preprocess_op = create_operators(pre_process_list)
    data = transform({"image": image}, preprocess_op)
    if data is None:
        return None, None

    img, shape_list = data
    img = np.expand_dims(img, axis=0).copy()
    shape_list = np.expand_dims(shape_list, axis=0)

    return img, shape_list


# =========================== 后处理 ===========================
def postprocess_boxes(preds, shape_list, ori_im_shape, config):
    """ 处理检测框结果 """
    postprocess_op = build_post_process({
        "name": "DBPostProcess",
        "thresh": config["thresh"],
        "box_thresh": config["box_thresh"],
        "max_candidates": config["max_candidates"],
        "unclip_ratio": config["unclip_ratio"],
        "use_dilation": config["use_dilation"],
        "score_mode": config["score_mode"],
        "box_type": config["box_type"]
    })

    post_result = postprocess_op(preds, shape_list)
    dt_boxes = post_result[0]["points"]

    # 如果 box_type 是 "quad"，则进行坐标矫正
    if config["box_type"] == "quad":
        img_height, img_width = ori_im_shape[:2]
        dt_boxes_new = []
        for box in dt_boxes:
            box = np.array(box) if isinstance(box, list) else box
            box = order_points_clockwise(box)
            box = clip_det_res(box, img_height, img_width)

            rect_width = int(np.linalg.norm(box[0] - box[1]))
            rect_height = int(np.linalg.norm(box[0] - box[3]))
            if rect_width > 3 and rect_height > 3:
                dt_boxes_new.append(box)

        dt_boxes = np.array(dt_boxes_new)

    return dt_boxes.astype(np.int32)


# =========================== 绘制检测框并显示 ===========================
def draw_boxes_and_show(image, dt_boxes):
    """ 在图片上绘制检测框，并显示 """
    cv2.polylines(image, [dt_boxes], isClosed=True, color=(0, 255, 0), thickness=2)
    cv2.imshow("Detected Box", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# =========================== 主流程 ===========================
if __name__ == "__main__":
    # 加载模型
    predictor = load_model(MODEL_PATH, USE_GPU, GPU_ID)
    input_tensor = predictor.get_inputs()[0]

    # 读取图片
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        raise ValueError(f"Failed to read image: {IMAGE_PATH}")

    ori_im = image.copy()

    # 预处理
    img, shape_list = preprocess_image(image, input_tensor.shape, DETECTOR_CONFIG)
    if img is None:
        print("Preprocessing failed.")
        exit(1)

    # 推理
    input_dict = {input_tensor.name: img}
    outputs = predictor.run(None, input_dict)

    # 解析预测结果
    preds = {"maps": outputs[0]}
    dt_boxes = postprocess_boxes(preds, shape_list, ori_im.shape, DETECTOR_CONFIG)

    # 打印检测框
    print(dt_boxes)

    # 绘制检测框并显示
    draw_boxes_and_show(image, dt_boxes)
