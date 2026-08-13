# 第 4 章：结构体、文件与模块

## 4.1 用结构体描述对象

```c
typedef struct {
    char name[64];
    char phone[32];
} Contact;
```

结构体把相关字段组合成一个有意义的类型。

## 4.2 文件读写

```c
FILE *file = fopen("contacts.txt", "a");
if (file == NULL) {
    perror("fopen");
    return 1;
}

fprintf(file, "%s,%s\n", contact.name, contact.phone);
fclose(file);
```

文件打开可能失败，写入和关闭也应当在真实程序中检查返回结果。

## 4.3 头文件和源文件

```text
contacts/
├── main.c       # 入口和菜单
├── contacts.c   # 联系人操作
└── contacts.h   # 类型和函数声明
```

头文件描述接口，源文件提供实现。这样可以让编译单元更小，也更容易测试。

## 本章练习

把通讯录的新增和查询功能拆分到 `contacts.c`，在 `main.c` 中只保留菜单和输入流程。
