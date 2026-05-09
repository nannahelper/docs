# 第 4 章：实战案例

> **综合实战** —— 信号处理、图像处理和数值分析三个经典案例。

---

## 4.1 案例一：信号处理 —— 音频频谱分析

```matlab
% 生成一个复合信号
fs = 1000;                    % 采样频率 1000 Hz
t = 0:1/fs:1;                 % 1 秒的时间向量

% 合成信号：50 Hz + 120 Hz + 噪声
signal = sin(2*pi*50*t) + 0.5*sin(2*pi*120*t) + 0.3*randn(size(t));

% 时域波形
figure(1);
subplot(2, 1, 1);
plot(t, signal);
xlabel('时间 (s)');
ylabel('幅度');
title('复合信号时域波形');
grid on;

% 频谱分析（FFT）
N = length(signal);
Y = fft(signal);
P2 = abs(Y/N);
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(0:(N/2))/N;

% 频谱图
subplot(2, 1, 2);
plot(f, P1);
xlabel('频率 (Hz)');
ylabel('幅度');
title('信号频谱');
xlim([0 200]);                % 只显示 0~200 Hz
grid on;
```

**渲染效果：** 上图显示复合信号的时域波形（杂乱无章），下图显示频谱（在 50 Hz 和 120 Hz 处有两个清晰的峰值），直观展示了傅里叶变换"从时域到频域"的魔力。

## 4.2 案例二：图像处理 —— 边缘检测

```matlab
% 读取图像
img = imread('cameraman.tif');    % MATLAB 内置示例图像
img = double(img) / 255;           % 归一化到 [0, 1]

% 显示原图
figure(2);
subplot(2, 2, 1);
imshow(img);
title('原始图像');

% 添加高斯噪声
noisy = img + 0.05 * randn(size(img));
noisy = max(0, min(1, noisy));     % 限制在 [0, 1]
subplot(2, 2, 2);
imshow(noisy);
title('添加噪声后');

% 高斯滤波去噪
h = fspecial('gaussian', [5 5], 1);
denoised = imfilter(noisy, h);
subplot(2, 2, 3);
imshow(denoised);
title('高斯滤波去噪');

% Sobel 边缘检测
sobel_x = [-1 0 1; -2 0 2; -1 0 1];    % 水平边缘
sobel_y = [-1 -2 -1; 0 0 0; 1 2 1];    % 垂直边缘
edges_x = imfilter(denoised, sobel_x);
edges_y = imfilter(denoised, sobel_y);
edges = sqrt(edges_x.^2 + edges_y.^2);   % 梯度幅值
subplot(2, 2, 4);
imshow(edges);
title('Sobel 边缘检测');
```

**渲染效果：** 四宫格展示图像处理流水线：原图 → 加噪 → 去噪 → 边缘检测。边缘检测结果中白色线条勾勒出物体的轮廓。

## 4.3 案例三：数值分析 —— 求解微分方程

```matlab
% 洛伦兹吸引子（混沌系统的经典例子）
% dx/dt = sigma*(y - x)
% dy/dt = x*(rho - z) - y
% dz/dt = x*y - beta*z

sigma = 10;
beta = 8/3;
rho = 28;

% 定义微分方程
lorenz = @(t, y) [
    sigma * (y(2) - y(1));
    y(1) * (rho - y(3)) - y(2);
    y(1) * y(2) - beta * y(3)
];

% 求解
[t, Y] = ode45(lorenz, [0 50], [1; 1; 1]);

% 三维轨迹图
figure(3);
plot3(Y(:,1), Y(:,2), Y(:,3), 'b-', 'LineWidth', 0.5);
xlabel('X');
ylabel('Y');
zlabel('Z');
title('洛伦兹吸引子');
grid on;
view(30, 30);    % 设置视角
```

**渲染效果：** 三维空间中显示著名的"蝴蝶形"轨迹——洛伦兹吸引子。轨迹在两个"翅膀"之间来回切换，展示了确定性系统中的混沌行为。

---

## 本章要点总结

- [ ] 掌握 FFT 频谱分析的基本流程
- [ ] 理解图像处理流水线：读取 → 滤波 → 边缘检测
- [ ] 了解 ODE 求解器 `ode45` 的用法
- [ ] 能综合运用 MATLAB 解决实际工程问题

---

## 课后练习

### 基础练习

1. 生成一个包含 100 Hz 和 200 Hz 分量的信号，用 FFT 分析其频谱。
2. 读取一张自己的照片，尝试不同的滤波和边缘检测方法。

### 进阶挑战

3. 用 MATLAB 实现一个简单的音频均衡器（调整不同频段的增益）。
4. 求解单摆的运动方程，并制作动画展示摆动过程。

---

👉 [返回首页 →](index.md)