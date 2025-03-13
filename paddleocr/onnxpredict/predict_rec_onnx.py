import os
import cv2
import numpy as np
import onnxruntime as ort
from custom_rec_process import build_post_process, resize_norm_img

# =========================== 配置参数 ===========================
MODEL_PATH = r"/path/to/model.onnx"
IMAGE_PATH = [
        r"train2_rec_ts/1_labels/test/TS_rec_pipe_type00_06_crop_0.jpg",
        r"train2_rec_ts/1_labels/test/TS_rec_pipe_type00_11_crop_0.jpg",
    ]

USE_GPU = True
GPU_ID = 0

RECOGNIZER_CONFIG = {
    "rec_batch_num": 0,
    "rec_image_shape": [3, 32, 320],
    "return_word_box": False,
    "rec_char_dict_path": "/path/to/dict",
    "use_space_char": False,
}


# =========================== 加载模型 ===========================
def load_model(model_path, use_gpu, gpu_id):
    if not os.path.exists(model_path):
        raise ValueError(f"Model file not found: {model_path}")
    providers = (
        [
            ("CUDAExecutionProvider", {"device_id": gpu_id, "cudnn_conv_algo_search": "DEFAULT"})
        ] if use_gpu else ["CPUExecutionProvider"]
    )
    return ort.InferenceSession(model_path, providers=providers)


# =========================== 预处理图像 ===========================
def preprocess_images(image_paths, rec_image_shape):
    img_list = [cv2.imread(path) for path in image_paths]
    width_list = [img.shape[1] / float(img.shape[0]) for img in img_list]
    indices = np.argsort(width_list)  # 按宽高比排序，提高识别效率
    return img_list, indices


# =========================== 运行推理 ===========================
def run_inference(predictor, img_list, indices, config):
    rec_res = [["", 0.0]] * len(img_list)
    batch_num = config["rec_batch_num"]
    imgC, imgH, imgW = config["rec_image_shape"][:3]

    postprocess_op = build_post_process({
        "name": "CTCLabelDecode",
        "character_dict_path": config["rec_char_dict_path"],
        "use_space_char": config["use_space_char"],
    })

    for beg in range(0, len(img_list), batch_num):
        end = min(len(img_list), beg + batch_num)
        norm_img_batch, wh_ratio_list, max_wh_ratio = [], [], imgW / imgH

        for i in range(beg, end):
            h, w = img_list[indices[i]].shape[:2]
            wh_ratio = w / h
            max_wh_ratio = max(max_wh_ratio, wh_ratio)
            wh_ratio_list.append(wh_ratio)

        for i in range(beg, end):
            norm_img = resize_norm_img(
                config["rec_image_shape"], predictor.get_inputs()[0], img_list[indices[i]], max_wh_ratio
            )
            norm_img_batch.append(norm_img[np.newaxis, :])

        norm_img_batch = np.concatenate(norm_img_batch).copy()
        outputs = predictor.run(None, {predictor.get_inputs()[0].name: norm_img_batch})
        preds = outputs[0]
        rec_result = postprocess_op(
            preds, return_word_box=config["return_word_box"], wh_ratio_list=wh_ratio_list, max_wh_ratio=max_wh_ratio
        )

        for r in range(len(rec_result)):
            rec_res[indices[beg + r]] = rec_result[r]

    return rec_res


# =========================== 主流程 ===========================
if __name__ == "__main__":
    predictor = load_model(MODEL_PATH, USE_GPU, GPU_ID)
    img_list, indices = preprocess_images(IMAGE_PATH, RECOGNIZER_CONFIG["rec_image_shape"])
    results = run_inference(predictor, img_list, indices, RECOGNIZER_CONFIG)
    print(results)
