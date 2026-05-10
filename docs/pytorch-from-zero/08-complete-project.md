# 第 8 章：完整项目实战

> **核心比喻：项目 = 烹饪全流程** —— 从买菜（数据准备）到切菜（预处理）到烹饪（训练）到摆盘（评估可视化），每一步都有讲究。

---

## 8.1 项目概述

本章将带你完成一个 **完整的图像分类项目**：在 CIFAR-10 数据集上训练一个 CNN 分类器。

!!! info "项目目标"
    - 数据集：CIFAR-10（10 类彩色图像，50000 训练 + 10000 测试）
    - 模型：自定义 CNN（约 100 万参数）
    - 目标准确率：> 85%（测试集）
    - 技术栈：PyTorch + torchvision + matplotlib

---

## 8.2 完整项目代码

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import os

# ============================================================
# 1. 配置与超参数
# ============================================================
class Config:
    # 数据
    DATA_DIR = './data'
    NUM_CLASSES = 10
    IMG_SIZE = 32
    
    # 训练
    BATCH_SIZE = 128
    NUM_EPOCHS = 30
    LEARNING_RATE = 0.001
    WEIGHT_DECAY = 1e-4
    
    # 系统
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    NUM_WORKERS = 0  # Windows 设为 0
    SEED = 42
    
    # 路径
    SAVE_DIR = './checkpoints'
    BEST_MODEL_PATH = os.path.join(SAVE_DIR, 'best_model.pth')

torch.manual_seed(Config.SEED)
np.random.seed(Config.SEED)

print(f"使用设备: {Config.DEVICE}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# ============================================================
# 2. 数据准备
# ============================================================
# 训练集数据增强
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.4914, 0.4822, 0.4465],
        std=[0.2470, 0.2435, 0.2616]
    ),
])

# 测试集只做标准化
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.4914, 0.4822, 0.4465],
        std=[0.2470, 0.2435, 0.2616]
    ),
])

# 加载数据集
full_train_dataset = datasets.CIFAR10(
    root=Config.DATA_DIR, train=True, download=True, transform=train_transform
)
test_dataset = datasets.CIFAR10(
    root=Config.DATA_DIR, train=False, download=True, transform=test_transform
)

# 划分训练集和验证集（90% 训练，10% 验证）
train_size = int(0.9 * len(full_train_dataset))
val_size = len(full_train_dataset) - train_size
train_dataset, val_dataset = random_split(full_train_dataset, [train_size, val_size])

# 验证集使用测试集的 transform
val_dataset.dataset.transform = test_transform

# 创建 DataLoader
train_loader = DataLoader(
    train_dataset, batch_size=Config.BATCH_SIZE,
    shuffle=True, num_workers=Config.NUM_WORKERS, pin_memory=True
)
val_loader = DataLoader(
    val_dataset, batch_size=Config.BATCH_SIZE,
    shuffle=False, num_workers=Config.NUM_WORKERS, pin_memory=True
)
test_loader = DataLoader(
    test_dataset, batch_size=Config.BATCH_SIZE,
    shuffle=False, num_workers=Config.NUM_WORKERS, pin_memory=True
)

print(f"\n训练集: {len(train_dataset)} 样本")
print(f"验证集: {len(val_dataset)} 样本")
print(f"测试集: {len(test_dataset)} 样本")

# CIFAR-10 类别名称
CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']

# ============================================================
# 3. 模型定义
# ============================================================
class ResidualBlock(nn.Module):
    """残差块：解决深层网络退化问题"""
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        
        self.conv1 = nn.Conv2d(
            in_channels, out_channels, kernel_size=3,
            stride=stride, padding=1, bias=False
        )
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3,
            stride=1, padding=1, bias=False
        )
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # shortcut 连接（当维度不匹配时使用 1x1 卷积调整）
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1,
                         stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class CIFAR10Classifier(nn.Module):
    """基于残差块的 CNN 分类器"""
    def __init__(self, num_classes=10):
        super(CIFAR10Classifier, self).__init__()
        
        # 初始卷积层
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        
        # 残差层
        self.layer1 = self._make_layer(64, 64, num_blocks=2, stride=1)
        self.layer2 = self._make_layer(64, 128, num_blocks=2, stride=2)
        self.layer3 = self._make_layer(128, 256, num_blocks=2, stride=2)
        
        # 分类头
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(256, num_classes)
        
        # 初始化
        self._initialize_weights()
    
    def _make_layer(self, in_channels, out_channels, num_blocks, stride):
        layers = []
        layers.append(ResidualBlock(in_channels, out_channels, stride))
        for _ in range(1, num_blocks):
            layers.append(ResidualBlock(out_channels, out_channels, 1))
        return nn.Sequential(*layers)
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

model = CIFAR10Classifier(num_classes=Config.NUM_CLASSES).to(Config.DEVICE)

# 统计参数量
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\n模型参数量: {total_params:,} (可训练: {trainable_params:,})")

# ============================================================
# 4. 训练配置
# ============================================================
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(
    model.parameters(),
    lr=Config.LEARNING_RATE,
    weight_decay=Config.WEIGHT_DECAY
)

# 学习率调度：余弦退火
scheduler = optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=Config.NUM_EPOCHS
)

# 创建保存目录
os.makedirs(Config.SAVE_DIR, exist_ok=True)

# ============================================================
# 5. 训练与评估函数
# ============================================================
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc='Training', leave=False)
    for data, target in pbar:
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        
        # 梯度裁剪
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()
        
        pbar.set_postfix({
            'loss': f'{loss.item():.3f}',
            'acc': f'{100.*correct/total:.1f}%'
        })
    
    return running_loss / len(loader), 100. * correct / total

@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for data, target in loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        loss = criterion(output, target)
        
        running_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()
    
    return running_loss / len(loader), 100. * correct / total

# ============================================================
# 6. 训练循环
# ============================================================
print("\n" + "="*60)
print("开始训练")
print("="*60)

history = {
    'train_loss': [], 'train_acc': [],
    'val_loss': [], 'val_acc': [],
    'lr': []
}

best_val_acc = 0.0

for epoch in range(Config.NUM_EPOCHS):
    current_lr = optimizer.param_groups[0]['lr']
    
    # 训练
    train_loss, train_acc = train_epoch(
        model, train_loader, criterion, optimizer, Config.DEVICE
    )
    
    # 验证
    val_loss, val_acc = evaluate(
        model, val_loader, criterion, Config.DEVICE
    )
    
    # 学习率调度
    scheduler.step()
    
    # 记录历史
    history['train_loss'].append(train_loss)
    history['train_acc'].append(train_acc)
    history['val_loss'].append(val_loss)
    history['val_acc'].append(val_acc)
    history['lr'].append(current_lr)
    
    # 保存最佳模型
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'val_acc': val_acc,
        }, Config.BEST_MODEL_PATH)
        save_marker = ' *'
    else:
        save_marker = ''
    
    print(f"Epoch {epoch+1:2d}/{Config.NUM_EPOCHS} | "
          f"LR: {current_lr:.6f} | "
          f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | "
          f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%{save_marker}")

print(f"\n最佳验证准确率: {best_val_acc:.2f}%")

# ============================================================
# 7. 测试评估
# ============================================================
print("\n" + "="*60)
print("测试集评估")
print("="*60)

# 加载最佳模型
checkpoint = torch.load(Config.BEST_MODEL_PATH, map_location=Config.DEVICE)
model.load_state_dict(checkpoint['model_state_dict'])

test_loss, test_acc = evaluate(
    model, test_loader, criterion, Config.DEVICE
)
print(f"测试集 Loss: {test_loss:.4f}")
print(f"测试集 Accuracy: {test_acc:.2f}%")

# ============================================================
# 8. 结果可视化
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 损失曲线
axes[0, 0].plot(history['train_loss'], label='Train Loss', color='#2196F3')
axes[0, 0].plot(history['val_loss'], label='Val Loss', color='#FF9800')
axes[0, 0].set_xlabel('Epoch')
axes[0, 0].set_ylabel('Loss')
axes[0, 0].set_title('训练与验证损失曲线')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 准确率曲线
axes[0, 1].plot(history['train_acc'], label='Train Acc', color='#2196F3')
axes[0, 1].plot(history['val_acc'], label='Val Acc', color='#FF9800')
axes[0, 1].axhline(y=test_acc, color='#4CAF50', linestyle='--', label=f'Test Acc ({test_acc:.1f}%)')
axes[0, 1].set_xlabel('Epoch')
axes[0, 1].set_ylabel('Accuracy (%)')
axes[0, 1].set_title('训练与验证准确率曲线')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# 学习率曲线
axes[1, 0].plot(history['lr'], color='#9C27B0')
axes[1, 0].set_xlabel('Epoch')
axes[1, 0].set_ylabel('Learning Rate')
axes[1, 0].set_title('学习率变化（余弦退火）')
axes[1, 0].grid(True, alpha=0.3)

# 预测示例可视化
model.eval()
test_images, test_labels = next(iter(test_loader))
test_images = test_images[:16].to(Config.DEVICE)

with torch.no_grad():
    outputs = model(test_images)
    _, predicted = outputs.max(1)

# 反标准化
mean = torch.tensor([0.4914, 0.4822, 0.4465]).view(3, 1, 1)
std = torch.tensor([0.2470, 0.2435, 0.2616]).view(3, 1, 1)
test_images_denorm = test_images.cpu() * std + mean
test_images_denorm = test_images_denorm.clamp(0, 1)

for i in range(16):
    ax = axes[1, 1] if i == 0 else axes[1, 1]
    
axes[1, 1].axis('off')
axes[1, 1].set_title(f'测试集准确率: {test_acc:.1f}%')

plt.tight_layout()
plt.savefig('training_results.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"\n训练结果图已保存为 training_results.png")
print(f"最佳模型已保存至 {Config.BEST_MODEL_PATH}")
```

---

## 8.3 项目结构总结

```
cifar10_project/
├── data/                    # 数据集（自动下载）
├── checkpoints/             # 模型检查点
│   └── best_model.pth       # 最佳模型
├── train.py                 # 训练脚本（上面的完整代码）
├── inference.py             # 推理脚本
└── training_results.png     # 训练结果可视化
```

---

## 8.4 推理脚本

```python
# inference.py - 使用训练好的模型进行单张图像推理
import torch
from PIL import Image
from torchvision import transforms

def predict_image(image_path, model, device, classes):
    """对单张图像进行预测"""
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.4914, 0.4822, 0.4465],
            std=[0.2470, 0.2435, 0.2616]
        ),
    ])
    
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    model.eval()
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted = probabilities.max(1)
    
    return classes[predicted.item()], confidence.item()

# 使用示例
"""
model = CIFAR10Classifier().to(device)
checkpoint = torch.load('checkpoints/best_model.pth')
model.load_state_dict(checkpoint['model_state_dict'])

class_name, confidence = predict_image('cat.jpg', model, device, CLASSES)
print(f'预测类别: {class_name}, 置信度: {confidence:.2%}')
"""
print("推理脚本结构已展示")
```

---

## 8.5 项目要点回顾

!!! tip "项目中的最佳实践"
    1.  **配置集中管理**：使用 `Config` 类统一管理超参数
    2.  **数据增强**：训练集使用随机翻转、裁剪、颜色抖动
    3.  **残差连接**：使用 Residual Block 解决深层网络退化
    4.  **学习率调度**：余弦退火让训练后期更稳定
    5.  **梯度裁剪**：防止梯度爆炸
    6.  **模型保存**：保存最佳验证准确率的模型
    7.  **结果可视化**：损失曲线、准确率曲线、预测示例

---

## 要点总结

- [x] 完整的深度学习项目包含：数据 → 模型 → 训练 → 评估 → 可视化
- [x] 数据增强是提升泛化能力的最有效手段
- [x] 残差连接（Residual Block）让深层网络更容易训练
- [x] 余弦退火学习率调度比固定衰减更平滑
- [x] 始终保存验证集上表现最好的模型
- [x] 训练完成后在测试集上做最终评估
- [x] 可视化训练曲线帮助诊断过拟合/欠拟合

---

## 课后练习

1.  **模型改进**：尝试增加网络深度（更多 Residual Blocks），观察准确率变化。

2.  **数据增强实验**：移除数据增强（只用 ToTensor + Normalize），观察过拟合程度。

3.  **迁移学习**：使用 torchvision 的预训练 ResNet-18，在 CIFAR-10 上微调，比较与从头训练的效果。

4.  **模型部署**：将训练好的模型导出为 ONNX 格式，尝试用 ONNX Runtime 进行推理。

---

[返回目录](index.md) | [上一章：GPU 训练与性能优化](07-gpu-training.md)