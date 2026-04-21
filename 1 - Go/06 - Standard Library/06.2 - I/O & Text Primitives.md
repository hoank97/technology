---

parent:: [[06 - Standard Library]]

---

# 06.2 I/O & Text Primitives

## io — Reader & Writer

`io` package định nghĩa các interface nền tảng của Go I/O system:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
type Writer interface {
    Write(p []byte) (n int, err error)
}
type Closer interface {
    Close() error
}
// Combo interfaces
type ReadCloser interface {
    Reader
    Closer
}
```

> Mọi thứ trong Go I/O đều xoay quanh `Reader`/`Writer` — file, network, buffer, pipe đều implement interface này.

### Read byte-by-byte (inefficient — tránh trong production)

```go
data, err := io.ReadAll(os.Stdin)       // ⚠️ allocate toàn bộ vào memory
_, err = io.Copy(os.Stdout, os.Stdin)    // ⚠️ copy toàn bộ

// ✅ Efficient: buffer theo chunk
buf := make([]byte, 32*1024)
io.CopyBuffer(os.Stdout, os.Stdin, buf)
```

### Copy — chi tiết

```go
// Copy từ reader → writer, tự động loop cho đến EOF
n, err := io.Copy(dst, src)

// CopyN giới hạn số byte
n64, err := io.CopyN(dst, src, 1024)

// CopyBuffer — reuse buffer để tránh allocate
buf := make([]byte, 64*1024)
io.CopyBuffer(writer, reader, buf)
```

### Pipe — in-memory pipeline

```go
// Pipe tạo synchronous in-memory connection
// Reader end ← goroutine writes → Writer end
pr, pw := io.Pipe()

go func() {
    defer pw.Close()
    // Write blocking — khi Read side đọc thì Write mới unblock
    pw.Write([]byte("data"))
}()

buf, _ := io.ReadAll(pr) // pr.Read() unblocks khi pw.Write() xong
```

### LimitReader — bounded read

```go
// Giới hạn đọc tối đa N bytes
limited := io.LimitReader(src, 1024) // ⚠️ trả về Reader, không panic khi over-limit
// Đọc >1024 bytes → trả về io.EOF sau khi đọc đủ
```

### MultiReader — read from multiple sources

```go
r1 := strings.NewReader("first")
r2 := strings.NewReader("second")
mr := io.MultiReader(r1, r2)

// Read() trả về data từ r1 trước, đến EOF rồi chuyển r2
data, _ := io.ReadAll(mr) // "firstsecond"
```

### MultiWriter — write to multiple destinations

```go
f, _ := os.Create("log.txt")
mw := io.MultiWriter(os.Stdout, f) // stdout + file cùng lúc

mw.Write([]byte("logged")) // ghi cả ra console lẫn file
```

### TeeReader — read + capture

```go
// Đọc từ reader, đồng thời copy vào writer
tr := io.TeeReader(src, dst)
// Đọc trả về data từ src, nhưng mỗi byte cũng được write vào dst
```

### SectionReader — slice của reader

```go
f, _ := os.Open("big.bin")
section := &io.SectionReader{
    R: f,
    Off: 100,
    N:  50,
}
// Đọc từ offset 100, tối đa 50 bytes
```

### ReableFrom / WriteTo — optimized interfaces

```go
// Nếu type implement ReadFrom → io.Copy dùng nó thay vì buffer loop
// os.File implement ReadFrom → OS-level sendfile(2), tránh user-space copy

// Tương tự WriteTo — type có thể write trực tiếp ra writer
// net.Conn implement WriteTo → zero-copy network send
```

---

## bufio — Buffered I/O

### bufio.Reader

```go
r := bufio.NewReader(file)

// ReadByte — đọc 1 byte, cache trong buffer
b, _ := r.ReadByte()

// ReadBytes(delim) — đọc đến delimiter
line, _ := r.ReadBytes('\n')

// ReadString(delim) — tương tự nhưng trả về string
line, _ := r.ReadString('\n')

// Peek(n) — nhìn trước n bytes mà không consume
peek, _ := r.Peek(4) // xem magic bytes của file

// ReadSlice(delim) — đọc đến delim (hữu ích cho line-by-line)
line, err := r.ReadSlice('\n') // ⚠️ có thể return ErrBufferFull

// Discard(n) — skip n bytes
r.Discard(1024)
```

### bufio.Writer

```go
w := bufio.NewWriter(file)

// WriteString — ghi string mà không cần convert sang []byte
w.WriteString("line\n")

// WriteByte, WriteRune

// Flush — bắt buộc ghi buffer ra disk/conn
w.Flush()

// Available() — xem còn bao nhiêu buffer trống
// Buffered() — xem bao nhiêu bytes trong buffer
```

### bufio.Scanner — line/token scanning

```go
sc := bufio.NewScanner(os.Stdin)

// Default: split trên newline, max token = 64KB
for sc.Scan() {
    line := sc.Text()
    fmt.Println(line)
}

// Custom split function
sc.Split(bufio.ScanWords)

// Split functions:
//   ScanLines()  — mặc định
//   ScanWords()  — từng word
//   ScanRunes()  — từng rune (Unicode-safe)
//   ScanBytes()  — từng byte

// Custom split cho CSV
split := func(data []byte, atEOF bool) (advance int, token []byte, err error) {
    // Trả về token và số bytes đã advance
}
// Nếu token quá lớn → trả về token too long
// Set Buffer capacity cho large tokens
sc.Buffer(make([]byte, 0, 64*1024), maxTokenSize)
```

---

## fmt — Formatting

### Format Verbs

| Verb | Type | Output |
|------|------|--------|
| `%v` | any | Default format |
| `%+v` | struct | Field names + values |
| `%#v` | any | Go syntax (type name) |
| `%T` | any | Type of value |
| `%s` | string/[]byte | String |
| `%q` | string | Quoted string `"..."` |
| `%x` | string/[]byte | Hex `48656c6c6f` |
| `%d` | int | Decimal |
| `%b` | int | Binary |
| `%o` | int | Octal |
| `%x` / `%X` | int | Hex |
| `%f` | float | Decimal float |
| `%e` / `%E` | float | Scientific |
| `%g` / `%G` | float | Best format |
| `%p` | pointer | Hex address `0x1a2b3c` |
| `%c` | rune | Character |
| `%t` | bool | true/false |

```go
s := "hello"
fmt.Printf("%s\n", s)       // hello
fmt.Printf("%q\n", s)       // "hello"   (quoted)
fmt.Printf("%x\n", s)       // 68656c6c6f (hex)
fmt.Printf("%v\n", s)       // hello
fmt.Printf("%+v\n", s)      // hello (string không có field name)
```

### Struct formatting

```go
type Point struct{ X, Y int }
p := Point{1, 2}

fmt.Printf("%v\n", p)      // {1 2}
fmt.Printf("%+v\n", p)    // {X:1 Y:2}
fmt.Printf("%#v\n", p)    // main.Point{X:1, Y:2}
```

### Width & Precision

```go
fmt.Printf("%8d", 123)     // "     123" (width 8, right-aligned)
fmt.Printf("%-8d", 123)    // "123     " (left-aligned)
fmt.Printf("%08d", 123)    // "00000123" (zero-padded)
fmt.Printf("%.2f", 3.1415) // "3.14" (2 decimal places)
fmt.Printf("%8.2f", 3.14)  // "    3.14" (width + precision)
fmt.Printf("%[1]d %[1]d", 1) // "1 1" — reuse arg #1
```

### Flag characters

```go
fmt.Printf("%+v", point)   // +  = always show sign (+/-)
fmt.Printf("%#v", value)   // #  = alternate format (0x prefix, etc.)
fmt.Printf("% 8d", 123)     // space = positive numbers show space
fmt.Printf("%08d", 123)    // 0  = zero-padding
```

### fmt.Stringer — custom string representation

```go
// Khi một type implement String() string → fmt.Print dùng nó thay vì default
type IP struct{ Quad [4]byte }

func (ip IP) String() string {
    return fmt.Sprintf("%d.%d.%d.%d", ip.Quad[0], ip.Quad[1], ip.Quad[2], ip.Quad[3])
}

ip := IP{[4]byte{127, 0, 0, 1}}
fmt.Println(ip) // "127.0.0.1" — gọi ip.String()
```

### fmt.Scanner / fmt.State — custom parsing

```go
// fmt.Scanner — fmt.Fscan có thể parse custom type từ reader
type Point struct{ X, Y int }

func (p *Point) Scan(state fmt.ScanState, verb rune) error {
    // Đọc từ state.ReadRune()
    // Trả về error nếu parse fail
    _, err := fmt.Fscan(state, &p.X, &p.Y)
    return err
}

// fmt.Formatter — custom formatted output với fmt.Printf %v
func (p Point) Format(f fmt.State, verb rune) {
    switch verb {
    case 'v':
        if f.Flag('+') {
            fmt.Fprintf(f, "Point{X:%d, Y:%d}", p.X, p.Y)
        } else {
            fmt.Fprintf(f, "(%d,%d)", p.X, p.Y)
        }
    }
}
```

### Print functions variants

```go
// Print — stdout, no newline
fmt.Print(x)

// Println — stdout, auto newline
fmt.Println(x)

// Printf — formatted stdout
fmt.Printf("format", args)

// Fprint — write ra Writer (file, buffer, etc.)
fmt.Fprint(w, x)

// Sprintf — trả về string
s := fmt.Sprintf("hello %s", name)

// Errorf — tạo error với formatted message (không wrap, chỉ message)
err := fmt.Errorf("invalid port: %d", port)
```

### Print with alignment

```go
// fmt.Falign — tabular output với fixed width columns
fmt.Falign(os.Stdout, []string{"Name", "Age", "City"}, 20)
```

---

## strings — String manipulation

### Builder — efficient string concatenation

```go
// ⚠️ strings + concatenation tạo nhiều temporary strings
// ✅ Builder dùng byte buffer, append không allocate interim strings

var sb strings.Builder
sb.Grow(100) // pre-allocate capacity

sb.WriteString("hello")
sb.WriteByte(' ')
sb.WriteRune('w')
sb.WriteString("orld")
sb.WriteString(fmt.Sprintf(" %d", 123))

result := sb.String()   // "hello world 123"
size := sb.Len()        // current bytes
capacity := sb.Cap()    // allocated capacity
```

### Common operations

```go
// Split
parts := strings.Split("a,b,c", ",")     // ["a", "b", "c"]
fields := strings.Fields("  a  b  c  ")  // ["a", "b", "c"] (whitespace)

// Join
joined := strings.Join([]string{"a", "b", "c"}, "-") // "a-b-c"

// Replace
s := strings.Replace("hello world", "world", "go", 1)  // "hello go" (count=1)
s := strings.ReplaceAll("aaa", "a", "b")               // "bbb"
s := strings.Replace("aaaa", "a", "b", 2)               // "bbaa" (count=2)
```

### Trim & manipulation

```go
s := "  hello  "

strings.TrimSpace(s)    // "hello" (bỏ cả leading + trailing whitespace)
strings.Trim(s, " ")    // "hello" (trim specific chars)
strings.TrimLeft(s, " ")
strings.TrimRight(s, " ")

strings.TrimPrefix(s, "prefix")
strings.TrimSuffix(s, "suffix")

// TrimFunc — custom trim
trimmed := strings.TrimFunc(s, func(r rune) bool {
    return r == ' ' || r == '\n'
})
```

### Search & check

```go
strings.Contains("hello world", "world")     // true
strings.ContainsAny("abc", "xyz")             // false (any of chars)
strings.HasPrefix("hello", "he")             // true
strings.HasSuffix("hello", "lo")              // true
strings.Index("hello", "ll")                  // 2 (first index), -1 if not found
strings.LastIndex("hello l", "l")             // 6 (last index)
strings.Count("hello", "l")                   // 2

// EqualFold — case-insensitive comparison
strings.EqualFold("Hello", "hello")           // true
```

### Map & Transform

```go
// Map — apply function to each rune
upper := strings.Map(func(r rune) rune {
    if r >= 'a' && r <= 'z' {
        return r - 32
    }
    return r
}, "hello") // "HELLO"

// ToLower, ToUpper, ToTitle
strings.ToLower("HELLO") // "hello"
strings.ToUpper("hello") // "HELLO"

// Title — first letter of each word uppercase
strings.ToTitle("hello world") // "HELLO WORLD"
```

### SplitN, SplitAfter

```go
// SplitN — giới hạn số parts (part cuối = tất cả còn lại)
parts := strings.SplitN("a/b/c/d", "/", 2)    // ["a", "b/c/d"]
// SplitAfter — giữ delimiter trong mỗi part
parts = strings.SplitAfter("a/b/c", "/")      // ["a/", "b/", "c"]

// FieldsFunc — split bằng custom function
fields := strings.FieldsFunc("a,b;c", func(r rune) bool {
    return r == ',' || r == ';'              // ["a", "b", "c"]
})
```

### Reader — io.Reader interface

```go
// strings.Reader — implement io.Reader
r := strings.NewReader("hello world")
buf := make([]byte, 5)
n, _ := r.Read(buf) // buf = "hello", n = 5
// Seek — di chuyển position
r.Seek(6, io.SeekStart) // đến "world"
n, _ = r.Read(buf)       // buf = "world"
```

---

## bytes — Binary data manipulation

### Buffer — growable byte buffer

```go
var buf bytes.Buffer

// Write — ghi []byte
buf.Write([]byte("hello"))

// WriteString — ghi string (tránh allocation)
buf.WriteString(" world")

// WriteByte, WriteRune

// WriteTo — implement io.WriterTo
buf.WriteTo(os.Stdout) // ghi ra stdout

// ReadFrom — implement io.ReaderFrom (efficient cho file)
f, _ := os.Open("data.bin")
buf.ReadFrom(f)

// ByteReader — đọc từng byte mà không bỏ qua
b, _ := buf.ReadByte()
buf.UnreadByte() // push back 1 byte

// ReadBytes(delim), ReadString(delim) — giống bufio
```

### Buffer internals & allocation

```go
// Buffer pre-allocate để tránh reallocation
buf := bytes.NewBuffer(make([]byte, 0, 1024)) // capacity 1024

// Concat — join []byte slices (không allocate tạm)
joined := bytes.Join([][]byte{a, b, c}, separator)

// Clone (Go 1.21+) — copy byte slice
copy := bytes.Clone(data)
```

### Compare & search

```go
bytes.Compare(a, b)     // 0 if equal, -1 if a<b, 1 if a>b
bytes.Equal(a, b)       // true if equal (constant-time-ish)
bytes.EqualFold(a, b)  // case-insensitive

// Index, Contains, HasPrefix, HasSuffix — giống strings nhưng []byte
bytes.Index(data, []byte("pattern"))
bytes.Contains(data, []byte("needle"))
```

### Reader & Runes

```go
r := bytes.NewReader([]byte("héllo"))
r.Seek(0, io.SeekStart)

// ReadRune — Unicode-aware (handle multi-byte chars)
rune, size, _ := r.ReadRune() // 'h', size=1
rune, size, _ = r.ReadRune()  // 'é', size=2

// ReadAll — đọc toàn bộ
data, _ := io.ReadAll(bytes.NewReader(raw))
```

### Buffer in concurrency context

```go
// ⚠️ bytes.Buffer NOT safe for concurrent use
// ✅ Dùng bufio.NewWriter + sync.Mutex, hoặc channel of []byte

// sync.Pool for buffer reuse
var bufPool = sync.Pool{
    New: func() any {
        return &bytes.Buffer{}
    },
}

func write(w io.Writer, data []byte) error {
    buf := bufPool.Get().(*bytes.Buffer)
    buf.Reset()
    buf.Write(data)
    _, err := w.Write(buf.Bytes())
    bufPool.Put(buf)
    return err
}
```

---

## Trade-off: bytes.Buffer vs strings.Builder vs string concat

| Approach | Allocation | Use case |
|----------|-----------|----------|
| `+` concatenation | N intermediate strings | Only for ≤3 short strings |
| `fmt.Sprintf` | 1 allocation per call | Rare, complex formatting |
| `strings.Builder` | 1 buffer, 1 string result | Building text output |
| `bytes.Buffer` | 1 buffer, 1 []byte result | Binary data, also text |
| `strings.Join` | 1 allocation total | Joining slice of strings |

```go
// Benchmark comparison (typical results)
var s string
for i := 0; i < 100; i++ {
    s += "piece"          // ❌ O(n²) — 100 calls × ~50 bytes avg
}
// ⚠️ Never use + in loop for large output

pieces := make([]string, 100)
for i := 0; i < 100; i++ {
    pieces[i] = "piece"
}
s = strings.Join(pieces, "") // ✅ O(n) — single allocation
```

---

## 📌 Tóm tắt

```
I/O & Text Primitives
├── io — Reader/Writer interfaces
│   ├── Copy / CopyN / CopyBuffer
│   ├── Pipe — synchronous in-memory
│   ├── LimitReader — bounded read
│   └── MultiReader / MultiWriter / TeeReader
├── bufio — Buffered I/O
│   ├── Reader: ReadByte, Peek, Discard
│   ├── Writer: WriteString, Flush
│   └── Scanner: line/token scanning, custom split
├── fmt — Formatting
│   ├── Verbs: %v, %T, %s, %d, %x, %p
│   ├── Width & Precision: %8d, %.2f
│   ├── Stringer interface: custom String() for Print
│   └── Print/Fprint/Sprintf variants
├── strings — Text manipulation
│   ├── Builder: efficient concatenation
│   ├── Split/Join/Replace
│   ├── Trim/Map/Search
│   └── Reader: io.Reader over string
└── bytes — Binary manipulation
    ├── Buffer: growable binary data
    ├── Compare / Clone / Join
    └── Reader: io.Reader over []byte
```

---

## Tags

#io #fmt #strings #bytes #bufio #reader #writer #scanner #format #go