# 第 6 章：时序逻辑设计

> **从"存钱罐"到"时间旅行者"——掌握有记忆电路设计**

---

## 章节概览

| 小节 | 内容 | 核心概念 |
|:---|:---|:---|
| 6.1 | 时序逻辑概述 | 时钟、复位、记忆元件 |
| 6.2 | D 触发器 | 最基本的时序元件 |
| 6.3 | 寄存器 | 多位数据存储与使能控制 |
| 6.4 | 计数器 | 二进制计数器、模 N 计数器 |
| 6.5 | 移位寄存器 | 串并转换、并串转换 |
| 6.6 | 时钟分频 | 分频器设计与应用 |
| 6.7 | 本章练习 | 时序逻辑综合练习 |

---

## 6.1 时序逻辑概述

### 什么是时序逻辑？

**时序逻辑** 是数字电路的另一基本类型。它的核心特征： **输出不仅取决于当前输入，还取决于电路的历史状态** 。

**乐高比喻：** 时序逻辑 = 存钱罐——你每次投币（输入），存钱罐里的钱（状态）都会变化。要知道现在有多少钱，你需要知道"之前投了多少"（历史状态）。

| 特性 | 组合逻辑 | 时序逻辑 |
|:---|:---|:---|
| **记忆能力** | 无 | 有 |
| **时钟依赖** | 不需要 | 需要时钟信号 |
| **Verilog 实现** | `assign` / `always @(*)` | `always @(posedge clk)` |
| **赋值方式** | 阻塞赋值 `=` | 非阻塞赋值 `<=` |
| **典型电路** | 门电路、选择器、加法器 | 触发器、计数器、状态机 |

### 时钟信号

时钟是时序逻辑的"心跳"——所有状态更新都在时钟边沿发生：

```
         ┌───┐   ┌───┐   ┌───┐   ┌───┐
clk: ────┘   └───┘   └───┘   └───┘   └───
         ↑       ↑       ↑       ↑
      上升沿   上升沿   上升沿   上升沿
     (posedge)(posedge)(posedge)(posedge)
```

**乐高比喻：** 时钟 = 节拍器。乐队中所有人跟着节拍器同步演奏，数字电路中所有时序元件跟着时钟同步更新。

### 复位信号

复位将电路恢复到已知的初始状态：

| 复位类型 | 触发条件 | 优点 | 缺点 |
|:---|:---|:---|:---|
| **同步复位** | 时钟边沿 + 复位有效 | 抗毛刺、时序可控 | 需要时钟工作 |
| **异步复位** | 复位有效（无需时钟） | 上电即复位、不依赖时钟 | 释放时可能产生亚稳态 |

```verilog
// 同步复位
always @(posedge clk) begin
    if (rst)
        q <= 1'b0;
    else
        q <= d;
end

// 异步复位（复位信号加入敏感列表）
always @(posedge clk or posedge rst) begin
    if (rst)
        q <= 1'b0;
    else
        q <= d;
end
```

!!! tip "复位策略建议"
    对于 FPGA 设计，推荐使用 **异步复位 + 同步释放** 的方式。本教程的示例使用同步复位以简化理解。

---

## 6.2 D 触发器

### 最基本的时序元件

D 触发器（D Flip-Flop）是时序逻辑的最小构建单元：

```verilog
module d_flip_flop (
    input  wire clk,
    input  wire rst,
    input  wire d,
    output reg  q
);

    always @(posedge clk) begin
        if (rst)
            q <= 1'b0;     // 复位时输出 0
        else
            q <= d;        // 时钟上升沿，将 d 的值传递给 q
    end

endmodule
```

**乐高比喻：** D 触发器 = 一个带时钟控制的"传送门"。时钟上升沿时，门打开一瞬间，输入 `d` 的值穿过门到达输出 `q`。其他时间门关闭，`q` 保持原值不变。

### 带使能的 D 触发器

```verilog
module d_flip_flop_en (
    input  wire clk,
    input  wire rst,
    input  wire en,      // 使能信号
    input  wire d,
    output reg  q
);

    always @(posedge clk) begin
        if (rst)
            q <= 1'b0;
        else if (en)
            q <= d;        // 仅当 en=1 时更新
        // en=0 时 q 保持原值（不写 else 分支）
    end

endmodule
```

!!! warning "非阻塞赋值 `<=`"
    时序逻辑中 **必须使用非阻塞赋值 `<=`** 。`<=` 的含义是"在当前时钟边沿，所有 `<=` 赋值同时采样右侧值，在时钟周期结束时统一更新左侧值"。这模拟了硬件中触发器的真实行为。

---

## 6.3 寄存器

### 多位寄存器

寄存器就是多位宽的 D 触发器：

```verilog
module register #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,
    input  wire             en,
    input  wire [WIDTH-1:0] d,
    output reg  [WIDTH-1:0] q
);

    always @(posedge clk) begin
        if (rst)
            q <= {WIDTH{1'b0}};   // 复位为全 0
        else if (en)
            q <= d;
    end

endmodule
```

### 寄存器堆（Register File）

```verilog
module register_file #(
    parameter ADDR_WIDTH = 3,     // 3 位地址 → 8 个寄存器
    parameter DATA_WIDTH = 8
) (
    input  wire                     clk,
    input  wire                     we,         // 写使能
    input  wire [ADDR_WIDTH-1:0]    raddr,      // 读地址
    input  wire [ADDR_WIDTH-1:0]    waddr,      // 写地址
    input  wire [DATA_WIDTH-1:0]    wdata,      // 写数据
    output wire [DATA_WIDTH-1:0]    rdata       // 读数据
);

    reg [DATA_WIDTH-1:0] regs [0:(1<<ADDR_WIDTH)-1];

    // 写操作（时序逻辑）
    always @(posedge clk) begin
        if (we)
            regs[waddr] <= wdata;
    end

    // 读操作（组合逻辑）
    assign rdata = regs[raddr];

endmodule
```

---

## 6.4 计数器

### 二进制加法计数器

```verilog
module counter #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,
    input  wire             en,
    output reg  [WIDTH-1:0] count
);

    always @(posedge clk) begin
        if (rst)
            count <= {WIDTH{1'b0}};
        else if (en)
            count <= count + 1'b1;
    end

endmodule
```

### 模 N 计数器（计数到 N-1 后归零）

```verilog
module mod_n_counter #(
    parameter N = 10,          // 模值（计数 0~N-1）
    parameter WIDTH = 4        // 位宽（需满足 2^WIDTH >= N）
) (
    input  wire             clk,
    input  wire             rst,
    input  wire             en,
    output reg  [WIDTH-1:0] count,
    output reg              overflow   // 计数到 N-1 时输出 1
);

    always @(posedge clk) begin
        if (rst) begin
            count <= {WIDTH{1'b0}};
            overflow <= 1'b0;
        end else if (en) begin
            if (count == N - 1) begin
                count <= {WIDTH{1'b0}};
                overflow <= 1'b1;
            end else begin
                count <= count + 1'b1;
                overflow <= 1'b0;
            end
        end
    end

endmodule
```

!!! example "实战：模 10 计数器（BCD 码）"
    ```verilog
    // 实例化：0→1→2→...→9→0→1→...
    mod_n_counter #(.N(10), .WIDTH(4)) bcd_counter (
        .clk(clk),
        .rst(rst),
        .en(1'b1),
        .count(bcd_count),
        .overflow()
    );
    ```

### 可逆计数器

```verilog
module up_down_counter #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,
    input  wire             en,
    input  wire             up_down,   // 1=加, 0=减
    output reg  [WIDTH-1:0] count
);

    always @(posedge clk) begin
        if (rst)
            count <= {WIDTH{1'b0}};
        else if (en) begin
            if (up_down)
                count <= count + 1'b1;
            else
                count <= count - 1'b1;
        end
    end

endmodule
```

---

## 6.5 移位寄存器

### 基本移位寄存器

```verilog
module shift_register #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,
    input  wire             en,
    input  wire             shift_in,   // 串行输入
    input  wire             direction,  // 0=右移, 1=左移
    output reg  [WIDTH-1:0] q,
    output wire             shift_out   // 串行输出
);

    always @(posedge clk) begin
        if (rst)
            q <= {WIDTH{1'b0}};
        else if (en) begin
            if (direction)
                q <= {q[WIDTH-2:0], shift_in};  // 左移
            else
                q <= {shift_in, q[WIDTH-1:1]};  // 右移
        end
    end

    assign shift_out = direction ? q[WIDTH-1] : q[0];

endmodule
```

### 串并转换（SIPO）

```verilog
module sipo #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,
    input  wire             serial_in,
    output reg  [WIDTH-1:0] parallel_out,
    output reg              data_ready   // 8 位数据接收完成
);

    reg [2:0] bit_count;  // 计数 0~7

    always @(posedge clk) begin
        if (rst) begin
            parallel_out <= {WIDTH{1'b0}};
            bit_count <= 3'b0;
            data_ready <= 1'b0;
        end else begin
            parallel_out <= {parallel_out[WIDTH-2:0], serial_in};
            if (bit_count == 3'd7) begin
                bit_count <= 3'b0;
                data_ready <= 1'b1;
            end else begin
                bit_count <= bit_count + 1'b1;
                data_ready <= 1'b0;
            end
        end
    end

endmodule
```

---

## 6.6 时钟分频

### 偶数分频器

```verilog
module clock_divider_even #(
    parameter DIV = 4     // 分频系数（偶数）
) (
    input  wire clk_in,
    input  wire rst,
    output reg  clk_out
);

    reg [$clog2(DIV)-1:0] counter;  // $clog2 计算位宽

    always @(posedge clk_in) begin
        if (rst) begin
            counter <= 0;
            clk_out <= 1'b0;
        end else begin
            if (counter == DIV/2 - 1) begin
                counter <= 0;
                clk_out <= ~clk_out;   // 翻转输出
            end else begin
                counter <= counter + 1'b1;
            end
        end
    end

endmodule
```

!!! warning "分频时钟的使用限制"
    在 FPGA 设计中， **不要用分频后的信号作为新时钟域** 。应使用 FPGA 内部的 PLL/MMCM 产生所需频率的时钟，或使用时钟使能信号代替分频时钟。

---

## 6.7 本章练习

### 基础练习

1. 实现一个带异步复位的 D 触发器，编写 Testbench 验证复位和正常工作的波形。

2. 实现一个 4 位寄存器，带使能控制，验证写入和保持功能。

### 计数器练习

3. 实现一个模 60 计数器（用于时钟的秒/分计数），编写 Testbench 验证 0→59→0 的循环。

4. 实现一个带使能和同步清零的 8 位可逆计数器。

### 移位寄存器练习

5. 实现一个 8 位串入并出（SIPO）移位寄存器，输入串行数据 `8'b10110010`，验证并行输出。

6. 实现一个 8 位并入串出（PISO）移位寄存器。

### 综合练习

7. 设计一个"数字跑表"的核心计时模块：
   - 输入：`clk`（100MHz）、`rst`、`start`、`stop`
   - 输出：`[23:0] time`（BCD 格式：HH:MM:SS，每个字段 8 位）
   - 功能：`start` 开始计时，`stop` 停止，`rst` 清零

8. 为练习 7 编写完整的 Testbench，模拟启动→计时→停止→清零的完整流程。

---

## FAQ：常见问题解答

!!! question "阻塞赋值 `=` 和非阻塞赋值 `<=` 到底有什么区别？"
    - `=`（阻塞）：立即生效，下一条语句看到的是更新后的值。用于组合逻辑。
    - `<=`（非阻塞）：所有右侧值在时钟边沿同时采样，所有左侧值在时钟周期结束时同时更新。用于时序逻辑。
    - 在时序逻辑中用 `=` 会导致仿真行为与硬件行为不一致（竞争条件）。

!!! question "同步复位和异步复位怎么选？"
    - **同步复位** ：更安全，时序可控，推荐用于大多数设计。
    - **异步复位** ：上电即复位，不依赖时钟。但释放时需要"同步释放"电路避免亚稳态。
    - 本教程示例使用同步复位以简化理解。

!!! question "计数器溢出后会发生什么？"
    取决于你的代码。如果没有写溢出处理逻辑，计数器会从最大值翻转到 0（二进制回绕）。例如 8 位计数器 255→0。如果需要特定模值（如模 60），必须在代码中显式处理。

!!! question "为什么 FPGA 中不推荐用分频时钟？"
    FPGA 有专用的时钟网络（Clock Tree），用 PLL/MMCM 产生的时钟才能走这些专用网络。分频逻辑产生的信号走的是普通数据路径，时钟质量差（抖动大、偏斜大），可能导致时序违规。

!!! question "`$clog2` 是什么？"
    `$clog2` 是 Verilog-2005 引入的系统函数，返回以 2 为底的对数向上取整。例如 `$clog2(10) = 4`（因为 $2^3=8 < 10 \leq 2^4=16$）。常用于计算计数器的位宽。

---

**下一章预告：** 在第 7 章中，我们将学习状态机设计——Moore 机和 Mealy 机的区别、状态编码策略，并通过交通灯控制器实战掌握 FSM 设计方法。