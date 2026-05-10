# 第 4 章：控制流程 —— 程序的"方向盘"

> **场景：** 你需要写一个程序来判断学生成绩等级——90 分以上是"优秀"，80~89 是"良好"，60~79 是"及格"，60 以下是"不及格"。程序不能只会"一条路走到黑"，它需要根据不同的条件做出不同的反应——这就是控制流程。

---

## 4.1 if-else：条件判断

!!! example "核心比喻：if-else 就像十字路口的红绿灯"
    你开车到十字路口：
    - **如果**（if）是绿灯 → 通行
    - **否则如果**（else if）是黄灯 → 减速准备停车
    - **否则**（else）→ 停车等待
    
    程序中的 if-else 就是这样的"交通规则"——根据不同条件，执行不同的代码。

### 4.1.1 基本 if 语句

```java
public class IfDemo {
    public static void main(String[] args) {
        int score = 85;
        
        // 最简单的 if：条件为 true 才执行
        if (score >= 60) {
            System.out.println("恭喜，你及格了！");
        }
        
        // if-else：二选一
        if (score >= 90) {
            System.out.println("等级：优秀");
        } else {
            System.out.println("等级：不是优秀");
        }
    }
}
```

**运行结果：**
```
恭喜，你及格了！
等级：不是优秀
```

### 4.1.2 if-else if-else 多分支

```java
public class GradeDemo {
    public static void main(String[] args) {
        int score = 85;
        String grade;
        
        if (score >= 90) {
            grade = "优秀";
        } else if (score >= 80) {
            grade = "良好";
        } else if (score >= 70) {
            grade = "中等";
        } else if (score >= 60) {
            grade = "及格";
        } else {
            grade = "不及格";
        }
        
        System.out.println("成绩: " + score + " → 等级: " + grade);
        
        // 测试不同分数
        int[] scores = {95, 82, 75, 61, 45};
        for (int s : scores) {
            String g;
            if (s >= 90)      g = "优秀";
            else if (s >= 80) g = "良好";
            else if (s >= 70) g = "中等";
            else if (s >= 60) g = "及格";
            else              g = "不及格";
            System.out.println(s + " 分 → " + g);
        }
    }
}
```

**运行结果：**
```
成绩: 85 → 等级: 良好
95 分 → 优秀
82 分 → 良好
75 分 → 中等
61 分 → 及格
45 分 → 不及格
```

!!! tip "if-else 执行规则"
    if-else if-else 是 **从上到下依次检查**，只要有一个条件为 true，就执行对应的代码块，然后跳过剩余的所有分支。所以条件的顺序很重要——范围小的条件应该写在前面。

---

## 4.2 switch：多路选择

当需要判断的条件是"某个变量等于什么值"时，`switch` 比一长串 `if-else` 更清晰：

```java
public class SwitchDemo {
    public static void main(String[] args) {
        int dayOfWeek = 3;  // 1=周一, 2=周二, ..., 7=周日
        
        // 传统 switch 写法
        switch (dayOfWeek) {
            case 1:
                System.out.println("周一：满课，加油！");
                break;
            case 2:
                System.out.println("周二：实验课，动手实践");
                break;
            case 3:
                System.out.println("周三：体育课，锻炼身体");
                break;
            case 4:
                System.out.println("周四：专业课，认真听讲");
                break;
            case 5:
                System.out.println("周五：周末快到了！");
                break;
            case 6:
            case 7:
                System.out.println("周末：休息时间！");
                break;
            default:
                System.out.println("输入错误，请输入 1-7");
        }
        
        // Java 14+ 新式 switch 表达式（更简洁）
        String schedule = switch (dayOfWeek) {
            case 1 -> "周一：满课，加油！";
            case 2 -> "周二：实验课，动手实践";
            case 3 -> "周三：体育课，锻炼身体";
            case 4 -> "周四：专业课，认真听讲";
            case 5 -> "周五：周末快到了！";
            case 6, 7 -> "周末：休息时间！";
            default -> "输入错误";
        };
        System.out.println("新式 switch: " + schedule);
    }
}
```

**运行结果：**
```
周三：体育课，锻炼身体
新式 switch: 周三：体育课，锻炼身体
```

!!! warning "别忘了 break！"
    传统 switch 中，如果忘记写 `break`，程序会"穿透"到下一个 case 继续执行。case 6 和 case 7 共享同一段代码就是利用了这个特性。

---

## 4.3 for 循环：重复执行

!!! example "核心比喻：for 循环就像操场跑圈"
    体育老师说："跑 5 圈！"你从第 1 圈开始，每跑完一圈检查"跑够 5 圈了吗？"，没跑够就继续，跑够了就停。
    
    for 循环就是这样的"计数器"——设置起点、终点和步长，自动重复执行。

```java
public class ForDemo {
    public static void main(String[] args) {
        // 基本 for 循环：打印 1 到 5
        System.out.println("===== 计数 1~5 =====");
        for (int i = 1; i <= 5; i++) {
            System.out.println("第 " + i + " 次循环");
        }
        
        // 计算 1 到 100 的和
        int sum = 0;
        for (int i = 1; i <= 100; i++) {
            sum += i;  // 等价于 sum = sum + i
        }
        System.out.println("\n1+2+...+100 = " + sum);
        
        // 倒序循环
        System.out.println("\n===== 倒计时 =====");
        for (int i = 5; i >= 1; i--) {
            System.out.println(i + "...");
        }
        System.out.println("发射！");
    }
}
```

**运行结果：**
```
===== 计数 1~5 =====
第 1 次循环
第 2 次循环
第 3 次循环
第 4 次循环
第 5 次循环

1+2+...+100 = 5050

===== 倒计时 =====
5...
4...
3...
2...
1...
发射！
```

### for 循环的结构解剖

```java
for (初始化; 条件; 更新) {
    // 循环体
}

// 例如：
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}
```

| 部分 | 作用 | 执行时机 |
|:---|:---|:---|
| `int i = 0` | 初始化计数器 | 只在循环开始前执行一次 |
| `i < 10` | 循环条件 | 每次循环前检查，false 则退出 |
| `i++` | 更新计数器 | 每次循环结束后执行 |
| `{ ... }` | 循环体 | 条件为 true 时执行 |

---

## 4.4 while 循环：条件驱动的重复

当你不知道要循环多少次，只知道"满足条件就继续"时，用 while：

```java
public class WhileDemo {
    public static void main(String[] args) {
        // while：先判断，再执行（可能一次都不执行）
        System.out.println("===== while 循环 =====");
        int count = 1;
        while (count <= 5) {
            System.out.println("count = " + count);
            count++;
        }
        
        // do-while：先执行，再判断（至少执行一次）
        System.out.println("\n===== do-while 循环 =====");
        int num = 1;
        do {
            System.out.println("num = " + num);
            num++;
        } while (num <= 5);
        
        // 实用场景：猜数字（模拟）
        System.out.println("\n===== 猜数字模拟 =====");
        int secret = 7;
        int guess = 1;
        int attempts = 0;
        
        while (guess != secret) {
            guess = (int)(Math.random() * 10) + 1;  // 随机猜 1~10
            attempts++;
            System.out.println("第 " + attempts + " 次猜: " + guess);
        }
        System.out.println("猜对了！共猜了 " + attempts + " 次");
    }
}
```

**运行结果：**
```
===== while 循环 =====
count = 1
count = 2
count = 3
count = 4
count = 5

===== do-while 循环 =====
num = 1
num = 2
num = 3
num = 4
num = 5

===== 猜数字模拟 =====
第 1 次猜: 3
第 2 次猜: 8
第 3 次猜: 7
猜对了！共猜了 3 次
```

| 循环类型 | 特点 | 使用场景 |
|:---|:---|:---|
| `for` | 知道循环次数 | 遍历数组、计数循环 |
| `while` | 先判断再执行 | 读取文件直到末尾、等待用户输入 |
| `do-while` | 先执行再判断 | 至少执行一次的场景（如菜单选择） |

---

## 4.5 break 与 continue

```java
public class BreakContinueDemo {
    public static void main(String[] args) {
        // break：立即退出整个循环
        System.out.println("===== break 示例 =====");
        for (int i = 1; i <= 10; i++) {
            if (i == 6) {
                System.out.println("遇到 6，退出循环！");
                break;
            }
            System.out.println("i = " + i);
        }
        
        // continue：跳过本次循环，继续下一次
        System.out.println("\n===== continue 示例 =====");
        for (int i = 1; i <= 10; i++) {
            if (i % 2 == 0) {  // 偶数
                continue;       // 跳过偶数
            }
            System.out.println("奇数: " + i);
        }
    }
}
```

**运行结果：**
```
===== break 示例 =====
i = 1
i = 2
i = 3
i = 4
i = 5
遇到 6，退出循环！

===== continue 示例 =====
奇数: 1
奇数: 3
奇数: 5
奇数: 7
奇数: 9
```

---

## 要点总结

- [x] `if-else` 根据条件选择执行路径，从上到下依次检查
- [x] `switch` 适合"变量等于某个值"的多路判断
- [x] `for` 循环适合已知次数的重复操作
- [x] `while` 循环适合条件驱动的重复操作
- [x] `do-while` 至少执行一次循环体
- [x] `break` 立即退出循环，`continue` 跳过本次循环
- [x] 条件顺序很重要：范围小的条件写在前面

---

## 课后练习

1.  **成绩等级** ：输入一个 0~100 的分数，输出对应的等级（优秀/良好/中等/及格/不及格）。

2.  **九九乘法表** ：用嵌套 for 循环打印九九乘法表。

3.  **素数判断** ：判断一个整数是否为素数（只能被 1 和自身整除）。

---

**下一章预告：** 循环让代码能重复执行，但如果每次都写重复的逻辑还是太麻烦。方法（函数）让你把一段逻辑"打包"起来，随用随调——就像把常用工具放进工具箱。

[继续第 5 章：方法与函数 →](05-methods.md)