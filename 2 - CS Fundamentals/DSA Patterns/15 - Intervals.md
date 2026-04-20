---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 15 — Intervals

> **Giải quyết**: Bài toán về **ranges/intervals** — merge overlaps, find gaps, minimum coverage, scheduling — thường bắt đầu bằng **sort**

---

## Bài Toán Giải Quyết

Interval problems khi input là các đoạn `[start, end]`:
1. **Merge**: Gộp overlapping intervals
2. **Insert**: Thêm interval vào sorted list
3. **Minimum coverage**: Ít intervals nhất để cover range
4. **Schedule**: Đếm rooms cần thiết, detect conflict
5. **Remove to make non-overlapping**: Minimum removals

**Core insight**: Hầu hết interval problems yêu cầu **sort by start** (hoặc end) trước.

---

## Pattern 1: Merge Intervals

```go
// Sort by start → scan and merge
sort.Slice(intervals, func(i, j int) bool {
    return intervals[i][0] < intervals[j][0]
})

result := [][]int{intervals[0]}
for i := 1; i < len(intervals); i++ {
    last := result[len(result)-1]
    cur := intervals[i]

    if cur[0] <= last[1] {           // overlap
        last[1] = max(last[1], cur[1])  // extend end
    } else {
        result = append(result, cur)    // no overlap → new interval
    }
}
return result
```

---

## Pattern 2: Insert Interval

```go
// Insert new interval into sorted non-overlapping list
result := [][]int{}
i := 0

// 1. Add all intervals BEFORE new interval
for i < len(intervals) && intervals[i][1] < newInterval[0] {
    result = append(result, intervals[i]); i++
}

// 2. Merge all overlapping intervals with new
for i < len(intervals) && intervals[i][0] <= newInterval[1] {
    newInterval[0] = min(newInterval[0], intervals[i][0])
    newInterval[1] = max(newInterval[1], intervals[i][1])
    i++
}
result = append(result, newInterval)

// 3. Add remaining intervals AFTER
for i < len(intervals) {
    result = append(result, intervals[i]); i++
}
return result
```

---

## Pattern 3: Meeting Rooms II (Min Rooms)

```go
// Minimum meeting rooms = max concurrent meetings at any time
// Sort starts and ends separately → two-pointer sweep
starts := make([]int, len(intervals))
ends := make([]int, len(intervals))
for i, iv := range intervals {
    starts[i] = iv[0]; ends[i] = iv[1]
}
sort.Ints(starts); sort.Ints(ends)

rooms, endPtr := 0, 0
for s := range starts {
    if starts[s] < ends[endPtr] {
        rooms++  // new meeting starts before earliest end → need new room
    } else {
        endPtr++  // one meeting ended → reuse room
    }
}
return rooms

// Alternative: min-heap of end times
```

---

## Pattern 4: Non-overlapping Intervals (Minimum Removal)

```go
// Sort by END time → greedy: keep interval with earliest end
sort.Slice(intervals, func(i, j int) bool {
    return intervals[i][1] < intervals[j][1]
})

end := intervals[0][1]
removals := 0
for i := 1; i < len(intervals); i++ {
    if intervals[i][0] < end {
        removals++  // overlap → remove (keep the one with earlier end)
    } else {
        end = intervals[i][1]
    }
}
return removals
```

---

## Pattern 5: Minimum Interval to Include Each Query

```go
// For each query q, find minimum length interval containing q
// Sort intervals + queries, sweep with heap
sort.Slice(intervals, func(i, j int) bool {
    return intervals[i][0] < intervals[j][0]
})

queries := make([][]int, len(qs))  // {value, original_index}
for i, q := range qs { queries[i] = []int{q, i} }
sort.Slice(queries, func(i, j int) bool { return queries[i][0] < queries[j][0] })

result := make([]int, len(qs))
h := &MinHeapByLength{}  // {length, end}
i := 0

for _, q := range queries {
    // Add all intervals starting ≤ q[0]
    for i < len(intervals) && intervals[i][0] <= q[0] {
        heap.Push(h, [2]int{intervals[i][1]-intervals[i][0]+1, intervals[i][1]})
        i++
    }
    // Remove intervals that ended before q[0]
    for h.Len() > 0 && (*h)[0][1] < q[0] { heap.Pop(h) }

    if h.Len() > 0 { result[q[1]] = (*h)[0][0] } else { result[q[1]] = -1 }
}
return result
```

---

## Overlap Logic

```
Interval A = [a1, a2]
Interval B = [b1, b2]

Overlap condition:
  a1 <= b2 AND b1 <= a2
  ↔ NOT (a2 < b1 OR b2 < a1)

Merge condition (after sort by start):
  B.start <= A.end  (B starts before A ends)

Contained condition:
  a1 <= b1 AND b2 <= a2
```

---

## Nhận Ra Pattern

| Signal | Interval technique |
|--------|------------------|
| "merge overlapping" | Sort start + scan |
| "insert new interval" | 3-phase: before, merge, after |
| "minimum rooms/resources" | Sort starts+ends separately |
| "minimum removal to non-overlap" | Sort by end + greedy |
| "meeting schedule conflict" | Sort start, check overlap |
| "cover range with minimum intervals" | Greedy sort |

---

## ✅ Ưu Điểm

- **O(n log n)** — sort + O(n) scan
- Pattern rõ ràng: sort → scan → merge/count
- Greedy thường đúng cho interval scheduling

## ❌ Nhược Điểm / Giới Hạn

- **Boundary conditions**: `<=` vs `<` khi check overlap — dễ sai
- Interval với start = end (point) cần handle riêng
- "Minimum Interval to Include Each Query" cần heap → phức tạp hơn

---

## Bài Tiêu Biểu

| Bài | Pattern | Sort by |
|-----|---------|---------|
| Meeting Rooms I | Check any overlap | start |
| Meeting Rooms II | Count concurrent | starts + ends separate |
| Merge Intervals | Merge overlapping | start |
| Insert Interval | 3-phase insert | Already sorted |
| Non-overlapping Intervals | Min removal | end (greedy) |
| Min Interval for Each Query | Heap + sweep | start + offline queries |

---

## 📌 Tóm tắt

```
Intervals
│
├── Always: Sort first (by start or end)
│
├── Patterns
│   ├── Merge: sort start → scan, extend end
│   ├── Insert: 3-phase (before / overlap / after)
│   ├── Min rooms: sort starts+ends → two-pointer
│   ├── Min removal: sort end → greedy keep earliest end
│   └── Query range: sort + heap + offline
│
├── Overlap: B.start <= A.end (after sort by start)
│
├── ✅ O(n log n), clear pattern
└── ❌ Boundary conditions (< vs <=) — careful!
```

## Tags

#intervals #scheduling #merge #sweep-line #interview-prep
