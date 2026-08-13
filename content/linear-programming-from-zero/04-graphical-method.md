# 第 4 章：图解法 —— 在坐标系中找到最优解

>  **场景：** 第 3 章我们把奶茶店问题列成了数学模型。现在让我们用 **画图** 的方法来求解。当只有两个变量时，图解法是最直观的方法——把约束条件画成区域，把目标函数画成等值线，然后在可行域中找到最佳位置。

---

## 4.1 图解法的核心思想

!!! example "核心比喻：地图找峰"
    想象你在一片山区（可行域）里，要找到最高点（最优解）。你看不见整片地形，但你有一条指向山顶方向的指南针（目标函数梯度）。图解法就是：
    
    1. 在地图上圈出你能去的区域（可行域）
    2. 沿着指南针方向移动，直到无法再升高（等值线平移）
    3. 停下的位置就是最高点（最优解）

---

## 4.2 图解法的步骤

### 步骤 1：建立坐标系

以决策变量为坐标轴：
- $x_1$ 轴：横坐标
- $x_2$ 轴：纵坐标

### 步骤 2：画出可行域

每个线性约束条件在图上对应一条直线，直线的一侧满足约束。

```python
import numpy as np
import matplotlib.pyplot as plt

# 奶茶店问题的约束：
# 2x1 + x2 <= 10  (牛奶约束)
# x1 + 2x2 <= 8   (茶叶约束)
# x1 >= 0, x2 >= 0

fig, ax = plt.subplots(figsize=(8, 8))

x1 = np.linspace(0, 12, 100)

# 约束1: 2x1 + x2 <= 10 → x2 <= 10 - 2x1
x2_1 = 10 - 2 * x1
ax.fill_between(x1, 0, np.minimum(x2_1, 12), alpha=0.2, color='blue', label='可行域')

# 约束2: x1 + 2x2 <= 8 → x2 <= (8 - x1) / 2
x2_2 = (8 - x1) / 2
ax.fill_between(x1, 0, np.minimum(x2_2, 12), alpha=0.1, color='green')

# 坐标轴
ax.axhline(y=0, color='black', linewidth=0.5)
ax.axvline(x=0, color='black', linewidth=0.5)

# 约束线
ax.plot(x1, x2_1, 'b-', linewidth=2, label=r'$2x_1 + x_2 \leq 10$')
ax.plot(x1, x2_2, 'g-', linewidth=2, label=r'$x_1 + 2x_2 \leq 8$')

ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.set_xlabel(r'$x_1$ (A 奶茶数量)', fontsize=12)
ax.set_ylabel(r'$x_2$ (B 奶茶数量)', fontsize=12)
ax.set_title('线性规划可行域（阴影区域）', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

 **渲染效果：** 生成一张坐标系图，显示两条约束线及其围成的可行域（阴影区域）。

---

## 4.3 目标函数的等值线

目标函数 $z = 5x_1 + 3x_2$ 在图上是一簇平行线：

$5x_1 + 3x_2 = z$

当 $z$ 取不同值时，这些直线互相平行。

```python
# 目标函数等值线：z = 5x1 + 3x2
fig, ax = plt.subplots(figsize=(8, 8))

x1 = np.linspace(0, 12, 100)

# 画出不同 z 值对应的等值线
for z in [5, 10, 15, 20, 25, 30]:
    x2 = (z - 5 * x1) / 3
    valid = x2 >= 0
    ax.plot(x1[valid], x2[valid], '--', linewidth=1.5, alpha=0.7)
    ax.text(x1[valid][-1] + 0.1, x2[valid][-1], f'z={z}', fontsize=9)

# 可行域
ax.fill_between(x1, 0, np.minimum(10 - 2*x1, (8 - x1)/2), alpha=0.15, color='blue')

# 约束线
ax.plot(x1, 10 - 2*x1, 'b-', linewidth=2)
ax.plot(x1, (8 - x1)/2, 'g-', linewidth=2)
ax.axhline(y=0, color='black', linewidth=0.5)
ax.axvline(x=0, color='black', linewidth=0.5)

ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.set_xlabel(r'$x_1$', fontsize=12)
ax.set_ylabel(r'$x_2$', fontsize=12)
ax.set_title(r'目标函数等值线 $z = 5x_1 + 3x_2$（虚线）', fontsize=14)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

 **渲染效果：** 显示一簇平行等值线穿过可行域，$z$ 值越大，直线越往右上方向移动。

---

## 4.4 确定最优解

最优解在 **等值线与可行域边界相切** 的位置。

```python
def solve_graphically():
    """
    图解法求解奶茶店问题
    max z = 5x1 + 3x2
    s.t. 2x1 + x2 <= 10
         x1 + 2x2 <= 8
         x1, x2 >= 0
    """
    # 可行域的顶点（极点）
    vertices = [
        (0, 0),      # 原点
        (5, 0),      # 2x1=10, x2=0
        (0, 4),      # x1=0, x2=4（茶叶线截距）
        (4, 2),      # 2x1+x2=10 且 x1+2x2=8 的交点
    ]
    
    # 检查每个顶点是否可行
    print("可行域顶点分析:")
    print("=" * 50)
    
    best_z = -float('inf')
    best_vertex = None
    
    for (x1, x2) in vertices:
        # 检查约束
        c1 = 2*x1 + x2 <= 10 + 1e-10
        c2 = x1 + 2*x2 <= 8 + 1e-10
        
        if c1 and c2:
            z = 5*x1 + 3*x2
            print(f"顶点 ({x1}, {x2}): z = 5×{x1} + 3×{x2} = {z:.2f} ✓")
            
            if z > best_z:
                best_z = z
                best_vertex = (x1, x2)
        else:
            print(f"顶点 ({x1}, {x2}): 不可行 ✗")
    
    print(f"\n最优解: x1 = {best_vertex[0]}, x2 = {best_vertex[1]}")
    print(f"最大利润: z = {best_z:.2f}")
    
    return best_vertex, best_z

vertex, z_opt = solve_graphically()
```

 **渲染效果：**
```
可行域顶点分析:
==================================================
顶点 (0, 0): z = 0.00 ✓
顶点 (5, 0): z = 25.00 ✓
顶点 (0, 4): z = 12.00 ✓
顶点 (4, 2): z = 26.00 ✓

最优解: x1 = 4, x2 = 2
最大利润: z = 26.00
```

---

## 4.4 四种解的分类

用图解法可以直观看到线性规划的四类解：

### 类型 1：唯一最优解

等值线与可行域边界恰好相交于一点。

```python
def plot_unique_optimal():
    """唯一最优解"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x1 = np.linspace(0, 6, 100)
    
    # 可行域
    ax.fill_between(x1, 0, np.minimum(10-2*x1, (8-x1)/2), alpha=0.15, color='blue')
    
    # 约束线
    ax.plot(x1, 10-2*x1, 'b-', lw=2)
    ax.plot(x1, (8-x1)/2, 'g-', lw=2)
    ax.axhline(y=0, color='k', lw=0.5)
    ax.axvline(x=0, color='k', lw=0.5)
    
    # 最优等值线（刚好通过 (4,2)）
    x2_best = (26 - 5*x1) / 3
    ax.plot(x1, x2_best, 'r--', lw=2.5, label=r'$z = 26$ (最优)')
    
    ax.scatter([4], [2], color='red', s=200, zorder=5, marker='*', label='最优解 (4, 2)')
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_xlabel(r'$x_1$')
    ax.set_ylabel(r'$x_2$')
    ax.set_title('唯一最优解 (4, 2), z = 26')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

plot_unique_optimal()
```

 **渲染效果：** 红色虚线（最优等值线）恰好通过点 (4, 2)，该店每天卖 4 杯 A 奶茶和 2 杯 B 奶茶，利润 26 元。

### 类型 2：无穷多最优解

当目标函数等值线与可行域的一条边界平行时，整条边界都是最优解。

```python
def plot_multiple_optimal():
    """无穷多最优解"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x1 = np.linspace(0, 8, 100)
    
    # 可行域
    ax.fill_between(x1, 0, np.minimum(8-x1, 8-2*x1), alpha=0.15, color='blue')
    
    # 约束线
    ax.plot(x1, 8-x1, 'b-', lw=2, label=r'$x_1 + x_2 = 8$')
    ax.plot(x1, 8-2*x1, 'g-', lw=2, label=r'$2x_1 + x_2 = 8$')
    ax.axhline(y=0, color='k', lw=0.5)
    ax.axvline(x=0, color='k', lw=0.5)
    
    # 目标函数 z = 4x1 + 4x2 与上边界平行！
    x2_best = (32 - 4*x1) / 4
    ax.plot(x1, x2_best, 'r--', lw=2.5, label=r'$z = 32$ (最优等值线)')
    
    # 标记整条最优边界
    ax.plot([0, 4], [8, 0], 'r-', lw=4, alpha=0.3, label='无穷多最优解')
    
    ax.scatter([0, 4], [8, 0], color='red', s=100, zorder=5)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 9)
    ax.set_xlabel(r'$x_1$')
    ax.set_ylabel(r'$x_2$')
    ax.set_title(r'无穷多最优解：$z = 4x_1 + 4x_2 = 32$（沿整个上边界）')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

plot_multiple_optimal()
```

 **渲染效果：** 最优等值线与可行域上边界平行，整条线段（从 (0,8) 到 (4,0)）上的所有点都是最优解。

### 类型 3：无界解

可行域向某个方向无限延伸，目标函数可以无限增大（或减小）。

### 类型 4：无可行解

约束条件相互矛盾，可行域为空集。

!!! tip "图解法的局限"
    图解法只能处理两个变量的问题。当变量增加到三个或更多时，我们需要 **单纯形法** ——一种能够处理任意维度问题的代数方法。

---

## 要点总结

- [x] 图解法核心：可行域（阴影区域）+ 等值线（平行线簇）
- [x] 最优解 = 等值线与可行域边界相切的位置
- [x] 最优解必定在可行域的  **顶点** （极点）上
- [x] 四类解：唯一最优、无穷多最优、无界解、无可行解
- [x] 图解法只适用于 2-3 个变量，更多变量需要单纯形法

---

## 课后练习

1.  **手算练习** ：用图解法求解以下问题：
   $\max \quad z = 4x_1 + 3x_2$

   约束条件：
   
   $x_1 + x_2 \le 6$
   
   $2x_1 + 3x_2 \le 15$
   
   $x_1, x_2 \ge 0$

2.  **分类练习** ：分析以下线性规划问题属于哪类解：
   - 可行域无界向右上延伸
   - 约束条件为 $x_1 + x_2 \le 1$ 和 $2x_1 + 2x_2 \ge 5$

3.  **思考题** ：如果目标函数是 $z = x_1 + x_2$ 而非 $z = 5x_1 + 3x_2$，最优解会变化吗？最优值呢？

---

 **下一章预告：** 图解法告诉我们最优解在顶点，但代数上如何系统地找到所有顶点？第 5 章将介绍 **标准形式** ——一种所有线性规划问题都可以转换成的统一格式，以及灵敏度分析。

[继续第 5 章：标准形式与灵敏度分析 →](05-standard-form-sensitivity.md)