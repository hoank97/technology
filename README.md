# 📘 Fundamentals Vault

> **Go + Backend Engineering + System Design** — Tài liệu tổng hợp kiến thức nền tảng cho backend developer
>
> Phù hợp: Interview backend, Senior engineer, System design prep

[![Go 1.22+](https://img.shields.io/badge/Go-1.22+-00ADD8?style=flat-square&logo=go&logoColor=white)](https://go.dev)
[![52 Files](https://img.shields.io/badge/52-Files-2DC26B?style=flat-square)]
[![6 Modules](https://img.shields.io/badge/6-Modules-F9A826?style=flat-square)
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
├── 1 - Go/                      ← Ngôn ngữ Go, Memory, Concurrency, Error Handling (16 files)
├── 2 - CS Fundamentals/          ← OOP, SOLID, Process, Thread, CAP, DSA (5 files)
├── 3 - Infrastructure/          ← VM, Container, Security, Cryptography (7 files)
├── 4 - Networking/              ← Socket, HTTP/2, gRPC (3 files)
├── 5 - Ecosystem/               ← Docker, Git, AI Tools, Go Embed (4 files)
└── 6 - System Design/          ← Database, Caching, MQ, Architecture (11 files)
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
| 1.11 | Error Handling | Error is a value, Custom error, Panic & Recover |
| log-slog | Structured Logging | log/slog, JSON handler, HTTP middleware |
| std-Generic Algorithms | Generic Algorithms | slices, maps, cmp packages (Go 1.21+) |

---

### 2. 🧮 CS Fundamentals

> Computer Science: OOP, SOLID, Process, Thread, CAP Theorem, DSA

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 2.1 | OOP & SOLID | 4 pillars, 5 principles, struct embedding |
| 2.2 | Concurrency vs Parallelism | Rob Pike's definition |
| 2.3 | Process & Thread | Isolation, creation cost, shared memory |
| 2.4 | CAP Theorem | Consistency, Availability, Partition tolerance |
| 2.5 | DSA | Data Structures & Algorithms |

---

### 3. 🏗️ Infrastructure

> VM, Container, Security, Cryptography

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 3.1 | VM vs Container | Virtualization vs Containerization |
| 3.2 | Hash vs Encrypt | One-way vs reversible |
| 3.3 | Symmetric vs Asymmetric | AES, RSA, key exchange |
| 3.4 | TLS & HTTPS | Transport Layer Security |
| 3.5 | Password Storage | Bcrypt, Argon2, Salt |
| 3.6 | JWT & Signature | Token-based auth, digital signatures |

---

### 4. 🌐 Networking

> Socket, HTTP/2, gRPC

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 4.1 | Socket | TCP/UDP, connection model |
| 4.2 | HTTP/2 | Multiplexing, header compression, server push |
| 4.3 | gRPC | Remote Procedure Call, Protocol Buffers |

---

### 5. 🛠️ Ecosystem

> Docker, Git, AI Tools, Go Embed

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 5.1 | Docker | Container runtime, images, compose |
| 5.2 | Git | Version control, branching, workflows |
| 5.3 | AI | AI tools for developers |
| 5.4 | Go Embed | Compile-time file embedding, embed.FS |

---

### 6. 🗄️ System Design

> Database, Caching, Message Queue, Architecture, Scaling

| # | Chủ đề | Mô tả |
|---|---------|--------|
| 6.1 | SQL vs NoSQL | Structured vs flexible schema |
| 6.2 | ACID vs BASE | Transaction consistency models |
| 6.3 | Transaction & Saga | Distributed transaction, Saga pattern |
| 6.4 | Database Index | B-Tree, trade-offs |
| 6.5 | Connection Pool | DB connection management |
| 6.6 | N+1 Query Problem | Performance issue & solutions |
| 6.7 | Caching | Layers, patterns, problems |
| 6.8 | Message Queue | RabbitMQ, Kafka, Idempotency |
| 6.9 | Retry Patterns | Immediate, Exponential, Jitter |
| 6.10 | Scaling | Vertical, Horizontal, Sharding |
| 6.11 | Monolithic vs Microservices | Architecture decisions |

---

## 🚀 Quick Start

1. Mở vault bằng **Obsidian**
2. Bắt đầu từ **1 - Go** hoặc **0 - Fundamentals**
3. Theo dõi roadmap: **1 - Go** → **6 - System Design**
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
