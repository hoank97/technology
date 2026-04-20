---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 02 — Sliding Window

> **Giải quyết**: Tìm subarray/substring tối ưu (longest/shortest/sum) trong O(n) — thay vì O(n²) hay O(n³) brute force

---

## Bài Toán Giải Quyết

Khi cần tìm **contiguous subarray hoặc substring** thỏa mãn điều kiện. Brute force kiểm tra mọi cặp (i, j) = O(n²). Sliding Window duy trì một "cửa sổ" [left, right] và mở rộng/thu hẹp thay vì restart từ đầu — mỗi phần tử chỉ được thêm/xóa khỏi window đúng 1 lần → O(n).

**Core insight**: Thay vì tính lại từ đầu, **slide** window sang phải: thêm `right`, bỏ `left` khi window không còn valid.

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

## Nhận Ra Pattern

| Signal | Bài |
|--------|-----|
| "subarray/substring" + "contiguous" | Almost always sliding window |
| "longest/shortest" + constraint | Variable window |
| "exactly k" / "at most k" | Window + freq tracking |
| "permutation of p in s" | Fixed window + freq compare |
| "minimum window containing" | Variable window + cover check |

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

## ✅ Ưu Điểm

- **O(n)** — mỗi element được add/remove đúng 1 lần dù có 2 vòng for lồng nhau
- **O(k) space** — chỉ lưu trạng thái window hiện tại (thường là freq map size k)
- **Elegant**: loại bỏ hoàn toàn brute force O(n² / n³)
- Áp dụng được cho cả string lẫn số

## ❌ Nhược Điểm / Giới Hạn

- **Chỉ hoạt động cho contiguous** (liền tiếp) — không dùng được cho subsequence
- Window state phải **additive và removable** — nếu state phức tạp (ví dụ: max trong window) cần thêm cấu trúc (Monotonic Deque)
- Shrink condition phải **monotonic**: khi window invalid, thêm phần tử không tự fix → cần shrink left
- Dễ nhầm giữa `right - left + 1` vs `right - left`

---

## Trade-off vs Alternatives

| Approach | Time | Space | Khi dùng |
|----------|------|-------|----------|
| **Sliding Window** | O(n) | O(k) | Contiguous subarray/string |
| Prefix Sum | O(n) precompute + O(1) query | O(n) | Sum queries, không cần track state |
| Brute Force | O(n²)–O(n³) | O(1) | Không áp dụng được window |
| DP | O(n²) | O(n) | Non-contiguous (LCS, etc.) |

---

## Monotonic Deque — Mở Rộng

Khi cần **max/min trong sliding window** → Deque (Double-ended queue):

```go
// Sliding Window Maximum
dq := []int{} // stores indices, decreasing value
result := []int{}

for i := 0; i < len(nums); i++ {
    // bỏ phần tử out of window
    for len(dq) > 0 && dq[0] < i-k+1 {
        dq = dq[1:]
    }
    // bỏ phần tử nhỏ hơn nums[i] (không có ích)
    for len(dq) > 0 && nums[dq[len(dq)-1]] < nums[i] {
        dq = dq[:len(dq)-1]
    }
    dq = append(dq, i)
    if i >= k-1 {
        result = append(result, nums[dq[0]])
    }
}
```

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

## 📌 Tóm tắt

```
Sliding Window
│
├── Khi nào
│   ├── Contiguous subarray/substring
│   └── Longest/Shortest/Sum tối ưu
│
├── Fixed Window (size k cố định)
│   └── Add right, remove left-k → O(n)
│
├── Variable Window (shrink khi invalid)
│   ├── Expand right
│   ├── Shrink left until valid
│   └── Update answer khi valid
│
├── Window State
│   ├── Freq map: char/num count
│   ├── Single counter: sum, have/need
│   └── Deque: max/min in window
│
├── ✅ O(n) — mỗi element processed đúng 1 lần
└── ❌ Chỉ contiguous, state phải monotonic
```

## Tags

#sliding-window #substring #subarray #interview-prep
