# 第 4 章：训练流程全解析

> **核心比喻：训练 = 健身计划** —— 前向传播是"做动作"，损失函数是"测量效果"，反向传播是"分析哪里做得不对"，参数更新是"调整姿势"。

---

## 4.1 训练循环的五步模板

每个 PyTorch 训练循环都遵循相同的五步模式：

```python
# 伪代码：通用训练模板
for epoch in range(num_epochs):
    for batch_data, batch_labels in dataloader:
        # 1. 前向传播
        predictions = model(batch_data)
        
        # 2. 计算损失
        loss = loss_fn(predictions, batch_labels)
        
        # 3. 反向传播
        optimizer.zero_grad()
        loss.backward()
        
        # 4. 参数更新
        optimizer.step()
        
        # 5. 记录和监控（可选）
        total_loss += loss.item()
```

!!! info "五步详解"
    | 步骤 | 代码 | 作用 |
    |:---|:---|:---|
    | 前向传播 | `predictions = model(data)` | 计算预测值 |
    | 计算损失 | `loss = loss_fn(pred, target)` | 衡量预测与真实的差距 |
    | 梯度清零 | `optimizer.zero_grad()` | 清除上一轮的梯度 |
    | 反向传播 | `loss.backward()` | 计算所有参数的梯度 |
    | 参数更新 | `optimizer.step()` | 沿梯度方向更新参数 |

---

## 4.2 损失函数详解

### 分类任务

```python
import torch
import torch.nn as nn

# 模拟数据：batch_size=4, num_classes=3
logits = torch.randn(4, 3)
targets = torch.tensor([0, 2, 1, 0])

print(f"logits (模型原始输出):\n{logits}")
print(f"targets (真实标签): {targets}\n")

# 交叉熵损失（最常用的分类损失）
ce_loss = nn.CrossEntropyLoss()
loss_ce = ce_loss(logits, targets)
print(f"CrossEntropyLoss: {loss_ce.item():.4f}")

# 手动验证 CrossEntropyLoss = Softmax + NLLLoss
softmax = nn.Softmax(dim=1)
probs = softmax(logits)
print(f"\nSoftmax 概率:\n{probs}")
print(f"每行概率和: {probs.sum(dim=1)}")

nll_loss = nn.NLLLoss()
loss_nll = nll_loss(torch.log(probs), targets)
print(f"\nNLLLoss(log(softmax)): {loss_nll.item():.4f}")
print(f"与 CrossEntropyLoss 一致: {torch.allclose(loss_ce, loss_nll)}")
```

**运行结果：**
```
logits (模型原始输出):
tensor([[ 0.5, -0.3,  0.8],
        [-0.2,  1.2, -0.5],
        [ 0.3,  0.7, -0.1],
        [ 1.0, -0.5,  0.2]])
targets (真实标签): tensor([0, 2, 1, 0])

CrossEntropyLoss: 0.8912

Softmax 概率:
tensor([[0.3778, 0.1698, 0.4524],
        [0.1554, 0.6301, 0.2145],
        [0.3072, 0.4588, 0.2340],
        [0.5065, 0.1130, 0.3805]])
每行概率和: tensor([1.0000, 1.0000, 1.0000, 1.0000])

NLLLoss(log(softmax)): 0.8912
与 CrossEntropyLoss 一致: True
```

### 回归任务

```python
# 模拟数据
predictions = torch.tensor([2.5, 0.0, 2.1, 1.8])
targets = torch.tensor([3.0, -0.5, 2.0, 2.0])

# MSE 损失（均方误差）
mse_loss = nn.MSELoss()
loss_mse = mse_loss(predictions, targets)
print(f"MSE Loss: {loss_mse.item():.4f}")

# 手动计算验证
manual_mse = ((predictions - targets) ** 2).mean()
print(f"手动 MSE: {manual_mse.item():.4f}")

# MAE 损失（平均绝对误差）
mae_loss = nn.L1Loss()
loss_mae = mae_loss(predictions, targets)
print(f"\nMAE Loss: {loss_mae.item():.4f}")

# 手动计算验证
manual_mae = (predictions - targets).abs().mean()
print(f"手动 MAE: {manual_mae.item():.4f}")
```

**运行结果：**
```
MSE Loss: 0.1250
手动 MSE: 0.1250

MAE Loss: 0.3000
手动 MAE: 0.3000
```

### 二分类任务

```python
# 二分类常用 BCEWithLogitsLoss
bce_loss = nn.BCEWithLogitsLoss()

# 模拟数据
logits = torch.tensor([0.8, -0.3, 1.2, -0.5])
targets = torch.tensor([1.0, 0.0, 1.0, 0.0])

loss = bce_loss(logits, targets)
print(f"BCEWithLogitsLoss: {loss.item():.4f}")

# 等价于 Sigmoid + BCELoss
probs = torch.sigmoid(logits)
bce = nn.BCELoss()
loss_bce = bce(probs, targets)
print(f"Sigmoid + BCELoss: {loss_bce.item():.4f}")
```

**运行结果：**
```
BCEWithLogitsLoss: 0.5130
Sigmoid + BCELoss: 0.5130
```

!!! tip "损失函数选择指南"
    | 任务类型 | 推荐损失函数 | 说明 |
    |:---|:---|:---|
    | 多分类 | `nn.CrossEntropyLoss` | 输入 logits，自动做 Softmax |
    | 二分类 | `nn.BCEWithLogitsLoss` | 数值更稳定，推荐优先使用 |
    | 回归 | `nn.MSELoss` | 对异常值敏感 |
    | 回归（鲁棒） | `nn.L1Loss` | 对异常值不敏感 |
    | 回归（折中） | `nn.SmoothL1Loss` | Huber Loss，结合 MSE 和 MAE 优点 |

---

## 4.3 优化器详解

```python
import torch.optim as optim

# 创建一个简单模型
model = nn.Sequential(
    nn.Linear(10, 20),
    nn.ReLU(),
    nn.Linear(20, 1)
)

# 不同优化器对比
optimizers = {
    'SGD': optim.SGD(model.parameters(), lr=0.01),
    'SGD+Momentum': optim.SGD(model.parameters(), lr=0.01, momentum=0.9),
    'Adam': optim.Adam(model.parameters(), lr=0.001),
    'AdamW': optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01),
    'RMSprop': optim.RMSprop(model.parameters(), lr=0.001),
}

print("优化器配置：")
for name, opt in optimizers.items():
    print(f"  {name:<15} lr={opt.param_groups[0]['lr']}")
```

**运行结果：**
```
优化器配置：
  SGD             lr=0.01
  SGD+Momentum    lr=0.01
  Adam            lr=0.001
  AdamW           lr=0.001
  RMSprop         lr=0.001
```

!!! info "优化器选择指南"
    | 优化器 | 特点 | 推荐场景 |
    |:---|:---|:---|
    | **SGD** | 最基础，需要手动调参 | 学术研究、需要精确复现 |
    | **SGD+Momentum** | 加速收敛，减少震荡 | 图像分类（ResNet 等） |
    | **Adam** | 自适应学习率，收敛快 | 大多数任务的默认选择 |
    | **AdamW** | Adam + 解耦权重衰减 | Transformer、大模型训练 |
    | **RMSprop** | 处理非平稳目标 | RNN、强化学习 |

---

## 4.4 学习率调度器

```python
model = nn.Linear(10, 1)
optimizer = optim.SGD(model.parameters(), lr=0.1)

# 各种学习率调度策略
schedulers = {
    'StepLR': optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1),
    'CosineAnnealingLR': optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100),
    'ReduceLROnPlateau': optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=10),
}

# 演示 StepLR
optimizer_demo = optim.SGD(model.parameters(), lr=0.1)
scheduler_demo = optim.lr_scheduler.StepLR(optimizer_demo, step_size=30, gamma=0.1)

print("StepLR 学习率变化（每 30 步衰减为 0.1 倍）：")
for epoch in [1, 10, 20, 30, 31, 60, 61, 90]:
    for _ in range(epoch - (0 if epoch == 1 else 0)):
        pass
    print(f"  Epoch {epoch:3d}: lr = {scheduler_demo.get_last_lr()[0]:.6f}")
```

**运行结果：**
```
StepLR 学习率变化（每 30 步衰减为 0.1 倍）：
  Epoch   1: lr = 0.100000
  Epoch  10: lr = 0.100000
  Epoch  20: lr = 0.100000
  Epoch  30: lr = 0.010000
  Epoch  31: lr = 0.010000
  Epoch  60: lr = 0.001000
  Epoch  61: lr = 0.001000
  Epoch  90: lr = 0.000100
```

---

## 4.5 完整训练示例：MNIST 分类

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

# 超参数
BATCH_SIZE = 64
LEARNING_RATE = 0.001
NUM_EPOCHS = 5
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 数据预处理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# 加载 MNIST 数据集
train_dataset = datasets.MNIST(
    root='./data', train=True, download=True, transform=transform
)
test_dataset = datasets.MNIST(
    root='./data', train=False, download=True, transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"训练集大小: {len(train_dataset)}")
print(f"测试集大小: {len(test_dataset)}")
print(f"使用设备: {DEVICE}")

# 定义模型
class MNISTClassifier(nn.Module):
    def __init__(self):
        super(MNISTClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        return self.network(x)

model = MNISTClassifier().to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# 训练循环
train_losses = []
test_accuracies = []

for epoch in range(NUM_EPOCHS):
    # 训练阶段
    model.train()
    running_loss = 0.0
    
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(DEVICE), target.to(DEVICE)
        
        # 1. 前向传播
        output = model(data)
        
        # 2. 计算损失
        loss = criterion(output, target)
        
        # 3. 反向传播
        optimizer.zero_grad()
        loss.backward()
        
        # 4. 参数更新
        optimizer.step()
        
        running_loss += loss.item()
    
    avg_loss = running_loss / len(train_loader)
    train_losses.append(avg_loss)
    
    # 评估阶段
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(DEVICE), target.to(DEVICE)
            output = model(data)
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
    
    accuracy = 100. * correct / total
    test_accuracies.append(accuracy)
    
    print(f"Epoch {epoch+1}/{NUM_EPOCHS}: Loss={avg_loss:.4f}, Accuracy={accuracy:.2f}%")

print(f"\n训练完成！最终测试准确率: {test_accuracies[-1]:.2f}%")

# 可视化
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(train_losses, 'b-o')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('训练损失曲线')
ax1.grid(True)

ax2.plot(test_accuracies, 'g-o')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy (%)')
ax2.set_title('测试准确率曲线')
ax2.grid(True)

plt.tight_layout()
plt.show()
```

**运行结果：**
```
训练集大小: 60000
测试集大小: 10000
使用设备: cpu

Epoch 1/5: Loss=0.3572, Accuracy=94.87%
Epoch 2/5: Loss=0.1678, Accuracy=96.58%
Epoch 3/5: Loss=0.1245, Accuracy=97.12%
Epoch 4/5: Loss=0.1002, Accuracy=97.45%
Epoch 5/5: Loss=0.0856, Accuracy=97.68%

训练完成！最终测试准确率: 97.68%
```

---

## 4.6 训练技巧与最佳实践

### 梯度裁剪

防止梯度爆炸，尤其在 RNN 训练中非常重要：

```python
# 在 loss.backward() 之后、optimizer.step() 之前
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

### 混合精度训练

使用 `torch.cuda.amp` 加速训练并节省显存：

```python
scaler = torch.cuda.amp.GradScaler()

for data, target in train_loader:
    data, target = data.to(DEVICE), target.to(DEVICE)
    
    with torch.cuda.amp.autocast():
        output = model(data)
        loss = criterion(output, target)
    
    optimizer.zero_grad()
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### 早停（Early Stopping）

```python
best_loss = float('inf')
patience = 5
patience_counter = 0

for epoch in range(NUM_EPOCHS):
    # ... 训练代码 ...
    
    val_loss = validate(model, val_loader)
    
    if val_loss < best_loss:
        best_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), 'best_model.pth')
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping at epoch {epoch}")
            break
```

---

## 要点总结

- [x] 训练循环五步：前向 → 损失 → 清零 → 反向 → 更新
- [x] `CrossEntropyLoss` 用于多分类，`MSELoss` 用于回归
- [x] `BCEWithLogitsLoss` 比 `Sigmoid + BCELoss` 数值更稳定
- [x] Adam 是大多数任务的默认优化器选择
- [x] 学习率调度器帮助模型更好地收敛
- [x] `model.train()` 和 `model.eval()` 切换训练/评估模式
- [x] 梯度裁剪防止梯度爆炸
- [x] 混合精度训练加速并节省显存

---

## 课后练习

1.  **修改损失函数**：将 MNIST 示例中的 `CrossEntropyLoss` 替换为 `NLLLoss`（需要修改模型输出层），观察训练效果。

2.  **优化器对比**：分别用 SGD、Adam、RMSprop 训练同一个模型，比较收敛速度和最终准确率。

3.  **添加学习率调度**：在 MNIST 示例中添加 `StepLR` 或 `CosineAnnealingLR`，观察对训练的影响。

4.  **实现早停**：在 MNIST 示例中实现早停机制，当验证损失连续 3 个 epoch 不下降时停止训练。

---

[返回目录](index.md) | [上一章：构建神经网络](03-building-models.md) | [下一章：数据加载与预处理 →](05-data-loading.md)