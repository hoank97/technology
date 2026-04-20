---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 14 — Greedy

> **Giải quyết**: Bài toán tối ưu mà **local optimal = global optimal** — chọn lựa chọn tốt nhất tại mỗi bước mà không cần xét lại các bước trước

---

## Bài Toán Giải Quyết

Greedy = đưa ra quyết định ngay lập tức, không bao giờ undo. **Không phải lúc nào cũng đúng** — chỉ đúng khi bài toán có **Greedy Choice Property** và **Optimal Substructure**.

**Greedy Choice Property**: Có một lựa chọn "locally optimal" mà luôn là một phần của globally optimal solution.

**Khi nào greedy sai**: Coin change với coins tùy ý (coins=[1,3,4], target=6: greedy chọn 4+1+1=3 coins, optimal là 3+3=2 coins).

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

## Pattern 2: Jump / Reach

```go
// Jump Game II — minimum jumps to reach end
maxReach, jumps, currentEnd := 0, 0, 0

for i := 0; i < len(nums)-1; i++ {
    maxReach = max(maxReach, i+nums[i])  // furthest we can reach from [0..currentEnd]
    if i == currentEnd {                  // must jump at end of current range
        jumps++
        currentEnd = maxReach
    }
}
return jumps
```

**Insight**: Tại mỗi "jump boundary", luôn chọn điểm đến xa nhất → minimize jumps.

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

## Pattern 4: Gas Station / Circular

```go
// Gas Station: find starting position
// Key insight: nếu total gas >= total cost → solution exists
// Nếu current tank < 0 → reset và thử bắt đầu từ i+1
tank, total, start := 0, 0, 0
for i := range gas {
    diff := gas[i] - cost[i]
    tank += diff
    total += diff
    if tank < 0 {
        start = i + 1
        tank = 0
    }
}
if total < 0 { return -1 }
return start
```

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

## Nhận Ra Pattern — Và Kiểm Tra Greedy Correctness

### Checklist để dùng Greedy

```
1. Có thể sort input theo tiêu chí nào đó không?
2. Quyết định tại mỗi bước có "locally obvious" không?
3. Quyết định đó không bao giờ cần undo không?
4. Có thể chứng minh greedy choice ≠ miss optimal solution?

→ Nếu YES cho cả 4 → Greedy an toàn
→ Nếu không chắc → dùng DP (đúng hơn, chậm hơn)
```

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

## Trade-off: Greedy vs DP

| | Greedy | DP |
|---|---|---|
| **Speed** | ✅ O(n) / O(n log n) | ⚠️ O(n²) / O(n×m) |
| **Space** | ✅ O(1) / O(n) | ⚠️ O(n) / O(n²) |
| **Correctness** | ⚠️ Only when provable | ✅ Always correct |
| **Proof** | Hard (exchange argument) | Obvious (recurrence) |
| **Use case** | Intervals, reach, scheduling | Knapsack, sequences |

**Heuristic**: Nếu bài có "minimum number of X to cover Y" hoặc "maximum coverage" → thử Greedy trước, fallback DP nếu sai.

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

## 📌 Tóm tắt

```
Greedy
│
├── Khi nào dùng
│   ├── Local optimal = global optimal (provable)
│   ├── "Minimum steps/pieces/coverage"
│   └── Interval scheduling: sort by end
│
├── Patterns
│   ├── Sort by end: Non-overlapping intervals
│   ├── Track max reach: Jump Game
│   ├── Last occurrence: Partition Labels
│   ├── Reset on negative: Gas Station
│   └── Process sorted + validate: Hand of Straights
│
├── Correctness check
│   ├── Sort → obvious local choice → never undo?
│   └── Không chắc → dùng DP (slower but correct)
│
├── ✅ O(n) or O(n log n), simple code
└── ❌ Sai nếu bài không có greedy property
    → Always prove or use DP as fallback
```

## Tags

#greedy #intervals #scheduling #optimization #interview-prep
