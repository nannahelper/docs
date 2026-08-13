# 第 3 章：运算符与表达式 —— 让数据"动"起来

> **场景：** 你已经把学生信息存进了变量（储物柜）。现在需要计算总分、判断是否及格、比较谁的成绩更高——这些都需要运算符来"操作"数据，就像用遥控器操控电视一样。

---

## 3.1 算术运算符

!!! example "核心比喻：算术运算符就像计算器按钮"
    你桌上的计算器有 +、-、×、÷ 按钮。Java 的算术运算符就是这些按钮的编程版本——只不过乘号用 `*`，除号用 `/`，还有一个特殊的"取余数"按钮 `%`。

```java
public class ArithmeticDemo {
    public static void main(String[] args) {
        int a = 17;
        int b = 5;
        
        System.out.println("a = " + a + ", b = " + b);
        System.out.println("===== 基本运算 =====");
        System.out.println("a + b  = " + (a + b));   // 加法：22
        System.out.println("a - b  = " + (a - b));   // 减法：12
        System.out.println("a * b  = " + (a * b));   // 乘法：85
        System.out.println("a / b  = " + (a / b));   // 除法：3（整数除法，舍去小数）
        System.out.println("a % b  = " + (a % b));   // 取余：2（17 ÷ 5 = 3 余 2）
        
        System.out.println("\n===== 小数除法 =====");
        double x = 17.0;
        double y = 5.0;
        System.out.println("x / y  = " + (x / y));   // 3.4（浮点除法，保留小数）
    }
}
```

**运行结果：**
```
a = 17, b = 5
===== 基本运算 =====
a + b  = 22
a - b  = 12
a * b  = 85
a / b  = 3
a % b  = 2

===== 小数除法 =====
x / y  = 3.4
```

!!! warning "整数除法陷阱"
    两个整数相除，结果还是整数（小数部分被直接丢弃，不是四舍五入）。如果需要小数结果，至少让其中一个操作数是浮点类型。

| 运算符 | 名称 | 示例 | 结果 |
|:---|:---|:---|:---|
| `+` | 加法 | `5 + 3` | `8` |
| `-` | 减法 | `5 - 3` | `2` |
| `*` | 乘法 | `5 * 3` | `15` |
| `/` | 除法 | `5 / 2` | `2`（整数）/ `2.5`（浮点） |
| `%` | 取余（模） | `5 % 2` | `1` |

---

## 3.2 自增与自减运算符

编程中经常需要"加 1"或"减 1"操作，Java 提供了快捷方式：

```java
public class IncrementDemo {
    public static void main(String[] args) {
        int count = 0;
        
        count++;  // 等价于 count = count + 1
        System.out.println("count++ 后: " + count);  // 1
        
        count--;  // 等价于 count = count - 1
        System.out.println("count-- 后: " + count);  // 0
        
        // 前置与后置的区别
        int a = 5;
        int b = ++a;  // 前置：先加 1，再赋值。a=6, b=6
        
        int c = 5;
        int d = c++;  // 后置：先赋值，再加 1。c=6, d=5
        
        System.out.println("\n前置 ++a: a=" + a + ", b=" + b);
        System.out.println("后置 c++: c=" + c + ", d=" + d);
    }
}
```

**运行结果：**
```
count++ 后: 1
count-- 后: 0

前置 ++a: a=6, b=6
后置 c++: c=6, d=5
```

!!! tip "记忆技巧"
    - `++x`：**先加后用**（"加加"在前面，所以先加）
    - `x++`：**先用后加**（"加加"在后面，所以后加）

---

## 3.3 赋值运算符

```java
public class AssignmentDemo {
    public static void main(String[] args) {
        int score = 80;
        
        score += 10;   // 等价于 score = score + 10  → 90
        System.out.println("加分后: " + score);
        
        score -= 5;    // 等价于 score = score - 5   → 85
        System.out.println("扣分后: " + score);
        
        score *= 2;    // 等价于 score = score * 2   → 170
        System.out.println("翻倍后: " + score);
        
        score /= 3;    // 等价于 score = score / 3   → 56
        System.out.println("除以3后: " + score);
        
        score %= 10;   // 等价于 score = score % 10  → 6
        System.out.println("对10取余: " + score);
    }
}
```

**运行结果：**
```
加分后: 90
扣分后: 85
翻倍后: 170
除以3后: 56
对10取余: 6
```

---

## 3.4 关系运算符（比较运算符）

关系运算符用来比较两个值，结果是 `true` 或 `false`：

```java
public class RelationalDemo {
    public static void main(String[] args) {
        int zhangsan = 85;
        int lisi = 92;
        
        System.out.println("张三: " + zhangsan + ", 李四: " + lisi);
        System.out.println("===== 比较结果 =====");
        System.out.println("张三 > 李四?  " + (zhangsan > lisi));    // false
        System.out.println("张三 < 李四?  " + (zhangsan < lisi));    // true
        System.out.println("张三 >= 85?  " + (zhangsan >= 85));      // true
        System.out.println("张三 <= 85?  " + (zhangsan <= 85));      // true
        System.out.println("张三 == 李四? " + (zhangsan == lisi));   // false
        System.out.println("张三 != 李四? " + (zhangsan != lisi));   // true
    }
}
```

**运行结果：**
```
张三: 85, 李四: 92
===== 比较结果 =====
张三 > 李四?  false
张三 < 李四?  true
张三 >= 85?  true
张三 <= 85?  true
张三 == 李四? false
张三 != 李四? true
```

!!! danger "字符串比较不能用 =="
    `==` 比较的是内存地址，不是内容。比较字符串内容请用 `.equals()`：
    ```java
    String a = "hello";
    String b = "hello";
    System.out.println(a == b);        // 可能是 true（字符串池），不可靠
    System.out.println(a.equals(b));   // true，这才是正确方式
    ```

---

## 3.5 逻辑运算符

逻辑运算符用来组合多个条件，就像"并且"、"或者"、"不是"：

```java
public class LogicalDemo {
    public static void main(String[] args) {
        int score = 85;
        boolean isStudent = true;
        
        // &&（与）：两边都为 true，结果才为 true
        boolean scholarship = (score >= 90) && isStudent;
        System.out.println("成绩>=90 且 是学生: " + scholarship);  // false
        
        // ||（或）：只要有一边为 true，结果就为 true
        boolean pass = (score >= 60) || !isStudent;
        System.out.println("成绩>=60 或 不是学生: " + pass);      // true
        
        // !（非）：取反
        boolean fail = !pass;
        System.out.println("不及格: " + fail);                     // false
        
        // 短路效应
        int a = 10;
        boolean result = (a > 5) || (a++ > 20);  // a > 5 已经是 true，后面的 a++ 不会执行
        System.out.println("短路后 a = " + a);    // 10，没有变成 11
    }
}
```

**运行结果：**
```
成绩>=90 且 是学生: false
成绩>=60 或 不是学生: true
不及格: false
短路后 a = 10
```

| 运算符 | 名称 | 说明 | 示例 |
|:---|:---|:---|:---|
| `&&` | 逻辑与 | 两边都为 true 才为 true | `(a > 0) && (b > 0)` |
| `\|\|` | 逻辑或 | 至少一边为 true 就为 true | `(a > 0) \|\| (b > 0)` |
| `!` | 逻辑非 | 取反 | `!isPassed` |

---

## 3.6 运算符优先级

当多个运算符出现在同一个表达式中，Java 按照优先级决定计算顺序。如果不确定，**加括号** 是最稳妥的做法：

```java
public class PrecedenceDemo {
    public static void main(String[] args) {
        // 不加括号：先乘除后加减
        int result1 = 10 + 5 * 2;        // 10 + 10 = 20
        System.out.println("10 + 5 * 2 = " + result1);
        
        // 加括号：改变优先级
        int result2 = (10 + 5) * 2;      // 15 * 2 = 30
        System.out.println("(10 + 5) * 2 = " + result2);
        
        // 复杂表达式
        int score = 85;
        int attendance = 90;
        boolean excellent = (score >= 90) && (attendance >= 80);
        System.out.println("优秀学生: " + excellent);
    }
}
```

**运行结果：**
```
10 + 5 * 2 = 20
(10 + 5) * 2 = 30
优秀学生: false
```

!!! tip "优先级速记"
    从高到低：`()` → `!` → `* / %` → `+ -` → `> < >= <=` → `== !=` → `&&` → `||` → `=`
    
    记不住？没关系——**有疑问就加括号**，括号里的先算。

---

## 要点总结

- [x] 算术运算符：`+` `-` `*` `/` `%`（整数除法舍去小数）
- [x] 自增自减：`++` `--`（前置先加后用，后置先用后加）
- [x] 赋值运算符：`=` `+=` `-=` `*=` `/=` `%=`
- [x] 关系运算符：`>` `<` `>=` `<=` `==` `!=`（结果是 boolean）
- [x] 逻辑运算符：`&&`（与）`||`（或）`!`（非）
- [x] 字符串比较用 `.equals()`，不能用 `==`
- [x] 不确定优先级时，加括号最安全

---

## 课后练习

1.  **成绩计算器** ：已知语文 88 分、数学 92 分、英语 79 分，计算总分和平均分（保留小数）。

2.  **闰年判断** ：编写程序判断 2026 年是否是闰年（能被 4 整除但不能被 100 整除，或者能被 400 整除）。

3.  **数字拆解** ：给定一个三位数 357，用运算符分别取出它的百位、十位、个位数字。

---

**下一章预告：** 运算符让数据"动"起来了，但程序还需要"判断"能力——控制流程，让程序根据不同条件走不同的路。

[继续第 4 章：控制流程 →](04-control-flow.md)