---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 03 — Hash Map & Hash Set

> **Giải quyết**: Lookup, insert, delete O(1) average — đánh đổi space để loại bỏ vòng lặp tìm kiếm O(n)

---

## Bài Toán Giải Quyết

Khi cần:
- **"Đã thấy X chưa?"** — membership check
- **"X xuất hiện bao nhiêu lần?"** — frequency count
- **"Complement của X là Y = target - X"** — complement lookup
- **"Group các phần tử theo key"** — grouping
- **"Cache kết quả đã tính"** — memoization

Không có Hash Map: O(n) search per lookup → toàn bài O(n²). Với Hash Map: O(1) lookup → O(n).

---

## Cơ Chế Nội Bộ

```
Hash Map = Array of buckets
key → hash(key) → bucket index → linked list (collision)

Hash("apple") → 42 → bucket[42] → [("apple", 1)]
Hash("banana") → 42 → bucket[42] → [("apple", 1), ("banana", 2)]  ← collision

Thực tế Go: dùng hash + open addressing, tự resize khi load factor > 0.65
```

**Load Factor**: `n_elements / n_buckets`. Khi vượt ngưỡng → resize (O(n)) → amortized O(1).

---

## Các Pattern

### 1. Two Sum — Complement Lookup

```go
// Thay vì: for i; for j: check a[i]+a[j]==target → O(n²)
// Dùng: lưu index của từng số → lookup complement trong O(1)
seen := make(map[int]int) // val → index
for i, n := range nums {
    if j, ok := seen[target-n]; ok {
        return []int{j, i}
    }
    seen[n] = i
}
```

### 2. Frequency Count

```go
// Valid Anagram, Group Anagrams
freq := make(map[rune]int)
for _, c := range s {
    freq[c]++
}
for _, c := range t {
    freq[c]--
    if freq[c] < 0 { return false }
}
return true
```

### 3. Group By Key

```go
// Group Anagrams: key = sorted string
groups := make(map[string][]string)
for _, word := range strs {
    key := sortString(word)   // "eat" → "aet"
    groups[key] = append(groups[key], word)
}
```

### 4. Seen/Visited Set

```go
// Contains Duplicate, Cycle Detection
seen := make(map[int]bool)
for _, n := range nums {
    if seen[n] { return true }
    seen[n] = true
}
return false
```

### 5. Memoization (Top-Down DP)

```go
var memo map[int]int

func fib(n int) int {
    if n <= 1 { return n }
    if v, ok := memo[n]; ok { return v }
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
}
```

---

## Nhận Ra Pattern

| Signal | Pattern |
|--------|---------|
| "two sum", "find pair with sum" | Complement lookup |
| "anagram", "frequency", "count" | Freq map |
| "duplicate", "unique", "seen" | Hash Set |
| "group by", "categorize" | Map[key][]values |
| "LRU cache", "O(1) get/put" | Map + Doubly Linked List |
| "longest consecutive" | Set + sequence expansion |

---

## ✅ Ưu Điểm

- **O(1) average** cho insert/delete/lookup
- **Đơn giản**: thường chỉ 1-2 dòng để setup
- Không cần sort (so với Two Pointers)
- Flexible key type: int, string, struct (nếu comparable)

## ❌ Nhược Điểm / Giới Hạn

- **O(n) extra space** — đánh đổi space lấy time
- **O(n) worst case** khi nhiều hash collision (hiếm với good hash function)
- **Không ordered** — nếu cần sorted order phải dùng `sort.Slice` hoặc BST
- **Go map iteration không deterministic** (random order)
- Không thread-safe — dùng `sync.Map` hoặc `sync.RWMutex` khi concurrent

---

## Trade-off vs Alternatives

| Approach | Time | Space | Khi dùng |
|----------|------|-------|----------|
| **Hash Map** | O(1) avg | O(n) | General lookup, no order needed |
| Sorted Array + Binary Search | O(log n) lookup | O(1) extra | Memory constrained, data already sorted |
| Two Pointers | O(n) total | O(1) | Sorted, pair/triplet only |
| Bucket Sort/Count Array | O(n) | O(k) | Keys are bounded integers [0, k) |

---

## Đặc Biệt: Longest Consecutive Sequence

Ví dụ điển hình kết hợp Set + thông minh tránh duplicate work:

```go
// O(n) không cần sort — key insight: chỉ start sequence từ phần tử đầu tiên
numSet := make(map[int]bool)
for _, n := range nums { numSet[n] = true }

longest := 0
for n := range numSet {
    if !numSet[n-1] {   // n là điểm bắt đầu sequence
        length := 1
        for numSet[n+length] { length++ }
        longest = max(longest, length)
    }
}
```

---

## Bài Tiêu Biểu

| Bài | Pattern | Key |
|-----|---------|-----|
| Two Sum | Complement lookup | `target - n` |
| Valid Anagram | Freq count | char → count |
| Group Anagrams | Group by key | sorted word as key |
| Longest Consecutive Sequence | Set + start detection | skip non-starts |
| Top K Frequent Elements | Freq map + heap/bucket | count → elements |
| LRU Cache | Map + Doubly Linked List | O(1) get+put |

---

## 📌 Tóm tắt

```
Hash Map & Hash Set
│
├── Khi nào
│   ├── Lookup O(1): complement, seen, membership
│   ├── Frequency count: anagram, top-K
│   ├── Group by key: anagram groups
│   └── Memoization: cache subproblem results
│
├── Internals
│   ├── hash(key) → bucket → amortized O(1)
│   └── Resize khi load factor > threshold
│
├── ✅ O(1) avg time, simple code
├── ❌ O(n) space, unordered, not thread-safe
│
└── vs Alternatives
    ├── Two Pointers: sorted, O(1) space
    ├── Binary Search: sorted, O(log n) time
    └── Bucket Sort: bounded integer keys
```

## Tags

#hash-map #hash-set #frequency #lookup #interview-prep
