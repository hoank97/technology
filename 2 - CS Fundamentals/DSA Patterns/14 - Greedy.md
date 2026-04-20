---
type: concept
status: complete
date_created: 2026-04-21
tags: [cs, fundamentals, greedy, intervals, interview-prep, optimization, scheduling]
---
parent:: [[00 - DSA Patterns]]

# 14 — Greedy

> **Giải quyết**: Bài toán tối ưu mà **local optimal = global optimal** — chọn lựa chọn tốt nhất tại mỗi bước mà không cần xét lại các bước trước

---
---

## Pattern 1: Interval-based Greedy

```go
// Non-overlapping Intervals — minimum removals
// Sort by END time → greedy: luôn chọn interval kết thúc sớm nhất
sort.Slice(intervals, func(i, j int) bool {
    return intervals[i][1] < intervals[j][1]
})

end := intervals[0][1]
count := 0
for i := 1; i < len(intervals); i++ {
    if intervals[i][0] < end {
        count++  // overlap → remove this interval
    } else {
        end = intervals[i][1]  // extend to new end
    }
}
return count
```

**Insight**: Sort by end → end sớm nhất = tốt nhất (để room cho intervals sau).

---
---

## Pattern 3: Last Occurrence Greedy

```go
// Partition Labels: minimize partitions sao cho mỗi char chỉ ở 1 partition
lastOccurrence := make([]int, 26)
for i, c := range s { lastOccurrence[c-'a'] = i }

result := []int{}
start, end := 0, 0
for i, c := range s {
    end = max(end, lastOccurrence[c-'a'])  // extend end if char appears later
    if i == end {                            // all chars in current part seen
        result = append(result, end-start+1)
        start = end + 1
    }
}
return result
```

---
---

## Pattern 5: Priority-based Greedy

```go
// Hand of Straights: form groups of w consecutive cards
freq := make(map[int]int)
for _, c := range hand { freq[c]++ }

keys := []int{}
for k := range freq { keys = append(keys, k) }
sort.Ints(keys)

for _, k := range keys {
    count := freq[k]
    if count == 0 { continue }
    for i := 0; i < w; i++ {
        if freq[k+i] < count { return false }
        freq[k+i] -= count
    }
}
return true
```

---
---

## ✅ Ưu Điểm

- **O(n) hoặc O(n log n)** — thường nhanh nhất
- **O(1) hoặc O(n) space** — không cần state phức tạp
- Code đơn giản, trực quan khi đã nhận ra pattern
- Tối ưu nhất khi áp dụng được

## ❌ Nhược Điểm / Giới Hạn

- **Sai nếu áp dụng sai bài** — không có cơ chế phát hiện sai sót
- **Khó chứng minh** correctness (cần exchange argument proof)
- Không tìm được **all solutions**
- Với interview: dễ bị interviewer hỏi "tại sao greedy đúng ở đây?"

---
---

## Bài Tiêu Biểu

| Bài | Greedy choice | Why it works |
|-----|--------------|-------------|
| Jump Game I | `maxReach >= n-1` | Track furthest reachable |
| Jump Game II | Jump to max reach at boundary | Minimum decisions |
| Non-overlapping Intervals | Sort by end, keep earliest | End early = more room |
| Partition Labels | Track last occurrence | Extend until all seen |
| Gas Station | Reset when tank < 0 | Negative prefix never helps |
| Valid Parenthesis String | Track min/max open count | Range of valid opens |
| Merge Triplets | Only accept if ≤ target | Never overshoot |

---
