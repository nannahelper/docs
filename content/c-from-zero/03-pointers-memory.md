# 第 3 章：指针与内存

指针不是“神秘的变量”，它只是保存地址的对象。真正重要的是：这个地址是否有效、类型是否匹配、生命周期是否结束。

## 3.1 取地址和解引用

```c
int value = 42;
int *pointer = &value;

printf("%d\n", *pointer);
*pointer = 43;
printf("%d\n", value);
```

`&value` 取得地址，`*pointer` 访问该地址对应的值。

## 3.2 用指针修改调用者的数据

```c
void swap(int *left, int *right) {
    int temp = *left;
    *left = *right;
    *right = temp;
}
```

## 3.3 动态内存

```c
#include <stdlib.h>

int *values = malloc(3 * sizeof(*values));
if (values == NULL) {
    return 1;
}

values[0] = 10;
free(values);
values = NULL;
```

每次 `malloc` 都必须有对应的 `free`。释放后把指针设为 `NULL`，可以减少误用悬空指针的风险。

## 本章练习

使用 `malloc` 创建一个由用户指定长度的整数数组，读取数据并计算平均值；检查分配失败，并在所有返回路径释放内存。
