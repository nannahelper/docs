"""可复用的 NumPy 网络层。

这里故意不依赖 PyTorch，用来把第 6 章手写的反向传播公式组织成
可以重复调用的函数。每个 forward 函数都会返回 cache，供对应的
backward 函数使用。
"""

import numpy as np


def linear_forward(inputs, weights, bias):
    """计算线性层 z = inputs @ weights + bias。

    参数
    ----
    inputs : np.ndarray
        单个样本形状为 (input_dim,)，批量样本形状为
        (batch_size, input_dim)。
    weights : np.ndarray
        形状为 (input_dim, output_dim)。
    bias : np.ndarray
        形状为 (output_dim,)。

    返回
    ----
    z : np.ndarray
        线性层输出。
    cache : tuple
        反向传播所需的 (inputs, weights, bias)。
    """
    z = inputs @ weights + bias
    return z, (inputs, weights, bias)


def linear_backward(dz, cache):
    """通过线性层反向传播。

    `dz` 是损失对 z 的梯度。这里不自动除以 batch size；损失函数
    是否取平均由调用方决定，这样公式和梯度检查更清楚。
    """
    inputs, weights, _ = cache

    if inputs.ndim == 1:
        d_weights = np.outer(inputs, dz)
        d_bias = dz.copy()
    else:
        d_weights = inputs.T @ dz
        d_bias = dz.sum(axis=0)

    d_inputs = dz @ weights.T
    return d_inputs, d_weights, d_bias


def relu_forward(z):
    """ReLU 前向传播：max(0, z)。"""
    activations = np.maximum(z, 0)
    return activations, z


def relu_backward(d_activations, cache):
    """通过 ReLU 反向传播。

    cache 保存的是 ReLU 的输入 z，而不是输出。z>0 的位置让梯度
    通过，z<=0 的位置把梯度置为 0。
    """
    z = cache
    return d_activations * (z > 0)


def mse_loss(predictions, targets):
    """半均方误差：0.5 * mean((predictions - targets) ** 2)。"""
    return 0.5 * np.mean((predictions - targets) ** 2)


def mse_backward(predictions, targets):
    """半均方误差对 predictions 的梯度。"""
    if predictions.ndim == 0:
        return predictions - targets
    return (predictions - targets) / predictions.shape[0]

def softmax(logits):
    max_value = np.max(logits, axis=-1, keepdims=True)

    shifted = logits - max_value
    exp_values = np.exp(shifted)

    total = np.sum(exp_values, axis=-1, keepdims=True)

    probabilities = exp_values / total

    return probabilities
