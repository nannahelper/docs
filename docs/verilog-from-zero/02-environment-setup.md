# 第 2 章：开发环境搭建与第一个 Verilog 程序

> **从"安装工具"到"看到波形"——搭建你的数字电路实验室**

---

## 章节概览

| 小节 | 内容 | 核心概念 |
|:---|:---|:---|
| 2.1 | 工具链介绍 | Icarus Verilog、GTKWave、VS Code |
| 2.2 | 安装 Icarus Verilog | Windows/macOS/Linux 安装指南 |
| 2.3 | 安装 GTKWave | 波形查看器安装与配置 |
| 2.4 | 第一个 Verilog 程序 | 与门电路——从代码到波形 |
| 2.5 | 测试平台（Testbench）入门 | 如何验证你的电路 |
| 2.6 | 本章练习 | 环境验证与简单电路仿真 |

---

## 2.1 工具链介绍

### 我们需要什么工具？

本教程使用 **完全免费开源** 的工具链，无需任何商业软件许可证：

| 工具 | 用途 | 乐高比喻 |
|:---|:---|:---|
| **Icarus Verilog（iverilog）** | Verilog 编译和仿真 | 积木搭建模拟器——在电脑上验证你的设计 |
| **GTKWave** | 波形查看器 | 高速摄像机——观察电路中每个信号的变化 |
| **VS Code** | 代码编辑器 | 工作台——编写和整理你的设计文档 |

!!! info "为什么不用 Vivado/Quartus？"
    Vivado（Xilinx）和 Quartus（Intel/Altera）是 FPGA 厂商的完整开发套件，功能强大但安装包巨大（20GB+），且需要注册账号。对于学习 Verilog 语法和仿真验证，Icarus Verilog 完全够用，而且安装只需几 MB。

---

## 2.2 安装 Icarus Verilog

=== "Windows"

    1. 访问 Icarus Verilog 下载页面：[bleyer.org/icarus/](https://bleyer.org/icarus/)
    2. 下载最新版本的安装程序（如 `iverilog-v12-20220611-x64_setup.exe`）
    3. 运行安装程序， **勾选"Add to PATH"** 选项
    4. 安装完成后，打开 **命令提示符** 或 **PowerShell** ，验证安装：

    ```powershell
    iverilog -v
    ```

    预期输出类似：

    ```
    Icarus Verilog version 12.0 (stable) (...)
    ```

=== "macOS"

    使用 Homebrew 安装：

    ```bash
    brew install icarus-verilog
    ```

    验证安装：

    ```bash
    iverilog -v
    ```

=== "Linux (Ubuntu/Debian)"

    ```bash
    sudo apt update
    sudo apt install iverilog
    ```

    验证安装：

    ```bash
    iverilog -v
    ```

!!! warning "PATH 环境变量"
    如果命令行提示 `iverilog` 命令找不到，说明 PATH 环境变量未正确配置。Windows 用户请重新运行安装程序并确保勾选"Add to PATH"；或手动将 Icarus Verilog 的 `bin` 目录添加到系统环境变量中。

---

## 2.3 安装 GTKWave

=== "Windows"

    1. 访问 GTKWave 下载页面：[sourceforge.net/projects/gtkwave/](https://sourceforge.net/projects/gtkwave/)
    2. 下载最新版本的安装程序
    3. 运行安装程序，同样 **勾选"Add to PATH"**
    4. 验证安装：

    ```powershell
    gtkwave --version
    ```

=== "macOS"

    ```bash
    brew install gtkwave
    ```

=== "Linux (Ubuntu/Debian)"

    ```bash
    sudo apt install gtkwave
    ```

---

## 2.4 第一个 Verilog 程序：与门电路

### 设计目标

实现一个简单的二输入与门：`y = a & b`

**乐高比喻：** 这就像搭建一个最基础的乐高结构——两块积木（a 和 b）通过一个连接件（与门）组合在一起，产生输出（y）。

### 步骤 1：创建项目目录

```powershell
mkdir verilog-lab
cd verilog-lab
```

### 步骤 2：编写 Verilog 设计文件

创建文件 `and_gate.v`：

```verilog
// and_gate.v —— 二输入与门
module and_gate (
    input  wire a,    // 输入端口 a（1 位宽）
    input  wire b,    // 输入端口 b（1 位宽）
    output wire y     // 输出端口 y（1 位宽）
);

    // assign 语句：建立持续的连接关系
    // y 始终等于 a & b，当 a 或 b 变化时 y 自动更新
    assign y = a & b;

endmodule
```

**逐行解释：**

| 代码行 | 解释 |
|:---|:---|
| `module and_gate (...)` | 定义一个名为 `and_gate` 的模块（类似软件中的"函数"） |
| `input wire a,` | 声明输入端口 `a`，`wire` 表示这是连线类型 |
| `output wire y` | 声明输出端口 `y` |
| `assign y = a & b;` | 持续赋值：`y` 始终等于 `a` 与 `b` 的结果 |
| `endmodule` | 模块定义结束 |

### 步骤 3：编写测试平台（Testbench）

创建文件 `and_gate_tb.v`：

```verilog
// and_gate_tb.v —— 与门测试平台
`timescale 1ns / 1ps    // 时间单位：1ns，仿真精度：1ps

module and_gate_tb;

    // 声明测试用的信号
    reg  a;    // reg 类型：用于在测试平台中驱动信号
    reg  b;
    wire y;    // wire 类型：用于接收被测模块的输出

    // 实例化被测模块（将测试信号连接到被测模块的端口）
    and_gate uut (
        .a(a),   // 将测试信号 a 连接到模块端口 a
        .b(b),   // 将测试信号 b 连接到模块端口 b
        .y(y)    // 将模块端口 y 连接到测试信号 y
    );

    // 初始块：定义测试激励（输入信号的波形）
    initial begin
        // 生成 VCD 文件用于 GTKWave 查看波形
        $dumpfile("and_gate_tb.vcd");
        $dumpvars(0, and_gate_tb);

        // 测试用例 1：a=0, b=0 → 期望 y=0
        a = 0; b = 0;
        #10;    // 等待 10 个时间单位（10ns）

        // 测试用例 2：a=0, b=1 → 期望 y=0
        a = 0; b = 1;
        #10;

        // 测试用例 3：a=1, b=0 → 期望 y=0
        a = 1; b = 0;
        #10;

        // 测试用例 4：a=1, b=1 → 期望 y=1
        a = 1; b = 1;
        #10;

        // 仿真结束
        $finish;
    end

endmodule
```

**逐行解释：**

| 代码行 | 解释 |
|:---|:---|
| `` `timescale 1ns / 1ps `` | 设置仿真时间单位和精度 |
| `reg a; reg b;` | `reg` 类型变量可以在 `initial` 块中赋值，用于产生测试激励 |
| `wire y;` | `wire` 类型变量用于连接被测模块的输出 |
| `and_gate uut (...)` | 实例化被测模块，`uut` 是实例名（Unit Under Test） |
| `.a(a)` | 端口连接：将外部信号 `a` 连接到模块端口 `a` |
| `initial begin ... end` | 仿真开始时执行一次，定义测试激励序列 |
| `$dumpfile(...)` | 指定波形输出文件名 |
| `$dumpvars(...)` | 指定要记录波形的信号 |
| `#10;` | 延时 10 个时间单位（此处为 10ns） |
| `$finish;` | 结束仿真 |

### 步骤 4：编译和仿真

在命令行中执行：

```powershell
iverilog -o and_gate_tb.vvp and_gate.v and_gate_tb.v
```

参数解释：
- `-o and_gate_tb.vvp`：指定输出文件名（vvp = Verilog VPI Program）
- `and_gate.v and_gate_tb.v`：需要编译的源文件（设计文件 + 测试平台）

编译成功后，运行仿真：

```powershell
vvp and_gate_tb.vvp
```

预期输出：

```
VCD info: dumpfile and_gate_tb.vcd opened for output.
```

仿真完成后，目录中会生成 `and_gate_tb.vcd` 波形文件。

### 步骤 5：查看波形

```powershell
gtkwave and_gate_tb.vcd
```

在 GTKWave 中：
1. 左侧 **SST** 面板展开 `and_gate_tb` → 选中 `a`、`b`、`y`
2. 点击左下角 **Append** 按钮将信号添加到波形窗口
3. 观察波形，验证与门真值表：

```
a: ___---___---    （0→1→0→1）
b: ___---___---    （0→0→1→1）
y: ______---___    （0→0→0→1）✅ 符合与门真值表
```

!!! tip "GTKWave 快捷键"
    - `Ctrl+滚轮`：缩放波形
    - `鼠标左键拖拽`：移动波形
    - `鼠标中键点击`：跳转到该时间点

---

## 2.5 测试平台（Testbench）入门

### Testbench 的本质

Testbench 也是一个 Verilog 模块，但它 **不会被综合成实际电路** ——它只存在于仿真环境中，用于产生测试激励和检查输出结果。

**乐高比喻：** Testbench 就像积木的"质量检测台"——你不需要把它放进最终产品，但它能帮你验证每个积木块是否正常工作。

### Testbench 的标准结构

```verilog
`timescale 1ns / 1ps

module [被测模块名]_tb;

    // 1. 信号声明
    reg  [输入信号];
    wire [输出信号];

    // 2. 实例化被测模块
    [模块名] uut (
        .端口1(信号1),
        .端口2(信号2),
        ...
    );

    // 3. 波形记录
    initial begin
        $dumpfile("[文件名].vcd");
        $dumpvars(0, [模块名]_tb);
    end

    // 4. 测试激励
    initial begin
        // 初始化
        [输入] = 初始值;
        #延时;

        // 测试用例1
        [输入] = 测试值;
        #延时;

        // 测试用例2
        ...

        $finish;
    end

endmodule
```

!!! note "reg vs wire 在 Testbench 中的使用"
    - 驱动被测模块输入的信号用 `reg`（因为需要在 `initial` 块中赋值）
    - 接收被测模块输出的信号用 `wire`（因为是被动接收）

---

## 2.6 本章练习

### 环境验证

1. 在命令行中运行 `iverilog -v` 和 `gtkwave --version`，确认两个工具都已正确安装。

### 基础仿真

2. 完成 2.4 节的与门仿真，截取 GTKWave 波形图。

3. 修改 `and_gate.v`，实现一个 **或门** （`y = a | b`），编写对应的 Testbench，仿真并验证波形。

4. 修改设计文件，实现一个 **异或门** （`y = a ^ b`），仿真验证。

### 多输入门

5. 实现一个 **三输入与门** （`y = a & b & c`），编写 Testbench 覆盖所有 8 种输入组合（000~111），验证波形。

### 思考题

6. 在 Testbench 中，`#10;` 表示延时 10ns。如果改为 `#5;`，波形会有什么变化？

7. 如果 Testbench 中忘记写 `$dumpfile` 和 `$dumpvars`，会发生什么？

---

## FAQ：常见问题解答

!!! question "iverilog 编译报错 `syntax error` 怎么办？"
    最常见的语法错误是 **忘记分号** 。Verilog 中每条语句必须以 `;` 结尾。检查报错行号附近是否有遗漏的分号。

!!! question "vvp 运行后没有生成 .vcd 文件？"
    检查 Testbench 中是否包含了 `$dumpfile` 和 `$dumpvars` 语句。这两个系统任务是生成波形文件的关键。

!!! question "GTKWave 打开后看不到信号？"
    在左侧 SST 面板中，点击模块名展开信号列表，选中信号后点击左下角的 **Append** 按钮。信号不会自动显示。

!!! question "为什么 Testbench 中 a、b 用 reg，y 用 wire？"
    因为 `a` 和 `b` 需要在 `initial` 块中被赋值（驱动），只有 `reg` 类型可以在 `initial` 块中赋值。`y` 是被动接收模块输出的，所以用 `wire`。

!!! question "`timescale 1ns / 1ps` 是什么意思？"
    `1ns` 是仿真时间单位——`#10` 表示延时 10ns。`1ps` 是仿真精度——仿真器的最小时间步长。对于初学者，使用默认值即可。

---

**下一章预告：** 在第 3 章中，我们将深入学习 Verilog 的数据类型（wire、reg、向量、数组）和运算符，理解它们与软件语言中"变量"的本质区别。