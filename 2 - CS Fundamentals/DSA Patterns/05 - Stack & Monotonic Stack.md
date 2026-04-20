---
type: concept
status: complete
date_created: 2026-04-21
tags: [cs, fundamentals, histogram, interview-prep, monotonic-stack, next-greater, stack]
---
parent:: [[00 - DSA Patterns]]

# 05 — Stack & Monotonic Stack

> **Stack giải quyết**: Bài toán cần "nhớ lại" hoặc "undo" theo thứ tự LIFO — matching, expression evaluation, DFS iterative

> **Monotonic Stack giải quyết**: Tìm **Next Greater/Smaller Element** hoặc calculate area liên quan đến "nearest element thỏa điều kiện" — O(n) thay vì O(n²)

---
---

## Phần 2: Monotonic Stack

### Bài Toán Giải Quyết

Khi cần tìm **"Next Greater Element"**, **"Previous Smaller Element"**, hoặc tính **diện tích histogram**.

**Core insight**: Duy trì stack chỉ chứa các phần tử "còn có ích" (theo thứ tự tăng/giảm). Khi gặp phần tử mới phá vỡ order → pop và xử lý → O(n) vì mỗi phần tử được push/pop đúng 1 lần.

### Monotonic Decreasing Stack — Next Greater Element

```go
// Daily Temperatures: tìm số ngày đến khi nhiệt độ cao hơn
result := make([]int, len(temps))
stack := []int{} // stores indices (decreasing temps)

for i, t := range temps {
    // pop tất cả phần tử trong stack nhỏ hơn temps[i]
    for len(stack) > 0 && temps[stack[len(stack)-1]] < t {
        idx := stack[len(stack)-1]
        stack = stack[:len(stack)-1]
        result[idx] = i - idx   // found next greater!
    }
    stack = append(stack, i)
}
// remain in stack: no next greater → result[i] = 0 (default)
```

### Monotonic Increasing Stack — Previous Smaller + Area

```go
// Largest Rectangle in Histogram
maxArea := 0
stack := []int{-1} // sentinel

for i := 0; i <= len(heights); i++ {
    h := 0
    if i < len(heights) { h = heights[i] }

    for len(stack) > 1 && heights[stack[len(stack)-1]] > h {
        height := heights[stack[len(stack)-1]]
        stack = stack[:len(stack)-1]
        width := i - stack[len(stack)-1] - 1
        maxArea = max(maxArea, height*width)
    }
    stack = append(stack, i)
}
return maxArea
```

---
---

## Nhận Ra Pattern

| Signal | Pattern |
|--------|---------|
| "matching brackets", "valid parentheses" | Classic Stack |
| "evaluate expression", "RPN" | Stack calculator |
| "next greater element", "next warmer temp" | Monotonic Decreasing Stack |
| "previous smaller", "span" | Monotonic Increasing Stack |
| "largest rectangle in histogram" | Monotonic Stack + area calc |
| "trapping rain water" | Stack hoặc Two Pointers |
| "car fleet" (relative ordering) | Monotonic Stack |

---
---

## Trade-off vs Alternatives

| Bài | Stack | Alternative | Better? |
|-----|-------|-------------|---------|
| Next Greater Element | O(n) Monotonic | O(n²) Brute Force | Stack ✅ |
| Histogram Max Area | O(n) Monotonic | O(n²) Brute Force | Stack ✅ |
| Trapping Rain Water | O(n) Stack | O(n) Two Pointers | Two Ptr (space O(1)) ✅ |
| Valid Parentheses | O(n) Stack | O(n²) Regex | Stack ✅ |
| DFS Tree/Graph | Stack (iterative) | Recursion (implicit stack) | Tùy depth |

---
---

## 📌 Tóm tắt

```
Stack & Monotonic Stack
│
├── Classic Stack (LIFO)
│   ├── Matching brackets
│   ├── Expression evaluation
│   └── Min/Max tracking (aux stack)
│
├── Monotonic Stack
│   ├── Decreasing stack → Next Greater Element
│   ├── Increasing stack → Next Smaller / Previous Smaller
│   └── Mỗi element push/pop đúng 1 lần → O(n)
│
├── Nhận ra pattern
│   ├── "next greater/smaller" → Monotonic
│   └── "matching", "undo" → Classic
│
├── ✅ O(n) cho bài O(n²) nếu dùng brute force
└── ❌ O(n) space, Monotonic khó visualize ban đầu
```
