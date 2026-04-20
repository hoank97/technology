---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 13 — Union-Find (Disjoint Set Union)

> **Giải quyết**: **Dynamic connectivity** — merge nhóm, check same group, detect cycle trong undirected graph — O(α(n)) ≈ O(1) per operation

---

## Bài Toán Giải Quyết

Union-Find (DSU) dùng khi:
1. **Connected components**: Đếm số nhóm, check cùng nhóm không
2. **Cycle detection** (undirected): Union edge → nếu đã cùng nhóm → cycle
3. **Redundant Connection**: Tìm edge tạo cycle trong undirected graph
4. **Kruskal's MST**: Build minimum spanning tree
5. **Dynamic friend groups**: Online queries

**Core insight**: Mỗi component có một **representative (root)**. Hai nodes cùng component ↔ cùng root. Union = merge hai roots.

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

## Pattern 1: Count Connected Components

```go
// Number of Connected Components in Undirected Graph
uf := NewUF(n)
for _, e := range edges {
    uf.Union(e[0], e[1])
}
return uf.count
```

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

## Pattern 3: Graph Valid Tree

```go
// n nodes, edges → valid tree?
// Tree = connected (1 component) + no cycle (n-1 edges)
if len(edges) != n-1 { return false }  // quick check

uf := NewUF(n)
for _, e := range edges {
    if !uf.Union(e[0], e[1]) { return false }  // cycle found
}
return true  // uf.count == 1 (connected)
```

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

## Nhận Ra Pattern

| Signal | Union-Find |
|--------|-----------|
| "connected components" | Count via union.count |
| "are X and Y in same group" | Find(x) == Find(y) |
| "detect cycle in undirected" | Union→false = cycle |
| "redundant edge", "extra edge" | First edge making cycle |
| "valid tree" | n-1 edges + no cycle |
| "minimum spanning tree" (Kruskal) | Sort edges + Union |
| "accounts merge" | Union by common email |

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

## Trade-off: Union-Find vs DFS/BFS

| | Union-Find | DFS/BFS |
|---|---|---|
| **Connectivity check** | O(α(n)) per query | O(V+E) per query |
| **Online queries** | ✅ | ❌ (need rebuild) |
| **Cycle detection** | Undirected only | Both directed + undirected |
| **Path finding** | ❌ | ✅ |
| **Level/distance** | ❌ | ✅ (BFS) |
| **Implementation** | Compact | More complex |

> **Quy tắc**: Nếu bài hỏi về **grouping, connectivity, cycle (undirected)** → Union-Find. Nếu cần **path, distance, level** → DFS/BFS.

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

## 📌 Tóm tắt

```
Union-Find (DSU)
│
├── Core: parent[] + rank[]
│   ├── Find(x): path compression → root
│   └── Union(x,y): merge by rank → false if already connected
│
├── Optimizations
│   ├── Path Compression: flatten tree during Find
│   └── Union by Rank: attach smaller under larger
│   → Combined: O(α(n)) ≈ O(1)
│
├── Patterns
│   ├── Count components: track uf.count
│   ├── Cycle (undirected): Union returns false
│   └── Dynamic grouping: online queries
│
├── ✅ Fastest for connectivity, online queries, O(α(n))
└── ❌ Only undirected, no split, no path/distance
    → Use DFS/BFS for path/level problems
```

## Tags

#union-find #dsu #connected-components #cycle-detection #graph #interview-prep
