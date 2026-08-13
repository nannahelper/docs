# 第 5 章：数据加载与预处理

> **核心比喻：DataLoader = 传送带** —— 就像工厂的传送带自动把原材料送到工位，DataLoader 自动把数据分批送到模型。

---

## 5.1 PyTorch 数据加载体系

PyTorch 提供了两个核心类来管理数据：

| 类 | 作用 | 比喻 |
|:---|:---|:---|
| `torch.utils.data.Dataset` | 存储数据及其标签 | 仓库 |
| `torch.utils.data.DataLoader` | 批量加载、打乱、并行处理 | 传送带 |

```python
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
```

---

## 5.2 自定义 Dataset

### 从内存数据创建

```python
class SimpleDataset(Dataset):
    """最简单的自定义数据集"""
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

# 创建模拟数据
X = torch.randn(1000, 10)
y = torch.randint(0, 3, (1000,))

dataset = SimpleDataset(X, y)
print(f"数据集大小: {len(dataset)}")
print(f"第 0 个样本: data shape={dataset[0][0].shape}, label={dataset[0][1]}")
```

**运行结果：**
```
数据集大小: 1000
第 0 个样本: data shape=torch.Size([10]), label=2
```

### 从文件创建

```python
import os
from PIL import Image

class ImageFolderDataset(Dataset):
    """从文件夹加载图像的数据集"""
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        # 遍历文件夹，每个子文件夹作为一个类别
        for label, class_name in enumerate(sorted(os.listdir(root_dir))):
            class_dir = os.path.join(root_dir, class_name)
            if os.path.isdir(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.endswith(('.jpg', '.png', '.jpeg')):
                        self.image_paths.append(os.path.join(class_dir, img_name))
                        self.labels.append(label)
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

print("ImageFolderDataset 类已定义（需要实际图像文件夹才能使用）")
```

---

## 5.3 DataLoader 详解

```python
# 创建数据集
X = torch.randn(1000, 10)
y = torch.randint(0, 3, (1000,))
dataset = SimpleDataset(X, y)

# 创建 DataLoader
dataloader = DataLoader(
    dataset,
    batch_size=32,       # 每批 32 个样本
    shuffle=True,        # 每个 epoch 打乱数据
    num_workers=0,       # 数据加载的子进程数（Windows 建议设为 0）
    drop_last=False,     # 是否丢弃最后不足一个 batch 的数据
    pin_memory=False,    # 是否将数据锁页（GPU 训练时设为 True 可加速）
)

# 遍历 DataLoader
for batch_idx, (data, labels) in enumerate(dataloader):
    print(f"Batch {batch_idx}: data shape={data.shape}, labels shape={labels.shape}")
    if batch_idx >= 2:
        break

print(f"\n总批次数: {len(dataloader)}")
print(f"每批大小: {dataloader.batch_size}")
```

**运行结果：**
```
Batch 0: data shape=torch.Size([32, 10]), labels shape=torch.Size([32])
Batch 1: data shape=torch.Size([32, 10]), labels shape=torch.Size([32])
Batch 2: data shape=torch.Size([32, 10]), labels shape=torch.Size([32])

总批次数: 32
每批大小: 32
```

!!! info "DataLoader 参数说明"
    | 参数 | 说明 | 建议值 |
    |:---|:---|:---|
    | `batch_size` | 每批样本数 | 32/64/128（根据显存调整） |
    | `shuffle` | 是否打乱 | 训练=True，验证=False |
    | `num_workers` | 并行加载进程数 | Linux: 4-8, Windows: 0 |
    | `drop_last` | 丢弃最后不完整 batch | 训练时若 BatchNorm 报错则设为 True |
    | `pin_memory` | 锁页内存 | GPU 训练时设为 True |

---

## 5.4 数据预处理（Transforms）

`torchvision.transforms` 提供了丰富的图像预处理操作：

```python
from torchvision import transforms

# 定义预处理流水线
transform_pipeline = transforms.Compose([
    transforms.Resize((256, 256)),        # 调整大小
    transforms.RandomCrop(224),           # 随机裁剪
    transforms.RandomHorizontalFlip(),    # 随机水平翻转
    transforms.ColorJitter(               # 颜色抖动
        brightness=0.2,
        contrast=0.2,
        saturation=0.2,
        hue=0.1
    ),
    transforms.ToTensor(),                # 转为张量 [0, 1]
    transforms.Normalize(                 # 标准化
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

print("训练预处理流水线：")
for i, t in enumerate(transform_pipeline.transforms):
    print(f"  {i+1}. {t.__class__.__name__}")

# 验证集预处理（不需要数据增强）
val_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

print("\n验证预处理流水线：")
for i, t in enumerate(val_transform.transforms):
    print(f"  {i+1}. {t.__class__.__name__}")
```

**运行结果：**
```
训练预处理流水线：
  1. Resize
  2. RandomCrop
  3. RandomHorizontalFlip
  4. ColorJitter
  5. ToTensor
  6. Normalize

验证预处理流水线：
  1. Resize
  2. CenterCrop
  3. ToTensor
  4. Normalize
```

!!! tip "数据增强的重要性"
    数据增强是防止过拟合的 **最有效手段之一**：
    - **随机翻转/旋转**：让模型学习方向不变性
    - **颜色抖动**：让模型适应光照变化
    - **随机裁剪**：让模型关注局部特征
    - **Cutout/RandomErasing**：随机遮挡，增强鲁棒性

---

## 5.5 使用内置数据集

PyTorch 的 `torchvision.datasets` 提供了许多常用数据集：

```python
from torchvision import datasets

# CIFAR-10
cifar10_train = datasets.CIFAR10(
    root='./data',
    train=True,
    download=True,
    transform=transforms.ToTensor()
)

# Fashion-MNIST
fashion_mnist = datasets.FashionMNIST(
    root='./data',
    train=True,
    download=True,
    transform=transforms.ToTensor()
)

print(f"CIFAR-10 训练集: {len(cifar10_train)} 张图像, 类别数: {len(cifar10_train.classes)}")
print(f"CIFAR-10 类别: {cifar10_train.classes}")
print(f"\nFashion-MNIST 训练集: {len(fashion_mnist)} 张图像, 类别数: {len(fashion_mnist.classes)}")
print(f"Fashion-MNIST 类别: {fashion_mnist.classes}")
```

**运行结果：**
```
CIFAR-10 训练集: 50000 张图像, 类别数: 10
CIFAR-10 类别: ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

Fashion-MNIST 训练集: 60000 张图像, 类别数: 10
Fashion-MNIST 类别: ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
```

---

## 5.6 数据划分：训练集 / 验证集 / 测试集

```python
from torch.utils.data import random_split

# 创建完整数据集
full_dataset = SimpleDataset(
    torch.randn(10000, 10),
    torch.randint(0, 3, (10000,))
)

# 按比例划分：80% 训练，10% 验证，10% 测试
train_size = int(0.8 * len(full_dataset))
val_size = int(0.1 * len(full_dataset))
test_size = len(full_dataset) - train_size - val_size

train_dataset, val_dataset, test_dataset = random_split(
    full_dataset, [train_size, val_size, test_size]
)

print(f"训练集: {len(train_dataset)} 样本")
print(f"验证集: {len(val_dataset)} 样本")
print(f"测试集: {len(test_dataset)} 样本")

# 为每个数据集创建 DataLoader
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
```

**运行结果：**
```
训练集: 8000 样本
验证集: 1000 样本
测试集: 1000 样本
```

---

## 5.7 文本数据加载

```python
from torch.utils.data import Dataset

class TextDataset(Dataset):
    """文本分类数据集"""
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # 分词
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'label': torch.tensor(label)
        }

# 模拟数据
texts = [
    "这部电影太棒了，强烈推荐",
    "浪费时间，剧情无聊透顶",
    "还不错，值得一看",
    "演员演技在线，导演功力深厚",
]
labels = [1, 0, 1, 1]

print(f"文本数据集: {len(texts)} 条文本")
print(f"标签分布: 正面={labels.count(1)}, 负面={labels.count(0)}")
```

**运行结果：**
```
文本数据集: 4 条文本
标签分布: 正面=3, 负面=1
```

---

## 要点总结

- [x] `Dataset` 定义数据存储和访问方式，必须实现 `__len__` 和 `__getitem__`
- [x] `DataLoader` 负责批量加载、打乱、并行处理
- [x] `transforms.Compose` 组合多个预处理操作
- [x] 训练集需要数据增强，验证/测试集只需要标准化
- [x] `random_split` 方便地划分数据集
- [x] `torchvision.datasets` 提供常用图像数据集
- [x] 自定义 Dataset 可处理任意类型的数据（图像、文本、音频等）

---

## 课后练习

1.  **自定义 Dataset**：创建一个 Dataset 类，从 CSV 文件加载数据（包含特征列和标签列）。

2.  **数据增强实验**：对同一张图像应用不同的 transforms 组合，观察增强效果。

3.  **DataLoader 参数调优**：尝试不同的 `batch_size` 和 `num_workers`，比较数据加载速度。

4.  **不平衡数据处理**：实现一个加权采样器（`WeightedRandomSampler`），处理类别不平衡的数据集。

---

[返回目录](index.md) | [上一章：训练流程全解析](04-training-pipeline.md) | [下一章：优化器与损失函数 →](06-optimization.md)