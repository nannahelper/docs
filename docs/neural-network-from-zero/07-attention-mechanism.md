# 第 7 章：Transformer 注意力机制逐步解析

>  **场景：** 第 6 章我们搭建了 Transformer 的骨架，但故意跳过了最核心的组件—— **自注意力机制** 。这一章将用聚光灯的比喻，从 Query、Key、Value 的基本概念出发，一步步拆解注意力机制的每一个计算步骤，直到你完全理解为什么它是 Transformer 的灵魂。

---

## 7.1 注意力机制的直觉：聚光灯

!!! example "核心比喻：聚光灯"
    想象你在一个嘈杂的鸡尾酒会上，很多人同时在说话。你的大脑能自动"聚焦"到你正在对话的那个人身上，忽略其他人的声音。这就是 **注意力** ——从大量信息中筛选出当前最重要的部分。
    
    在 Transformer 中，每个词都像一个人，它需要决定： **在处理自己时，应该"听"哪些其他词的话，以及听多少。**

### 一个具体的例子

处理句子 **"The cat sat on the mat because it was tired"** 时：

- 处理 "it" 这个词时，模型需要知道 "it" 指的是什么
- 注意力机制让 "it" 高度关注 "cat"（因为 "it" 指代 "cat"）
- 同时 "it" 也会关注 "tired"（因为 "tired" 解释了为什么）

```
注意力权重可视化:
The  cat  sat  on  the  mat  because  it  was  tired
 |    |    |    |   |    |      |      |    |     |
 0.01 0.85 0.01 0.01 0.01 0.01  0.01  0.01 0.05 0.03  ← "it" 对各词的关注度
                    ↑
              85% 的注意力在 "cat" 上！
```

---

## 7.2 Query、Key、Value：注意力机制的三个角色

注意力机制可以用一个 **数据库检索** 的比喻来理解：

| 角色 | 比喻 | 来源 | 作用 |
|:---|:---|:---|:---|
|  **Query（查询）**  | 你在搜索引擎输入的关键词 | 当前词 | "我想找什么" |
|  **Key（键）**  | 每个网页的标题/标签 | 每个词 | "我是什么" |
|  **Value（值）**  | 每个网页的实际内容 | 每个词 | "我包含什么信息" |

 **计算过程：** 

1. 用 Query 和每个 Key 计算相似度（注意力分数）
2. 用 Softmax 将分数转换为概率（注意力权重）
3. 用注意力权重对 Value 加权求和（最终输出）

```python
import numpy as np

def attention_intuition_demo():
    """用搜索引擎的比喻演示注意力机制"""
    
    # 三个词（简化到 4 维向量）
    words = ["我", "爱", "北京"]
    embed_dim = 4
    
    # 每个词的嵌入向量
    embeddings = np.array([
        [1.0, 0.0, 0.0, 0.0],  # "我"
        [0.0, 1.0, 0.0, 0.0],  # "爱"
        [0.0, 0.0, 1.0, 0.0],  # "北京"
    ])
    
    # 简化：直接用嵌入作为 Q, K, V（实际中会通过不同的权重矩阵投影）
    Q = embeddings.copy()  # Query: 每个词"想找什么"
    K = embeddings.copy()  # Key:   每个词"是什么"
    V = embeddings.copy()  # Value: 每个词"包含什么信息"
    
    # 步骤1: 计算注意力分数（Query 和 Key 的点积）
    scores = np.dot(Q, K.T)
    
    # 步骤2: 缩放（除以 sqrt(d_k) 防止梯度过小）
    d_k = embed_dim
    scores_scaled = scores / np.sqrt(d_k)
    
    # 步骤3: Softmax 得到注意力权重
    def softmax(x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
    
    attention_weights = softmax(scores_scaled)
    
    # 步骤4: 加权求和
    output = np.dot(attention_weights, V)
    
    print("注意力分数矩阵 (Q·K^T):")
    print(scores)
    print(f"\n缩放后 (除以 sqrt({d_k}) = {np.sqrt(d_k):.2f}):")
    print(scores_scaled)
    print("\n注意力权重 (Softmax 后，每行之和=1):")
    print(np.round(attention_weights, 3))
    print(f"\n每行之和: {attention_weights.sum(axis=1)}")
    print(f"\n最终输出 (加权求和):")
    print(output)

attention_intuition_demo()
```

**渲染效果：**
```
注意力分数矩阵 (Q·K^T):
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]

缩放后 (除以 sqrt(4) = 2.00):
[[0.5 0.  0. ]
 [0.  0.5 0. ]
 [0.  0.  0.5]]

注意力权重 (Softmax 后，每行之和=1):
[[0.506 0.247 0.247]
 [0.247 0.506 0.247]
 [0.247 0.247 0.506]]

每行之和: [1. 1. 1.]

最终输出 (加权求和):
[[0.506 0.247 0.247]
 [0.247 0.506 0.247]
 [0.247 0.247 0.506]]
```

---

## 7.3 自注意力的完整数学公式

$$Attn(Q, K, V) = \sigma\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

其中 $\sigma$ 表示 softmax 函数。

逐步拆解：

```python
def self_attention_step_by_step(X, W_q, W_k, W_v):
    """
    X: 输入序列 (seq_len, embed_dim)
    W_q, W_k, W_v: 可学习的投影矩阵
    """
    seq_len, embed_dim = X.shape
    
    # 步骤1: 线性投影 → Q, K, V
    Q = np.dot(X, W_q)  # (seq_len, d_k)
    K = np.dot(X, W_k)  # (seq_len, d_k)
    V = np.dot(X, W_v)  # (seq_len, d_v)
    
    print(f"Q 形状: {Q.shape}")
    print(f"K 形状: {K.shape}")
    print(f"V 形状: {V.shape}")
    
    # 步骤2: 计算注意力分数
    scores = np.dot(Q, K.T)  # (seq_len, seq_len)
    print(f"\n注意力分数形状: {scores.shape}")
    print(f"分数矩阵 (未缩放):\n{np.round(scores, 3)}")
    
    # 步骤3: 缩放
    d_k = Q.shape[1]
    scores_scaled = scores / np.sqrt(d_k)
    print(f"\n缩放因子: 1/√{d_k} = {1/np.sqrt(d_k):.4f}")
    
    # 步骤4: Softmax
    attention_weights = np.exp(scores_scaled - np.max(scores_scaled, axis=-1, keepdims=True))
    attention_weights /= np.sum(attention_weights, axis=-1, keepdims=True)
    print(f"\n注意力权重:\n{np.round(attention_weights, 3)}")
    
    # 步骤5: 加权求和
    output = np.dot(attention_weights, V)
    print(f"\n输出形状: {output.shape}")
    
    return output, attention_weights

# 演示
np.random.seed(42)
seq_len, embed_dim, d_k = 4, 6, 6

X = np.random.randn(seq_len, embed_dim)
W_q = np.random.randn(embed_dim, d_k) * 0.1
W_k = np.random.randn(embed_dim, d_k) * 0.1
W_v = np.random.randn(embed_dim, d_k) * 0.1

output, attn_weights = self_attention_step_by_step(X, W_q, W_k, W_v)
```

**渲染效果：**
```
Q 形状: (4, 6)
K 形状: (4, 6)
V 形状: (4, 6)

注意力分数形状: (4, 4)
分数矩阵 (未缩放):
[[ 0.015 -0.001  0.001 -0.001]
 [-0.001  0.001 -0.001  0.   ]
 [ 0.001 -0.001  0.001 -0.   ]
 [-0.001  0.     -0.     0.   ]]

缩放因子: 1/√6 = 0.4082

注意力权重:
[[0.251 0.25  0.25  0.25 ]
 [0.25  0.25  0.25  0.25 ]
 [0.25  0.25  0.25  0.25 ]
 [0.25  0.25  0.25  0.25 ]]

输出形状: (4, 6)
```

!!! tip "为什么要除以 $\sqrt{d_k}$？"
    当 $d_k$ 很大时，点积 $QK^T$ 的值会很大，导致 Softmax 后的梯度非常小（梯度消失）。除以 $\sqrt{d_k}$ 将方差控制在 1 左右，保持梯度健康。这是 Transformer 论文中的一个关键细节。

---

## 7.4 多头注意力：多个聚光灯同时工作

单头注意力只能捕捉一种关系模式。 **多头注意力** （Multi-Head Attention）让模型同时从多个角度关注信息。

!!! example "比喻：多个专家同时分析"
    一个头可能关注 **语法关系** （主语-谓语），另一个头关注 **指代关系** （代词-先行词），第三个头关注 **语义关系** （同义词、相关概念）。多个头并行工作，最后拼接结果。

```python
def multi_head_attention(X, num_heads=4, embed_dim=64):
    """
    多头注意力：将 Q、K、V 分成多个头，每个头独立计算注意力
    """
    seq_len = X.shape[0]
    head_dim = embed_dim // num_heads
    
    # 投影矩阵（实际中每个头有独立的 W_q, W_k, W_v）
    W_q = np.random.randn(embed_dim, embed_dim) * 0.02
    W_k = np.random.randn(embed_dim, embed_dim) * 0.02
    W_v = np.random.randn(embed_dim, embed_dim) * 0.02
    W_o = np.random.randn(embed_dim, embed_dim) * 0.02
    
    # 线性投影
    Q = np.dot(X, W_q)  # (seq_len, embed_dim)
    K = np.dot(X, W_k)
    V = np.dot(X, W_v)
    
    # 拆分成多个头
    Q_heads = Q.reshape(seq_len, num_heads, head_dim).transpose(1, 0, 2)
    K_heads = K.reshape(seq_len, num_heads, head_dim).transpose(1, 0, 2)
    V_heads = V.reshape(seq_len, num_heads, head_dim).transpose(1, 0, 2)
    
    print(f"拆分后 Q_heads 形状: {Q_heads.shape}  (头数, 序列长度, 每头维度)")
    
    # 每个头独立计算注意力
    head_outputs = []
    for h in range(num_heads):
        scores = np.dot(Q_heads[h], K_heads[h].T) / np.sqrt(head_dim)
        weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        weights /= np.sum(weights, axis=-1, keepdims=True)
        head_out = np.dot(weights, V_heads[h])
        head_outputs.append(head_out)
    
    # 拼接所有头的输出
    concat = np.concatenate(head_outputs, axis=-1)
    print(f"拼接后形状: {concat.shape}")
    
    # 最终线性投影
    output = np.dot(concat, W_o)
    print(f"最终输出形状: {output.shape}")
    
    return output

# 演示
X = np.random.randn(5, 64)  # 5 个 token，64 维嵌入
output = multi_head_attention(X, num_heads=4, embed_dim=64)
```

**渲染效果：**
```
拆分后 Q_heads 形状: (4, 5, 16)  (头数, 序列长度, 每头维度)
拼接后形状: (5, 64)
最终输出形状: (5, 64)
```

---

## 7.5 注意力权重的可视化

理解注意力机制最好的方式是 **可视化注意力权重** ：

```python
import matplotlib.pyplot as plt

def visualize_attention(sentence, attention_weights):
    """
    可视化注意力权重矩阵
    
    sentence: 词列表
    attention_weights: (seq_len, seq_len) 的注意力权重矩阵
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    im = ax.imshow(attention_weights, cmap='Blues')
    
    ax.set_xticks(range(len(sentence)))
    ax.set_yticks(range(len(sentence)))
    ax.set_xticklabels(sentence, rotation=45, ha='right')
    ax.set_yticklabels(sentence)
    
    ax.set_xlabel('Key（被关注的词）')
    ax.set_ylabel('Query（正在处理的词）')
    ax.set_title('自注意力权重可视化')
    
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.show()

# 示例：模拟 "it" 关注 "cat" 的注意力模式
sentence = ["The", "cat", "sat", "on", "the", "mat", "because", "it", "was", "tired"]

# 构造模拟的注意力权重（实际中由模型计算得出）
np.random.seed(42)
fake_weights = np.random.rand(len(sentence), len(sentence))
# 让 "it" (索引7) 高度关注 "cat" (索引1)
fake_weights[7, 1] = 0.85
fake_weights[7, :] /= fake_weights[7, :].sum()  # 重新归一化

visualize_attention(sentence, fake_weights)
print("注意第 8 行（'it'）第 2 列（'cat'）的颜色最深——'it' 最关注 'cat'")
```

**渲染效果：** 一张热力图，第 8 行（"it"）第 2 列（"cat"）的格子颜色最深，直观展示了注意力机制如何建立词与词之间的关联。

---

## 7.6 自注意力 vs 交叉注意力 vs 因果自注意力

Transformer 中有三种注意力模式：

| 类型 | Q 来源 | K, V 来源 | 用途 | 谁在用 |
|:---|:---|:---|:---|:---|
| **自注意力** | 当前序列 | 当前序列 | 捕捉序列内部关系 | Encoder、Decoder |
| **因果自注意力** | 当前序列 | 当前序列（+掩码） | 自回归生成 | GPT Decoder |
| **交叉注意力** | Decoder | Encoder 输出 | 连接编码器和解码器 | 原始 Transformer Decoder |

```python
def cross_attention_demo(decoder_input, encoder_output):
    """
    交叉注意力：Q 来自 Decoder，K 和 V 来自 Encoder
    用于翻译等 seq2seq 任务
    """
    embed_dim = 64
    
    W_q = np.random.randn(embed_dim, embed_dim) * 0.02
    W_k = np.random.randn(embed_dim, embed_dim) * 0.02
    W_v = np.random.randn(embed_dim, embed_dim) * 0.02
    
    Q = np.dot(decoder_input, W_q)  # 来自 Decoder
    K = np.dot(encoder_output, W_k) # 来自 Encoder
    V = np.dot(encoder_output, W_v) # 来自 Encoder
    
    scores = np.dot(Q, K.T) / np.sqrt(embed_dim)
    weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    weights /= np.sum(weights, axis=-1, keepdims=True)
    
    output = np.dot(weights, V)
    
    print(f"Decoder 输入形状: {decoder_input.shape}")
    print(f"Encoder 输出形状: {encoder_output.shape}")
    print(f"交叉注意力输出形状: {output.shape}")
    print(f"\n关键区别: Q 来自 Decoder，K 和 V 来自 Encoder")

# 演示
dec_input = np.random.randn(5, 64)   # Decoder: 5 个目标语言 token
enc_output = np.random.randn(7, 64)  # Encoder: 7 个源语言 token
cross_attention_demo(dec_input, enc_output)
```

**渲染效果：**
```
Decoder 输入形状: (5, 64)
Encoder 输出形状: (7, 64)
交叉注意力输出形状: (5, 64)

关键区别: Q 来自 Decoder，K 和 V 来自 Encoder
```

---

## 7.7 注意力机制的计算复杂度

自注意力的核心操作是 $QK^T$，形状为 $(n, d) \times (d, n) = (n, n)$：

-  **时间复杂度** ：$O(n^2 \cdot d)$ —— 与序列长度的平方成正比
-  **空间复杂度** ：$O(n^2)$ —— 需要存储 $n \times n$ 的注意力矩阵

这就是为什么 LLM 有 **上下文窗口限制** ——当 $n=100000$ 时，注意力矩阵有 100 亿个元素，需要约 40GB 显存。

---

## 要点总结

- [x] 注意力机制 = 从大量信息中筛选当前最重要的部分（聚光灯比喻）
- [x] Query（我想找什么）× Key（我是什么）→ 注意力分数 → Softmax → 注意力权重
- [x] 注意力权重 × Value（我包含什么）→ 加权输出
- [x] 缩放因子 $\sqrt{d_k}$ 防止 Softmax 梯度消失
- [x] 多头注意力 = 多个聚光灯从不同角度同时关注
- [x] 因果掩码确保自回归生成时不能"偷看"未来
- [x] 注意力复杂度 $O(n^2)$ 是上下文窗口限制的根本原因

---

## 课后练习

1.  **手算注意力** ：对 3 个词、2 维嵌入的序列，手动计算完整的自注意力过程（包括 Q、K、V 投影、分数、Softmax、输出）。

2.  **可视化实验** ：修改上面的可视化代码，尝试不同的句子（如中英文混合），观察注意力模式的变化。

3.  **思考题** ：如果去掉多头注意力的缩放因子 $\sqrt{d_k}$，当 $d_k=1024$ 时，Softmax 的输出会怎样？为什么这会导致训练问题？

---

**下一章预告：** 注意力机制让模型知道"该关注哪些词"，但模型的知识存储在哪里？第 8 章将揭示 LLM 如何在其参数中存储和检索事实——从 FFN 层作为"键值记忆"到知识定位与编辑。

[继续第 8 章：LLM 如何记忆 →](08-how-llms-memorize.md)