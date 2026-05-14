# 第 7 章：宏与 VBA 入门

> **从"手动重复"到"一键执行"——用宏和 VBA 解放你的双手**

每天重复同样的操作 50 次？录制一个宏，让 Excel 帮你做。本章从录制宏开始，逐步介绍 VBA 编程基础，帮你迈出自动化的第一步。

---

## 7.1 录制宏：零代码自动化

### 什么是宏？

**宏** 是一系列操作的录像。录制后，可以一键"回放"这些操作。

!!! example "实战：录制格式化报表的宏"
    1. 视图 → 宏 → 录制宏
    2. 宏名：FormatReport
    3. 快捷键：`Ctrl+Shift+F`
    4. 说明：格式化月度销售报表
    5. 点击"确定"开始录制
    6. 执行你要录制的操作：
       - 选中标题行 → 加粗、填充蓝色、白色字体
       - 选中数据区域 → 添加边框、设置数字格式
       - 自动调整列宽
    7. 视图 → 宏 → 停止录制

    此后选中任意报表，按 `Ctrl+Shift+F` 一键格式化。

### 宏的存储位置

| 存储位置 | 说明 | 适用场景 |
|:---|:---|:---|
| **当前工作簿** | 宏保存在当前文件中 | 仅当前文件使用 |
| **新工作簿** | 创建新文件保存宏 | 不常用 |
| **个人宏工作簿** | 保存在 PERSONAL.XLSB | 所有 Excel 文件都能使用 |

!!! tip "个人宏工作簿"
    将常用宏保存在"个人宏工作簿"中，它们会在 Excel 启动时自动加载，所有文件都能使用。PERSONAL.XLSB 位于 `%APPDATA%\Microsoft\Excel\XLSTART\`。

---

## 7.2 VBA 基础

### 打开 VBA 编辑器

`Alt+F11` 打开 VBA 编辑器。左侧是工程资源管理器，右侧是代码窗口。

### VBA 的基本语法

```vba
' 这是注释

' 变量声明
Dim name As String
Dim age As Integer
Dim amount As Double

' 赋值
name = "张三"
age = 30
amount = 12345.67

' 消息框
MsgBox "Hello, " & name

' 条件判断
If amount > 10000 Then
    MsgBox "大额交易"
ElseIf amount > 1000 Then
    MsgBox "普通交易"
Else
    MsgBox "小额交易"
End If

' 循环
For i = 1 To 10
    Cells(i, 1).Value = i
Next i
```

### 常用对象

| 对象 | 说明 | 示例 |
|:---|:---|:---|
| `Workbooks` | 工作簿集合 | `Workbooks("Book1.xlsx")` |
| `Worksheets` | 工作表集合 | `Worksheets("Sheet1")` |
| `Range` | 单元格区域 | `Range("A1:B10")` |
| `Cells` | 单个单元格 | `Cells(1, 1)` = A1 |
| `ActiveCell` | 当前选中单元格 | `ActiveCell.Value = 100` |
| `Selection` | 当前选中区域 | `Selection.Font.Bold = True` |

!!! example "实战：遍历工作表并重命名"
    ```vba
    Sub RenameSheets()
        Dim ws As Worksheet
        Dim i As Integer
        i = 1
        For Each ws In ThisWorkbook.Worksheets
            ws.Name = "第" & i & "季度"
            i = i + 1
        Next ws
    End Sub
    ```

---

## 7.3 常用 VBA 实战案例

### 批量处理文件

```vba
Sub ProcessAllFiles()
    Dim folderPath As String
    Dim fileName As String
    
    folderPath = "C:\Reports\"
    fileName = Dir(folderPath & "*.xlsx")
    
    Do While fileName <> ""
        Workbooks.Open folderPath & fileName
        ' 在这里添加处理逻辑
        ActiveWorkbook.Close SaveChanges:=True
        fileName = Dir()
    Loop
End Sub
```

### 自动发送邮件（需 Outlook）

```vba
Sub SendEmail()
    Dim OutApp As Object
    Dim OutMail As Object
    
    Set OutApp = CreateObject("Outlook.Application")
    Set OutMail = OutApp.CreateItem(0)
    
    With OutMail
        .To = "manager@company.com"
        .Subject = "每日销售报告"
        .Body = "请查收附件中的销售报告。"
        .Attachments.Add ActiveWorkbook.FullName
        .Send
    End With
End Sub
```

### 创建自定义函数

```vba
Function ChineseGrade(score As Double) As String
    Select Case score
        Case Is >= 90: ChineseGrade = "优秀"
        Case Is >= 80: ChineseGrade = "良好"
        Case Is >= 60: ChineseGrade = "及格"
        Case Else: ChineseGrade = "不及格"
    End Select
End Function
```

在 Excel 中直接使用：`=ChineseGrade(A1)`

!!! warning "VBA 安全提示"
    - 只运行来自可信来源的宏
    - 文件 → 选项 → 信任中心 → 宏设置 → 选择"禁用所有宏，并发出通知"
    - 不要启用来源不明的 .xlsm 文件中的宏

---

## 7.4 宏的调试与错误处理

### 调试技巧

| 技巧 | 快捷键 | 说明 |
|:---|:---|:---|
| 设置断点 | `F9` | 在代码行左侧点击 |
| 逐行执行 | `F8` | 逐步执行每行代码 |
| 快速执行 | `F5` | 运行到下一个断点 |
| 查看变量值 | 悬停 | 鼠标悬停在变量上 |
| 立即窗口 | `Ctrl+G` | 输入 `?变量名` 查看值 |

### 错误处理

```vba
Sub SafeOperation()
    On Error GoTo ErrorHandler
    
    ' 可能出错的操作
    Workbooks.Open "C:\data.xlsx"
    
    Exit Sub
    
ErrorHandler:
    MsgBox "错误：" & Err.Description
End Sub
```

---

## 要点总结

- [ ] 能录制宏来自动化重复操作
- [ ] 了解个人宏工作簿的用途
- [ ] 掌握 VBA 的基本语法（变量、条件、循环）
- [ ] 能使用 Range、Cells 等对象操作单元格
- [ ] 了解宏的安全设置和调试方法

---

## 课后练习

1. 录制一个宏：一键将选中区域格式化为"表样式中等深浅 2"
2. 编写一个 VBA 自定义函数，根据销售额返回提成比例（阶梯式）
3. 编写一个宏，遍历当前文件夹下所有 .xlsx 文件，在每个文件的 A1 单元格写入文件名

---

**下一章预告：** [第 8 章：综合实战项目](08-final-project.md) —— 从零搭建一个交互式销售数据分析仪表盘。