# 借助旧版本的detectron2代码实现mask模型的导出与部署

## 一、环境安装

### 1. 源码克隆

https://github.com/facebookresearch/detectron2/tree/v0.3

### 2. 创建conda环境

```shell
conda create --name dt_export python==3.8.16
conda activate dt_export
```

### 3. 安装pytorch

```shell
pip install torch==1.8.1 torchvision==0.9.1
```

### 4. 安装detectron2

```shell
pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 5. 安装其他依赖

```shell
conda install opencv
pip install onnx==1.17.0
pip install pillow==8.0.0
pip install protobuf==3.20.0
```

## 二、模型导出

### 1. 导出模型配置

```python
# 在训练的环境下导出
cfg = _get_cfg()	# 模型训练时的配置
with open("config.yaml", "w") as f:
    f.write(cfg.dump())
```

### 2. 修改配置文件

删去以下配置项：

- `DATALOADER.REPEAT_SQRT`

- `FLOAT32_PRECISION`
- `MODEL.ROI_BOX_HEAD.FED_LOSS_FREQ_WEIGHT_POWER`
- `MODEL.ROI_BOX_HEAD.FED_LOSS_NUM_CLASSES`
- `MODEL.ROI_BOX_HEAD.USE_FED_LOSS`
- `MODEL.ROI_BOX_HEAD.USE_SIGMOID_CE`
- `MODEL.ROI_HEADS.OHEM`
- `MODEL.RPN.CONV_DIMS`    # 有两个`CONV_DIMS`，别删错了
- `SOLVER.BASE_LR_END`
- `SOLVER.NUM_DECAYS`
- `SOLVER.RESCALE_INTERVAL`

修改以下配置项：

- `INPUT.MIN_SIZE_TRAIN: (800, )`

### 3. 修改`tools/deploy/caffe2_converter.py`

```python
# 以下代码替换setup_cfg函数的内容
# 注册内容和训练时保持一致，注册任意一个数据集即可
# 合并自己导出的配置文件
def setup_cfg(args):
    cfg = get_cfg()
    register_coco_instances("name", {}, "json_file", "image_root")
    cfg.merge_from_file("config.yaml")
    cfg = add_export_config(cfg)
    cfg.freeze()

    if cfg.MODEL.DEVICE != "cpu":
        TORCH_VERSION = tuple(int(x) for x in torch.__version__.split(".")[:2])
        assert TORCH_VERSION >= (1, 5), "PyTorch>=1.5 required for GPU conversion!"

    return cfg
```

### 4. 导出指令

```shell
python tools/deploy/caffe2_converter.py  --format torchscript --output train_data/train1/3_output/models  MODEL.DEVICE gpu
```

## 三、部署和推理

### 1. 环境安装

- 直接使用导出时的环境

- ```shell
  # 单独安装推理的环境
  pip install torch==1.8.1 torchvision==0.9.1
  conda install opencv
  ```

### 2. 推理代码

```python
from __future__ import division
import torch
from torch import device
from torch.nn import functional as F
import cv2
import numpy as np
from typing import Any, List, Tuple

TORCH_VERSION = tuple(int(x) for x in torch.__version__.split(".")[:2])

model_path = "train_data/train1/3_output/models/model.ts"
model_local = torch.jit.load(model_path, _extra_files={"_caffe2::GenerateProposals": ""})
model_size = (2000, 1125)

image_path = "train_data/train1/2_labels/test_images/1L_a008.jpeg"
image = cv2.imread(image_path)

ori_h, ori_w = image.shape[:2]

if model_size[1]/ori_h <= model_size[0]/ori_w:
    new_h = model_size[1]
    new_w = int(round(ori_w * model_size[1] / ori_h))
    scale = ori_h / model_size[1]
else:
    new_w = model_size[0]
    new_h = int(round(ori_h * model_size[0] / ori_w))
    scale = ori_w / model_size[0]

resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

padded_image = np.zeros((model_size[1], model_size[0], 3), dtype=np.uint8)  # 创建空白填充图像，大小为模型输入尺寸
padded_image[:new_h, :new_w, :] = resized_image     # 将 resized_image 贴到左上角

tensor_image = torch.tensor(padded_image, dtype=torch.uint8).permute(2, 0, 1).unsqueeze(0).cuda()   # 转换为 PyTorch Tensor，并调整形状为 (1, 3, H, W)
im_info = torch.tensor([[model_size[1], model_size[0], scale]], dtype=torch.float32).cuda()     # 生成 im_info 张量 (固定H, 固定W, scale_factor)

# 这段是直接复制的别人的轮子，能不改尽量不改
class ImageList(object):
    """
    Structure that holds a list of images (of possibly
    varying sizes) as a single tensor.
    This works by padding the images to the same size,
    and storing in a field the original sizes of each image

    Attributes:
        image_sizes (list[tuple[int, int]]): each tuple is (h, w)
    """

    def __init__(self, tensor: torch.Tensor, image_sizes: List[Tuple[int, int]]):
        """
        Arguments:
            tensor (Tensor): of shape (N, H, W) or (N, C_1, ..., C_K, H, W) where K >= 1
            image_sizes (list[tuple[int, int]]): Each tuple is (h, w). It can
                be smaller than (H, W) due to padding.
        """
        self.tensor = tensor
        self.image_sizes = image_sizes

    def __len__(self) -> int:
        return len(self.image_sizes)

    def __getitem__(self, idx) -> torch.Tensor:
        """
        Access the individual image in its original size.

        Args:
            idx: int or slice

        Returns:
            Tensor: an image of shape (H, W) or (C_1, ..., C_K, H, W) where K >= 1
        """
        size = self.image_sizes[idx]
        return self.tensor[idx, ..., : size[0], : size[1]]

    @torch.jit.unused
    def to(self, *args: Any, **kwargs: Any) -> "ImageList":
        cast_tensor = self.tensor.to(*args, **kwargs)
        return ImageList(cast_tensor, self.image_sizes)

    @property
    def device(self) -> device:
        return self.tensor.device

    @staticmethod
    def from_tensors(
        tensors: List[torch.Tensor], size_divisibility: int = 0, pad_value: float = 0.0
    ) -> "ImageList":
        """
        Args:
            tensors: a tuple or list of `torch.Tensors`, each of shape (Hi, Wi) or
                (C_1, ..., C_K, Hi, Wi) where K >= 1. The Tensors will be padded
                to the same shape with `pad_value`.
            size_divisibility (int): If `size_divisibility > 0`, add padding to ensure
                the common height and width is divisible by `size_divisibility`.
                This depends on the model and many models need a divisibility of 32.
            pad_value (float): value to pad

        Returns:
            an `ImageList`.
        """
        assert len(tensors) > 0
        assert isinstance(tensors, (tuple, list))
        for t in tensors:
            assert isinstance(t, torch.Tensor), type(t)
            assert t.shape[1:-2] == tensors[0].shape[1:-2], t.shape

        # Magic code below that handles dynamic shapes for both scripting and tracing ...

        image_sizes = [(im.shape[-2], im.shape[-1]) for im in tensors]

        if torch.jit.is_scripting():
            max_size = torch.stack([torch.as_tensor(x) for x in image_sizes]).max(0).values
            if size_divisibility > 1:
                stride = size_divisibility
                # the last two dims are H,W, both subject to divisibility requirement
                max_size = (max_size + (stride - 1)) // stride * stride

            max_size: List[int] = max_size.to(dtype=torch.long).tolist()
        else:
            # https://github.com/pytorch/pytorch/issues/42448
            if TORCH_VERSION >= (1, 7) and torch.jit.is_tracing():
                # In tracing mode, x.shape[i] is a scalar Tensor, and should not be converted
                # to int: this will cause the traced graph to have hard-coded shapes.
                # Instead we convert each shape to a vector with a stack()
                image_sizes = [torch.stack(x) for x in image_sizes]

                # maximum (H, W) for the last two dims
                # find the maximum in a tracable way
                max_size = torch.stack(image_sizes).max(0).values
            else:
                # Original eager logic here -- not scripting, not tracing:
                # (can be unified with scripting after
                # https://github.com/pytorch/pytorch/issues/47379)
                max_size = torch.as_tensor(
                    [max(s) for s in zip(*[img.shape[-2:] for img in tensors])]
                )

            if size_divisibility > 1:
                stride = size_divisibility
                # the last two dims are H,W, both subject to divisibility requirement
                max_size = (max_size + (stride - 1)) // stride * stride

        if len(tensors) == 1:
            # This seems slightly (2%) faster.
            # TODO: check whether it's faster for multiple images as well
            image_size = image_sizes[0]
            padding_size = [0, max_size[-1] - image_size[1], 0, max_size[-2] - image_size[0]]
            batched_imgs = F.pad(tensors[0], padding_size, value=pad_value).unsqueeze_(0)
        else:
            # max_size can be a tensor in tracing mode, therefore convert to list
            batch_shape = [len(tensors)] + list(tensors[0].shape[:-2]) + list(max_size)
            batched_imgs = tensors[0].new_full(batch_shape, pad_value)
            for img, pad_img in zip(tensors, batched_imgs):
                pad_img[..., : img.shape[-2], : img.shape[-1]].copy_(img)

        return ImageList(batched_imgs.contiguous(), image_sizes)

tensor_image = torch.tensor(padded_image, dtype=torch.uint8).permute(2, 0, 1)
tensor_image = ImageList.from_tensors([tensor_image], 32)
tensor_image = tensor_image.tensor.cuda()

inputs = (tensor_image, im_info)

y2_local = model_local(inputs)
print('y2_local:', y2_local)
```

## 四、参考资料

detectron2 模型部署大作战2

https://juejin.cn/post/6844904201135357960