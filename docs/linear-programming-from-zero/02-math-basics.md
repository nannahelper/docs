# 第 2 章：数学基础回顾 —— 搭建你的工具箱

> **场景：** 在开始正式学习线性规划之前，我们需要确认自己的"数学工具箱"里有足够的工具。本章将快速回顾线性代数和微积分中与线性规划最相关的概念，确保你带上正确的装备出发。

---

## 2.1 线性代数基础

### 向量与向量运算

向量是有方向和大小的量。在线性规划中，决策变量通常组织成向量：

$$\mathbf{x} = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{pmatrix}$$

```python
import numpy as np

x = np.array([2, 3, 1])
y = np.array([1, 1, 2])

print(f"x = {x}")
print(f"y = {y}")
print(f"x + y = {x + y}")       # 向量加法
print(f"3 * x = {3 * x}")       # 标量乘法
print(f"x · y = {np.dot(x, y)}") # 点积（内积）
```

**渲染效果：**
```
x = [2 3 1]
y = [1 1 2]
x + y = [3 4 3]
3 * x = [6 9 3]
x · y = 7
```

!!! tip "向量点积的几何意义"
    $\mathbf{x} \cdot \mathbf{y} = |\mathbf{x}| \cdot |\mathbf{y}| \cdot \cos\theta$
    
    当 $\cos\theta = 1$（同向）时，点积最大；
    当 $\cos\theta = -1$（反向）时，点积最小。

### 向量范数：向量的"长度"

向量范数是向量的"长度"的数学描述：

$$\|\mathbf{x}\|_2 = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2}$$

```python
x = np.array([3, 4])
norm_l2 = np.linalg.norm(x, ord=2)
print(f"向量 x = {x}")
print(f"L2 范数（欧几里得长度）: {norm_l2}")  # = 5.0
```

**渲染效果：**
```
向量 x = [3 4]
L2 范数（欧几里得长度）: 5.0
```

常见范数：

| 范数 | 公式 | 几何意义 |
|:---|:---|:---|
| L1 范数 | $\|\mathbf{x}\|_1 = \sum |x_i|$ | 曼哈顿距离 |
| L2 范数 | $\|\mathbf{x}\|_2 = \sqrt{\sum x_i^2}$ | 欧几里得距离 |
| L∞ 范数 | $\|\mathbf{x}\|_\infty = \max\|x_i\|$ | 最大分量 |

### 矩阵与矩阵运算

矩阵是线性规划中的核心工具。约束条件 $A\mathbf{x} \le \mathbf{b}$ 中的 $A$ 就是一个矩阵。

```python
A = np.array([[2, 1], [1, 2]])
b = np.array([10, 8])
x = np.array([2, 3])

print(f"矩阵 A:\n{A}")
print(f"向量 b: {b}")
print(f"向量 x: {x}")
print(f"Ax = {np.dot(A, x)}")  # 矩阵乘法
print(f"Ax ≤ b ? {np.dot(A, x) <= b}")  # 验证约束
```

**渲染效果：**
```
矩阵 A:
[[2 1]
 [1 2]]
向量 b: [10  8]
向量 x: [2 3]
Ax = [7 8]
Ax ≤ b ? [ True  True]
```

### 矩阵的秩与线性相关性

!!! info "秩（Rank）的直观理解"
    矩阵的秩 = 矩阵中"线性无关"的行（或列）的最大数量。
    
    直观上，秩告诉你：这个矩阵能"张开"多大的空间？

```python
A1 = np.array([[1, 2], [2, 4]])  # 两行成比例
A2 = np.array([[1, 2], [2, 3]])  # 两行线性无关

print(f"矩阵 A1（两行成比例）: rank = {np.linalg.matrix_rank(A1)}")
print(f"矩阵 A2（线性无关）: rank = {np.linalg.matrix_rank(A2)}")
```

**渲染效果：**
```
矩阵 A1（两行成比例）: rank = 1
矩阵 A2（线性无关）: rank = 2
```

### 特征值与正定性

对称矩阵的正定性决定了二次函数的"形状"：

```python
import numpy as np

A1 = np.array([[2, 1], [1, 2]])  # 正定矩阵
A2 = np.array([[1, 2], [2, 1]])  # 不正定

eigvals1 = np.linalg.eigvals(A1)
eigvals2 = np.linalg.eigvals(A2)

print(f"A1 特征值: {eigvals1}")  # 全为正 → 正定
print(f"A2 特征值: {eigvals2}")  # 有负 → 不正定
```

**渲染效果：**
```
A1 特征值: [3. 1.]
A2 特征值: [ 3. -1.]
```

---

## 2.2 微积分基础

### 多元函数与梯度

多元函数 $f(x_1, x_2, ..., x_n)$ 的梯度是一个向量，指向函数增长最快的方向：

$$\nabla f = \begin{pmatrix} \frac{\partial f}{\partial x_1} \\ \frac{\partial f}{\partial x_2} \\ \vdots \\ \frac{\partial f}{\partial x_n} \end{pmatrix}$$

```python
def gradient_example(x1, x2):
    """f(x1, x2) = x1^2 + x2^2 的梯度"""
    df_dx1 = 2 * x1
    df_dx2 = 2 * x2
    return np.array([df_dx1, df_dx2])

x = np.array([3.0, 4.0])
grad = gradient_example(x[0], x[1])
print(f"在点 ({x[0]}, {x[1]}) 处:")
print(f"  梯度 ∇f = {grad}")
print(f"  梯度方向: {grad / np.linalg.norm(grad)}")
print(f"  梯度范数: {np.linalg.norm(grad)}")
```

**渲染效果：**
```
在点 (3.0, 4.0) 处:
  梯度 ∇f = [6. 8.]
  梯度方向: [0.6 0.8]
  梯度范数: 10.0
```

!!! tip "梯度的几何直觉"
    梯度 $\nabla f(\mathbf{x})$ 指向函数 $f$ 在点 $\mathbf{x}$ 处增长最快的方向。
    
    这就是优化算法中"沿梯度方向上升，沿负梯度方向下降"的原因。

### 海森矩阵（Hessian Matrix）

海森矩阵是梯度的梯度，描述函数的曲率：

$$H = \begin{pmatrix} \frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} \\ \frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} \end{pmatrix}$$

对于 $f(x_1, x_2) = x_1^2 + x_2^2$：

$$H = \begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}$$

海森矩阵正定 → 函数是**严格凸**的 → 有唯一全局最小点。

### 泰勒定理

泰勒定理用多项式近似任意函数：

$$f(\mathbf{x} + \Delta \mathbf{x}) \approx f(\mathbf{x}) + \nabla f(\mathbf{x})^T \Delta \mathbf{x} + \frac{1}{2} \Delta \mathbf{x}^T H(\mathbf{x}) \Delta \mathbf{x}$$

这在线性规划的**灵敏度分析**中非常重要——它帮助我们理解参数变化对最优解的影响。

---

## 2.3 凸集与凸函数

### 凸集

!!! example "核心比喻：凸集 = 形状像碗的集合"
    如果一个集合内的任意两点连成的线段都在集合内，这个集合就是**凸集**。
    
    - 圆是凸集：圆内任意两点连线，整条线都在圆内
    - 月牙形不是凸集：两端在月牙上，线段中间可能出了月牙

**线性规划的可行域是凸集**——这是一个关键性质。

```python
# 验证可行域是凸集
def is_convex_set(points, A, b):
    """
    检验点集是否为凸集
    理论上：凸集中的任意两点连线仍在集合内
    """
    # 取两点中点
    mid = (points[0] + points[1]) / 2
    return np.all(np.dot(A, mid) <= b)

# 可行域：Ax <= b
A = np.array([[2, 1], [1, 2]])
b = np.array([10, 8])

# 任意两点
p1 = np.array([1, 1])
p2 = np.array([4, 2])
mid = (p1 + p2) / 2

print(f"p1 = {p1}, p2 = {p2}")
print(f"中点 = {mid}")
print(f"中点是否满足约束: {np.all(np.dot(A, mid) <= b)}")
```

**渲染效果：**
```
p1 = [1 1], p2 = [4 2]
中点 = [2.5 1.5]
中点是否满足约束: True
```

### 凸函数

**凸函数**的直观特征：函数的"上方"总是被线段支撑（想象一个碗的内部）。

$$\text{凸函数：} f(\lambda x_1 + (1-\lambda)x_2) \le \lambda f(x_1) + (1-\lambda)f(x_2)$$

!!! info "为什么凸性很重要？"
    对于凸优化问题（目标函数凸 + 可行域凸），**任何局部最优都是全局最优**。
    
    线性规划既是凸的（目标函数是线性的，可行域是凸的），又是非平凡的——这保证了单纯形法找到的解一定是全局最优。

---

## 2.4 线性规划的标准形式回顾

线性代数工具让我们能简洁地表达线性规划：

$$\min \quad \mathbf{c}^T \mathbf{x}$$

$$\text{s.t.} \quad A \mathbf{x} \le \mathbf{b}$$

其中：

- $\mathbf{c}$ 是目标函数系数向量（告诉你每个决策变量的"价值"）
- $A$ 是约束系数矩阵（告诉你每个决策变量消耗多少资源）
- $\mathbf{b}$ 是资源限制向量（告诉你每种资源有多少）
- $\mathbf{x}$ 是决策变量向量（你要决定的量）

---

## 要点总结

- [x] 向量范数 $\|\mathbf{x}\|_2 = \sqrt{\sum x_i^2}$ 是向量的"长度"
- [x] 矩阵乘法 $A\mathbf{x}$ 对应线性约束 $Ax \le b$
- [x] 梯度 $\nabla f$ 指向函数增长最快的方向
- [x] 凸集：任意两点连线仍在集合内
- [x] 线性规划的可行域是凸集，保证全局最优

---

## 课后练习

1. **计算练习**：已知 $\mathbf{x} = (1, 2, 3)$，求 $\|\mathbf{x}\|_1$、$\|\mathbf{x}\|_2$、$\|\mathbf{x}\|_\infty$。

2. **梯度练习**：求函数 $f(x_1, x_2) = 3x_1^2 + 2x_2^2 + 4x_1 x_2$ 的梯度和海森矩阵。

3. **判断练习**：以下集合哪些是凸集？
   - 圆盘 $\{(x,y): x^2 + y^2 \le 1\}$
   - 正方形 $\{(x,y): |x| \le 1, |y| \le 1\}$
   - L 形区域

---

**下一章预告：** 工具准备好了！第 3 章我们将学习如何把实际问题转化为线性规划模型——这是线性规划中最"艺术"的部分。

[继续第 3 章：线性规划数学模型 →](03-lp-model.md)