# 第 10 章：集合框架 —— 数据的"超级仓库"

> **场景：** 你要管理一个班级的学生名单——随时有新同学加入、有同学转走。数组大小固定，增删元素非常麻烦。Java 集合框架提供了 `ArrayList`（动态数组）、`HashMap`（键值对）等强大工具，让你像操作"超级仓库"一样灵活管理数据。

---

## 10.1 为什么需要集合？

!!! example "核心比喻：数组 vs 集合就像固定车位 vs 立体车库"
    数组像地面停车场——10 个车位，建好就不能改。来第 11 辆车？没地方停。
    
    集合像立体车库——自动伸缩，来多少车都能停，车开走了位置自动释放。还能按车牌号（键）快速找到车的位置。

| 对比 | 数组 | 集合（ArrayList） |
|:---|:---|:---|
| 大小 | 固定，创建后不能改 | 动态，自动扩容 |
| 增删 | 麻烦，需要手动移动元素 | 简单，`.add()` `.remove()` |
| 类型 | 可以存基本类型 | 只能存引用类型（用包装类） |
| 功能 | 只有 `.length` | 丰富的 API（排序、查找、遍历） |

---

## 10.2 ArrayList：动态数组

```java
import java.util.ArrayList;
import java.util.Collections;

public class ArrayListDemo {
    public static void main(String[] args) {
        // 创建一个存储字符串的 ArrayList
        ArrayList<String> students = new ArrayList<>();
        
        // ===== 添加元素 =====
        students.add("张三");
        students.add("李四");
        students.add("王五");
        System.out.println("初始名单: " + students);
        
        // ===== 在指定位置插入 =====
        students.add(1, "赵六");  // 在索引 1 处插入
        System.out.println("插入后: " + students);
        
        // ===== 获取元素 =====
        String first = students.get(0);
        System.out.println("第一个学生: " + first);
        
        // ===== 修改元素 =====
        students.set(0, "张三丰");
        System.out.println("修改后: " + students);
        
        // ===== 删除元素 =====
        students.remove("王五");     // 按内容删除
        students.remove(1);          // 按索引删除
        System.out.println("删除后: " + students);
        
        // ===== 常用操作 =====
        System.out.println("学生总数: " + students.size());
        System.out.println("包含张三丰? " + students.contains("张三丰"));
        System.out.println("李四的索引: " + students.indexOf("李四"));
        
        // ===== 排序 =====
        Collections.sort(students);
        System.out.println("排序后: " + students);
        
        // ===== 遍历 =====
        System.out.println("\n===== 遍历学生 =====");
        for (int i = 0; i < students.size(); i++) {
            System.out.println((i+1) + ". " + students.get(i));
        }
        
        // 增强 for 循环遍历
        System.out.println("\n===== for-each 遍历 =====");
        for (String name : students) {
            System.out.println("→ " + name);
        }
    }
}
```

**运行结果：**
```
初始名单: [张三, 李四, 王五]
插入后: [张三, 赵六, 李四, 王五]
第一个学生: 张三
修改后: [张三丰, 赵六, 李四, 王五]
删除后: [张三丰, 李四]
学生总数: 2
包含张三丰? true
李四的索引: 1
排序后: [张三丰, 李四]

===== 遍历学生 =====
1. 张三丰
2. 李四

===== for-each 遍历 =====
→ 张三丰
→ 李四
```

!!! info "ArrayList 常用方法速查"
    | 方法 | 作用 |
    |:---|:---|
    | `.add(元素)` | 在末尾添加 |
    | `.add(索引, 元素)` | 在指定位置插入 |
    | `.get(索引)` | 获取元素 |
    | `.set(索引, 元素)` | 修改元素 |
    | `.remove(索引)` / `.remove(元素)` | 删除元素 |
    | `.size()` | 获取元素个数 |
    | `.contains(元素)` | 判断是否包含 |
    | `.indexOf(元素)` | 查找索引 |
    | `.clear()` | 清空所有元素 |

---

## 10.3 包装类：让基本类型也能放进集合

集合只能存引用类型，不能存基本类型。Java 为每种基本类型提供了对应的包装类：

| 基本类型 | 包装类 |
|:---|:---|
| `int` | `Integer` |
| `double` | `Double` |
| `char` | `Character` |
| `boolean` | `Boolean` |
| `long` | `Long` |
| `float` | `Float` |
| `short` | `Short` |
| `byte` | `Byte` |

```java
import java.util.ArrayList;

public class WrapperDemo {
    public static void main(String[] args) {
        // 存储成绩的 ArrayList
        ArrayList<Integer> scores = new ArrayList<>();
        
        // 自动装箱：基本类型自动转为包装类
        scores.add(85);   // int → Integer（自动）
        scores.add(92);
        scores.add(78);
        
        // 自动拆箱：包装类自动转为基本类型
        int first = scores.get(0);  // Integer → int（自动）
        
        // 计算平均分
        int sum = 0;
        for (Integer score : scores) {
            sum += score;  // 自动拆箱
        }
        double avg = (double) sum / scores.size();
        
        System.out.println("成绩: " + scores);
        System.out.println("总分: " + sum);
        System.out.println("平均: " + String.format("%.1f", avg));
    }
}
```

**运行结果：**
```
成绩: [85, 92, 78]
总分: 255
平均: 85.0
```

---

## 10.4 HashMap：键值对存储

!!! example "核心比喻：HashMap 就像字典"
    查字典时，你通过"单词"（键）找到"释义"（值）。HashMap 就是程序中的字典——通过一个键快速找到对应的值。

```java
import java.util.HashMap;

public class HashMapDemo {
    public static void main(String[] args) {
        // 创建 HashMap：学号 → 姓名
        HashMap<String, String> studentMap = new HashMap<>();
        
        // ===== 添加键值对 =====
        studentMap.put("2024001", "张三");
        studentMap.put("2024002", "李四");
        studentMap.put("2024003", "王五");
        studentMap.put("2024004", "赵六");
        
        // ===== 通过键获取值 =====
        String name = studentMap.get("2024002");
        System.out.println("学号 2024002 的学生: " + name);
        
        // ===== 检查键是否存在 =====
        System.out.println("包含 2024005? " + studentMap.containsKey("2024005"));
        
        // ===== 修改值（覆盖） =====
        studentMap.put("2024001", "张三丰");
        System.out.println("修改后 2024001: " + studentMap.get("2024001"));
        
        // ===== 删除 =====
        studentMap.remove("2024004");
        
        // ===== 遍历所有键值对 =====
        System.out.println("\n===== 所有学生 =====");
        for (String id : studentMap.keySet()) {
            System.out.println(id + " → " + studentMap.get(id));
        }
        
        // 更优雅的遍历方式
        System.out.println("\n===== entrySet 遍历 =====");
        for (HashMap.Entry<String, String> entry : studentMap.entrySet()) {
            System.out.println(entry.getKey() + " → " + entry.getValue());
        }
        
        System.out.println("\n学生总数: " + studentMap.size());
    }
}
```

**运行结果：**
```
学号 2024002 的学生: 李四
包含 2024005? false
修改后 2024001: 张三丰

===== 所有学生 =====
2024001 → 张三丰
2024002 → 李四
2024003 → 王五

===== entrySet 遍历 =====
2024001 → 张三丰
2024002 → 李四
2024003 → 王五

学生总数: 3
```

---

## 10.5 综合示例：学生成绩管理

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Collections;

public class ScoreManager {
    public static void main(String[] args) {
        // 用 HashMap 存储：姓名 → 成绩
        HashMap<String, Integer> scoreMap = new HashMap<>();
        scoreMap.put("张三", 85);
        scoreMap.put("李四", 92);
        scoreMap.put("王五", 78);
        scoreMap.put("赵六", 88);
        scoreMap.put("孙七", 95);
        
        // 用 ArrayList 存储所有成绩（方便排序）
        ArrayList<Integer> scores = new ArrayList<>(scoreMap.values());
        
        // 统计
        int sum = 0;
        for (int s : scores) sum += s;
        double avg = (double) sum / scores.size();
        
        Collections.sort(scores);
        int max = scores.get(scores.size() - 1);
        int min = scores.get(0);
        
        System.out.println("===== 成绩统计 =====");
        System.out.println("总分: " + sum);
        System.out.println("平均: " + String.format("%.1f", avg));
        System.out.println("最高: " + max);
        System.out.println("最低: " + min);
        
        // 找出最高分的学生
        System.out.println("\n===== 最高分学生 =====");
        for (String name : scoreMap.keySet()) {
            if (scoreMap.get(name) == max) {
                System.out.println(name + ": " + max + " 分");
            }
        }
        
        // 按成绩排序打印
        System.out.println("\n===== 成绩排名 =====");
        ArrayList<HashMap.Entry<String, Integer>> entries = 
            new ArrayList<>(scoreMap.entrySet());
        entries.sort((a, b) -> b.getValue() - a.getValue());  // 降序
        
        int rank = 1;
        for (HashMap.Entry<String, Integer> entry : entries) {
            System.out.println(rank + ". " + entry.getKey() + ": " + entry.getValue() + " 分");
            rank++;
        }
    }
}
```

**运行结果：**
```
===== 成绩统计 =====
总分: 438
平均: 87.6
最高: 95
最低: 78

===== 最高分学生 =====
孙七: 95 分

===== 成绩排名 =====
1. 孙七: 95 分
2. 李四: 92 分
3. 赵六: 88 分
4. 张三: 85 分
5. 王五: 78 分
```

---

## 要点总结

- [x] `ArrayList` 是动态数组，自动扩容，增删方便
- [x] 集合只能存引用类型，基本类型需要用包装类（`Integer`、`Double` 等）
- [x] 自动装箱/拆箱让基本类型和包装类之间自动转换
- [x] `HashMap` 是键值对存储，通过键快速查找值
- [x] `Collections.sort()` 排序，`.size()` 获取大小
- [x] 泛型 `<类型>` 指定集合中存储的数据类型

---

## 课后练习

1.  **购物清单** ：用 `ArrayList` 实现一个购物清单，支持添加、删除、查看和清空操作。

2.  **电话簿** ：用 `HashMap` 实现一个电话簿（姓名 → 电话号码），支持添加、查找、删除。

3.  **成绩分析** ：用 `ArrayList` 存储 10 个成绩，计算平均分、最高分、最低分，并统计各等级人数。

---

**下一章预告：** 程序运行时的数据存在内存中，关掉程序就没了。文件 I/O 让你把数据保存到硬盘上——下次打开程序还能读到之前的数据。

[继续第 11 章：文件输入输出 →](11-file-io.md)