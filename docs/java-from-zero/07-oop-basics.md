# 第 7 章：面向对象编程（上）—— 类的"蓝图"

> **场景：** 你要管理全校上万名学生。每个学生都有姓名、学号、成绩等属性，还有选课、考试等行为。如果只用数组和变量，代码会乱成一团。面向对象编程（OOP）让你把"学生"抽象成一个模板（类），然后像盖章一样批量"生产"学生对象——每个对象都有自己的属性和行为。

---

## 7.1 什么是面向对象？

!!! example "核心比喻：类就像饼干模具，对象就是饼干"
    你有一个星星形状的饼干模具（**类**）。用这个模具在面团上按一下，就做出一个星星饼干（**对象**）。再按一下，又一个。所有饼干形状一样，但你可以给它们装饰不同的糖霜（不同的属性值）。
    
    - **类（Class）** = 饼干模具 = 描述"学生应该有什么"的蓝图
    - **对象（Object）** = 饼干 = 按照蓝图造出来的具体学生
    - **属性（Field）** = 饼干的特征 = 学生的姓名、年龄、成绩
    - **方法（Method）** = 饼干的功能 = 学生可以做的事（考试、选课）

---

## 7.2 定义你的第一个类

```java
/**
 * Student 类 —— 描述一个学生应该有什么、能做什么
 */
public class Student {
    // ===== 属性（成员变量）=====
    String name;      // 姓名
    String studentId; // 学号
    int age;          // 年龄
    double score;     // 成绩
    
    // ===== 方法（行为）=====
    
    // 自我介绍
    public void introduce() {
        System.out.println("我叫" + name + "，学号" + studentId + "，今年" + age + "岁。");
    }
    
    // 考试
    public void takeExam(double newScore) {
        this.score = newScore;  // this 指代"当前这个对象"
        System.out.println(name + " 参加了考试，成绩: " + score);
    }
    
    // 判断是否及格
    public boolean isPassed() {
        return score >= 60;
    }
}
```

---

## 7.3 创建和使用对象

```java
public class StudentTest {
    public static void main(String[] args) {
        // 创建对象：用 new 关键字 + 构造方法
        Student zhangsan = new Student();
        Student lisi = new Student();
        
        // 给属性赋值
        zhangsan.name = "张三";
        zhangsan.studentId = "2024001";
        zhangsan.age = 20;
        
        lisi.name = "李四";
        lisi.studentId = "2024002";
        lisi.age = 21;
        
        // 调用方法
        zhangsan.introduce();
        zhangsan.takeExam(85);
        System.out.println("张三及格了吗？ " + zhangsan.isPassed());
        
        System.out.println();
        
        lisi.introduce();
        lisi.takeExam(55);
        System.out.println("李四及格了吗？ " + lisi.isPassed());
    }
}
```

**运行结果：**
```
我叫张三，学号2024001，今年20岁。
张三 参加了考试，成绩: 85.0
张三及格了吗？ true

我叫李四，学号2024002，今年21岁。
李四 参加了考试，成绩: 55.0
李四及格了吗？ false
```

!!! info "对象在内存中"
    每个 `new Student()` 都在内存中创建了一个独立的"小房间"，里面存放着这个学生的属性值。`zhangsan` 和 `lisi` 是两个不同的引用，指向两个不同的房间。

---

## 7.4 构造方法：对象的"出生设置"

每次 `new Student()` 后还要手动给属性赋值，太麻烦。构造方法让你在创建对象时就设置好属性：

```java
public class StudentV2 {
    String name;
    String studentId;
    int age;
    double score;
    
    // 构造方法：名字与类名相同，没有返回类型
    public StudentV2(String name, String studentId, int age) {
        this.name = name;           // this.name 是属性，name 是参数
        this.studentId = studentId;
        this.age = age;
        this.score = 0;             // 默认成绩为 0
    }
    
    // 方法重载：另一个构造方法（只传姓名和学号）
    public StudentV2(String name, String studentId) {
        this(name, studentId, 18);  // 调用上面的构造方法
    }
    
    public void introduce() {
        System.out.println(name + " | " + studentId + " | " + age + "岁 | " + score + "分");
    }
}
```

```java
public class ConstructorTest {
    public static void main(String[] args) {
        // 创建对象时直接传入属性值
        StudentV2 s1 = new StudentV2("张三", "2024001", 20);
        StudentV2 s2 = new StudentV2("李四", "2024002");  // 使用默认年龄 18
        
        s1.introduce();
        s2.introduce();
    }
}
```

**运行结果：**
```
张三 | 2024001 | 20岁 | 0.0分
李四 | 2024002 | 18岁 | 0.0分
```

!!! tip "this 关键字"
    `this` 指代"当前对象"。当参数名和属性名相同时，用 `this.name` 区分属性和参数。`this(参数)` 可以在构造方法中调用另一个构造方法。

---

## 7.5 封装：保护数据不被随意修改

直接把属性暴露给外部（`public`）是不安全的——别人可以把 `age` 设成 -5。封装通过 `private` + getter/setter 方法来保护数据：

```java
public class BankAccount {
    // 属性设为 private，外部不能直接访问
    private String owner;
    private double balance;
    private String password;
    
    public BankAccount(String owner, String password) {
        this.owner = owner;
        this.password = password;
        this.balance = 0;
    }
    
    // getter：获取余额（只读）
    public double getBalance() {
        return balance;
    }
    
    // getter：获取户主名
    public String getOwner() {
        return owner;
    }
    
    // setter：存款（有验证逻辑）
    public void deposit(double amount) {
        if (amount <= 0) {
            System.out.println("存款金额必须大于 0！");
            return;
        }
        balance += amount;
        System.out.println("存入 " + amount + " 元，余额: " + balance);
    }
    
    // setter：取款（需要密码验证）
    public boolean withdraw(double amount, String pwd) {
        if (!pwd.equals(password)) {
            System.out.println("密码错误！");
            return false;
        }
        if (amount > balance) {
            System.out.println("余额不足！");
            return false;
        }
        balance -= amount;
        System.out.println("取出 " + amount + " 元，余额: " + balance);
        return true;
    }
}
```

```java
public class BankTest {
    public static void main(String[] args) {
        BankAccount account = new BankAccount("张三", "123456");
        
        System.out.println("户主: " + account.getOwner());
        System.out.println("初始余额: " + account.getBalance());
        
        account.deposit(1000);
        account.deposit(-50);  // 被拦截
        
        account.withdraw(300, "wrong");   // 密码错误
        account.withdraw(300, "123456");  // 成功
        account.withdraw(800, "123456");  // 余额不足
    }
}
```

**运行结果：**
```
户主: 张三
初始余额: 0.0
存入 1000.0 元，余额: 1000.0
存款金额必须大于 0！
密码错误！
取出 300.0 元，余额: 700.0
余额不足！
```

!!! info "封装的三大好处"
    | 好处 | 说明 |
    |:---|:---|
    | **数据保护** | 防止非法值（如负年龄、负余额） |
    | **隐藏细节** | 外部只需知道"能做什么"，不需要知道"怎么做" |
    | **灵活修改** | 内部实现可以改，只要接口不变，外部代码不用改 |

---

## 要点总结

- [x] 类 = 对象的蓝图/模具，对象 = 类的具体实例
- [x] 属性（成员变量）描述对象的状态
- [x] 方法描述对象的行为
- [x] `new 类名()` 创建对象
- [x] 构造方法与类同名，在创建对象时自动调用
- [x] `this` 指代当前对象
- [x] `private` + getter/setter 实现封装，保护数据

---

## 课后练习

1.  **图书类** ：设计一个 `Book` 类，包含书名、作者、价格、库存属性，以及借出和归还方法。

2.  **手机类** ：设计一个 `Phone` 类，包含品牌、型号、电量属性，以及开机、关机、充电方法。

3.  **改进 Student 类** ：给 Student 类添加封装，确保年龄在 1~150 之间，成绩在 0~100 之间。

---

**下一章预告：** 一个类只能描述一种东西。但"研究生"也是"学生"，"老师"也是"人"——继承和多态让你描述"is-a"关系，实现代码复用和灵活扩展。

[继续第 8 章：面向对象编程（下）→](08-oop-advanced.md)