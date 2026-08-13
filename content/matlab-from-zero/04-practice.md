# 第 4 章：完成数据分析项目

> **场景：** 你掌握了 MATLAB 的核心技能，现在来完成一个端到端的数据分析项目——从原始数据到可视化报告，展示你的完整能力。

---

## 4.1 项目：心电信号分析

假设你有一份心电信号（ECG）数据，需要完成：去噪、峰值检测、心率计算和可视化。

```matlab
% ecg_analysis.m —— 心电信号分析项目
clear; clc; close all;

% ========== 1. 生成模拟 ECG 信号 ==========
fs = 500;                        % 采样率 500 Hz
t = 0:1/fs:10;                   % 10 秒数据
f_heart = 1.2;                   % 心率 72 bpm (1.2 Hz)

% 生成 ECG 波形（简化模型）
ecg_clean = 2.5 * sin(2*pi*f_heart*t);
ecg_clean(ecg_clean < 0) = 0;    % 只保留正向波
ecg_clean = ecg_clean .^ 2;      % 锐化峰值

% 添加噪声
noise = 0.3 * randn(size(t));     % 高斯噪声
noise = noise + 0.1 * sin(2*pi*50*t);  % 50 Hz 工频干扰
ecg_noisy = ecg_clean + noise;

% ========== 2. 信号去噪 ==========
% 低通滤波器设计
fc = 30;                         % 截止频率 30 Hz
[b, a] = butter(4, fc/(fs/2), 'low');
ecg_filtered = filtfilt(b, a, ecg_noisy);

% ========== 3. 峰值检测 ==========
min_peak_height = 0.5 * max(ecg_filtered);
min_peak_distance = 0.3 * fs;    % 最小间隔 0.3 秒
[pks, locs] = findpeaks(ecg_filtered, 'MinPeakHeight', min_peak_height, ...
                        'MinPeakDistance', min_peak_distance);

% ========== 4. 计算心率 ==========
rr_intervals = diff(locs) / fs;  % RR 间期（秒）
heart_rate = 60 ./ rr_intervals; % 瞬时心率（bpm）
hr_mean = mean(heart_rate);
hr_std = std(heart_rate);

% ========== 5. 可视化 ==========
figure('Position', [100, 100, 1000, 700]);

% 子图 1：原始信号 vs 去噪信号
subplot(3, 1, 1);
plot(t, ecg_noisy, 'Color', [0.7, 0.7, 0.7]);
hold on;
plot(t, ecg_filtered, 'b-', 'LineWidth', 1.5);
xlabel('时间 (s)');
ylabel('幅值 (mV)');
title('ECG 信号去噪');
legend('含噪信号', '去噪后信号');
grid on;
xlim([0, 5]);

% 子图 2：峰值检测结果
subplot(3, 1, 2);
plot(t, ecg_filtered, 'b-', 'LineWidth', 1);
hold on;
plot(t(locs), pks, 'ro', 'MarkerSize', 6, 'MarkerFaceColor', 'r');
xlabel('时间 (s)');
ylabel('幅值 (mV)');
title(sprintf('R 波峰值检测（共检测到 %d 个峰值）', length(pks)));
grid on;
xlim([0, 5]);

% 子图 3：心率变化
subplot(3, 1, 3);
plot(t(locs(2:end)), heart_rate, 'g-o', 'LineWidth', 1.5, 'MarkerSize', 4);
hold on;
yline(hr_mean, 'r--', sprintf('均值 = %.1f bpm', hr_mean), 'LineWidth', 1.5);
xlabel('时间 (s)');
ylabel('心率 (bpm)');
title('瞬时心率变化');
grid on;
xlim([0, 10]);
ylim([hr_mean - 20, hr_mean + 20]);

% ========== 6. 输出报告 ==========
fprintf('========== ECG 分析报告 ==========\n');
fprintf('采样率：%d Hz\n', fs);
fprintf('数据时长：%.1f 秒\n', t(end));
fprintf('检测到 R 波数量：%d\n', length(pks));
fprintf('平均心率：%.1f bpm\n', hr_mean);
fprintf('心率标准差：%.1f bpm\n', hr_std);
fprintf('心率变异性 (HRV)：%.1f ms\n', std(rr_intervals) * 1000);
```

**渲染效果：** 一个图窗包含三个子图：信号去噪对比（灰色含噪 vs 蓝色去噪）、R 波峰值检测（红色标记）、瞬时心率变化（绿色折线+红色均值线）。命令窗口输出完整分析报告。

---

## 4.2 项目：图像处理

```matlab
% image_processing.m —— 图像处理示例
clear; clc; close all;

% 读取图像
img = imread('sample.jpg');
if size(img, 3) == 3
    img_gray = rgb2gray(img);
else
    img_gray = img;
end

% 边缘检测
edges_canny = edge(img_gray, 'canny');
edges_sobel = edge(img_gray, 'sobel');

% 图像增强
img_enhanced = imadjust(img_gray);

% 可视化
figure('Position', [100, 100, 900, 600]);

subplot(2, 2, 1);
imshow(img_gray);
title('原始灰度图像');

subplot(2, 2, 2);
imshow(img_enhanced);
title('对比度增强');

subplot(2, 2, 3);
imshow(edges_canny);
title('Canny 边缘检测');

subplot(2, 2, 4);
imshow(edges_sobel);
title('Sobel 边缘检测');
```

**渲染效果：** 2×2 子图布局，分别显示原始灰度图、对比度增强图、Canny 边缘检测结果和 Sobel 边缘检测结果。

---

## 4.3 学习旅程回顾

| 章节 | 场景 | 核心技能 |
|:---|:---|:---|
| 第 1 章 | 分析实验数据 | 变量、矩阵、基本运算、脚本 |
| 第 2 章 | 绘制专业图表 | 二维/三维绘图、子图、标注 |
| 第 3 章 | 批量处理数据 | 函数、流程控制、文件读写 |
| 第 4 章 | 端到端项目 | 信号处理、图像处理、报告生成 |

---

## 课后练习

### 基础练习

1. 用 MATLAB 分析一组实验数据，完成线性拟合和可视化。
2. 编写一个函数，输入矩阵返回其转置、逆矩阵和行列式。

### 进阶挑战

3. 下载一份公开数据集（如气温数据），完成从导入到可视化的完整分析流程。
4. 用 App Designer 创建一个简单的数据导入和绘图 GUI。

---

👉 [返回首页 →](index.md)