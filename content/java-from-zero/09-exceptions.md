# 第 9 章：异常处理 —— 程序的"安全气囊"

> **场景：** 你写了一个除法计算器，用户输入 `10 / 0`，程序直接崩溃了。或者用户输入了字母而不是数字，程序又崩溃了。异常处理让程序在遇到错误时不崩溃，而是优雅地提示用户并继续运行——就像汽车的安全气囊，撞车时保护乘客而不是让车爆炸。

---

## 9.1 什么是异常？

!!! example "核心比喻：异常就像开车时遇到的意外"
    你开车去学校，可能遇到：
    - 轮胎爆了（**运行时异常**）——你没法预测，但可以准备备胎
    - 前方修路（**检查型异常**）——导航提前告诉你，你必须绕路
    
    异常就是程序运行时遇到的"意外情况"。Java 把异常分为两类：一种你必须处理，一种你可以选择处理。

```java
// 常见的异常示例
public class ExceptionExamples {
    public static void main(String[] args) {
        // 1. 除零异常：ArithmeticException
        // int result = 10 / 0;
        
        // 2. 空指针异常：NullPointerException
        // String str = null;
        // str.length();
        
        // 3. 数组越界：ArrayIndexOutOfBoundsException
        // int[] arr = {1, 2, 3};
        // arr[5] = 10;
        
        // 4. 数字格式异常：NumberFormatException
        // int num = Integer.parseInt("abc");
        
        System.out.println("这些异常如果不处理，程序会直接崩溃！");
    }
}
```

---

## 9.2 try-catch：捕获异常

```java
import java.util.Scanner;

public class TryCatchDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        try {
            // 可能出错的代码放在 try 块里
            System.out.print("请输入被除数: ");
            int a = scanner.nextInt();
            
            System.out.print("请输入除数: ");
            int b = scanner.nextInt();
            
            int result = a / b;
            System.out.println(a + " / " + b + " = " + result);
            
        } catch (ArithmeticException e) {
            // 捕获除零异常
            System.out.println("错误：除数不能为 0！");
            System.out.println("异常信息: " + e.getMessage());
            
        } catch (Exception e) {
            // 捕获其他所有异常
            System.out.println("发生未知错误: " + e.getMessage());
            
        } finally {
            // finally 块中的代码无论是否发生异常都会执行
            System.out.println("计算结束，感谢使用！");
            scanner.close();
        }
    }
}
```

**运行结果（正常输入）：**
```
请输入被除数: 10
请输入除数: 2
10 / 2 = 5
计算结束，感谢使用！
```

**运行结果（除零）：**
```
请输入被除数: 10
请输入除数: 0
错误：除数不能为 0！
异常信息: / by zero
计算结束，感谢使用！
```

!!! info "try-catch-finally 结构"
    | 块 | 作用 | 是否必须 |
    |:---|:---|:---|
    | `try` | 包含可能抛出异常的代码 | 必须 |
    | `catch` | 捕获并处理特定类型的异常 | 至少一个 |
    | `finally` | 无论是否异常都会执行的清理代码 | 可选 |

---

## 9.3 throws：声明异常

有些异常你必须处理，否则编译不通过。可以用 `throws` 声明"这个方法可能抛出异常，调用者来处理"：

```java
import java.io.*;

public class ThrowsDemo {
    // 声明这个方法可能抛出 IOException
    public static void readFile(String path) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(path));
        String line = reader.readLine();
        System.out.println("文件内容: " + line);
        reader.close();
    }
    
    public static void main(String[] args) {
        try {
            readFile("不存在的文件.txt");
        } catch (IOException e) {
            System.out.println("读取文件失败: " + e.getMessage());
            System.out.println("请检查文件路径是否正确。");
        }
    }
}
```

**运行结果：**
```
读取文件失败: 不存在的文件.txt (系统找不到指定的文件。)
请检查文件路径是否正确。
```

---

## 9.4 自定义异常

当 Java 内置的异常不够用时，可以创建自己的异常类：

```java
// 自定义异常：成绩不合法
class InvalidScoreException extends Exception {
    public InvalidScoreException(String message) {
        super(message);
    }
}

// 自定义异常：年龄不合法
class InvalidAgeException extends RuntimeException {
    public InvalidAgeException(String message) {
        super(message);
    }
}

public class CustomExceptionDemo {
    // 使用自定义异常验证学生数据
    public static void validateStudent(String name, int age, double score) 
            throws InvalidScoreException {
        
        if (age < 1 || age > 150) {
            throw new InvalidAgeException("年龄不合法: " + age + "（应在 1~150 之间）");
        }
        
        if (score < 0 || score > 100) {
            throw new InvalidScoreException("成绩不合法: " + score + "（应在 0~100 之间）");
        }
        
        System.out.println("学生信息验证通过: " + name + ", " + age + "岁, " + score + "分");
    }
    
    public static void main(String[] args) {
        // 测试合法数据
        try {
            validateStudent("张三", 20, 85);
        } catch (InvalidScoreException e) {
            System.out.println("验证失败: " + e.getMessage());
        }
        
        // 测试非法成绩
        try {
            validateStudent("李四", 22, 150);
        } catch (InvalidScoreException e) {
            System.out.println("验证失败: " + e.getMessage());
        }
        
        // 测试非法年龄（运行时异常，可以不捕获）
        try {
            validateStudent("王五", -5, 80);
        } catch (InvalidScoreException e) {
            System.out.println("验证失败: " + e.getMessage());
        } catch (InvalidAgeException e) {
            System.out.println("验证失败: " + e.getMessage());
        }
    }
}
```

**运行结果：**
```
学生信息验证通过: 张三, 20岁, 85.0分
验证失败: 成绩不合法: 150.0（应在 0~100 之间）
验证失败: 年龄不合法: -5（应在 1~150 之间）
```

!!! tip "异常设计原则"
    - **不要用异常控制正常流程**：异常只用于"异常情况"
    - **尽早抛出，延迟捕获**：在出错的地方抛，在能处理的地方捕获
    - **提供有意义的错误信息**：让调用者知道哪里错了、怎么改

---

## 要点总结

- [x] 异常 = 程序运行时的意外情况
- [x] `try-catch` 捕获并处理异常，程序不会崩溃
- [x] `finally` 中的代码无论是否异常都会执行（常用于关闭资源）
- [x] `throws` 声明方法可能抛出的异常
- [x] `throw` 手动抛出异常
- [x] 自定义异常继承 `Exception`（检查型）或 `RuntimeException`（运行时）

---

## 课后练习

1.  **安全除法** ：编写一个除法方法，当除数为 0 时抛出 `IllegalArgumentException`，在 main 中捕获并提示用户。

2.  **年龄验证** ：编写一个方法验证年龄（1~150），不合法时抛出自定义异常。

3.  **文件读取** ：尝试读取一个文件，如果文件不存在则创建它（使用 try-catch）。

---

**下一章预告：** 数组大小固定，操作也不方便。Java 集合框架提供了 ArrayList（动态数组）、HashMap（键值对）等强大工具——数据的"超级仓库"。

[继续第 10 章：集合框架 →](10-collections.md)