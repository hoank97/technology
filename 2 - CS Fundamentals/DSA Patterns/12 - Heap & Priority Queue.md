---
type: concept
status: complete
date_created: 2026-04-21
tags: [cs, fundamentals, heap, interview-prep, median, priority-queue, top-k, two-heaps]
---
parent:: [[00 - DSA Patterns]]

# 12 — Heap & Priority Queue

> **Giải quyết**: Lấy **min/max liên tục** trong stream dữ liệu động, hoặc chọn **Top-K** phần tử — O(log n) per operation thay vì O(n) scan

---
---

## Go Heap Implementation

```go
import "container/heap"

// Min-heap
type MinHeap []int
func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *MinHeap) Pop() any {
    old := *h; n := len(old)
    x := old[n-1]; *h = old[:n-1]; return x
}

// Usage
h := &MinHeap{3, 1, 4, 1, 5}
heap.Init(h)
heap.Push(h, 2)
min := heap.Pop(h).(int)  // 1

// Max-heap: negate the values
// Less(i,j) { return h[i] > h[j] }
```

---
---

## Pattern 2: Kth Element

```go
// Kth Largest Element in Array
h := &MinHeap{}
heap.Init(h)
for _, n := range nums {
    heap.Push(h, n)
    if h.Len() > k { heap.Pop(h) }
}
return (*h)[0]  // root = kth largest

// Alternative: Quickselect O(n) avg, O(n²) worst
```

---
---

## Pattern 4: Merge K Sorted Lists

```go
// Min-heap của (val, listIndex, nodeIndex)
// Luôn lấy node nhỏ nhất từ K lists
h := &NodeHeap{}
for i, list := range lists {
    if list != nil { heap.Push(h, [2]*ListNode{list, nil}) }
}

dummy := &ListNode{}
curr := dummy
for h.Len() > 0 {
    item := heap.Pop(h).(*ListNode)
    curr.Next = item
    curr = curr.Next
    if item.Next != nil { heap.Push(h, item.Next) }
}
return dummy.Next
```

---
---

## Nhận Ra Pattern

| Signal | Heap pattern |
|--------|-------------|
| "kth largest/smallest" | Min-heap size K |
| "top K frequent" | Min-heap size K |
| "median from stream" | Two heaps (lo/hi) |
| "merge K sorted" | Min-heap with K heads |
| "schedule tasks with cooldown" | Max-heap greedy |
| "meet deadlines optimally" | Greedy + heap |
| "shortest path" | Min-heap (Dijkstra) |

---
---

## Complexity

| Operation | Min/Max Heap |
|-----------|-------------|
| Push | O(log n) |
| Pop (root) | O(log n) |
| Peek (root) | O(1) |
| Heapify | O(n) |
| Search | O(n) |

---
---

## Bài Tiêu Biểu

| Bài | Pattern | Key |
|-----|---------|-----|
| Kth Largest in Array | Min-heap size K | Pop when size > k |
| Top K Frequent | Min-heap size K | Heap on freq |
| Find Median from Stream | Two heaps | lo.size >= hi.size |
| Merge K Sorted Lists | Min-heap K heads | Push next node of popped |
| Task Scheduler | Max-heap + cooldown | Simulate n+1 windows |
| K Closest Points | Max-heap size K | Heap on distance |
| Design Twitter | Max-heap K tweets | Merge per-user lists |

---
