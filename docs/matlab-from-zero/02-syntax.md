# 第 2 章：让数据说话

> **场景：** 你的实验数据已经算好了，但导师说"光有数字不够，画张图看看趋势"。MATLAB 的可视化能力正是它的王牌——让我们把枯燥的数据变成直观的图表。

---

## 2.1 绘制弹簧实验数据图

继续上一章的弹簧实验，把数据画出来：

```matlab
% 实验数据
F = [0, 1, 2, 3, 4, 5];
x = [0, 1.2, 2.3, 3.5, 4.6, 5.8];

% 绘制散点图
figure;                          % 创建新图窗
plot(F, x, 'ro', ...             % 红色圆圈标记
     'MarkerSize', 8, ...        % 标记大小
     'MarkerFaceColor', 'r');    % 填充颜色
hold on;                         % 保持图形，叠加新内容

% 线性拟合
p = polyfit(F, x, 1);            % 一次多项式拟合
F_fit = linspace(0, 5, 100);
x_fit = polyval(p, F_fit);
plot(F_fit, x_fit, 'b-', 'LineWidth', 2);

% 标注
xlabel('拉力 F (N)');
ylabel('伸长量 x (cm)');
title('弹簧伸长量与拉力的关系');
legend('实验数据', '线性拟合', 'Location', 'northwest');
grid on;

% 显示拟合方程
fprintf('拟合方程：x = %.4f F + %.4f\n', p(1), p(2));
```

**渲染效果：** 生成一个图形窗口，红色实心圆点表示实验数据，蓝色实线表示拟合直线。坐标轴带标签，标题在顶部，图例在左上角，背景有网格线。拟合方程显示在命令窗口。

---

## 2.2 绘图基础：`plot` 函数

```matlab
x = linspace(0, 2*pi, 100);

plot(x, sin(x));                 % 默认蓝色实线
plot(x, sin(x), 'r--');          % 红色虚线
plot(x, sin(x), 'g:');           % 绿色点线
plot(x, sin(x), 'k-.');          % 黑色点划线
plot(x, sin(x), 'mo');           % 品红色圆圈（无连线）
```

**渲染效果：** 不同颜色和线型组合产生不同视觉效果。颜色字符：`r`红 `g`绿 `b`蓝 `k`黑 `m`品红 `c`青 `y`黄。线型字符：`-`实线 `--`虚线 `:`点线 `-.`点划线 `o`圆圈。

---

## 2.3 多图布局：`subplot`

```matlab
x = linspace(0, 2*pi, 100);

figure;

subplot(2, 2, 1);                % 2行2列，第1个
plot(x, sin(x));
title('sin(x)');
grid on;

subplot(2, 2, 2);                % 第2个
plot(x, cos(x));
title('cos(x)');
grid on;

subplot(2, 2, 3);                % 第3个
plot(x, tan(x));
title('tan(x)');
ylim([-5, 5]);                   % 限制 y 轴范围
grid on;

subplot(2, 2, 4);                % 第4个
plot(x, sin(x), 'b-', x, cos(x), 'r--');
title('sin 与 cos 对比');
legend('sin', 'cos');
grid on;
```

**渲染效果：** 一个图窗中排列 2×2 共 4 个子图，每个子图独立设置标题、坐标轴和图例。`tan(x)` 的 y 轴被限制在 [-5, 5] 避免无穷大。

---

## 2.4 更多图表类型

### 柱状图

```matlab
methods = {'方法A', '方法B', '方法C', '方法D'};
accuracy = [92.1, 94.5, 96.8, 91.3];

figure;
bar(accuracy);
set(gca, 'XTickLabel', methods);
xlabel('方法');
ylabel('准确率 (%)');
title('不同方法的分类准确率对比');
grid on;
```

**渲染效果：** 蓝色柱状图，x 轴显示方法名称，y 轴显示准确率百分比，柱高直观反映性能差异。

### 饼图

```matlab
categories = {'房租', '餐饮', '交通', '娱乐', '其他'};
expenses = [2500, 1800, 500, 800, 400];

figure;
pie(expenses, categories);
title('月度支出分布');
```

**渲染效果：** 彩色饼图，每个扇区标注类别名称和百分比，直观展示支出结构。

### 三维曲面图

```matlab
[X, Y] = meshgrid(-2:0.1:2, -2:0.1:2);
Z = X .* exp(-X.^2 - Y.^2);

figure;
surf(X, Y, Z);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('三维曲面：z = x·e^{-x^2-y^2}');
colorbar;                        % 添加颜色条
```

**渲染效果：** 彩色三维曲面，颜色表示 Z 值高度，右侧有颜色条映射数值到颜色，可旋转视角观察。

---

## 2.5 图形美化

```matlab
x = linspace(0, 10, 100);
y = sin(x) .* exp(-0.2 * x);

figure;
plot(x, y, 'LineWidth', 2, 'Color', [0.2, 0.6, 0.8]);

% 标题和标签
title('阻尼振荡', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('时间 t (s)', 'FontSize', 12);
ylabel('振幅', 'FontSize', 12);

% 坐标轴设置
xlim([0, 10]);
ylim([-1, 1]);
grid on;

% 添加文本注释
text(5, 0.5, '\leftarrow 峰值', 'FontSize', 10);

% 保存图片
saveas(gcf, 'damped_oscillation.png');
```

**渲染效果：** 图形具有自定义颜色（RGB 三元组）、加粗标题、坐标轴范围限制、文本注释和网格线。`saveas` 将图形保存为 PNG 文件。

---

## 2.6 完善弹簧实验报告

把数据分析和可视化整合到一个脚本中：

```matlab
% spring_report.m —— 弹簧实验完整分析
clear; clc; close all;

% 实验数据
F = [0, 1, 2, 3, 4, 5];
x = [0, 1.2, 2.3, 3.5, 4.6, 5.8];

% 线性拟合
p = polyfit(F, x, 1);
F_fit = linspace(0, 5, 100);
x_fit = polyval(p, F_fit);

% 计算弹性系数
k = F(2:end) ./ x(2:end);
k_mean = mean(k);
k_std = std(k);

% 绘制结果
figure('Position', [100, 100, 800, 400]);

subplot(1, 2, 1);
plot(F, x, 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r');
hold on;
plot(F_fit, x_fit, 'b-', 'LineWidth', 2);
xlabel('拉力 F (N)');
ylabel('伸长量 x (cm)');
title('胡克定律验证');
legend('实验数据', sprintf('拟合: x = %.3fF + %.3f', p(1), p(2)), ...
       'Location', 'northwest');
grid on;

subplot(1, 2, 2);
bar(k);
hold on;
yline(k_mean, 'r--', 'LineWidth', 1.5);
xlabel('数据点');
ylabel('弹性系数 k (N/cm)');
title(sprintf('弹性系数分布 (均值=%.3f, 标准差=%.3f)', k_mean, k_std));
grid on;

% 输出结论
fprintf('========== 实验结论 ==========\n');
fprintf('弹性系数 k = %.3f ± %.3f N/cm\n', k_mean, k_std);
fprintf('拟合优度 R^2 = %.4f\n', 1 - sum((x - polyval(p, F)).^2) / sum((x - mean(x)).^2));
```

**渲染效果：** 一个图窗包含两个子图：左侧是散点图+拟合线，右侧是弹性系数柱状图+均值线。命令窗口输出实验结论。

---

## 本章回顾

你的实验数据现在有了直观的可视化呈现！回顾掌握的技能：

- [x] 用 `plot` 绘制二维曲线，控制颜色、线型和标记
- [x] 用 `subplot` 创建多图布局
- [x] 用 `bar`、`pie`、`surf` 创建柱状图、饼图和三维曲面
- [x] 添加标题、标签、图例和网格线
- [x] 用 `xlim`/`ylim` 控制坐标轴范围
- [x] 用 `saveas` 导出图片

---

👉 [进入第 3 章：自动化你的工作 →](03-tips.md)