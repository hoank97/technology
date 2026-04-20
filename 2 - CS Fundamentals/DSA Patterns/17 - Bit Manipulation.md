---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 17 — Bit Manipulation

> **Giải quyết**: Thao tác trực tiếp trên **binary representation** — thường cho phép O(1) space và tăng tốc đáng kể các bài toán set, XOR, counting

---

## Bài Toán Giải Quyết

Bit Manipulation dùng khi:
1. **XOR tricks**: Tìm phần tử xuất hiện lẻ lần, swap không cần temp
2. **Bit counting**: Count 1-bits, check power of 2
3. **Subset generation**: Dùng bits để enumerate subsets
4. **Bit DP**: Bitmask DP cho n ≤ 20
5. **Addition không dùng +**: Interview trick

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

## Core Bit Tricks

```go
// Check if bit i is set
(n >> i) & 1 == 1

// Set bit i
n |= (1 << i)

// Clear bit i
n &= ^(1 << i)

// Toggle bit i
n ^= (1 << i)

// Get lowest set bit
n & (-n)    // -n = ~n + 1

// Check power of 2
n > 0 && (n & (n-1)) == 0  // power of 2 has exactly 1 bit set

// Count set bits (Brian Kernighan)
count := 0
for n > 0 {
    n &= (n - 1)  // remove lowest set bit
    count++
}

// Count set bits (built-in)
import "math/bits"
bits.OnesCount(uint(n))
```

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

## Pattern 2: Count Bits — DP

```go
// Counting Bits: count 1-bits for [0..n]
dp := make([]int, n+1)
for i := 1; i <= n; i++ {
    dp[i] = dp[i>>1] + (i & 1)
    // dp[i>>1] = bits of i/2, + 1 if i is odd
}
return dp

// Alternative patterns:
// dp[i] = dp[i&(i-1)] + 1  (remove lowest bit)
```

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

## Pattern 4: Reverse Bits

```go
// Reverse bits of 32-bit unsigned integer
func reverseBits(num uint32) uint32 {
    result := uint32(0)
    for i := 0; i < 32; i++ {
        result = (result << 1) | (num & 1)
        num >>= 1
    }
    return result
}
```

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

## Pattern 6: Bitmask Subset Enumeration

```go
// Enumerate all subsets of set represented as bitmask
n := len(nums)
for mask := 0; mask < (1 << n); mask++ {
    subset := []int{}
    for i := 0; i < n; i++ {
        if mask & (1 << i) != 0 {
            subset = append(subset, nums[i])
        }
    }
    // process subset
}
// Total: 2^n subsets — same complexity as backtracking
// Cleaner code, can be combined with DP (Bitmask DP)
```

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

## Nhận Ra Pattern

| Signal | Bit technique |
|--------|--------------|
| "single number", "odd times" | XOR all |
| "power of 2" | n & (n-1) == 0 |
| "count 1-bits" | Brian Kernighan / OnesCount |
| "missing number" | XOR all indices+values |
| "reverse bits" | Shift + OR loop |
| "add without +" | XOR + AND carry loop |
| "all subsets" | Bitmask enumeration |
| "n ≤ 20, find optimal subset" | Bitmask DP |

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

## Common Gotchas in Go

```go
// ❌ Integer overflow
1 << 32      // fine cho int64, nhưng cẩn thận type
uint32(1 << 32)  // 0! (overflow)

// ✅ Safe
var n int64 = 1 << 32

// Arithmetic right shift (Go dùng arithmetic >> cho signed int)
-4 >> 1  // = -2 (keeps sign bit) — platform safe in Go

// XOR với negative numbers: careful với two's complement
// a ^ b khi a,b là signed int: works, nhưng result có thể negative
```

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

## Bài Tiêu Biểu

| Bài | Technique | Key |
|-----|-----------|-----|
| Single Number | XOR all | a^a=0, a^0=a |
| Number of 1 Bits | Brian Kernighan | n&(n-1) removes lowest bit |
| Counting Bits | DP + bit | dp[i] = dp[i>>1] + i&1 |
| Missing Number | XOR indices+values | pairs cancel |
| Reverse Bits | Shift loop | (result<<1) | (num&1) |
| Sum of Two Integers | XOR + carry | repeat until carry=0 |

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

## Tags

#bit-manipulation #xor #bitmask #interview-prep
