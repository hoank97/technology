---
type: concept
status: complete
date_created: 2026-04-21
tags: [cs, dp-2d, dynamic-programming, edit-distance, fundamentals, grid, interview-prep, lcs]
---
parent:: [[00 - DSA Patterns]]

# 10 — Dynamic Programming (2D)

> **Giải quyết**: Bài toán tối ưu/đếm liên quan đến **2 sequences** (strings, arrays) hoặc **grid** — state phụ thuộc vào 2 chiều

---
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
