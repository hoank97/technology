---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 04 — Binary Search

> **Giải quyết**: Tìm kiếm trong không gian có **monotonicity** (đơn điệu) từ O(n) xuống O(log n) — hoặc tìm điểm "threshold" tối ưu trong một range

---

## Bài Toán Giải Quyết

Binary Search không chỉ dùng để tìm phần tử trong sorted array. Pattern rộng hơn:

1. **Classic**: Tìm phần tử x trong sorted array
2. **Boundary**: Tìm vị trí leftmost/rightmost thỏa điều kiện
3. **On Answer**: Tìm minimum/maximum value thỏa constraint (không phải search trên array)
4. **Rotated**: Array bị rotate nhưng vẫn có monotonic property từng phần

**Core insight**: Nếu có **predicate** `f(x)` mà:
- Với x < threshold: `f(x) = false`
- Với x ≥ threshold: `f(x) = true`

→ Binary search tìm threshold trong O(log n).

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

## Biến Thể

### 1. Classic — Exact Match

```go
lo, hi := 0, len(nums)-1
for lo <= hi {
    mid := lo + (hi-lo)/2
    if nums[mid] == target { return mid }
    if nums[mid] < target { lo = mid+1 } else { hi = mid-1 }
}
return -1
```

### 2. Leftmost Boundary — "First True"

```go
// Tìm vị trí đầu tiên mà nums[i] >= target
lo, hi := 0, len(nums)
for lo < hi {
    mid := lo + (hi-lo)/2
    if nums[mid] >= target { hi = mid } else { lo = mid+1 }
}
return lo  // lo = first index where nums[lo] >= target
```

### 3. Binary Search on Answer

```go
// Koko Eating Bananas: tìm minimum speed k để ăn hết trong h giờ
canFinish := func(speed int) bool {
    hours := 0
    for _, p := range piles {
        hours += (p + speed - 1) / speed  // ceiling division
    }
    return hours <= h
}

lo, hi := 1, maxPile
for lo < hi {
    mid := lo + (hi-lo)/2
    if canFinish(mid) { hi = mid } else { lo = mid+1 }
}
return lo
```

### 4. Rotated Sorted Array

```go
// Khai thác: một nửa array luôn sorted
lo, hi := 0, len(nums)-1
for lo <= hi {
    mid := lo + (hi-lo)/2
    if nums[mid] == target { return mid }

    if nums[lo] <= nums[mid] {  // left half is sorted
        if nums[lo] <= target && target < nums[mid] {
            hi = mid - 1
        } else {
            lo = mid + 1
        }
    } else {  // right half is sorted
        if nums[mid] < target && target <= nums[hi] {
            lo = mid + 1
        } else {
            hi = mid - 1
        }
    }
}
return -1
```

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

## ✅ Ưu Điểm

- **O(log n)** — giảm search space một nửa sau mỗi bước
- **O(1) space** — không cần extra memory
- Áp dụng được cho bất kỳ **monotonic predicate** — không chỉ sorted array
- "On Answer" mở rộng phạm vi áp dụng rất lớn

## ❌ Nhược Điểm / Giới Hạn

- **Yêu cầu monotonicity** — nếu không có đơn điệu tuyến tính → không áp dụng
- **Off-by-one errors** cực kỳ phổ biến — `lo <= hi` vs `lo < hi`, `mid+1` vs `mid`
- "On Answer" cần define rõ predicate và bound đúng
- Khó debug vì boundary conditions

---

## Trade-off vs Alternatives

| Approach | Time | Space | Điều kiện |
|----------|------|-------|-----------|
| **Binary Search** | O(log n) | O(1) | Sorted / monotonic predicate |
| Linear Search | O(n) | O(1) | Bất kỳ |
| Hash Set | O(1) avg | O(n) | Exact match, unsorted |
| Two Pointers | O(n) | O(1) | Sorted, pair/sum |

---

## Common Mistakes

```go
// ❌ Sai: vòng thi lo <= hi + hi = mid → infinite loop khi lo == hi
for lo <= hi {
    mid := (lo + hi) / 2
    if condition(mid) { hi = mid }   // ❌ nếu lo==hi==mid → loop mãi
    else { lo = mid + 1 }
}

// ✅ Đúng: lo < hi + hi = mid (an toàn vì mid < hi khi lo < hi)
for lo < hi {
    mid := lo + (hi-lo)/2
    if condition(mid) { hi = mid }   // ✅ hi nhỏ dần, chắc chắn terminate
    else { lo = mid + 1 }
}

// ❌ Integer overflow
mid := (lo + hi) / 2  // lo + hi có thể overflow int32

// ✅ Safe
mid := lo + (hi-lo)/2
```

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

## 📌 Tóm tắt

```
Binary Search
│
├── Khi nào
│   ├── Sorted array → tìm phần tử hoặc boundary
│   ├── Monotonic predicate → tìm threshold
│   └── "Minimum X that satisfies Y" → on answer
│
├── Template chuẩn
│   ├── lo < hi (không phải lo <= hi)
│   ├── mid = lo + (hi-lo)/2  (tránh overflow)
│   ├── condition true → hi = mid
│   └── condition false → lo = mid+1
│
├── Biến thể
│   ├── Classic: exact match, lo <= hi
│   ├── Boundary: leftmost/rightmost
│   ├── On Answer: feasibility check
│   └── Rotated: xác định sorted half
│
├── ✅ O(log n) time, O(1) space
└── ❌ Off-by-one prone, yêu cầu monotonicity
```

## Tags

#binary-search #sorted #monotonic #interview-prep
