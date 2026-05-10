# 第 7 章：GPU 训练与性能优化

> **核心比喻：GPU = 千人工厂** —— CPU 像一个技艺精湛的工匠，一次做一件精细活；GPU 像一座千人工厂，同时处理大量简单任务。

---

## 7.1 为什么 GPU 比 CPU 快？

!!! example "生活化类比"
    **CPU** 像一个 **大学教授**：什么都会，但一次只能辅导一个学生。
    
    **GPU** 像一个 **小学老师带早读**：只会简单的加减乘除，但能同时指挥 1000 个学生一起朗读。
    
    深度学习中的矩阵运算恰好就是"大量简单的乘加运算"，完美匹配 GPU 的架构。

```python
import torch
import time

# 矩阵乘法性能对比
size = 5000
a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

# CPU 计算
start = time.time()
c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start
print(f"CPU 矩阵乘法 ({size}x{size}): {cpu_time:.3f}s")

# GPU 计算（如果可用）
if torch.cuda.is_available():
    a_gpu = a_cpu.to('cuda')
    b_gpu = b_cpu.to('cuda')
    
    # 预热
    _ = a_gpu @ b_gpu
    torch.cuda.synchronize()
    
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU 矩阵乘法 ({size}x{size}): {gpu_time:.3f}s")
    print(f"加速比: {cpu_time / gpu_time:.1f}x")
else:
    print("GPU 不可用，跳过 GPU 测试")
```

---

## 7.2 设备管理最佳实践

```python
# 统一的设备管理
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")

if torch.cuda.is_available():
    print(f"GPU 名称: {torch.cuda.get_device_name(0)}")
    print(f"GPU 数量: {torch.cuda.device_count()}")
    print(f"当前 GPU: {torch.cuda.current_device()}")
    print(f"显存总量: {torch.cuda.get_device_properties(0).total_mem / 1024**3:.1f} GB")

# 创建张量时指定设备
x = torch.randn(3, 4, device=device)
print(f"\n张量所在设备: {x.device}")

# 模型迁移到设备
model = torch.nn.Linear(10, 1).to(device)
print(f"模型所在设备: {next(model.parameters()).device}")
```

---

## 7.3 完整的 GPU 训练流程

```python
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 设备配置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 生成模拟数据
X = torch.randn(10000, 20)
y = (X.sum(dim=1) > 0).float().unsqueeze(1)

dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True, pin_memory=True)

# 模型
model = nn.Sequential(
    nn.Linear(20, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 1),
    nn.Sigmoid()
).to(device)

criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# GPU 训练循环
model.train()
for epoch in range(3):
    running_loss = 0.0
    
    for batch_idx, (data, target) in enumerate(dataloader):
        # 将数据移到 GPU
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f"Epoch {epoch+1}: Loss={running_loss/len(dataloader):.4f}")

print("GPU 训练完成！")
```

**运行结果（有 GPU 时）：**
```
Epoch 1: Loss=0.5234
Epoch 2: Loss=0.3456
Epoch 3: Loss=0.2891
GPU 训练完成！
```

!!! tip "GPU 训练的关键步骤"
    1.  **模型移到 GPU**：`model.to(device)`
    2.  **数据移到 GPU**：`data, target = data.to(device), target.to(device)`
    3.  **损失函数不需要移到 GPU**：它自动跟随输入数据
    4.  **pin_memory=True**：加速 CPU 到 GPU 的数据传输

---

## 7.4 混合精度训练

混合精度训练使用 `float16` 和 `float32` 混合计算，可显著加速并节省显存：

```python
if torch.cuda.is_available():
    model = nn.Sequential(
        nn.Linear(20, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 1),
    ).to(device)
    
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    # 创建 GradScaler
    scaler = torch.cuda.amp.GradScaler()
    
    model.train()
    for epoch in range(3):
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            
            # 使用 autocast 自动混合精度
            with torch.cuda.amp.autocast():
                output = model(data)
                loss = criterion(output, target)
            
            # 缩放 loss 并反向传播
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        
        print(f"Epoch {epoch+1}: Loss={loss.item():.4f}")
    
    print("混合精度训练完成！")
```

!!! info "混合精度训练原理"
    | 组件 | 作用 |
    |:---|:---|
    | `autocast()` | 自动选择 float16 或 float32 进行前向计算 |
    | `GradScaler` | 放大 loss 防止 float16 梯度下溢 |
    | `scaler.scale(loss).backward()` | 反向传播时自动缩放梯度 |
    | `scaler.step(optimizer)` | 自动还原梯度并更新参数 |
    | `scaler.update()` | 动态调整缩放因子 |

---

## 7.5 多 GPU 训练

### DataParallel（简单但效率较低）

```python
if torch.cuda.is_available() and torch.cuda.device_count() > 1:
    model = nn.Sequential(
        nn.Linear(20, 64),
        nn.ReLU(),
        nn.Linear(64, 1),
    )
    
    # 使用 DataParallel 包装模型
    model = nn.DataParallel(model)
    model = model.to(device)
    
    print(f"使用 {torch.cuda.device_count()} 个 GPU (DataParallel)")
    
    # 训练代码与单 GPU 完全相同
    x = torch.randn(64, 20).to(device)
    y = model(x)
    print(f"输出形状: {y.shape}")
```

### DistributedDataParallel（推荐）

```python
# DDP 通常通过启动脚本运行，这里展示核心代码结构
"""
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# 初始化进程组
dist.init_process_group(backend='nccl')

# 模型包装
model = MyModel().to(device)
model = DDP(model, device_ids=[local_rank])

# 分布式采样器
sampler = DistributedSampler(dataset)
dataloader = DataLoader(dataset, sampler=sampler)

# 训练循环中设置 epoch（确保每个 epoch 的 shuffle 不同）
for epoch in range(num_epochs):
    sampler.set_epoch(epoch)
    # ... 训练代码 ...

# 只在主进程保存模型
if dist.get_rank() == 0:
    torch.save(model.state_dict(), 'model.pth')
"""
print("DDP 代码结构已展示（需要多 GPU 环境运行）")
```

---

## 7.6 显存管理与优化

```python
if torch.cuda.is_available():
    print("=== 显存使用情况 ===")
    
    # 查看当前显存使用
    print(f"已分配: {torch.cuda.memory_allocated() / 1024**2:.1f} MB")
    print(f"已缓存: {torch.cuda.memory_reserved() / 1024**2:.1f} MB")
    
    # 创建一些张量
    tensors = [torch.randn(1000, 1000, device='cuda') for _ in range(5)]
    print(f"\n创建 5 个大张量后:")
    print(f"已分配: {torch.cuda.memory_allocated() / 1024**2:.1f} MB")
    
    # 释放张量
    del tensors
    torch.cuda.empty_cache()
    print(f"\n释放并清空缓存后:")
    print(f"已分配: {torch.cuda.memory_allocated() / 1024**2:.1f} MB")
    print(f"已缓存: {torch.cuda.memory_reserved() / 1024**2:.1f} MB")
```

**运行结果（有 GPU 时）：**
```
=== 显存使用情况 ===
已分配: 0.0 MB
已缓存: 0.0 MB

创建 5 个大张量后:
已分配: 19.1 MB

释放并清空缓存后:
已分配: 0.0 MB
已缓存: 20.0 MB
```

!!! tip "节省显存的技巧"
    | 技巧 | 效果 | 实现方式 |
    |:---|:---|:---|
    | 混合精度训练 | 节省约 40% 显存 | `torch.cuda.amp` |
    | 梯度累积 | 用小 batch 模拟大 batch | 多个 step 后再 `optimizer.step()` |
    | 梯度检查点 | 用计算换显存 | `torch.utils.checkpoint` |
    | 减小 batch_size | 最直接的方式 | 调整 DataLoader 参数 |
    | 及时释放变量 | 避免显存泄漏 | `del` + `torch.cuda.empty_cache()` |

---

## 7.7 性能分析工具

```python
if torch.cuda.is_available():
    # 使用 PyTorch Profiler
    print("PyTorch Profiler 使用示例：")
    print("""
    from torch.profiler import profile, ProfilerActivity
    
    with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
        # 你的训练代码
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
    
    # 打印耗时最长的操作
    print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    
    # 导出 Chrome Trace
    prof.export_chrome_trace("trace.json")
    """)
    
    # 简单的计时工具
    starter = torch.cuda.Event(enable_timing=True)
    ender = torch.cuda.Event(enable_timing=True)
    
    x = torch.randn(1000, 1000, device='cuda')
    
    starter.record()
    y = x @ x.T
    ender.record()
    
    torch.cuda.synchronize()
    elapsed = starter.elapsed_time(ender)
    print(f"GPU 矩阵乘法耗时: {elapsed:.2f} ms")
```

---

## 要点总结

- [x] GPU 擅长并行计算，特别适合深度学习中的矩阵运算
- [x] 统一使用 `device` 变量管理 CPU/GPU 切换
- [x] 模型和数据都需要 `.to(device)`
- [x] 混合精度训练（AMP）可加速 1.5-2x 并节省约 40% 显存
- [x] `DataParallel` 简单但效率低，`DistributedDataParallel` 是生产环境首选
- [x] 及时释放不需要的张量，使用 `torch.cuda.empty_cache()` 清理缓存
- [x] 使用 Profiler 定位性能瓶颈

---

## 课后练习

1.  **CPU vs GPU 对比**：用不同大小的矩阵乘法，测试 CPU 和 GPU 的加速比，画出加速比曲线。

2.  **混合精度训练**：将第 4 章的 MNIST 训练改为混合精度，比较训练速度和显存占用。

3.  **显存监控**：在训练循环中添加显存监控代码，观察不同 batch_size 下的显存使用情况。

4.  **梯度累积**：实现梯度累积（每 4 个 step 更新一次参数），模拟 4 倍 batch_size 的效果。

---

[返回目录](index.md) | [上一章：优化器与损失函数](06-optimization.md) | [下一章：完整项目实战 →](08-complete-project.md)