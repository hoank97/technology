---
type: concept
status: complete
date_created: 2026-04-21
tags: [binary-search, cs, fundamentals, interview-prep, monotonic, sorted]
---
parent:: [[00 - DSA Patterns]]

# 04 — Binary Search

> **Giải quyết**: Tìm kiếm trong không gian có **monotonicity** (đơn điệu) từ O(n) xuống O(log n) — hoặc tìm điểm "threshold" tối ưu trong một range

---
---

## Template — Tổng Quát Nhất

```go
// Luôn dùng template này — tránh off-by-one errors
// Tìm vị trí LO nhỏ nhất mà condition(lo) = true
lo, hi := lowerBound, upperBound  // [lo, hi)

for lo < hi {
    mid := lo + (hi-lo)/2  // tránh overflow (không dùng (lo+hi)/2)
    if condition(mid) {
        hi = mid            // condition true → search left half (including mid)
    } else {
        lo = mid + 1        // condition false → search right half (exclude mid)
    }
}
return lo  // lo == hi == điểm threshold
```

> **Lưu ý**: `lo + (hi-lo)/2` thay vì `(lo+hi)/2` — tránh integer overflow khi lo+hi > MaxInt.

---
---

## Nhận Ra Pattern

| Signal | Binary Search type |
|--------|-------------------|
| Sorted array, tìm phần tử | Classic |
| "First/Last occurrence" | Leftmost/Rightmost boundary |
| "Minimum speed/size/capacity that can..." | On Answer |
| "Rotated sorted array" | Rotated variant |
| "Median of two sorted arrays" | Partition-based |
| "Search in matrix" (sorted rows) | 2D binary search |

**Câu hỏi để nhận diện "on answer"**: *"Nếu tôi cố định giá trị answer = x, tôi có thể check feasibility trong O(n) không?"* → Nếu có → Binary Search on Answer.

---
---

## Trade-off vs Alternatives

| Approach | Time | Space | Điều kiện |
|----------|------|-------|-----------|
| **Binary Search** | O(log n) | O(1) | Sorted / monotonic predicate |
| Linear Search | O(n) | O(1) | Bất kỳ |
| Hash Set | O(1) avg | O(n) | Exact match, unsorted |
| Two Pointers | O(n) | O(1) | Sorted, pair/sum |

---
---

## Bài Tiêu Biểu

| Bài | Type | Key insight |
|-----|------|------------|
| Binary Search | Classic | Standard template |
| Find Minimum in Rotated Array | Rotated | So sánh mid với right |
| Search in Rotated Array | Rotated | Xác định half nào sorted |
| Koko Eating Bananas | On Answer | `canFinish(speed)` check |
| Time Based Key-Value | On Answer | Binary search trên timestamps |
| Median of Two Sorted Arrays | Partition | Balance left partition |

---
