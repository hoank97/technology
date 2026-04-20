---
type: concept
status: complete
date_created: 2026-04-21
tags: [bellman-ford, bfs, cs, dfs, dijkstra, fundamentals, graphs, interview-prep, topological-sort]
---
parent:: [[00 - DSA Patterns]]

# 11 — Graphs

> **Giải quyết**: Connected components, cycle detection, topological ordering, shortest path — bài toán có mối **quan hệ** giữa các nodes

---
---

## Pattern 1: DFS — Connected Components / Flood Fill

```go
// Number of Islands
visited := make([][]bool, rows)
for i := range visited { visited[i] = make([]bool, cols) }

dirs := [][]int{{0,1},{0,-1},{1,0},{-1,0}}

var dfs func(r, c int)
dfs = func(r, c int) {
    if r < 0 || r >= rows || c < 0 || c >= cols { return }
    if visited[r][c] || grid[r][c] == '0' { return }
    visited[r][c] = true
    for _, d := range dirs { dfs(r+d[0], c+d[1]) }
}

count := 0
for r := range grid {
    for c := range grid[r] {
        if !visited[r][c] && grid[r][c] == '1' {
            dfs(r, c); count++
        }
    }
}
```

---
---

## Pattern 3: Topological Sort

### Kahn's BFS (detect cycle + produce order)

```go
inDegree := make([]int, n)
for _, e := range prerequisites {
    graph[e[1]] = append(graph[e[1]], e[0])
    inDegree[e[0]]++
}

q := []int{}
for i, d := range inDegree {
    if d == 0 { q = append(q, i) }
}

order := []int{}
for len(q) > 0 {
    node := q[0]; q = q[1:]
    order = append(order, node)
    for _, next := range graph[node] {
        inDegree[next]--
        if inDegree[next] == 0 { q = append(q, next) }
    }
}

// len(order) < n → có cycle → impossible
return len(order) == n
```

---
---

## Pattern 5: Bellman-Ford (Negative Weights / K Steps)

```go
// Cheapest Flights Within K Stops
// Relax edges K+1 times
dist := make([]int, n)
for i := range dist { dist[i] = math.MaxInt }
dist[src] = 0

for i := 0; i <= k; i++ {
    temp := append([]int{}, dist...)  // copy — avoid chaining
    for _, e := range flights {
        u, v, w := e[0], e[1], e[2]
        if dist[u] != math.MaxInt && dist[u]+w < temp[v] {
            temp[v] = dist[u] + w
        }
    }
    dist = temp
}
```

---
---

## ✅ Ưu Điểm

- **DFS/BFS**: O(V+E) — optimal cho traversal
- **Kahn's**: tự nhiên detect cycle AND produce topological order
- **Dijkstra**: O((V+E)log V) — efficient với min-heap

## ❌ Nhược Điểm / Giới Hạn

- **Dijkstra**: không hoạt động với negative edges → Bellman-Ford
- **Bellman-Ford**: O(V×E) — chậm hơn Dijkstra
- **DFS cycle detect**: cần cẩn thận directed vs undirected (khác cách)
- **Dense graph**: adjacency matrix O(V²) memory

---
---

## Bài Tiêu Biểu

| Bài | Algorithm | Key |
|-----|-----------|-----|
| Number of Islands | DFS grid | Mark visited in-place |
| Course Schedule I | Kahn's / DFS 3-color | Cycle detection |
| Course Schedule II | Kahn's | Return topological order |
| Network Delay Time | Dijkstra | Single-source shortest path |
| Cheapest Flights K Stops | Bellman-Ford | K+1 relaxation rounds |
| Word Ladder | BFS implicit graph | 26-char substitution |
| Reconstruct Itinerary | DFS Eulerian path | Hierholzer's algorithm |

---
