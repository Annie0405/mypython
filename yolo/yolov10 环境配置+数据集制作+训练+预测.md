# yolov10 环境配置+数据集制作+训练+预测

## 一、环境配置

### 1. yolov10源码下载

[GitHub - THU-MIG/yolov10: YOLOv10: Real-Time End-to-End Object Detection [NeurIPS 2024]](https://github.com/THU-MIG/yolov10)

下载到本地，下翻找到模型权重，下载到`yolov10`根目录下，可以只下载`yolov10n.pt`和`yolov10m.pt`。

### 2. 创建虚拟环境

```shell
conda create -n yolov10 python=3.9
conda activate yolov10
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

### 6. 下载yolov10依赖库

进入yolov10项目的根目录，执行如下指令：

```shell
pip install -r requirements.txt
pip install -e .
```

### 7. 目前使用过的稳定版本

- python=3.9, cudatoolkit=11.8, cudnn=8700, pytorch=2.0.1

## 二、数据集制作

### 1. 数据集标注

使用`labelme`完成数据标注。

### 2. 数据集划分

可按8：1：1的比例划分为训练集、验证集、测试集；

也可按8：2的比例划分为训练集和验证集。

如果总数据量超过10w，那么验证集1w，训练集1w，其他都为训练集。

### 3. 数据集的结构和配置文件

```makefile
train1/
├────images/
│    ├────train/
│    │    ├────train_image0.jpg
│    │    ├────train_image1.jpg
│    │    ├────train_image2.jpg
│    │    └────······
│    ├────val/
│    └────test/
│
└────labels/
     ├────train/
     │    ├────train_label0.txt
     │    ├────train_label1.txt
     │    ├────train_label2.txt
     │    └────······
     ├────val/
     └────test/
```

```yaml
# data.yml
path: /absolute/path/to/dataset/root/dir/train1  # dataset root dir
train: images/train # train images (relative to 'path')
val: images/val # val images (relative to 'path')
test: images/test # test images (optional)

# Classes
names:
  0: class1
  1: class2
```

## 三、训练

### 1. 训练配置

在 yolov10/ultralytics/cfg 目录下找到 default.yaml 文件，修改如下参数：

```yaml
# config.yaml
model: /absolute/path/to/yolov10n.pt
data: /absolute/path/to/data.yml
epochs: 500
patience: 0
batch: 32
save: True
save_period: 50
device: 0
workers: 8
project: /absolute/path/to/yolov10
name: datasets/train/model
pretrained: True
```

### 2. 训练指令

```shell
yolo cfg=path/to/config.yaml
```

### 3. 可能遇到的bug

遇到如下报错：

```shell
Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.
```

解决方法：

在项目目录下执行：

```shell
$env:KMP_DUPLICATE_LIB_OK = 'TRUE'
```

## 四、预测

可以使用如下脚本预测：

```python
# predict.py
from ultralytics import YOLOv10
import os
import cv2

model = YOLOv10("path/to/model.pt")

folder = r"path/to/images/dir"
out_folder = r"path/to/output"
os.makedirs(out_folder, exist_ok=True)

# 设置置信度和IOU阈值
conf_threshold = 0.5  # 置信度阈值
iou_threshold = 0.5   # IOU阈值

for image in os.listdir(folder):
    # 图片路径
    image_path = os.path.join(folder, image)
    # 读取图片
    img = cv2.imread(image_path)
    # 将图像从BGR转为RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 模型预测
    results = model.predict(img_rgb, conf=conf_threshold, iou=iou_threshold)
    # 获取渲染后的结果图像，.plot()方法获取带有检测框的图像
    result_img = results[0].plot()
    # 保存预测结果的路径
    out_path = os.path.join(out_folder, image)
    result_img_bgr = cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(out_path, result_img_bgr)

print("预测结果保存完成！")
```
