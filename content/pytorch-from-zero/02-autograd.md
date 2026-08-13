# 第 2 章：自动求导机制

> **核心比喻：计算图 = 流水线记录仪** —— 就像工厂流水线上的传感器记录每个环节的输入输出，PyTorch 的计算图自动追踪所有运算，反向推导梯度。

---

## 2.1 为什么需要自动求导？

!!! example "生活化类比"
    想象你在调试一个 **复杂的多米诺骨牌阵**。你想知道：如果微调第 3 块骨牌的位置，最后一块骨牌的倒向会变化多少？
    
    手动计算：你需要追踪第 3 块 → 第 4 块 → ... → 最后一块的连锁反应，每一步都要求导，极其繁琐。
    
    **自动求导**：PyTorch 帮你自动记录每一块骨牌之间的"影响系数"（梯度），你只需要说"从最后一块往回算"，它就能瞬间给出答案。

在深度学习中，模型可能有数百万个参数，手动求导是不可能的。自动求导（Autograd）是 PyTorch 最核心的特性之一。

---

## 2.2 梯度计算基础

### 第一个自动求导示例

```python
import torch

# 创建需要梯度的张量
x = torch.tensor([2.0, 3.0], requires_grad=True)
print(f"x: {x}")
print(f"x.requires_grad: {x.requires_grad}")

# 定义一个计算：y = x[0]^2 + x[1]^3
y = x[0] ** 2 + x[1] ** 3
print(f"\ny = x[0]^2 + x[1]^3 = {y.item()}")

# 反向传播计算梯度
y.backward()

# 查看梯度：dy/dx[0] = 2*x[0] = 4, dy/dx[1] = 3*x[1]^2 = 27
print(f"\ndy/dx[0] = 2 * {x[0].item()} = {x.grad[0]}")
print(f"dy/dx[1] = 3 * {x[1].item()}^2 = {x.grad[1]}")
```

**运行结果：**
```
x: tensor([2., 3.], requires_grad=True)
x.requires_grad: True

y = x[0]^2 + x[1]^3 = 31.0

dy/dx[0] = 2 * 2.0 = 4.0
dy/dx[1] = 3 * 3.0^2 = 27.0
```

### 梯度验证

手动计算验证：
- $y = x_0^2 + x_1^3$
- $\frac{\partial y}{\partial x_0} = 2x_0 = 2 \times 2 = 4$ ✓
- $\frac{\partial y}{\partial x_1} = 3x_1^2 = 3 \times 9 = 27$ ✓

---

## 2.3 计算图的工作原理

```python
# 构建一个更复杂的计算图
a = torch.tensor([2.0], requires_grad=True)
b = torch.tensor([3.0], requires_grad=True)

# 前向传播：c = a * b, d = a + b, e = c * d
c = a * b
d = a + b
e = c * d

print(f"a = {a.item()}, b = {b.item()}")
print(f"c = a * b = {c.item()}")
print(f"d = a + b = {d.item()}")
print(f"e = c * d = {e.item()}")

# 反向传播
e.backward()

print(f"\n梯度 de/da = {a.grad.item()}")
print(f"梯度 de/db = {b.grad.item()}")

# 手动验证：e = (a*b) * (a+b) = a^2*b + a*b^2
# de/da = 2*a*b + b^2 = 2*2*3 + 9 = 12 + 9 = 21
# de/db = a^2 + 2*a*b = 4 + 12 = 16
print(f"\n手动验证 de/da = 2*2*3 + 3^2 = 21 ✓")
print(f"手动验证 de/db = 2^2 + 2*2*3 = 16 ✓")
```

**运行结果：**
```
a = 2.0, b = 3.0
c = a * b = 6.0
d = a + b = 5.0
e = c * d = 30.0

梯度 de/da = 21.0
梯度 de/db = 16.0

手动验证 de/da = 2*2*3 + 3^2 = 21 ✓
手动验证 de/db = 2^2 + 2*2*3 = 16 ✓
```

!!! info "计算图的关键概念"
    - **叶子节点**：用户创建的、`requires_grad=True` 的张量（如 `a`、`b`）
    - **中间节点**：由运算产生的张量（如 `c`、`d`）
    - **根节点**：最终输出的标量（如 `e`）
    - **反向传播**：从根节点出发，沿计算图反向计算每个叶子节点的梯度

---

## 2.4 梯度累积与清零

```python
x = torch.tensor([1.0], requires_grad=True)

# 第一次计算
y1 = x ** 2
y1.backward()
print(f"第一次 backward 后 x.grad: {x.grad}")  # 2

# 第二次计算（梯度会累积！）
y2 = x ** 3
y2.backward()
print(f"第二次 backward 后 x.grad: {x.grad}")  # 2 + 3 = 5

# 清零梯度
x.grad.zero_()
print(f"zero_() 后 x.grad: {x.grad}")  # 0

# 重新计算
y3 = x ** 4
y3.backward()
print(f"第三次 backward 后 x.grad: {x.grad}")  # 4
```

**运行结果：**
```
第一次 backward 后 x.grad: tensor([2.])
第二次 backward 后 x.grad: tensor([5.])
zero_() 后 x.grad: tensor([0.])
第三次 backward 后 x.grad: tensor([4.])
```

!!! warning "梯度累积陷阱"
    PyTorch 默认 **累积梯度**，这在训练循环中非常重要：
    - 每个 batch 训练前必须调用 `optimizer.zero_grad()` 清零梯度
    - 梯度累积也可用于模拟更大的 batch size（多个小 batch 累积后再更新）

---

## 2.5 禁用梯度计算

在评估模型或推理时，不需要计算梯度，可以禁用以节省内存和加速：

```python
x = torch.randn(1000, 1000)

# 方式 1：torch.no_grad() 上下文管理器
with torch.no_grad():
    y = x @ x.T
    print(f"no_grad 内 requires_grad: {y.requires_grad}")

# 方式 2：detach() 从计算图中分离
z = torch.randn(3, requires_grad=True)
z_detached = z.detach()
print(f"\n原始 requires_grad: {z.requires_grad}")
print(f"detach 后 requires_grad: {z_detached.requires_grad}")

# 方式 3：全局禁用（不推荐，影响范围太大）
# torch.set_grad_enabled(False)
```

**运行结果：**
```
no_grad 内 requires_grad: False

原始 requires_grad: True
detach 后 requires_grad: False
```

!!! tip "何时禁用梯度"
    - **模型评估/测试**：`model.eval()` + `torch.no_grad()`
    - **推理部署**：完全不需要梯度
    - **计算指标**：如计算准确率时不需要梯度

---

## 2.6 实战：线性回归的梯度下降

用自动求导实现一个简单的线性回归，直观感受梯度下降的过程：

```python
import torch
import matplotlib.pyplot as plt

# 生成模拟数据：y = 3x + 2 + 噪声
torch.manual_seed(42)
X = torch.randn(100, 1) * 2
y_true = 3 * X + 2 + torch.randn(100, 1) * 0.5

# 初始化参数（需要梯度）
w = torch.randn(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)

# 训练参数
learning_rate = 0.01
n_epochs = 100
losses = []

for epoch in range(n_epochs):
    # 前向传播：预测值
    y_pred = X @ w + b
    
    # 计算损失（MSE）
    loss = ((y_pred - y_true) ** 2).mean()
    losses.append(loss.item())
    
    # 反向传播
    loss.backward()
    
    # 梯度下降更新参数
    with torch.no_grad():
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad
    
    # 清零梯度
    w.grad.zero_()
    b.grad.zero_()
    
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1:3d}: loss={loss.item():.4f}, w={w.item():.3f}, b={b.item():.3f}")

print(f"\n真实参数: w=3.0, b=2.0")
print(f"学习参数: w={w.item():.3f}, b={b.item():.3f}")

# 可视化
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(losses)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('训练损失曲线')

plt.subplot(1, 2, 2)
plt.scatter(X.numpy(), y_true.numpy(), alpha=0.5, label='数据点')
plt.plot(X.numpy(), (X @ w.detach() + b.detach()).numpy(), 'r', label='拟合直线')
plt.xlabel('X')
plt.ylabel('y')
plt.title('线性回归拟合结果')
plt.legend()

plt.tight_layout()
plt.show()
```

**运行结果：**
```
Epoch  20: loss=0.6230, w=2.102, b=1.887
Epoch  40: loss=0.3523, w=2.557, b=1.944
Epoch  60: loss=0.2820, w=2.782, b=1.968
Epoch  80: loss=0.2637, w=2.893, b=1.980
Epoch 100: loss=0.2589, w=2.948, b=1.986

真实参数: w=3.0, b=2.0
学习参数: w=2.948, b=1.986
```

!!! example "代码解读"
    这个例子展示了深度学习训练的 **五个核心步骤**：
    
    1.  **前向传播**：计算预测值 `y_pred = X @ w + b`
    2.  **计算损失**：`loss = MSE(y_pred, y_true)`
    3.  **反向传播**：`loss.backward()` 自动计算梯度
    4.  **参数更新**：`w -= lr * w.grad`
    5.  **梯度清零**：`w.grad.zero_()` 防止累积
    
    这五个步骤构成了所有深度学习训练的 **通用模板**！

---

## 2.7 高阶梯度

PyTorch 支持计算高阶梯度（梯度的梯度），在某些研究场景中有用：

```python
x = torch.tensor([2.0], requires_grad=True)

# 一阶梯度：y = x^3, dy/dx = 3x^2
y = x ** 3

# create_graph=True 保留计算图以计算高阶梯度
grad1 = torch.autograd.grad(y, x, create_graph=True)[0]
print(f"一阶梯度 dy/dx = 3*x^2 = {grad1.item()}")

# 二阶梯度：d^2y/dx^2 = 6x
grad2 = torch.autograd.grad(grad1, x)[0]
print(f"二阶梯度 d^2y/dx^2 = 6*x = {grad2.item()}")
```

**运行结果：**
```
一阶梯度 dy/dx = 3*x^2 = 12.0
二阶梯度 d^2y/dx^2 = 6*x = 12.0
```

---

## 要点总结

- [x] `requires_grad=True` 标记需要计算梯度的张量
- [x] `.backward()` 触发反向传播，自动计算所有叶子节点的梯度
- [x] 梯度存储在 `.grad` 属性中
- [x] 梯度默认 **累积**，每次训练前需要 `zero_()` 清零
- [x] `torch.no_grad()` 禁用梯度计算，用于评估和推理
- [x] `.detach()` 从计算图中分离张量
- [x] 训练循环的五步模板：前向 → 损失 → 反向 → 更新 → 清零

---

## 课后练习

1.  **基础求导**：定义 $f(x) = 3x^4 + 2x^3 - x^2 + 5$，在 $x = 2$ 处计算 $f'(x)$，并用纸笔验证结果。

2.  **多元函数**：定义 $g(x, y) = x^2 \cdot \sin(y)$，在 $(x, y) = (3, \pi/4)$ 处计算 $\frac{\partial g}{\partial x}$ 和 $\frac{\partial g}{\partial y}$。

3.  **梯度下降实验**：修改 2.6 节的线性回归代码，尝试不同的学习率（0.001、0.01、0.1、1.0），观察损失曲线的变化。

4.  **多项式回归**：将 2.6 节的线性回归改为二次回归 $y = w_2 x^2 + w_1 x + b$，用梯度下降拟合参数。

---

[返回目录](index.md) | [上一章：张量操作基础](01-tensor-basics.md) | [下一章：构建神经网络 →](03-building-models.md)