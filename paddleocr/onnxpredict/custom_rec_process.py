import copy
import math
import cv2
import numpy as np
# 必须导入，这些是 eval 动态实例化用到的类名
from custom_rec_operators import CTCLabelDecode


def build_post_process(config, global_config=None):
    support_dict = [
        "DBPostProcess",
        "EASTPostProcess",
        "SASTPostProcess",
        "FCEPostProcess",
        "CTCLabelDecode",
        "AttnLabelDecode",
        "ClsPostProcess",
        "SRNLabelDecode",
        "PGPostProcess",
        "DistillationCTCLabelDecode",
        "TableLabelDecode",
        "DistillationDBPostProcess",
        "NRTRLabelDecode",
        "SARLabelDecode",
        "SEEDLabelDecode",
        "VQASerTokenLayoutLMPostProcess",
        "VQAReTokenLayoutLMPostProcess",
        "PRENLabelDecode",
        "DistillationSARLabelDecode",
        "ViTSTRLabelDecode",
        "ABINetLabelDecode",
        "TableMasterLabelDecode",
        "SPINLabelDecode",
        "DistillationSerPostProcess",
        "DistillationRePostProcess",
        "VLLabelDecode",
        "PicoDetPostProcess",
        "CTPostProcess",
        "RFLLabelDecode",
        "DRRGPostprocess",
        "CANLabelDecode",
        "SATRNLabelDecode",
        "ParseQLabelDecode",
        "CPPDLabelDecode",
        "LaTeXOCRDecode",
    ]

    if config["name"] == "PSEPostProcess":
        support_dict.append("PSEPostProcess")

    config = copy.deepcopy(config)
    module_name = config.pop("name")
    if module_name == "None":
        return
    if global_config is not None:
        config.update(global_config)
    assert module_name in support_dict, Exception(
        "post process only support {}".format(support_dict)
    )
    module_class = eval(module_name)(**config)
    return module_class


def resize_norm_img(shape, input_tensor, img, max_wh_ratio):
    imgC, imgH, imgW = shape

    assert imgC == img.shape[2]
    imgW = int((imgH * max_wh_ratio))
    w = input_tensor.shape[3:][0]
    if isinstance(w, str):
        pass
    elif w is not None and w > 0:
        imgW = w
    h, w = img.shape[:2]
    ratio = w / float(h)
    if math.ceil(imgH * ratio) > imgW:
        resized_w = imgW
    else:
        resized_w = int(math.ceil(imgH * ratio))
    resized_image = cv2.resize(img, (resized_w, imgH))
    resized_image = resized_image.astype("float32")
    resized_image = resized_image.transpose((2, 0, 1)) / 255
    resized_image -= 0.5
    resized_image /= 0.5
    padding_im = np.zeros((imgC, imgH, imgW), dtype=np.float32)
    padding_im[:, :, 0:resized_w] = resized_image
    return padding_im
