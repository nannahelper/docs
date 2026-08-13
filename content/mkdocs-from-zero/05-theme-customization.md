# 第 5 章：主题定制

> **打造独一无二的品牌形象** —— 自定义 Material 主题的配色、字体、Logo 和样式，让文档站点脱颖而出。

---

## 5.1 设置网站图标和 Logo

### Favicon（浏览器标签页图标）

将你的图标文件（推荐 `favicon.png` 或 `favicon.ico`）放入 `docs/assets/` 目录，然后在 `mkdocs.yml` 中配置：

```yaml
theme:
  name: material
  favicon: assets/favicon.png
```

### Logo（导航栏图标）

```yaml
theme:
  name: material
  logo: assets/logo.png
```

!!! tip "图标尺寸建议"

    - **favicon**：32×32 或 64×64 像素
    - **logo**：高度约 40~60 像素，宽度不限
    - 推荐使用 PNG 格式（支持透明背景）

---

## 5.2 自定义配色

除了使用预设的主题色，你还可以通过自定义 CSS 变量实现更精细的颜色控制：

```yaml
theme:
  name: material
  palette:
    - scheme: default
      primary: custom        # 使用自定义颜色
      accent: custom
```

然后在 `docs/assets/` 下创建 `extra.css`：

```css
/* docs/assets/extra.css */

/* 自定义主色调 */
[data-md-color-primary="custom"] {
  --md-primary-fg-color:        #2E7D32;   /* 主色 */
  --md-primary-fg-color--light: #66BB6A;   /* 浅色变体 */
  --md-primary-fg-color--dark:  #1B5E20;   /* 深色变体 */
}

/* 自定义强调色 */
[data-md-color-accent="custom"] {
  --md-accent-fg-color:         #FF6F00;
}
```

然后在 `mkdocs.yml` 中引入这个 CSS 文件：

```yaml
extra_css:
  - assets/extra.css
```

---

## 5.3 自定义字体

### 使用 Google Fonts

```yaml
theme:
  name: material
  font:
    text: Noto Sans SC      # 正文字体（支持中文）
    code: JetBrains Mono     # 代码字体
```

**渲染效果：** `text` 控制正文和标题的字体，`code` 控制代码块的字体。`Noto Sans SC` 是 Google 推出的开源中文字体，渲染清晰美观。`JetBrains Mono` 是专为编程设计的等宽字体，支持连字（ligatures）。

!!! info "推荐的中文字体组合"

    | 用途 | 推荐字体 | 特点 |
    |:---|:---|:---|
    | 正文 | `Noto Sans SC` | 开源、多字重、屏幕阅读舒适 |
    | 代码 | `JetBrains Mono` | 连字支持、字符区分度高 |
    | 代码备选 | `Fira Code` | 同样支持连字，风格更圆润 |

---

## 5.4 添加页脚信息

### 版权声明

```yaml
copyright: Copyright &copy; 2026 你的名字
```

### 社交链接

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/你的用户名
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/你的用户名
```

这些图标会显示在页脚或导航栏中，使用 Font Awesome 图标库。

---

## 5.5 自定义公告栏

Material 主题支持在页面顶部显示公告栏：

```yaml
extra:
  announcement:
    content: |
      🎉 <strong>新版本 v2.0 已发布！</strong> 
      <a href="/changelog/">查看更新日志</a>
    dismissable: true        # 允许用户关闭
```

---

## 5.6 启用插件增强功能

MkDocs 的插件系统可以扩展站点功能。以下是最常用的几个插件：

### 搜索插件（内置）

```yaml
plugins:
  - search:
      lang: zh              # 中文分词支持
      separator: '[\s\-,:!=\[\]()"/]+'   # 分词分隔符
```

### Git 修订日期插件

显示每个页面的最后修改时间：

```bash
pip install mkdocs-git-revision-date-localized-plugin
```

```yaml
plugins:
  - git-revision-date-localized:
      enable_creation_date: true
      type: datetime
```

### 网站统计插件（Google Analytics）

```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX   # 你的 Google Analytics 测量 ID
```

---

## 5.7 实战：完整的自定义配置

将以下内容整合到你的 `mkdocs.yml` 中：

```yaml
# 站点信息
site_name: 我的文档站点
site_description: 专业的技术文档中心

# 主题配置
theme:
  name: material
  language: zh
  logo: assets/logo.png
  favicon: assets/favicon.png
  font:
    text: Noto Sans SC
    code: JetBrains Mono
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/brightness-7
        name: 切换至深色模式
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/brightness-4
        name: 切换至浅色模式
  features:
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

# 自定义样式
extra_css:
  - assets/extra.css

# 页脚
copyright: Copyright &copy; 2026 你的名字

# 社交链接
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/你的用户名
```

---

## 本章要点总结

- [ ] 了解如何设置 favicon 和 logo
- [ ] 能通过 CSS 变量自定义主题配色
- [ ] 能配置 Google Fonts 中英文字体
- [ ] 了解页脚版权和社交链接的配置方法
- [ ] 了解公告栏和常用插件的配置
- [ ] 完成了一份包含自定义样式的完整配置

---

👉 [进入第 6 章：部署上线 →](06-deployment.md)