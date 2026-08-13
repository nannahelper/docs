# 第 12 章：综合项目实战 —— 学生管理系统

> **场景：** 你已经学完了 Java 的核心知识——变量、控制流、方法、面向对象、集合、异常处理、文件 I/O。现在是时候把它们全部整合起来，从零开发一个完整的命令行学生管理系统。这个项目将是你 Java 学习之路的"毕业设计"。

---

## 12.1 项目需求

开发一个命令行界面的学生成绩管理系统，支持以下功能：

| 功能 | 说明 |
|:---|:---|
| 添加学生 | 输入姓名、学号、成绩 |
| 查看所有学生 | 列表展示所有学生信息 |
| 查找学生 | 按学号或姓名查找 |
| 修改成绩 | 修改指定学生的成绩 |
| 删除学生 | 删除指定学生 |
| 成绩统计 | 平均分、最高分、最低分、排名 |
| 保存到文件 | 将数据持久化到 CSV 文件 |
| 从文件加载 | 启动时自动加载已有数据 |

---

## 12.2 项目结构

```
StudentManager/
├── Student.java          # 学生实体类
├── StudentManager.java   # 核心管理逻辑
└── Main.java             # 程序入口 + 菜单交互
```

---

## 12.3 完整代码

### Student.java —— 学生实体类

```java
import java.io.Serializable;

/**
 * 学生实体类 —— 描述一个学生的属性和行为
 */
public class Student implements Serializable {
    private String name;
    private String studentId;
    private double score;
    
    public Student(String name, String studentId, double score) {
        this.name = name;
        this.studentId = studentId;
        setScore(score);  // 使用 setter 进行验证
    }
    
    // ===== Getter 方法 =====
    public String getName() { return name; }
    public String getStudentId() { return studentId; }
    public double getScore() { return score; }
    
    // ===== Setter 方法（带验证） =====
    public void setName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("姓名不能为空");
        }
        this.name = name.trim();
    }
    
    public void setScore(double score) {
        if (score < 0 || score > 100) {
            throw new IllegalArgumentException("成绩必须在 0~100 之间");
        }
        this.score = score;
    }
    
    /**
     * 获取成绩等级
     */
    public String getGrade() {
        if (score >= 90)      return "优秀";
        else if (score >= 80) return "良好";
        else if (score >= 70) return "中等";
        else if (score >= 60) return "及格";
        else                  return "不及格";
    }
    
    /**
     * 转换为 CSV 格式（用于保存到文件）
     */
    public String toCSV() {
        return name + "," + studentId + "," + score;
    }
    
    /**
     * 从 CSV 行创建 Student 对象
     */
    public static Student fromCSV(String csvLine) {
        String[] parts = csvLine.split(",");
        if (parts.length != 3) {
            throw new IllegalArgumentException("CSV 格式错误: " + csvLine);
        }
        return new Student(parts[0], parts[1], Double.parseDouble(parts[2]));
    }
    
    @Override
    public String toString() {
        return String.format("%-8s | %-10s | %6.1f 分 | %s",
                name, studentId, score, getGrade());
    }
}
```

### StudentManager.java —— 核心管理逻辑

```java
import java.io.*;
import java.util.*;

/**
 * 学生管理器 —— 负责学生的增删改查和统计
 */
public class StudentManager {
    private HashMap<String, Student> students;  // 学号 → 学生
    private static final String DATA_FILE = "student_data.csv";
    
    public StudentManager() {
        students = new HashMap<>();
        loadFromFile();  // 启动时自动加载数据
    }
    
    /**
     * 添加学生
     */
    public boolean addStudent(String name, String studentId, double score) {
        if (students.containsKey(studentId)) {
            System.out.println("错误：学号 " + studentId + " 已存在！");
            return false;
        }
        try {
            Student student = new Student(name, studentId, score);
            students.put(studentId, student);
            System.out.println("添加成功：" + student.getName());
            return true;
        } catch (IllegalArgumentException e) {
            System.out.println("添加失败：" + e.getMessage());
            return false;
        }
    }
    
    /**
     * 查看所有学生
     */
    public void listAllStudents() {
        if (students.isEmpty()) {
            System.out.println("暂无学生数据。");
            return;
        }
        
        System.out.println("\n===== 学生列表（共 " + students.size() + " 人）=====");
        System.out.println(String.format("%-8s | %-10s | %-8s | %s", 
                "姓名", "学号", "成绩", "等级"));
        System.out.println("-".repeat(50));
        
        // 按学号排序显示
        ArrayList<String> ids = new ArrayList<>(students.keySet());
        Collections.sort(ids);
        
        for (String id : ids) {
            System.out.println(students.get(id));
        }
    }
    
    /**
     * 按学号查找
     */
    public Student findByStudentId(String studentId) {
        return students.get(studentId);
    }
    
    /**
     * 按姓名查找（可能多个）
     */
    public ArrayList<Student> findByName(String name) {
        ArrayList<Student> result = new ArrayList<>();
        for (Student s : students.values()) {
            if (s.getName().contains(name)) {
                result.add(s);
            }
        }
        return result;
    }
    
    /**
     * 修改成绩
     */
    public boolean updateScore(String studentId, double newScore) {
        Student student = students.get(studentId);
        if (student == null) {
            System.out.println("错误：学号 " + studentId + " 不存在！");
            return false;
        }
        try {
            student.setScore(newScore);
            System.out.println("成绩已更新：" + student.getName() + " → " + newScore + " 分");
            return true;
        } catch (IllegalArgumentException e) {
            System.out.println("修改失败：" + e.getMessage());
            return false;
        }
    }
    
    /**
     * 删除学生
     */
    public boolean deleteStudent(String studentId) {
        Student removed = students.remove(studentId);
        if (removed == null) {
            System.out.println("错误：学号 " + studentId + " 不存在！");
            return false;
        }
        System.out.println("已删除：" + removed.getName());
        return true;
    }
    
    /**
     * 成绩统计
     */
    public void showStatistics() {
        if (students.isEmpty()) {
            System.out.println("暂无学生数据。");
            return;
        }
        
        ArrayList<Double> scores = new ArrayList<>();
        for (Student s : students.values()) {
            scores.add(s.getScore());
        }
        
        double sum = 0;
        double max = scores.get(0);
        double min = scores.get(0);
        
        for (double s : scores) {
            sum += s;
            if (s > max) max = s;
            if (s < min) min = s;
        }
        
        double avg = sum / scores.size();
        
        // 统计各等级人数
        int excellent = 0, good = 0, medium = 0, pass = 0, fail = 0;
        for (Student s : students.values()) {
            switch (s.getGrade()) {
                case "优秀": excellent++; break;
                case "良好": good++; break;
                case "中等": medium++; break;
                case "及格": pass++; break;
                case "不及格": fail++; break;
            }
        }
        
        System.out.println("\n===== 成绩统计 =====");
        System.out.println("学生总数: " + students.size());
        System.out.println("平均分:   " + String.format("%.1f", avg));
        System.out.println("最高分:   " + String.format("%.1f", max));
        System.out.println("最低分:   " + String.format("%.1f", min));
        System.out.println("\n等级分布:");
        System.out.println("  优秀: " + excellent + " 人 " + "★".repeat(excellent));
        System.out.println("  良好: " + good + " 人 " + "★".repeat(good));
        System.out.println("  中等: " + medium + " 人 " + "★".repeat(medium));
        System.out.println("  及格: " + pass + " 人 " + "★".repeat(pass));
        System.out.println("  不及格: " + fail + " 人 " + "★".repeat(fail));
    }
    
    /**
     * 成绩排名
     */
    public void showRanking() {
        if (students.isEmpty()) {
            System.out.println("暂无学生数据。");
            return;
        }
        
        ArrayList<Student> list = new ArrayList<>(students.values());
        list.sort((a, b) -> Double.compare(b.getScore(), a.getScore()));
        
        System.out.println("\n===== 成绩排名 =====");
        System.out.println(String.format("%-4s | %-8s | %-10s | %s", 
                "排名", "姓名", "学号", "成绩"));
        System.out.println("-".repeat(45));
        
        for (int i = 0; i < list.size(); i++) {
            Student s = list.get(i);
            System.out.println(String.format("%-4d | %-8s | %-10s | %.1f 分",
                    i + 1, s.getName(), s.getStudentId(), s.getScore()));
        }
    }
    
    /**
     * 保存数据到文件
     */
    public void saveToFile() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(DATA_FILE))) {
            for (Student s : students.values()) {
                writer.println(s.toCSV());
            }
            System.out.println("数据已保存到 " + DATA_FILE + "（" + students.size() + " 条记录）");
        } catch (IOException e) {
            System.out.println("保存失败：" + e.getMessage());
        }
    }
    
    /**
     * 从文件加载数据
     */
    private void loadFromFile() {
        File file = new File(DATA_FILE);
        if (!file.exists()) {
            return;  // 文件不存在，跳过
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            int count = 0;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty()) continue;
                try {
                    Student s = Student.fromCSV(line);
                    students.put(s.getStudentId(), s);
                    count++;
                } catch (Exception e) {
                    System.out.println("跳过无效行: " + line);
                }
            }
            if (count > 0) {
                System.out.println("已从文件加载 " + count + " 条学生记录。");
            }
        } catch (IOException e) {
            System.out.println("加载数据失败：" + e.getMessage());
        }
    }
}
```

### Main.java —— 程序入口 + 菜单交互

```java
import java.util.ArrayList;
import java.util.Scanner;

/**
 * 学生管理系统 —— 主程序
 */
public class Main {
    private static StudentManager manager = new StudentManager();
    private static Scanner scanner = new Scanner(System.in);
    
    public static void main(String[] args) {
        System.out.println("========================================");
        System.out.println("     欢迎使用学生成绩管理系统 v1.0");
        System.out.println("========================================");
        
        boolean running = true;
        while (running) {
            printMenu();
            System.out.print("\n请选择操作 [1-8]: ");
            String choice = scanner.nextLine().trim();
            
            switch (choice) {
                case "1": addStudent(); break;
                case "2": manager.listAllStudents(); break;
                case "3": searchStudent(); break;
                case "4": updateScore(); break;
                case "5": deleteStudent(); break;
                case "6": manager.showStatistics(); break;
                case "7": manager.showRanking(); break;
                case "8": 
                    manager.saveToFile();
                    running = false;
                    break;
                default:
                    System.out.println("无效选择，请输入 1-8。");
            }
        }
        
        System.out.println("\n感谢使用，再见！");
        scanner.close();
    }
    
    private static void printMenu() {
        System.out.println("\n========== 主菜单 ==========");
        System.out.println("1. 添加学生");
        System.out.println("2. 查看所有学生");
        System.out.println("3. 查找学生");
        System.out.println("4. 修改成绩");
        System.out.println("5. 删除学生");
        System.out.println("6. 成绩统计");
        System.out.println("7. 成绩排名");
        System.out.println("8. 保存并退出");
    }
    
    private static void addStudent() {
        System.out.println("\n===== 添加学生 =====");
        System.out.print("姓名: ");
        String name = scanner.nextLine().trim();
        System.out.print("学号: ");
        String id = scanner.nextLine().trim();
        System.out.print("成绩: ");
        try {
            double score = Double.parseDouble(scanner.nextLine().trim());
            manager.addStudent(name, id, score);
        } catch (NumberFormatException e) {
            System.out.println("错误：成绩必须是数字！");
        }
    }
    
    private static void searchStudent() {
        System.out.println("\n===== 查找学生 =====");
        System.out.println("1. 按学号查找");
        System.out.println("2. 按姓名查找");
        System.out.print("请选择: ");
        String choice = scanner.nextLine().trim();
        
        if (choice.equals("1")) {
            System.out.print("请输入学号: ");
            String id = scanner.nextLine().trim();
            Student s = manager.findByStudentId(id);
            if (s != null) {
                System.out.println("\n查找结果:");
                System.out.println(String.format("%-8s | %-10s | %-8s | %s", 
                        "姓名", "学号", "成绩", "等级"));
                System.out.println(s);
            } else {
                System.out.println("未找到学号为 " + id + " 的学生。");
            }
        } else if (choice.equals("2")) {
            System.out.print("请输入姓名（支持模糊搜索）: ");
            String name = scanner.nextLine().trim();
            ArrayList<Student> results = manager.findByName(name);
            if (results.isEmpty()) {
                System.out.println("未找到包含 '" + name + "' 的学生。");
            } else {
                System.out.println("\n找到 " + results.size() + " 个学生:");
                System.out.println(String.format("%-8s | %-10s | %-8s | %s", 
                        "姓名", "学号", "成绩", "等级"));
                for (Student s : results) {
                    System.out.println(s);
                }
            }
        } else {
            System.out.println("无效选择。");
        }
    }
    
    private static void updateScore() {
        System.out.println("\n===== 修改成绩 =====");
        System.out.print("请输入学号: ");
        String id = scanner.nextLine().trim();
        System.out.print("请输入新成绩: ");
        try {
            double newScore = Double.parseDouble(scanner.nextLine().trim());
            manager.updateScore(id, newScore);
        } catch (NumberFormatException e) {
            System.out.println("错误：成绩必须是数字！");
        }
    }
    
    private static void deleteStudent() {
        System.out.println("\n===== 删除学生 =====");
        System.out.print("请输入要删除的学生学号: ");
        String id = scanner.nextLine().trim();
        System.out.print("确认删除？(y/n): ");
        String confirm = scanner.nextLine().trim();
        if (confirm.equalsIgnoreCase("y")) {
            manager.deleteStudent(id);
        } else {
            System.out.println("已取消删除。");
        }
    }
}
```

---

## 12.4 运行演示

```
========================================
     欢迎使用学生成绩管理系统 v1.0
========================================

========== 主菜单 ==========
1. 添加学生
2. 查看所有学生
3. 查找学生
4. 修改成绩
5. 删除学生
6. 成绩统计
7. 成绩排名
8. 保存并退出

请选择操作 [1-8]: 1

===== 添加学生 =====
姓名: 张三
学号: 2024001
成绩: 85
添加成功：张三

请选择操作 [1-8]: 1

===== 添加学生 =====
姓名: 李四
学号: 2024002
成绩: 92
添加成功：李四

请选择操作 [1-8]: 2

===== 学生列表（共 2 人）=====
姓名       | 学号         | 成绩       | 等级
--------------------------------------------------
张三       | 2024001     |   85.0 分 | 良好
李四       | 2024002     |   92.0 分 | 优秀

请选择操作 [1-8]: 6

===== 成绩统计 =====
学生总数: 2
平均分:   88.5
最高分:   92.0
最低分:   85.0

等级分布:
  优秀: 1 人 ★
  良好: 1 人 ★
  中等: 0 人 
  及格: 0 人 
  不及格: 0 人 

请选择操作 [1-8]: 8
数据已保存到 student_data.csv（2 条记录）

感谢使用，再见！
```

---

## 12.5 项目总结

!!! tip "这个项目用到的知识点"
    | 知识点 | 在项目中的应用 |
    |:---|:---|
    | 类与对象 | `Student` 实体类封装学生数据 |
    | 封装 | `private` 属性 + getter/setter + 数据验证 |
    | 构造方法 | `Student(name, id, score)` 创建对象 |
    | 方法 | `addStudent()`、`findByName()` 等 |
    | 集合框架 | `HashMap<String, Student>` 存储学生数据 |
    | 异常处理 | `try-catch` 处理文件读写和数字解析错误 |
    | 文件 I/O | CSV 格式的读写，数据持久化 |
    | 控制流程 | `switch` 菜单选择，`for` 循环遍历 |
    | 字符串操作 | `split()` 解析 CSV，`format()` 格式化输出 |

---

## 课后练习

1.  **功能扩展** ：为系统添加"按成绩区间筛选"功能（如查看所有 80~90 分的学生）。

2.  **数据验证增强** ：确保学号唯一且格式正确（如必须是 7 位数字）。

3.  **多班级支持** ：扩展系统支持多个班级，每个班级独立管理学生。

---

🎉 **恭喜你完成了 Java 新手指南的全部内容！** 你已经掌握了 Java 编程的核心知识，能够独立开发命令行应用程序。接下来可以继续学习 Java 高级特性（多线程、网络编程、数据库操作）或转向 Spring 框架进行 Web 开发。