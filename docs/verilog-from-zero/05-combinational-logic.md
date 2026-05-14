# 第 5 章：组合逻辑设计

> **从"自动售货机"到"数据高速公路"——掌握无记忆电路设计**

---

## 章节概览

| 小节 | 内容 | 核心概念 |
|:---|:---|:---|
| 5.1 | 组合逻辑概述 | 什么是组合逻辑、assign 与 always 对比 |
| 5.2 | assign 语句详解 | 持续赋值、条件赋值、位操作 |
| 5.3 | always @(*) 块 | 过程赋值、敏感列表、阻塞赋值 |
| 5.4 | 多路选择器 | 二选一、四选一、参数化多路选择器 |
| 5.5 | 译码器与编码器 | 3-8 译码器、8-3 优先编码器 |
| 5.6 | 算术电路 | 加法器、比较器、ALU |
| 5.7 | 本章练习 | 组合逻辑综合练习 |

---

## 5.1 组合逻辑概述

### 什么是组合逻辑？

**组合逻辑** 是数字电路的两大基本类型之一。它的核心特征： **输出仅取决于当前输入，没有任何记忆功能** 。

**乐高比喻：** 组合逻辑 = 自动售货机——你投什么硬币（输入），就出什么商品（输出）。售货机不记得你上次买了什么，每次都是"根据当前投币，决定当前出货"。

| 特性 | 组合逻辑 | 时序逻辑（第 6 章） |
|:---|:---|:---|
| **记忆能力** | 无 | 有（能记住过去的状态） |
| **输出决定因素** | 仅当前输入 | 当前输入 + 历史状态 |
| **时钟依赖** | 不需要时钟 | 需要时钟驱动 |
| **典型电路** | 与门、或门、多路选择器、加法器 | 计数器、寄存器、状态机 |
| **Verilog 实现** | `assign` 或 `always @(*)` | `always @(posedge clk)` |

### 两种实现方式

```verilog
// 方式 1：assign 语句（适合简单逻辑）
assign y = (a & b) | (c & d);

// 方式 2：always @(*) 块（适合复杂逻辑）
always @(*) begin
    if (sel)
        y = a;
    else
        y = b;
end
```

!!! note "两种方式等价吗？"
    在功能上等价，综合结果也相同。选择哪种取决于代码可读性：
    - 简单表达式 → `assign`
    - 复杂条件/多分支 → `always @(*)`

---

## 5.2 assign 语句详解

### 基本语法

```verilog
assign [驱动强度] [延时] 目标信号 = 表达式;
```

对于可综合设计，我们只关心基本形式：

```verilog
assign y = a & b;           // 简单逻辑运算
assign y = sel ? a : b;     // 条件选择
assign y = {a[3:0], b[3:0]}; // 拼接
```

### 条件赋值实现多路选择

```verilog
// 四选一多路选择器
module mux_4to1 (
    input  wire [1:0] sel,
    input  wire [7:0] d0, d1, d2, d3,
    output wire [7:0] y
);

    assign y = (sel == 2'b00) ? d0 :
               (sel == 2'b01) ? d1 :
               (sel == 2'b10) ? d2 :
                                d3;  // sel == 2'b11

endmodule
```

!!! warning "嵌套条件运算符的可读性"
    嵌套超过 3 层的条件运算符会严重降低可读性。复杂的选择逻辑建议使用 `always @(*)` + `case` 语句。

---

## 5.3 always @(*) 块

### 什么是 always 块？

`always` 块是 Verilog 中最重要的过程块。对于组合逻辑，使用 `always @(*)`：

```verilog
always @(*) begin
    // 组合逻辑描述
    // 当任何输入信号变化时，块内的语句重新执行
end
```

`@(*)` 是 **自动敏感列表** ——编译器自动将所有输入信号加入敏感列表，避免遗漏。

!!! warning "组合逻辑 always 块的陷阱"
    在 `always @(*)` 块中描述组合逻辑时， **必须使用阻塞赋值 `=`** ，且 **必须为所有分支赋值** ，否则会推断出锁存器（latch）。

### 避免锁存器

```verilog
// ❌ 错误：else 分支未赋值 → 综合出锁存器
always @(*) begin
    if (enable)
        y = a;
    // 缺少 else！当 enable=0 时 y 保持原值 → 需要记忆 → 锁存器
end

// ✅ 正确：所有分支都赋值
always @(*) begin
    if (enable)
        y = a;
    else
        y = 1'b0;  // 明确赋默认值
end
```

!!! danger "锁存器（Latch）的危害"
    锁存器在 FPGA 设计中通常是 **不期望的** 。它会导致时序分析困难、亚稳态风险增加。绝大多数情况下，锁存器的出现意味着你的代码有 bug。

### case 语句

```verilog
always @(*) begin
    case (sel)
        2'b00: y = d0;
        2'b01: y = d1;
        2'b10: y = d2;
        2'b11: y = d3;
        default: y = 1'b0;  // 必须有 default，避免锁存器
    endcase
end
```

!!! tip "case 语句最佳实践"
    - **始终写 `default` 分支** ，即使你认为所有情况都已覆盖
    - 使用 `casez` 处理无关位（`?` 表示不关心），但谨慎使用

---

## 5.4 多路选择器

### 二选一多路选择器

```verilog
module mux_2to1 (
    input  wire sel,
    input  wire [7:0] a,
    input  wire [7:0] b,
    output wire [7:0] y
);

    assign y = sel ? a : b;

endmodule
```

### 参数化多路选择器

```verilog
module mux #(
    parameter SEL_WIDTH = 2,     // 选择信号位宽
    parameter DATA_WIDTH = 8     // 数据位宽
) (
    input  wire [SEL_WIDTH-1:0]              sel,
    input  wire [(1<<SEL_WIDTH)*DATA_WIDTH-1:0] data_in,  // 扁平化输入
    output wire [DATA_WIDTH-1:0]             y
);

    // 将扁平化输入拆分为独立通道
    // 使用 generate 或 case 选择
    // （此处简化，实际实现略）

endmodule
```

---

## 5.5 译码器与编码器

### 3-8 译码器

3 位输入 → 8 位输出（独热码）：

```verilog
module decoder_3to8 (
    input  wire [2:0] addr,
    input  wire       en,       // 使能信号
    output reg  [7:0] y
);

    always @(*) begin
        if (en) begin
            case (addr)
                3'b000: y = 8'b0000_0001;
                3'b001: y = 8'b0000_0010;
                3'b010: y = 8'b0000_0100;
                3'b011: y = 8'b0000_1000;
                3'b100: y = 8'b0001_0000;
                3'b101: y = 8'b0010_0000;
                3'b110: y = 8'b0100_0000;
                3'b111: y = 8'b1000_0000;
                default: y = 8'b0000_0000;
            endcase
        end else begin
            y = 8'b0000_0000;   // 未使能时输出全 0
        end
    end

endmodule
```

**更优雅的写法（使用移位）：**

```verilog
module decoder_3to8_compact (
    input  wire [2:0] addr,
    input  wire       en,
    output wire [7:0] y
);

    assign y = en ? (8'b0000_0001 << addr) : 8'b0000_0000;

endmodule
```

### 8-3 优先编码器

8 位输入 → 3 位编码输出（高位优先）：

```verilog
module priority_encoder_8to3 (
    input  wire [7:0] d,
    output reg  [2:0] y,
    output reg        valid   // 指示是否有有效输入
);

    always @(*) begin
        valid = 1'b1;
        casez (d)           // casez：? 表示不关心的位
            8'b1???_????: y = 3'b111;  // d[7] = 1
            8'b01??_????: y = 3'b110;  // d[6] = 1
            8'b001?_????: y = 3'b101;  // d[5] = 1
            8'b0001_????: y = 3'b100;  // d[4] = 1
            8'b0000_1???: y = 3'b011;  // d[3] = 1
            8'b0000_01??: y = 3'b010;  // d[2] = 1
            8'b0000_001?: y = 3'b001;  // d[1] = 1
            8'b0000_0001: y = 3'b000;  // d[0] = 1
            default: begin
                y = 3'b000;
                valid = 1'b0;           // 无有效输入
            end
        endcase
    end

endmodule
```

---

## 5.6 算术电路

### 加法器

```verilog
module adder #(
    parameter WIDTH = 8
) (
    input  wire [WIDTH-1:0] a,
    input  wire [WIDTH-1:0] b,
    input  wire             cin,
    output wire [WIDTH-1:0] sum,
    output wire             cout
);

    assign {cout, sum} = a + b + cin;

endmodule
```

### 比较器

```verilog
module comparator #(
    parameter WIDTH = 8
) (
    input  wire [WIDTH-1:0] a,
    input  wire [WIDTH-1:0] b,
    output wire             eq,   // a == b
    output wire             gt,   // a > b
    output wire             lt    // a < b
);

    assign eq = (a == b);
    assign gt = (a > b);
    assign lt = (a < b);

endmodule
```

### 简单 ALU

```verilog
module alu #(
    parameter WIDTH = 8
) (
    input  wire [1:0]       op,     // 操作码
    input  wire [WIDTH-1:0] a,
    input  wire [WIDTH-1:0] b,
    output reg  [WIDTH-1:0] result,
    output reg              zero    // 结果为零标志
);

    always @(*) begin
        case (op)
            2'b00: result = a + b;      // 加法
            2'b01: result = a - b;      // 减法
            2'b10: result = a & b;      // 按位与
            2'b11: result = a | b;      // 按位或
            default: result = {WIDTH{1'b0}};
        endcase
        zero = (result == 0);
    end

endmodule
```

---

## 5.7 本章练习

### 基础练习

1. 使用 `assign` 语句实现一个 4 输入与门（`y = a & b & c & d`）。

2. 使用 `always @(*)` 块实现一个 4 输入或门。

### 多路选择器练习

3. 实现一个 8 位宽的四选一多路选择器，编写 Testbench 覆盖所有选择组合。

4. 使用嵌套的三目运算符实现一个 4 位宽的四选一多路选择器。

### 译码器练习

5. 实现一个带使能信号的 2-4 译码器，编写 Testbench 验证。

6. 使用移位运算符重写 3-8 译码器，对比两种实现方式的代码量。

### 算术电路练习

7. 实现一个 4 位 ALU，支持 8 种操作（加法、减法、与、或、异或、左移、右移、比较），编写 Testbench 验证所有操作。

### 综合练习

8. 设计一个"简单计算器"：输入两个 4 位数和一个 2 位操作码，输出 8 位结果。支持加减乘除（乘法用重复加法实现，除法输出商和余数）。

---

## FAQ：常见问题解答

!!! question "`assign` 和 `always @(*)` 有什么区别？什么时候用哪个？"
    - `assign`：简洁，适合简单表达式和条件选择。一行代码搞定。
    - `always @(*)`：灵活，适合复杂条件（`if-else`、`case`）、多分支逻辑。
    - 综合结果相同，选择取决于代码可读性。

!!! question "为什么我的 `always @(*)` 块综合出了锁存器？"
    因为你在某些分支中没有给输出赋值。组合逻辑的 `always` 块中， **每个输出信号在所有可能的分支中都必须被赋值** 。使用 `default` 分支或在开头赋默认值可以避免。

!!! question "`case`、`casez`、`casex` 有什么区别？"
    - `case`：精确匹配，所有位必须完全相等
    - `casez`：`?` 或 `z` 表示不关心的位（推荐用于优先编码器）
    - `casex`：`?`、`z`、`x` 都表示不关心的位（ **不推荐** ，`x` 可能掩盖真实 bug）

!!! question "组合逻辑中可以用 `<=`（非阻塞赋值）吗？"
    **不要。** 组合逻辑中始终使用 `=`（阻塞赋值）。`<=` 用于时序逻辑。混用会导致仿真与综合行为不一致。

!!! question "多路选择器的输入太多怎么办？"
    使用 `case` 语句 + `always @(*)` 块。对于超大型多路选择器（如 32 选 1），综合工具会自动优化为最优结构（可能是多级选择器树）。

---

**下一章预告：** 在第 6 章中，我们将进入时序逻辑的世界——时钟、复位、D 触发器、计数器、寄存器，理解"有记忆"的电路如何工作。