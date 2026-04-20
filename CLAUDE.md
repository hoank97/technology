# CLAUDE.md — AI Collaboration Guide

> Tài liệu này hướng dẫn Claude (và các AI assistant khác) về bối cảnh, quy ước, và nguyên tắc khi làm việc với repo **Fundamentals Vault**.

---

## 🗺️ Tổng Quan Repo

### Mục đích

**Fundamentals Vault** là kho tài liệu học tập cá nhân, được xây dựng theo phong cách Obsidian knowledge base. Mục tiêu:

- Ghi chép và tổng hợp kiến thức nền tảng backend engineering
- Phục vụ ôn thi phỏng vấn Senior/Principal Engineer
- Chuẩn bị cho System Design interviews
- Tham khảo nhanh khi làm việc thực tế

### Audience

Người dùng duy nhất là **chủ repo** — một backend developer có kinh nghiệm, đang học nâng cao. Tài liệu viết mix tiếng Anh/Việt (kỹ thuật giữ tiếng Anh, diễn giải bằng tiếng Việt).

### Tech Stack / Tooling

- **Editor**: Obsidian (primary), VS Code (editing với AI)
- **Format**: Markdown (`.md`)
- **Links**: Obsidian-style `[[wikilinks]]` và `parent::` / `children::` dataview notation
- **Version Control**: Git (không có CI/CD)

---

## 📁 Cấu Trúc Thư Mục

```
Knowledge/
│
├── CLAUDE.md                    ← File này — AI collaboration guide
├── README.md                    ← Public-facing overview
├── 0 - Fundamentals.md          ← Root index (entry point Obsidian)
│
├── 1 - Go/                      ← Nhóm 1: Go language deep dive
│   ├── go.md                    ← Index của nhóm 1
│   ├── 01 - Language Basics/
│   │   ├── 01 - Language Basics.md   ← Index nhóm con
│   │   ├── 01.1 - Data Types & Basics.md
│   │   └── 01.2 - Control Flow & Functions.md
│   ├── 02 - Memory & Runtime/
│   ├── 03 - Concurrency/
│   ├── 04 - Error Handling/
│   ├── 05 - Generics/
│   ├── 06 - Standard Library/
│   └── 07 - Testing & Tooling/
│
├── 2 - CS Fundamentals/         ← OOP, SOLID, Process, Thread, CAP, DSA
├── 3 - Infrastructure/          ← VM, Container, Security, Cryptography
├── 4 - Networking/              ← Socket, HTTP/2, gRPC
├── 5 - Ecosystem/               ← Docker, Git, AI Tools, Go Embed
└── 6 - System Design/           ← Database, Caching, MQ, Architecture
```

### Naming Convention

| Loại | Pattern | Ví dụ |
|------|---------|-------|
| Nhóm thư mục | `NN - Name/` | `01 - Language Basics/` |
| File index nhóm | `NN - Name.md` | `01 - Language Basics.md` |
| File bài học | `NN.M - Topic.md` | `01.1 - Data Types & Basics.md` |
| File index top-level | `_index.md` hoặc `go.md` | `go.md` |
| Root index | `0 - Fundamentals.md` | — |

---

## ✍️ File Template & Conventions

### Frontmatter (bắt buộc cho tất cả file)

```markdown
---

parent:: [[NhómCha]]
type: concept
status: complete
date_created: 2026-04-21

---
```

> File index nhóm có thêm `children::`:

```markdown
---

parent:: [[go]]
type: index
status: complete

children:: [[01.1 - Data Types & Basics]]
children:: [[01.2 - Control Flow & Functions]]

---
```

### Metadata Fields

| Field | Values | Ý nghĩa |
|-------|--------|--------|
| `type` | `concept`, `index`, `reference`, `comparison` | Loại ghi chú |
| `status` | `draft`, `in-progress`, `complete` | Tiến độ hoàn thành |
| `date_created` | `YYYY-MM-DD` | Ngày tạo (index files không cần) |

> **Quan trọng — Tags vs Links**: Dùng `#tag` cho **trạng thái/loại** (ví dụ: `#draft`, `#todo`). Dùng `[[wikilink]]` cho **chủ đề/khái niệm** (ví dụ: `[[Goroutine]]`, `[[Error Handling]]`). Không dùng tag để phân loại chủ đề — đó là việc của links.

### Cấu trúc nội dung chuẩn

```markdown
---

parent:: [[Xxx]]

---

# NN.M Tiêu đề

## Concept 1

[Định nghĩa ngắn gọn]

```go / sql / bash
[Code example]
```

### Sub-topic (nếu cần)

[Bảng so sánh, diagram, trade-offs]

---

## 📌 Tóm tắt

```
Tree diagram tóm tắt toàn bộ nội dung
├── Concept A
│   ├── detail
│   └── detail
└── Concept B
```

---

## Tags

#tag1 #tag2 #tag3
```

### Heading Convention

| Level | Dùng cho |
|-------|---------|
| `# H1` | Tiêu đề file (duy nhất 1 per file) |
| `## H2` | Section chính (Concept, Pattern, Trade-off) |
| `### H3` | Sub-section, variant, pattern con |
| `#### H4` | Hiếm dùng — chỉ khi H3 quá phức tạp |

---

## 🎯 Content Standards

### Mỗi topic nên có đủ 4 lớp

1. **Định nghĩa** — Là gì, hoạt động thế nào (internals khi cần)
2. **Code examples** — Runnable, idiomatic, có comment giải thích
3. **Góc nhìn đa chiều** — So sánh approaches, khi nào dùng cái nào
4. **Trade-off analysis** — Bảng hoặc prose: pros/cons, performance, use case

### Code examples

- Luôn dùng `go` làm fenced code block language cho Go code
- Dùng `bash` cho commands, `sql` cho SQL, `json` cho JSON
- Comment `// ✅` cho good practice, `// ❌` cho bad practice, `// ⚠️` cho caveats
- Với benchmark numbers: dùng xấp xỉ hợp lý (`~5ns`, `~25ns`) không cần exact

### Bảng so sánh

- Mọi trade-off analysis nên có bảng
- Dùng ✅ ❌ ⚠️ để scan nhanh
- Cột cuối nên là "Use case" hoặc "When to use"

### Tóm tắt (Tóm tắt section)

- Luôn dùng tree diagram (ASCII art)
- Đủ ngắn để scan trong 30 giây
- Mirror cấu trúc H2 sections của file

### Atomic Notes — Khi nào split file

Mỗi file nên tập trung vào **một domain/cluster khái niệm duy nhất**. File hiện tại (`01.1`, `01.2`, ...) đã là đơn vị atomic nhỏ nhất của repo này — không mở rộng vô hạn.

**Nên split thành file mới khi:**

- File vượt ~600 dòng và vẫn còn nhiều nội dung cần thêm
- Một H2 section đủ lớn để đứng độc lập (ví dụ: `Channel` tách khỏi `Concurrency`)
- Có một concept đủ phức tạp để cần file riêng (ví dụ: `slog` → `06.1 - Structured Logging.md`)
- Concept mới không thuộc cluster của file hiện tại

**Không nên mở rộng file hiện tại khi:**

```
❌ Mở rộng 01.1 - Data Types & Basics.md với toàn bộ nội dung về Generics
✅ Tạo file mới: 05.1 - Generics.md trong thư mục 05 - Generics/

❌ Heap thêm mọi thứ về Channels vào 03 - Concurrency.md
✅ Tạo file riêng: 03.2 - Channel & Select.md
```

> **Quy tắc ngón tay cái**: Nếu bạn phải scroll quá 3 lần để đọc hết một section → đó là dấu hiệu cần split.

---

## 🔗 Obsidian Link Rules

### Wikilinks

- **Luôn** dùng `[[Name]]` thay vì `[Name](path.md)` — Obsidian render tốt hơn
- Link đến file name, không phải path: `[[01.1 - Data Types & Basics]]`
- Link text có thể custom: `[[01.1 - Data Types & Basics|Data Types]]`

### parent:: / children::

- **Bắt buộc** có `parent::` trong frontmatter của mọi file (trừ root)
- `children::` chỉ ở file index (nhóm hoặc sub-nhóm)
- Một file có thể có nhiều `children::` — mỗi dòng 1 child
- Format: `parent:: [[FileName]]` — không có extension `.md`

### Hierarchy

```
0 - Fundamentals
    └── go (1 - Go)
        ├── 01 - Language Basics
        │   ├── 01.1 - Data Types & Basics
        │   └── 01.2 - Control Flow & Functions
        └── ...
```

### Cross-linking & MOC (Map of Content)

Folder chỉ giải quyết bài toán **phân loại**. Wikilinks giải quyết bài toán **kết nối ý tưởng** — quan trọng hơn nhiều trong knowledge base.

**Luôn cross-link khi một concept liên quan đến concept khác:**

```markdown
## Goroutine vs OS Thread

Goroutine sử dụng dynamic stack — xem thêm [[02.1 - Memory & Runtime#Stack Growth]].
Scheduler dùng G-M-P model — liên quan đến [[02.2 - Memory Model#Happens-Before]].
```

**MOC (Map of Content)** — Các file index (`go.md`, `01 - Language Basics.md`) đóng vai trò MOC:

- MOC không chứa nội dung chi tiết — chỉ chứa links và context ngắn
- Khi một topic xuất hiện ở nhiều nơi, thêm link vào MOC tương ứng
- Không tạo folder mới nếu có thể giải quyết bằng MOC + wikilinks

**Khi nào mới tạo folder:**

| Tình huống | Dùng folder | Dùng MOC + links |
|-----------|-------------|------------------|
| Có ≥3 files cùng domain | ✅ | — |
| Muốn group files cùng chủ đề con | ✅ | ⚠️ tùy |
| Chỉ có 1-2 files liên quan | ❌ | ✅ link từ MOC |
| Concept liên quan nhiều module | ❌ | ✅ cross-link |

**Link section cụ thể** dùng `#` anchor:

```markdown
[[03.2 - Channel & Select#Semaphore Pattern]]
[[02.2 - Memory Model#Happens-Before]]
```

---

## 🤖 Rules cho AI (Claude)

### Nguyên tắc tổng quát

1. **Không tự ý restructure** thư mục hay rename file trừ khi được yêu cầu rõ ràng
2. **Preserve frontmatter** — không xóa hoặc thay đổi `parent::` / `children::` khi không cần thiết
3. **Giữ nguyên code examples đã có** — chỉ bổ sung thêm, không thay thế trừ khi sai
4. **Consistent language mix** — kỹ thuật (tên hàm, type, pattern) giữ tiếng Anh; giải thích bằng tiếng Việt
5. **Không thêm H1 mới** — mỗi file chỉ có 1 H1

### Khi bổ sung nội dung (enrichment)

- Chèn section mới vào **trước** `## 📌 Tóm tắt`, không sau
- **Cập nhật Tóm tắt** để phản ánh section mới thêm vào
- **Cập nhật Tags** để bao gồm keywords của section mới
- Dùng `---` separator giữa các H2 sections
- Không duplicate nội dung đã có — thêm bổ sung, không viết lại toàn bộ

### Khi tạo file mới

```markdown
---

parent:: [[TênFileCha]]

---

# NN.M Tiêu đề

[nội dung]

---

## 📌 Tóm tắt

```
Tree diagram
```

---

## Tags

#go #topic
```

### Khi cập nhật file index

- Thêm `children:: [[TênFile]]` mới vào frontmatter
- Cập nhật bảng mục lục trong file
- Đảm bảo số thứ tự (NN.M) nhất quán với thư mục

### Không làm

- ❌ Xóa `## 📌 Tóm tắt` hoặc `## Tags`
- ❌ Thêm `# New H1` — chỉ 1 H1 per file
- ❌ Dùng `[link](./relative/path.md)` — dùng `[[wikilink]]` thay
- ❌ Thay đổi tên file mà không cập nhật tất cả wikilinks trỏ đến nó
- ❌ Tạo file không có `parent::` frontmatter
- ❌ Viết toàn tiếng Anh — phải có giải thích tiếng Việt
- ❌ Dùng `#tag` để phân loại chủ đề — dùng `[[wikilink]]` thay
- ❌ Mở rộng vô hạn một file — split thành file mới khi >600 dòng
- ❌ Tạo folder mới khi chỉ có 1-2 file — dùng MOC + links thay
- ❌ Tạo file mới thiếu `type:` và `status:` trong frontmatter

---

## 📊 File Count & Status

| Module | Files | Status |
|--------|-------|--------|
| 1 - Go | 23 | ✅ Enriched (Apr 2026) |
| 2 - CS Fundamentals | ~5 | ⬜ Basic |
| 3 - Infrastructure | ~7 | ⬜ Basic |
| 4 - Networking | ~3 | ⬜ Basic |
| 5 - Ecosystem | ~4 | ⬜ Basic |
| 6 - System Design | ~11 | ⬜ Basic |

> **Last major update**: April 2026 — restructured `1 - Go` từ flat files → 7 domain folders, enriched tất cả 23 files với trade-off analysis, internals, và multi-perspective views.

---

## 📋 Note Types & Workflow

Repo này chủ yếu chứa **Permanent Notes** — kiến thức đã tổng hợp, sẵn sàng lưu trữ lâu dài. Nhưng khi thêm kiến thức mới, nên theo 3 giai đoạn:

### Giai đoạn 1 — Fleeting Note (nháp)

- Ghi chép nhanh khi đọc tài liệu, xem video, làm thực tế
- Có thể đặt ở root hoặc một file tạm `_inbox.md`
- Không cần format chuẩn
- `status: draft`

### Giai đoạn 2 — Literature Note (tổng hợp nguồn)

- Diễn đạt lại kiến thức từ nguồn bằng ngôn ngữ của mình
- Ghi rõ nguồn (link docs, tên sách, tên bài blog)
- Đặt trong thư mục module phù hợp, `status: in-progress`

### Giai đoạn 3 — Permanent Note (hoàn chỉnh)

- Nội dung đã được tổng hợp, so sánh với kiến thức đã có
- Đủ 4 lớp: Định nghĩa + Code + Góc nhìn đa chiều + Trade-off
- Có cross-links tới các file liên quan
- `status: complete`

### Quy tắc intake cho AI

```
Người dùng muốn thêm topic mới:
  ├── Nếu topic thuộc domain đã có → thêm section vào file hiện tại
  │   └── Nếu file >600 dòng → tạo file mới NN.M trong cùng thư mục
  ├── Nếu topic là domain mới → tạo folder + index + content file
  └── Luôn cross-link từ file mới sang các file liên quan
```

---

## 🗓️ Changelog

| Date | Action |
|------|--------|
| Apr 2026 | Add CLAUDE.md: repo guide, rules, Obsidian conventions |
| Apr 2026 | Restructure `1 - Go`: flat → 7 domain folders với consistent numbering |
| Apr 2026 | Enrichment `01-07`: thêm internals, trade-offs, multi-perspective cho 23 files |
| — | Initial vault creation |

---

## 💡 Tips cho AI

- **Context reset?** Đọc file này + `README.md` + file index nhóm đang làm việc trước
- **Không chắc về structure?** Check `go.md` (hoặc index tương đương của module) để hiểu hierarchy
- **Thêm file mới vào Go?** Đặt trong sub-folder đúng, cập nhật `children::` trong file index nhóm tương ứng
- **Cần biết nội dung đang có?** Đọc phần `## 📌 Tóm tắt` của file — đây là summary nhanh nhất
- **Cross-reference?** Dùng `[[wikilink]]` để link sang file khác trong vault
