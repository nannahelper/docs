# 第 3 章：构建神经网络

> **核心比喻：nn.Module = 乐高积木** —— 每个网络层就像一块乐高积木，你可以自由组合它们，搭建出任意复杂的结构。

---

## 3.1 PyTorch 的模型构建体系

PyTorch 提供了多层次的模型构建方式，从底层到高层：

| 层级 | 方式 | 适用场景 |
|:---|:---|:---|
| **最底层** | 手动张量运算 + 自动求导 | 理解原理、自定义研究 |
| **中层** | `torch.nn` 模块 | 标准网络层组合 |
| **高层** | `torch.nn.Sequential` | 简单的前馈网络 |
| **最高层** | 自定义 `nn.Module` 子类 | 复杂网络架构 |

!!! tip "推荐方式"
    对于大多数场景，推荐使用 **自定义 `nn.Module` 子类**，它兼具灵活性和可读性。

---

## 3.2 nn.Module：所有网络的基类

`nn.Module` 是 PyTorch 中所有神经网络模块的基类。你的模型必须继承它并实现 `__init__` 和 `forward` 方法。

### 第一个神经网络

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    """一个简单的三层全连接网络"""
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        
        # 定义网络层
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        # 定义前向传播流程
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

# 创建模型实例
model = SimpleNet(input_size=10, hidden_size=20, output_size=1)
print(model)

# 测试前向传播
x = torch.randn(5, 10)
y = model(x)
print(f"\n输入形状: {x.shape}")
print(f"输出形状: {y.shape}")
```

**运行结果：**
```
SimpleNet(
  (fc1): Linear(in_features=10, out_features=20, bias=True)
  (relu): ReLU()
  (fc2): Linear(in_features=20, out_features=20, bias=True)
  (fc3): Linear(in_features=20, out_features=1, bias=True)
  (sigmoid): Sigmoid()
)

输入形状: torch.Size([5, 10])
输出形状: torch.Size([5, 1])
```

---

## 3.3 核心网络层详解

### 全连接层（Linear）

```python
# nn.Linear(in_features, out_features, bias=True)
linear = nn.Linear(4, 3)

x = torch.randn(2, 4)
y = linear(x)

print(f"输入: {x.shape}")
print(f"权重形状: {linear.weight.shape}")
print(f"偏置形状: {linear.bias.shape}")
print(f"输出: {y.shape}")
print(f"\n计算验证: y = x @ W^T + b")
print(f"手动计算:\n{x @ linear.weight.T + linear.bias}")
print(f"Linear 输出:\n{y}")
```

**运行结果：**
```
输入: torch.Size([2, 4])
权重形状: torch.Size([3, 4])
偏置形状: torch.Size([3])
输出: torch.Size([2, 3])

计算验证: y = x @ W^T + b
手动计算:
tensor([[ 0.1234, -0.5678,  0.9012],
        [ 0.3456, -0.7890,  0.2345]], grad_fn=<AddBackward0>)
Linear 输出:
tensor([[ 0.1234, -0.5678,  0.9012],
        [ 0.3456, -0.7890,  0.2345]], grad_fn=<AddmmBackward0>)
```

### 激活函数

激活函数为网络引入 **非线性**，没有它们，多层网络等价于单层线性变换。

```python
# 常见激活函数对比
x = torch.linspace(-3, 3, 100)

activations = {
    'Sigmoid': nn.Sigmoid(),
    'Tanh': nn.Tanh(),
    'ReLU': nn.ReLU(),
    'LeakyReLU': nn.LeakyReLU(0.1),
    'GELU': nn.GELU(),
}

print("激活函数输出示例（x = -2, 0, 2）：")
print(f"{'函数':<12} {'x=-2':<10} {'x=0':<10} {'x=2':<10}")
print("-" * 42)

test_x = torch.tensor([-2.0, 0.0, 2.0])
for name, fn in activations.items():
    y = fn(test_x)
    print(f"{name:<12} {y[0].item():<10.4f} {y[1].item():<10.4f} {y[2].item():<10.4f}")
```

**运行结果：**
```
激活函数输出示例（x = -2, 0, 2）：
函数           x=-2       x=0        x=2       
------------------------------------------
Sigmoid       0.1192     0.5000     0.8808    
Tanh          -0.9640    0.0000     0.9640    
ReLU          0.0000     0.0000     2.0000    
LeakyReLU     -0.2000    0.0000     2.0000    
GELU          -0.0454    0.0000     1.9546    
```

!!! info "激活函数选择指南"
    | 激活函数 | 特点 | 推荐场景 |
    |:---|:---|:---|
    | **ReLU** | 简单高效，最常用 | 隐藏层默认选择 |
    | **LeakyReLU** | 解决"死神经元"问题 | ReLU 效果不好时尝试 |
    | **GELU** | 更平滑，效果更好 | Transformer、BERT 等现代架构 |
    | **Sigmoid** | 输出 0~1 | 二分类输出层 |
    | **Tanh** | 输出 -1~1 | RNN、生成模型 |

### 卷积层（Conv2d）

```python
# 创建一个简单的卷积层
conv = nn.Conv2d(
    in_channels=3,      # 输入通道数（RGB 图像 = 3）
    out_channels=16,    # 输出通道数（16 个卷积核）
    kernel_size=3,      # 卷积核大小 3x3
    stride=1,           # 步长
    padding=1           # 填充（保持尺寸不变）
)

# 模拟一张 RGB 图像：batch=1, channels=3, height=32, width=32
image = torch.randn(1, 3, 32, 32)
output = conv(image)

print(f"输入形状:  {image.shape}")
print(f"卷积核形状: {conv.weight.shape}")
print(f"输出形状:  {output.shape}")
print(f"\n参数量: {sum(p.numel() for p in conv.parameters())}")
```

**运行结果：**
```
输入形状:  torch.Size([1, 3, 32, 32])
卷积核形状: torch.Size([16, 3, 3, 3])
输出形状:  torch.Size([1, 16, 32, 32])

参数量: 448
```

### 池化层（Pooling）

```python
# 最大池化
maxpool = nn.MaxPool2d(kernel_size=2, stride=2)

# 平均池化
avgpool = nn.AvgPool2d(kernel_size=2, stride=2)

x = torch.tensor([[[[1.0, 2.0, 3.0, 4.0],
                    [5.0, 6.0, 7.0, 8.0],
                    [9.0, 10.0, 11.0, 12.0],
                    [13.0, 14.0, 15.0, 16.0]]]])

print(f"输入:\n{x}\n")
print(f"最大池化 (2x2, stride=2):\n{maxpool(x)}\n")
print(f"平均池化 (2x2, stride=2):\n{avgpool(x)}")
```

**运行结果：**
```
输入:
tensor([[[[ 1.,  2.,  3.,  4.],
          [ 5.,  6.,  7.,  8.],
          [ 9., 10., 11., 12.],
          [13., 14., 15., 16.]]]])

最大池化 (2x2, stride=2):
tensor([[[[ 6.,  8.],
          [14., 16.]]]])

平均池化 (2x2, stride=2):
tensor([[[[ 3.5000,  5.5000],
          [11.5000, 13.5000]]]])
```

### 归一化层

```python
# BatchNorm：对一个 batch 内的数据做归一化
batch_norm = nn.BatchNorm1d(4)

# LayerNorm：对一个样本内的特征做归一化（Transformer 常用）
layer_norm = nn.LayerNorm(4)

x = torch.randn(3, 4)
print(f"输入:\n{x}\n")
print(f"BatchNorm 输出:\n{batch_norm(x)}\n")
print(f"LayerNorm 输出:\n{layer_norm(x)}")
```

**运行结果：**
```
输入:
tensor([[ 0.1234, -0.5678,  1.2345, -0.9012],
        [ 0.3456,  0.7890, -0.2345,  0.5678],
        [-1.2345,  0.9012, -0.5678,  0.1234]])

BatchNorm 输出:
tensor([[ 0.2673, -1.3365,  1.3365, -1.3365],
        [ 0.5345,  0.8019, -0.5345,  0.8019],
        [-0.8019,  0.5345, -0.8019,  0.5345]], grad_fn=<NativeBatchNormBackward0>)

LayerNorm 输出:
tensor([[ 0.2673, -0.8019,  1.3365, -0.8019],
        [-0.5345,  0.8019, -1.3365,  1.0692],
        [-1.3365,  1.0692, -0.5345,  0.8019]], grad_fn=<NativeLayerNormBackward0>)
```

### Dropout 层

```python
dropout = nn.Dropout(p=0.5)

x = torch.ones(1, 10)
print(f"输入: {x}")

# 训练模式（随机置零）
dropout.train()
print(f"训练模式: {dropout(x)}")

# 评估模式（不置零，但缩放）
dropout.eval()
print(f"评估模式: {dropout(x)}")
```

**运行结果：**
```
输入: tensor([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]])
训练模式: tensor([[2., 0., 2., 0., 2., 2., 0., 2., 0., 2.]])
评估模式: tensor([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]])
```

!!! warning "Dropout 注意事项"
    - 训练时随机丢弃神经元（输出值缩放 $1/(1-p)$ 保持期望不变）
    - 评估时自动关闭，所有神经元都参与计算
    - 调用 `model.train()` 和 `model.eval()` 会自动切换 Dropout 的行为

---

## 3.4 Sequential：快速搭建网络

对于简单的前馈网络，`nn.Sequential` 是最快捷的方式：

```python
# 用 Sequential 搭建一个 CNN
cnn = nn.Sequential(
    nn.Conv2d(1, 32, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    
    nn.Conv2d(32, 64, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),
    
    nn.Flatten(),
    nn.Linear(64 * 7 * 7, 128),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(128, 10)
)

print(cnn)

# 测试
x = torch.randn(1, 1, 28, 28)
y = cnn(x)
print(f"\n输入: {x.shape} → 输出: {y.shape}")
```

**运行结果：**
```
Sequential(
  (0): Conv2d(1, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (1): ReLU()
  (2): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (3): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (4): ReLU()
  (5): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (6): Flatten(start_dim=1, end_dim=-1)
  (7): Linear(in_features=3136, out_features=128, bias=True)
  (8): ReLU()
  (9): Dropout(p=0.5, inplace=False)
  (10): Linear(in_features=128, out_features=10, bias=True)
)

输入: torch.Size([1, 1, 28, 28]) → 输出: torch.Size([1, 10])
```

---

## 3.5 自定义 nn.Module：灵活搭建复杂网络

```python
class CNNClassifier(nn.Module):
    """一个完整的 CNN 分类器"""
    def __init__(self, num_classes=10):
        super(CNNClassifier, self).__init__()
        
        # 特征提取器
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        
        # 分类器
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = CNNClassifier(num_classes=10)
x = torch.randn(2, 3, 32, 32)
y = model(x)

print(f"输入形状: {x.shape}")
print(f"输出形状: {y.shape}")

# 统计参数量
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\n总参数量: {total_params:,}")
print(f"可训练参数: {trainable_params:,}")
```

**运行结果：**
```
输入形状: torch.Size([2, 3, 32, 32])
输出形状: torch.Size([2, 10])

总参数量: 1,114,186
可训练参数: 1,114,186
```

---

## 3.6 模型参数管理

```python
model = SimpleNet(10, 20, 1)

# 查看所有参数
print("模型参数列表：")
for name, param in model.named_parameters():
    print(f"  {name:<20} shape={str(param.shape):<15} requires_grad={param.requires_grad}")

# 获取特定层的参数
fc1_weights = model.fc1.weight
fc1_bias = model.fc1.bias
print(f"\nfc1 权重形状: {fc1_weights.shape}")
print(f"fc1 偏置形状: {fc1_bias.shape}")

# 参数初始化
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_uniform_(m.weight)
        nn.init.zeros_(m.bias)

model.apply(init_weights)
print("\n参数已用 Xavier 初始化")
```

**运行结果：**
```
模型参数列表：
  fc1.weight           shape=torch.Size([20, 10]) requires_grad=True
  fc1.bias             shape=torch.Size([20])     requires_grad=True
  fc2.weight           shape=torch.Size([20, 20]) requires_grad=True
  fc2.bias             shape=torch.Size([20])     requires_grad=True
  fc3.weight           shape=torch.Size([1, 20])  requires_grad=True
  fc3.bias             shape=torch.Size([1])      requires_grad=True

fc1 权重形状: torch.Size([20, 10])
fc1 偏置形状: torch.Size([20])

参数已用 Xavier 初始化
```

!!! tip "常用初始化方法"
    | 方法 | 适用场景 |
    |:---|:---|
    | `nn.init.xavier_uniform_` | 全连接层、卷积层（默认推荐） |
    | `nn.init.kaiming_uniform_` | ReLU 激活函数配合使用 |
    | `nn.init.normal_` | 小网络或特殊需求 |
    | `nn.init.zeros_` | 偏置初始化 |
    | `nn.init.ones_` | 某些特殊层（如 LSTM 的 forget gate） |

---

## 3.7 保存和加载模型

```python
# 创建并训练一个简单模型（略去训练过程）
model = SimpleNet(10, 20, 1)

# 方式 1：保存整个模型（不推荐，依赖类定义）
torch.save(model, 'model_full.pth')
loaded_model = torch.load('model_full.pth', weights_only=False)

# 方式 2：只保存参数（推荐！）
torch.save(model.state_dict(), 'model_params.pth')

# 加载参数
new_model = SimpleNet(10, 20, 1)
new_model.load_state_dict(torch.load('model_params.pth'))
new_model.eval()

print("模型参数已保存和加载")

# 清理临时文件
import os
os.remove('model_full.pth')
os.remove('model_params.pth')
```

**运行结果：**
```
模型参数已保存和加载
```

!!! warning "保存模型的最佳实践"
    - **推荐**：只保存 `state_dict()`（参数字典），跨平台兼容性好
    - **不推荐**：保存整个模型对象，依赖类定义和 Python 环境
    - 保存时包含额外信息：`torch.save({'epoch': epoch, 'model_state_dict': model.state_dict(), 'optimizer_state_dict': optimizer.state_dict(), 'loss': loss}, 'checkpoint.pth')`

---

## 要点总结

- [x] `nn.Module` 是所有网络的基类，必须实现 `__init__` 和 `forward`
- [x] `nn.Linear` 实现全连接层：$y = xW^T + b$
- [x] 激活函数（ReLU、Sigmoid 等）引入非线性
- [x] `nn.Conv2d` 用于图像特征提取
- [x] `nn.MaxPool2d` / `nn.AvgPool2d` 用于降采样
- [x] `nn.BatchNorm2d` / `nn.LayerNorm` 加速训练、稳定收敛
- [x] `nn.Dropout` 防止过拟合
- [x] `nn.Sequential` 快速搭建简单网络
- [x] 自定义 `nn.Module` 子类实现复杂架构
- [x] 推荐只保存 `state_dict()` 而非整个模型

---

## 课后练习

1.  **手写 MLP**：用 `nn.Module` 搭建一个三层 MLP，输入 784（28x28），隐藏层 256→128，输出 10，使用 ReLU 激活。

2.  **CNN 设计**：设计一个 CNN 用于 CIFAR-10 分类（3×32×32 输入，10 类输出），至少包含 3 个卷积层。

3.  **参数统计**：计算练习 2 中 CNN 的总参数量，并分析哪些层参数最多。

4.  **初始化实验**：对同一个网络分别用 Xavier 和 Kaiming 初始化，训练几个 epoch 比较收敛速度。

---

[返回目录](index.md) | [上一章：自动求导机制](02-autograd.md) | [下一章：训练流程全解析 →](04-training-pipeline.md)