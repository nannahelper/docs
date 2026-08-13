# 第 5 章：综合项目——命令行记账本 — 交付一个小工具

## 📋 本章概览

| 项目 | 内容 |
|:---|:---|
| 学习时长 | 50 分钟 |
| 核心概念 | 菜单循环、数据校验、持久化、模块职责 |
| 核心比喻 | 把前四章的零件组装成一台可使用的小机器 |
| 实践任务 | 完成可新增、查看和统计的记账本 |
| 难度等级 | ★★★☆☆ |

现在把前四章组合起来，完成一个最小可用的记账本。第一版只实现新增记录、查看记录和统计总额。

## 5.1 数据结构

每条记录使用字典表示：

```python
{
    "title": "午餐",
    "amount": 25.0,
    "category": "餐饮",
}
```

## 5.2 菜单循环

```python
def show_menu():
    print("\n1. 新增记录")
    print("2. 查看记录")
    print("3. 查看总额")
    print("q. 退出")


records = []
while True:
    show_menu()
    choice = input("请选择：").strip().lower()
    if choice == "1":
        title = input("事项：").strip()
        amount = float(input("金额："))
        category = input("分类：").strip()
        records.append({"title": title, "amount": amount, "category": category})
    elif choice == "2":
        for item in records:
            print(f"{item['category']} | {item['title']} | {item['amount']:.2f} 元")
    elif choice == "3":
        print(f"总额：{sum(item['amount'] for item in records):.2f} 元")
    elif choice == "q":
        break
    else:
        print("无法识别的选项。")
```

## 5.3 继续升级

- 启动时从 JSON 文件加载记录，退出时保存
- 为金额输入增加异常处理
- 按分类统计金额
- 为核心函数补充 pytest 测试
- 使用 Git 提交一个可运行版本

完成这些升级后，你已经拥有一个小型但完整的 Python 应用：有输入、有状态、有持久化，也有可以继续演进的结构。

## ✅ 验证步骤

1. 新增餐饮和交通记录，确认查看和统计结果正确。
2. 退出后重新启动，确认记录仍然存在。
3. 输入字母作为金额，确认程序提示错误并允许重试。
4. 删除或移动 JSON 文件后重新启动，确认程序能安全处理空数据。

## 📝 本章总结

- 小项目应先明确数据结构，再组织流程。
- 输入校验、错误处理和持久化决定程序是否真正可用。
- 一个可交付的程序必须有明确的手工验收步骤。

## ✏️ 课后练习

1. 增加按日期筛选和删除记录功能。
2. 将程序拆为 main.py、storage.py 和 reports.py。
3. 为金额校验、分类统计和文件加载分别编写测试。

## 🔮 学完之后

建议进入“调试与测试指南”，把刚完成的记账本变得更可靠。
