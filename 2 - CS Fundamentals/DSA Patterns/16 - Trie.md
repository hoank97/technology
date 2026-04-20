---

parent:: [[00 - DSA Patterns]]
type: concept
status: complete
date_created: 2026-04-21

---

# 16 — Trie (Prefix Tree)

> **Giải quyết**: Tìm kiếm theo **prefix** trong tập từ — O(L) per query (L = word length) thay vì O(n×L) linear scan

---

## Bài Toán Giải Quyết

Trie = cây n-ary lưu trữ ký tự theo từng level, mỗi path từ root → leaf = một từ.

Dùng khi:
1. **Prefix search**: "startsWith", autocomplete
2. **Word dictionary**: Add words, search exact/pattern
3. **Pattern matching**: Ký tự wildcard '.'
4. **Word Search trên Grid**: Trie + backtracking (Word Search II)

**Core insight**: Nhiều từ chia sẻ prefix → lưu prefix một lần → tiết kiệm space + search nhanh.

---

## Implementation Chuẩn

```go
type TrieNode struct {
    children [26]*TrieNode  // lowercase a-z
    isEnd    bool
}

type Trie struct {
    root *TrieNode
}

func Constructor() Trie {
    return Trie{root: &TrieNode{}}
}

func (t *Trie) Insert(word string) {
    node := t.root
    for _, c := range word {
        i := c - 'a'
        if node.children[i] == nil {
            node.children[i] = &TrieNode{}
        }
        node = node.children[i]
    }
    node.isEnd = true
}

func (t *Trie) Search(word string) bool {
    node := t.root
    for _, c := range word {
        i := c - 'a'
        if node.children[i] == nil { return false }
        node = node.children[i]
    }
    return node.isEnd  // must end here
}

func (t *Trie) StartsWith(prefix string) bool {
    node := t.root
    for _, c := range prefix {
        i := c - 'a'
        if node.children[i] == nil { return false }
        node = node.children[i]
    }
    return true  // prefix exists (regardless of isEnd)
}
```

---

## Pattern 1: Wildcard Search (Design Add and Search)

```go
// '.' matches any character → DFS at '.' nodes
func (t *Trie) SearchWithWildcard(word string) bool {
    var dfs func(node *TrieNode, i int) bool
    dfs = func(node *TrieNode, i int) bool {
        if i == len(word) { return node.isEnd }
        c := word[i]
        if c == '.' {
            for _, child := range node.children {
                if child != nil && dfs(child, i+1) { return true }
            }
            return false
        }
        idx := c - 'a'
        if node.children[idx] == nil { return false }
        return dfs(node.children[idx], i+1)
    }
    return dfs(t.root, 0)
}
```

---

## Pattern 2: Word Search II (Trie + Grid Backtracking)

```go
// Trie + DFS trên grid — tìm tất cả words từ wordList có trong grid
// Không search từng word riêng → O(4^(m×n) × W) 
// Dùng Trie → O(4^(m×n) × L) với L = max word length

var result []string

func dfs(node *TrieNode, r, c int, board [][]byte) {
    if node.isEnd {
        result = append(result, node.word)
        node.isEnd = false  // avoid duplicate
    }
    if r < 0 || r >= rows || c < 0 || c >= cols { return }
    ch := board[r][c]
    if ch == '#' || node.children[ch-'a'] == nil { return }

    board[r][c] = '#'  // mark visited
    next := node.children[ch-'a']
    dirs := [][]int{{0,1},{0,-1},{1,0},{-1,0}}
    for _, d := range dirs { dfs(next, r+d[0], c+d[1], board) }
    board[r][c] = ch   // restore
}
```

---

## Trie với Map (Flexible Keys)

Khi key không phải lowercase a-z:

```go
// General Trie với map (supports any character)
type TrieNode struct {
    children map[rune]*TrieNode
    isEnd    bool
}

// Dùng khi: unicode, numbers, longer alphabets
// Tradeoff: slower (map lookup) vs [26] array (O(1))
```

---

## Nhận Ra Pattern

| Signal | Trie usage |
|--------|-----------|
| "startsWith", "prefix search" | Basic Trie |
| "word dictionary" + exact/wildcard | Trie + DFS |
| "autocomplete", "type-ahead" | Trie traversal |
| "find all words in grid" | Trie + Grid DFS |
| "count words with prefix" | Trie + count field |
| "longest word in dictionary" | Trie + BFS/DFS |

---

## ✅ Ưu Điểm

- **O(L) search/insert** — L = word length, independent of n (number of words)
- **Prefix queries**: trivially answered
- **Space sharing**: common prefixes stored once
- **Pattern matching with wildcards**: natural DFS

## ❌ Nhược Điểm / Giới Hạn

- **O(n×L) space** — có thể lớn với nhiều words, long words
- **[26] children array**: 26 pointers per node dù phần lớn null → memory heavy
- Chậm hơn Hash Set cho exact match (Hash Set: O(L) average, simpler)
- Không hỗ trợ fuzzy search (Levenshtein distance)

---

## Trade-off vs Alternatives

| | Trie | Hash Set | Sorted List + BS |
|---|---|---|---|
| **Exact search** | O(L) | O(L) avg | O(L log n) |
| **Prefix search** | O(P) ✅ | O(n×L) ❌ | O(P + log n) |
| **Wildcard** | O(L × 26^depth) | ❌ | ❌ |
| **Space** | O(n×L×26) | O(n×L) | O(n×L) |
| **Insert** | O(L) | O(L) | O(log n) |

> **Kết luận**: Prefix queries → Trie. Chỉ exact search → Hash Set. Sorted prefix range → Binary Search trên sorted list.

---

## Bài Tiêu Biểu

| Bài | Pattern | Key |
|-----|---------|-----|
| Implement Trie | Basic | Insert/Search/StartsWith |
| Design Add and Search Words | Wildcard | DFS on '.' |
| Word Search II | Trie + Grid DFS | Trie prunes invalid paths |

---

## 📌 Tóm tắt

```
Trie (Prefix Tree)
│
├── Structure: TrieNode{children[26], isEnd}
│
├── Operations
│   ├── Insert: O(L) — walk/create nodes
│   ├── Search: O(L) — walk, check isEnd
│   └── StartsWith: O(P) — walk prefix only
│
├── Patterns
│   ├── Basic: prefix dictionary
│   ├── Wildcard: DFS at '.' nodes
│   └── Grid search: Trie + backtracking DFS
│
├── ✅ O(L) prefix queries — fastest for prefix search
├── ❌ O(n×L×26) space, complex vs Hash Set
│
└── vs Hash Set: Trie wins on PREFIX, HashSet wins on EXACT only
```

## Tags

#trie #prefix-tree #string #word-search #interview-prep
