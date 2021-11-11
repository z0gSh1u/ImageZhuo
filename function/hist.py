# Histogram
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io


# 对data绘制直方图，返回直方图的PIL Image
def drawHistogram(data: np.ndarray, bins=256):
    fig = plt.figure()
    plt.hist(data.ravel(), bins)
    plt.xlabel('Gray Value')
    plt.ylabel('Pixel Count')

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    pilImage = Image.open(buf).copy()
    buf.close()

    # 调整直方图图片宽度为480
    targetSize = lambda wh, newW: (newW, int(newW / wh[0] * wh[1]))
    pilImage = pilImage.resize(targetSize(pilImage.size, 480))

    return pilImage
