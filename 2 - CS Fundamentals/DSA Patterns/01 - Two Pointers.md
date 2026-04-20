---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 01 — Two Pointers

> **Giải quyết**: Tìm pair/triplet thỏa mãn điều kiện trong array đã sorted — giảm từ O(n²) xuống O(n)

---

## Bài Toán Giải Quyết

Khi cần kiểm tra **hai phần tử** (hoặc nhiều) trong array thỏa mãn một điều kiện (sum = target, không overlap, palindrome...). Brute force dùng 2 vòng lặp lồng nhau = O(n²). Two Pointers khai thác **sorted order** để loại bỏ nhánh không cần xét.

**Core insight**: Nếu `arr[left] + arr[right] > target` → `right--` (giảm sum). Nếu `< target` → `left++` (tăng sum). Mỗi lần cả hai pointer chỉ di chuyển một chiều → O(n).

---

## Các Biến Thể

### 1. Opposite Ends (Two Sum style)

```go
// Tìm pair trong sorted array có sum = target
left, right := 0, len(nums)-1
for left < right {
    sum := nums[left] + nums[right]
    if sum == target {
        return []int{left, right}
    } else if sum < target {
        left++
    } else {
        right--
    }
}
```

**Dùng khi**: Array sorted, tìm pair thỏa điều kiện.

### 2. Same Direction (Fast/Slow)

```go
// Remove duplicates in-place
slow := 0
for fast := 1; fast < len(nums); fast++ {
    if nums[fast] != nums[slow] {
        slow++
        nums[slow] = nums[fast]
    }
}
return slow + 1
```

**Dùng khi**: Partition, remove in-place, cycle detection.

### 3. Three Pointers (3Sum)

```go
sort.Ints(nums)
for i := 0; i < len(nums)-2; i++ {
    if i > 0 && nums[i] == nums[i-1] { continue } // skip dup
    left, right := i+1, len(nums)-1
    for left < right {
        sum := nums[i] + nums[left] + nums[right]
        if sum == 0 {
            result = append(result, []int{nums[i], nums[left], nums[right]})
            for left < right && nums[left] == nums[left+1] { left++ }
            for left < right && nums[right] == nums[right-1] { right-- }
            left++; right--
        } else if sum < 0 {
            left++
        } else {
            right--
        }
    }
}
```

---

## Nhận Ra Pattern

| Signal | Ví dụ |
|--------|-------|
| "sorted array" + pair/triplet | Two Sum II, 3Sum |
| "in-place" + remove/partition | Remove Duplicates |
| "palindrome" check | Valid Palindrome |
| Tìm area/distance giữa 2 phần tử | Container With Most Water |
| Largest sum ≤ target (sorted) | Two Sum II |

---

## ✅ Ưu Điểm

- **O(n) time** thay vì O(n²) brute force
- **O(1) space** — không cần extra data structure
- Code đơn giản, dễ implement
- Tự nhiên handle sorted order

## ❌ Nhược Điểm / Giới Hạn

- **Yêu cầu sorted** (hoặc phải biết property của input) — nếu không sorted phải sort trước O(n log n)
- Chỉ hoạt động khi có **monotonic property** (tăng/giảm một pointer → sum tăng/giảm predictably)
- Không hoạt động cho unsorted + no monotonicity → dùng Hash Map thay
- 3Sum với dedup: dễ bị sai khi handle duplicate cases

---

## Trade-off vs Alternatives

| Approach | Time | Space | Điều kiện |
|----------|------|-------|-----------|
| **Two Pointers** | O(n) | O(1) | Array đã sorted |
| Hash Map (Two Sum) | O(n) | O(n) | Unsorted, chỉ cần 1 pair |
| Brute Force | O(n²) | O(1) | Không điều kiện |
| Binary Search (outer + BS) | O(n log n) | O(1) | Sorted, tìm 1 phần tử |

> **Kết luận**: Nếu sorted → Two Pointers. Nếu không sorted và tìm 1 pair → Hash Map. Nếu cần tất cả pairs → sort + Two Pointers.

---

## Bài Tiêu Biểu

| Bài | Pattern cụ thể | Insight |
|-----|---------------|---------|
| Valid Palindrome | Opposite ends, skip non-alnum | `isAlphanumeric` filter |
| Two Sum II | Opposite ends, sum compare | Sorted → monotonic |
| 3Sum | Sort + fix i + two ptr | Dedup triple at 3 levels |
| Container With Most Water | Opposite ends, maximize area | Move shorter side inward |
| Trapping Rain Water | Two ptr với left/right max | Track max từ hai phía |

---

## 📌 Tóm tắt

```
Two Pointers
│
├── Khi nào dùng
│   ├── Sorted array + pair/triplet condition
│   ├── In-place partition / remove
│   └── Palindrome, window comparison
│
├── Biến thể
│   ├── Opposite ends: left ↔ right → nhau
│   ├── Same direction: slow/fast (partition, cycle)
│   └── Three ptrs: fix i + two ptr inward
│
├── ✅ O(n) time, O(1) space
├── ❌ Cần sorted (hoặc monotonic property)
│
└── vs Hash Map
    ├── Two Ptr: sorted, O(1) space
    └── Hash Map: unsorted, O(n) space
```

## Tags

#two-pointers #array #sort #interview-prep
