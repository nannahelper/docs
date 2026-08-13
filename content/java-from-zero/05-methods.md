# 第 5 章：方法与函数 —— 代码的"工具箱"

> **场景：** 你的程序中需要多次计算圆的面积、判断素数、打印分隔线。如果每次都重写一遍代码，不仅麻烦还容易出错。方法（函数）让你把一段逻辑"打包"成一个工具，给它起个名字，以后直接喊名字就能用——就像把常用工具放进工具箱。

---

## 5.1 什么是方法？

!!! example "核心比喻：方法就像微波炉的预设按钮"
    微波炉上有"热牛奶"、"解冻"、"爆米花"等预设按钮。你不需要每次都手动设置时间和火力——按一下按钮，微波炉自动按照预设程序运行。
    
    方法就是程序的"预设按钮"：把一段代码打包，起个名字，以后调用这个名字就能执行那段代码。

```java
public class MethodIntro {
    // 定义一个方法：打印分隔线
    public static void printLine() {
        System.out.println("========================");
    }
    
    public static void main(String[] args) {
        System.out.println("学生成绩管理系统");
        printLine();  // 调用方法
        System.out.println("1. 添加学生");
        System.out.println("2. 查询成绩");
        System.out.println("3. 退出系统");
        printLine();  // 再次调用
    }
}
```

**运行结果：**
```
学生成绩管理系统
========================
1. 添加学生
2. 查询成绩
3. 退出系统
========================
```

---

## 5.2 方法的定义与调用

### 方法的基本结构

```java
public static 返回类型 方法名(参数列表) {
    // 方法体：要执行的代码
    return 返回值;  // 如果返回类型不是 void
}
```

| 部分 | 说明 | 示例 |
|:---|:---|:---|
| `public static` | 修饰符（初学阶段固定写法） | `public static` |
| 返回类型 | 方法返回什么类型的数据 | `int`、`double`、`String`、`void`（无返回） |
| 方法名 | 自定义的名字（小驼峰命名） | `calculateSum`、`getGrade` |
| 参数列表 | 传入的数据（类型 + 名字） | `(int a, int b)` |
| 方法体 | 要执行的代码 | `{ return a + b; }` |

### 带参数和返回值的方法

```java
public class MethodDemo {
    // 有参数、有返回值：计算两个数的和
    public static int add(int a, int b) {
        return a + b;
    }
    
    // 有参数、有返回值：判断是否及格
    public static boolean isPassed(int score) {
        return score >= 60;
    }
    
    // 有参数、有返回值：获取成绩等级
    public static String getGrade(int score) {
        if (score >= 90)      return "优秀";
        else if (score >= 80) return "良好";
        else if (score >= 70) return "中等";
        else if (score >= 60) return "及格";
        else                  return "不及格";
    }
    
    // 无参数、无返回值：打印菜单
    public static void printMenu() {
        System.out.println("===== 主菜单 =====");
        System.out.println("1. 开始游戏");
        System.out.println("2. 读取存档");
        System.out.println("3. 退出");
    }
    
    public static void main(String[] args) {
        // 调用有返回值的方法
        int sum = add(10, 20);
        System.out.println("10 + 20 = " + sum);
        
        System.out.println("85 分及格吗？ " + isPassed(85));
        System.out.println("55 分及格吗？ " + isPassed(55));
        
        System.out.println("92 分的等级: " + getGrade(92));
        System.out.println("73 分的等级: " + getGrade(73));
        System.out.println("48 分的等级: " + getGrade(48));
        
        // 调用无返回值的方法
        printMenu();
    }
}
```

**运行结果：**
```
10 + 20 = 30
85 分及格吗？ true
55 分及格吗？ false
92 分的等级: 优秀
73 分的等级: 中等
48 分的等级: 不及格
===== 主菜单 =====
1. 开始游戏
2. 读取存档
3. 退出
```

---

## 5.3 参数传递

Java 中，基本类型参数传递的是 **值的副本**，方法内修改参数不会影响原始变量：

```java
public class ParameterDemo {
    public static void changeValue(int x) {
        x = 100;  // 修改的是副本，不影响原始变量
        System.out.println("方法内: x = " + x);
    }
    
    public static void main(String[] args) {
        int num = 10;
        System.out.println("调用前: num = " + num);
        changeValue(num);
        System.out.println("调用后: num = " + num);  // 还是 10
    }
}
```

**运行结果：**
```
调用前: num = 10
方法内: x = 100
调用后: num = 10
```

!!! info "值传递 vs 引用传递"
    Java 中基本类型（int、double 等）是 **值传递**——方法拿到的是副本，改副本不影响原件。引用类型（String、数组、对象）传递的是 **引用的副本**，通过引用可以修改对象的内容。

---

## 5.4 方法重载

同一个类中，可以有多个 **同名但参数不同** 的方法——这叫方法重载：

```java
public class OverloadDemo {
    // 两个整数相加
    public static int add(int a, int b) {
        return a + b;
    }
    
    // 三个整数相加（参数个数不同）
    public static int add(int a, int b, int c) {
        return a + b + c;
    }
    
    // 两个小数相加（参数类型不同）
    public static double add(double a, double b) {
        return a + b;
    }
    
    public static void main(String[] args) {
        System.out.println("add(5, 3)     = " + add(5, 3));
        System.out.println("add(5, 3, 2)  = " + add(5, 3, 2));
        System.out.println("add(5.5, 3.2) = " + add(5.5, 3.2));
    }
}
```

**运行结果：**
```
add(5, 3)     = 8
add(5, 3, 2)  = 10
add(5.5, 3.2) = 8.7
```

!!! tip "重载的判断标准"
    Java 根据 **方法名 + 参数列表**（参数类型、个数、顺序）来区分方法。**返回值类型不算**——两个方法不能只有返回值类型不同。

---

## 5.5 递归：方法调用自己

递归是编程中一种优雅但需要小心的技术——方法自己调用自己：

```java
public class RecursionDemo {
    // 计算阶乘：n! = n * (n-1) * ... * 1
    public static long factorial(int n) {
        if (n <= 1) {
            return 1;  // 递归终止条件（必须有！）
        }
        return n * factorial(n - 1);  // 自己调用自己
    }
    
    // 斐波那契数列：1, 1, 2, 3, 5, 8, 13, ...
    public static long fibonacci(int n) {
        if (n <= 2) {
            return 1;
        }
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    
    public static void main(String[] args) {
        System.out.println("5!  = " + factorial(5));    // 120
        System.out.println("10! = " + factorial(10));   // 3628800
        
        System.out.println("\n斐波那契数列前 10 项:");
        for (int i = 1; i <= 10; i++) {
            System.out.print(fibonacci(i) + " ");
        }
    }
}
```

**运行结果：**
```
5!  = 120
10! = 3628800

斐波那契数列前 10 项:
1 1 2 3 5 8 13 21 34 55
```

!!! danger "递归必须有终止条件"
    没有终止条件的递归会无限调用自己，最终导致 `StackOverflowError`（栈溢出）。就像两面镜子对在一起，会无限反射。

---

## 要点总结

- [x] 方法 = 把一段代码打包，起名字，随用随调
- [x] 方法结构：`返回类型 方法名(参数) { 方法体; return 返回值; }`
- [x] `void` 表示无返回值
- [x] 基本类型参数是值传递，方法内修改不影响原始变量
- [x] 方法重载：同名方法，参数列表不同
- [x] 递归：方法调用自己，必须有终止条件

---

## 课后练习

1.  **计算器方法** ：编写 `add`、`subtract`、`multiply`、`divide` 四个方法，并在 main 中调用测试。

2.  **最大值方法** ：编写一个方法，接收三个整数，返回其中最大的那个。

3.  **递归求和** ：用递归方法计算 $1 + 2 + ... + n$ 的和。

---

**下一章预告：** 单个变量只能存一个值，要管理全班 50 个学生的成绩怎么办？数组和字符串——数据的"集装箱"，让你批量管理数据。

[继续第 6 章：数组与字符串 →](06-arrays-and-strings.md)