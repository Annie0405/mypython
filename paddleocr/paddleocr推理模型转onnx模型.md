# paddleocr推理模型转onnx模型

## 一、环境安装

需要准备 PaddleOCR、Paddle2ONNX 模型转换环境，和 ONNXRuntime 预测环境。

默认已经准备好 PaddleOCR 环境。

### 1. 安装 Paddle2ONNX

```shell
python -m pip install paddle2onnx
```

### 2. 安装 ONNXRuntime

```shell
python -m pip install onnxruntime
```

## 二、模型转换

### 1. det模型转换

```shell
paddle2onnx --model_dir ./inference/ch_PP-OCRv3_det_infer \
--model_filename inference.pdmodel \
--params_filename inference.pdiparams \
--save_file ./inference/det_onnx/model.onnx \
--opset_version 11 \
--enable_onnx_checker True
```

### 2. rec模型转换

```shell
paddle2onnx --model_dir ./inference/ch_PP-OCRv3_rec_infer \
--model_filename inference.pdmodel \
--params_filename inference.pdiparams \
--save_file ./inference/rec_onnx/model.onnx \
--opset_version 11 \
--enable_onnx_checker True
```

## 三、参数保存

需手动保存部分模型参数。

### 1. 通用参数



### 2. det参数



### 3. rec参数



## 四、推理预测

### 1. 验证

在 PaddleOCR 环境下使用 ONNXRuntime 预测：

```shell
python tools/infer/predict_system.py --use_gpu=False --use_onnx=True \
--det_model_dir=./inference/det_onnx/model.onnx  \
--rec_model_dir=./inference/rec_onnx/model.onnx  \
--image_dir=./docs/infer_deploy/images/lite_demo.png \
--rec_image_shape='3, 32, 320' --rec_char_dict_path=./ppocr/utils/en_dict.txt
```

### 2. 预测代码

详见 `paddleocr/onnxpredict/predict_det_onnx.py` 和 `paddleocr/onnxpredict/predict_rec_onnx.py` 。

## 五、参考资料

https://paddlepaddle.github.io/PaddleOCR/latest/infer_deploy/paddle2onnx.html#_3