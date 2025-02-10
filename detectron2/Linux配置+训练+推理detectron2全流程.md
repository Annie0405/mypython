# 一、环境配置

## 1. 虚拟环境创建

```
conda create --name detectron2 python=3.8.16
conda activate detectron2
```

## 2. 安装pycocotools

```
pip install cython -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install "git+https://gitee.com/wsyin/cocoapi.git#subdirectory=PythonAPI"
```

如果提示未安装git：

```
conda install git
```

## 3. 安装cuda和pytroch

别管为什么，就这么装：

```
pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
```

torch比较大，可能会装的很慢，可以先下载到本地：

```
https://download.pytorch.org/whl/cu111/torch-1.9.0%2Bcu111-cp38-cp38-linux_x86_64.whl
https://download.pytorch.org/whl/cu111/torchvision-0.10.0%2Bcu111-cp38-cp38-linux_x86_64.whl
```

然后cd到.whl文件的目录：

```
pip install torch-1.9.0+cu111-cp38-cp38-linux_x86_64.whl
pip install torchvision-0.10.0+cu111-cp38-cp38-linux_x86_64.whl
```

## 4. 安装opencv

```
pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 5. 克隆detectron2源码

```
git clone https://github.com/facebookresearch/detectron2.git
cd detectron2
```

报错超时/找不到地址：多试几次。

## 6. 运行本地安装

```
pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
```

可能遇到如下问题，没有问题则直接跳到第7步：

### we could not find ninja

```
conda install ninja -c conda-forge
```

### No such file or directory: ':/usr/local/cuda/bin/nvcc'

```
which nvcc
# 假设在/usr/local/cuda/bin/nvcc
# 配置CUDA_HOME
export CUDA_HOME=/usr/local/cuda
# 确保LD_LIBRARY_PATH包含CUDA库路径
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

### subprocess.CalledProcessError: Command '['which', 'c++']' returned non-zero exit status 1

```
which c++
# 如果没有返回值
sudo apt update
sudo apt install g++ build-essential
```

## 7. 运行demo.py测试

### 修改demo.py源码

```
# 注释掉第17行，修改为如下：
# from vision.fair.detectron2.demo.predictor import VisualizationDemo
from predictor import VisualizationDemo
```

### 测试指令

```
cd demo
python demo.py --config-file ../configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml --input input.png --output output.png --opts MODEL.WEIGHTS detectron2://COCO-Detection/faster_rcnn_R_50_FPN_3x/137849458/model_final_280758.pkl
```

## 8. 运行训练测试

### 准备数据集

准备COCO格式的数据集，根据`start.py`中的配置来搭建目录结构

### 配置训练环境

直接使用`start.py`和`train_app.py`这两个文件，修改`start.py`中的相关配置，运行即可。

### 可能遇到如下问题：

#### AttributeError: module 'distutils' has no attribute 'version'

更新pytorch（一定不要在前面装新版本pytorch）：

```
pip install --upgrade torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
```

# 二、训练+推理

以下是对代码的解释。配置`start.py`并运行即可快速执行训练和推理。

### 1. 初始化日志记录器

```python
from detectron2.utils.logger import setup_logger
setup_logger()
```

- 通过 `setup_logger()` 设置 Detectron2 的日志记录器，以便后续在控制台输出日志信息，便于调试和监控训练过程。

### 2. 注册数据集

```python
register_coco_instances(
    train, {}, self.register["json_file"]["train"],
    self.register["image_root"]["train"]
)
register_coco_instances(
    val, {}, self.register["json_file"]["val"],
    self.register["image_root"]["val"]
)
register_coco_instances(
    test, {}, self.register["json_file"]["test"],
    self.register["image_root"]["test"]
)
```

- 使用 `register_coco_instances` 将数据集注册为 Detectron2 可以识别的格式。这里的数据集分为训练集、验证集和测试集。
- 第一个参数是数据集名称，是一个字符串；第二个参数是元数据，可置空；第三个参数是json文件路径；第四个参数是图片根目录。

### 3. 获取数据集的元数据

```python
train_metadata = MetadataCatalog.get(train_dataset_name)
val_metadata = MetadataCatalog.get(val_dataset_name)
test_metadata = MetadataCatalog.get(test_dataset_name)
```

- 获取已经注册的数据集的元数据（包括类别信息等），get接收的参数是注册数据集时指定的数据集名称。

### 4. 可视化样本（可选）

```python
metadata = MetadataCatalog.get(test_dataset_name)
dataset_dicts = DatasetCatalog.get(test_dataset_name)
for idx, d in enumerate(dataset_dicts):
    im = cv2.imread(d["file_name"])
    outputs = predictor(im)
    visualizer = Visualizer(im[:, :, ::-1], metadata=metadata,
        scale=1.0, instance_mode=ColorMode.IMAGE)
    out = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
    image_name = os.path.basename(d["file_name"])
    save_path = os.path.join(output_dir, image_name)
    cv2.imwrite(save_path, out.get_image()[:, :, ::-1])
```

- 确保`save_path`路径存在。
- 用于人工检查数据标注是否正确。

### 5. 训练模型

```python
trainer = DefaultTrainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()
```

- 创建一个 `DefaultTrainer` 实例，开始训练过程。
- `resume_or_load(resume=False)` 表示从头开始训练（而不是恢复已有训练）。

# 三、参考链接

https://blog.csdn.net/qq_22583741/article/details/130078485