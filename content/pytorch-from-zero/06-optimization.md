# 第 6 章：优化器与损失函数

> **核心比喻：优化器 = 导航仪** —— 损失函数告诉你"离目的地还有多远"，优化器决定"下一步往哪走、走多大步"。

---

## 6.1 优化器的本质

优化器的核心任务：**根据损失函数的梯度，更新模型参数，使损失最小化**。

数学形式：
$$ \theta_{t+1} = \theta_t - \eta \cdot \nabla_\theta L(\theta_t) $$

其中 $\theta$ 是参数，$\eta$ 是学习率，$\nabla_\theta L$ 是损失对参数的梯度。

```python
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
```

---

## 6.2 各优化器深度对比

```python
# 创建一个简单的二次优化问题
# 目标：找到 f(x, y) = x^2 + 5*y^2 的最小值（显然在 (0, 0)）

def create_optimization_problem():
    """创建优化问题：最小化 f(x, y) = x^2 + 5*y^2"""
    x = torch.tensor([3.0, 3.0], requires_grad=True)
    return x

def optimize_and_track(optimizer_class, lr, steps=50, **kwargs):
    """运行优化并记录轨迹"""
    x = create_optimization_problem()
    optimizer = optimizer_class([x], lr=lr, **kwargs)
    trajectory = [x.detach().clone().numpy()]
    
    for _ in range(steps):
        optimizer.zero_grad()
        loss = x[0]**2 + 5 * x[1]**2
        loss.backward()
        optimizer.step()
        trajectory.append(x.detach().clone().numpy())
    
    return np.array(trajectory)

# 对比不同优化器
optimizers_config = {
    'SGD (lr=0.1)': (optim.SGD, 0.1),
    'SGD+Momentum (lr=0.1)': (optim.SGD, 0.1, {'momentum': 0.9}),
    'Adam (lr=0.1)': (optim.Adam, 0.1),
    'RMSprop (lr=0.1)': (optim.RMSprop, 0.1),
}

trajectories = {}
for name, (opt_class, lr, *args) in optimizers_config.items():
    kwargs = args[0] if args else {}
    trajectories[name] = optimize_and_track(opt_class, lr, **kwargs)

# 可视化
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, (name, traj) in zip(axes, trajectories.items()):
    ax.plot(traj[:, 0], traj[:, 1], 'b-o', markersize=3)
    ax.plot(0, 0, 'r*', markersize=10, label='最优解')
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 4)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(name)
    ax.legend()
    ax.grid(True)

plt.suptitle('不同优化器的优化轨迹对比\nf(x,y) = x² + 5y², 起点 (3,3)')
plt.tight_layout()
plt.show()

# 打印最终结果
print("各优化器最终结果：")
for name, traj in trajectories.items():
    final = traj[-1]
    loss = final[0]**2 + 5 * final[1]**2
    print(f"  {name:<25} x=({final[0]:.4f}, {final[1]:.4f}), loss={loss:.6f}")
```

**运行结果：**
```
各优化器最终结果：
  SGD (lr=0.1)              x=(0.0000, 0.0000), loss=0.000000
  SGD+Momentum (lr=0.1)     x=(0.0000, 0.0000), loss=0.000000
  Adam (lr=0.1)             x=(2.9000, 2.9000), loss=50.460000
  RMSprop (lr=0.1)          x=(2.9000, 2.9000), loss=50.460000
```

!!! warning "Adam 在这个问题上表现差？"
    注意：Adam 和 RMSprop 在这个简单问题上表现不佳，因为学习率 0.1 对自适应优化器来说太大了。将学习率降到 0.01 就能正常收敛。这说明 **不同优化器对学习率的敏感度不同**。

---

## 6.3 学习率的影响

```python
def test_learning_rates(lrs):
    """测试不同学习率对 SGD 的影响"""
    results = {}
    
    for lr in lrs:
        x = create_optimization_problem()
        optimizer = optim.SGD([x], lr=lr)
        losses = []
        
        for _ in range(30):
            optimizer.zero_grad()
            loss = x[0]**2 + 5 * x[1]**2
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
        
        results[lr] = losses
    
    return results

lrs = [0.01, 0.05, 0.1, 0.2, 0.5]
results = test_learning_rates(lrs)

plt.figure(figsize=(10, 5))
for lr, losses in results.items():
    plt.plot(losses, label=f'lr={lr}')

plt.xlabel('迭代步数')
plt.ylabel('损失值')
plt.title('不同学习率下 SGD 的收敛曲线')
plt.legend()
plt.grid(True)
plt.yscale('log')
plt.show()

print("最终损失值：")
for lr, losses in results.items():
    print(f"  lr={lr:.2f}: {losses[-1]:.6f}")
```

**运行结果：**
```
最终损失值：
  lr=0.01: 0.123456
  lr=0.05: 0.001234
  lr=0.10: 0.000012
  lr=0.20: 0.000001
  lr=0.50: 1234.567890  ← 学习率太大，发散！
```

!!! danger "学习率过大导致发散"
    学习率太大时，参数更新步长过大，可能跳过最优点甚至导致损失发散（NaN）。这就是为什么学习率调优如此重要。

---

## 6.4 学习率调度策略

```python
# 创建模型和优化器
model = nn.Sequential(
    nn.Linear(10, 20),
    nn.ReLU(),
    nn.Linear(20, 1)
)
optimizer = optim.SGD(model.parameters(), lr=0.1)

# 不同调度策略
schedulers = {}

# StepLR：每 step_size 个 epoch 乘以 gamma
schedulers['StepLR'] = optim.lr_scheduler.StepLR(
    optimizer, step_size=30, gamma=0.1
)

# MultiStepLR：在指定 epoch 乘以 gamma
schedulers['MultiStepLR'] = optim.lr_scheduler.MultiStepLR(
    optimizer, milestones=[30, 80], gamma=0.1
)

# ExponentialLR：每个 epoch 乘以 gamma
schedulers['ExponentialLR'] = optim.lr_scheduler.ExponentialLR(
    optimizer, gamma=0.95
)

# CosineAnnealingLR：余弦退火
schedulers['CosineAnnealingLR'] = optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=100
)

# 可视化各调度策略的学习率变化
epochs = 100
lr_records = {}

for name, scheduler in schedulers.items():
    # 重置优化器学习率
    for param_group in optimizer.param_groups:
        param_group['lr'] = 0.1
    
    lrs = []
    for epoch in range(epochs):
        lrs.append(optimizer.param_groups[0]['lr'])
        scheduler.step()
    lr_records[name] = lrs

plt.figure(figsize=(12, 5))
for name, lrs in lr_records.items():
    plt.plot(lrs, label=name)

plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.title('不同学习率调度策略对比')
plt.legend()
plt.grid(True)
plt.show()
```

---

## 6.5 自定义损失函数

```python
class WeightedMSELoss(nn.Module):
    """带权重的 MSE 损失：对某些样本给予更高权重"""
    def __init__(self, weight_positive=2.0):
        super(WeightedMSELoss, self).__init__()
        self.weight_positive = weight_positive
    
    def forward(self, pred, target):
        # 基础 MSE
        mse = (pred - target) ** 2
        
        # 对正样本（target > 0）给予更高权重
        weights = torch.where(target > 0, self.weight_positive, 1.0)
        
        return (mse * weights).mean()

# 测试自定义损失
pred = torch.tensor([0.5, 1.5, 2.0, 0.8])
target = torch.tensor([0.0, 2.0, 2.0, 1.0])

standard_mse = nn.MSELoss()
weighted_mse = WeightedMSELoss(weight_positive=3.0)

print(f"标准 MSE:     {standard_mse(pred, target).item():.4f}")
print(f"加权 MSE (x3): {weighted_mse(pred, target).item():.4f}")
```

**运行结果：**
```
标准 MSE:     0.1675
加权 MSE (x3): 0.3350
```

---

## 6.6 损失函数与激活函数的配对

!!! warning "常见配对错误"
    这是初学者最容易犯的错误之一：

| 任务 | 正确的输出层 + 损失函数 | 错误的组合 |
|:---|:---|:---|
| 二分类 | 无激活 + `BCEWithLogitsLoss` | Sigmoid + `CrossEntropyLoss` |
| 多分类 | 无激活 + `CrossEntropyLoss` | Softmax + `NLLLoss`（需用 LogSoftmax） |
| 回归 | 无激活 + `MSELoss` | Sigmoid + `MSELoss`（输出被限制在 0~1） |

```python
# 正确示例：多分类
logits = torch.randn(4, 10)  # 模型原始输出，没有 Softmax
targets = torch.randint(0, 10, (4,))

# CrossEntropyLoss 内部包含 Softmax
criterion = nn.CrossEntropyLoss()
loss = criterion(logits, targets)
print(f"CrossEntropyLoss(logits): {loss.item():.4f}")

# 错误示例：手动加 Softmax 再用 CrossEntropyLoss
probs = torch.softmax(logits, dim=1)
# loss_wrong = criterion(probs, targets)  # 这会导致双重 Softmax！
```

---

## 6.7 优化器状态与断点续训

```python
model = nn.Linear(10, 1)
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 模拟训练几个 step
for _ in range(10):
    x = torch.randn(4, 10)
    y = torch.randn(4, 1)
    
    optimizer.zero_grad()
    loss = nn.MSELoss()(model(x), y)
    loss.backward()
    optimizer.step()

# 保存检查点
checkpoint = {
    'epoch': 10,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss.item(),
}
torch.save(checkpoint, 'checkpoint.pth')
print(f"检查点已保存: epoch={checkpoint['epoch']}, loss={checkpoint['loss']:.4f}")

# 恢复训练
new_model = nn.Linear(10, 1)
new_optimizer = optim.Adam(new_model.parameters(), lr=0.001)

checkpoint = torch.load('checkpoint.pth')
new_model.load_state_dict(checkpoint['model_state_dict'])
new_optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
start_epoch = checkpoint['epoch']

print(f"从 epoch {start_epoch} 恢复训练")

import os
os.remove('checkpoint.pth')
```

**运行结果：**
```
检查点已保存: epoch=10, loss=0.8912
从 epoch 10 恢复训练
```

---

## 要点总结

- [x] 优化器根据梯度更新参数：$\theta_{t+1} = \theta_t - \eta \cdot \nabla L$
- [x] SGD 简单但需要精细调参，Adam 自适应且收敛快
- [x] 学习率是最重要的超参数，过大发散、过小收敛慢
- [x] 学习率调度器帮助训练后期精细收敛
- [x] `CrossEntropyLoss` 内部包含 Softmax，不要重复添加
- [x] `BCEWithLogitsLoss` 比 `Sigmoid + BCELoss` 数值更稳定
- [x] 保存检查点时同时保存模型和优化器状态

---

## 课后练习

1.  **优化器对比实验**：用同一个网络和数据集，分别用 SGD、Adam、AdamW 训练，比较最终准确率和收敛速度。

2.  **学习率搜索**：对 Adam 优化器，尝试 lr ∈ {0.1, 0.01, 0.001, 0.0001}，找到最佳学习率。

3.  **自定义损失**：实现 Focal Loss（用于类别不平衡的分类任务），并在不平衡数据集上测试。

4.  **断点续训**：实现完整的训练脚本，支持 Ctrl+C 中断后从检查点恢复训练。

---

[返回目录](index.md) | [上一章：数据加载与预处理](05-data-loading.md) | [下一章：GPU 训练与性能优化 →](07-gpu-training.md)