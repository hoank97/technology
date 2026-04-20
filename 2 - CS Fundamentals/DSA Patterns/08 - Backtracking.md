---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 08 — Backtracking

> **Giải quyết**: Tìm **tất cả** solutions thỏa điều kiện (combinations, permutations, subsets, paths) bằng cách thử từng lựa chọn và undo nếu không thoả — "controlled brute force"

---

## Bài Toán Giải Quyết

Backtracking dùng khi:
1. **Combinations**: Chọn k phần tử từ n, không quan tâm thứ tự
2. **Permutations**: Sắp xếp n phần tử theo mọi thứ tự
3. **Subsets**: Mọi tập con của một tập
4. **Grid/Graph paths**: Tìm đường đi thỏa ràng buộc
5. **Constraint satisfaction**: N-Queens, Sudoku

**Core insight**: Không khác brute force về complexity, nhưng **pruning** cắt bỏ sớm các nhánh không thể có solution → thực tế nhanh hơn nhiều.

```
Backtracking = DFS + Pruning + Undo
```

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

## Biến Thể

### 1. Subsets (không reuse, thứ tự không quan trọng)

```go
func subsets(nums []int) [][]int {
    result := [][]int{}
    var bt func(start int, curr []int)
    bt = func(start int, curr []int) {
        result = append(result, append([]int{}, curr...))  // add at every node
        for i := start; i < len(nums); i++ {
            bt(i+1, append(curr, nums[i]))
        }
    }
    bt(0, nil)
    return result
}
```

### 2. Combinations (chọn đúng k)

```go
// Combination Sum II — có duplicates trong input
sort.Ints(candidates)
var bt func(start int, curr []int, remaining int)
bt = func(start int, curr []int, remaining int) {
    if remaining == 0 { result = append(result, append([]int{}, curr...)); return }
    if remaining < 0 { return }  // pruning

    for i := start; i < len(candidates); i++ {
        if i > start && candidates[i] == candidates[i-1] { continue }  // dedup
        bt(i+1, append(curr, candidates[i]), remaining-candidates[i])
    }
}
```

### 3. Permutations (reuse không cho, thứ tự quan trọng)

```go
used := make([]bool, len(nums))
var bt func(curr []int)
bt = func(curr []int) {
    if len(curr) == len(nums) { result = append(result, append([]int{}, curr...)); return }
    for i := 0; i < len(nums); i++ {
        if used[i] { continue }
        used[i] = true
        bt(append(curr, nums[i]))
        used[i] = false
    }
}
```

### 4. Grid Backtracking (Word Search)

```go
var dfs func(r, c, idx int) bool
dfs = func(r, c, idx int) bool {
    if idx == len(word) { return true }
    if r < 0 || r >= rows || c < 0 || c >= cols { return false }
    if board[r][c] != word[idx] { return false }

    temp := board[r][c]
    board[r][c] = '#'  // mark visited (backtrack trick)

    found := dfs(r+1,c,idx+1) || dfs(r-1,c,idx+1) ||
             dfs(r,c+1,idx+1) || dfs(r,c-1,idx+1)

    board[r][c] = temp  // restore
    return found
}
```

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

## Dedup Strategies

```go
// 1. Sort + skip adjacent duplicates
sort.Ints(nums)
for i := start; i < len(nums); i++ {
    if i > start && nums[i] == nums[i-1] { continue }
    // ...
}

// 2. Use set to track choices in current level
used := make(map[int]bool)
for i := start; i < len(nums); i++ {
    if used[nums[i]] { continue }
    used[nums[i]] = true
    // ...
}
```

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

## ✅ Ưu Điểm

- **Tìm ALL solutions** — không cách nào khác làm được exhaustive search
- **Pruning** cắt bỏ sớm → thực tế nhanh hơn exhaustive brute force (dù worst case y nhau)
- Code structure rõ ràng: choose → recurse → unchoose
- Linh hoạt: thêm constraint bằng cách thêm pruning condition

## ❌ Nhược Điểm / Giới Hạn

- **Exponential time worst case** — O(2^n) subsets, O(n!) permutations
- **Không scale** với n lớn (n > 20 là đã slow với permutations)
- Dễ quên **copy slice** khi save result → shared backing array bug
- Dễ quên **undo** → state bị toxic
- **Stack depth**: n layers deep → stack overflow nếu n lớn

---

## Complexity

| Problem | Time | Space |
|---------|------|-------|
| Subsets | O(2^n) | O(n) |
| Combinations (n choose k) | O(n^k / k!) | O(k) |
| Permutations | O(n! × n) | O(n) |
| Grid word search | O(4^(m×n)) | O(m×n) |

---

## Trade-off vs DP

| | Backtracking | DP |
|---|---|---|
| **Output** | All solutions | Optimal / count |
| **Overlapping subproblems** | ❌ (explores many times) | ✅ (memoize) |
| **Count solutions** | BT (slow) | DP (faster if overlapping) |
| **Enumerate solutions** | ✅ Only option | ❌ |

> Nếu chỉ cần **count** hoặc **optimal** → DP. Nếu cần **liệt kê** → Backtracking.

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

## 📌 Tóm tắt

```
Backtracking
│
├── Khi nào
│   ├── Cần ALL solutions (tất cả combinations/permutations)
│   ├── Constraint satisfaction (N-Queens, Sudoku)
│   └── Grid path enumeration
│
├── Template: Choose → Recurse → Unchoose
│   ├── start: tránh reuse (combinations)
│   ├── i (same): allow reuse (Combination Sum I)
│   └── used[]: permutations
│
├── Dedup: Sort + skip adjacent (i > start && nums[i]==nums[i-1])
│
├── Pruning: thêm condition để return sớm
│   └── → Thực tế nhanh hơn brute force
│
├── ⚠️ Luôn COPY slice khi save result
│
├── ✅ Duy nhất có thể enumerate all solutions
└── ❌ O(2^n) / O(n!) — không dùng khi n lớn
    → vs DP: nếu chỉ count/optimal → dùng DP
```

## Tags

#backtracking #combinations #permutations #dfs #pruning #interview-prep
