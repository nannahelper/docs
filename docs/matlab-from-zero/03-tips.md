# 第 3 章：常用技巧

> **数据可视化与文件操作** —— 用 MATLAB 绘制专业图表，读写各种格式的数据文件。

---

## 3.1 二维绘图

```matlab
x = linspace(0, 2*pi, 100);

% 基本线图
figure(1);
plot(x, sin(x), 'b-', 'LineWidth', 2);    % 蓝色实线
hold on;
plot(x, cos(x), 'r--', 'LineWidth', 2);   % 红色虚线
hold off;

% 图形美化
xlabel('x (弧度)', 'FontSize', 12);
ylabel('函数值', 'FontSize', 12);
title('正弦与余弦函数', 'FontSize', 14);
legend('sin(x)', 'cos(x)', 'Location', 'northwest');
grid on;
axis([0 2*pi -1.5 1.5]);    % 设置坐标轴范围

% 散点图
figure(2);
x = randn(100, 1);
y = randn(100, 1);
scatter(x, y, 50, 'filled');    % 大小为 50，实心
xlabel('X');
ylabel('Y');
title('随机散点图');
```

**渲染效果：** 图形窗口 1 显示两条曲线，蓝色实线为正弦、红色虚线为余弦，有完整的标签和图例。图形窗口 2 显示实心散点图。

**代码解读：**

- `'b-'` 表示蓝色（b）实线（-），`'r--'` 表示红色（r）虚线（--）
- `hold on` 保持当前图形，使后续绘图叠加在同一图上
- `axis([xmin xmax ymin ymax])` 精确控制坐标轴范围

## 3.2 子图与多图

```matlab
figure(3);

% 2×2 子图布局
subplot(2, 2, 1);
plot(x, sin(x));
title('sin(x)');

subplot(2, 2, 2);
plot(x, cos(x));
title('cos(x)');

subplot(2, 2, 3);
plot(x, sin(2*x));
title('sin(2x)');

subplot(2, 2, 4);
plot(x, cos(2*x));
title('cos(2x)');
```

**渲染效果：** 一个图形窗口中排列 4 个子图（2 行 2 列），每个子图有独立的坐标轴和标题。

## 3.3 三维绘图

```matlab
% 三维曲面
[X, Y] = meshgrid(-2:0.1:2, -2:0.1:2);
Z = X .* exp(-X.^2 - Y.^2);

figure(4);
surf(X, Y, Z);              % 曲面图
xlabel('X');
ylabel('Y');
zlabel('Z');
title('三维曲面：z = x·e^{-x^2-y^2}');
colormap('jet');            % 设置颜色映射
colorbar;                   % 显示颜色条

% 等高线图
figure(5);
contour(X, Y, Z, 20);       % 20 条等高线
xlabel('X');
ylabel('Y');
title('等高线图');
colorbar;
```

**渲染效果：** 曲面图以彩色三维表面展示函数形态，可旋转视角观察。等高线图以二维方式展示三维曲面的"海拔"信息。

## 3.4 文件读写

```matlab
% 读取 CSV 文件
data = readtable('data.csv');       % 读取为 table 类型
disp(data(1:5, :));                 % 显示前 5 行

% 读取 Excel 文件
data = readtable('data.xlsx', 'Sheet', 'Sheet1');

% 写入 CSV
writetable(data, 'output.csv');

% 读取文本文件
fid = fopen('text.txt', 'r');
content = fread(fid, '*char')';     % 读取全部内容
fclose(fid);

% 写入文本文件
fid = fopen('output.txt', 'w');
fprintf(fid, 'Hello, MATLAB!\n');
fprintf(fid, '计算结果：%f\n', pi);
fclose(fid);

% 保存和加载 MATLAB 数据
save('workspace.mat');              % 保存整个工作区
save('data.mat', 'A', 'B');         % 保存指定变量
load('data.mat');                   % 加载数据
```

## 3.5 数据分析基础

```matlab
data = randn(1000, 1);    % 1000 个正态分布随机数

% 描述性统计
mean(data)                % 均值
median(data)              % 中位数
std(data)                 % 标准差
var(data)                 % 方差
min(data)                 % 最小值
max(data)                 % 最大值

% 直方图
figure(6);
histogram(data, 30);      % 30 个区间
xlabel('数值');
ylabel('频数');
title('数据分布直方图');

% 曲线拟合
x = linspace(0, 10, 50);
y = 2*x + 1 + randn(1, 50);    % 带噪声的线性数据
p = polyfit(x, y, 1);           % 一次多项式拟合
y_fit = polyval(p, x);          % 计算拟合值

figure(7);
plot(x, y, 'o');                % 原始数据点
hold on;
plot(x, y_fit, 'r-', 'LineWidth', 2);  % 拟合直线
legend('原始数据', '拟合直线');
title('线性拟合');
```

**渲染效果：** 直方图展示数据分布形态；拟合图显示原始散点和最佳拟合直线。

---

## 本章要点总结

- [ ] 掌握 `plot`、`scatter` 等二维绘图函数
- [ ] 会用 `subplot` 创建多子图布局
- [ ] 了解 `surf`、`contour` 三维绘图
- [ ] 掌握 `readtable`、`writetable` 文件读写
- [ ] 了解 `polyfit` 曲线拟合

---

👉 [进入第 4 章：实战案例 →](04-practice.md)