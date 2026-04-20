---
type: concept
status: complete
date_created: 2026-04-21
tags: [cs, fundamentals, interview-prep, sliding-window, subarray, substring]
---
parent:: [[00 - DSA Patterns]]

# 02 — Sliding Window

> **Giải quyết**: Tìm subarray/substring tối ưu (longest/shortest/sum) trong O(n) — thay vì O(n²) hay O(n³) brute force

---
---

## Hai Loại Window

### 1. Fixed Size Window

Khi đề cho kích thước k cố định.

```go
// Kích thước k cố định — dùng cho: max/min/avg trong k phần tử
windowSum := 0
for i := 0; i < k; i++ {
    windowSum += nums[i]
}
maxSum := windowSum

for i := k; i < len(nums); i++ {
    windowSum += nums[i]     // thêm right
    windowSum -= nums[i-k]   // bỏ left
    maxSum = max(maxSum, windowSum)
}
```

**Dùng khi**: "Find max/min/average in window of size k", "permutation in string".

### 2. Variable Size Window

Khi kích thước window thay đổi theo constraint.

```go
// Variable window — template chung
left := 0
windowState := /* vd: map[byte]int{} */

for right := 0; right < len(s); right++ {
    // EXPAND: thêm s[right] vào window state
    add(s[right], windowState)

    // SHRINK: thu hẹp khi window không valid
    for !isValid(windowState) {
        remove(s[left], windowState)
        left++
    }

    // UPDATE ANSWER: window [left, right] đang valid
    ans = max(ans, right-left+1)
}
```

**Dùng khi**: "Longest substring without...", "minimum window containing...".

---
---

## Window State Patterns

### Freq Map (char count)

```go
// Longest Substring Without Repeating Characters
freq := make(map[byte]int)
left, maxLen := 0, 0

for right := 0; right < len(s); right++ {
    freq[s[right]]++
    for freq[s[right]] > 1 {   // duplicate found
        freq[s[left]]--
        left++
    }
    maxLen = max(maxLen, right-left+1)
}
```

### Count / Need Tracking

```go
// Minimum Window Substring — track what we still need
need := make(map[byte]int)
for _, c := range t { need[c]++ }
have, total := 0, len(need)
window := make(map[byte]int)
left, minLen, minL := 0, math.MaxInt, 0

for right := 0; right < len(s); right++ {
    c := s[right]
    window[c]++
    if need[c] > 0 && window[c] == need[c] { have++ }

    for have == total {             // window covers t
        if right-left+1 < minLen {
            minLen = right - left + 1
            minL = left
        }
        window[s[left]]--
        if need[s[left]] > 0 && window[s[left]] < need[s[left]] { have-- }
        left++
    }
}
```

---
---

## Trade-off vs Alternatives

| Approach | Time | Space | Khi dùng |
|----------|------|-------|----------|
| **Sliding Window** | O(n) | O(k) | Contiguous subarray/string |
| Prefix Sum | O(n) precompute + O(1) query | O(n) | Sum queries, không cần track state |
| Brute Force | O(n²)–O(n³) | O(1) | Không áp dụng được window |
| DP | O(n²) | O(n) | Non-contiguous (LCS, etc.) |

---
---

## Bài Tiêu Biểu

| Bài | Loại | Window State |
|-----|------|-------------|
| Best Time to Buy/Sell Stock | Variable (min so far) | 1 var: min price |
| Longest Substring No Repeat | Variable | freq map |
| Longest Repeating Char Replacement | Variable | freq map + max freq |
| Permutation in String | Fixed | freq map compare |
| Minimum Window Substring | Variable (shrink when valid) | need/have count |
| Sliding Window Maximum | Fixed + Monotonic Deque | deque of indices |

---
