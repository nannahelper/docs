# 第 6 章：数组与字符串 —— 数据的"集装箱"

> **场景：** 你要管理全班 50 个学生的成绩。如果声明 50 个变量 `score1, score2, ..., score50`，代码会又臭又长。数组让你用一个变量名管理一整排数据——就像集装箱能一次装下很多货物。

---

## 6.1 什么是数组？

!!! example "核心比喻：数组就像停车场的车位"
    一个停车场有一排 10 个车位，编号从 0 到 9。每个车位可以停一辆车（存一个数据），你可以通过车位号快速找到对应的车。
    
    数组就是这样的"数据停车场"——**连续排列、编号访问、类型统一**。

```java
// 数组的三个特征：
// 1. 类型统一：一个数组只能存同一种类型的数据
// 2. 连续排列：元素在内存中一个挨一个
// 3. 编号访问：通过索引（从 0 开始）快速定位
```

---

## 6.2 数组的创建与使用

```java
public class ArrayDemo {
    public static void main(String[] args) {
        // ===== 方式1：先声明，再分配空间 =====
        int[] scores;
        scores = new int[5];  // 分配 5 个"车位"
        
        // ===== 方式2：声明 + 分配一步完成 =====
        double[] heights = new double[3];
        
        // ===== 方式3：声明 + 初始化一步完成 =====
        String[] names = {"张三", "李四", "王五", "赵六"};
        
        // ===== 给数组元素赋值 =====
        scores[0] = 85;  // 第 1 个元素（索引 0）
        scores[1] = 92;
        scores[2] = 78;
        scores[3] = 88;
        scores[4] = 95;
        
        // ===== 访问数组元素 =====
        System.out.println("第 1 个学生成绩: " + scores[0]);
        System.out.println("第 3 个学生成绩: " + scores[2]);
        System.out.println("学生总数: " + scores.length);  // 数组长度
        
        // ===== 遍历数组 =====
        System.out.println("\n===== 所有成绩 =====");
        for (int i = 0; i < scores.length; i++) {
            System.out.println("学生" + (i+1) + ": " + scores[i] + " 分");
        }
    }
}
```

**运行结果：**
```
第 1 个学生成绩: 85
第 3 个学生成绩: 78
学生总数: 5

===== 所有成绩 =====
学生1: 85 分
学生2: 92 分
学生3: 78 分
学生4: 88 分
学生5: 95 分
```

!!! warning "数组索引从 0 开始"
    `scores[0]` 是第一个元素，`scores[4]` 是第五个元素。访问 `scores[5]` 会抛出 `ArrayIndexOutOfBoundsException`（数组越界异常）。

---

## 6.3 数组的常用操作

```java
public class ArrayOperations {
    public static void main(String[] args) {
        int[] scores = {85, 92, 78, 88, 95, 62, 73, 90};
        
        // ===== 计算总分和平均分 =====
        int sum = 0;
        for (int i = 0; i < scores.length; i++) {
            sum += scores[i];
        }
        double average = (double) sum / scores.length;
        System.out.println("总分: " + sum);
        System.out.println("平均分: " + String.format("%.1f", average));
        
        // ===== 找最高分和最低分 =====
        int max = scores[0];
        int min = scores[0];
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] > max) max = scores[i];
            if (scores[i] < min) min = scores[i];
        }
        System.out.println("最高分: " + max);
        System.out.println("最低分: " + min);
        
        // ===== 统计及格人数 =====
        int passCount = 0;
        for (int score : scores) {  // 增强 for 循环（for-each）
            if (score >= 60) {
                passCount++;
            }
        }
        System.out.println("及格人数: " + passCount + "/" + scores.length);
    }
}
```

**运行结果：**
```
总分: 663
平均分: 82.9
最高分: 95
最低分: 62
及格人数: 8/8
```

### 增强 for 循环（for-each）

```java
// 传统 for 循环
for (int i = 0; i < scores.length; i++) {
    System.out.println(scores[i]);
}

// 增强 for 循环（更简洁，但不能获取索引）
for (int score : scores) {
    System.out.println(score);
}
```

---

## 6.4 数组排序

```java
import java.util.Arrays;

public class ArraySort {
    public static void main(String[] args) {
        int[] scores = {85, 92, 78, 88, 95, 62, 73, 90};
        
        // 排序前
        System.out.println("排序前: " + Arrays.toString(scores));
        
        // 升序排序
        Arrays.sort(scores);
        System.out.println("排序后: " + Arrays.toString(scores));
        
        // 反转（手动实现降序）
        System.out.print("降序:   [");
        for (int i = scores.length - 1; i >= 0; i--) {
            System.out.print(scores[i]);
            if (i > 0) System.out.print(", ");
        }
        System.out.println("]");
    }
}
```

**运行结果：**
```
排序前: [85, 92, 78, 88, 95, 62, 73, 90]
排序后: [62, 73, 78, 85, 88, 90, 92, 95]
降序:   [95, 92, 90, 88, 85, 78, 73, 62]
```

---

## 6.5 二维数组：表格数据

```java
public class TwoDArray {
    public static void main(String[] args) {
        // 3 个学生，每人 4 门课的成绩
        int[][] scoreTable = {
            {85, 92, 78, 88},  // 张三的成绩
            {90, 85, 92, 87},  // 李四的成绩
            {72, 88, 95, 80}   // 王五的成绩
        };
        
        String[] subjects = {"语文", "数学", "英语", "物理"};
        String[] students = {"张三", "李四", "王五"};
        
        // 打印成绩表
        System.out.println("===== 成绩表 =====");
        System.out.print("姓名\t");
        for (String sub : subjects) {
            System.out.print(sub + "\t");
        }
        System.out.println("平均");
        
        for (int i = 0; i < scoreTable.length; i++) {
            System.out.print(students[i] + "\t");
            int sum = 0;
            for (int j = 0; j < scoreTable[i].length; j++) {
                System.out.print(scoreTable[i][j] + "\t");
                sum += scoreTable[i][j];
            }
            System.out.println(String.format("%.1f", sum / 4.0));
        }
    }
}
```

**运行结果：**
```
===== 成绩表 =====
姓名    语文    数学    英语    物理    平均
张三    85      92      78      88      85.8
李四    90      85      92      87      88.5
王五    72      88      95      80      83.8
```

---

## 6.6 String 深入

```java
public class StringAdvanced {
    public static void main(String[] args) {
        String text = "  Hello, Java World!  ";
        
        // 去除首尾空格
        System.out.println("去空格: [" + text.trim() + "]");
        
        // 替换
        System.out.println("替换: " + text.replace("Java", "编程"));
        
        // 分割字符串
        String csv = "张三,85,92,78";
        String[] parts = csv.split(",");
        System.out.println("\n===== CSV 解析 =====");
        System.out.println("姓名: " + parts[0]);
        System.out.println("成绩: " + parts[1] + ", " + parts[2] + ", " + parts[3]);
        
        // 判断开头和结尾
        String file = "report.pdf";
        System.out.println("\n是 PDF 文件? " + file.endsWith(".pdf"));
        System.out.println("以 'rep' 开头? " + file.startsWith("rep"));
        
        // 查找子串位置
        String sentence = "今天天气真好，适合写代码";
        int pos = sentence.indexOf("代码");
        System.out.println("'代码' 在第 " + pos + " 个位置");
    }
}
```

**运行结果：**
```
去空格: [Hello, Java World!]
替换:   Hello, 编程 World!

===== CSV 解析 =====
姓名: 张三
成绩: 85, 92, 78

是 PDF 文件? true
以 'rep' 开头? true
'代码' 在第 10 个位置
```

---

## 要点总结

- [x] 数组 = 同类型数据的连续存储，通过索引（从 0 开始）访问
- [x] `数组名.length` 获取数组长度
- [x] 增强 for 循环（`for (类型 变量 : 数组)`）简化遍历
- [x] `Arrays.sort()` 排序，`Arrays.toString()` 打印
- [x] 二维数组 = 数组的数组，适合表格数据
- [x] String 常用方法：`trim()`、`replace()`、`split()`、`indexOf()`

---

## 课后练习

1.  **成绩统计** ：创建一个包含 10 个成绩的数组，计算平均分、最高分、最低分，并统计各等级人数。

2.  **数组反转** ：将一个数组的元素顺序反转（不使用额外数组）。

3.  **字符串统计** ：统计一段文字中某个字出现的次数。

---

**下一章预告：** 数组管理数据很方便，但数据和操作是分离的。面向对象编程让你把数据和操作"打包"在一起——就像设计一辆车，既有属性（颜色、速度）又有行为（加速、刹车）。

[继续第 7 章：面向对象编程（上）→](07-oop-basics.md)