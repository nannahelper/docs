# 第 7 章：状态机设计

> **从"红绿灯"到"智能控制器"——掌握有限状态机（FSM）**

---

## 章节概览

| 小节 | 内容 | 核心概念 |
|:---|:---|:---|
| 7.1 | 状态机概述 | FSM 概念、Moore vs Mealy |
| 7.2 | 状态机编码方式 | 二进制码、格雷码、独热码 |
| 7.3 | 三段式状态机 | 标准 FSM 写法（推荐） |
| 7.4 | Moore 状态机实战 | 交通灯控制器 |
| 7.5 | Mealy 状态机实战 | 序列检测器 |
| 7.6 | 状态机设计技巧 | 默认状态、未使用状态处理 |
| 7.7 | 本章练习 | 状态机综合练习 |

---

## 7.1 状态机概述

### 什么是有限状态机？

**有限状态机** （Finite State Machine, FSM）是一种描述系统在不同"状态"之间转换的数学模型。它是数字电路设计中最强大的工具之一。

**乐高比喻：** 状态机 = 交通灯控制系统。交通灯有固定的几个状态（红灯→绿灯→黄灯→红灯），每个状态持续固定时间，状态之间的转换有明确的规则。系统"记住"当前是什么灯，这就是状态机的"记忆"能力。

### 状态机的三要素

```
┌──────────────────────────────────────┐
│              状态机                   │
│                                      │
│  输入 ──→ ┌──────────┐ ──→ 输出     │
│           │ 组合逻辑  │              │
│           │ (下一状态) │              │
│           └─────┬────┘              │
│                 │                    │
│           ┌─────▼────┐              │
│           │ 状态寄存器 │ ←── 时钟    │
│           │ (当前状态) │              │
│           └─────┬────┘              │
│                 │                    │
│           ┌─────▼────┐              │
│           │ 组合逻辑  │              │
│           │ (输出逻辑) │              │
│           └──────────┘              │
└──────────────────────────────────────┘
```

| 要素 | 说明 | 乐高比喻 |
|:---|:---|:---|
| **状态寄存器** | 存储当前状态（时序逻辑） | 交通灯当前的颜色 |
| **下一状态逻辑** | 根据当前状态和输入决定下一状态（组合逻辑） | 决定"绿灯结束后该亮什么灯"的规则 |
| **输出逻辑** | 根据当前状态（和输入）产生输出（组合逻辑） | 根据当前灯色控制各方向车辆通行 |

### Moore 机 vs Mealy 机

| 特性 | Moore 状态机 | Mealy 状态机 |
|:---|:---|:---|
| **输出决定因素** | 仅取决于当前状态 | 取决于当前状态 + 当前输入 |
| **输出时序** | 在状态转换后的时钟周期变化 | 输入变化后立即响应 |
| **状态数量** | 通常更多 | 通常更少 |
| **稳定性** | 输出更稳定（抗毛刺） | 输入毛刺可能影响输出 |
| **典型应用** | 交通灯、控制器 | 序列检测器、协议解析 |

```verilog
// Moore 机：输出仅取决于状态
assign red_light    = (state == S_RED);
assign green_light  = (state == S_GREEN);
assign yellow_light = (state == S_YELLOW);

// Mealy 机：输出取决于状态 + 输入
assign detected = (state == S_LAST) && (input_bit == 1'b1);
```

---

## 7.2 状态机编码方式

### 三种编码方式对比

| 编码方式 | 示例（4 状态） | 优点 | 缺点 |
|:---|:---|:---|:---|
| **二进制码** | 00, 01, 10, 11 | 寄存器用量最少 | 多位同时翻转，可能产生毛刺 |
| **格雷码** | 00, 01, 11, 10 | 每次只变 1 位，抗毛刺 | 解码需要额外逻辑 |
| **独热码** | 0001, 0010, 0100, 1000 | 解码简单，速度快 | 寄存器用量多（N 状态需 N 位） |

!!! tip "FPGA 中推荐独热码"
    FPGA 有丰富的寄存器资源，独热码虽然多用寄存器，但解码逻辑最简单、速度最快。大多数综合工具默认使用独热码。

### 状态定义

```verilog
// 使用 parameter 定义状态（推荐）
parameter S_IDLE  = 4'b0001;  // 独热码
parameter S_START = 4'b0010;
parameter S_RUN   = 4'b0100;
parameter S_DONE  = 4'b1000;

// 使用 localparam 定义（如果状态不应被外部修改）
localparam S_IDLE  = 3'b000;  // 二进制码
localparam S_START = 3'b001;
localparam S_RUN   = 3'b010;
localparam S_DONE  = 3'b011;
```

---

## 7.3 三段式状态机

### 标准写法（强烈推荐）

三段式状态机将状态机的三个要素分离到三个 `always` 块中，结构清晰、易于维护：

```verilog
module fsm_template (
    input  wire clk,
    input  wire rst,
    input  wire [输入端口],
    output reg  [输出端口]
);

    // ============ 状态定义 ============
    parameter S_IDLE  = 3'b001;
    parameter S_STATE1 = 3'b010;
    parameter S_STATE2 = 3'b100;

    // ============ 第一段：状态寄存器（时序逻辑）============
    reg [2:0] current_state, next_state;

    always @(posedge clk) begin
        if (rst)
            current_state <= S_IDLE;
        else
            current_state <= next_state;
    end

    // ============ 第二段：下一状态逻辑（组合逻辑）============
    always @(*) begin
        next_state = current_state;  // 默认保持当前状态
        case (current_state)
            S_IDLE: begin
                if (start)
                    next_state = S_STATE1;
            end
            S_STATE1: begin
                if (done)
                    next_state = S_STATE2;
            end
            S_STATE2: begin
                next_state = S_IDLE;
            end
            default: next_state = S_IDLE;
        endcase
    end

    // ============ 第三段：输出逻辑（时序逻辑，Moore 机）============
    always @(posedge clk) begin
        if (rst) begin
            // 复位时输出默认值
            output_signal <= 1'b0;
        end else begin
            case (next_state)  // 注意：用 next_state 提前一拍输出
                S_IDLE:  output_signal <= 1'b0;
                S_STATE1: output_signal <= 1'b1;
                S_STATE2: output_signal <= 1'b0;
                default: output_signal <= 1'b0;
            endcase
        end
    end

endmodule
```

!!! tip "三段式的优势"
    - **第一段** （状态寄存器）：纯粹的时序逻辑，只做状态更新
    - **第二段** （下一状态逻辑）：纯粹的组合逻辑，描述状态转换条件
    - **第三段** （输出逻辑）：时序输出（Moore 机），避免输出毛刺
    - 三段分离，修改任一段不影响其他段

---

## 7.4 Moore 状态机实战：交通灯控制器

### 需求描述

设计一个十字路口交通灯控制器：
- 主干道绿灯 30 秒 → 黄灯 5 秒 → 红灯 20 秒（支路绿灯）→ 循环
- 支路绿灯时主干道红灯

### 状态转换图

```
        ┌──────────┐
        │  S_MAIN  │ 主干道绿灯，支路红灯（30s）
        │  _GREEN  │
        └────┬─────┘
             │ timer >= 30
        ┌────▼─────┐
        │  S_MAIN  │ 主干道黄灯，支路红灯（5s）
        │  _YELLOW │
        └────┬─────┘
             │ timer >= 5
        ┌────▼─────┐
        │  S_SIDE  │ 主干道红灯，支路绿灯（20s）
        │  _GREEN  │
        └────┬─────┘
             │ timer >= 20
             └──────→ 回到 S_MAIN_GREEN
```

### Verilog 实现

```verilog
module traffic_light_controller (
    input  wire clk,
    input  wire rst,
    output reg  main_red,      // 主干道红灯
    output reg  main_yellow,   // 主干道黄灯
    output reg  main_green,    // 主干道绿灯
    output reg  side_red,      // 支路红灯
    output reg  side_yellow,   // 支路黄灯
    output reg  side_green     // 支路绿灯
);

    // ============ 状态定义 ============
    parameter S_MAIN_GREEN  = 3'b001;  // 主干道绿灯
    parameter S_MAIN_YELLOW = 3'b010;  // 主干道黄灯
    parameter S_SIDE_GREEN  = 3'b100;  // 支路绿灯

    // ============ 时间参数（单位：秒）============
    parameter MAIN_GREEN_TIME  = 30;
    parameter MAIN_YELLOW_TIME = 5;
    parameter SIDE_GREEN_TIME  = 20;

    // ============ 内部信号 ============
    reg [2:0] current_state, next_state;
    reg [5:0] timer;  // 0~63 秒计数器

    // ============ 第一段：状态寄存器 ============
    always @(posedge clk) begin
        if (rst)
            current_state <= S_MAIN_GREEN;
        else
            current_state <= next_state;
    end

    // ============ 计时器 ============
    reg timer_reset;  // 计时器复位信号

    always @(posedge clk) begin
        if (rst || timer_reset)
            timer <= 6'b0;
        else
            timer <= timer + 1'b1;
    end

    // ============ 第二段：下一状态逻辑 ============
    always @(*) begin
        next_state = current_state;
        timer_reset = 1'b0;

        case (current_state)
            S_MAIN_GREEN: begin
                if (timer >= MAIN_GREEN_TIME - 1) begin
                    next_state = S_MAIN_YELLOW;
                    timer_reset = 1'b1;
                end
            end

            S_MAIN_YELLOW: begin
                if (timer >= MAIN_YELLOW_TIME - 1) begin
                    next_state = S_SIDE_GREEN;
                    timer_reset = 1'b1;
                end
            end

            S_SIDE_GREEN: begin
                if (timer >= SIDE_GREEN_TIME - 1) begin
                    next_state = S_MAIN_GREEN;
                    timer_reset = 1'b1;
                end
            end

            default: begin
                next_state = S_MAIN_GREEN;
                timer_reset = 1'b1;
            end
        endcase
    end

    // ============ 第三段：输出逻辑（Moore 机）============
    always @(posedge clk) begin
        if (rst) begin
            {main_red, main_yellow, main_green} <= 3'b001;
            {side_red, side_yellow, side_green} <= 3'b100;
        end else begin
            case (next_state)
                S_MAIN_GREEN: begin
                    {main_red, main_yellow, main_green} <= 3'b001;  // 主干道绿灯
                    {side_red, side_yellow, side_green}   <= 3'b100;  // 支路红灯
                end

                S_MAIN_YELLOW: begin
                    {main_red, main_yellow, main_green} <= 3'b010;  // 主干道黄灯
                    {side_red, side_yellow, side_green}   <= 3'b100;  // 支路红灯
                end

                S_SIDE_GREEN: begin
                    {main_red, main_yellow, main_green} <= 3'b100;  // 主干道红灯
                    {side_red, side_yellow, side_green}   <= 3'b001;  // 支路绿灯
                end

                default: begin
                    {main_red, main_yellow, main_green} <= 3'b001;
                    {side_red, side_yellow, side_green}   <= 3'b100;
                end
            endcase
        end
    end

endmodule
```

---

## 7.5 Mealy 状态机实战：序列检测器

### 需求描述

检测串行输入流中的"1101"序列（可重叠检测）。

### 状态转换图

```
    S0 ──1──→ S1 ──1──→ S2 ──0──→ S3 ──1──→ S0 (检测到 1101)
     │         │         │         │
     └─0─→S0   └─0─→S0   └─1─→S2   └─0─→S0
```

### Verilog 实现

```verilog
module sequence_detector_1101 (
    input  wire clk,
    input  wire rst,
    input  wire data_in,     // 串行输入
    output reg  detected     // 检测到序列时输出 1
);

    // ============ 状态定义（独热码）============
    parameter S0 = 4'b0001;  // 初始状态（收到 0 个匹配位）
    parameter S1 = 4'b0010;  // 收到 1
    parameter S2 = 4'b0100;  // 收到 11
    parameter S3 = 4'b1000;  // 收到 110

    // ============ 内部信号 ============
    reg [3:0] current_state, next_state;

    // ============ 第一段：状态寄存器 ============
    always @(posedge clk) begin
        if (rst)
            current_state <= S0;
        else
            current_state <= next_state;
    end

    // ============ 第二段：下一状态逻辑 ============
    always @(*) begin
        next_state = current_state;
        case (current_state)
            S0: begin
                if (data_in)
                    next_state = S1;   // 收到 1，进入 S1
                else
                    next_state = S0;   // 收到 0，保持 S0
            end

            S1: begin
                if (data_in)
                    next_state = S2;   // 收到 11，进入 S2
                else
                    next_state = S0;   // 收到 10，回到 S0
            end

            S2: begin
                if (data_in)
                    next_state = S2;   // 收到 111，保持 S2（重叠检测）
                else
                    next_state = S3;   // 收到 110，进入 S3
            end

            S3: begin
                if (data_in)
                    next_state = S1;   // 收到 1101，检测成功！回到 S1（重叠）
                else
                    next_state = S0;   // 收到 1100，回到 S0
            end

            default: next_state = S0;
        endcase
    end

    // ============ 第三段：输出逻辑（Mealy 机：输出取决于状态 + 输入）============
    always @(posedge clk) begin
        if (rst)
            detected <= 1'b0;
        else
            // Mealy 输出：在 S3 状态且当前输入为 1 时检测到序列
            detected <= (current_state == S3) && (data_in == 1'b1);
    end

endmodule
```

!!! example "Testbench 验证"
    ```verilog
    // 输入序列：1 1 0 1 1 0 1 ...
    //           ↑___↑ 检测到第一个 1101
    //               ↑___↑ 检测到第二个（重叠）
    initial begin
        data_in = 0; #10;
        data_in = 1; #10;  // S0→S1
        data_in = 1; #10;  // S1→S2
        data_in = 0; #10;  // S2→S3
        data_in = 1; #10;  // S3→S1, detected=1 ✅
        data_in = 1; #10;  // S1→S2
        data_in = 0; #10;  // S2→S3
        data_in = 1; #10;  // S3→S1, detected=1 ✅（重叠检测）
    end
    ```

---

## 7.6 状态机设计技巧

### 默认状态处理

```verilog
always @(*) begin
    // 技巧 1：先赋默认值，再在 case 中覆盖
    next_state = current_state;  // 默认保持

    case (current_state)
        S_IDLE: if (start) next_state = S_RUN;
        S_RUN:  if (done)  next_state = S_IDLE;
        default: next_state = S_IDLE;  // 安全兜底
    endcase
end
```

### 未使用状态的安全处理

```verilog
// 如果状态编码有未使用的值（如 4 位独热码有 16 种可能，只用了 4 种）
// 在 default 分支中跳转到安全状态
default: begin
    next_state = S_IDLE;     // 跳转到安全状态
    error_flag = 1'b1;       // 可选：标记异常
end
```

!!! danger "未处理状态的危害"
    如果状态机因为干扰（如宇宙射线导致的位翻转）进入未定义状态，且没有 `default` 分支处理，状态机可能"卡死"在无效状态中，永远无法恢复。

### 状态机验证清单

| 检查项 | 说明 |
|:---|:---|
| ✅ 所有状态都有 `default` 分支 | 防止进入未定义状态 |
| ✅ 复位后进入已知状态 | `rst` 时将 `current_state` 设为初始状态 |
| ✅ 每个状态的转换条件互斥 | 避免同时满足多个转换条件 |
| ✅ 输出信号在所有状态下都有定义 | 避免锁存器推断 |
| ✅ 三段式结构清晰 | 状态寄存器 / 下一状态逻辑 / 输出逻辑分离 |

---

## 7.7 本章练习

### 基础练习

1. 将 7.4 节的交通灯控制器改为 **两段式** 写法（合并第二段和第三段），对比两种写法的代码可读性。

2. 修改序列检测器，检测序列"1011"（不可重叠）。

### 状态机设计练习

3. 设计一个"自动售货机"状态机：
   - 商品价格：5 元
   - 只接受 1 元和 2 元硬币
   - 投币达到或超过 5 元时出货，并找零
   - 状态包括：等待投币、已投 1 元、已投 2 元、已投 3 元、已投 4 元、出货找零

4. 设计一个"电梯控制器"简化版（3 层楼）：
   - 输入：当前楼层传感器（`floor[2:0]`）、目标楼层按钮（`up_request[2:0]`、`down_request[2:0]`）
   - 输出：电机控制（`motor_up`、`motor_down`、`motor_stop`）、门控制（`door_open`）

### 综合练习

5. 设计一个"洗衣机控制器"状态机：
   - 状态：空闲 → 进水 → 洗涤（正转 5s → 停 2s → 反转 5s，循环 3 次）→ 排水 → 脱水（高速旋转 10s）→ 完成
   - 输入：`start`、`water_level_ok`、`drain_done`
   - 输出：`water_in_valve`、`motor_forward`、`motor_reverse`、`motor_high_speed`、`drain_pump`、`done_led`

6. 为练习 5 编写完整的 Testbench，模拟一次完整的洗衣流程。

---

## FAQ：常见问题解答

!!! question "Moore 机和 Mealy 机怎么选？"
    - **Moore 机** ：输出稳定（只在时钟边沿变化），适合控制类应用（交通灯、电机控制）
    - **Mealy 机** ：响应更快（输入变化立即影响输出），状态更少，适合检测类应用（序列检测、协议解析）
    - 不确定时， **默认用 Moore 机** ，更安全

!!! question "三段式一定要用三段吗？两段式不行吗？"
    两段式（状态寄存器 + 组合逻辑输出）也可以，但三段式将输出也寄存一拍，能有效过滤组合逻辑的毛刺。对于 FPGA 设计， **推荐三段式** 。

!!! question "状态机中可以用 `=` 吗？"
    - 第一段（状态寄存器）：必须用 `<=`（时序逻辑）
    - 第二段（下一状态逻辑）：必须用 `=`（组合逻辑）
    - 第三段（输出逻辑）：时序输出用 `<=`，组合输出用 `=`

!!! question "状态太多怎么办？"
    如果状态超过 20 个，考虑：
    1. 拆分为多个子状态机（层次化 FSM）
    2. 使用计数器 + 少量状态代替大量状态
    3. 检查是否有冗余状态可以合并

!!! question "`case` 中忘记写 `default` 会怎样？"
    综合工具会推断出锁存器（因为某些状态下 `next_state` 没有被赋值）。这通常不是你想要的。 **始终写 `default` 分支。**

---

**下一章预告：** 在第 8 章中，我们将综合运用前 7 章的知识，从零开始设计一个完整的数字钟——整合计数器、显示译码、按键消抖、闹钟功能，完成从"单个模块"到"完整系统"的跨越。

[继续第 8 章：综合实战项目——数字钟 →](08-digital-clock-project.md)