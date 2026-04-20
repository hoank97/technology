# 🐛 Obsidian Compatibility Issues

> Audit date: 2026-04-21
> Scope: Toàn bộ vault `/Knowledge`
> Status: 5 issues, 0 resolved

---

## Issue #1 — `parent::` / `children::` nằm SAI chỗ trong YAML block

**Mức độ**: 🔴 High — Obsidian Properties panel không nhận ra, Dataview có thể không parse đúng

**Mô tả**: Các field `parent::` và `children::` đang được đặt **bên trong** `---` YAML block, nhưng chúng không phải YAML syntax hợp lệ. Chúng là Dataview **inline field** syntax, phải đặt **ngoài** YAML block (trong body). Hiện tại Obsidian Properties panel sẽ báo warning và có thể render sai.

**Hiện trạng (sai)**:
```yaml
---
parent:: [[01 - Language Basics]]   ← KHÔNG PHẢI YAML
---
```

**Fix đúng (chọn một)**:
- **Option A** — Dataview inline fields (đặt ở đầu body, sau `---`):
  ```markdown
  ---
  type: concept
  status: complete
  tags: [go, concurrency]
  ---
  
  parent:: [[01 - Language Basics]]
  ```
- **Option B** — Thuần YAML Properties (Obsidian native, không cần Dataview):
  ```yaml
  ---
  parent: "01 - Language Basics"
  type: concept
  status: complete
  tags: [go, concurrency]
  ---
  ```

**Recommendation**: Option A — giữ `parent::` / `children::` syntax để tương thích Dataview Graph, nhưng chuyển ra ngoài YAML block.

**Files bị ảnh hưởng** (23 files trong `1 - Go/`):

- [ ] `1 - Go/1 - Go.md`
- [ ] `1 - Go/01 - Language Basics/01 - Language Basics.md`
- [ ] `1 - Go/01 - Language Basics/01.1 - Data Types & Basics.md`
- [ ] `1 - Go/01 - Language Basics/01.2 - Control Flow & Functions.md`
- [ ] `1 - Go/02 - Memory & Runtime/02 - Memory & Runtime.md`
- [ ] `1 - Go/02 - Memory & Runtime/02.1 - Memory & Runtime.md`
- [ ] `1 - Go/02 - Memory & Runtime/02.2 - Memory Model.md`
- [ ] `1 - Go/03 - Concurrency/03 - Concurrency.md`
- [ ] `1 - Go/03 - Concurrency/03.1 - Goroutine & Scheduler.md`
- [ ] `1 - Go/03 - Concurrency/03.2 - Channel & Select.md`
- [ ] `1 - Go/03 - Concurrency/03.3 - Concurrency Tools.md`
- [ ] `1 - Go/04 - Error Handling/04 - Error Handling.md`
- [ ] `1 - Go/04 - Error Handling/04.1 - Error is a Value.md`
- [ ] `1 - Go/04 - Error Handling/04.2 - Custom Error.md`
- [ ] `1 - Go/04 - Error Handling/04.3 - Panic & Recover.md`
- [ ] `1 - Go/05 - Generics/05 - Generics.md`
- [ ] `1 - Go/05 - Generics/05.1 - Generics.md`
- [ ] `1 - Go/05 - Generics/05.2 - Generic Algorithms (std).md`
- [ ] `1 - Go/06 - Standard Library/06 - Standard Library.md`
- [ ] `1 - Go/06 - Standard Library/06.1 - Structured Logging (slog).md`
- [ ] `1 - Go/07 - Testing & Tooling/07 - Testing & Tooling.md`
- [ ] `1 - Go/07 - Testing & Tooling/07.1 - Testing.md`
- [ ] `1 - Go/07 - Testing & Tooling/07.2 - Build & Tooling.md`

**Ghi chú**: Các module 2–6 chưa audit nhưng khả năng cao cùng vấn đề.

> - [x] **[RESOLVED]** Toàn bộ 23 files trong `1 - Go/` đã được fix

---

## Issue #2 — Tags trong `## Tags` section của body, không trong YAML frontmatter

**Mức độ**: 🟡 Medium — Tags pane và Graph View filter hoạt động kém hiệu quả

**Mô tả**: Obsidian đọc tags tốt nhất từ YAML frontmatter (`tags: [go, concurrency]`). Tags dạng `#go #concurrency` ở cuối body vẫn được nhận, nhưng:
- **Tags pane** không hiển thị đầy đủ
- **Graph View** filtering theo tag kém chính xác
- **Search** `tag:#go` có thể miss một số files

**Hiện trạng (mọi content file)**:
```markdown
## Tags

#go #goroutine #scheduler #gmp
```

**Fix mong muốn**:
```yaml
---
tags: [go, goroutine, scheduler, gmp]
type: concept
status: complete
---
```

**Files bị ảnh hưởng**: Tất cả 23 files trong `1 - Go/` (xem danh sách ở Issue #1)

> - [x] **[RESOLVED]** Toàn bộ 23 files đã migrate tags vào YAML frontmatter

---

## Issue #3 — Thiếu `type`, `status`, `date_created` trong frontmatter

**Mức độ**: 🟡 Medium — Không thể filter/query theo trạng thái trong Dataview hoặc Obsidian Search

**Mô tả**: CLAUDE.md đã định nghĩa 3 metadata fields mới nhưng chưa được backfill vào các file hiện có. Không có `status` field thì không thể tạo Dataview query như:
```dataview
TABLE status, type FROM "1 - Go"
WHERE status = "draft"
```

**Fields cần thêm vào mọi file**:

| Field | Content files | Index files |
|-------|--------------|-------------|
| `type` | `concept` | `index` |
| `status` | `complete` (đã enriched) | `complete` |
| `date_created` | `2026-04-21` | không cần |

**Files bị ảnh hưởng** — cần thêm `type` + `status`:

- [ ] `1 - Go/1 - Go.md` — `type: index`
- [ ] `1 - Go/01 - Language Basics/01 - Language Basics.md` — `type: index`
- [ ] `1 - Go/01 - Language Basics/01.1 - Data Types & Basics.md` — `type: concept`
- [ ] `1 - Go/01 - Language Basics/01.2 - Control Flow & Functions.md` — `type: concept`
- [ ] `1 - Go/02 - Memory & Runtime/02 - Memory & Runtime.md` — `type: index`
- [ ] `1 - Go/02 - Memory & Runtime/02.1 - Memory & Runtime.md` — `type: concept`
- [ ] `1 - Go/02 - Memory & Runtime/02.2 - Memory Model.md` — `type: concept`
- [ ] `1 - Go/03 - Concurrency/03 - Concurrency.md` — `type: index`
- [ ] `1 - Go/03 - Concurrency/03.1 - Goroutine & Scheduler.md` — `type: concept`
- [ ] `1 - Go/03 - Concurrency/03.2 - Channel & Select.md` — `type: concept`
- [ ] `1 - Go/03 - Concurrency/03.3 - Concurrency Tools.md` — `type: concept`
- [ ] `1 - Go/04 - Error Handling/04 - Error Handling.md` — `type: index`
- [ ] `1 - Go/04 - Error Handling/04.1 - Error is a Value.md` — `type: concept`
- [ ] `1 - Go/04 - Error Handling/04.2 - Custom Error.md` — `type: concept`
- [ ] `1 - Go/04 - Error Handling/04.3 - Panic & Recover.md` — `type: concept`
- [ ] `1 - Go/05 - Generics/05 - Generics.md` — `type: index`
- [ ] `1 - Go/05 - Generics/05.1 - Generics.md` — `type: concept`
- [ ] `1 - Go/05 - Generics/05.2 - Generic Algorithms (std).md` — `type: reference`
- [ ] `1 - Go/06 - Standard Library/06 - Standard Library.md` — `type: index`
- [ ] `1 - Go/06 - Standard Library/06.1 - Structured Logging (slog).md` — `type: concept`
- [ ] `1 - Go/07 - Testing & Tooling/07 - Testing & Tooling.md` — `type: index`
- [ ] `1 - Go/07 - Testing & Tooling/07.1 - Testing.md` — `type: concept`
- [ ] `1 - Go/07 - Testing & Tooling/07.2 - Build & Tooling.md` — `type: reference`

> - [x] **[RESOLVED]** Toàn bộ 23 files đã có `type`, `status`, `date_created`

---

## Issue #4 — Broken wikilink: `parent:: [[_index]]`

**Mức độ**: 🔴 High — Obsidian Graph View hiển thị unresolved link, broken hierarchy

**Mô tả**: 7 file index của các sub-folder trong `1 - Go/` đang trỏ tới `[[_index]]` — một file **không tồn tại** trong vault. Link đúng phải là `[[1 - Go]]` (tên file index của nhóm Go).

**Cần đổi**: `parent:: [[_index]]` → `parent:: [[1 - Go]]`

**Files bị ảnh hưởng**:

- [ ] `1 - Go/01 - Language Basics/01 - Language Basics.md` — `parent:: [[_index]]` → `[[1 - Go]]`
- [ ] `1 - Go/02 - Memory & Runtime/02 - Memory & Runtime.md` — `parent:: [[_index]]` → `[[1 - Go]]`
- [ ] `1 - Go/03 - Concurrency/03 - Concurrency.md` — `parent:: [[_index]]` → `[[1 - Go]]`
- [ ] `1 - Go/04 - Error Handling/04 - Error Handling.md` — `parent:: [[_index]]` → `[[1 - Go]]`
- [ ] `1 - Go/05 - Generics/05 - Generics.md` — `parent:: [[_index]]` → `[[1 - Go]]`
- [ ] `1 - Go/06 - Standard Library/06 - Standard Library.md` — `parent:: [[_index]]` → `[[1 - Go]]`
- [ ] `1 - Go/07 - Testing & Tooling/07 - Testing & Tooling.md` — `parent:: [[_index]]` → `[[1 - Go]]`

> - [x] **[RESOLVED]** Toàn bộ 7 broken links đã được fix

---

## Issue #5 — `0 - Fundamentals.md` dùng `parent:: []` (invalid)

**Mức độ**: 🟢 Low — Không gây lỗi nghiêm trọng, nhưng không đúng convention

**Mô tả**: File root `0 - Fundamentals.md` có `parent:: []` — đây là syntax không hợp lệ. File root không cần `parent::`.

**Hiện trạng**:
```yaml
---
parent:: []
---
```

**Fix**:
```yaml
---
type: index
status: complete
---
```

**Files bị ảnh hưởng**:

- [ ] `0 - Fundamentals.md` — xóa `parent:: []`, thêm `type: index`

> - [x] **[RESOLVED]**

---

## 📋 Tổng Kết

| # | Issue | Mức độ | Files | Status |
|---|-------|--------|-------|--------|
| #1 | `parent::` sai vị trí trong YAML | 🔴 High | 23 | ✅ Done |
| #2 | Tags trong body thay vì frontmatter | 🟡 Medium | 23 | ✅ Done |
| #3 | Thiếu `type`, `status` metadata | 🟡 Medium | 23 | ✅ Done |
| #4 | Broken `[[_index]]` links | 🔴 High | 7 | ✅ Done |
| #5 | `parent:: []` invalid ở root file | 🟢 Low | 1 | ✅ Done |

> **Recommended fix order**: #4 (quick, critical) → #1 (structural fix) → #2+#3 (can batch via script)

---

## 💡 Fix Strategy

Issues #1, #2, #3 có thể giải quyết cùng lúc bằng **Python/bash script** để:
1. Parse từng `.md` file
2. Tách `parent::` / `children::` ra khỏi YAML block
3. Đưa `tags:` vào YAML block
4. Thêm `type:` và `status:` vào YAML block
5. Ghi lại file

Khi muốn resolve, nói với Claude: *"resolve issue #1 #2 #3 bằng script tự động"*

Issues #4 và #5 đơn giản, có thể fix thủ công hoặc bằng `sed`.
