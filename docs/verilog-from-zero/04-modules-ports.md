# 第 4 章：模块与端口

> **从"单个积木"到"乐高城堡"——掌握层次化设计**

---

## 章节概览

| 小节 | 内容 | 核心概念 |
|:---|:---|:---|
| 4.1 | 模块定义 | module 结构、端口声明语法 |
| 4.2 | 端口类型 | input/output/inout 的使用规则 |
| 4.3 | 模块实例化 | 位置映射与名称映射 |
| 4.4 | 层次化设计 | 自顶向下与自底向上的设计方法 |
| 4.5 | 参数化模块 | parameter 的使用与模块复用 |
| 4.6 | 本章练习 | 模块化设计综合练习 |

---

## 4.1 模块定义

### 模块是 Verilog 的基本单元

在 Verilog 中， **一切皆模块** 。一个模块就像一个乐高积木块——有输入接口（凸起）、输出接口（凹槽），内部封装了具体的电路逻辑。

```verilog
module 模块名 (
    // 端口声明
    input  wire 端口1,
    input  wire 端口2,
    output wire 端口3
);

    // 模块内部逻辑
    // ...

endmodule
```

**乐高比喻：** 每个 Verilog 模块 = 一个乐高积木块。积木的凸起是输入端口（接收信号），凹槽是输出端口（发送信号）。多个积木可以拼接成更大的结构。

### 模块的基本结构

```verilog
module full_adder (
    input  wire a,      // 输入：加数 a
    input  wire b,      // 输入：加数 b
    input  wire cin,    // 输入：低位进位
    output wire sum,    // 输出：和
    output wire cout    // 输出：向高位的进位
);

    // 内部逻辑：sum = a ⊕ b ⊕ cin
    assign sum  = a ^ b ^ cin;

    // 内部逻辑：cout = ab + acin + bcin（多数表决）
    assign cout = (a & b) | (a & cin) | (b & cin);

endmodule
```

!!! tip "模块命名规范"
    - 模块名使用 **小写字母 + 下划线** （`full_adder`、`data_memory`）
    - 文件名与模块名保持一致（`full_adder.v`）
    - 一个文件只放一个模块（便于管理和复用）

---

## 4.2 端口类型

### 三种端口方向

| 端口类型 | 方向 | 默认数据类型 | 能否在模块内赋值 | 乐高比喻 |
|:---|:---|:---|:---|:---|
| **input** | 外部 → 模块内部 | `wire` | ❌ 不可赋值 | 积木的凸起（接收） |
| **output** | 模块内部 → 外部 | `wire` | ✅ 可赋值 | 积木的凹槽（输出） |
| **inout** | 双向 | `wire` | ⚠️ 需三态控制 | 双向通道（少见） |

### 端口声明语法

```verilog
// 风格 1：ANSI C 风格（推荐，简洁）
module adder (
    input  wire [7:0] a,     // 端口类型 + 数据类型 + 位宽 + 端口名
    input  wire [7:0] b,
    output wire [7:0] sum,
    output wire       carry
);

// 风格 2：传统风格（旧代码中常见，不推荐）
module adder (a, b, sum, carry);
    input  [7:0] a;
    input  [7:0] b;
    output [7:0] sum;
    output       carry;
```

!!! note "wire 可以省略吗？"
    对于 `input` 和 `output` 端口，`wire` 关键字可以省略（默认就是 `wire`）。但建议 **始终显式写出** ，提高代码可读性。

### output reg 的特殊情况

当输出端口在 `always` 块中被赋值时，需要声明为 `output reg`：

```verilog
module d_flip_flop (
    input  wire clk,
    input  wire d,
    output reg  q      // 注意：output reg，因为 q 在 always 块中被赋值
);

    always @(posedge clk)
        q <= d;

endmodule
```

---

## 4.3 模块实例化

### 什么是实例化？

实例化就是 **使用一个模块** ——就像用乐高积木搭建时，你拿一个积木块放到搭建中的结构上。

```verilog
// 定义了一个与门模块
module and_gate (input a, input b, output y);
    assign y = a & b;
endmodule

// 在另一个模块中实例化（使用）它
module top_module (
    input  wire x1, x2, x3,
    output wire result
);

    wire intermediate;  // 中间连线

    // 实例化第一个与门：计算 x1 & x2
    and_gate u1 (
        .a(x1),
        .b(x2),
        .y(intermediate)
    );

    // 实例化第二个与门：计算 intermediate & x3
    and_gate u2 (
        .a(intermediate),
        .b(x3),
        .y(result)
    );

endmodule
```

### 两种端口连接方式

```verilog
// 方式 1：名称映射（推荐 ✅）
and_gate u1 (
    .a(x1),          // .端口名(连接的信号名)
    .b(x2),
    .y(intermediate)
);

// 方式 2：位置映射（不推荐 ❌，容易出错）
and_gate u1 (x1, x2, intermediate);  // 必须严格按端口声明顺序
```

!!! warning "始终使用名称映射"
    位置映射虽然简短，但端口顺序记错就会导致难以发现的 bug。名称映射自文档化，代码更易读、更安全。

### 实例名的作用

每个实例化都必须有一个唯一的 **实例名** （如 `u1`、`u2`）：

```verilog
and_gate u1 (...);  // u1 是实例名
and_gate u2 (...);  // u2 是另一个实例名
```

实例名用于：
- 在仿真波形中区分不同实例的信号
- 在层次化路径中引用（如 `top.u1.y`）

---

## 4.4 层次化设计

### 自底向上 vs 自顶向下

| 方法 | 流程 | 优点 | 乐高比喻 |
|:---|:---|:---|:---|
| **自底向上** | 先设计小模块，再组合成大模块 | 小模块可复用，易于测试 | 先做好每种积木，再搭建 |
| **自顶向下** | 先定义顶层接口，再逐层分解 | 全局视角清晰，接口明确 | 先画好蓝图，再找需要的积木 |

### 层次化设计示例：4 位加法器

```
4 位加法器（顶层）
├── 全加器 bit0（a[0], b[0], cin → sum[0], c1）
├── 全加器 bit1（a[1], b[1], c1  → sum[1], c2）
├── 全加器 bit2（a[2], b[2], c2  → sum[2], c3）
└── 全加器 bit3（a[3], b[3], c3  → sum[3], cout）
```

```verilog
// 步骤 1：定义全加器模块（底层积木）
module full_adder (
    input  wire a, b, cin,
    output wire sum, cout
);
    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (a & cin) | (b & cin);
endmodule

// 步骤 2：用 4 个全加器搭建 4 位加法器（顶层结构）
module adder_4bit (
    input  wire [3:0] a, b,
    input  wire       cin,
    output wire [3:0] sum,
    output wire       cout
);

    wire c1, c2, c3;  // 内部进位连线

    full_adder fa0 (.a(a[0]), .b(b[0]), .cin(cin),  .sum(sum[0]), .cout(c1));
    full_adder fa1 (.a(a[1]), .b(b[1]), .cin(c1),   .sum(sum[1]), .cout(c2));
    full_adder fa2 (.a(a[2]), .b(b[2]), .cin(c2),   .sum(sum[2]), .cout(c3));
    full_adder fa3 (.a(a[3]), .b(b[3]), .cin(c3),   .sum(sum[3]), .cout(cout));

endmodule
```

**乐高比喻：** 全加器 = 1×2 基础积木。4 位加法器 = 用 4 个 1×2 积木拼成的 1×8 长条。每个积木的进位输出连接到下一个积木的进位输入，形成"进位链"。

---

## 4.5 参数化模块

### 为什么需要参数化？

如果不使用参数，你需要为每种位宽写一个模块：

```verilog
module adder_4bit (...);   // 4 位加法器
module adder_8bit (...);   // 8 位加法器
module adder_16bit (...);  // 16 位加法器
// 大量重复代码！
```

使用参数后，一个模块适配所有位宽：

```verilog
module adder #(
    parameter WIDTH = 8    // 默认位宽为 8
) (
    input  wire [WIDTH-1:0] a,
    input  wire [WIDTH-1:0] b,
    output wire [WIDTH-1:0] sum,
    output wire             cout
);

    assign {cout, sum} = a + b;

endmodule
```

### 参数化模块的实例化

```verilog
// 使用默认位宽（8 位）
adder add8 (.a(a8), .b(b8), .sum(s8), .cout(c8));

// 覆盖参数：实例化 16 位加法器
adder #(.WIDTH(16)) add16 (
    .a(a16), .b(b16), .sum(s16), .cout(c16)
);

// 覆盖参数：实例化 4 位加法器
adder #(.WIDTH(4)) add4 (
    .a(a4), .b(b4), .sum(s4), .cout(c4)
);
```

!!! example "实战：参数化多路选择器"
    ```verilog
    module mux #(
        parameter WIDTH = 8
    ) (
        input  wire             sel,
        input  wire [WIDTH-1:0] a,
        input  wire [WIDTH-1:0] b,
        output wire [WIDTH-1:0] y
    );

        assign y = sel ? a : b;

    endmodule
    ```

### 多参数模块

```verilog
module memory #(
    parameter ADDR_WIDTH = 8,    // 地址位宽
    parameter DATA_WIDTH = 16    // 数据位宽
) (
    input  wire                     clk,
    input  wire                     we,     // 写使能
    input  wire [ADDR_WIDTH-1:0]    addr,
    input  wire [DATA_WIDTH-1:0]    wdata,
    output wire [DATA_WIDTH-1:0]    rdata
);

    // 存储器深度 = 2^ADDR_WIDTH
    reg [DATA_WIDTH-1:0] mem [0:(1<<ADDR_WIDTH)-1];

    always @(posedge clk)
        if (we)
            mem[addr] <= wdata;

    assign rdata = mem[addr];

endmodule
```

---

## 4.6 本章练习

### 基础练习

1. 定义一个名为 `xor_gate` 的模块，实现二输入异或门。

2. 使用名称映射方式实例化练习 1 的 `xor_gate` 模块。

### 层次化设计练习

3. 使用 2.4 节中的 `and_gate` 模块和练习 1 的 `xor_gate` 模块，搭建一个 **半加器** （`half_adder`）：
   - 输入：`a`、`b`
   - 输出：`sum`（= a ^ b）、`carry`（= a & b）

4. 使用两个半加器和一个或门，搭建一个 **全加器** （`full_adder`）。

### 参数化练习

5. 编写一个参数化的 N 位二选一多路选择器，并在 Testbench 中分别实例化 4 位和 8 位版本进行验证。

6. 编写一个参数化的 N 位比较器（输出 `a == b`、`a > b`、`a < b`），验证 4 位和 8 位版本。

### 综合练习

7. 设计一个 4 位算术逻辑单元（ALU），支持以下操作：
   - `op = 2'b00`：加法（`a + b`）
   - `op = 2'b01`：减法（`a - b`）
   - `op = 2'b10`：按位与（`a & b`）
   - `op = 2'b11`：按位或（`a | b`）

---

## FAQ：常见问题解答

!!! question "一个 .v 文件可以放多个模块吗？"
    可以，但 **不推荐** 。最佳实践是每个 `.v` 文件只包含一个模块，文件名与模块名一致。这样便于代码管理和复用。Testbench 可以与被测模块放在同一文件中，但建议分开。

!!! question "实例名可以省略吗？"
    **不可以。** 每个实例化必须有一个唯一的实例名。即使你不关心它叫什么，仿真器和综合工具也需要它来区分不同实例。

!!! question "`parameter` 和 `localparam` 有什么区别？"
    - `parameter`：可以在实例化时从外部覆盖（类似函数的参数）
    - `localparam`：模块内部常量，外部不可覆盖（类似函数的局部常量）
    - 如果某个值不应该被外部修改，使用 `localparam`

!!! question "端口声明中 `wire` 和 `reg` 怎么选？"
    - `input` 端口：始终是 `wire`（外部驱动，内部只读）
    - `output` 端口：`assign` 驱动用 `wire`，`always` 驱动用 `reg`
    - 不确定时，先写 `wire`，编译器会提示你是否需要改为 `reg`

!!! question "层次化太深会影响性能吗？"
    在仿真中，层次化深度不影响仿真性能。在综合中，综合工具会"展平"（flatten）层次结构，优化为最优的门级网表。所以大胆使用层次化设计，它只会让代码更清晰。

---

**下一章预告：** 在第 5 章中，我们将深入学习组合逻辑设计——多路选择器、译码器、编码器、算术电路等，掌握 `assign` 语句和 `always @(*)` 块的用法。

[继续第 5 章：组合逻辑设计 →](05-combinational-logic.md)