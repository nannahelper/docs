# 第 2 章：变量与数据类型 —— 数据的"储物柜"

> **场景：** 你需要写一个程序来管理学生信息——姓名、年龄、成绩。但电脑不像人脑，它需要你明确告诉它：每个信息是什么类型、占多大空间。这就是变量与数据类型的作用——给不同种类的数据分配合适的"储物柜"。

---

## 2.1 什么是变量？

!!! example "核心比喻：变量就像储物柜"
    想象你去健身房，前台给你一个储物柜。这个柜子有：
    
    - **编号**（变量名）：比如"柜子 A3"，方便你找到它
    - **大小**（数据类型）：小柜子放钱包，大柜子放背包
    - **内容**（变量值）：你放进去的东西
    
    在 Java 中，变量就是这样一个"带标签的储物柜"——你给它起个名字，指定它能放什么类型的数据，然后把数据存进去。

```java
// 声明一个变量：指定类型 + 起名字
int age;

// 给变量赋值：把数据放进"储物柜"
age = 20;

// 声明 + 赋值一步完成
String name = "张三";
```

---

## 2.2 Java 的八种基本数据类型

Java 提供了 8 种"标准储物柜"，每种大小不同，能放的东西也不同：

| 数据类型 | 大小 | 范围 | 生活比喻 | 示例 |
|:---|:---|:---|:---|:---|
| `byte` | 1 字节 | -128 ~ 127 | 小药盒 | `byte b = 100;` |
| `short` | 2 字节 | -32768 ~ 32767 | 铅笔盒 | `short s = 30000;` |
| `int` | 4 字节 | ±21 亿 | 书包 | `int age = 20;` |
| `long` | 8 字节 | ±9×10¹⁸ | 行李箱 | `long pop = 80_0000_0000L;` |
| `float` | 4 字节 | 约 ±3.4×10³⁸ | 小量杯（单精度） | `float pi = 3.14f;` |
| `double` | 8 字节 | 约 ±1.8×10³⁰⁸ | 大量杯（双精度） | `double e = 2.71828;` |
| `char` | 2 字节 | 0 ~ 65535 | 单个字母卡片 | `char grade = 'A';` |
| `boolean` | 1 位 | `true` / `false` | 开关（开/关） | `boolean pass = true;` |

!!! tip "记忆口诀"
    - **整数四兄弟**：byte < short < int < long（从小到大）
    - **小数两姐妹**：float（单精度）< double（双精度）
    - **字符一个娃**：char（单个字符，用单引号）
    - **布尔小开关**：boolean（只有 true 和 false）

---

## 2.3 变量的声明与使用

```java
public class VariableDemo {
    public static void main(String[] args) {
        // ========== 整数类型 ==========
        byte    score = 100;           // 小整数，范围 -128~127
        short   year  = 2026;          // 中等整数
        int     count = 1000000;       // 最常用的整数类型
        long    world = 80_0000_0000L; // 大整数，注意末尾的 L
        
        // ========== 浮点类型 ==========
        float  pi_f  = 3.1415926f;     // 单精度，注意末尾的 f
        double pi_d  = 3.141592653589793; // 双精度，默认小数类型
        
        // ========== 字符类型 ==========
        char grade = 'A';              // 单个字符，用单引号
        char chinese = '中';           // Java 支持 Unicode，可以存中文
        
        // ========== 布尔类型 ==========
        boolean isPassed = true;       // 只有 true 或 false
        boolean isAdult  = false;
        
        // ========== 打印所有变量 ==========
        System.out.println("===== 整数类型 =====");
        System.out.println("byte:   " + score);
        System.out.println("short:  " + year);
        System.out.println("int:    " + count);
        System.out.println("long:   " + world);
        
        System.out.println("\n===== 浮点类型 =====");
        System.out.println("float:  " + pi_f);
        System.out.println("double: " + pi_d);
        
        System.out.println("\n===== 字符类型 =====");
        System.out.println("char:   " + grade);
        System.out.println("char:   " + chinese);
        
        System.out.println("\n===== 布尔类型 =====");
        System.out.println("是否及格: " + isPassed);
        System.out.println("是否成年: " + isAdult);
    }
}
```

**运行结果：**
```
===== 整数类型 =====
byte:   100
short:  2026
int:    1000000
long:   8000000000

===== 浮点类型 =====
float:  3.1415925
double: 3.141592653589793

===== 字符类型 =====
char:   A
char:   中

===== 布尔类型 =====
是否及格: true
是否成年: false
```

---

## 2.4 引用类型：String（字符串）

除了 8 种基本类型，最常用的就是 `String`（字符串）——它属于 **引用类型**，可以存储任意长度的文本。

```java
public class StringDemo {
    public static void main(String[] args) {
        // 创建字符串
        String name = "张三";
        String school = "南哪大学";
        String motto = "今天搓代码了吗？";
        
        // 字符串拼接（用 + 号）
        String greeting = "你好，" + name + "！欢迎来到" + school;
        
        // 获取字符串长度
        int length = motto.length();
        
        // 获取某个位置的字符（从 0 开始数）
        char firstChar = motto.charAt(0);
        
        // 判断是否包含某个词
        boolean hasCode = motto.contains("代码");
        
        System.out.println(greeting);
        System.out.println("校训长度: " + length + " 个字");
        System.out.println("第一个字: " + firstChar);
        System.out.println("包含'代码'吗？ " + hasCode);
    }
}
```

**运行结果：**
```
你好，张三！欢迎来到南哪大学
校训长度: 9 个字
第一个字: 今
包含'代码'吗？ true
```

!!! info "String 常用方法速查"
    | 方法 | 作用 | 示例 |
    |:---|:---|:---|
    | `.length()` | 获取字符串长度 | `"Hello".length()` → 5 |
    | `.charAt(n)` | 获取第 n 个字符（从 0 开始） | `"Java".charAt(0)` → 'J' |
    | `.contains(s)` | 判断是否包含子串 | `"Hello".contains("ell")` → true |
    | `.toUpperCase()` | 转为全大写 | `"java".toUpperCase()` → "JAVA" |
    | `.toLowerCase()` | 转为全小写 | `"JAVA".toLowerCase()` → "java" |
    | `.equals(s)` | 判断内容是否相等 | `"abc".equals("abc")` → true |
    | `.substring(a, b)` | 截取子串 [a, b) | `"Hello".substring(1, 4)` → "ell" |

---

## 2.5 类型转换

有时候需要把一种类型的"储物柜"里的东西转移到另一种类型的柜子里。

### 2.5.1 自动类型转换（小 → 大）

把小柜子的东西放进大柜子，不会丢东西，Java 自动帮你做：

```java
int    small = 100;
long   big   = small;     // int → long，自动转换，安全
double d     = small;     // int → double，自动转换，安全

System.out.println("long: " + big);     // 100
System.out.println("double: " + d);     // 100.0
```

### 2.5.2 强制类型转换（大 → 小）

把大柜子的东西硬塞进小柜子，可能会溢出或丢失精度，需要你明确告诉编译器"我知道风险"：

```java
double pi = 3.1415926;
int    n  = (int) pi;     // double → int，强制转换，小数部分被截断

long   bigNum = 300;
byte   small  = (byte) bigNum;  // long → byte，强制转换

System.out.println("pi 转 int: " + n);       // 3（小数被丢弃）
System.out.println("300 转 byte: " + small);  // 44（溢出！300 超出了 byte 的范围）
```

!!! danger "强制转换风险"
    大类型转小类型时，如果值超出了小类型的范围，会发生 **数据溢出**，得到意想不到的结果。务必确认值在目标类型的范围内！

---

## 2.6 常量：上了锁的储物柜

有些数据在整个程序中都不应该被修改——比如圆周率 π、学校的名称。用 `final` 关键字把它变成常量：

```java
public class ConstantDemo {
    public static void main(String[] args) {
        // 常量：一旦赋值，就不能再改
        final double PI = 3.141592653589793;
        final String SCHOOL_NAME = "南哪大学";
        final int MAX_STUDENTS = 50;
        
        // 使用常量
        double radius = 5.0;
        double area = PI * radius * radius;
        
        System.out.println("学校: " + SCHOOL_NAME);
        System.out.println("半径为 " + radius + " 的圆面积: " + area);
        System.out.println("最大学生数: " + MAX_STUDENTS);
        
        // 下面这行会报错！常量不能被修改
        // PI = 3.14;  // 编译错误！
    }
}
```

**运行结果：**
```
学校: 南哪大学
半径为 5.0 的圆面积: 78.53981633974483
最大学生数: 50
```

!!! note "命名规范"
    Java 社区约定：
    - 变量名和方法名：**小驼峰**（`studentName`、`getScore()`）
    - 类名：**大驼峰**（`StudentManager`、`HelloWorld`）
    - 常量名：**全大写 + 下划线**（`MAX_VALUE`、`SCHOOL_NAME`）

---

## 要点总结

- [x] 变量 = 带名字和类型的"数据储物柜"
- [x] Java 有 8 种基本类型：byte、short、int、long、float、double、char、boolean
- [x] `int` 是最常用的整数类型，`double` 是最常用的小数类型
- [x] `String` 是引用类型，用于存储文本，用双引号
- [x] `char` 用单引号，只能存一个字符
- [x] 小类型 → 大类型自动转换；大类型 → 小类型需要强制转换 `(类型)`
- [x] `final` 关键字定义常量，值不可修改

---

## 课后练习

1.  **个人信息卡** ：声明变量存储你的姓名（String）、年龄（int）、身高（double，单位米）、是否是学生（boolean），然后打印出来。

2.  **温度转换** ：将摄氏温度 37.5 度（double）转换为华氏温度（公式：$F = C \times 1.8 + 32$），打印结果。

3.  **溢出实验** ：将 `int` 的最大值 `2147483647` 加 1，观察结果变成了什么？思考为什么。

---

**下一章预告：** 数据存好了，接下来要让它们"动"起来——运算符与表达式，就像给储物柜里的东西贴上运算标签。

[继续第 3 章：运算符与表达式 →](03-operators.md)