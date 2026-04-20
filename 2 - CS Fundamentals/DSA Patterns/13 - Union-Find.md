---
type: concept
status: complete
date_created: 2026-04-21
tags: [connected-components, cs, cycle-detection, dsu, fundamentals, graph, interview-prep, union-find]
---
parent:: [[00 - DSA Patterns]]

# 13 — Union-Find (Disjoint Set Union)

> **Giải quyết**: **Dynamic connectivity** — merge nhóm, check same group, detect cycle trong undirected graph — O(α(n)) ≈ O(1) per operation

---
---

## Implementation Đầy Đủ

```go
type UnionFind struct {
    parent []int
    rank   []int
    count  int  // số components
}

func NewUF(n int) *UnionFind {
    parent := make([]int, n)
    for i := range parent { parent[i] = i }
    return &UnionFind{parent: parent, rank: make([]int, n), count: n}
}

// Find với Path Compression — O(α(n)) amortized
func (uf *UnionFind) Find(x int) int {
    if uf.parent[x] != x {
        uf.parent[x] = uf.Find(uf.parent[x])  // path compression
    }
    return uf.parent[x]
}

// Union với Rank — O(α(n)) amortized
func (uf *UnionFind) Union(x, y int) bool {
    px, py := uf.Find(x), uf.Find(y)
    if px == py { return false }  // already connected

    // attach smaller rank tree under larger
    if uf.rank[px] < uf.rank[py] { px, py = py, px }
    uf.parent[py] = px
    if uf.rank[px] == uf.rank[py] { uf.rank[px]++ }
    uf.count--
    return true
}

func (uf *UnionFind) Connected(x, y int) bool {
    return uf.Find(x) == uf.Find(y)
}
```

---
---

## Pattern 2: Cycle Detection (Redundant Connection)

```go
// Redundant Connection: tìm edge tạo cycle
uf := NewUF(n+1)
for _, e := range edges {
    if !uf.Union(e[0], e[1]) {  // Union returns false = already connected
        return e  // this edge creates a cycle
    }
}
return nil
```

---
---

## Tại Sao O(α(n)) ≈ O(1)?

```
Không có optimization:
  Find: O(n) worst (chain: 1→2→3→...→n)

Path Compression only:
  Find: O(log n) amortized

Union by Rank only:
  Find: O(log n)

Both (Path Compression + Union by Rank):
  Find: O(α(n)) — Inverse Ackermann function
  Practically: α(n) ≤ 4 for any n ≤ 10^600

α(n) là hàm tăng cực kỳ chậm:
  α(1) = 0, α(2) = 1, α(4) = 2, α(16) = 3, α(65536) = 4
  → Với mọi input thực tế: ≤ 4 steps
```

---
---

## ✅ Ưu Điểm

- **O(α(n)) ≈ O(1)** per operation — fastest for dynamic connectivity
- **Online queries**: process queries one by one (vs BFS/DFS cần full graph)
- Simple implementation sau khi quen
- Tự nhiên detect cycle trong undirected graph
- Space O(n) — chỉ lưu parent + rank

## ❌ Nhược Điểm / Giới Hạn

- **Chỉ cho undirected graph** — directed graph cycle: dùng DFS 3-color
- **Không hỗ trợ Split** (disconnect) — chỉ union, không un-union
- **Không tìm path** giữa nodes — chỉ check connectivity
- Ít linh hoạt hơn DFS/BFS cho traversal problems

---
---

## Bài Tiêu Biểu

| Bài | Pattern | Key |
|-----|---------|-----|
| Redundant Connection | Cycle detect | First false Union = redundant |
| Number of Connected Components | Count | uf.count after all unions |
| Graph Valid Tree | Tree check | n-1 edges + no cycle |
| Accounts Merge | Group by email | Union accounts sharing email |
| Satisfiability of Equality Equations | Group by == | Check != against groups |

---
