---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 10 — Dynamic Programming (2D)

> **Giải quyết**: Bài toán tối ưu/đếm liên quan đến **2 sequences** (strings, arrays) hoặc **grid** — state phụ thuộc vào 2 chiều

---

## Bài Toán Giải Quyết

2D DP xuất hiện khi:
1. **Hai chuỗi**: So sánh, edit, match giữa string s và t
2. **Grid path**: Tìm đường đi tối ưu trong ma trận
3. **Interval DP**: Tính trên đoạn [i, j] (palindrome, burst balloons)
4. **Knapsack 2D**: Weight + value, 2 constraints

**State**: `dp[i][j]` = answer cho subproblem liên quan đến `s1[0..i]` và `s2[0..j]` (hoặc cell (i,j)).

---

## Pattern 1: Two Strings — LCS Family

### Longest Common Subsequence

```go
// dp[i][j] = LCS length của s1[0..i-1] và s2[0..j-1]
dp := make([][]int, m+1)
for i := range dp { dp[i] = make([]int, n+1) }

for i := 1; i <= m; i++ {
    for j := 1; j <= n; j++ {
        if s1[i-1] == s2[j-1] {
            dp[i][j] = dp[i-1][j-1] + 1      // match: extend LCS
        } else {
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])  // skip one char
        }
    }
}
return dp[m][n]
```

### Edit Distance (Levenshtein)

```go
// dp[i][j] = min ops để convert word1[0..i-1] → word2[0..j-1]
// Ops: insert, delete, replace
for i := 1; i <= m; i++ {
    for j := 1; j <= n; j++ {
        if word1[i-1] == word2[j-1] {
            dp[i][j] = dp[i-1][j-1]           // no op needed
        } else {
            dp[i][j] = 1 + min(
                dp[i-1][j],    // delete from word1
                dp[i][j-1],    // insert into word1
                dp[i-1][j-1],  // replace
            )
        }
    }
}
```

### Distinct Subsequences

```go
// dp[i][j] = số cách t[0..j-1] xuất hiện trong s[0..i-1] as subsequence
for i := 1; i <= m; i++ {
    for j := 1; j <= n; j++ {
        dp[i][j] = dp[i-1][j]                   // không dùng s[i-1]
        if s[i-1] == t[j-1] {
            dp[i][j] += dp[i-1][j-1]            // dùng s[i-1] match với t[j-1]
        }
    }
}
```

---

## Pattern 2: Grid Path

```go
// Unique Paths: từ (0,0) → (m-1,n-1), chỉ đi right/down
dp := make([][]int, m)
for i := range dp { dp[i] = make([]int, n) }

for i := 0; i < m; i++ { dp[i][0] = 1 }  // first col
for j := 0; j < n; j++ { dp[0][j] = 1 }  // first row

for i := 1; i < m; i++ {
    for j := 1; j < n; j++ {
        dp[i][j] = dp[i-1][j] + dp[i][j-1]
    }
}
return dp[m-1][n-1]
```

### Grid với obstacles / costs

```go
// Minimum path sum
for i := 0; i < m; i++ {
    for j := 0; j < n; j++ {
        if i == 0 && j == 0 { continue }
        up, left := math.MaxInt, math.MaxInt
        if i > 0 { up = dp[i-1][j] }
        if j > 0 { left = dp[i][j-1] }
        dp[i][j] = grid[i][j] + min(up, left)
    }
}
```

---

## Pattern 3: Interval DP

```go
// Burst Balloons: chọn thứ tự nổ để maximize coins
// dp[i][j] = max coins từ balloons giữa i và j (exclusive)
for length := 1; length <= n; length++ {
    for left := 0; left < n-length+1; left++ {
        right := left + length - 1
        for k := left; k <= right; k++ {
            // k là balloon nổ CUỐI CÙNG trong [left, right]
            dp[left][right] = max(dp[left][right],
                nums[left-1]*nums[k]*nums[right+1] +
                dp[left][k-1] + dp[k+1][right])
        }
    }
}
```

---

## Pattern 4: 2D Knapsack

```go
// Coin Change 2: số cách trả amount dùng coins (unlimited)
// dp[i][j] = số cách dùng coins[0..i-1] để đạt sum j
dp := make([][]int, len(coins)+1)
for i := range dp { dp[i] = make([]int, amount+1); dp[i][0] = 1 }

for i := 1; i <= len(coins); i++ {
    for j := 0; j <= amount; j++ {
        dp[i][j] = dp[i-1][j]                      // không dùng coin i
        if j >= coins[i-1] {
            dp[i][j] += dp[i][j-coins[i-1]]         // dùng coin i (unlimited)
        }
    }
}
// Space optimize: flatten to 1D (unbounded → iterate forward)
```

---

## Space Optimization

```go
// LCS: O(m×n) → O(n) với rolling array
prev := make([]int, n+1)
curr := make([]int, n+1)

for i := 1; i <= m; i++ {
    for j := 1; j <= n; j++ {
        if s1[i-1] == s2[j-1] {
            curr[j] = prev[j-1] + 1
        } else {
            curr[j] = max(prev[j], curr[j-1])
        }
    }
    prev, curr = curr, make([]int, n+1)
}
```

---

## Nhận Ra Pattern

| Signal | DP 2D type |
|--------|-----------|
| "two strings", "edit distance" | Two-string DP |
| "common subsequence/substring" | LCS family |
| "distinct subsequences" | Count DP on 2 strings |
| "grid", "robot paths", "min path" | Grid DP |
| "burst balloons", "matrix chain" | Interval DP |
| "coin change II" (count ways) | 2D Knapsack |
| "regular expression matching" | 2D string DP |
| "interleaving strings" | 2D DP |

---

## ✅ Ưu Điểm

- Giải chính xác các bài "2 variable" không thể 1D
- **Space optimize** thường được (O(m×n) → O(n))
- Transition thường elegant và logical

## ❌ Nhược Điểm / Giới Hạn

- **O(m×n) time và space** — với m,n ~ 10^3 thì 10^6 operations (vẫn OK); 10^4 thì 10^8 (too slow)
- **Harder to define state** cho bài phức tạp (interval DP)
- **Transition order** quan trọng: phải fill đúng thứ tự để có dependencies

---

## Trade-off: 2D DP vs Recursion+Memo

| | 2D DP (bottom-up) | Recursion+Memo (top-down) |
|---|---|---|
| **Code** | Harder to write | Closer to natural recursion |
| **Performance** | Faster (no overhead) | Slightly slower |
| **Space** | Optimizable | O(m×n) memo dict |
| **Subproblems** | All computed | Only needed ones |

---

## Bài Tiêu Biểu

| Bài | Pattern | Key transition |
|-----|---------|---------------|
| Longest Common Subsequence | Two-string | match → diag+1, else max(up,left) |
| Edit Distance | Two-string | match → diag, else 1+min(3 dirs) |
| Distinct Subsequences | Two-string | dp[i][j] = dp[i-1][j] + (match?dp[i-1][j-1]) |
| Unique Paths | Grid | dp[i][j] = dp[i-1][j] + dp[i][j-1] |
| Coin Change II | 2D Knapsack | count ways (forward iteration) |
| Burst Balloons | Interval DP | k = last balloon in interval |
| Interleaving String | 2D DP | dp[i][j] = from i-1 or j-1 |
| Regular Expression | 2D DP | handle `*` with 0 or 1+ prev |

---

## 📌 Tóm tắt

```
Dynamic Programming 2D
│
├── Khi nào
│   ├── Two strings: compare, edit, match
│   ├── Grid: path counting, min cost
│   ├── Interval [i,j]: burst balloons
│   └── 2D Knapsack: 2 constraints
│
├── State: dp[i][j] = subproblem(s1[0..i], s2[0..j]) or cell(i,j)
│
├── Patterns
│   ├── LCS: match→diag+1, else max(up,left)
│   ├── Edit Distance: match→diag, else 1+min(3dirs)
│   ├── Grid: dp[i][j] = dp[i-1][j] + dp[i][j-1]
│   └── Interval: fix length outer, endpoints inner
│
├── Space: O(m×n) → O(n) rolling array
│
└── ✅ Exact for 2-variable problems
    ❌ O(m×n) — slow when m,n > 10^4
```

## Tags

#dynamic-programming #dp-2d #lcs #edit-distance #grid #interview-prep
