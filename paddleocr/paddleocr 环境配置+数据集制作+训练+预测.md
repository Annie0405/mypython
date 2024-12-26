# paddleocr 环境配置+数据集制作+训练+预测

## 一、环境配置

### 1. paddleocr源码下载

[GitHub - PaddlePaddle/PaddleOCR: Awesome multilingual OCR toolkits based on PaddlePaddle (practical ultra lightweight OCR system, support 80+ languages recognition, provide data annotation and synthesis tools, support training and deployment among server, mobile, embedded and IoT devices)](https://github.com/PaddlePaddle/PaddleOCR)

### 2. 创建虚拟环境

```shell
conda create -n ocr python=3.9
```

### 3. cuda安装

#### 查询cuda版本及下载地址

```shell
conda search cudatoolkit --info
conda search cudnn --info
```

#### 进入url链接下载

https://repo.anaconda.com/pkgs/main/win-64/cudatoolkit-11.8.0-hd77b12b_0.conda

https://repo.anaconda.com/pkgs/main/win-64/cudnn-8.9.2.26-cuda11_0.conda

#### 本地安装（可使用绝对路径）：

```shell
conda install --use-local cudatoolkit-11.8.0-hd77b12b_0.conda
conda install --use-local cudnn-8.9.2.26-cuda11_0.conda
```

### 4. 下载pytorch

在以下链接查找合适的安装指令：

https://pytorch.org/get-started/previous-versions/

```shell
conda install pytorch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 5. 检查是否安装正确

在环境中运行如下脚本：

```python
import torch
print('CUDA版本:',torch.version.cuda)
print('cudnn版本:', torch.backends.cudnn.version())
print('Pytorch版本:',torch.__version__)
print('显卡是否可用:','可用' if(torch.cuda.is_available()) else '不可用')
print('显卡数量:',torch.cuda.device_count())
print('当前显卡型号:',torch.cuda.get_device_name())
print('当前显卡的CUDA算力:',torch.cuda.get_device_capability())
print('当前显卡的总显存:',torch.cuda.get_device_properties(0).total_memory/1024/1024/1024,'GB')
print('是否支持TensorCore:','支持' if (torch.cuda.get_device_properties(0).major >= 7) else '不支持')
print('当前显卡的显存使用率:',torch.cuda.memory_allocated(0)/torch.cuda.get_device_properties(0).total_memory*100,'%')
```

### 6. 安装paddleocr依赖库

进入paddleocr根目录，执行如下指令：

```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 7. 下载paddlepaddle

在paddlepaddle官网：

[https://www.paddlepaddle.org.cn/](https://www.paddlepaddle.org.cn/)

找到合适的版本：

```shell
python -m pip install paddlepaddle-gpu==2.6.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 8. 目前使用过的稳定版本

- python=3.9, cudatoolkit=11.8, cudnn=8700, pytorch=2.0.1, paddlepaddle-gpu=2.6.1

## 二、数据集制作

### 1. 数据集标注

#### 数据集标注工具PPOCRLable

- [GitHub - PaddlePaddle/PaddleOCR at release/2.6](https://github.com/PaddlePaddle/PaddleOCR/tree/release/2.6)

        把上述链接中的PPOCRLable文件夹直接拷贝到上文下载的paddleocr源码目录下

- 进入PPOCRLabel目录，安装依赖：

```shell
pip install python-docx
pip install beautifulsoup4
pip install xlrd
pip install pyqt5
```

- 运行标注程序：

第一次运行会下载一堆东西：

```shell
python PPOCRLabel.py --lang ch
python PPOCRLabel.py --lang ch --kie True
```

#### PPOCRLabel生成的标签文件

- 所有的标注信息都存放在`Label.txt`中，裁切图片存放在`crop_img/`，建议自己编写脚本根据`Label.txt`来构建训练集，标签文件中不同字段使用`\t`分割。

- PPOCRLabel标注工具的坑：

        如果在标注过程中曾经删除过标注框，这项标注内容有可能不会从`crop_img`和`rec_gt.txt`中被删去。即使没有勾选自动保存，或没有提前导出过标注结果，也会出现这种情况。

### 2. 数据集划分

- 可按8：1：1的比例划分为训练集、验证集、测试集；

- 也可按8：2的比例划分为训练集和验证集。

- 如果总数据量超过10w，那么验证集1w，训练集1w，其他都为训练集。

- `PPOCRLable`有现成的数据集划分脚本，不过生成的标签是绝对路径，如果需要更改训练集存放路径，或者修改划分方式，可以自己写脚本

```shell
python gen_ocr_train_val_test.py --trainValTestRatio 8:1:1 --datasetRootPath ../train_data/my_dataset
```

### 3. 数据集的结构

划分完成后的数据集结构如下，可根据需要灵活调整：

```makefile
train_data/
├────det/
│    ├────train/
│    │    ├────train_image0.jpg
│    │    ├────train_image1.jpg
│    │    ├────train_image2.jpg
│    │    └────······
│    ├────val/
│    ├────test/
│    ├────train.txt
│    ├────val.txt
│    └────test.txt
└────rec/
     ├────train/
     ├────val/
     ├────test/
     ├────train.txt
     ├────val.txt
     └────test.txt
```

## 三、训练模型

### 1. 下载官方预训练模型及相应配置文件

[PaddleOCR/doc/doc_ch/models_list.md at release/2.6 · PaddlePaddle/PaddleOCR · GitHub](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/models_list.md)

根据需要下载预训练模型和相应配置文件

### 2. 配置模型文件

需要修改的参数如下：

```yaml
# config.yml

Global:
    use_gpu: true
    epoch_num: 350
    log_smooth_window: 20
    print_batch_step: 99999999999
    save_model_dir: path/to/save/train_models
    save_epoch_step: 50
    eval_batch_step: [3500, 3500]
    pretrained_model: path/to/pretrained_model
    save_inference_dir: path/to/save/inference_model
    max_text_length: &max_text_length 10    # det模型没有

Train:
    dataset:
        data_dir: path/to/train_data    # 可使用相对路径
        label_file_list:
            - path/to/train.txt    # 可使用相对路径
    loader：
        batch_size_per_card: 128    # 如果是det模型，调到32或64
        num_workers: 8

Eval:
    dataset:
        data_dir: path/to/train_data    # 可使用相对路径
        label_file_list:
            - path/to/val.txt    # 可使用相对路径
    loader：
        batch_size_per_card: 128    # 如果是det模型，这里必须是1
        num_workers: 4


```

- `print_batch_step`: `linux`设置为无穷大，`windows`上设置为一个`epoch`的步长

### 3. 指令训练

```shell
python tools/train.py -c path/to/config.yml
```

## 四、测试训练模型

执行如下指令来测试训练模型：

```shell
# det模型
python tools/infer_det.py -c path/to/config.yml -o \
    Global.pretrained_model=path/to/train_model \
    Global.infer_img=path/to/image_folder_or_file \
    Global.save_res_path=path/to/predict_db.txt
# rec模型
python tools/infer_rec.py -c path/to/config.yml -o \
    Global.pretrained_model=path/to/train_model \
    Global.infer_img=path/to/image_folder_or_file \
    Global.save_res_path=path/to/rec_results.txt
```

## 五、导出训练模型为推理模型

执行如下指令来导出训练模型为推理模型：

```shell
python tools/export_model.py -c path/to/config.yml -o \
    Global.pretrained_model=path/to/train_model \
    Global.save_inference_dir=path/to/save/inference_model
```

## 六、验证推理模型

### 1. 指令验证

```shell
# det模型
python tools/infer/predict_det.py --image_dir=path/to/image_dir \
    --det_model_dir=path/to/det_model
# rec模型
python tools/infer/predict_rec.py --image_dir=path/to/image_dir \
    --rec_model_dir=path/to/rec_model
# det模型和rec模型联合验证
python tools/infer/predict_system.py --image_dir=path/to/image_dir \
    --det_model_dir=path/to/det_model --rec_model_dir=path/to/rec_model
```

### 2. 可能出现的问题

如果出现推理模型效果与训练模型效果不一致的情况，可能是两个模型使用的后处理参数不一样所导致的，解决方法如下：

找到`tools/infer/predict_det.py`中的`TextDetector`，这里默认配置了`limit_side_len=960`和`limit_type='max'`，此参数与训练时不一致，注释掉这两行即可。

## 七、可能出现的bug

### 1. albucore版本错误

- 在`linux`环境下运行`paddleocr`的训练指令后遇到如下报错：

```shell
Traceback (most recent call last):
  File "/home/ai/nar_projects/driving_license/PaddleOCR/tools/train.py", line 30, in <module>
    from ppocr.data import build_dataloader, set_signal_handlers
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/data/__init__.py", line 35, in <module>
    from ppocr.data.imaug import transform, create_operators
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/data/imaug/__init__.py", line 64, in <module>
    from .latex_ocr_aug import *
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/data/imaug/latex_ocr_aug.py", line 32, in <module>
    import albumentations as A
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/albumentations/__init__.py", line 6, in <module>
    from .augmentations import *
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/albumentations/augmentations/__init__.py", line 1, in <module>
    from .blur.functional import *
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/albumentations/augmentations/blur/__init__.py", line 1, in <module>
    from .functional import *
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/albumentations/augmentations/blur/functional.py", line 7, in <module>
    from albucore.utils import clipped, maybe_process_in_chunks, preserve_channel_dim
ImportError: cannot import name 'preserve_channel_dim' from 'albucore.utils' (/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/albucore/utils.py)
```

- 问题解决方案参照如下链接：

[ImportError: cannot import name &#39;preserve_channel_dim&#39; from &#39;albucore.utils&#39; · Issue #432 · Gourieff/comfyui-reactor-node · GitHub](https://github.com/Gourieff/comfyui-reactor-node/issues/432)

- 解决方案：

```shell
python -m pip install albucore==0.0.16
```

### 2. cuDNN第三方库缺失

- 在`linux`环境下运行`paddleocr`的训练指令后遇到如下报错：

```shell
W1011 16:22:07.015483 788278 gpu_resources.cc:119] Please NOTE: device: 0, GPU Compute Capability: 7.0, Driver API Version: 12.4, Runtime API Version: 11.8
W1011 16:22:07.015712 788278 dynamic_loader.cc:314] The third-party dynamic library (libcudnn.so) that Paddle depends on is not configured correctly. (error code is /usr/local/cuda/lib64/libcudnn.so: cannot open shared object file: No such file or directory)
  Suggestions:
  1. Check if the third-party dynamic library (e.g. CUDA, CUDNN) is installed correctly and its version is matched with paddlepaddle you installed.
  2. Configure third-party dynamic library environment variables as follows:
  - Linux: set LD_LIBRARY_PATH by `export LD_LIBRARY_PATH=...`
  - Windows: set PATH by `set PATH=XXX;
Traceback (most recent call last):
  File "/home/ai/nar_projects/driving_license/PaddleOCR/tools/train.py", line 255, in <module>
    main(config, device, logger, vdl_writer, seed)
  File "/home/ai/nar_projects/driving_license/PaddleOCR/tools/train.py", line 137, in main
    model = build_model(config["Architecture"])
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/modeling/architectures/__init__.py", line 30, in build_model
    arch = BaseModel(config)
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/modeling/architectures/base_model.py", line 55, in __init__
    self.backbone = build_backbone(config["Backbone"], model_type)
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/modeling/backbones/__init__.py", line 133, in build_backbone
    module_class = eval(module_name)(**config)
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/modeling/backbones/det_resnet_vd.py", line 293, in __init__
    self.conv1_1 = ConvBNLayer(
  File "/home/ai/nar_projects/driving_license/PaddleOCR/ppocr/modeling/backbones/det_resnet_vd.py", line 127, in __init__
    self._conv = nn.Conv2D(
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/paddle/nn/layer/conv.py", line 690, in __init__
    super().__init__(
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/paddle/nn/layer/conv.py", line 156, in __init__
    self.weight = self.create_parameter(
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/paddle/nn/layer/layers.py", line 781, in create_parameter
    return self._helper.create_parameter(
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/paddle/base/layer_helper_base.py", line 430, in create_parameter
    return self.main_program.global_block().create_parameter(
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/paddle/base/framework.py", line 4381, in create_parameter
    initializer(param, self)
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/paddle/nn/initializer/initializer.py", line 40, in __call__
    return self.forward(param, block)
  File "/home/ai/anaconda3/envs/ocr_gpu2/lib/python3.9/site-packages/paddle/nn/initializer/normal.py", line 75, in forward
    out_var = _C_ops.gaussian(
RuntimeError: (PreconditionNotMet) Cannot load cudnn shared library. Cannot invoke method cudnnGetVersion.
  [Hint: cudnn_dso_handle should not be null.] (at /paddle/paddle/phi/backends/dynload/cudnn.cc:64)
```

- 出现问题的原因参考如下链接：

[PaddleOCR遇到RuntimeError: (PreconditionNotMet) Cannot load cudnn shared library. 错误的解决-CSDN博客](https://blog.csdn.net/WinterShiver/article/details/129902882)

- 解决方案：

在下面的`NVIDIA官网`下载`cuDNN`配置文件

[cuDNN Archive | NVIDIA Developer](https://developer.nvidia.com/rdp/cudnn-archive)

- 每次训练前执行指令：

```shell
export LD_LIBRARY_PATH=xxx/lib:$LD_LIBRARY_PATH
```

注意，设置的路径是`libcudnn.so`的路径

- 可能会遇到另一个`cuda`相关报错，解决方法如下：

```shell
export LD_LIBRARY_PATH=/path/to/anaconda3/envs/env_name/lib:$LD_LIBRARY_PATH
```

## 八、参考文档

[Redirecting](https://paddlepaddle.github.io/PaddleOCR)

遇到瓶颈时，可查阅`paddleocr官网`的`FAQ`模块。


