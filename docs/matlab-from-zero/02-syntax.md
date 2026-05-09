# 第 2 章：核心语法

> **MATLAB 的灵魂：矩阵运算** —— 脚本、函数、流程控制，构建程序的四大要素。

---

## 2.1 矩阵与数组

MATLAB 中一切皆矩阵。标量是 1×1 的矩阵，向量是 1×n 或 n×1 的矩阵。

```matlab
% 创建矩阵
A = [1 2 3; 4 5 6; 7 8 9];    % 分号分隔行，空格或逗号分隔列
v = [1, 2, 3, 4, 5];           % 行向量
w = [1; 2; 3];                  % 列向量

% 特殊矩阵
zeros(3, 4)       % 3×4 全零矩阵
ones(2, 3)        % 2×3 全一矩阵
eye(4)            % 4×4 单位矩阵
rand(3)           % 3×3 随机矩阵（0~1 均匀分布）
randn(3)          % 3×3 随机矩阵（标准正态分布）

% 生成序列
1:10              % 1 到 10，步长为 1
1:2:10            % 1, 3, 5, 7, 9（步长为 2）
linspace(0, 1, 5) % 0 到 1 的 5 个等分点
```

**运行效果：** 矩阵在命令窗口中以行列格式整齐显示。`zeros`、`ones`、`eye` 是初始化矩阵的常用函数。

## 2.2 矩阵运算

```matlab
A = [1 2; 3 4];
B = [5 6; 7 8];

% 基本运算
A + B            % 矩阵加法
A * B            % 矩阵乘法（线性代数）
A .* B           % 逐元素乘法（点运算）
A^2              % 矩阵幂（A * A）
A.^2             % 逐元素幂
A'               % 转置

% 矩阵函数
det(A)           % 行列式
inv(A)           % 逆矩阵
eig(A)           % 特征值和特征向量
rank(A)          % 秩
size(A)          % 矩阵大小 → [3, 3]
length(v)        % 向量长度

% 索引（MATLAB 索引从 1 开始）
A(2, 1)          % 第 2 行第 1 列 → 3
A(1, :)          % 第 1 行全部
A(:, 2)          % 第 2 列全部
A(1:2, 2:3)      % 第 1~2 行，第 2~3 列的子矩阵
A(end, :)        % 最后一行
```

**运行效果：** 矩阵运算遵循线性代数规则。点运算（`.*`、`.^`）是 MATLAB 的特色——对矩阵的每个元素独立执行运算。

## 2.3 流程控制

```matlab
% if-elseif-else
score = 85;
if score >= 90
    grade = 'A';
elseif score >= 80
    grade = 'B';
elseif score >= 70
    grade = 'C';
else
    grade = 'D';
end
fprintf('成绩等级：%s\n', grade);

% for 循环
sum = 0;
for i = 1:100
    sum = sum + i;
end
fprintf('1 到 100 的和：%d\n', sum);

% while 循环
n = 1;
while n^2 < 1000
    n = n + 1;
end
fprintf('第一个平方超过 1000 的整数：%d\n', n);

% switch-case
day = 3;
switch day
    case 1
        disp('星期一');
    case 2
        disp('星期二');
    case {3, 4, 5}
        disp('工作日');
    otherwise
        disp('周末');
end
```

**运行效果：** 流程控制语法与大多数编程语言类似，但注意每个块必须以 `end` 结尾。

## 2.4 函数定义

```matlab
% 方式一：独立函数文件（calculate_stats.m）
function [mean_val, std_val] = calculate_stats(data)
    % 计算数据的均值和标准差
    mean_val = mean(data);
    std_val = std(data);
end

% 方式二：匿名函数
square = @(x) x^2;
square(5)        % → 25

% 方式三：脚本中的局部函数（MATLAB R2016b+）
% 在脚本末尾定义函数
result = my_add(3, 5);
disp(result);

function c = my_add(a, b)
    c = a + b;
end
```

**运行效果：** 函数文件（`.m`）的文件名必须与函数名一致。匿名函数适合简单的单行函数。

---

## 本章要点总结

- [ ] 掌握矩阵的创建（`[]`、`zeros`、`ones`、`eye`）
- [ ] 理解矩阵运算（`*`）与逐元素运算（`.*`）的区别
- [ ] 熟练使用矩阵索引（`()`、`:`、`end`）
- [ ] 掌握 if-else、for、while 流程控制
- [ ] 能定义函数文件和匿名函数

---

👉 [进入第 3 章：常用技巧 →](03-tips.md)