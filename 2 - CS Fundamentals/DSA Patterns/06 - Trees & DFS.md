---
type: concept
status: complete
date_created: 2026-04-21
tags: [bst, cs, dfs, fundamentals, interview-prep, traversal, trees]
---
parent:: [[00 - DSA Patterns]]

# 06 — Trees & DFS

> **Giải quyết**: Traverse, validate, construct, hoặc calculate trên tree structure — mọi bài tree đều có thể giải bằng DFS với cấu trúc `process(left) + process(right) + use results`

---
---

## DFS Templates

### Template 1: Return value từ subtree (postorder)

```go
// Áp dụng cho: Max depth, Diameter, Balance check, Path sum
func dfs(node *TreeNode) int {
    if node == nil { return 0 }      // base case

    left := dfs(node.Left)           // get result from left
    right := dfs(node.Right)         // get result from right

    // process: combine left + right + current node
    return max(left, right) + 1      // example: max depth
}
```

### Template 2: Track global result (side effect)

```go
// Áp dụng cho: Diameter, Max path sum (xuyên qua node)
var result int

func dfs(node *TreeNode) int {
    if node == nil { return 0 }

    left := max(0, dfs(node.Left))    // ignore negative paths
    right := max(0, dfs(node.Right))

    result = max(result, left+right+node.Val)  // update global

    return max(left, right) + node.Val  // return max path through this node
}
```

### Template 3: Pass down constraint (preorder)

```go
// Áp dụng cho: BST validate, Count good nodes
func dfs(node *TreeNode, minVal, maxVal int) bool {
    if node == nil { return true }    // base case OK

    if node.Val <= minVal || node.Val >= maxVal { return false }

    return dfs(node.Left, minVal, node.Val) &&   // left: max = current
           dfs(node.Right, node.Val, maxVal)      // right: min = current
}
// Call: dfs(root, math.MinInt, math.MaxInt)
```

### Template 4: Inorder (BST → sorted sequence)

```go
// Inorder của BST = sorted array
var result []int

func inorder(node *TreeNode) {
    if node == nil { return }
    inorder(node.Left)
    result = append(result, node.Val)  // process at inorder position
    inorder(node.Right)
}
// Kth smallest in BST: stop at kth element
```

---
---

## BST Properties

```
BST invariant:
  left.val < node.val < right.val (strictly)

→ Inorder = sorted sequence
→ Search: O(h) — O(log n) balanced, O(n) skewed
→ LCA: walk toward target from root
```

```go
// LCA in BST — không cần DFS toàn bộ
func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
    if p.Val < root.Val && q.Val < root.Val {
        return lowestCommonAncestor(root.Left, p, q)
    }
    if p.Val > root.Val && q.Val > root.Val {
        return lowestCommonAncestor(root.Right, p, q)
    }
    return root  // split point = LCA
}
```

---
---

## ✅ Ưu Điểm

- **O(n) time** — thăm mỗi node đúng 1 lần
- **O(h) space** — h = height (O(log n) balanced, O(n) worst)
- Recursive code cực kỳ ngắn và rõ ràng
- Postorder pattern giải quyết rất nhiều dạng bài

## ❌ Nhược Điểm / Giới Hạn

- **Stack overflow** với tree rất sâu (n > 10^5 nodes, skewed tree) → cần iterative
- **O(n) space worst case** (skewed tree = linked list)
- Khó debug vì recursive — cần visualize rõ call stack
- Dễ quên handle `node == nil` base case

---
---

## Trade-off: DFS vs BFS trên Tree

| | DFS | BFS |
|---|---|---|
| **Level-by-level** | ❌ | ✅ |
| **Shortest path** | ❌ | ✅ |
| **Path/subtree** | ✅ | ❌ |
| **Space** | O(h) | O(w) max width |
| **Code** | Recursive (simple) | Queue-based |

> Nếu bài hỏi "level", "right side view", "zigzag" → BFS. Còn lại thường DFS.

---
---

## 📌 Tóm tắt

```
Trees & DFS
│
├── Core insight: "con trái + con phải → kết quả node hiện tại" (postorder)
│
├── Templates
│   ├── T1: Postorder return value — depth, height, balance
│   ├── T2: Postorder + global var — diameter, max path sum
│   ├── T3: Preorder + pass constraint — BST validate, good nodes
│   └── T4: Inorder — BST sorted sequence, kth smallest
│
├── Traversal order
│   ├── Preorder: serialize, copy
│   ├── Inorder: BST → sorted
│   └── Postorder: calculate subtree results
│
├── ✅ O(n) time, O(h) space, code ngắn gọn
├── ❌ Stack overflow khi skewed tree → dùng iterative
│
└── DFS vs BFS
    ├── DFS: path, subtree, validate
    └── BFS: level-order, shortest path, right-side view
```
