# 第 1 章：张量操作基础

> **核心比喻：张量 = 多维数组容器** —— 就像快递盒可以装不同形状的物品，张量可以存储任意维度的数据。

---

## 1.1 什么是张量？

!!! example "生活化类比"
    想象你有一个 **收纳盒系统**：
    
    - **标量（0 维张量）**：一个单独的数字，就像盒子里的 **一颗糖**
    - **向量（1 维张量）**：一排数字，就像 **一列火车车厢**
    - **矩阵（2 维张量）**：一个表格，就像 **Excel 电子表格**
    - **3 维张量**：多张表格叠在一起，就像 **一本有多页的账本**
    - **更高维张量**：多个账本放在不同书架上，就像 **图书馆的藏书体系**

在 PyTorch 中，**张量（Tensor）** 是最基本的数据结构，类似于 NumPy 的 `ndarray`，但增加了 GPU 加速和自动求导的能力。

---

## 1.2 创建张量

### 从列表创建

```python
import torch
import numpy as np

# 从 Python 列表创建
scalar = torch.tensor(3.14)
vector = torch.tensor([1, 2, 3, 4])
matrix = torch.tensor([[1, 2], [3, 4], [5, 6]])

print(f"标量: {scalar}, 形状: {scalar.shape}")
print(f"向量: {vector}, 形状: {vector.shape}")
print(f"矩阵:\n{matrix}, 形状: {matrix.shape}")
```

**运行结果：**
```
标量: 3.1400, 形状: torch.Size([])
向量: tensor([1, 2, 3, 4]), 形状: torch.Size([4])
矩阵:
tensor([[1, 2],
        [3, 4],
        [5, 6]]), 形状: torch.Size([3, 2])
```

### 使用内置函数创建

```python
# 全零张量
zeros = torch.zeros(3, 4)

# 全一张量
ones = torch.ones(2, 3)

# 随机张量（均匀分布）
rand = torch.rand(2, 3)

# 随机张量（标准正态分布）
randn = torch.randn(2, 3)

# 指定值的张量
full = torch.full((2, 3), 7.0)

# 单位矩阵
eye = torch.eye(3)

# 等差序列
arange = torch.arange(0, 10, 2)

# 等分序列
linspace = torch.linspace(0, 1, 5)

print(f"全零:\n{zeros}\n")
print(f"全一:\n{ones}\n")
print(f"均匀随机:\n{rand}\n")
print(f"正态随机:\n{randn}\n")
print(f"填充 7:\n{full}\n")
print(f"单位矩阵:\n{eye}\n")
print(f"等差: {arange}")
print(f"等分: {linspace}")
```

**运行结果：**
```
全零:
tensor([[0., 0., 0., 0.],
        [0., 0., 0., 0.],
        [0., 0., 0., 0.]])

全一:
tensor([[1., 1., 1.],
        [1., 1., 1.]])

均匀随机:
tensor([[0.1234, 0.5678, 0.9012],
        [0.3456, 0.7890, 0.2345]])

正态随机:
tensor([[ 0.1234, -0.5678,  1.2345],
        [-0.9012,  0.3456, -0.7890]])

填充 7:
tensor([[7., 7., 7.],
        [7., 7., 7.]])

单位矩阵:
tensor([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]])

等差: tensor([0, 2, 4, 6, 8])
等分: tensor([0.0000, 0.2500, 0.5000, 0.7500, 1.0000])
```

### 从 NumPy 数组创建

```python
# NumPy 转 PyTorch
np_array = np.array([[1, 2], [3, 4]])
tensor_from_np = torch.from_numpy(np_array)

# PyTorch 转 NumPy
tensor = torch.tensor([[5, 6], [7, 8]])
np_from_tensor = tensor.numpy()

print(f"从 NumPy 创建:\n{tensor_from_np}")
print(f"转为 NumPy:\n{np_from_tensor}")

# 注意：它们共享内存！
np_array[0, 0] = 999
print(f"修改 NumPy 后张量也变了:\n{tensor_from_np}")
```

**运行结果：**
```
从 NumPy 创建:
tensor([[1, 2],
        [3, 4]])
转为 NumPy:
[[5 6]
 [7 8]]
修改 NumPy 后张量也变了:
tensor([[999,   2],
        [  3,   4]])
```

!!! warning "内存共享注意"
    `torch.from_numpy()` 创建的张量与原始 NumPy 数组 **共享内存**。如果需要独立副本，使用 `torch.tensor(np_array)` 或 `.clone()`。

---

## 1.3 张量属性

```python
tensor = torch.randn(2, 3, 4)

print(f"形状 (shape):     {tensor.shape}")
print(f"维度数 (ndim):    {tensor.ndim}")
print(f"元素总数:         {tensor.numel()}")
print(f"数据类型 (dtype): {tensor.dtype}")
print(f"所在设备:         {tensor.device}")
print(f"是否需要梯度:     {tensor.requires_grad}")
```

**运行结果：**
```
形状 (shape):     torch.Size([2, 3, 4])
维度数 (ndim):    3
元素总数:         24
数据类型 (dtype): torch.float32
所在设备:         cpu
是否需要梯度:     False
```

---

## 1.4 数据类型

PyTorch 支持多种数据类型，选择合适的类型可以节省内存并提升性能：

```python
# 常见数据类型
float_tensor = torch.tensor([1.0, 2.0], dtype=torch.float32)
double_tensor = torch.tensor([1.0, 2.0], dtype=torch.float64)
int_tensor = torch.tensor([1, 2], dtype=torch.int32)
long_tensor = torch.tensor([1, 2], dtype=torch.int64)
bool_tensor = torch.tensor([True, False])

print(f"float32: {float_tensor.dtype}")
print(f"float64: {double_tensor.dtype}")
print(f"int32:   {int_tensor.dtype}")
print(f"int64:   {long_tensor.dtype}")
print(f"bool:    {bool_tensor.dtype}")

# 类型转换
a = torch.tensor([1, 2, 3])
b = a.float()
c = a.double()
d = a.to(torch.float16)

print(f"\n原始 int64: {a.dtype}")
print(f"转 float32: {b.dtype}")
print(f"转 float64: {c.dtype}")
print(f"转 float16: {d.dtype}")
```

**运行结果：**
```
float32: torch.float32
float64: torch.float64
int32:   torch.int32
int64:   torch.int64
bool:    torch.bool

原始 int64: torch.int64
转 float32: torch.float32
转 float64: torch.float64
转 float16: torch.float16
```

!!! tip "数据类型选择建议"
    - 深度学习模型训练默认使用 `float32`
    - 推理部署可使用 `float16` 加速（需要 GPU 支持）
    - 标签和索引使用 `int64`（`torch.long`）
    - 大规模数据可考虑 `float16` 或 `bfloat16` 节省显存

---

## 1.5 张量运算

### 基本算术运算

```python
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])

# 逐元素运算
print(f"加法 a + b:   {a + b}")
print(f"减法 a - b:   {a - b}")
print(f"乘法 a * b:   {a * b}")
print(f"除法 a / b:   {a / b}")
print(f"幂运算 a ** 2: {a ** 2}")
print(f"平方根:       {torch.sqrt(a)}")
print(f"指数:         {torch.exp(a)}")
print(f"对数:         {torch.log(a)}")
```

**运行结果：**
```
加法 a + b:   tensor([5., 7., 9.])
减法 a - b:   tensor([-3., -3., -3.])
乘法 a * b:   tensor([ 4., 10., 18.])
除法 a / b:   tensor([0.2500, 0.4000, 0.5000])
幂运算 a ** 2: tensor([1., 4., 9.])
平方根:       tensor([1.0000, 1.4142, 1.7321])
指数:         tensor([ 2.7183,  7.3891, 20.0855])
对数:         tensor([0.0000, 0.6931, 1.0986])
```

### 矩阵运算

```python
A = torch.tensor([[1, 2], [3, 4]])
B = torch.tensor([[5, 6], [7, 8]])

# 矩阵乘法（三种等价写法）
matmul1 = A @ B
matmul2 = torch.matmul(A, B)
matmul3 = torch.mm(A, B)

print(f"矩阵乘法 A @ B:\n{matmul1}")

# 转置
print(f"\nA 的转置:\n{A.T}")

# 逆矩阵
A_inv = torch.inverse(A.float())
print(f"\nA 的逆矩阵:\n{A_inv}")

# 验证：A @ A_inv = I
print(f"\n验证 A @ A_inv:\n{A.float() @ A_inv}")
```

**运行结果：**
```
矩阵乘法 A @ B:
tensor([[19, 22],
        [43, 50]])

A 的转置:
tensor([[1, 3],
        [2, 4]])

A 的逆矩阵:
tensor([[-2.0000,  1.0000],
        [ 1.5000, -0.5000]])

验证 A @ A_inv:
tensor([[1.0000, 0.0000],
        [0.0000, 1.0000]])
```

### 统计运算

```python
x = torch.tensor([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])

print(f"求和:              {x.sum()}")
print(f"平均值:            {x.mean()}")
print(f"最大值:            {x.max()}")
print(f"最小值:            {x.min()}")
print(f"标准差:            {x.std()}")

# 按维度操作
print(f"\n按行求和 (dim=0):  {x.sum(dim=0)}")
print(f"按列求和 (dim=1):  {x.sum(dim=1)}")
print(f"按行求最大值:      {x.max(dim=0)}")
print(f"按列求最大值:      {x.max(dim=1)}")

# argmax：最大值的位置
print(f"\n每列最大值位置:    {x.argmax(dim=0)}")
print(f"每行最大值位置:    {x.argmax(dim=1)}")
```

**运行结果：**
```
求和:              21.0
平均值:            3.5
最大值:            6.0
最小值:            1.0
标准差:            1.8708

按行求和 (dim=0):  tensor([5., 7., 9.])
按列求和 (dim=1):  tensor([ 6., 15.])
按行求最大值:      torch.return_types.max(values=tensor([4., 5., 6.]), indices=tensor([1, 1, 1]))
按列求最大值:      torch.return_types.max(values=tensor([3., 6.]), indices=tensor([2, 2]))

每列最大值位置:    tensor([1, 1, 1])
每行最大值位置:    tensor([2, 2])
```

---

## 1.6 索引与切片

```python
tensor = torch.arange(1, 13).reshape(3, 4)
print(f"原始张量:\n{tensor}\n")

# 基本索引
print(f"第 0 行:        {tensor[0]}")
print(f"第 0 行第 2 列: {tensor[0, 2]}")
print(f"前两行:        \n{tensor[:2]}")
print(f"第 1 到 2 行:  \n{tensor[1:3]}")
print(f"所有行的第 1 列: {tensor[:, 1]}")
print(f"前两行的后两列: \n{tensor[:2, -2:]}")

# 花式索引
indices = torch.tensor([0, 2])
print(f"\n选择第 0 和第 2 行:\n{tensor[indices]}")

# 布尔索引
mask = tensor > 6
print(f"\n大于 6 的元素: {tensor[mask]}")
```

**运行结果：**
```
原始张量:
tensor([[ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12]])

第 0 行:        tensor([1, 2, 3, 4])
第 0 行第 2 列: 3
前两行:        
tensor([[1, 2, 3, 4],
        [5, 6, 7, 8]])
第 1 到 2 行:  
tensor([[ 5,  6,  7,  8],
        [ 9, 10, 11, 12]])
所有行的第 1 列: tensor([ 2,  6, 10])
前两行的后两列: 
tensor([[3, 4],
        [7, 8]])

选择第 0 和第 2 行:
tensor([[ 1,  2,  3,  4],
        [ 9, 10, 11, 12]])

大于 6 的元素: tensor([ 7,  8,  9, 10, 11, 12])
```

---

## 1.7 形状操作

```python
x = torch.arange(12)
print(f"原始: {x}")

# reshape：改变形状（不改变数据）
reshaped = x.reshape(3, 4)
print(f"\nreshape(3, 4):\n{reshaped}")

# view：与 reshape 类似，但要求内存连续
viewed = x.view(4, 3)
print(f"\nview(4, 3):\n{viewed}")

# 使用 -1 自动推断维度
auto = x.reshape(2, -1)
print(f"\nreshape(2, -1):\n{auto}")

# squeeze：移除大小为 1 的维度
y = torch.randn(1, 3, 1, 4)
print(f"\n原始形状: {y.shape}")
print(f"squeeze 后: {y.squeeze().shape}")
print(f"squeeze(dim=0) 后: {y.squeeze(0).shape}")

# unsqueeze：添加大小为 1 的维度
z = torch.tensor([1, 2, 3])
print(f"\n原始形状: {z.shape}")
print(f"unsqueeze(0) 后: {z.unsqueeze(0).shape}")
print(f"unsqueeze(1) 后: {z.unsqueeze(1).shape}")

# 拼接
a = torch.tensor([[1, 2], [3, 4]])
b = torch.tensor([[5, 6], [7, 8]])
cat_dim0 = torch.cat([a, b], dim=0)
cat_dim1 = torch.cat([a, b], dim=1)
print(f"\n按行拼接 (dim=0):\n{cat_dim0}")
print(f"\n按列拼接 (dim=1):\n{cat_dim1}")

# 堆叠（创建新维度）
stacked = torch.stack([a, b], dim=0)
print(f"\n堆叠 (dim=0), 形状 {stacked.shape}:\n{stacked}")
```

**运行结果：**
```
原始: tensor([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])

reshape(3, 4):
tensor([[ 0,  1,  2,  3],
        [ 4,  5,  6,  7],
        [ 8,  9, 10, 11]])

view(4, 3):
tensor([[ 0,  1,  2],
        [ 3,  4,  5],
        [ 6,  7,  8],
        [ 9, 10, 11]])

reshape(2, -1):
tensor([[ 0,  1,  2,  3,  4,  5],
        [ 6,  7,  8,  9, 10, 11]])

原始形状: torch.Size([1, 3, 1, 4])
squeeze 后: torch.Size([3, 4])
squeeze(dim=0) 后: torch.Size([3, 1, 4])

原始形状: torch.Size([3])
unsqueeze(0) 后: torch.Size([1, 3])
unsqueeze(1) 后: torch.Size([3, 1])

按行拼接 (dim=0):
tensor([[1, 2],
        [3, 4],
        [5, 6],
        [7, 8]])

按列拼接 (dim=1):
tensor([[1, 2, 5, 6],
        [3, 4, 7, 8]])

堆叠 (dim=0), 形状 torch.Size([2, 2, 2]):
tensor([[[1, 2],
         [3, 4]],

        [[5, 6],
         [7, 8]]])
```

---

## 1.8 设备管理（CPU / GPU）

```python
# 检查 GPU 是否可用
print(f"CUDA 是否可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU 数量: {torch.cuda.device_count()}")
    print(f"当前 GPU: {torch.cuda.get_device_name(0)}")

# 创建张量并指定设备
cpu_tensor = torch.tensor([1, 2, 3])
print(f"\nCPU 张量: {cpu_tensor.device}")

if torch.cuda.is_available():
    # 移动到 GPU
    gpu_tensor = cpu_tensor.to('cuda')
    print(f"GPU 张量: {gpu_tensor.device}")
    
    # 移回 CPU
    back_to_cpu = gpu_tensor.to('cpu')
    print(f"移回 CPU: {back_to_cpu.device}")
    
    # 直接在 GPU 上创建
    gpu_direct = torch.tensor([4, 5, 6], device='cuda')
    print(f"直接在 GPU 创建: {gpu_direct.device}")
```

**运行结果（有 GPU 时）：**
```
CUDA 是否可用: True
GPU 数量: 1
当前 GPU: NVIDIA GeForce RTX 3060

CPU 张量: cpu
GPU 张量: cuda:0
移回 CPU: cpu
直接在 GPU 创建: cuda:0
```

!!! note "设备管理最佳实践"
    定义设备变量，让代码在 CPU 和 GPU 环境下都能运行：
    ```python
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor = torch.randn(3, 4).to(device)
    ```

---

## 1.9 原地操作

以 `_` 结尾的方法会 **原地修改** 张量，不创建新副本：

```python
x = torch.tensor([1.0, 2.0, 3.0])
print(f"原始: {x}")

# 原地加法
x.add_(1)
print(f"add_(1) 后: {x}")

# 原地乘法
x.mul_(2)
print(f"mul_(2) 后: {x}")

# 原地填充
x.zero_()
print(f"zero_() 后: {x}")
```

**运行结果：**
```
原始: tensor([1., 2., 3.])
add_(1) 后: tensor([2., 3., 4.])
mul_(2) 后: tensor([4., 6., 8.])
zero_() 后: tensor([0., 0., 0.])
```

!!! warning "原地操作的注意事项"
    - 原地操作节省内存，但可能破坏自动求导的计算图
    - 在需要梯度的张量上使用原地操作需格外小心
    - 一般建议优先使用非原地操作，仅在性能关键处使用原地操作

---

## 要点总结

- [x] 张量是 PyTorch 的核心数据结构，类似 NumPy 的 ndarray
- [x] 可通过列表、NumPy 数组、内置函数等多种方式创建张量
- [x] 张量支持丰富的数学运算：算术、矩阵、统计
- [x] 索引和切片语法与 NumPy 高度一致
- [x] `reshape`、`view`、`squeeze`、`unsqueeze` 用于改变张量形状
- [x] `cat` 和 `stack` 用于拼接和堆叠张量
- [x] `.to(device)` 可在 CPU 和 GPU 之间移动张量
- [x] 以 `_` 结尾的方法执行原地操作

---

## 课后练习

1.  **创建练习**：分别用 `torch.zeros`、`torch.ones`、`torch.rand`、`torch.randn` 创建一个形状为 `(4, 5)` 的张量，观察它们的值分布。

2.  **运算练习**：创建两个 $3 \times 3$ 的随机矩阵 $A$ 和 $B$，计算 $A + B$、$A \times B$（逐元素）、$A @ B$（矩阵乘法）、$A^T$（转置）。

3.  **索引练习**：创建一个形状为 `(5, 6)` 的张量，提取第 1、3、5 行和第 2、4 列的交集。

4.  **形状练习**：创建一个包含 24 个元素的张量，尝试用 `reshape` 将其变为 `(2, 3, 4)`、`(4, 6)`、`(2, -1)` 等形状。

---

[返回目录](index.md) | [下一章：自动求导机制 →](02-autograd.md)