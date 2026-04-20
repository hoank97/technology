---
type: concept
status: complete
date_created: 2026-04-21
tags: [bit-manipulation, bitmask, cs, fundamentals, interview-prep, xor]
---
parent:: [[00 - DSA Patterns]]

# 17 — Bit Manipulation

> **Giải quyết**: Thao tác trực tiếp trên **binary representation** — thường cho phép O(1) space và tăng tốc đáng kể các bài toán set, XOR, counting

---
---

## Bit Operators

```
& (AND):  1&1=1, 1&0=0    | "Mask" — giữ bits cụ thể
| (OR):   1|0=1, 0|0=0    | "Set" — bật bit
^ (XOR):  1^1=0, 1^0=1    | "Toggle" — self-inverse
~ (NOT):  ~1=0, ~0=1      | "Flip all bits"
<< n:     left shift n     | Multiply by 2^n
>> n:     right shift n    | Divide by 2^n (arithmetic)
```

---
---

## Pattern 1: XOR — Find Single Number

```go
// XOR properties:
//   a ^ a = 0  (self-cancel)
//   a ^ 0 = a  (identity)
//   XOR is commutative and associative

// Single Number: find element appearing odd times
result := 0
for _, n := range nums {
    result ^= n  // all pairs cancel, single remains
}
return result

// XOR swap (no temp variable)
a ^= b
b ^= a
a ^= b
```

---
---

## Pattern 3: Missing Number

```go
// XOR all indices + all nums → pairs cancel, missing remains
result := len(nums)
for i, n := range nums {
    result ^= i ^ n
}
return result

// Alternative: math
// sum = n*(n+1)/2 - sum(nums)
```

---
---

## Pattern 5: Sum Without + (Add Two Integers)

```go
// a + b = XOR (sum without carry) + AND<<1 (carry)
// Repeat until no carry
func getSum(a, b int) int {
    for b != 0 {
        carry := (a & b) << 1  // carry bits
        a = a ^ b              // sum without carry
        b = carry
    }
    return a
}
```

---
---

## Pattern 7: Hamming Distance / Weight

```go
// Number of differing bits between x and y
func hammingDistance(x, y int) int {
    xor := x ^ y
    count := 0
    for xor > 0 {
        count += xor & 1
        xor >>= 1
    }
    return count
    // or: return bits.OnesCount(uint(x ^ y))
}
```

---
---

## ✅ Ưu Điểm

- **O(1) space** cho hầu hết tricks
- **O(1) time** cho single operations
- XOR tricks elegant và không cần extra memory
- Bitmask DP: giải bài O(2^n × n) thay vì O(n!) backtracking

## ❌ Nhược Điểm / Giới Hạn

- **Không intuitive**: code khó đọc, khó debug
- **Platform-specific**: signed int behavior với `>>` (arithmetic vs logical shift)
- **Go Int size**: 64-bit → cẩn thận với `1 << 32` overflow
- Bitmask DP chỉ dùng được với **n ≤ 20** (2^20 ≈ 10^6)

---
---

## Trade-off vs Alternatives

| Problem | Bit Trick | Alternative |
|---------|-----------|-------------|
| Find single number | XOR, O(1) space | Hash map O(n) space |
| Count bits | Brian Kernighan O(k) | lookup table O(1) |
| All subsets enumerate | Bitmask O(2^n) | Backtracking O(2^n) |
| Missing number | XOR O(1) space | Sort O(n log n) / Math |
| Power of 2 | n&(n-1)==0, O(1) | Loop O(log n) |

---
---

## 📌 Tóm tắt

```
Bit Manipulation
│
├── Operators: & | ^ ~ << >>
│
├── Essential tricks
│   ├── n & (n-1): remove lowest set bit / check power of 2
│   ├── n & (-n): isolate lowest set bit
│   ├── a ^ a = 0: XOR self-cancel
│   └── a ^ 0 = a: XOR identity
│
├── Patterns
│   ├── XOR: find single/missing (O(1) space)
│   ├── OnesCount: Brian Kernighan / math/bits
│   ├── Counting Bits DP: dp[i] = dp[i>>1] + i&1
│   ├── Bitmask: enumerate 2^n subsets
│   └── Add w/o +: XOR + carry loop
│
├── ✅ O(1) space, elegant for specific problems
└── ❌ Hard to read, careful with overflow, n≤20 for bitmask DP
```
