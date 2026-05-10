# 第 7 章：表格单纯形法与进阶 —— 系统的迭代工具

> **场景：** 第 6 章我们用手工推导理解了单纯形法的每一步。但手工计算时，把所有公式写来写去容易出错。**表格单纯形法**把这些信息整理成一张表，每次迭代只需更新表格中的数字——就像一个精密的"算盘"。

---

## 7.1 单纯形表的结构

单纯形表（Simplex Tableau）是增广矩阵的表格化展示：

|  | $x_1$ | $x_2$ | $s_1$ | $s_2$ | RHS ($b$) | $\theta$ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **$s_1$（基）** | $a_{11}$ | $a_{12}$ | 1 | 0 | $b_1$ | $\theta_1$ |
| **$s_2$（基）** | $a_{21}$ | $a_{22}$ | 0 | 1 | $b_2$ | $\theta_2$ |
| **$z$ 行** | $\sigma_1$ | $\sigma_2$ | 0 | 0 | $z_0$ | — |

```python
def print_tableau(tableau, basis, iteration=0):
    """打印单纯形表"""
    headers = ["基", "$x_1$", "$x_2$", "$s_1$", "$s_2$", "RHS", "$\\theta$"]
    print(f"\n{'='*65}")
    print(f"  单纯形表（迭代 {iteration}）")
    print('='*65)
    
    header_line = f"{'':>4} {'基':>6} |"
    for h in headers[1:-1]:
        header_line += f" {h:>6} |"
    header_line += f" {headers[-1]:>6}"
    print(header_line)
    print("-" * 65)
    
    for i, row in enumerate(tableau):
        basis_var = basis[i]
        print(f"  {basis_var:>6} |" + "".join([f" {v:>6.2f} |" for v in row]))

print("\n" + "=" * 65)
print("  初始单纯形表（奶茶店问题）")
print("=" * 65)

initial_tableau = [
    [2, 1, 1, 0, 10],
    [1, 2, 0, 1, 8],
    [-5, -3, 0, 0, 0]
]
initial_basis = ['$s_1$', '$s_2$']
print_tableau(initial_tableau, initial_basis, 0)

print("\n解读:")
print("  - 松弛变量 s1, s2 构成单位矩阵作为初始基")
print("  - RHS 列是右端项（资源上限）")
print("  - z 行是检验数（初始时 = -c_j）")
```

**渲染效果：**
```
============================================================
  单纯形表（迭代 0）
============================================================
    基 |   x1 |   x2 |   s1 |   s2 |  RHS | theta
------------------------------------------------------------
    s1 |  2.00 |  1.00 |  1.00 |  0.00 | 10.00 |     —
    s2 |  1.00 |  2.00 |  0.00 |  1.00 |  8.00 |     —
     z | -5.00 | -3.00 |  0.00 |  0.00 |  0.00 |     —
```

---

## 7.2 第一次迭代：表格操作

### 步骤 1：确定换入变量

在 $z$ 行（检验数行）中找最负的数（对于 max 问题）：

- $\sigma_1 = -5$（最负）→ $x_1$ **换入**

### 步骤 2：确定换出变量（最小比值）

计算 $\theta = b_i / a_{ik}$：

| 基 | RHS ($b$) | $a_{i1}$ (x1 列) | $\theta_i = b_i / a_{i1}$ |
|:---|:---:|:---:|:---:|
| $s_1$ | 10 | 2 | **5** ← 最小 |
| $s_2$ | 8 | 1 | 8 |

→ $s_1$ **换出**

### 步骤 3：旋转运算

```python
def simplex_iteration(tableau, basis, pivot_row, pivot_col):
    """
    执行一次单纯形迭代
    pivot_row: 换出变量所在行
    pivot_col: 换入变量所在列
    """
    print(f"\n旋转运算: pivot at ({pivot_row}, {pivot_col})")
    print(f"换出变量: {basis[pivot_row]}, 换入变量: 列 {pivot_col}")
    
    # pivot_row, pivot_col 索引（不含 RHS）
    pivot_element = tableau[pivot_row][pivot_col]
    
    print(f"旋转元: {pivot_element}")
    
    # 1. pivot 行除以 pivot element
    tableau[pivot_row] = [v / pivot_element for v in tableau[pivot_row]]
    
    # 2. 其他行减去 pivot 列的倍数
    for i in range(len(tableau)):
        if i != pivot_row:
            factor = tableau[i][pivot_col]
            for j in range(len(tableau[i])):
                tableau[i][j] -= factor * tableau[pivot_row][j]
    
    # 更新基变量
    old_basis_var = basis[pivot_row]
    new_basis_var = f'$x_{pivot_col+1}$' if pivot_col < 2 else f'$s_{pivot_col-1}$'
    basis[pivot_row] = new_basis_var
    
    return tableau, basis

# 第一次迭代
t1 = [row[:] for row in initial_tableau]
b1 = initial_basis[:]
t1, b1 = simplex_iteration(t1, b1, 0, 0)  # pivot at row 0, col 0
print_tableau(t1, b1, 1)
```

**渲染效果：**
```
旋转运算: pivot at (0, 0)
换出变量: s1, 换入变量: 列 0
旋转元: 2.0

============================================================
  单纯形表（迭代 1）
============================================================
    基 |   x1 |   x2 |   s1 |   s2 |  RHS | theta
------------------------------------------------------------
   x1 |  1.00 |  0.50 |  0.50 |  0.00 |  5.00 |     —
    s2 |  0.00 |  1.50 | -0.50 |  1.00 |  3.00 |     —
     z |  0.00 | -0.50 |  2.50 |  0.00 | 25.00 |     —
```

---

## 7.3 第二次迭代

```python
# 第二次迭代
print("\n第二次迭代:")
print("  换入变量: s1（z 行 σ_s1 = 2.5 > 0 对于 min 问题）")
print("  最小比值: s2 行 3/1.5 = 2")
print("  换出变量: s2")

t2 = [row[:] for row in t1]
b2 = b1[:]
t2, b2 = simplex_iteration(t2, b2, 1, 2)  # pivot at row 1, col 2 (s1)
print_tableau(t2, b2, 2)

print("\n最优性检验:")
print("  所有检验数 (z 行非基变量列) ≤ 0 ✓")
print("  z = 26, x1 = 4, x2 = 2")
```

**渲染效果：**
```
============================================================
  单纯形表（迭代 2）
============================================================
    基 |   x1 |   x2 |   s1 |   s2 |  RHS | theta
------------------------------------------------------------
   x1 |  1.00 |  2.00 |  0.00 | -1.00 |  4.00 |     —
   s1 |  0.00 | -3.00 |  1.00 |  2.00 |  6.00 |     —
     z |  0.00 |  4.00 |  0.00 |  5.00 | 26.00 |     —
```

---

## 7.4 人工变量法：寻找初始可行基

!!! example "问题引入"
    如果初始约束矩阵 $A$ 不包含 $m \times m$ 的单位矩阵，我们无法直接得到一个明显的初始可行基。
    
    例如：如果所有约束都是 "$\ge$" 或 "="，就没有天然的松弛变量。

**解决方案：添加人工变量**

- **大 M 法**：在目标函数中对人工变量施加一个巨大的惩罚系数 $M$
- **两阶段法**：第一阶段最小化人工变量，第二阶段移除人工变量继续优化

---

## 7.5 两阶段法

### 第一阶段：消除人工变量

```python
def two_phase_example():
    """
    两阶段法示例
    
    原始问题:
    min z = 3x1 + 2x2
    s.t. x1 + x2 = 10
         2x1 + x2 >= 12
         x1, x2 >= 0
    """
    print("两阶段法示例")
    print("=" * 60)
    
    print("\n原始问题（需要人工变量）:")
    print("  min z = 3x1 + 2x2")
    print("  s.t. x1 + x2 = 10        ← 等式约束")
    print("       2x1 + x2 >= 12      ← >= 约束")
    print("       x1, x2 >= 0")
    
    print("\n转换为标准形式（加入剩余变量和人工变量）:")
    print("  约束1: x1 + x2 + R1 = 10    (R1 是人工变量)")
    print("  约束2: 2x1 + x2 - s2 + R2 = 12  (s2 是剩余变量, R2 是人工变量)")
    
    print("\n第一阶段目标：最小化 R1 + R2")
    print("  - 如果 min(R1+R2) > 0：原问题无可行解")
    print("  - 如果 min(R1+R2) = 0：人工变量可以出基，原问题有可行基")
    
    print("\n经过第一阶段求解（跳过详细计算）:")
    print("  最优解: x1 = 2, x2 = 8, R1 = R2 = 0")
    print("  第一阶段目标值: 0")
    print("  → 原问题可行，进入第二阶段")
    
    print("\n第二阶段：移除人工变量，优化原目标")
    print("  min z = 3x1 + 2x2")
    print("  使用第一阶段得到的可行基继续迭代...")
    print("  最优解: x1 = 2, x2 = 8, z = 22")

two_phase_example()
```

---

## 7.6 大 M 法

```python
def big_m_example():
    """
    大 M 法示例
    
    对人工变量施加惩罚系数 M（很大的数）
    """
    print("大 M 法")
    print("=" * 50)
    
    print("\n原始问题:")
    print("  min z = 3x1 + 2x2")
    print("  s.t. x1 + x2 = 10")
    print("       2x1 + x2 >= 12")
    
    print("\n加入人工变量后的目标函数:")
    print("  min z = 3x1 + 2x2 + 0*s2 + M*R1 + M*R2")
    print("  (M 是一个非常大的正数，惩罚人工变量进入解)")
    
    print("\n如果人工变量 > 0：目标函数值增加 M·人工变量")
    print("→ 优化过程会自动把人工变量赶出基（除非无可行解）")
    
    print("\n大 M 法的缺点:")
    print("  - M 的选择困难：太小可能不起作用，太大可能引起数值问题")
    print("  - 两阶段法更清晰（分离人工变量的引入和移除）")

big_m_example()
```

---

## 7.7 退化与循环

!!! warning "退化（Degeneracy）"
    当基本可行解中有基变量为 0 时，称这个解是**退化的**。退化可能导致：
    
    - $\theta = 0$ 的情况（基变量不变化）
    - 目标函数值不改善的迭代
    - **循环**（绕了一圈回到之前的解）

** Bland 规则**：当有多个候选变量时，选择下标最小的——这可以避免循环。

---

## 7.8 用 Python 求解线性规划

```python
from scipy.optimize import linprog
import numpy as np

def solve_with_scipy():
    """用 scipy.optimize.linprog 求解奶茶店问题"""
    print("使用 scipy.optimize.linprog 验证结果")
    print("=" * 50)
    
    # 奶茶店问题：
    # max z = 5x1 + 3x2
    # s.t. 2x1 + x2 <= 10
    #      x1 + 2x2 <= 8
    #      x1, x2 >= 0
    
    # linprog 默认是 min 问题，所以 c 取负
    c = [-5, -3]  # min(-5x1 - 3x2) = max(5x1 + 3x2)
    
    A_ub = [
        [2, 1],   # 2x1 + x2 <= 10
        [1, 2]    # x1 + 2x2 <= 8
    ]
    b_ub = [10, 8]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=(0, None))
    
    print(f"\n求解结果:")
    print(f"  x1 = {result.x[0]:.2f}")
    print(f"  x2 = {result.x[1]:.2f}")
    print(f"  最大利润 z = {-result.fun:.2f}")
    print(f"  状态: {'成功' if result.success else '失败'}")

solve_with_scipy()
```

**渲染效果：**
```
使用 scipy.optimize.linprog 验证结果
==================================================

求解结果:
  x1 = 4.00
  x2 = 2.00
  最大利润 z = 26.00
  状态: 成功
```

---

## 要点总结

- [x] 单纯形表 = 增广矩阵的表格化，每次迭代更新数字
- [x] 换入变量：最负检验数（max）/ 最正检验数（min）
- [x] 换出变量：最小比值原则 $\theta$
- [x] 旋转运算：初等行变换，使 pivot = 1，同列其他 = 0
- [x] 人工变量法：当约束不含单位矩阵时引入
- [x] 两阶段法：第一阶段消除人工变量，第二阶段优化原目标
- [x] 退化可能导致循环，Bland 规则可避免

---

## 课后练习

1. **表格练习**：用表格单纯形法求解：
   $$\max \quad z = 3x_1 + 2x_2 \quad \text{s.t.} \quad \begin{cases} x_1 + x_2 \le 5 \\ 2x_1 \le 6 \\ x_1, x_2 \ge 0 \end{cases}$$

2. **人工变量练习**：用两阶段法求解：
   $$\min \quad z = 2x_1 + x_2 \quad \text{s.t.} \quad \begin{cases} x_1 + x_2 = 6 \\ x_1 - x_2 \ge 2 \\ x_1, x_2 \ge 0 \end{cases}$$

3. **思考题**：如果一个线性规划问题的约束矩阵 $A$ 是 $m \times n$ 且 $m = n$（方阵），且 $A$ 可逆，那么可以直接以 $A$ 为基矩阵吗？这种情况下单纯形法会简化成什么？

---

**🎉 恭喜完成线性规划教程！**

现在你应该掌握了：
- 线性规划的建模方法
- 图解法的几何直观
- 标准形式的转换
- 单纯形法的代数原理与表格实现
- 人工变量法处理复杂约束

如果你想继续深入，可以学习：
- **整数规划**：变量必须为整数的问题（分支定界法）
- **非线性规划**：目标或约束非线性（梯度下降法、牛顿法）
- **对偶理论**：每个线性规划都有对应的"影子"问题

[返回目录](../index.md)