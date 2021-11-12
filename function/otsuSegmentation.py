# Otsu threshold segmentation
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np


# 大津阈值分割，返回二值图
def OtsuSegmentation(data: np.ndarray, h, w):
    min_ = np.min(data)
    max_ = np.max(data)
    res = np.zeros_like(data, dtype=np.uint8)
    total_pixel = h * w

    def OtsuThreshold(I):
        var_max = 0
        best_th = 0
        for th in range(min_, max_):
            mask_fore = I > th
            mask_back = I <= th  # 按当前测试阈值分割
            len_fore = np.sum(mask_fore)
            len_back = np.sum(mask_back)  # 前后景像素数
            if len_fore == 0:  # 已经分不出前景了，没有必要继续提高阈值了
                break
            if len_back == 0:  # 背景过多，说明阈值不够，继续提高
                continue
            # 算法相关参数
            w0 = float(len_fore) / total_pixel
            w1 = float(len_back) / total_pixel  # 两类的占比
            u0 = float(np.sum(I * mask_fore)) / len_fore
            u1 = float(np.sum(I * mask_back)) / len_back  # 两类的平均灰度
            var = w0 * w1 * ((u0 - u1)**2)  # 类间方差
            if var > var_max:
                var_max = var
                best_th = th
        return best_th

    threshold = OtsuThreshold(data)
    # 按该阈值进行二值化
    for i in range(h):
        for j in range(w):
            res[i, j] = 255 if data[i, j] > threshold else 0

    return res