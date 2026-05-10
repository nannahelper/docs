# 第 6 章：Transformer 架构解读 —— LLM 引擎如何运转

> **场景：** 2017 年，Google 的一篇论文《Attention Is All You Need》彻底改变了 AI 的格局。Transformer 架构抛弃了传统的循环神经网络（RNN），用一种全新的"注意力机制"来处理序列数据。本章将拆解 Transformer 的每一个组件，让你理解这个"流水线工厂"如何高效处理语言。

---

## 6.1 为什么需要 Transformer？

### RNN 的困境

在 Transformer 之前，处理文本的主流架构是 RNN（循环神经网络）：

```
RNN 处理 "我 爱 北京 天安门":
步骤1: "我"    → 隐藏状态 h1
步骤2: "爱"    → 隐藏状态 h2 (依赖 h1)
步骤3: "北京"  → 隐藏状态 h3 (依赖 h2)
步骤4: "天安门" → 隐藏状态 h4 (依赖 h3)
```

RNN 的三大问题：

| 问题 | 描述 | 后果 |
|:---|:---|:---|
| **串行处理** | 必须等前一个词处理完才能处理下一个 | 训练极慢，无法利用 GPU 并行 |
| **长距离遗忘** | 第 1 个词的信息传到第 100 个词时几乎消失 | 无法捕捉长距离依赖 |
| **梯度问题** | 反向传播经过 100 步链式法则 | 梯度消失或爆炸 |

!!! example "核心比喻：流水线工厂 vs 手工作坊"
    - **RNN** = 手工作坊：一个工人（隐藏状态）依次处理每个零件（词），处理第 100 个时已经忘了第 1 个长什么样
    - **Transformer** = 流水线工厂：所有零件同时放在传送带上，每个工位（注意力头）可以同时看到所有零件，并决定自己该关注哪些

---

## 6.2 Transformer 的整体结构

Transformer 由 **编码器（Encoder）** 和 **解码器（Decoder）** 组成。GPT 系列只用了 Decoder 部分，所以我们重点讲 Decoder。

```
输入文本 → [Token Embedding + 位置编码]
              ↓
    ┌─────────────────────────┐
    │  Masked Multi-Head      │  ← 第7章详解
    │  Self-Attention         │
    ├─────────────────────────┤
    │  Add & Layer Norm       │  ← 残差连接 + 层归一化
    ├─────────────────────────┤
    │  Feed Forward Network   │  ← 全连接层
    ├─────────────────────────┤
    │  Add & Layer Norm       │
    └─────────────────────────┘
              ↓
         (重复 N 次，GPT-3 有 96 层)
              ↓
    [Linear + Softmax] → 下一个词的概率分布
```

---

## 6.3 组件 1：输入嵌入（Token Embedding）

第一步：把 token ID 转换为稠密向量。

```python
import numpy as np

# 假设词汇表有 50000 个 token，每个用 768 维向量表示
vocab_size = 50000
embed_dim = 768

# 嵌入矩阵：每一行是一个 token 的向量表示
embedding_matrix = np.random.randn(vocab_size, embed_dim) * 0.02

# 输入: "今天天气真好" → token IDs
token_ids = np.array([1234, 5678, 9012, 3456, 7890])

# 查表获取嵌入向量
token_embeddings = embedding_matrix[token_ids]
print(f"输入 token 数: {len(token_ids)}")
print(f"嵌入向量形状: {token_embeddings.shape}")  # (5, 768)
print(f"第一个 token 的嵌入向量 (前5维): {token_embeddings[0, :5]}")
```

**渲染效果：**
```
输入 token 数: 5
嵌入向量形状: (5, 768)
第一个 token 的嵌入向量 (前5维): [ 0.0098 -0.0124  0.0032 -0.0087  0.0156]
```

!!! info "嵌入向量的意义"
    嵌入向量是模型学习到的"词义表示"。语义相近的词（如"开心"和"快乐"）在向量空间中距离很近。这些向量在预训练过程中不断优化，最终编码了丰富的语义信息。

---

## 6.4 组件 2：位置编码（Positional Encoding）

Transformer 并行处理所有词，但丢失了词的顺序信息。位置编码就是给每个位置打上"时间戳"。

```python
def sinusoidal_position_encoding(seq_len, embed_dim):
    """
    原始 Transformer 使用正弦/余弦函数生成位置编码
    每个维度的频率不同，形成独特的位置"指纹"
    """
    position = np.arange(seq_len)[:, np.newaxis]  # (seq_len, 1)
    div_term = np.exp(np.arange(0, embed_dim, 2) * 
                      (-np.log(10000.0) / embed_dim))  # (embed_dim/2,)
    
    pe = np.zeros((seq_len, embed_dim))
    pe[:, 0::2] = np.sin(position * div_term)   # 偶数维用 sin
    pe[:, 1::2] = np.cos(position * div_term)   # 奇数维用 cos
    
    return pe

# 可视化位置编码
import matplotlib.pyplot as plt

seq_len, embed_dim = 50, 128
pe = sinusoidal_position_encoding(seq_len, embed_dim)

plt.figure(figsize=(10, 4))
plt.imshow(pe, aspect='auto', cmap='RdBu')
plt.colorbar(label='编码值')
plt.xlabel('嵌入维度')
plt.ylabel('位置')
plt.title('正弦位置编码：每个位置有独特的"指纹"')
plt.show()
```

**渲染效果：** 一张热力图，每行是一个位置的编码向量，呈现出独特的条纹模式——相邻位置的编码相似但不相同，模型可以从中推断词的顺序。

```python
# 最终输入 = 词嵌入 + 位置编码
final_input = token_embeddings + pe[:len(token_ids)]
print(f"最终输入形状: {final_input.shape}")  # (5, 768)
```

---

## 6.5 组件 3：前馈网络（Feed Forward Network）

注意力层之后，每个位置的向量会通过一个简单的两层全连接网络：

$$\text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$$

```python
def feed_forward_network(x, W1, b1, W2, b2):
    """
    x: 输入向量，形状 (seq_len, embed_dim)
    W1: 第一层权重 (embed_dim, ffn_dim)，ffn_dim 通常是 embed_dim 的 4 倍
    W2: 第二层权重 (ffn_dim, embed_dim)
    """
    # 第一层：升维
    hidden = np.maximum(0, np.dot(x, W1) + b1)  # ReLU
    
    # 第二层：降维回原始维度
    output = np.dot(hidden, W2) + b2
    
    return output

# 示例
embed_dim, ffn_dim = 768, 3072  # ffn_dim = 4 * embed_dim
W1 = np.random.randn(embed_dim, ffn_dim) * 0.02
b1 = np.zeros(ffn_dim)
W2 = np.random.randn(ffn_dim, embed_dim) * 0.02
b2 = np.zeros(embed_dim)

x = np.random.randn(5, embed_dim)  # 5 个 token
output = feed_forward_network(x, W1, b1, W2, b2)
print(f"FFN 输入形状: {x.shape}")
print(f"FFN 输出形状: {output.shape}")  # 形状不变
```

**渲染效果：**
```
FFN 输入形状: (5, 768)
FFN 输出形状: (5, 768)
```

!!! tip "为什么 FFN 要先升维再降维？"
    升维（768 → 3072）给了模型更大的"思考空间"来对每个 token 进行非线性变换。降维（3072 → 768）把结果压缩回标准维度，以便和下一层对接。这种"先扩展再压缩"的设计被证明非常有效。

---

## 6.6 组件 4：残差连接与层归一化

每个子层（注意力、FFN）后面都有两个操作：

```
输出 = LayerNorm(x + Sublayer(x))
```

### 残差连接（Residual Connection）

$$\text{output} = x + \text{Sublayer}(x)$$

**直觉：** 给梯度一条"高速公路"，让它能直接流到前面的层，缓解梯度消失。

```python
def residual_connection(x, sublayer_fn):
    """残差连接：输入 + 子层输出"""
    return x + sublayer_fn(x)
```

### 层归一化（Layer Normalization）

对每个样本的特征维度做归一化，让训练更稳定。

```python
def layer_norm(x, epsilon=1e-5):
    """
    对每个样本的所有特征做归一化
    x: (seq_len, embed_dim)
    """
    mean = np.mean(x, axis=-1, keepdims=True)
    std = np.std(x, axis=-1, keepdims=True)
    return (x - mean) / (std + epsilon)
```

---

## 6.7 组件 5：因果掩码（Causal Mask）

GPT 是自回归模型——预测第 $t$ 个词时，只能看到前 $t-1$ 个词，不能偷看后面的词。

```python
def create_causal_mask(seq_len):
    """
    创建因果掩码矩阵
    1 表示可以看到，0 表示需要屏蔽
    """
    mask = np.tril(np.ones((seq_len, seq_len)))  # 下三角矩阵
    return mask

# 可视化
seq_len = 5
mask = create_causal_mask(seq_len)

print("因果掩码矩阵（1=可见, 0=屏蔽）:")
print(mask)
print("\n解读: 第 i 行第 j 列 = 1 表示预测第 i 个词时可以看第 j 个词")
print("例如第 3 行: 预测第 3 个词时，可以看到第 0,1,2 个词，不能看第 3,4 个词")
```

**渲染效果：**
```
因果掩码矩阵（1=可见, 0=屏蔽）:
[[1. 0. 0. 0. 0.]
 [1. 1. 0. 0. 0.]
 [1. 1. 1. 0. 0.]
 [1. 1. 1. 1. 0.]
 [1. 1. 1. 1. 1.]]

解读: 第 i 行第 j 列 = 1 表示预测第 i 个词时可以看第 j 个词
例如第 3 行: 预测第 3 个词时，可以看到第 0,1,2 个词，不能看第 3,4 个词
```

---

## 6.8 完整 Transformer Block 的代码实现

```python
class TransformerBlock:
    """一个 Transformer Decoder 层的完整实现"""
    
    def __init__(self, embed_dim=768, num_heads=12, ffn_dim=3072):
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        
        # 自注意力参数（第7章详解）
        self.W_q = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_k = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_v = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_o = np.random.randn(embed_dim, embed_dim) * 0.02
        
        # 前馈网络参数
        self.W1 = np.random.randn(embed_dim, ffn_dim) * 0.02
        self.b1 = np.zeros(ffn_dim)
        self.W2 = np.random.randn(ffn_dim, embed_dim) * 0.02
        self.b2 = np.zeros(embed_dim)
    
    def self_attention(self, x, mask=None):
        """多头自注意力（简化版，第7章详解）"""
        Q = np.dot(x, self.W_q)
        K = np.dot(x, self.W_k)
        V = np.dot(x, self.W_v)
        
        # 注意力分数
        scores = np.dot(Q, K.T) / np.sqrt(self.embed_dim)
        
        # 应用因果掩码
        if mask is not None:
            scores = np.where(mask == 0, -1e9, scores)
        
        # Softmax + 加权求和
        attention_weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        attention_weights /= np.sum(attention_weights, axis=-1, keepdims=True)
        
        context = np.dot(attention_weights, V)
        return np.dot(context, self.W_o)
    
    def forward(self, x, mask=None):
        # 1. 自注意力 + 残差 + 层归一化
        attn_out = self.self_attention(x, mask)
        x = layer_norm(x + attn_out)
        
        # 2. 前馈网络 + 残差 + 层归一化
        ffn_out = feed_forward_network(x, self.W1, self.b1, self.W2, self.b2)
        x = layer_norm(x + ffn_out)
        
        return x

# 测试
seq_len, embed_dim = 5, 768
x = np.random.randn(seq_len, embed_dim)
mask = create_causal_mask(seq_len)

block = TransformerBlock()
output = block.forward(x, mask)
print(f"Transformer Block 输入形状: {x.shape}")
print(f"Transformer Block 输出形状: {output.shape}")
print(f"输入输出形状相同: {x.shape == output.shape}")
```

**渲染效果：**
```
Transformer Block 输入形状: (5, 768)
Transformer Block 输出形状: (5, 768)
输入输出形状相同: True
```

---

## 6.9 GPT 系列模型的规模

| 模型 | 层数 | 嵌入维度 | 注意力头数 | FFN 维度 | 总参数 |
|:---|:---|:---|:---|:---|:---|
| GPT-1 | 12 | 768 | 12 | 3072 | 1.17 亿 |
| GPT-2 | 48 | 1600 | 25 | 6400 | 15 亿 |
| GPT-3 | 96 | 12288 | 96 | 49152 | 1750 亿 |
| GPT-4 | ~120 | 未公开 | 未公开 | 未公开 | ~1.76 万亿 |

---

## 要点总结

- [x] Transformer 用自注意力替代了 RNN 的循环结构，实现并行处理
- [x] 输入嵌入 + 位置编码 = 模型看到的"词 + 位置"信息
- [x] 前馈网络（FFN）先升维再降维，给每个 token 独立的非线性变换
- [x] 残差连接 = 梯度高速公路，缓解深层网络的梯度消失
- [x] 层归一化 = 稳定训练，加速收敛
- [x] 因果掩码 = 确保预测时不能"偷看"未来的词
- [x] 多个 Transformer Block 堆叠形成深度网络

---

## 课后练习

1. **手算位置编码**：对 `seq_len=3, embed_dim=4`，手动计算正弦位置编码矩阵。

2. **残差连接实验**：修改上面的 `TransformerBlock`，去掉残差连接，观察训练 100 层网络时的梯度变化。

3. **思考题**：为什么 Transformer 的 FFN 维度通常是嵌入维度的 4 倍？如果改成 2 倍或 8 倍会怎样？

---

**下一章预告：** 第 6 章中我们跳过了 Transformer 最核心的组件——**自注意力机制**。第 7 章将深入剖析注意力机制的工作原理：Query、Key、Value 分别是什么？多头注意力为什么有效？注意力权重如何可视化？

[继续第 7 章：注意力机制 →](07-attention-mechanism.md)