# 第 1 章：认识 Java —— 从"你好，世界"开始

> **场景：** 你决定学习编程，选择了 Java 作为第一门语言。就像学开车前要先了解方向盘和油门，学 Java 前需要先搭建开发环境，并运行你的第一个程序——让电脑对你说"你好，世界"。

---

## 1.1 Java 是什么？

!!! example "核心比喻：Java 就像一家跨国餐厅"
    想象你开了一家餐厅。你写了一份菜谱（Java 源代码），这份菜谱不是直接给厨师看的，而是先翻译成一套"国际标准烹饪指令"（字节码）。然后，无论你的餐厅开在纽约、东京还是巴黎，只要厨房里有一台"标准烹饪机"（JVM），就能按照这套指令做出同样的菜。
    
    - **菜谱** = Java 源代码（`.java` 文件）
    - **国际标准烹饪指令** = 字节码（`.class` 文件）
    - **标准烹饪机** = JVM（Java Virtual Machine，Java 虚拟机）
    
    这就是 Java 的核心理念：**Write Once, Run Anywhere（一次编写，到处运行）**。

Java 由 Sun Microsystems 公司（后被 Oracle 收购）于 1995 年发布，由 James Gosling 领导开发。经过近 30 年的发展，Java 已成为企业级应用开发的首选语言之一。

| 特性 | 说明 |
|:---|:---|
| **跨平台** | 编译成字节码，在任何装有 JVM 的设备上运行 |
| **面向对象** | 一切皆对象，支持封装、继承、多态 |
| **强类型** | 变量必须先声明类型，编译时检查类型错误 |
| **自动内存管理** | 垃圾回收器（GC）自动回收不再使用的内存 |
| **丰富的类库** | 官方提供数千个标准类，覆盖网络、IO、数据库等 |

---

## 1.2 安装 Java 开发环境

### 1.2.1 安装 JDK

JDK（Java Development Kit）是 Java 开发工具包，包含编译器和运行时环境。

**步骤 1：下载 JDK**

打开浏览器，访问 [Oracle JDK 下载页面](https://www.oracle.com/java/technologies/downloads/) 或使用开源的 [OpenJDK](https://adoptium.net/)。

选择适合你操作系统的版本（推荐 JDK 17 或 JDK 21，这是长期支持版本 LTS）。

**步骤 2：安装 JDK**

=== "Windows"

    1. 双击下载的 `.msi` 或 `.exe` 安装包
    2. 一路点击"下一步"，记住安装路径（默认：`C:\Program Files\Java\jdk-17`）
    3. 安装完成后，打开 **命令提示符**（按 `Win + R`，输入 `cmd`，回车）
    4. 输入以下命令验证安装：

    ```cmd
    java -version
    javac -version
    ```

=== "macOS"

    1. 双击下载的 `.dmg` 文件，按提示安装
    2. 打开 **终端**（在"启动台 → 其他"中找到）
    3. 输入以下命令验证安装：

    ```bash
    java -version
    javac -version
    ```

=== "Linux"

    1. 打开终端，使用包管理器安装：

    ```bash
    # Ubuntu/Debian
    sudo apt update
    sudo apt install openjdk-17-jdk

    # Fedora
    sudo dnf install java-17-openjdk-devel
    ```

    2. 验证安装：

    ```bash
    java -version
    javac -version
    ```

**预期输出：**
```
java version "17.0.9" 2023-10-17 LTS
Java(TM) SE Runtime Environment (build 17.0.9+11-LTS-201)
Java HotSpot(TM) 64-Bit Server VM (build 17.0.9+11-LTS-201, mixed mode, sharing)

javac 17.0.9
```

!!! warning "常见问题"
    - 如果提示 `'java' 不是内部或外部命令`，说明系统找不到 Java。需要配置环境变量 `JAVA_HOME`，指向 JDK 安装目录，并将 `%JAVA_HOME%\bin` 添加到 `PATH` 中。
    - 如果版本号不是 17 或更高，建议升级到 JDK 17+。

---

## 1.3 你的第一个 Java 程序

### 1.3.1 编写源代码

用任意文本编辑器（记事本、VS Code、Notepad++ 等）创建一个新文件，命名为 `HelloWorld.java`，输入以下内容：

```java
/**
 * HelloWorld.java —— 我的第一个 Java 程序
 * 
 * 这个程序会在屏幕上打印"你好，世界！"
 */
public class HelloWorld {
    public static void main(String[] args) {
        // 向世界问好
        System.out.println("你好，世界！");
        System.out.println("这是我的第一个 Java 程序。");
    }
}
```

!!! info "代码逐行解释"
    | 代码 | 含义 |
    |:---|:---|
    | `public class HelloWorld` | 定义一个名为 `HelloWorld` 的公共类。**文件名必须与类名完全一致**（包括大小写） |
    | `public static void main(String[] args)` | 程序的入口方法。Java 程序从这里开始执行 |
    | `System.out.println(...)` | 向控制台打印一行文字，并在末尾自动换行 |
    | `// 向世界问好` | 单行注释，编译器会忽略，给人看的说明文字 |
    | `/** ... */` | 文档注释，用于生成 API 文档 |

### 1.3.2 编译源代码

打开终端（命令提示符），进入 `HelloWorld.java` 所在的目录，执行编译命令：

```cmd
javac HelloWorld.java
```

如果没有任何输出，说明编译成功。此时目录下会多出一个 `HelloWorld.class` 文件——这就是编译后的字节码。

!!! tip "编译过程"
    ```
    HelloWorld.java  ──javac编译──▶  HelloWorld.class
       （源代码）                      （字节码）
    ```

### 1.3.3 运行程序

```cmd
java HelloWorld
```

!!! warning "注意"
    运行命令是 `java HelloWorld`，**不要加 `.class` 后缀**！

**预期输出：**
```
你好，世界！
这是我的第一个 Java 程序。
```

---

## 1.4 Java 程序的基本结构

每个 Java 程序都遵循固定的结构。让我们解剖一下 `HelloWorld.java`：

```java
// 1. 类声明
public class HelloWorld {
    
    // 2. 主方法（程序入口）
    public static void main(String[] args) {
        
        // 3. 语句（程序要执行的指令）
        System.out.println("你好，世界！");
    }
}
```

| 组成部分 | 说明 |
|:---|:---|
| **类（Class）** | Java 程序的基本组织单元。所有代码都必须写在类里面 |
| **主方法（main）** | 程序的入口点。`public static void main(String[] args)` 是固定写法 |
| **语句（Statement）** | 程序要执行的具体指令，每条语句以分号 `;` 结尾 |
| **注释（Comment）** | 给人看的说明，编译器忽略。`//` 单行，`/* */` 多行 |

!!! note "为什么 main 方法这么长？"
    初学时不需要完全理解 `public static void main(String[] args)` 每个词的含义。你可以把它当作一个"咒语"——只要记住这个固定写法，程序就能运行。随着后续章节的学习，你会逐渐理解每个关键字的意义。

---

## 1.5 使用 IDE（集成开发环境）

虽然用记事本 + 命令行可以写 Java，但专业开发都使用 IDE。推荐以下两款：

| IDE | 特点 | 适合人群 |
|:---|:---|:---|
| **IntelliJ IDEA** | 功能最强大，智能提示一流 | 专业开发者（社区版免费） |
| **VS Code + 扩展** | 轻量灵活，多语言支持 | 喜欢轻量工具的学习者 |

!!! tip "推荐选择"
    对于初学者，推荐使用 **IntelliJ IDEA Community Edition**（免费）。它内置了代码补全、错误提示、一键运行等功能，能大幅降低学习门槛。

**IntelliJ IDEA 快速上手：**

1. 下载并安装 [IntelliJ IDEA Community Edition](https://www.jetbrains.com/idea/download/)
2. 打开 IDEA，选择 `New Project` → 设置项目名称和位置 → `Create`
3. 在 `src` 文件夹上右键 → `New` → `Java Class` → 输入 `HelloWorld`
4. 输入 `main` 然后按 `Tab` 键，IDEA 会自动生成 main 方法
5. 输入 `sout` 然后按 `Tab` 键，IDEA 会自动生成 `System.out.println()`
6. 点击行号旁边的绿色三角 ▶ 运行程序

---

## 要点总结

- [x] Java 通过 JVM 实现"一次编写，到处运行"
- [x] JDK 包含编译器（javac）和运行时（java）
- [x] 源代码（`.java`）→ 编译（`javac`）→ 字节码（`.class`）→ 运行（`java`）
- [x] 每个 Java 程序必须有一个 `main` 方法作为入口
- [x] 类名必须与文件名一致（包括大小写）
- [x] 每条语句以分号 `;` 结尾
- [x] IDE 可以大幅提高开发效率

---

## 课后练习

1.  **修改问候语** ：修改 `HelloWorld.java`，让它打印你的名字和今天的日期。

2.  **多行输出** ：编写程序，用 `System.out.println()` 打印一首你喜欢的诗（至少 4 行）。

3.  **探索 IDE** ：在 IntelliJ IDEA 中创建一个新项目，尝试使用代码补全功能（输入 `sout` + Tab）。

---

**下一章预告：** 现在你知道了如何让 Java 程序"说话"。第 2 章将学习如何让程序"记住"信息——变量与数据类型，就像给数据分配不同大小的储物柜。

[继续第 2 章：变量与数据类型 →](02-variables-and-types.md)