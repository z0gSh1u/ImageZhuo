# Retinex (log domain unsharp masking)
# ImageZhuo by z0gSh1u @ https://github.com/z0gSh1u/ImageZhuo

# 注：本部分代码修改自本人本科的《数字图像处理》（鲍旭东）课程实验代码，学号09017227

import numpy as np

from misc.utils import getMinMax


# 在0~N（N可不为256）范围内做同态滤波
def Retinex(I_: np.ndarray, HH=1.8, HL=0.8, C=1, CUT_FREQ=40):
    # HL 低频减益系数
    # HH 高频增益系数
    # C 坡度控制参数
    # CUT_FREQ 截止频率

    minI, maxI = getMinMax(I_)

    I = I_.copy() + 1.  # 避免log(0)错误
    # 不使用 I=I+微小量 的原因是log(0)→-∞，会对后续exp过程产生影响
    I_log = np.log(I)  # log I = log L + log R

    # * 为保证运算效率，此处调用了numpy的FFT，而非自己实现的FFT。自己实现的FFT可见function/fft.py
    I_log_fft = np.fft.fft2(I_log)  # 对数域作DFT转入频域
    I_log_fft_shift = np.fft.fftshift(I_log_fft)  # shift结果，把低频放到中心而不是四角

    # 接下来设计一个滤波器，它减益低频，增益高频
    # 其中心在图像中心，与前面的shift对应
    def AdjustedGaussFilter(lowAlpha, highAlpha, c, cutFreq, height, width):
        H = np.zeros((height, width))
        squareD0 = cutFreq**2
        delta = highAlpha - lowAlpha
        centerX, centerY = height // 2, width // 2
        for i in range(height):
            for j in range(width):
                squareD = (i - centerX)**2 + (j - centerY)**2
                res = delta * (1 - np.exp(-c * squareD / squareD0)) + lowAlpha
                H[i, j] = res
        return H

    AGF = AdjustedGaussFilter(HL, HH, C, CUT_FREQ, I.shape[0], I.shape[1])

    # 用这个滤波器作用于I_log_fft_shift，可以认为削减了照度L的量
    R_log_fft_shift = I_log_fft_shift * AGF
    # 反傅里叶变换
    R_log_fft = np.fft.ifftshift(R_log_fft_shift)
    R_log = np.fft.ifft2(R_log_fft)
    R = np.abs(np.exp(R_log))  # 指数处理，去掉log
    R = R - 1  # 把之前加的1减去
    # 化到原有区间
    R_norm = np.zeros(R.shape)
    minR, maxR = getMinMax(R)
    rangeR = maxR - minR
    for i in range(R.shape[0]):
        for j in range(R.shape[1]):
            R_norm[i, j] = (R[i, j] - minR) / rangeR * (maxI - minI) + minI

    res = np.array(R_norm, dtype=I_.dtype)
    return res
