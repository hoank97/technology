---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 07 — BFS (Breadth-First Search)

> **Giải quyết**: **Shortest path** trong unweighted graph/tree — BFS đảm bảo tìm thấy path ngắn nhất vì explore theo từng "layer" khoảng cách

---

## Bài Toán Giải Quyết

BFS = Level-order traversal. Dùng khi:
1. **Shortest path** — unweighted graph (Dijkstra không cần)
2. **Level-by-level** processing — tree right side view, zigzag
3. **Multi-source BFS** — Rotting Oranges, Walls & Gates (xử lý nhiều điểm nguồn cùng lúc)
4. **Connected components** — Number of Islands
5. **Word transformation** — Word Ladder (mỗi transform = 1 edge)

**Core insight**: BFS dùng queue (FIFO) → mọi node ở distance d được xử lý trước distance d+1 → đảm bảo shortest path.

---

## Template Chuẩn

```go
// Single-source BFS
q := []int{start}
visited := map[int]bool{start: true}
steps := 0

for len(q) > 0 {
    // process entire current level
    for size := len(q); size > 0; size-- {
        node := q[0]; q = q[1:]

        if node == target { return steps }

        for _, next := range graph[node] {
            if !visited[next] {
                visited[next] = true
                q = append(q, next)
            }
        }
    }
    steps++  // level complete → distance + 1
}
return -1  // unreachable
```

---

## Multi-Source BFS

Khi có **nhiều nguồn đồng thời** → enqueue tất cả vào queue từ đầu:

```go
// Rotting Oranges: tất cả rotten oranges lan ra cùng lúc
q := [][]int{}
freshCount := 0

for r := range grid {
    for c := range grid[r] {
        if grid[r][c] == 2 { q = append(q, []int{r, c}) }
        if grid[r][c] == 1 { freshCount++ }
    }
}

minutes := 0
dirs := [][]int{{0,1},{0,-1},{1,0},{-1,0}}

for len(q) > 0 && freshCount > 0 {
    for size := len(q); size > 0; size-- {
        cell := q[0]; q = q[1:]
        for _, d := range dirs {
            nr, nc := cell[0]+d[0], cell[1]+d[1]
            if nr >= 0 && nr < len(grid) && nc >= 0 && nc < len(grid[0]) &&
               grid[nr][nc] == 1 {
                grid[nr][nc] = 2
                freshCount--
                q = append(q, []int{nr, nc})
            }
        }
    }
    minutes++
}

if freshCount > 0 { return -1 }
return minutes
```

---

## BFS trên Matrix (Grid)

```go
// Number of Islands — BFS từ mỗi unvisited '1'
dirs := [][]int{{0,1},{0,-1},{1,0},{-1,0}}

bfs := func(r, c int) {
    q := [][]int{{r, c}}
    grid[r][c] = '0'  // mark visited

    for len(q) > 0 {
        cell := q[0]; q = q[1:]
        for _, d := range dirs {
            nr, nc := cell[0]+d[0], cell[1]+d[1]
            if nr >= 0 && nr < len(grid) && nc >= 0 && nc < len(grid[0]) &&
               grid[nr][nc] == '1' {
                grid[nr][nc] = '0'
                q = append(q, []int{nr, nc})
            }
        }
    }
}

count := 0
for r := range grid {
    for c := range grid[r] {
        if grid[r][c] == '1' { bfs(r, c); count++ }
    }
}
```

---

## Word Ladder — BFS trên Implicit Graph

```go
// Mỗi word = node, edge = differ by 1 char
q := []string{beginWord}
visited := map[string]bool{beginWord: true}
steps := 1
wordSet := map[string]bool{}
for _, w := range wordList { wordSet[w] = true }

for len(q) > 0 {
    for size := len(q); size > 0; size-- {
        word := q[0]; q = q[1:]
        if word == endWord { return steps }

        for i := 0; i < len(word); i++ {
            for c := byte('a'); c <= 'z'; c++ {
                next := word[:i] + string(c) + word[i+1:]
                if wordSet[next] && !visited[next] {
                    visited[next] = true
                    q = append(q, next)
                }
            }
        }
    }
    steps++
}
return 0
```

---

## Nhận Ra Pattern

| Signal | BFS variant |
|--------|-------------|
| "shortest path", "minimum steps" | Standard BFS |
| "level order", "right side view" | BFS by level |
| "multiple sources spread simultaneously" | Multi-source BFS |
| "minimum path in grid (4 dirs)" | BFS on matrix |
| "word transformation", "shortest conversion" | BFS on implicit graph |
| "minimum distance to nearest X" | Multi-source BFS from all X |

---

## ✅ Ưu Điểm

- **Guaranteed shortest path** (unweighted) — DFS không có property này
- **Level-by-level**: tự nhiên xử lý bài toán theo layer
- **Multi-source**: trivially enqueue all sources → xử lý đồng thời
- Tránh được recursion depth issues (dùng queue thay call stack)

## ❌ Nhược Điểm / Giới Hạn

- **O(V+E) space** — queue có thể chứa toàn bộ một layer (rộng)
- **Không tìm được path qua negative weight edges** → Dijkstra/Bellman-Ford
- **Với weighted graph**: BFS tìm min hops nhưng không min cost → Dijkstra
- Slow hơn DFS nếu chỉ cần check existence (không cần shortest)

---

## Trade-off: BFS vs DFS

| | BFS | DFS |
|---|---|---|
| **Shortest path** | ✅ Guaranteed | ❌ Không guarantee |
| **Level-by-level** | ✅ | ❌ |
| **Space** | O(w) — width | O(h) — height |
| **Tree path** | ❌ Awkward | ✅ Natural |
| **Cycle detection** | ✅ (mark visited) | ✅ |
| **Connected components** | ✅ | ✅ |
| **Dense graph (wide)** | ❌ High memory | ✅ Less memory |
| **Deep graph (tall)** | ✅ Less memory | ❌ Stack overflow |

---

## Trade-off: BFS vs Dijkstra

| | BFS | Dijkstra |
|---|---|---|
| **Weight** | Unweighted (all = 1) | Weighted |
| **Time** | O(V+E) | O((V+E) log V) |
| **Space** | O(V) queue | O(V) priority queue |
| **Use case** | Grid, word ladder | Road network, network delay |

---

## Bài Tiêu Biểu

| Bài | BFS type | Key |
|-----|----------|-----|
| Binary Tree Level Order | Tree BFS by level | Size = len(q) before inner loop |
| Number of Islands | Matrix BFS/DFS | Mark visited = '0' |
| Rotting Oranges | Multi-source BFS | Enqueue all rotten initially |
| Walls and Gates | Multi-source BFS | Enqueue all gates (0) |
| Word Ladder | Implicit graph BFS | Generate 26 char changes |
| Right Side View | Tree BFS | Take last element of each level |

---

## 📌 Tóm tắt

```
BFS
│
├── Khi nào
│   ├── Shortest path (unweighted) → BFS over DFS
│   ├── Level-by-level processing
│   └── Multiple sources spread simultaneously
│
├── Template
│   ├── Queue (FIFO)
│   ├── Visited set (avoid revisit)
│   ├── Process level by capturing len(q)
│   └── steps++ after each level
│
├── Variants
│   ├── Standard: single source
│   ├── Multi-source: enqueue all sources initially
│   ├── Matrix: 4-directional neighbors
│   └── Implicit graph: generate neighbors on-the-fly
│
├── ✅ Guaranteed shortest path, level-by-level natural
├── ❌ High memory for wide graphs
│
└── vs DFS: BFS=shortest, DFS=path/subtree
    vs Dijkstra: BFS=unweighted, Dijkstra=weighted
```

## Tags

#bfs #shortest-path #level-order #graph #interview-prep
