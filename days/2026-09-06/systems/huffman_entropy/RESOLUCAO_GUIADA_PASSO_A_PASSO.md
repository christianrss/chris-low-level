# RESOLUÇÃO GUIADA — Systems / Huffman entropy codec

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `COMP-HUF-01` | `starter/bit_io.cpp` | `write_bit` / `flush` / `read_bit` |
| `COMP-HUF-02` | `starter/huffman.cpp` | `build_huffman_codes` |
| `COMP-HUF-03` | `starter/huffman.cpp` | `encode_huffman` |
| `COMP-HUF-04` | `starter/huffman.cpp` | `decode_huffman` |

IDs: `TODO [ID]` no starter, `PEDAGOGY-SOLUTION` no gabarito, `PEDAGOGY-TEST` em `starter/test_huffman.cpp`.

> Trabalhe em `days/2026-09-06/systems/huffman_entropy/starter/`. Consulte `solutions/` só depois.

---

## COMP-HUF-01 — BitWriter / BitReader MSB-first

### 1. O problema (starter stub)

Em `starter/bit_io.cpp`, `write_bit`/`flush`/`read_bit` estão vazios; `write_bits` já chama `write_bit` do MSB ao LSB. Caso 1 espera `0xB0`.

```cpp
void BitWriter::write_bit(bool bit) {
    // TODO [COMP-HUF-01]: empilhar bit MSB-first no acumulador e flush a cada 8 bits
    (void)bit;
}
void BitWriter::flush() {
    // TODO [COMP-HUF-01]: alinhar último byte parcial à esquerda (MSB)
}
bool BitReader::read_bit(bool& out) {
    // TODO [COMP-HUF-01]: ler próximo bit MSB-first do stream
    (void)out;
    return false;
}
```

### 2. O algoritmo

```text
write_bit: acc=(acc<<1)|bit; se 8 bits → push e zerar
flush: se parcial, acc<<=(8-k); push
read_bit: carregar byte; out=(current&0x80); current<<=1
```

### 3. Código completo

```cpp
void BitWriter::write_bit(bool bit) {
    acc_ = static_cast<std::uint8_t>((acc_ << 1) | (bit ? 1u : 0u));
    ++bits_in_acc_;
    if (bits_in_acc_ == 8) {
        bytes_.push_back(acc_);
        acc_ = 0;
        bits_in_acc_ = 0;
    }
}

void BitWriter::flush() {
    if (bits_in_acc_ > 0) {
        acc_ = static_cast<std::uint8_t>(acc_ << (8 - bits_in_acc_));
        bytes_.push_back(acc_);
        acc_ = 0;
        bits_in_acc_ = 0;
    }
}

bool BitReader::read_bit(bool& out) {
    if (bits_left_in_byte_ == 0) {
        if (byte_index_ >= data_.size()) return false;
        current_ = data_[byte_index_++];
        bits_left_in_byte_ = 8;
    }
    out = (current_ & 0x80u) != 0;
    current_ = static_cast<std::uint8_t>(current_ << 1);
    --bits_left_in_byte_;
    return true;
}
```

### 4. Por que funciona? (entenda linha a linha)

- Shift+OR empilha o bit; após 8 pushes o primeiro bit escrito está no MSB.
- `flush` alinha à esquerda: `1011` → `10110000` = `0xB0`.
- Reader mascara `0x80` e shift left — espelho do writer.

### 5. Verificação cmake/ctest

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\huffman_entropy\starter
cmake -S . -B build
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Suite ainda FAIL (huffman stub); Caso 1 passa se só bit I/O estiver certo.

---

## COMP-HUF-02 — build_huffman_codes

### 1. O problema (starter stub)

```cpp
bool build_huffman_codes(const std::uint32_t freq[256], std::vector<HuffmanCodeEntry>& table) {
    table.clear();
    // TODO [COMP-HUF-02]: construir árvore Huffman e gerar tabela de códigos MSB-first
    (void)freq;
    return false;
}
```

### 2. O algoritmo

Folhas com freq>0 → min-heap → unir pares até 1 raiz; se 1 símbolo, embrulhar numa raiz; DFS left=0/right=1; `code = prefix<<(16-len)`; sort por symbol.

### 3. Código completo

No topo de `starter/huffman.cpp`, além de `huffman.hpp`/`bit_io.hpp`, inclua `<algorithm>`, `<cstring>`, `<queue>`, `<vector>`. Depois:

```cpp
namespace {
struct Node {
    std::uint8_t symbol = 0;
    std::uint32_t freq = 0;
    Node* left = nullptr;
    Node* right = nullptr;
    bool leaf = false;
};
struct NodeCompare {
    bool operator()(const Node* a, const Node* b) const { return a->freq > b->freq; }
};
void collect_codes(const Node* node, std::uint32_t prefix, int depth,
                   std::vector<HuffmanCodeEntry>& out) {
    if (!node) return;
    if (node->leaf) {
        HuffmanCodeEntry e;
        e.symbol = node->symbol;
        e.bit_length = static_cast<std::uint8_t>(depth == 0 ? 1 : depth);
        e.code = static_cast<std::uint16_t>(prefix << (16 - e.bit_length));
        out.push_back(e);
        return;
    }
    collect_codes(node->left, prefix << 1, depth + 1, out);
    collect_codes(node->right, (prefix << 1) | 1u, depth + 1, out);
}
void free_tree(Node* node) {
    if (!node) return;
    free_tree(node->left);
    free_tree(node->right);
    delete node;
}
}  // namespace

bool build_huffman_codes(const std::uint32_t freq[256], std::vector<HuffmanCodeEntry>& table) {
    table.clear();
    std::priority_queue<Node*, std::vector<Node*>, NodeCompare> pq;
    for (int i = 0; i < 256; ++i) {
        if (freq[i] == 0) continue;
        auto* n = new Node();
        n->symbol = static_cast<std::uint8_t>(i);
        n->freq = freq[i];
        n->leaf = true;
        pq.push(n);
    }
    if (pq.empty()) return false;
    if (pq.size() == 1) {
        Node* only = pq.top(); pq.pop();
        auto* root = new Node();
        root->freq = only->freq;
        root->left = only;
        pq.push(root);
    }
    while (pq.size() > 1) {
        Node* a = pq.top(); pq.pop();
        Node* b = pq.top(); pq.pop();
        auto* parent = new Node();
        parent->freq = a->freq + b->freq;
        parent->left = a;
        parent->right = b;
        pq.push(parent);
    }
    Node* root = pq.top();
    collect_codes(root, 0, 0, table);
    free_tree(root);
    std::sort(table.begin(), table.end(),
              [](const HuffmanCodeEntry& a, const HuffmanCodeEntry& b) { return a.symbol < b.symbol; });
    return !table.empty();
}
```

### 4. Por que funciona? (entenda linha a linha)

- Min-heap via `freq >`.
- Wrap de símbolo único → `bit_length ≥ 1`.
- `prefix<<(16-len)` alinha o código ao bit 15 para o frame CHHUF.

### 5. Verificação

Rebuild/`ctest`: Caso 2 (`PEDAGOGY-TEST: COMP-HUF-02`) exige tabela não vazia. Casos 3–4 ainda FAIL.

---

## COMP-HUF-03 — encode_huffman

### 1. O problema (starter stub)

```cpp
bool encode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-HUF-03]: contar frequências, serializar header CHHUF + tabela + bitstream
    (void)input;
    return false;
}
```

### 2. O algoritmo

Contar freq → build → lookup → `write_bits(code>>(16-len), len)` → flush → `CHHUF|len LE32|n LE16|entries|payload`.

### 3. Código completo

```cpp
bool encode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    std::uint32_t freq[256] = {};
    for (std::uint8_t b : input) ++freq[b];
    std::vector<HuffmanCodeEntry> table;
    if (!build_huffman_codes(freq, table)) return false;
    HuffmanCodeEntry lookup[256] = {};
    for (const auto& e : table) lookup[e.symbol] = e;
    BitWriter writer;
    for (std::uint8_t b : input) {
        const auto& e = lookup[b];
        writer.write_bits(e.code >> (16 - e.bit_length), e.bit_length);
    }
    writer.flush();
    const auto& payload = writer.bytes();
    out.clear();
    out.insert(out.end(), CHHUF_MAGIC, CHHUF_MAGIC + 5);
    const std::uint32_t len = static_cast<std::uint32_t>(input.size());
    out.push_back(static_cast<std::uint8_t>(len & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 24) & 0xFF));
    const std::uint16_t n = static_cast<std::uint16_t>(table.size());
    out.push_back(static_cast<std::uint8_t>(n & 0xFF));
    out.push_back(static_cast<std::uint8_t>((n >> 8) & 0xFF));
    for (const auto& e : table) {
        out.push_back(e.symbol);
        out.push_back(e.bit_length);
        out.push_back(static_cast<std::uint8_t>((e.code >> 8) & 0xFF));
        out.push_back(static_cast<std::uint8_t>(e.code & 0xFF));
    }
    out.insert(out.end(), payload.begin(), payload.end());
    return true;
}
```

### 4. Por que funciona? (entenda linha a linha)

- `code>>(16-len)` entrega só os bits úteis a `write_bits`.
- `flush` obrigatório antes de copiar `bytes()`.
- Entradas: sym, len, code hi/lo (MSB do code no primeiro byte).

### 5. Verificação

Caso 3 (`COMP-HUF-03`): encode true. Sem decode, Caso 4 FAIL.

```powershell
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

---

## COMP-HUF-04 — decode_huffman

### 1. O problema (starter stub)

```cpp
bool decode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    // TODO [COMP-HUF-04]: reconstruir árvore a partir da tabela e decodificar bit a bit
    (void)input;
    return false;
}
```

### 2. O algoritmo

Validar magic/size → ler len,n → inserir cada code bit15→folha no trie → `BitReader` no resto → emitir exatamente `len` símbolos.

### 3. Código completo

```cpp
bool decode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    if (input.size() < 11 || std::memcmp(input.data(), CHHUF_MAGIC, 5) != 0) return false;
    std::uint32_t len = 0;
    len |= input[5];
    len |= static_cast<std::uint32_t>(input[6]) << 8;
    len |= static_cast<std::uint32_t>(input[7]) << 16;
    len |= static_cast<std::uint32_t>(input[8]) << 24;
    const std::uint16_t n =
        static_cast<std::uint16_t>(input[9] | (static_cast<std::uint16_t>(input[10]) << 8));
    std::size_t p = 11;
    if (p + n * 4 > input.size()) return false;
    struct DecodeNode { int left = -1, right = -1, symbol = -1; };
    std::vector<DecodeNode> nodes(1);
    for (std::uint16_t i = 0; i < n; ++i) {
        const std::uint8_t sym = input[p++];
        const std::uint8_t bit_len = input[p++];
        const std::uint16_t code =
            static_cast<std::uint16_t>((static_cast<std::uint16_t>(input[p]) << 8) | input[p + 1]);
        p += 2;
        int node = 0;
        for (int b = 0; b < bit_len; ++b) {
            const bool bit = ((code >> (15 - b)) & 1u) != 0;
            if (bit) {
                if (nodes[node].right < 0) {
                    nodes[node].right = static_cast<int>(nodes.size());
                    nodes.push_back({});
                }
                node = nodes[node].right;
            } else {
                if (nodes[node].left < 0) {
                    nodes[node].left = static_cast<int>(nodes.size());
                    nodes.push_back({});
                }
                node = nodes[node].left;
            }
        }
        nodes[node].symbol = sym;
    }
    BitReader reader(std::span<const std::uint8_t>(input.data() + p, input.size() - p));
    out.reserve(len);
    while (out.size() < len) {
        int node = 0;
        while (nodes[node].symbol < 0) {
            bool bit = false;
            if (!reader.read_bit(bit)) return false;
            node = bit ? nodes[node].right : nodes[node].left;
            if (node < 0) return false;
        }
        out.push_back(static_cast<std::uint8_t>(nodes[node].symbol));
    }
    return out.size() == len;
}
```

### 4. Por que funciona? (entenda linha a linha)

- `(code>>(15-b))` casa com o alinhamento do encode.
- Parar em `orig_len` ignora padding do flush.
- `enc[0]='X'` cai no `memcmp` → false.

### 5. Verificação cmake/ctest

```powershell
cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Esperado: `OK huffman`. Gabarito:

```powershell
cd E:\Aulas\low-level-unified-portfolio\days\2026-09-06\systems\huffman_entropy\solutions
cmake -S . -B build && cmake --build build --config Release
ctest --test-dir build -C Release --output-on-failure
```

Starter sem TODOs: FAIL intencional.

---

## Mapa de consistência auditada

- `COMP-HUF-01` — `starter/bit_io.cpp` → `solutions/bit_io.cpp`
- `COMP-HUF-02` — `starter/huffman.cpp` → `solutions/huffman.cpp`
- `COMP-HUF-03` — `starter/huffman.cpp` → `solutions/huffman.cpp`
- `COMP-HUF-04` — `starter/huffman.cpp` → `solutions/huffman.cpp`

## Relatório de resolução

### O que foi validado

- TODOs `COMP-HUF-01..04` com bit I/O MSB-first, árvore, frame `CHHUF` e decode por trie.
- `starter/test_huffman.cpp` (Casos 1–4 / `PEDAGOGY-TEST`) passa após a implementação.
- Starter original falha até cada ID ser preenchido.

### Armadilhas encontradas

- Flush sem shift left → `0x0B` em vez de `0xB0`.
- Símbolo único sem wrap → length 0.
- Decode até EOF de bits interpreta padding como dados.

### Depuração e saída esperada

- Isole Caso 1; imprima `(sym,len,code)`; hexdump header; só então round-trip.
- Saída: `OK huffman`.

### Próximo passo sugerido

Refazer sem esta resolução; registrar razões de tamanho em `BENCHMARK_GUIADO.md` → **Resultados observados**.
