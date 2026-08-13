# 第 2 章：C/C++ 编译环境 — 把施工图变成机器

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 35 分钟 |
| 核心概念 | 编译器、标准库、C17、C++20、构建产物 |
| 核心比喻 | 编译器把源代码施工图加工成机器能执行的文件 |
| 实践任务 | 编译并运行 C 与 C++ 程序 |
| 难度等级 | ★★☆☆☆ |

## 2.1 选择编译器

初学阶段优先使用系统包管理器安装工具链。不要同时安装多个互不兼容的编译器，再靠猜测决定调用哪个。

=== "Windows"
    推荐使用 Visual Studio Build Tools 的 **Desktop development with C++** 工作负载，或使用 MSYS2/LLVM。安装后在对应开发者终端验证：

    ```powershell
    cl
    ```

    如果使用 MSYS2 UCRT64：

    ```bash
    pacman -Syu
    pacman -S --needed mingw-w64-ucrt-x86_64-toolchain
    gcc --version
    g++ --version
    ```

=== "macOS"
    ```bash
    xcode-select --install
    clang --version
    clang++ --version
    ```

=== "Ubuntu / Debian"
    ```bash
    sudo apt update
    sudo apt install build-essential
    gcc --version
    g++ --version
    ```

## 2.2 编译 C 和 C++

创建 `hello.c`：

```c
#include <stdio.h>

int main(void) {
    puts("Hello, C");
    return 0;
}
```

```bash
cc -std=c17 -Wall -Wextra -pedantic hello.c -o hello
./hello
```

创建 `hello.cpp`：

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, C++\n";
}
```

```bash
c++ -std=c++20 -Wall -Wextra -pedantic hello.cpp -o hello-cpp
./hello-cpp
```

!!! info "编译器和编辑器不是一回事"
    VS Code、Visual Studio、CLion 等编辑器可以调用编译器，但编辑器本身不会替代编译器。遇到“运行按钮不能用”，先在命令行验证工具链。

## ✅ 验证步骤

两个程序都应输出对应的 Hello 文本；编译时打开警告选项，确认没有未处理警告。故意把 C 程序中的分号删掉，观察编译器如何报告错误，再恢复并重新验证。

## 📝 本章总结

- C 和 C++ 通过编译器生成可执行文件。
- 标准选项和警告选项能让错误更早暴露。
- 编辑器是工作界面，编译器才是构建工具。

## ✏️ 课后练习

1. 让 C 程序读取一个整数并输出它的平方。
2. 用 `g++` 编译一个包含函数的 C++ 程序。

## 🔮 下一章预告

下一章会配置 Python、虚拟环境和包管理器，理解“项目依赖隔离”。
