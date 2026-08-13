# 第 3 章：自动化你的工作

> **场景：** 导师给了你 50 组实验数据文件，每组都要做同样的分析和绘图。手动处理会疯掉的——让我们用函数和流程控制来自动化这一切。

---

## 3.1 编写函数：封装可复用的逻辑

把弹簧分析逻辑封装成函数 `analyze_spring.m`：

```matlab
function [k_mean, k_std, R2] = analyze_spring(F, x, plotFlag)
% analyze_spring  分析弹簧实验数据
%   输入：
%     F - 拉力数据向量
%     x - 伸长量数据向量
%     plotFlag - 是否绘图（true/false）
%   输出：
%     k_mean - 弹性系数均值
%     k_std  - 弹性系数标准差
%     R2     - 拟合优度

    if nargin < 3
        plotFlag = false;        % 默认不绘图
    end

    % 线性拟合
    p = polyfit(F, x, 1);

    % 计算弹性系数
    k = F(2:end) ./ x(2:end);
    k_mean = mean(k);
    k_std = std(k);

    % 拟合优度
    x_pred = polyval(p, F);
    R2 = 1 - sum((x - x_pred).^2) / sum((x - mean(x)).^2);

    % 可选绘图
    if plotFlag
        figure;
        plot(F, x, 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r');
        hold on;
        F_fit = linspace(min(F), max(F), 100);
        plot(F_fit, polyval(p, F_fit), 'b-', 'LineWidth', 2);
        xlabel('拉力 F (N)');
        ylabel('伸长量 x (cm)');
        title(sprintf('k = %.3f ± %.3f N/cm, R^2 = %.4f', k_mean, k_std, R2));
        legend('数据', '拟合');
        grid on;
    end
end
```

**使用方式：**

```matlab
% 调用函数
F = [0, 1, 2, 3, 4, 5];
x = [0, 1.2, 2.3, 3.5, 4.6, 5.8];
[k_mean, k_std, R2] = analyze_spring(F, x, true);
```

**输出效果：** 命令窗口返回三个计算结果，同时弹出图形窗口显示数据和拟合线。

---

## 3.2 流程控制

### 条件判断

```matlab
score = 85;

if score >= 90
    grade = 'A';
elseif score >= 80
    grade = 'B';
elseif score >= 70
    grade = 'C';
elseif score >= 60
    grade = 'D';
else
    grade = 'F';
end

fprintf('成绩等级：%s\n', grade);
```

**输出效果：** `成绩等级：B`

### for 循环

```matlab
% 计算斐波那契数列前 20 项
n = 20;
fib = zeros(1, n);
fib(1) = 1;
fib(2) = 1;

for i = 3:n
    fib(i) = fib(i-1) + fib(i-2);
end

disp(fib);
```

**输出效果：** 命令窗口显示 `1 1 2 3 5 8 13 21 34 55 ...`

### while 循环

```matlab
% 找到第一个大于 1000 的 2 的幂
n = 1;
while 2^n <= 1000
    n = n + 1;
end
fprintf('2^%d = %d > 1000\n', n, 2^n);
```

**输出效果：** `2^10 = 1024 > 1000`

---

## 3.3 向量化：MATLAB 的效率秘诀

MATLAB 中，向量化代码比循环快得多：

```matlab
n = 1000000;

% 慢：使用循环
tic;
result1 = zeros(1, n);
for i = 1:n
    result1(i) = sin(i) * cos(i);
end
t_loop = toc;

% 快：向量化
tic;
i = 1:n;
result2 = sin(i) .* cos(i);
t_vec = toc;

fprintf('循环耗时：%.4f 秒\n', t_loop);
fprintf('向量化耗时：%.4f 秒\n', t_vec);
fprintf('加速比：%.1f 倍\n', t_loop / t_vec);
```

**输出效果：** 向量化通常比循环快 10~100 倍。`tic`/`toc` 用于计时。

---

## 3.4 文件读写

### 读取 CSV 数据

```matlab
% 读取 CSV 文件
data = readmatrix('experiment_data.csv');

% 或使用 readtable（保留列名）
T = readtable('experiment_data.csv');
F = T.Force;     % 按列名访问
x = T.Elongation;
```

### 写入结果

```matlab
% 保存结果到文本文件
results = table(F', x', k', 'VariableNames', {'Force', 'Elongation', 'k'});
writetable(results, 'spring_results.csv');

% 保存 MATLAB 数据格式
save('spring_analysis.mat', 'F', 'x', 'k_mean', 'k_std');
```

---

## 3.5 批量处理多组数据

现在处理 50 组实验数据：

```matlab
% batch_analysis.m —— 批量分析弹簧实验数据
clear; clc;

% 存储所有结果
all_results = table();

for i = 1:50
    % 读取第 i 组数据
    filename = sprintf('data/experiment_%02d.csv', i);

    if ~exist(filename, 'file')
        fprintf('文件 %s 不存在，跳过\n', filename);
        continue;
    end

    T = readtable(filename);
    F = T.Force;
    x = T.Elongation;

    % 调用分析函数
    [k_mean, k_std, R2] = analyze_spring(F, x, false);

    % 保存结果
    all_results.Group(i) = i;
    all_results.k_mean(i) = k_mean;
    all_results.k_std(i) = k_std;
    all_results.R2(i) = R2;

    fprintf('第 %d 组：k = %.3f ± %.3f, R² = %.4f\n', i, k_mean, k_std, R2);
end

% 保存汇总结果
writetable(all_results, 'batch_results.csv');

% 绘制汇总图
figure;
subplot(1, 3, 1);
histogram(all_results.k_mean);
xlabel('弹性系数 k (N/cm)');
ylabel('频次');
title('弹性系数分布');

subplot(1, 3, 2);
plot(all_results.k_mean, all_results.k_std, 'o');
xlabel('弹性系数均值');
ylabel('标准差');
title('均值 vs 标准差');
grid on;

subplot(1, 3, 3);
histogram(all_results.R2);
xlabel('拟合优度 R²');
ylabel('频次');
title('拟合优度分布');

fprintf('\n========== 汇总 ==========\n');
fprintf('共处理 %d 组数据\n', i);
fprintf('弹性系数总均值：%.4f N/cm\n', mean(all_results.k_mean));
fprintf('平均拟合优度：%.4f\n', mean(all_results.R2));
```

**输出效果：** 命令窗口逐行显示每组数据的处理结果，最后输出汇总统计。图形窗口显示三个子图：弹性系数分布直方图、均值-标准差散点图、拟合优度分布直方图。

---

## 3.6 调试技巧

```matlab
% 设置断点：点击行号左侧的横杠
% 调试命令
dbstop if error     % 出错时自动停在出错行
dbclear all         % 清除所有断点

% 在命令窗口查看变量
% 在断点处，命令窗口可以访问所有局部变量

% 常用调试操作
% F10 - 单步执行（不进入函数）
% F11 - 单步执行（进入函数）
% F5  - 继续运行到下一个断点
```

---

## 本章回顾

你现在可以自动化处理大规模数据了！回顾掌握的技能：

- [x] 编写函数封装可复用逻辑
- [x] 使用 `if-elseif-else` 条件判断
- [x] 使用 `for` 和 `while` 循环
- [x] 理解向量化编程的性能优势
- [x] 用 `readmatrix`/`readtable` 读取数据文件
- [x] 用 `writetable`/`save` 保存结果
- [x] 批量处理多组数据文件

---

👉 [进入第 4 章：完成数据分析项目 →](04-practice.md)