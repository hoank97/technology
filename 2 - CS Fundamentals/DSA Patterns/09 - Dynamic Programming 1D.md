---
type: concept
status: complete
date_created: 2026-04-21
tags: [cs, dp-1d, dynamic-programming, fundamentals, interview-prep, knapsack, memoization]
---
parent:: [[00 - DSA Patterns]]

# 09 — Dynamic Programming (1D)

> **Giải quyết**: Bài toán **tối ưu hoặc đếm** có **overlapping subproblems** và **optimal substructure** — tính một lần, lưu lại, dùng nhiều lần

---
---

## Framework 4 Bước

```
1. DEFINE STATE:  dp[i] = answer cho subproblem "ending at / using index i"
2. BASE CASE:     dp[0] hoặc dp[1] = giá trị rõ ràng
3. TRANSITION:    dp[i] = f(dp[i-1], dp[i-2], ...) — recurrence relation
4. ANSWER:        dp[n] hoặc max/min(dp) tùy bài
```

---
---

## Nhận Ra Pattern

| Signal | DP type |
|--------|---------|
| "min/max ways", "can achieve" | Linear DP |
| "climbing stairs", "jump game" | Fibonacci / linear |
| "rob houses", "skip adjacent" | House Robber pattern |
| "min coins", "total ways for amount" | Unbounded Knapsack |
| "partition sum", "subset sum" | 0/1 Knapsack |
| "longest increasing subsequence" | LIS |
| "decode ways" | DP với condition |
| "stock with cooldown/fee" | State Machine DP |

---
---

## Top-down vs Bottom-up

```go
// Top-down (memoization) — thường dễ viết hơn
var memo map[int]int
var dp func(i int) int
dp = func(i int) int {
    if i <= 1 { return i }
    if v, ok := memo[i]; ok { return v }
    memo[i] = dp(i-1) + dp(i-2)
    return memo[i]
}

// Bottom-up (tabulation) — thường faster (no recursion overhead)
table := make([]int, n+1)
table[0], table[1] = 0, 1
for i := 2; i <= n; i++ {
    table[i] = table[i-1] + table[i-2]
}
```

| | Top-down | Bottom-up |
|---|---|---|
| **Code** | Closer to recursion, natural | Need figure out order |
| **Performance** | Function call overhead | Faster (no overhead) |
| **Space** | O(n) stack + memo | O(n) table, optimizable |
| **Unused subproblems** | Only computes needed | Computes all |

---
---

## Bài Tiêu Biểu

| Bài | Pattern | Key transition |
|-----|---------|---------------|
| Climbing Stairs | Fibonacci | dp[i] = dp[i-1] + dp[i-2] |
| House Robber II | Circular → 2 linear DP | Rob [0..n-2] or [1..n-1] |
| Coin Change | Unbounded Knapsack | dp[i] = min(dp[i-c]+1) ∀ coins |
| Partition Equal Subset | 0/1 Knapsack | Backward iteration |
| Word Break | Linear DP | dp[i] = any dp[j] && word[j..i] in dict |
| LIS | Quadratic DP | dp[i] = max(dp[j]+1) where nums[j]<nums[i] |
| Decode Ways | DP với condition | 1-2 digit decode |

---
