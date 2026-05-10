# 第 11 章：文件输入输出 —— 数据的"持久化"

> **场景：** 你的学生管理系统运行得很好，但每次关掉程序，所有数据都消失了。文件 I/O（输入输出）让你把数据保存到硬盘上——下次打开程序时，数据还在。就像把纸质档案存进档案柜，随时可以取出来查阅。

---

## 11.1 为什么需要文件 I/O？

!!! example "核心比喻：内存 vs 文件就像白板 vs 笔记本"
    内存（RAM）像教室里的白板——写字快，但一擦就没了，容量有限。
    
    硬盘上的文件像笔记本——写字慢一些，但可以永久保存，容量大得多。
    
    文件 I/O 就是"把白板上的重要内容抄到笔记本上"的过程。

---

## 11.2 写入文件

```java
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class FileWriteDemo {
    public static void main(String[] args) {
        String filePath = "students.txt";
        
        try (PrintWriter writer = new PrintWriter(new FileWriter(filePath))) {
            // 写入学生数据
            writer.println("===== 学生名单 =====");
            writer.println("张三,2024001,85");
            writer.println("李四,2024002,92");
            writer.println("王五,2024003,78");
            writer.println("赵六,2024004,88");
            
            System.out.println("数据已写入: " + filePath);
            
        } catch (IOException e) {
            System.out.println("写入文件失败: " + e.getMessage());
        }
    }
}
```

**运行结果：**
```
数据已写入: students.txt
```

**生成的 `students.txt` 内容：**
```
===== 学生名单 =====
张三,2024001,85
李四,2024002,92
王五,2024003,78
赵六,2024004,88
```

!!! tip "try-with-resources"
    `try (资源声明) { ... }` 是 Java 7 引入的语法。括号内的资源会在 try 块结束后自动关闭，不需要手动调用 `.close()`。任何实现了 `AutoCloseable` 接口的类都可以这样用。

---

## 11.3 读取文件

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class FileReadDemo {
    public static void main(String[] args) {
        String filePath = "students.txt";
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            int lineNumber = 0;
            
            System.out.println("===== 读取文件: " + filePath + " =====");
            
            // 逐行读取
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                System.out.println(lineNumber + ": " + line);
            }
            
            System.out.println("\n共读取 " + lineNumber + " 行");
            
        } catch (IOException e) {
            System.out.println("读取文件失败: " + e.getMessage());
        }
    }
}
```

**运行结果：**
```
===== 读取文件: students.txt =====
1: ===== 学生名单 =====
2: 张三,2024001,85
3: 李四,2024002,92
4: 王五,2024003,78
5: 赵六,2024004,88

共读取 5 行
```

---

## 11.4 解析 CSV 数据

CSV（逗号分隔值）是最常见的数据交换格式。让我们解析学生数据：

```java
import java.io.*;
import java.util.ArrayList;

class Student {
    String name;
    String id;
    int score;
    
    public Student(String name, String id, int score) {
        this.name = name;
        this.id = id;
        this.score = score;
    }
    
    @Override
    public String toString() {
        return String.format("%s | %s | %d 分", name, id, score);
    }
}

public class CSVParser {
    public static void main(String[] args) {
        ArrayList<Student> students = new ArrayList<>();
        
        // 读取并解析 CSV
        try (BufferedReader reader = new BufferedReader(new FileReader("students.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                // 跳过标题行
                if (line.startsWith("=====")) continue;
                
                // 按逗号分割
                String[] parts = line.split(",");
                if (parts.length == 3) {
                    String name = parts[0];
                    String id = parts[1];
                    int score = Integer.parseInt(parts[2]);
                    students.add(new Student(name, id, score));
                }
            }
        } catch (IOException e) {
            System.out.println("读取失败: " + e.getMessage());
        } catch (NumberFormatException e) {
            System.out.println("数据格式错误: " + e.getMessage());
        }
        
        // 打印解析结果
        System.out.println("===== 解析结果 =====");
        int sum = 0;
        for (Student s : students) {
            System.out.println(s);
            sum += s.score;
        }
        System.out.println("\n平均分: " + (sum / (double) students.size()));
    }
}
```

**运行结果：**
```
===== 解析结果 =====
张三 | 2024001 | 85 分
李四 | 2024002 | 92 分
王五 | 2024003 | 78 分
赵六 | 2024004 | 88 分

平均分: 85.75
```

---

## 11.5 追加写入与文件检查

```java
import java.io.*;

public class FileAppendDemo {
    public static void main(String[] args) {
        String filePath = "log.txt";
        
        // 检查文件是否存在
        File file = new File(filePath);
        if (!file.exists()) {
            System.out.println("文件不存在，将创建新文件: " + filePath);
        } else {
            System.out.println("文件已存在，大小: " + file.length() + " 字节");
        }
        
        // 追加模式写入（第二个参数 true 表示追加）
        try (FileWriter fw = new FileWriter(filePath, true);
             PrintWriter writer = new PrintWriter(fw)) {
            
            writer.println("[" + java.time.LocalDateTime.now() + "] 程序启动");
            writer.println("[" + java.time.LocalDateTime.now() + "] 数据加载完成");
            
            System.out.println("日志已追加到: " + filePath);
            
        } catch (IOException e) {
            System.out.println("写入失败: " + e.getMessage());
        }
    }
}
```

**运行结果：**
```
文件不存在，将创建新文件: log.txt
日志已追加到: log.txt
```

---

## 要点总结

- [x] `FileWriter` + `PrintWriter` 写入文件
- [x] `FileReader` + `BufferedReader` 读取文件
- [x] `try-with-resources` 自动关闭文件资源
- [x] `readLine()` 逐行读取，读到末尾返回 `null`
- [x] `split(",")` 解析 CSV 格式数据
- [x] `new FileWriter(path, true)` 追加模式写入
- [x] `File` 类检查文件是否存在、获取文件大小

---

## 课后练习

1.  **日记本** ：编写程序，让用户输入日记内容，追加写入 `diary.txt` 文件。

2.  **成绩导入** ：从 CSV 文件中读取学生成绩，计算总分和平均分，将统计结果写入另一个文件。

3.  **文件复制** ：编写程序，将一个文本文件的内容复制到另一个文件中。

---

**下一章预告：** 你已经学完了 Java 的所有核心知识。最后一章将把它们全部整合起来——从零开发一个完整的命令行学生管理系统！

[继续第 12 章：综合项目实战 →](12-final-project.md)