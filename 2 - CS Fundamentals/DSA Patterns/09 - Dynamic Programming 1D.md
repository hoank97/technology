---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 09 — Dynamic Programming (1D)

> **Giải quyết**: Bài toán **tối ưu hoặc đếm** có **overlapping subproblems** và **optimal substructure** — tính một lần, lưu lại, dùng nhiều lần

---

## Bài Toán Giải Quyết

Dynamic Programming (DP) = Recursion + Memoization (top-down) hoặc Tabulation (bottom-up).

Hai điều kiện phải có:
1. **Optimal substructure**: Optimal solution của bài toán lớn được xây dựng từ optimal solutions của subproblems
2. **Overlapping subproblems**: Các subproblems được giải lặp đi lặp lại → cache kết quả

**Không dùng DP khi**: Subproblems độc lập (dùng D&C như Merge Sort).

---

## Framework 4 Bước

```
1. DEFINE STATE:  dp[i] = answer cho subproblem "ending at / using index i"
2. BASE CASE:     dp[0] hoặc dp[1] = giá trị rõ ràng
3. TRANSITION:    dp[i] = f(dp[i-1], dp[i-2], ...) — recurrence relation
4. ANSWER:        dp[n] hoặc max/min(dp) tùy bài
```

---

## Các Pattern 1D

### Pattern 1: Fibonacci / Linear Dependency

```go
// Climbing Stairs: dp[i] = dp[i-1] + dp[i-2]
dp := make([]int, n+1)
dp[0], dp[1] = 1, 1
for i := 2; i <= n; i++ {
    dp[i] = dp[i-1] + dp[i-2]
}
return dp[n]

// Space optimized: chỉ cần 2 biến
prev, curr := 1, 1
for i := 2; i <= n; i++ {
    prev, curr = curr, prev+curr
}
return curr
```

### Pattern 2: House Robber (không chọn adjacent)

```go
// dp[i] = max tiền có thể lấy từ nhà 0..i
// dp[i] = max(dp[i-1], dp[i-2] + nums[i])
prev2, prev1 := 0, 0
for _, n := range nums {
    curr := max(prev1, prev2+n)
    prev2 = prev1
    prev1 = curr
}
return prev1
```

### Pattern 3: Unbounded Knapsack

```go
// Coin Change: tìm min coins để đạt amount
dp := make([]int, amount+1)
for i := range dp { dp[i] = math.MaxInt }
dp[0] = 0

for i := 1; i <= amount; i++ {
    for _, coin := range coins {
        if coin <= i && dp[i-coin] != math.MaxInt {
            dp[i] = min(dp[i], dp[i-coin]+1)
        }
    }
}
if dp[amount] == math.MaxInt { return -1 }
return dp[amount]
```

### Pattern 4: 0/1 Knapsack

```go
// Partition Equal Subset Sum: có thể đạt sum = total/2?
dp := make([]bool, target+1)
dp[0] = true

for _, num := range nums {
    // iterate BACKWARDS để tránh dùng num nhiều lần
    for j := target; j >= num; j-- {
        dp[j] = dp[j] || dp[j-num]
    }
}
return dp[target]
```

### Pattern 5: LIS (Longest Increasing Subsequence)

```go
// dp[i] = length of LIS ending at index i
dp := make([]int, len(nums))
for i := range dp { dp[i] = 1 }

for i := 1; i < len(nums); i++ {
    for j := 0; j < i; j++ {
        if nums[j] < nums[i] {
            dp[i] = max(dp[i], dp[j]+1)
        }
    }
}
// answer = max(dp)

// Optimized O(n log n): binary search + patience sorting
```

### Pattern 6: State Machine DP

```go
// Buy/Sell Stock with Cooldown: 3 states
// holding, sold (cooldown), rest
holding, sold, rest := -prices[0], 0, 0

for i := 1; i < len(prices); i++ {
    prevHolding := holding
    holding = max(holding, rest-prices[i])  // buy from rest state
    rest = max(rest, sold)                   // wait out cooldown
    sold = prevHolding + prices[i]           // sell
}
return max(sold, rest)
```

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

## ✅ Ưu Điểm

- **Exponential → Polynomial**: O(2^n) recursion → O(n) hoặc O(n²) DP
- **Chính xác**: không bỏ sót case nào (vs Greedy)
- **Count AND optimize**: cả đếm số cách lẫn tìm optimal
- Space optimization: thường compact từ O(n) → O(1)

## ❌ Nhược Điểm / Giới Hạn

- **Khó define state**: không rõ dp[i] nên biểu diễn gì → sai từ đầu
- **Transition sai thứ tự**: 0/1 knapsack phải iterate ngược, unbounded xuôi
- Không tìm được **all solutions** → dùng Backtracking
- Bài phức tạp: state space 2D/3D → O(n²/n³) memory

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

## Trade-off: DP vs Greedy vs Backtracking

| | DP | Greedy | Backtracking |
|---|---|---|---|
| **Find optimal** | ✅ | ✅ (khi applicable) | ✅ (slow) |
| **Count ways** | ✅ | ❌ | ✅ (slow) |
| **All solutions** | ❌ | ❌ | ✅ |
| **Time** | Polynomial | Linear/O(n log n) | Exponential |
| **When** | Overlapping subproblems | Local optimal = global | Must enumerate |

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

## 📌 Tóm tắt

```
Dynamic Programming 1D
│
├── Khi nào
│   ├── Overlapping subproblems + optimal substructure
│   ├── "Min/max ways", "count ways", "can achieve"
│   └── Khi Greedy không chứng minh được correctness
│
├── Framework
│   ├── 1. Define state: dp[i] = ?
│   ├── 2. Base case: dp[0] / dp[1]
│   ├── 3. Transition: dp[i] = f(dp[i-1], ...)
│   └── 4. Answer: dp[n] or max/min(dp)
│
├── Patterns
│   ├── Fibonacci: dp[i] = dp[i-1] + dp[i-2]
│   ├── House Robber: max(skip, take+prev)
│   ├── Unbounded Knapsack: iterate forward
│   ├── 0/1 Knapsack: iterate backward
│   ├── LIS: O(n²) or O(n log n)
│   └── State Machine: holding/sold/rest
│
├── Top-down vs Bottom-up
│   ├── Top-down: natural, memo dict
│   └── Bottom-up: faster, table
│
└── vs Greedy: DP correct always; Greedy only when provably optimal
    vs Backtracking: DP count/optimize; BT enumerate all
```

## Tags

#dynamic-programming #dp-1d #knapsack #memoization #interview-prep
