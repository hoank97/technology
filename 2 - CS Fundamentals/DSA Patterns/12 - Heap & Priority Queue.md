---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 12 — Heap & Priority Queue

> **Giải quyết**: Lấy **min/max liên tục** trong stream dữ liệu động, hoặc chọn **Top-K** phần tử — O(log n) per operation thay vì O(n) scan

---

## Bài Toán Giải Quyết

Heap = Complete binary tree với **heap property**: parent ≤ children (min-heap) hoặc parent ≥ children (max-heap).

Dùng khi:
1. **Top-K**: K phần tử lớn/nhỏ nhất
2. **Kth element**: Phần tử thứ K trong stream
3. **Merge K sorted lists**: Luôn lấy min từ K lists
4. **Median of stream**: Two-heap technique
5. **Dijkstra**: Priority queue cho shortest path

**Core insight**: Thay vì sort toàn bộ O(n log n) để lấy K phần tử → min-heap size K cho O(n log k).

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

## Pattern 1: Top-K Elements

```go
// Top K Frequent Elements — min-heap size K
// Loại bỏ min khi size > K → còn lại là K lớn nhất
freq := make(map[int]int)
for _, n := range nums { freq[n]++ }

h := &MinHeap{}
heap.Init(h)
for val, cnt := range freq {
    heap.Push(h, [2]int{cnt, val})
    if h.Len() > k { heap.Pop(h) }  // remove smallest freq
}

result := make([]int, k)
for i := k-1; i >= 0; i-- {
    result[i] = heap.Pop(h).([2]int)[1]
}
```

**Pattern**: `min-heap size K` = K largest. `max-heap size K` = K smallest.

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

## Pattern 3: Two Heaps — Median of Stream

```go
// Maintain: maxHeap (lower half) và minHeap (upper half)
// Median = avg of two tops hoặc top of larger heap

type MedianFinder struct {
    lo *MaxHeap  // lower half, max at top
    hi *MinHeap  // upper half, min at top
}

func (mf *MedianFinder) AddNum(num int) {
    heap.Push(mf.lo, num)               // always push to lo first
    heap.Push(mf.hi, heap.Pop(mf.lo))  // balance: push lo-max to hi

    if mf.hi.Len() > mf.lo.Len() {     // keep lo >= hi
        heap.Push(mf.lo, heap.Pop(mf.hi))
    }
}

func (mf *MedianFinder) FindMedian() float64 {
    if mf.lo.Len() > mf.hi.Len() {
        return float64((*mf.lo)[0])
    }
    return float64((*mf.lo)[0] + (*mf.hi)[0]) / 2.0
}
```

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

## Pattern 5: Task Scheduler (Greedy + Heap)

```go
// Luôn chọn task có frequency cao nhất
freq := make(map[byte]int)
for _, t := range tasks { freq[t]++ }

h := &MaxHeap{}
for _, f := range freq { heap.Push(h, f) }

time := 0
for h.Len() > 0 {
    temp := []int{}
    for i := 0; i < n+1; i++ {  // n+1 là cooldown window
        if h.Len() > 0 { temp = append(temp, heap.Pop(h).(int)-1) }
    }
    for _, f := range temp {
        if f > 0 { heap.Push(h, f) }
    }
    if h.Len() > 0 { time += n+1 } else { time += len(temp) }
}
```

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

## ✅ Ưu Điểm

- **O(log n)** insert/delete — cân bằng tốt
- **O(1)** peek min/max — không cần sort
- **Heapify O(n)** từ array — hiệu quả hơn n lần push
- Top-K: **O(n log k)** thay vì O(n log n) sort

## ❌ Nhược Điểm / Giới Hạn

- **Không support O(log n) search/delete by value** — chỉ delete root
- Nếu cần thay đổi priority một node cụ thể → cần lazy deletion hoặc decrease-key
- **Go heap boilerplate nhiều** — phải implement 5 methods
- Không có ordered iteration (phải pop all → O(n log n))

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

## Trade-off: Heap vs Sort vs QuickSelect

| | Heap Top-K | Sort + take K | QuickSelect |
|---|---|---|---|
| **Time** | O(n log k) | O(n log n) | O(n) avg, O(n²) worst |
| **Space** | O(k) | O(n) | O(1) |
| **Streaming** | ✅ Online | ❌ Need all data | ❌ Need all data |
| **Stability** | ❌ | ✅ (Merge sort) | ❌ |

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

## 📌 Tóm tắt

```
Heap & Priority Queue
│
├── Min-heap: root = minimum → Pop gives min
├── Max-heap: negate values (Go) or flip Less
│
├── Patterns
│   ├── Top-K largest: min-heap size K (evict smallest)
│   ├── Top-K smallest: max-heap size K (evict largest)
│   ├── Kth element: heap size K → peek root
│   ├── Two heaps: median of stream (lo/hi balance)
│   ├── Merge K sorted: push K heads, pop-push
│   └── Greedy + heap: task scheduler
│
├── Complexity: Push/Pop O(log n), Peek O(1), Heapify O(n)
│
├── ✅ O(n log k) Top-K, streaming support
└── ❌ No O(log n) arbitrary delete, Go boilerplate heavy
```

## Tags

#heap #priority-queue #top-k #median #two-heaps #interview-prep
