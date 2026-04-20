---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 05 — Stack & Monotonic Stack

> **Stack giải quyết**: Bài toán cần "nhớ lại" hoặc "undo" theo thứ tự LIFO — matching, expression evaluation, DFS iterative

> **Monotonic Stack giải quyết**: Tìm **Next Greater/Smaller Element** hoặc calculate area liên quan đến "nearest element thỏa điều kiện" — O(n) thay vì O(n²)

---

## Phần 1: Stack Cơ Bản

### Bài Toán Giải Quyết

- Matching pairs: `()`, `{}`, `[]`
- Expression evaluation (RPN, calculator)
- Undo operations, browser history
- DFS iterative (thay recursive call stack)
- "Nearest element" bài toán

### Pattern: Matching Brackets

```go
stack := []byte{}
pairs := map[byte]byte{')': '(', '}': '{', ']': '['}

for i := 0; i < len(s); i++ {
    c := s[i]
    if c == '(' || c == '{' || c == '[' {
        stack = append(stack, c)
    } else {
        if len(stack) == 0 || stack[len(stack)-1] != pairs[c] {
            return false
        }
        stack = stack[:len(stack)-1]   // pop
    }
}
return len(stack) == 0
```

### Pattern: Min Stack

```go
// Maintain auxiliary stack tracking minimum so far
type MinStack struct {
    stack    []int
    minStack []int
}

func (ms *MinStack) Push(val int) {
    ms.stack = append(ms.stack, val)
    minVal := val
    if len(ms.minStack) > 0 && ms.minStack[len(ms.minStack)-1] < val {
        minVal = ms.minStack[len(ms.minStack)-1]
    }
    ms.minStack = append(ms.minStack, minVal)
}

func (ms *MinStack) GetMin() int {
    return ms.minStack[len(ms.minStack)-1]
}
```

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

## Phân Biệt: Monotonic Increasing vs Decreasing

| | Stack order | Pop khi | Tìm được |
|---|---|---|---|
| **Decreasing** (lớn → nhỏ) | decreasing top→bottom | new element > top | **Next Greater** to the right |
| **Increasing** (nhỏ → lớn) | increasing top→bottom | new element < top | **Next Smaller** / Previous smaller |

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

## ✅ Ưu Điểm

**Classic Stack**:
- O(n) time, O(n) space — thường không còn cách nào tốt hơn
- Đơn giản, trực quan

**Monotonic Stack**:
- **O(n)** cho bài "next greater/smaller" — so với O(n²) brute force
- Mỗi phần tử push/pop đúng 1 lần → amortized O(1) per element
- Xử lý được nhiều bài tưởng phải O(n²)

## ❌ Nhược Điểm / Giới Hạn

- **O(n) extra space** cho stack
- Monotonic Stack khó visualize ban đầu — cần practice để nhận ra
- Dễ sai khi handle phần tử còn lại trong stack sau vòng lặp
- Stack trong Go không có built-in type → dùng slice (append/re-slice)

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

## Bài Tiêu Biểu

| Bài | Pattern | Key |
|-----|---------|-----|
| Valid Parentheses | Classic matching | map close→open |
| Min Stack | Aux min-tracking stack | minStack|
| Evaluate RPN | Classic calculator | pop 2, push result |
| Daily Temperatures | Monotonic decreasing | pop khi temp > top |
| Car Fleet | Monotonic (time to reach) | pop faster = same fleet |
| Largest Rectangle | Monotonic increasing + sentinel | width = i - left - 1 |

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

## Tags

#stack #monotonic-stack #next-greater #histogram #interview-prep
