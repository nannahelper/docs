# 第 8 章：综合实战项目——数字钟设计

> **从"单个积木"到"完整城堡"——整合所有知识打造一个真实项目**

---

## 章节概览

| 小节 | 内容 | 核心概念 |
|:---|:---|:---|
| 8.1 | 项目概述与架构设计 | 系统框图、模块划分、接口定义 |
| 8.2 | 时钟分频模块 | 将高频时钟分频为 1Hz |
| 8.3 | 计时核心模块 | 时/分/秒计数器 |
| 8.4 | 显示译码模块 | BCD 转七段数码管 |
| 8.5 | 按键消抖模块 | 按键输入处理 |
| 8.6 | 顶层模块集成 | 将所有子模块连接起来 |
| 8.7 | 仿真验证 | 完整系统仿真与波形分析 |
| 8.8 | 项目总结与拓展 | 技能回顾、拓展方向 |

---

## 8.1 项目概述与架构设计

### 项目目标

设计一个功能完整的 **数字钟** ，具备以下功能：
- 时:分:秒计时（24 小时制）
- 六位数码管显示（HH:MM:SS）
- 按键调时（时/分调整）
- 整点报时信号

### 系统框图

```
┌─────────────────────────────────────────────────────────┐
│                      digital_clock_top                   │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │ 时钟分频  │──→│ 计时核心  │──→│ 显示译码  │──→ seg_out │
│  │ (1Hz)    │   │ (HH:MM:SS)│   │ (BCD→7段) │            │
│  └──────────┘   └────┬─────┘   └──────────┘            │
│                      │                                   │
│  ┌──────────┐        │                                   │
│  │ 按键消抖  │────────┘                                   │
│  └──────────┘                                            │
│      ↑                                                   │
│   key_in                                                 │
└─────────────────────────────────────────────────────────┘
```

### 模块清单

| 模块 | 文件名 | 功能 | 对应章节 |
|:---|:---|:---|:---|
| **时钟分频** | `clk_divider.v` | 将系统时钟分频为 1Hz | 第 6 章 |
| **计时核心** | `time_counter.v` | 时/分/秒计数 | 第 6 章 |
| **显示译码** | `bcd_to_7seg.v` | BCD 码转七段数码管 | 第 5 章 |
| **按键消抖** | `debounce.v` | 按键去抖动 | 第 6 章 |
| **顶层集成** | `digital_clock_top.v` | 连接所有子模块 | 第 4 章 |

---

## 8.2 时钟分频模块

### 设计说明

假设系统时钟为 100MHz，需要产生 1Hz 的使能信号（每秒一个脉冲）。

```verilog
// clk_divider.v —— 时钟分频器（产生 1Hz 使能信号）
module clk_divider #(
    parameter CLK_FREQ = 100_000_000  // 系统时钟频率（Hz）
) (
    input  wire clk,
    input  wire rst,
    output reg  tick_1hz    // 每秒一个时钟周期的脉冲
);

    // 计数器位宽：需要计数到 CLK_FREQ-1
    // 100_000_000 需要 27 位（2^27 = 134_217_728）
    reg [26:0] counter;

    always @(posedge clk) begin
        if (rst) begin
            counter <= 27'b0;
            tick_1hz <= 1'b0;
        end else begin
            if (counter == CLK_FREQ - 1) begin
                counter <= 27'b0;
                tick_1hz <= 1'b1;    // 产生一个时钟周期的脉冲
            end else begin
                counter <= counter + 1'b1;
                tick_1hz <= 1'b0;
            end
        end
    end

endmodule
```

!!! tip "为什么用使能信号而不是分频时钟？"
    `tick_1hz` 是一个脉冲信号（每秒一个时钟周期的高电平），而不是一个新的时钟。下游模块仍然使用原始 `clk`，只是用 `tick_1hz` 作为使能条件。这避免了多时钟域问题。

---

## 8.3 计时核心模块

### 设计说明

实现 24 小时制的时/分/秒计数，支持按键调整。

```verilog
// time_counter.v —— 计时核心模块
module time_counter (
    input  wire       clk,
    input  wire       rst,
    input  wire       tick_1hz,       // 1Hz 使能信号
    input  wire       adj_hour,       // 调时按键
    input  wire       adj_min,        // 调分按键
    output wire [5:0] hour,           // 0~23（BCD 格式的高位和低位）
    output wire [5:0] minute,         // 0~59
    output wire [5:0] second,         // 0~59
    output wire       alarm           // 整点报时（59:59→00:00 时输出）
);

    reg [5:0] sec_cnt;   // 秒：0~59
    reg [5:0] min_cnt;   // 分：0~59
    reg [5:0] hour_cnt;  // 时：0~23

    // ============ 秒计数器 ============
    always @(posedge clk) begin
        if (rst) begin
            sec_cnt <= 6'b0;
        end else if (tick_1hz) begin
            if (sec_cnt == 6'd59)
                sec_cnt <= 6'b0;
            else
                sec_cnt <= sec_cnt + 1'b1;
        end
    end

    // ============ 分计数器 ============
    always @(posedge clk) begin
        if (rst) begin
            min_cnt <= 6'b0;
        end else if (adj_min) begin
            // 按键调分：每次加 1
            if (min_cnt == 6'd59)
                min_cnt <= 6'b0;
            else
                min_cnt <= min_cnt + 1'b1;
        end else if (tick_1hz && sec_cnt == 6'd59) begin
            // 秒进位：59 秒后分加 1
            if (min_cnt == 6'd59)
                min_cnt <= 6'b0;
            else
                min_cnt <= min_cnt + 1'b1;
        end
    end

    // ============ 时计数器 ============
    always @(posedge clk) begin
        if (rst) begin
            hour_cnt <= 6'b0;
        end else if (adj_hour) begin
            // 按键调时：每次加 1
            if (hour_cnt == 6'd23)
                hour_cnt <= 6'b0;
            else
                hour_cnt <= hour_cnt + 1'b1;
        end else if (tick_1hz && sec_cnt == 6'd59 && min_cnt == 6'd59) begin
            // 分进位：59 分 59 秒后时加 1
            if (hour_cnt == 6'd23)
                hour_cnt <= 6'b0;
            else
                hour_cnt <= hour_cnt + 1'b1;
        end
    end

    // ============ 整点报时 ============
    // 当 59:59 秒且 tick_1hz 到来时（即将变为 00:00），输出报时信号
    reg alarm_reg;
    always @(posedge clk) begin
        if (rst)
            alarm_reg <= 1'b0;
        else
            alarm_reg <= tick_1hz && (sec_cnt == 6'd59) &&
                         (min_cnt == 6'd59) && (hour_cnt == 6'd23);
    end

    // ============ 输出 ============
    assign hour   = hour_cnt;
    assign minute = min_cnt;
    assign second = sec_cnt;
    assign alarm  = alarm_reg;

endmodule
```

---

## 8.4 显示译码模块

### 设计说明

将 BCD 码转换为七段数码管显示。六位数码管显示 HH:MM:SS。

```verilog
// bcd_to_7seg.v —— BCD 码转七段数码管
module bcd_to_7seg (
    input  wire [3:0] bcd,       // BCD 码输入（0~9）
    output reg  [6:0] seg        // 七段数码管（低电平有效）
);

    // 七段数码管编码（共阳极，低电平有效）
    //   --0--
    //  |     |
    //  5     1
    //  |     |
    //   --6--
    //  |     |
    //  4     2
    //  |     |
    //   --3--
    //
    // seg[6:0] = {g, f, e, d, c, b, a}

    always @(*) begin
        case (bcd)
            4'd0: seg = 7'b100_0000;  // 显示 0
            4'd1: seg = 7'b111_1001;  // 显示 1
            4'd2: seg = 7'b010_0100;  // 显示 2
            4'd3: seg = 7'b011_0000;  // 显示 3
            4'd4: seg = 7'b001_1001;  // 显示 4
            4'd5: seg = 7'b001_0010;  // 显示 5
            4'd6: seg = 7'b000_0010;  // 显示 6
            4'd7: seg = 7'b111_1000;  // 显示 7
            4'd8: seg = 7'b000_0000;  // 显示 8
            4'd9: seg = 7'b001_0000;  // 显示 9
            default: seg = 7'b111_1111;  // 全灭
        endcase
    end

endmodule
```

### 显示扫描模块

六位数码管采用动态扫描方式（一次只亮一个位，快速切换产生"同时亮"的视觉效果）：

```verilog
// display_scanner.v —— 数码管动态扫描
module display_scanner (
    input  wire       clk,
    input  wire       rst,
    input  wire [5:0] hour,      // 时（0~23）
    input  wire [5:0] minute,    // 分（0~59）
    input  wire [5:0] second,    // 秒（0~59）
    output reg  [6:0] seg_out,   // 段选
    output reg  [5:0] dig_sel    // 位选（6 位数码管）
);

    // 扫描时钟（约 1kHz，6 位 × 1kHz = 6kHz 刷新率）
    reg [15:0] scan_counter;
    wire scan_tick = (scan_counter == 16'd49_999);  // 100MHz / 50000 = 2kHz

    always @(posedge clk) begin
        if (rst)
            scan_counter <= 16'b0;
        else if (scan_tick)
            scan_counter <= 16'b0;
        else
            scan_counter <= scan_counter + 1'b1;
    end

    // 位选循环（0→1→2→3→4→5→0→...）
    reg [2:0] current_digit;

    always @(posedge clk) begin
        if (rst)
            current_digit <= 3'b0;
        else if (scan_tick) begin
            if (current_digit == 3'd5)
                current_digit <= 3'b0;
            else
                current_digit <= current_digit + 1'b1;
        end
    end

    // 根据当前位选，输出对应的 BCD 值
    reg [3:0] current_bcd;

    always @(*) begin
        case (current_digit)
            // 数码管 5：时的十位（0~2）
            3'd5: current_bcd = hour / 10;

            // 数码管 4：时的个位（0~9）
            3'd4: current_bcd = hour % 10;

            // 数码管 3：分的十位（0~5）
            3'd3: current_bcd = minute / 10;

            // 数码管 2：分的个位（0~9）
            3'd2: current_bcd = minute % 10;

            // 数码管 1：秒的十位（0~5）
            3'd1: current_bcd = second / 10;

            // 数码管 0：秒的个位（0~9）
            3'd0: current_bcd = second % 10;

            default: current_bcd = 4'd0;
        endcase
    end

    // 位选输出（低电平有效）
    always @(*) begin
        dig_sel = 6'b111_111;
        dig_sel[current_digit] = 1'b0;
    end

    // 段选输出
    wire [6:0] seg_data;
    bcd_to_7seg u_seg (
        .bcd(current_bcd),
        .seg(seg_data)
    );

    always @(posedge clk) begin
        if (rst)
            seg_out <= 7'b111_1111;
        else
            seg_out <= seg_data;
    end

endmodule
```

---

## 8.5 按键消抖模块

### 设计说明

机械按键在按下和释放时会产生抖动（约 5~20ms），需要消抖处理。

```verilog
// debounce.v —— 按键消抖模块
module debounce #(
    parameter DEBOUNCE_MS = 20,          // 消抖时间（ms）
    parameter CLK_FREQ    = 100_000_000  // 时钟频率（Hz）
) (
    input  wire clk,
    input  wire rst,
    input  wire key_in,       // 原始按键输入
    output wire key_out       // 消抖后的按键输出（单周期脉冲）
);

    // 消抖所需的时钟周期数
    // 20ms × 100MHz = 2_000_000 个周期
    localparam DEBOUNCE_CYCLES = (CLK_FREQ / 1000) * DEBOUNCE_MS;

    reg [$clog2(DEBOUNCE_CYCLES)-1:0] counter;
    reg key_sync_0, key_sync_1;  // 两级同步器（防止亚稳态）
    reg key_stable;               // 稳定后的按键值
    reg key_stable_d1;            // 延迟一拍，用于边沿检测

    // 两级同步器
    always @(posedge clk) begin
        if (rst) begin
            key_sync_0 <= 1'b1;  // 按键未按下（上拉）
            key_sync_1 <= 1'b1;
        end else begin
            key_sync_0 <= key_in;
            key_sync_1 <= key_sync_0;
        end
    end

    // 消抖计数器
    always @(posedge clk) begin
        if (rst) begin
            counter <= 0;
            key_stable <= 1'b1;
        end else begin
            if (key_sync_1 != key_stable) begin
                // 输入与稳定值不同，开始计数
                if (counter == DEBOUNCE_CYCLES - 1) begin
                    // 消抖时间到，更新稳定值
                    key_stable <= key_sync_1;
                    counter <= 0;
                end else begin
                    counter <= counter + 1'b1;
                end
            end else begin
                counter <= 0;
            end
        end
    end

    // 边沿检测：产生单周期脉冲
    always @(posedge clk) begin
        if (rst)
            key_stable_d1 <= 1'b1;
        else
            key_stable_d1 <= key_stable;
    end

    // 下降沿检测（按键按下时输出一个脉冲）
    assign key_out = key_stable_d1 && !key_stable;

endmodule
```

---

## 8.6 顶层模块集成

```verilog
// digital_clock_top.v —— 数字钟顶层模块
module digital_clock_top (
    input  wire       clk_100mhz,   // 100MHz 系统时钟
    input  wire       rst,
    input  wire       key_hour,     // 调时按键
    input  wire       key_min,      // 调分按键
    output wire [6:0] seg_out,      // 数码管段选
    output wire [5:0] dig_sel,      // 数码管位选
    output wire       alarm_out     // 整点报时
);

    // ============ 内部连线 ============
    wire tick_1hz;
    wire [5:0] hour, minute, second;
    wire adj_hour, adj_min;

    // ============ 子模块实例化 ============

    // 1. 时钟分频器
    clk_divider #(.CLK_FREQ(100_000_000)) u_clk_div (
        .clk      (clk_100mhz),
        .rst      (rst),
        .tick_1hz (tick_1hz)
    );

    // 2. 按键消抖（调时）
    debounce #(.DEBOUNCE_MS(20), .CLK_FREQ(100_000_000)) u_deb_hour (
        .clk     (clk_100mhz),
        .rst     (rst),
        .key_in  (key_hour),
        .key_out (adj_hour)
    );

    // 3. 按键消抖（调分）
    debounce #(.DEBOUNCE_MS(20), .CLK_FREQ(100_000_000)) u_deb_min (
        .clk     (clk_100mhz),
        .rst     (rst),
        .key_in  (key_min),
        .key_out (adj_min)
    );

    // 4. 计时核心
    time_counter u_time (
        .clk      (clk_100mhz),
        .rst      (rst),
        .tick_1hz (tick_1hz),
        .adj_hour (adj_hour),
        .adj_min  (adj_min),
        .hour     (hour),
        .minute   (minute),
        .second   (second),
        .alarm    (alarm_out)
    );

    // 5. 显示扫描
    display_scanner u_display (
        .clk      (clk_100mhz),
        .rst      (rst),
        .hour     (hour),
        .minute   (minute),
        .second   (second),
        .seg_out  (seg_out),
        .dig_sel  (dig_sel)
    );

endmodule
```

---

## 8.7 仿真验证

### Testbench 设计

```verilog
// digital_clock_tb.v —— 数字钟仿真测试
`timescale 1ns / 1ps

module digital_clock_tb;

    reg clk;
    reg rst;
    reg key_hour;
    reg key_min;
    wire [6:0] seg_out;
    wire [5:0] dig_sel;
    wire alarm_out;

    // 实例化被测模块
    digital_clock_top uut (
        .clk_100mhz (clk),
        .rst        (rst),
        .key_hour   (key_hour),
        .key_min    (key_min),
        .seg_out    (seg_out),
        .dig_sel    (dig_sel),
        .alarm_out  (alarm_out)
    );

    // 时钟生成（100MHz → 周期 10ns）
    always #5 clk = ~clk;  // 5ns 半周期

    // 波形记录
    initial begin
        $dumpfile("digital_clock_tb.vcd");
        $dumpvars(0, digital_clock_tb);
    end

    // 测试激励
    initial begin
        // 初始化
        clk = 0;
        rst = 1;
        key_hour = 1'b1;  // 未按下（上拉）
        key_min  = 1'b1;

        // 复位释放
        #100;
        rst = 0;

        // 等待 1 秒（100M 个时钟周期，仿真太慢）
        // 实际仿真时建议缩短分频系数，或使用参数化
        // 此处仅示意，实际仿真需调整 CLK_FREQ 参数

        // 模拟调时按键
        #1000;
        key_hour = 1'b0;  // 按下调时键
        #20000000;        // 保持 20ms（消抖时间）
        key_hour = 1'b1;  // 释放

        // 继续仿真...
        #100000;
        $finish;
    end

endmodule
```

!!! tip "仿真加速技巧"
    在实际仿真中，100MHz 时钟跑 1 秒需要 1 亿个时钟周期，太慢了。建议：
    1. 将 `CLK_FREQ` 参数改为较小的值（如 1000）进行功能验证
    2. 功能验证通过后，再改回真实频率进行时序验证

---

## 8.8 项目总结与拓展

### 技能回顾

| 章节 | 技能 | 在本项目中的应用 |
|:---|:---|:---|
| 第 1 章 | 数字逻辑基础 | 理解七段数码管编码原理 |
| 第 2 章 | 环境搭建 | 使用 Icarus Verilog 编译仿真 |
| 第 3 章 | 数据类型与运算符 | 向量声明、位选择、拼接 |
| 第 4 章 | 模块与端口 | 顶层模块集成 5 个子模块 |
| 第 5 章 | 组合逻辑 | BCD 转七段码译码器 |
| 第 6 章 | 时序逻辑 | 计数器、分频器、消抖 |
| 第 7 章 | 状态机 | （本项目未使用，但可扩展） |

### 拓展方向

| 拓展功能 | 涉及知识点 | 难度 |
|:---|:---|:---:|
| **闹钟功能** | 比较器 + 状态机 | ⭐⭐ |
| **12/24 小时制切换** | 多路选择器 + 按键处理 | ⭐⭐ |
| **秒表功能** | 状态机（计时/暂停/复位） | ⭐⭐⭐ |
| **UART 串口输出** | 串行通信协议 | ⭐⭐⭐⭐ |
| **VGA 显示时钟** | VGA 时序 + 字符生成 | ⭐⭐⭐⭐⭐ |

---

## 本章练习

1. 修改 `clk_divider` 模块，增加一个参数 `TARGET_FREQ`，使其能产生任意频率的使能信号。

2. 为数字钟添加 **闹钟功能** ：
   - 增加闹钟时间设置（时/分）
   - 当前时间与闹钟时间匹配时，输出 `alarm_trigger` 信号
   - 闹钟触发后持续 60 秒或直到按键取消

3. 修改显示模块，在时和分之间显示闪烁的冒号（每秒闪烁一次）。

4. 编写完整的 Testbench，验证以下场景：
   - 正常计时：00:00:00 → 00:00:01 → ... → 00:01:00
   - 分钟进位：00:59:59 → 01:00:00
   - 小时进位：23:59:59 → 00:00:00
   - 按键调时：按下调时键，小时数 +1
   - 按键调分：按下调分键，分钟数 +1

---

## FAQ：常见问题解答

!!! question "为什么顶层模块中不写逻辑，只做连线？"
    这是 **结构化设计** 的核心思想——顶层只负责"连接"，所有功能实现在子模块中。这样做的好处是：顶层清晰（一眼看出系统结构）、子模块可复用、便于团队协作。

!!! question "仿真时 100MHz 跑太慢了怎么办？"
    在 Testbench 中使用 `defparam` 覆盖参数，将 `CLK_FREQ` 改为较小的值（如 100）。功能验证通过后再改回真实值。注意：这只是仿真技巧，不影响综合结果。

!!! question "按键消抖为什么需要 20ms？"
    机械按键的抖动通常在 5~20ms 范围内。20ms 是一个安全值，能覆盖绝大多数按键。如果消抖时间太短，可能无法完全消除抖动；太长则按键响应变慢。

!!! question "数码管动态扫描的频率应该是多少？"
    每位扫描频率至少 50Hz（6 位数码管 → 总扫描频率 ≥ 300Hz）。通常取 1kHz 左右，既能避免闪烁，又不会消耗太多功耗。

!!! question "这个数字钟能直接在 FPGA 上运行吗？"
    可以！但需要根据你的 FPGA 开发板修改引脚约束文件（XDC/QSF）。数码管的段选和位选极性（共阳/共阴）也需要根据实际硬件调整。

---

**恭喜你完成了 Verilog 零基础入门指南的全部内容！**

从逻辑门到时序电路，从单个模块到完整系统，你已经掌握了使用 Verilog 描述数字电路的核心技能。接下来，建议你：
- 在 FPGA 开发板上实际运行这些设计
- 学习更多高级主题（FIFO、UART、SPI、VGA 等）
- 阅读开源项目的 Verilog 代码，学习工业级设计风格