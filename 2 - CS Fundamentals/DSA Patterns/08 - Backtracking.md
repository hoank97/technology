---
type: concept
status: complete
date_created: 2026-04-21
tags: [backtracking, combinations, cs, dfs, fundamentals, interview-prep, permutations, pruning]
---
parent:: [[00 - DSA Patterns]]

# 08 — Backtracking

> **Giải quyết**: Tìm **tất cả** solutions thỏa điều kiện (combinations, permutations, subsets, paths) bằng cách thử từng lựa chọn và undo nếu không thoả — "controlled brute force"

---
---

## Template Chuẩn

```go
var result [][]int

func backtrack(start int, current []int, /* other state */) {
    // 1. Base case — valid complete solution
    if len(current) == k {
        result = append(result, append([]int{}, current...))  // COPY!
        return
    }

    // 2. Try each choice
    for i := start; i < len(nums); i++ {
        // 3. Pruning — skip invalid choices early
        if shouldPrune(i, current) { continue }

        // 4. Choose
        current = append(current, nums[i])

        // 5. Recurse
        backtrack(i+1, current)  // i+1: no reuse; i: allow reuse

        // 6. Unchoose (backtrack)
        current = current[:len(current)-1]
    }
}
```

> **Critical**: `append([]int{}, current...)` — phải copy slice, không append trực tiếp (shared backing array).

---
---

## Nhận Ra Pattern

| Signal | Backtracking type |
|--------|------------------|
| "all combinations/subsets" | Subset/Combination BT |
| "all permutations" | Permutation BT |
| "generate valid parentheses" | Build string BT |
| "find path in grid", "word search" | Grid DFS BT |
| "N-Queens", "Sudoku" | Constraint satisfaction BT |
| "partition into groups" | Partition BT |

---
---

## Pruning Examples

```go
// Prune khi remaining < 0 (Combination Sum)
if remaining < 0 { return }

// Prune khi không đủ phần tử để đạt k (Combinations)
if len(current) + (len(nums)-i) < k { return }

// Prune khi chuỗi hiện tại đã invalid (Generate Parentheses)
if open < 0 || close < 0 || open > n { return }
```

---
---

## Complexity

| Problem | Time | Space |
|---------|------|-------|
| Subsets | O(2^n) | O(n) |
| Combinations (n choose k) | O(n^k / k!) | O(k) |
| Permutations | O(n! × n) | O(n) |
| Grid word search | O(4^(m×n)) | O(m×n) |

---
---

## Bài Tiêu Biểu

| Bài | Pattern | Key |
|-----|---------|-----|
| Subsets I | BT at every node | Add result at every call |
| Subsets II | BT + dedup | Sort + skip duplicate |
| Combination Sum I | BT, can reuse | Next call: i (not i+1) |
| Combination Sum II | BT + dedup | Sort + skip, i+1 |
| Permutations | BT + used[] | No start index, use `used` |
| Word Search | Grid BT | Inplace mark '#' |
| N-Queens | Constraint BT | Track col, diag1, diag2 sets |

---
