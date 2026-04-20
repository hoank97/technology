---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 11 — Graphs

> **Giải quyết**: Connected components, cycle detection, topological ordering, shortest path — bài toán có mối **quan hệ** giữa các nodes

---

## Bài Toán Giải Quyết

Graph problems phổ biến:
1. **Connected Components**: Đếm số thành phần liên thông
2. **Cycle Detection**: Có vòng lặp không (undirected/directed)
3. **Topological Sort**: Thứ tự hợp lệ trong DAG (Course Schedule)
4. **Shortest Path**: Weighted → Dijkstra, Unweighted → BFS
5. **Flood Fill / Islands**: DFS/BFS trên grid

**Representation**:
```go
// Adjacency list (thường dùng)
graph := make(map[int][]int)
for _, e := range edges {
    graph[e[0]] = append(graph[e[0]], e[1])
}
```

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

## Pattern 2: Cycle Detection

### Undirected Graph (DFS + parent tracking)

```go
// DFS: cycle nếu thấy visited node không phải parent
var hasCycle func(node, parent int) bool
hasCycle = func(node, parent int) bool {
    visited[node] = true
    for _, next := range graph[node] {
        if !visited[next] {
            if hasCycle(next, node) { return true }
        } else if next != parent { return true }  // cycle!
    }
    return false
}
```

### Directed Graph (DFS + 3 colors)

```go
// White=0, Gray=1 (in stack), Black=2 (done)
color := make([]int, n)

var dfs func(node int) bool
dfs = func(node int) bool {
    color[node] = 1  // gray: in current DFS path
    for _, next := range graph[node] {
        if color[next] == 1 { return true }   // back edge = cycle
        if color[next] == 0 && dfs(next) { return true }
    }
    color[node] = 2  // black: done
    return false
}
```

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

## Pattern 4: Shortest Path — Dijkstra

```go
// Network Delay Time: min time từ k đến all nodes
dist := make([]int, n+1)
for i := range dist { dist[i] = math.MaxInt }
dist[k] = 0

// min-heap: [dist, node]
pq := &MinHeap{{0, k}}
heap.Init(pq)

for pq.Len() > 0 {
    item := heap.Pop(pq).([2]int)
    d, u := item[0], item[1]
    if d > dist[u] { continue }  // stale

    for _, e := range graph[u] {
        v, w := e[0], e[1]
        if dist[u]+w < dist[v] {
            dist[v] = dist[u] + w
            heap.Push(pq, [2]int{dist[v], v})
        }
    }
}
```

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

## Nhận Ra Pattern

| Signal | Algorithm |
|--------|-----------|
| "connected", "islands", "components" | DFS/BFS + visited |
| "detect cycle" (undirected) | DFS + parent |
| "detect cycle" (directed) | DFS 3-color / Kahn's |
| "course schedule", "dependencies" | Topological Sort (Kahn's) |
| "shortest path", weighted | Dijkstra |
| "shortest path with at most K edges" | Bellman-Ford / DP |
| "minimum spanning tree" | Prim's / Kruskal's |
| "redundant connection" | Union-Find |

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

## Algorithm Selector

```
Có edge weights?
  ├── Không → BFS (shortest hops)
  └── Có →
        ├── Negative weights? → Bellman-Ford
        ├── K steps limit? → Bellman-Ford / DP
        └── Non-negative → Dijkstra

Cần order/cycle?
  ├── Directed acyclic → Topological Sort (Kahn's)
  └── Just detect cycle → DFS 3-color

Connected components?
  ├── Static → DFS/BFS
  └── Dynamic (union queries) → Union-Find
```

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

## 📌 Tóm tắt

```
Graphs
│
├── Representation: adjacency list map[int][]int
│
├── Traversal
│   ├── DFS: recursive/iterative — components, paths
│   └── BFS: queue — shortest hops, level-order
│
├── Cycle Detection
│   ├── Undirected: DFS + parent tracking
│   └── Directed: DFS 3-color (white/gray/black)
│
├── Topological Sort (DAG)
│   ├── Kahn's BFS: inDegree + queue
│   └── Auto-detects cycle (len(order) < n)
│
├── Shortest Path
│   ├── Unweighted: BFS O(V+E)
│   ├── Non-negative weights: Dijkstra O((V+E)logV)
│   └── Negative / K steps: Bellman-Ford O(V×E)
│
└── Decision: weight? → neg? → K steps? → BFS/Dijkstra/Bellman-Ford
```

## Tags

#graphs #dfs #bfs #dijkstra #topological-sort #bellman-ford #interview-prep
