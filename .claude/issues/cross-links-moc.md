# 🐛 Issue #6 — Thiếu Cross-links Giữa Content Files

> Audit date: 2026-04-21
> Priority: 🟡 Medium-High — Ảnh hưởng đến giá trị cốt lõi của Obsidian (Graph View, knowledge network)

---

## Mô Tả

Hiện tại tất cả `[[wikilinks]]` trong vault chỉ tồn tại ở **index files** (top-down links từ MOC → children). **Không có** cross-links ngang giữa các content files với nhau.

Graph View hiện tại = cây thuần túy (tree), không phải mạng kiến thức (knowledge graph):

```
[1-Go]
  ├── [01 - Language Basics] ──→ [01.1] ──→ (điểm chết)
  ├── [02 - Memory]          ──→ [02.1] ──→ (điểm chết)
  ├── [03 - Concurrency]     ──→ [03.1] ──→ (điểm chết)
  │                          ──→ [03.2] ──→ (điểm chết)
  │                          ──→ [03.3] ──→ (điểm chết)
  └── ...
```

**Graph lý tưởng:**

```
[01.1] ─── liên quan ──→ [02.1 Memory & Runtime]
[03.1 Goroutine]  ──────→ [02.1 Stack Growth]
[03.1 Goroutine]  ──────→ [02.2 Memory Model]
[03.3 sync.Pool]  ──────→ [02.1 GC & sync.Pool]
[04.1 Error]      ──────→ [04.2 Custom Error]
[03.2 Channel]    ──────→ [03.3 Context]
[05.1 Generics]   ──────→ [01.1 Interface]
```

---

## Cross-links Cần Thêm

### `01 - Language Basics` nhóm

#### `01.1 - Data Types & Basics.md`

- [ ] Thêm link đến `[[01.2 - Control Flow & Functions]]` — section về Closure liên quan đến capturing variables
- [ ] Thêm link đến `[[05.1 - Generics]]` — Interface internals liên quan đến generic constraints
- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — section về Escape Analysis (Interface boxing)

#### `01.2 - Control Flow & Functions.md`

- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — Defer open-coded optimization liên quan đến Stack
- [ ] Thêm link đến `[[04.3 - Panic & Recover]]` — Defer + recover pattern
- [ ] Thêm link đến `[[03.1 - Goroutine & Scheduler]]` — init() execution và goroutine startup

---

### `02 - Memory & Runtime` nhóm

#### `02.1 - Memory & Runtime.md`

- [ ] Thêm link đến `[[03.1 - Goroutine & Scheduler]]` — Stack growth liên quan đến goroutine stack
- [ ] Thêm link đến `[[03.3 - Concurrency Tools]]` — sync.Pool section overlap
- [ ] Thêm link đến `[[07.2 - Build & Tooling]]` — pprof profiling cho memory

#### `02.2 - Memory Model.md`

- [ ] Thêm link đến `[[03.2 - Channel & Select]]` — Channel là synchronization point
- [ ] Thêm link đến `[[03.3 - Concurrency Tools]]` — Mutex, Atomic là sync points
- [ ] Thêm link đến `[[03.1 - Goroutine & Scheduler]]` — Goroutine creation as sync point

---

### `03 - Concurrency` nhóm

#### `03.1 - Goroutine & Scheduler.md`

- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — Stack growth section
- [ ] Thêm link đến `[[02.2 - Memory Model]]` — Happens-before với goroutine creation
- [ ] Thêm link đến `[[03.2 - Channel & Select]]` — gopark triggered by channel ops
- [ ] Thêm link đến `[[03.3 - Concurrency Tools]]` — gopark triggered by mutex

#### `03.2 - Channel & Select.md`

- [ ] Thêm link đến `[[02.2 - Memory Model]]` — Channel là synchronization point / happens-before
- [ ] Thêm link đến `[[03.3 - Concurrency Tools]]` — done channel vs context.Context
- [ ] Thêm link đến `[[03.1 - Goroutine & Scheduler]]` — goroutine leak prevention

#### `03.3 - Concurrency Tools.md`

- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — sync.Pool giảm GC pressure
- [ ] Thêm link đến `[[02.2 - Memory Model]]` — Atomic as memory barrier, Mutex happens-before
- [ ] Thêm link đến `[[03.2 - Channel & Select]]` — Context cancellation flow

---

### `04 - Error Handling` nhóm

#### `04.1 - Error is a Value.md`

- [ ] Thêm link đến `[[04.2 - Custom Error]]` — Sentinel vs Custom Error types
- [ ] Thêm link đến `[[04.3 - Panic & Recover]]` — khi nào dùng panic thay error

#### `04.2 - Custom Error.md`

- [ ] Thêm link đến `[[04.1 - Error is a Value]]` — error interface internals
- [ ] Thêm link đến `[[04.3 - Panic & Recover]]` — Must pattern dùng panic

#### `04.3 - Panic & Recover.md`

- [ ] Thêm link đến `[[03.1 - Goroutine & Scheduler]]` — recover() trong goroutine
- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — defer execution liên quan stack

---

### `05 - Generics` nhóm

#### `05.1 - Generics.md`

- [ ] Thêm link đến `[[01.1 - Data Types & Basics]]` — Interface vs Generics comparison
- [ ] Thêm link đến `[[05.2 - Generic Algorithms (std)]]` — Xem standard library implementations
- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — GCShape stenciling liên quan đến memory layout

#### `05.2 - Generic Algorithms (std).md`

- [ ] Thêm link đến `[[05.1 - Generics]]` — Constraints và type parameters
- [ ] Thêm link đến `[[07.1 - Testing]]` — slices.SortFunc dùng trong benchmark tests

---

### `06 - Standard Library` nhóm

#### `06.1 - Structured Logging (slog).md`

- [ ] Thêm link đến `[[03.3 - Concurrency Tools]]` — slog dùng sync.Pool nội bộ
- [ ] Thêm link đến `[[07.2 - Build & Tooling]]` — production build config (ENV, log level)
- [ ] Thêm link đến `[[04.1 - Error is a Value]]` — error logging patterns

---

### `07 - Testing & Tooling` nhóm

#### `07.1 - Testing.md`

- [ ] Thêm link đến `[[07.2 - Build & Tooling]]` — build tags cho integration tests
- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — benchmark + memory profiling
- [ ] Thêm link đến `[[03.1 - Goroutine & Scheduler]]` — goroutine leak trong tests

#### `07.2 - Build & Tooling.md`

- [ ] Thêm link đến `[[02.1 - Memory & Runtime]]` — pprof profiling sections
- [ ] Thêm link đến `[[03.1 - Goroutine & Scheduler]]` — GOMAXPROCS tuning
- [ ] Thêm link đến `[[07.1 - Testing]]` — test + coverage commands

---

## Hướng Dẫn Thêm Cross-link

Cross-link nên được thêm **tự nhiên trong câu văn**, không phải dưới dạng danh sách rời:

```markdown
<!-- ✅ Tự nhiên, hữu ích -->
Goroutine sử dụng **dynamic stack** — xem [[02.1 - Memory & Runtime#Stack Growth]].
Pattern này liên quan đến [[02.2 - Memory Model#Goroutine Creation Synchronization]].

<!-- ❌ Liệt kê gượng ép -->
Xem thêm: [[02.1]], [[02.2]], [[03.3]]
```

Dùng **section anchor** khi có thể:
```markdown
[[02.1 - Memory & Runtime#sync.Pool — GC pressure reduction]]
[[03.3 - Concurrency Tools#Sync Primitive Decision Guide]]
```

---

## Tracking

- [ ] Nhóm 01 - Language Basics (5 links)
- [ ] Nhóm 02 - Memory & Runtime (6 links)
- [ ] Nhóm 03 - Concurrency (10 links)
- [ ] Nhóm 04 - Error Handling (6 links)
- [ ] Nhóm 05 - Generics (5 links)
- [ ] Nhóm 06 - Standard Library (3 links)
- [ ] Nhóm 07 - Testing & Tooling (6 links)

**Tổng**: ~41 cross-links cần thêm

> - [x] **[RESOLVED]** ~30 cross-links đã được thêm vào các content files
