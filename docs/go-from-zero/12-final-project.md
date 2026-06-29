# 第 12 章：综合实战 —— 构建 RESTful API 服务

> **综合实战** —— 综合运用前 11 章的知识，从零构建一个完整的 RESTful API 服务：Todo List 应用

---

## 12.1 项目概述

本章将通过构建一个功能完整的 **Todo List API** 服务，将前 11 章所学的 Go 语言知识融会贯通。本项目涵盖以下核心技术点：

- 项目结构设计（go mod init、包划分）
- 数据模型定义（struct、JSON tags）
- 内存存储层（map + sync.RWMutex 并发安全）
- HTTP Handler 实现（net/http 路由分发）
- CRUD 操作（POST/GET/PUT/DELETE）
- JSON 请求解析与响应编码
- Middleware 模式（日志记录、请求 ID）
- 单元测试（net/http/httptest）
- 编译与交叉编译

### 12.1.1 项目目录结构

```
todo-api/
├── main.go              # 程序入口，路由注册，服务启动
├── go.mod               # Go module 定义
├── model/
│   └── todo.go          # 数据模型定义
├── store/
│   └── memory.go        # 内存存储实现
├── handler/
│   ├── todo.go          # HTTP Handler 实现
│   └── todo_test.go     # Handler 测试
└── Dockerfile           # 容器化部署配置（可选）
```

---

## 12.2 项目初始化

### 12.2.1 创建项目目录和 Module

```bash
# 创建项目目录结构
mkdir -p todo-api/model
mkdir -p todo-api/store
mkdir -p todo-api/handler

# 初始化 Go module
cd todo-api
go mod init todo-api
```

---

## 12.3 定义数据模型

`model/todo.go` —— 定义 Todo 项的数据结构：

```go
// model/todo.go
// 包 model 定义了 Todo 应用的数据模型。
// 所有的数据结构定义集中在此包中，便于维护和复用。
package model

// Status 表示 Todo 项的状态类型。
type Status string

const (
    StatusPending    Status = "pending"     // 待办
    StatusInProgress Status = "in_progress" // 进行中
    StatusCompleted  Status = "completed"   // 已完成
)

// Todo 表示一个待办事项。
// JSON tags 用于控制序列化和反序列化时的字段名。
type Todo struct {
    ID          int    `json:"id"`                     // 唯一标识符
    Title       string `json:"title"`                  // 标题
    Description string `json:"description,omitempty"`  // 描述（可选，为空时省略）
    Status      Status `json:"status"`                 // 状态
    CreatedAt   string `json:"created_at"`             // 创建时间（ISO 8601 格式）
    UpdatedAt   string `json:"updated_at"`             // 更新时间（ISO 8601 格式）
}

// CreateTodoRequest 创建 Todo 的请求体。
type CreateTodoRequest struct {
    Title       string `json:"title"`
    Description string `json:"description,omitempty"`
}

// UpdateTodoRequest 更新 Todo 的请求体。
// 使用指针类型表示可选字段：nil 表示不更新。
type UpdateTodoRequest struct {
    Title       *string `json:"title,omitempty"`
    Description *string `json:"description,omitempty"`
    Status      *Status `json:"status,omitempty"`
}
```

---

## 12.4 实现内存存储层

`store/memory.go` —— 使用 map 和 sync.RWMutex 实现线程安全的内存存储：

```go
// store/memory.go
// 包 store 提供了 Todo 数据的存储接口和内存实现。
package store

import (
    "fmt"
    "sort"
    "sync"
    "time"
    "todo-api/model"
)

// Store 定义了 Todo 存储的接口。
// 通过接口抽象，后续可以替换为数据库实现而不影响 handler 层。
type Store interface {
    GetAll() ([]model.Todo, error)
    GetByID(id int) (*model.Todo, error)
    Create(req model.CreateTodoRequest) (*model.Todo, error)
    Update(id int, req model.UpdateTodoRequest) (*model.Todo, error)
    Delete(id int) error
}

// MemoryStore 基于内存的 Todo 存储实现。
// 使用 sync.RWMutex 保证并发安全：读操作使用读锁，写操作使用写锁。
type MemoryStore struct {
    mu     sync.RWMutex
    data   map[int]model.Todo
    nextID int
}

// NewMemoryStore 创建并初始化一个新的 MemoryStore 实例。
func NewMemoryStore() *MemoryStore {
    return &MemoryStore{
        data:   make(map[int]model.Todo),
        nextID: 1,
    }
}

// GetAll 返回所有 Todo 项，按创建时间升序排列。
func (s *MemoryStore) GetAll() ([]model.Todo, error) {
    s.mu.RLock()         // 获取读锁：允许多个 goroutine 同时读取
    defer s.mu.RUnlock() // 函数返回时释放读锁

    // 将 map 中的值收集到切片中
    todos := make([]model.Todo, 0, len(s.data))
    for _, todo := range s.data {
        todos = append(todos, todo)
    }

    // 按 ID 排序：越早创建的 ID 越小
    sort.Slice(todos, func(i, j int) bool {
        return todos[i].ID < todos[j].ID
    })

    return todos, nil
}

// GetByID 根据 ID 获取单个 Todo 项。
// 当 ID 不存在时返回 error。
func (s *MemoryStore) GetByID(id int) (*model.Todo, error) {
    s.mu.RLock()
    defer s.mu.RUnlock()

    todo, ok := s.data[id]
    if !ok {
        return nil, fmt.Errorf("todo 项不存在：id=%d", id)
    }

    // 返回副本，避免外部修改内部状态
    return &todo, nil
}

// Create 创建一个新的 Todo 项。
func (s *MemoryStore) Create(req model.CreateTodoRequest) (*model.Todo, error) {
    s.mu.Lock()         // 获取写锁：独占访问
    defer s.mu.Unlock() // 函数返回时释放写锁

    now := time.Now().Format(time.RFC3339)

    todo := model.Todo{
        ID:          s.nextID,
        Title:       req.Title,
        Description: req.Description,
        Status:      model.StatusPending, // 新建 Todo 默认状态为 pending
        CreatedAt:   now,
        UpdatedAt:   now,
    }

    s.data[s.nextID] = todo
    s.nextID++

    return &todo, nil
}

// Update 更新指定 ID 的 Todo 项。
// 只更新请求体中非 nil 的字段（部分更新 / PATCH 语义）。
func (s *MemoryStore) Update(id int, req model.UpdateTodoRequest) (*model.Todo, error) {
    s.mu.Lock()
    defer s.mu.Unlock()

    todo, ok := s.data[id]
    if !ok {
        return nil, fmt.Errorf("todo 项不存在：id=%d", id)
    }

    // 部分更新：仅修改提供了值的字段
    if req.Title != nil {
        todo.Title = *req.Title
    }
    if req.Description != nil {
        todo.Description = *req.Description
    }
    if req.Status != nil {
        todo.Status = *req.Status
    }

    todo.UpdatedAt = time.Now().Format(time.RFC3339)
    s.data[id] = todo

    return &todo, nil
}

// Delete 删除指定 ID 的 Todo 项。
func (s *MemoryStore) Delete(id int) error {
    s.mu.Lock()
    defer s.mu.Unlock()

    if _, ok := s.data[id]; !ok {
        return fmt.Errorf("todo 项不存在：id=%d", id)
    }

    delete(s.data, id)
    return nil
}
```

---

## 12.5 实现 HTTP Handler

`handler/todo.go` —— 实现 Todo 相关的 HTTP 请求处理：

```go
// handler/todo.go
// 包 handler 实现了 HTTP 请求处理逻辑。
// 每个函数对应一个 API 端点。
package handler

import (
    "encoding/json"
    "log"
    "net/http"
    "strconv"
    "strings"
    "todo-api/model"
    "todo-api/store"
)

// TodoHandler 封装 Todo 相关的 HTTP 处理逻辑。
type TodoHandler struct {
    store store.Store // 通过接口依赖存储层，便于测试替换
}

// NewTodoHandler 创建新的 TodoHandler 实例。
func NewTodoHandler(s store.Store) *TodoHandler {
    return &TodoHandler{store: s}
}

// HandleTodos 处理 /api/todos 路径的请求。
// GET  ：获取所有 Todo 列表
// POST ：创建新的 Todo
func (h *TodoHandler) HandleTodos(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        h.listTodos(w, r)
    case http.MethodPost:
        h.createTodo(w, r)
    default:
        // 方法不允许：返回 405
        writeJSON(w, http.StatusMethodNotAllowed, map[string]string{
            "error": "方法不允许，仅支持 GET 和 POST",
        })
    }
}

// HandleTodo 处理 /api/todos/{id} 路径的请求。
// GET    ：获取指定 ID 的 Todo
// PUT    ：更新指定 ID 的 Todo
// DELETE ：删除指定 ID 的 Todo
func (h *TodoHandler) HandleTodo(w http.ResponseWriter, r *http.Request) {
    // 从 URL 路径中提取 ID
    id, err := extractID(r.URL.Path)
    if err != nil {
        writeJSON(w, http.StatusBadRequest, map[string]string{
            "error": err.Error(),
        })
        return
    }

    switch r.Method {
    case http.MethodGet:
        h.getTodo(w, r, id)
    case http.MethodPut:
        h.updateTodo(w, r, id)
    case http.MethodDelete:
        h.deleteTodo(w, r, id)
    default:
        writeJSON(w, http.StatusMethodNotAllowed, map[string]string{
            "error": "方法不允许，仅支持 GET、PUT 和 DELETE",
        })
    }
}

// listTodos 处理 GET /api/todos：返回所有 Todo 列表。
func (h *TodoHandler) listTodos(w http.ResponseWriter, r *http.Request) {
    todos, err := h.store.GetAll()
    if err != nil {
        writeJSON(w, http.StatusInternalServerError, map[string]string{
            "error": "获取 Todo 列表失败",
        })
        return
    }

    writeJSON(w, http.StatusOK, todos)
}

// createTodo 处理 POST /api/todos：创建新的 Todo。
func (h *TodoHandler) createTodo(w http.ResponseWriter, r *http.Request) {
    var req model.CreateTodoRequest

    // 解析请求体中的 JSON
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        writeJSON(w, http.StatusBadRequest, map[string]string{
            "error": "请求体格式错误：" + err.Error(),
        })
        return
    }

    // 验证必填字段
    if strings.TrimSpace(req.Title) == "" {
        writeJSON(w, http.StatusBadRequest, map[string]string{
            "error": "标题不能为空",
        })
        return
    }

    todo, err := h.store.Create(req)
    if err != nil {
        writeJSON(w, http.StatusInternalServerError, map[string]string{
            "error": "创建 Todo 失败：" + err.Error(),
        })
        return
    }

    // 201 Created：资源创建成功
    writeJSON(w, http.StatusCreated, todo)
}

// getTodo 处理 GET /api/todos/{id}：获取指定 Todo。
func (h *TodoHandler) getTodo(w http.ResponseWriter, r *http.Request, id int) {
    todo, err := h.store.GetByID(id)
    if err != nil {
        writeJSON(w, http.StatusNotFound, map[string]string{
            "error": err.Error(),
        })
        return
    }

    writeJSON(w, http.StatusOK, todo)
}

// updateTodo 处理 PUT /api/todos/{id}：更新指定 Todo。
func (h *TodoHandler) updateTodo(w http.ResponseWriter, r *http.Request, id int) {
    var req model.UpdateTodoRequest

    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        writeJSON(w, http.StatusBadRequest, map[string]string{
            "error": "请求体格式错误：" + err.Error(),
        })
        return
    }

    todo, err := h.store.Update(id, req)
    if err != nil {
        writeJSON(w, http.StatusNotFound, map[string]string{
            "error": err.Error(),
        })
        return
    }

    writeJSON(w, http.StatusOK, todo)
}

// deleteTodo 处理 DELETE /api/todos/{id}：删除指定 Todo。
func (h *TodoHandler) deleteTodo(w http.ResponseWriter, r *http.Request, id int) {
    err := h.store.Delete(id)
    if err != nil {
        writeJSON(w, http.StatusNotFound, map[string]string{
            "error": err.Error(),
        })
        return
    }

    writeJSON(w, http.StatusOK, map[string]string{
        "message": "删除成功",
    })
}

// ---- 辅助函数 ----

// writeJSON 将 data 编码为 JSON 并写入 HTTP 响应。
func writeJSON(w http.ResponseWriter, statusCode int, data any) {
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
    w.WriteHeader(statusCode)
    json.NewEncoder(w).Encode(data)
}

// extractID 从 URL 路径中提取末尾的数字 ID。
// 示例：/api/todos/42 → 42
func extractID(path string) (int, error) {
    parts := strings.Split(strings.TrimRight(path, "/"), "/")
    if len(parts) < 1 {
        return 0, nil
    }
    idStr := parts[len(parts)-1]
    id, err := strconv.Atoi(idStr)
    if err != nil {
        return 0, fmt.Errorf("无效的 ID：%s", idStr)
    }
    return id, nil
}
```

---

## 12.6 程序入口和中间件

`main.go` —— 程序入口，包含路由注册、中间件实现和服务启动：

```go
// main.go
// 包 main 是 Todo API 服务的程序入口。
package main

import (
    "context"
    "fmt"
    "log"
    "log/slog"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
    "todo-api/handler"
    "todo-api/store"
)

// requestIDKey 用于在 context 中存储请求 ID 的键类型。
// 使用自定义类型避免 context key 冲突。
type requestIDKey struct{}

// loggingMiddleware 日志记录中间件。
// 记录每个 HTTP 请求的方法、路径、状态码和耗时。
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // 使用 ResponseWriter 包装器以获取状态码
        wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

        // 执行下一个 handler
        next.ServeHTTP(wrapped, r)

        // 请求完成后记录日志
        duration := time.Since(start)
        slog.Info("HTTP 请求",
            "method", r.Method,
            "path", r.URL.Path,
            "status", wrapped.statusCode,
            "duration", duration.String(),
            "remote_addr", r.RemoteAddr,
        )
    })
}

// requestIDMiddleware 请求 ID 中间件。
// 为每个请求生成唯一的标识符，存储在 context 中。
func requestIDMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 从请求头获取请求 ID，如果没有则生成一个
        requestID := r.Header.Get("X-Request-ID")
        if requestID == "" {
            requestID = fmt.Sprintf("req-%d", time.Now().UnixNano())
        }

        // 将请求 ID 存储在 request context 中
        ctx := context.WithValue(r.Context(), requestIDKey{}, requestID)
        r = r.WithContext(ctx)

        // 设置响应头
        w.Header().Set("X-Request-ID", requestID)

        next.ServeHTTP(w, r)
    })
}

// recoveryMiddleware panic 恢复中间件。
// 捕获 handler 中的 panic，返回 500 错误而非让程序崩溃。
func recoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                slog.Error("handler panic 恢复", "error", rec)
                http.Error(w, `{"error":"服务器内部错误"}`, http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}

// responseWriter 包装 http.ResponseWriter，用于捕获状态码。
type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

// WriteHeader 捕获状态码并调用原始的 WriteHeader。
func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

func main() {
    // ---- 初始化依赖 ----
    todoStore := store.NewMemoryStore()
    todoHandler := handler.NewTodoHandler(todoStore)

    // ---- 注册路由 ----
    mux := http.NewServeMux()
    mux.HandleFunc("/api/todos", todoHandler.HandleTodos)
    mux.HandleFunc("/api/todos/", todoHandler.HandleTodo)

    // ---- 应用中间件 ----
    // 中间件按从外到内的顺序执行：
    // 请求进入：recovery → requestID → logging → handler
    // 响应返回：handler → logging → requestID → recovery
    var app http.Handler = mux
    app = loggingMiddleware(app)
    app = requestIDMiddleware(app)
    app = recoveryMiddleware(app)

    // ---- 配置和启动 HTTP 服务 ----
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    server := &http.Server{
        Addr:         ":" + port,
        Handler:      app,
        ReadTimeout:  10 * time.Second,  // 读取请求超时
        WriteTimeout: 15 * time.Second,  // 写入响应超时
        IdleTimeout:  60 * time.Second,  // 保持连接超时
    }

    // 在独立的 goroutine 中启动服务
    go func() {
        slog.Info("Todo API 服务启动", "addr", server.Addr)
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("服务启动失败：%v", err)
        }
    }()

    // ---- 优雅关闭 ----
    // 监听操作系统信号（Ctrl+C 或 SIGTERM）
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    slog.Info("正在关闭服务...")

    // 设置 30 秒的超时等待未完成的请求处理完成
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Fatalf("服务关闭失败：%v", err)
    }

    slog.Info("服务已安全关闭")
}
```

---

## 12.7 编写 Handler 测试

`handler/todo_test.go` —— 使用 `net/http/httptest` 编写测试：

```go
// handler/todo_test.go
// 包 handler_test 包含 TodoHandler 的测试用例。
// 使用外部测试包实现黑盒测试。
package handler_test

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    "todo-api/handler"
    "todo-api/model"
    "todo-api/store"
)

// setupTest 创建测试环境，返回 TodoHandler 和测试用的 HTTP Server。
func setupTest() *handler.TodoHandler {
    s := store.NewMemoryStore()
    return handler.NewTodoHandler(s)
}

// executeRequest 发送 HTTP 请求到 handler 并返回响应。
func executeRequest(h *handler.TodoHandler, method, path string, body any) *httptest.ResponseRecorder {
    var reqBody []byte
    if body != nil {
        reqBody, _ = json.Marshal(body)
    }

    req := httptest.NewRequest(method, path, bytes.NewReader(reqBody))
    req.Header.Set("Content-Type", "application/json")

    rr := httptest.NewRecorder()

    // 根据路径分发到对应的 handler
    if path == "/api/todos" {
        h.HandleTodos(rr, req)
    } else {
        h.HandleTodo(rr, req)
    }

    return rr
}

// TestCreateTodo 测试创建 Todo 的功能。
func TestCreateTodo(t *testing.T) {
    h := setupTest()

    // 测试创建成功
    t.Run("成功创建 Todo", func(t *testing.T) {
        body := model.CreateTodoRequest{
            Title:       "学习 Go 并发编程",
            Description: "完成第 10 章的练习",
        }

        rr := executeRequest(h, http.MethodPost, "/api/todos", body)
        if rr.Code != http.StatusCreated {
            t.Errorf("期望状态码 %d，得到 %d", http.StatusCreated, rr.Code)
        }

        var todo model.Todo
        if err := json.Unmarshal(rr.Body.Bytes(), &todo); err != nil {
            t.Fatalf("JSON 解析失败：%v", err)
        }

        if todo.Title != body.Title {
            t.Errorf("期望标题 %q，得到 %q", body.Title, todo.Title)
        }
        if todo.Status != model.StatusPending {
            t.Errorf("新创建的 Todo 状态应为 pending，得到 %q", todo.Status)
        }
        if todo.ID <= 0 {
            t.Errorf("ID 应大于 0，得到 %d", todo.ID)
        }
    })

    // 测试标题为空时创建失败
    t.Run("标题为空时返回 400", func(t *testing.T) {
        body := model.CreateTodoRequest{
            Title: "",
        }

        rr := executeRequest(h, http.MethodPost, "/api/todos", body)
        if rr.Code != http.StatusBadRequest {
            t.Errorf("期望状态码 %d，得到 %d", http.StatusBadRequest, rr.Code)
        }

        var resp map[string]string
        json.Unmarshal(rr.Body.Bytes(), &resp)
        if resp["error"] == "" {
            t.Error("期望返回错误消息")
        }
    })
}

// TestGetTodo 测试获取 Todo 的功能。
func TestGetTodo(t *testing.T) {
    h := setupTest()

    // 先创建一个 Todo
    createBody := model.CreateTodoRequest{Title: "测试获取"}
    createResp := executeRequest(h, http.MethodPost, "/api/todos", createBody)

    var created model.Todo
    json.Unmarshal(createResp.Body.Bytes(), &created)

    // 测试获取已存在的 Todo
    t.Run("获取已存在的 Todo", func(t *testing.T) {
        rr := executeRequest(h, http.MethodGet, "/api/todos/"+itoa(created.ID), nil)
        if rr.Code != http.StatusOK {
            t.Errorf("期望状态码 %d，得到 %d", http.StatusOK, rr.Code)
        }

        var todo model.Todo
        json.Unmarshal(rr.Body.Bytes(), &todo)

        if todo.ID != created.ID {
            t.Errorf("期望 ID %d，得到 %d", created.ID, todo.ID)
        }
    })

    // 测试获取不存在的 Todo
    t.Run("获取不存在的 Todo 返回 404", func(t *testing.T) {
        rr := executeRequest(h, http.MethodGet, "/api/todos/99999", nil)
        if rr.Code != http.StatusNotFound {
            t.Errorf("期望状态码 %d，得到 %d", http.StatusNotFound, rr.Code)
        }
    })
}

// TestUpdateTodo 测试更新 Todo 的功能。
func TestUpdateTodo(t *testing.T) {
    h := setupTest()

    // 创建测试数据
    createBody := model.CreateTodoRequest{Title: "需要更新"}
    createResp := executeRequest(h, http.MethodPost, "/api/todos", createBody)

    var created model.Todo
    json.Unmarshal(createResp.Body.Bytes(), &created)

    // 测试部分更新
    t.Run("部分更新 Todo", func(t *testing.T) {
        newTitle := "已更新标题"
        updateBody := model.UpdateTodoRequest{
            Title: &newTitle,
        }

        status := model.StatusCompleted
        updateBody.Status = &status

        rr := executeRequest(h, http.MethodPut, "/api/todos/"+itoa(created.ID), updateBody)
        if rr.Code != http.StatusOK {
            t.Errorf("期望状态码 %d，得到 %d", http.StatusOK, rr.Code)
        }

        var updated model.Todo
        json.Unmarshal(rr.Body.Bytes(), &updated)

        if updated.Title != newTitle {
            t.Errorf("期望标题 %q，得到 %q", newTitle, updated.Title)
        }
        if updated.Status != model.StatusCompleted {
            t.Errorf("期望状态 %q，得到 %q", model.StatusCompleted, updated.Status)
        }
    })
}

// TestDeleteTodo 测试删除 Todo 的功能。
func TestDeleteTodo(t *testing.T) {
    h := setupTest()

    // 创建测试数据
    createBody := model.CreateTodoRequest{Title: "需要删除"}
    createResp := executeRequest(h, http.MethodPost, "/api/todos", createBody)

    var created model.Todo
    json.Unmarshal(createResp.Body.Bytes(), &created)

    // 测试删除
    t.Run("删除存在的 Todo", func(t *testing.T) {
        rr := executeRequest(h, http.MethodDelete, "/api/todos/"+itoa(created.ID), nil)
        if rr.Code != http.StatusOK {
            t.Errorf("期望状态码 %d，得到 %d", http.StatusOK, rr.Code)
        }
    })

    // 验证删除后无法获取
    t.Run("删除后返回 404", func(t *testing.T) {
        rr := executeRequest(h, http.MethodGet, "/api/todos/"+itoa(created.ID), nil)
        if rr.Code != http.StatusNotFound {
            t.Errorf("期望状态码 %d，得到 %d", http.StatusNotFound, rr.Code)
        }
    })
}

// TestListTodos 测试获取 Todo 列表的功能。
func TestListTodos(t *testing.T) {
    h := setupTest()

    // 创建多个测试数据
    titles := []string{"任务 A", "任务 B", "任务 C"}
    for _, title := range titles {
        body := model.CreateTodoRequest{Title: title}
        executeRequest(h, http.MethodPost, "/api/todos", body)
    }

    // 获取列表
    rr := executeRequest(h, http.MethodGet, "/api/todos", nil)
    if rr.Code != http.StatusOK {
        t.Errorf("期望状态码 %d，得到 %d", http.StatusOK, rr.Code)
    }

    var todos []model.Todo
    json.Unmarshal(rr.Body.Bytes(), &todos)

    if len(todos) != len(titles) {
        t.Errorf("期望 %d 个 Todo，得到 %d", len(titles), len(todos))
    }
}

// itoa 是一个简单的整数转字符串辅助函数。
func itoa(n int) string {
    if n == 0 {
        return "0"
    }
    s := ""
    for n > 0 {
        s = string(rune('0'+n%10)) + s
        n /= 10
    }
    return s
}
```

---

## 12.8 编译与部署

### 12.8.1 常规编译

```bash
# 编译为当前平台的二进制文件
go build -o todo-api.exe .

# 运行
./todo-api.exe

# 测试 API 端点
curl http://localhost:8080/api/todos
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"学习 Go","description":"完成第 12 章"}'
```

### 12.8.2 交叉编译

Go 支持为不同平台编译二进制文件，通过环境变量 `GOOS` 和 `GOARCH` 控制：

```bash
# 为 Linux (amd64) 编译
GOOS=linux GOARCH=amd64 go build -o todo-api-linux .

# 为 macOS (arm64/M 系列芯片) 编译
GOOS=darwin GOARCH=arm64 go build -o todo-api-macos .

# 为 Windows (amd64) 编译
GOOS=windows GOARCH=amd64 go build -o todo-api.exe .
```

**常见的 GOOS/GOARCH 组合**：

| 目标平台 | GOOS | GOARCH |
|----------|------|--------|
| Linux (x86_64) | linux | amd64 |
| Linux (ARM64) | linux | arm64 |
| macOS (Intel) | darwin | amd64 |
| macOS (Apple Silicon) | darwin | arm64 |
| Windows (x86_64) | windows | amd64 |

### 12.8.3 Docker 部署（可选）

`Dockerfile`：

```dockerfile
# 构建阶段：使用 Go 官方镜像编译二进制文件
FROM golang:1.22-alpine AS builder

WORKDIR /app

# 先复制依赖文件，利用 Docker 层缓存
COPY go.mod go.sum ./
RUN go mod download

# 复制源码并编译
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/todo-api .

# 运行阶段：使用极小的 scratch 镜像
FROM scratch

WORKDIR /app

# 从构建阶段复制编译好的二进制文件
COPY --from=builder /app/todo-api .

# 暴露 API 端口
EXPOSE 8080

# 启动服务
CMD ["./todo-api"]
```

构建和运行 Docker 镜像：

```bash
# 构建 Docker 镜像
docker build -t todo-api .

# 运行容器
docker run -d -p 8080:8080 --name todo-api todo-api
```

---

## 12.9 测试和验证

### 12.9.1 运行单元测试

```bash
# 运行所有测试
go test -v ./...

# 运行测试并检查竞态条件
go test -race -v ./...

# 生成测试覆盖率报告
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
```

### 12.9.2 手动验证 API

启动服务后，可以通过 curl 或浏览器验证各端点：

```bash
# 1. 创建两个 Todo 项
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"学习 Go 语法","description":"完成前 6 章"}'

curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"练习并发编程"}'

# 2. 获取所有 Todo 列表
curl http://localhost:8080/api/todos

# 3. 获取单个 Todo（假设 ID 为 1）
curl http://localhost:8080/api/todos/1

# 4. 更新 Todo（标记为完成）
curl -X PUT http://localhost:8080/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# 5. 删除 Todo
curl -X DELETE http://localhost:8080/api/todos/2
```

### 12.9.3 API 端点总览

| 方法 | 路径 | 功能 | 状态码 |
|------|------|------|--------|
| GET | `/api/todos` | 获取所有 Todo | 200 |
| POST | `/api/todos` | 创建 Todo | 201 |
| GET | `/api/todos/{id}` | 获取单个 Todo | 200 / 404 |
| PUT | `/api/todos/{id}` | 更新 Todo | 200 / 404 |
| DELETE | `/api/todos/{id}` | 删除 Todo | 200 / 404 |

---

## 12.10 项目扩展方向

本章实现的 Todo API 是一个最小可行产品。以下是可以进一步探索的扩展方向：

1. **持久化存储**：替换 MemoryStore 为 SQLite 或 PostgreSQL 实现
2. **数据库 ORM**：使用 GORM 或 sqlx 简化数据库操作
3. **配置管理**：使用 Viper 库管理配置文件
4. **路由框架**：使用 Gin 或 Chi 替代标准库 mux
5. **认证授权**：添加 JWT Token 认证
6. **API 文档**：集成 Swagger/OpenAPI 文档生成
7. **日志聚合**：将结构化日志输出到集中式日志系统
8. **健康检查**：添加 `/health` 和 `/ready` 探活端点

---

## 12.11 本章小结

- 项目结构设计遵循 Go 标准布局，按职责划分包（model / store / handler）
- 数据模型使用 struct tag 控制 JSON 序列化行为
- 内存存储层通过接口抽象和 `sync.RWMutex` 实现并发安全
- HTTP Handler 使用标准库 `net/http` 实现 RESTful API
- Middleware 通过装饰器模式实现横切关注点的分离
- `net/http/httptest` 支持编写高质量的 handler 级别黑盒测试
- 交叉编译通过 `GOOS` / `GOARCH` 环境变量实现
- Docker 多阶段构建可以有效减小最终镜像体积

---

## 实践任务

1. 基于本章代码，为 Todo 模型添加 `Priority`（优先级：low / medium / high）和 `DueDate`（截止日期）字段，并更新 CRUD 的实现
2. 实现一个 `PaginationMiddleware`，支持 `?page=1&limit=10` 参数对 Todo 列表进行分页
3. 添加一个搜索端点 `GET /api/todos?q=keyword`，支持按标题和描述的关键字搜索
4. 将存储层替换为文件存储（JSON 文件持久化），实现 `FileStore` 并实现 `store.Store` 接口

---

👉 [返回教程首页 →](index.md)
