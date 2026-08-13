# 第 8 章：面向对象编程（下）—— 继承与多态

> **场景：** 你已经有了 `Student` 类。但大学里还有 `GraduateStudent`（研究生），他们除了有学生的所有属性，还有导师和研究方向。与其重写一遍代码，不如让 `GraduateStudent` **继承** `Student`——自动获得所有属性和方法，再添加自己特有的内容。

---

## 8.1 继承：子承父业

!!! example "核心比喻：继承就像家族基因"
    你继承了父亲的身高和母亲的肤色（**属性**），也学会了家族祖传的做饭手艺（**方法**）。但你也可以发展自己的特长——比如编程（**新增方法**），或者改良做饭手艺（**重写方法**）。
    
    在 Java 中，子类用 `extends` 关键字继承父类，自动获得父类的所有属性和方法。

```java
// 父类：学生
public class Student {
    protected String name;      // protected：子类可以访问
    protected String studentId;
    protected double score;
    
    public Student(String name, String studentId) {
        this.name = name;
        this.studentId = studentId;
    }
    
    public void study() {
        System.out.println(name + " 正在学习...");
    }
    
    public void introduce() {
        System.out.println("我叫" + name + "，学号" + studentId);
    }
}

// 子类：研究生（继承 Student）
public class GraduateStudent extends Student {
    private String supervisor;  // 导师
    private String researchArea; // 研究方向
    
    public GraduateStudent(String name, String studentId, 
                           String supervisor, String researchArea) {
        super(name, studentId);  // 调用父类的构造方法
        this.supervisor = supervisor;
        this.researchArea = researchArea;
    }
    
    // 重写父类的方法（加上研究生特有的信息）
    @Override
    public void introduce() {
        super.introduce();  // 先调用父类的 introduce
        System.out.println("我是研究生，导师: " + supervisor + "，方向: " + researchArea);
    }
    
    // 研究生特有的方法
    public void doResearch() {
        System.out.println(name + " 正在进行 " + researchArea + " 方向的研究...");
    }
}
```

```java
public class InheritanceTest {
    public static void main(String[] args) {
        // 普通学生
        Student undergrad = new Student("张三", "2024001");
        undergrad.introduce();
        undergrad.study();
        
        System.out.println();
        
        // 研究生
        GraduateStudent grad = new GraduateStudent("李四", "2023001", "王教授", "人工智能");
        grad.introduce();     // 调用重写后的方法
        grad.study();         // 继承自父类的方法
        grad.doResearch();    // 研究生特有的方法
    }
}
```

**运行结果：**
```
我叫张三，学号2024001
张三 正在学习...

我叫李四，学号2023001
我是研究生，导师: 王教授，方向: 人工智能
李四 正在学习...
李四 正在进行 人工智能 方向的研究...
```

!!! info "继承的关键字"
    | 关键字 | 作用 |
    |:---|:---|
    | `extends` | 声明继承关系 |
    | `super` | 调用父类的构造方法或方法 |
    | `@Override` | 标注重写父类方法（可选但推荐，编译器会帮你检查） |
    | `protected` | 本类和子类可以访问（比 private 宽松，比 public 严格） |

---

## 8.2 多态：同一个方法，不同的表现

!!! example "核心比喻：多态就像"叫"这个动作"
    你对狗说"叫"，狗汪汪叫。你对猫说"叫"，猫喵喵叫。你对人说"叫"，人说"你好"。
    
    同一个指令"叫"，不同的对象有不同的表现——这就是多态。

```java
// 父类：动物
class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public void makeSound() {
        System.out.println(name + " 发出了声音");
    }
}

// 子类：狗
class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + "：汪汪！");
    }
}

// 子类：猫
class Cat extends Animal {
    public Cat(String name) {
        super(name);
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + "：喵喵！");
    }
}
```

```java
public class PolymorphismTest {
    public static void main(String[] args) {
        // 多态：父类引用指向子类对象
        Animal a1 = new Dog("旺财");
        Animal a2 = new Cat("咪咪");
        Animal a3 = new Animal("未知生物");
        
        // 同一个方法调用，不同的表现
        a1.makeSound();  // 汪汪！
        a2.makeSound();  // 喵喵！
        a3.makeSound();  // 发出了声音
        
        // 多态的威力：用统一的方式处理不同对象
        System.out.println("\n===== 动物园大合唱 =====");
        Animal[] zoo = {
            new Dog("大黄"),
            new Cat("小花"),
            new Dog("小黑"),
            new Cat("小白")
        };
        
        for (Animal animal : zoo) {
            animal.makeSound();  // 每个动物用自己的方式"叫"
        }
    }
}
```

**运行结果：**
```
旺财：汪汪！
咪咪：喵喵！
未知生物 发出了声音

===== 动物园大合唱 =====
大黄：汪汪！
小花：喵喵！
小黑：汪汪！
小白：喵喵！
```

!!! tip "多态的三个条件"
    1. **继承**：子类继承父类
    2. **重写**：子类重写父类方法
    3. **父类引用指向子类对象**：`Animal a = new Dog();`

---

## 8.3 抽象类：不能被实例化的"半成品"

有些类不应该被直接创建对象——比如"动物"太抽象了，应该创建"狗"或"猫"：

```java
// 抽象类：用 abstract 修饰
abstract class Shape {
    protected String color;
    
    public Shape(String color) {
        this.color = color;
    }
    
    // 抽象方法：没有方法体，子类必须实现
    public abstract double getArea();
    public abstract double getPerimeter();
    
    // 普通方法：有方法体，子类可以直接用
    public void describe() {
        System.out.println("这是一个" + color + "色的图形");
        System.out.println("面积: " + String.format("%.2f", getArea()));
        System.out.println("周长: " + String.format("%.2f", getPerimeter()));
    }
}

// 子类必须实现所有抽象方法
class Circle extends Shape {
    private double radius;
    
    public Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }
    
    @Override
    public double getArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public double getPerimeter() {
        return 2 * Math.PI * radius;
    }
}

class Rectangle extends Shape {
    private double width, height;
    
    public Rectangle(String color, double width, double height) {
        super(color);
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double getArea() {
        return width * height;
    }
    
    @Override
    public double getPerimeter() {
        return 2 * (width + height);
    }
}
```

```java
public class AbstractTest {
    public static void main(String[] args) {
        // Shape s = new Shape("红");  // 编译错误！抽象类不能实例化
        
        Shape circle = new Circle("红", 5);
        Shape rect = new Rectangle("蓝", 4, 6);
        
        circle.describe();
        System.out.println();
        rect.describe();
    }
}
```

**运行结果：**
```
这是一个红色的图形
面积: 78.54
周长: 31.42

这是一个蓝色的图形
面积: 24.00
周长: 20.00
```

---

## 8.4 接口：定义"能做什么"的契约

接口比抽象类更纯粹——它只定义"能做什么"，完全不关心"怎么做"：

```java
// 接口：定义能力
interface Flyable {
    void fly();  // 接口中的方法默认是 public abstract
}

interface Swimmable {
    void swim();
}

// 一个类可以实现多个接口
class Duck implements Flyable, Swimmable {
    private String name;
    
    public Duck(String name) {
        this.name = name;
    }
    
    @Override
    public void fly() {
        System.out.println(name + " 扑腾着翅膀飞起来了！");
    }
    
    @Override
    public void swim() {
        System.out.println(name + " 在水面上悠闲地游着...");
    }
}

class Fish implements Swimmable {
    private String name;
    
    public Fish(String name) {
        this.name = name;
    }
    
    @Override
    public void swim() {
        System.out.println(name + " 摆动着尾巴在水中穿梭...");
    }
}
```

```java
public class InterfaceTest {
    public static void main(String[] args) {
        Duck duck = new Duck("唐老鸭");
        Fish fish = new Fish("尼莫");
        
        // 鸭子既能飞又能游
        duck.fly();
        duck.swim();
        
        // 鱼只能游
        fish.swim();
        
        // 用接口类型引用对象
        System.out.println("\n===== 游泳比赛 =====");
        Swimmable[] contestants = {duck, fish};
        for (Swimmable c : contestants) {
            c.swim();
        }
    }
}
```

**运行结果：**
```
唐老鸭 扑腾着翅膀飞起来了！
唐老鸭 在水面上悠闲地游着...
尼莫 摆动着尾巴在水中穿梭...

===== 游泳比赛 =====
唐老鸭 在水面上悠闲地游着...
尼莫 摆动着尾巴在水中穿梭...
```

| 对比 | 抽象类 | 接口 |
|:---|:---|:---|
| 关键字 | `abstract class` | `interface` |
| 继承数量 | 只能继承 1 个 | 可以实现多个 |
| 构造方法 | 有 | 没有 |
| 成员变量 | 可以有 | 只能有常量 |
| 方法 | 可以有具体方法 | Java 8+ 可以有 default 方法 |
| 使用场景 | "是什么"（is-a） | "能做什么"（can-do） |

---

## 要点总结

- [x] `extends` 实现继承，子类获得父类的属性和方法
- [x] `super` 调用父类构造方法或方法
- [x] `@Override` 重写父类方法
- [x] 多态：父类引用指向子类对象，同一方法不同表现
- [x] 抽象类（`abstract`）：不能被实例化，定义模板
- [x] 接口（`interface`）：定义能力契约，一个类可实现多个接口

---

## 课后练习

1.  **形状体系** ：创建 `Shape` 抽象类和 `Circle`、`Rectangle`、`Triangle` 子类，实现面积和周长计算。

2.  **员工体系** ：创建 `Employee` 父类和 `Manager`、`Developer` 子类，重写 `work()` 方法展示多态。

3.  **接口练习** ：定义 `Chargeable`（可充电）接口，让 `Phone`、`Laptop`、`ElectricCar` 实现它。

---

**下一章预告：** 程序运行中难免出错——用户输入了字母而不是数字、文件不存在、网络断开。异常处理就是程序的"安全气囊"，让程序优雅地应对意外。

[继续第 9 章：异常处理 →](09-exceptions.md)