# 第 5 章：综合项目——命令行记账本

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
