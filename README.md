# 📘 Fundamentals Vault

> **Go + Backend Engineering + System Design** — Tài liệu tổng hợp kiến thức nền tảng cho backend developer
>
> Phù hợp: Interview backend, Senior engineer, System design prep

[![Go 1.22+](https://img.shields.io/badge/Go-1.22+-00ADD8?style=flat-square&logo=go&logoColor=white)](https://go.dev)
[![52 Files](https://img.shields.io/badge/52-Files-2DC26B?style=flat-square)]
[![7 Modules](https://img.shields.io/badge/7-Modules-F9A826?style=flat-square)
[![License](https://img.shields.io/badge/License-CC--BY--NC-FF6B6B?style=flat-square)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## 🎯 Mục tiêu

Vault này tổng hợp kiến thức nền tảng cho quá trình:

- **Học Go** từ cơ bản đến chuyên sâu (Memory, Concurrency, Channel, Testing)
- **Ôn phỏng vấn** Backend / Senior Engineer
- **Chuẩn bị System Design** (Database, Caching, MQ, Scaling)
- **Hiểu sâu Infrastructure** (Security, Cryptography, Docker)

---

## 🗂️ Cấu trúc

```
Fundamentals/
│
├── 1 - Go/                      ← Ngôn ngữ Go, Memory, Concurrency (15 files)
├── 2 - Error Handling/          ← Error là value, Panic, Recover (3 files)
├── 3 - CS Fundamentals/         ← OOP, SOLID, Process, Thread, DSA (5 files)
├── 4 - Infrastructure/          ← VM, Container, Security, Cryptography (6 files)
├── 5 - Networking/              ← Socket, HTTP/2, gRPC (3 files)
├── 6 - Ecosystem/               ← Docker, Git, AI Tools, Go Embed (4 files)
└── 7 - System Design/          ← Database, Caching, MQ, Architecture (11 files)
                                   ─────────
                                   52 files
```

---

## 📚 Modules

### 1. 🧠 Go

> Ngôn ngữ Go: Data types, Memory, Concurrency, Channel, Testing, Build

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 1.1 | Data Types & Basics | Array, Slice, Struct, Interface |
| 1.2 | Control Flow & Functions | Defer, Closure, Pass by Value |
| 1.3 | Memory & Runtime | Stack, Heap, Escape Analysis, GC tri-color |
| 1.4 | Concurrency | Goroutine, Go Scheduler, Context switch |
| 1.5 | Channel & Select | Channel, Select, nil channel, errgroup |
| 1.6 | Concurrency Tools | Mutex, RWMutex, Once, Atomic, Context |
| 1.7 | Memory Model | Happens-before, synchronizes-with, race detector |
| 1.8 | Generics | Type parameters, constraints, generic types |
| 1.9 | Testing | Table tests, benchmarking, httptest, mocking |
| 1.10 | Build & Tooling | Build constraints, cross-compile, profiling |
| log-slog | Structured Logging | log/slog, JSON handler, HTTP middleware |
| std-Generic Algorithms | Generic Algorithms | slices, maps, cmp packages (Go 1.21+) |

---

### 2. 💥 Error Handling

> Error là value trong Go. Panic là trường hợp không thể khôi phục.

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 2.1 | Error is a Value | Go philosophy, return error |
| 2.2 | Custom Error | Sentinel, custom type, wrapping, errors.Join |
| 2.3 | Panic & Recover | Khi nào panic, cách recover |

---

### 3. 🧮 CS Fundamentals

> Computer Science: OOP, SOLID, Process, Thread, CAP Theorem, DSA

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 3.1 | OOP & SOLID | 4 pillars, 5 principles, struct embedding |
| 3.2 | Concurrency vs Parallelism | Rob Pike's definition |
| 3.3 | Process & Thread | Isolation, creation cost, shared memory |
| 3.4 | CAP Theorem | Consistency, Availability, Partition tolerance |
| 3.5 | DSA | Data Structures & Algorithms |

---

### 4. 🏗️ Infrastructure

> VM, Container, Security, Cryptography

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 4.1 | VM vs Container | Virtualization vs Containerization |
| 4.2 | Hash vs Encrypt | One-way vs reversible |
| 4.3 | Symmetric vs Asymmetric | AES, RSA, key exchange |
| 4.4 | TLS & HTTPS | Transport Layer Security |
| 4.5 | Password Storage | Bcrypt, Argon2, Salt |
| 4.6 | JWT & Signature | Token-based auth, digital signatures |

---

### 5. 🌐 Networking

> Socket, HTTP/2, gRPC

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 5.1 | Socket | TCP/UDP, connection model |
| 5.2 | HTTP/2 | Multiplexing, header compression, server push |
| 5.3 | gRPC | Remote Procedure Call, Protocol Buffers |

---

### 6. 🛠️ Ecosystem

> Docker, Git, AI Tools, Go Embed

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 6.1 | Docker | Container runtime, images, compose |
| 6.2 | Git | Version control, branching, workflows |
| 6.3 | AI | AI tools for developers |
| 6.4 | Go Embed | Compile-time file embedding, embed.FS |

---

### 7. 🗄️ System Design

> Database, Caching, Message Queue, Architecture, Scaling

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 7.1 | SQL vs NoSQL | Structured vs flexible schema |
| 7.2 | ACID vs BASE | Transaction consistency models |
| 7.3 | Transaction & Saga | Distributed transaction, Saga pattern |
| 7.4 | Database Index | B-Tree, trade-offs |
| 7.5 | Connection Pool | DB connection management |
| 7.6 | N+1 Query Problem | Performance issue & solutions |
| 7.7 | Caching | Layers, patterns, problems |
| 7.8 | Message Queue | RabbitMQ, Kafka, Idempotency |
| 7.9 | Retry Patterns | Immediate, Exponential, Jitter |
| 7.10 | Scaling | Vertical, Horizontal, Sharding |
| 7.11 | Monolithic vs Microservices | Architecture decisions |

---

## 🚀 Quick Start

1. Mở vault bằng **Obsidian**
2. Bắt đầu từ **1 - Go** hoặc **0 - Fundamentals**
3. Theo dõi roadmap: **1 - Go** → **7 - System Design**
4. Ôn tập với **flashcards / quiz** (sẽ cập nhật)

## 📖 Định dạng mỗi file

Mỗi file trong vault tuân theo cấu trúc:

```
# <Module> <Tiêu đề>

## <Section>
  - Khái niệm cốt lõi
  - Code examples (Go, SQL, ...)
  - So sánh / Bảng

## 📌 Tóm tắt
  ← Tree diagram tóm tắt

## Tags
#tag #tag
```

## 📝 License

<a rel="license" href="https://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="vertical-align:middle" src="https://licensebuttons.net/l/by-nc/4.0/88x31.png" /></a>

This vault is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

---

**Tags:** #go #backend #system-design #interview
