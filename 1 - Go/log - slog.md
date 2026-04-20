# log — Structured Logging (slog)

## Overview

`slog` (structured logging) được thêm vào **Go 1.21** standard library — thay thế `log` cho production logging.

> `log` = unstructured text → `slog` = structured key-value → production observability

---

## log vs slog

| | log | slog |
|---|---|---|
| Format | Plain text | Structured (key-value) |
| Output | `os.Stderr` only | Configurable handler |
| Log levels | ❌ No built-in levels | ✅ Debug/Info/Warn/Error |
| JSON output | ❌ Manual | ✅ Built-in JSON handler |
| Context | ❌ | ✅ `slog.FromContext(ctx)` |

```go
// log — unstructured
log.Printf("user %s logged in from %s", userID, ip)
// → "2024/01/01 10:00:00 user 123 logged in from 192.168.1.1"

// slog — structured
slog.Info("user logged in", "userID", userID, "ip", ip)
// → {"time":"2024-01-01T10:00:00Z","level":"INFO","msg":"user logged in","userID":"123","ip":"192.168.1.1"}
```

---

## Logger với Levels

### Tạo Logger

```go
import "log/slog"

// Text handler (mặc định, dễ đọc)
log := slog.New(slog.NewTextHandler(os.Stdout, nil))

// JSON handler (production standard)
jsonLog := slog.New(slog.NewJSONHandler(os.Stdout, nil))

// Set default global logger
slog.SetDefault(jsonLog)
```

### Log Levels

```go
slog.Debug("debug message", "key", "value")
slog.Info("info message", "count", 42)
slog.Warn("warning message", "latency", "200ms")
slog.Error("error message", "err", err)
```

### Cấu hình Level

```go
// Chỉ log Warn trở lên
handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelWarn,
})
logger := slog.New(handler)
logger.Info("this is ignored")    // NOT logged
logger.Warn("this is logged")    // logged
```

---

## Structured Attributes

### Basic types

```go
slog.Info("request completed",
    "status", 200,
    "latency_ms", 150,
    "bytes", 1024,
    "success", true,
)
```

### Nested Group

```go
slog.Info("user action",
    slog.Group("user",
        "id", "123",
        "name", "Alice",
        "role", "admin",
    ),
    "action", "login",
)
```

### Nested output (JSON)

```json
{"time":"...","level":"INFO","msg":"user action","user":{"id":"123","name":"Alice","role":"admin"},"action":"login"}
```

---

## Logger với Context

### Tạo logger từ context

```go
// Set logger vào context
ctx := slog.WithContext(context.Background(),
    slog.With("service", "auth"),
    slog.With("version", "1.0"),
)

// Inject vào request
func Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := slog.WithContext(r.Context(),
            slog.With("request_id", uuid.NewString()),
        )
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Dùng trong handler
func handler(w http.ResponseWriter, r *http.Request) {
    slog.Info("handling request", "path", r.URL.Path)
}
```

---

## HTTP Server với slog

```go
func main() {
    // JSON logger cho production
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

    server := &http.Server{
        Addr:         ":8080",
        Handler:      nil,
        ErrorLog:     slog.NewLogLogger(logger.Handler(), slog.LevelError),
    }

    // Hoặc dùng slog default
    slog.SetDefault(logger)

    // Log startup
    slog.Info("server starting", "addr", server.Addr)

    if err := server.ListenAndServe(); err != nil {
        slog.Error("server failed", "err", err)
    }
}
```

---

## Tích hợp với existing code

### Từ log → slog

```go
// Trước: dùng log
log.Printf("failed to connect: %v", err)

// Sau: dùng slog
slog.Error("failed to connect", "err", err)
```

### Wrap existing libraries

```go
import "log"

type logAdapter struct {
    logger *slog.Logger
}

func (l *logAdapter) Printf(format string, args ...any) {
    l.logger.Info(fmt.Sprintf(format, args...))
}

grpclog.SetLoggerV2(grpclog.NewLoggerV2WithLogger(l.logger))
```

---

## Common patterns

### Error logging với stack

```go
if err != nil {
    slog.Error("operation failed",
        "err", err,
        "operation", "db_query",
        "table", "users",
    )
}
```

### Request/Response logging (middleware)

```go
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        wrapped := &responseWriter{ResponseWriter: w, status: http.StatusOK}
        next.ServeHTTP(wrapped, r)

        slog.Info("http request",
            "method", r.Method,
            "path", r.URL.Path,
            "status", wrapped.status,
            "duration", time.Since(start),
        )
    })
}

type responseWriter struct {
    http.ResponseWriter
    status int
}

func (w *responseWriter) WriteHeader(code int) {
    w.status = code
    w.ResponseWriter.WriteHeader(code)
}
```

### Development vs Production

```go
// Development: text, debug level
// Production: JSON, info level

import "os"

var logger *slog.Logger

func init() {
    if os.Getenv("ENV") == "production" {
        logger = slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
            Level: slog.LevelInfo,
        }))
    } else {
        logger = slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
            Level: slog.LevelDebug,
        }))
    }
}
```

---

## vs other logging libraries

| Library | Notes |
|---------|-------|
| `slog` (Go 1.21+) | ✅ Standard library, production-ready |
| `log/slog` | Same thing — import path |
| `zerolog` | 3rd party, faster than slog, similar API |
| `zap` | Uber's logger, very fast, structured |
| `logrus` | Popular but slower, deprecated in favor of slog/zap |

> **Recommendation**: Dùng `slog` cho internal projects; `zap`/`zerolog` cho high-throughput services.

---

## 📌 Tóm tắt

```
log/slog (Go 1.21+)
│
├── vs log
│   ├── log: plain text, no levels
│   └── slog: structured key-value, log levels
│
├── Handlers
│   ├── NewTextHandler: development (human-readable)
│   ├── NewJSONHandler: production (machine-readable)
│   └── Custom: implement slog.Handler interface
│
├── Log Levels
│   ├── Debug < Info < Warn < Error
│   └── HandlerOptions.Level filter
│
├── Attributes
│   ├── Any type: slog.Info("msg", "key", value)
│   ├── slog.Group: nested structure
│   └── slog.With: add default attributes
│
└── Patterns
    ├── HTTP middleware logging
    ├── FromContext(ctx)
    ├── SetDefault(logger)
    └── Error with context
```

---

## Tags

#go #logging #slog #structured-logging #go-1.21