---
type: concept
status: complete
date_created: 2026-04-21
tags: [bfs, cs, fundamentals, graph, interview-prep, level-order, shortest-path]
---
parent:: [[00 - DSA Patterns]]

# 07 — BFS (Breadth-First Search)

> **Giải quyết**: **Shortest path** trong unweighted graph/tree — BFS đảm bảo tìm thấy path ngắn nhất vì explore theo từng "layer" khoảng cách

---
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
