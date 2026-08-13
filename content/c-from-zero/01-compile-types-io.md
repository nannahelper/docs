# 第 1 章：编译、类型与输入输出

## 1.1 第一个 C 程序

```c
#include <stdio.h>

int main(void) {
    printf("Hello, C!\n");
    return 0;
}
```

保存为 `hello.c`，编译并运行：

```bash
cc -std=c17 -Wall -Wextra -pedantic hello.c -o hello
./hello
```

编译器会把源代码翻译为可执行文件。`-Wall -Wextra` 会打开重要警告，学习阶段不要忽略警告。

## 1.2 类型和变量

```c
int count = 3;
double price = 12.5;
char grade = 'A';
```

变量的类型决定它能表示什么，以及编译器如何解释内存中的位。

## 1.3 读取输入

```c
int age = 0;
printf("Age: ");
if (scanf("%d", &age) == 1) {
    printf("Next year: %d\n", age + 1);
}
```

`scanf` 需要变量地址，因此传入 `&age`。输入函数的返回值要检查，否则错误输入可能让程序继续使用无效数据。

## 本章练习

写一个程序，读取商品单价和数量，输出总价。编译时打开全部常用警告，并修复编译器给出的警告。
