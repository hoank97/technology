---
type: concept
status: complete
date_created: 2026-04-21
tags: [cs, frequency, fundamentals, hash-map, hash-set, interview-prep, lookup]
---
parent:: [[00 - DSA Patterns]]

# 03 — Hash Map & Hash Set

> **Giải quyết**: Lookup, insert, delete O(1) average — đánh đổi space để loại bỏ vòng lặp tìm kiếm O(n)

---
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
---

## Trade-off vs Alternatives

| Approach | Time | Space | Khi dùng |
|----------|------|-------|----------|
| **Hash Map** | O(1) avg | O(n) | General lookup, no order needed |
| Sorted Array + Binary Search | O(log n) lookup | O(1) extra | Memory constrained, data already sorted |
| Two Pointers | O(n) total | O(1) | Sorted, pair/triplet only |
| Bucket Sort/Count Array | O(n) | O(k) | Keys are bounded integers [0, k) |

---
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
