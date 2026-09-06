# Teoria passo a passo — RLE byte codec (CHRLE)

## 1. O que estamos construindo

Um codec de **Run-Length Encoding** em bytes: `encode_rle` / `decode_rle` com container próprio `CHRLE`. O encoder agrupa runs de bytes idênticos em pares `(count, byte)`; o decoder valida magic, lê o comprimento original LE32 e expande os pares até recuperar exatamente `len` bytes.

TODOs do lab: `COMP-RLE-01` (encode + header), `COMP-RLE-02` (decode + magic), `COMP-RLE-03` (rejeitar truncamento).

## 2. Por que RLE antes de Huffman/LZ

RLE é o compressor mais simples que ainda força contratos de formato binário: magic, endianness, comprimento declarado vs bytes produzidos, e limites de contador (`count ∈ [1,255]`). Sem dicionário nem árvore — só varredura linear e validação defensiva.

## 3. Formato CHRLE — layout de bytes

```text
offset | tamanho | campo
-------|---------|---------------------------
0x00   | 5       | magic "CHRLE"
0x05   | 4       | orig_len (u32 little-endian)
0x09   | 2*N     | N pares (count, byte)
```

### O quê
Um arquivo/buffer autodescrito: quem abre sabe o tamanho original sem precisar do input cru.

### Como
`CHRLE_MAGIC` em `rle.hpp` é `"CHRLE"` (5 chars + NUL no array C; só os 5 primeiros vão ao fio). `orig_len` é escrito byte a byte: `len & 0xFF`, `(len>>8)&0xFF`, …

### Por quê
Sem `orig_len`, um payload truncado no meio de um run poderia parecer “válido” até o EOF. Com length, `decode_rle` exige `out.size() == len` (`COMP-RLE-03`).

### Trace manual — header para input de 10 zeros

```text
input.size() = 10
magic: 43 48 52 4C 45   ('C''H''R''L''E')
len LE32: 0A 00 00 00
```

### Invariantes
- Magic exatamente 5 bytes `CHRLE`.
- `orig_len` cabe em u32 e descreve o plaintext, não o tamanho do arquivo comprimido.
- Payload começa no offset 9.

### Bugs comuns
- Escrever `"CHRLE\0"` (6 bytes) no stream.
- Big-endian no length (`0A` no último byte em vez do primeiro).
- Usar `strlen("CHRLE")` e esquecer que o comparador do decoder usa `memcmp(..., 5)`.

## 4. Modelo de runs — pares (count, byte)

### O quê
Uma run é a maior sequência consecutiva do mesmo byte, limitada a 255.

### Como (`COMP-RLE-01`)
Índice `i` marca o início da run; `j` avança enquanto `input[j] == input[i]` e `(j - i) < 255`. Emite `count = j - i` e `input[i]`; depois `i = j`.

### Por quê o teto 255
`count` é um `uint8_t`. Runs maiores que 255 viram dois (ou mais) pares com o mesmo byte — ex.: 300×`A` → `(255,'A')` + `(45,'A')`.

### Trace manual — `"AAABBC"` → hex do payload

```text
input: 41 41 41 42 42 43
runs:  (3,A) (2,B) (1,C)
payload após header:
  03 41  02 42  01 43
```

Buffer completo:

```text
43 48 52 4C 45  06 00 00 00  03 41 02 42 01 43
```

### Invariantes
- Todo `count ≥ 1` (run vazia nunca é emitida).
- `count ≤ 255`.
- Soma dos counts = `orig_len`.

### Bugs comuns
- Loop `while (j < n && same)` sem checar `j - i < 255` → overflow de `uint8_t` ou cast errado.
- Emitir só o byte sem count (formato “paint” vs RLE).
- Tratar ASCII e binário de forma diferente — RLE é agnóstico a texto.

## 5. Encoder completo — `encode_rle` (`COMP-RLE-01`)

### O quê
`bool encode_rle(span<input>, vector& out)` limpa `out`, escreve header + runs, retorna `true`.

### Como
1. `out.clear()`
2. Inserir 5 bytes magic.
3. Empurrar LE32 de `input.size()`.
4. Varredura de runs como na seção 4.

### Por quê sempre `true` no caminho feliz
O formato RLE deste lab sempre consegue representar qualquer input (runs de 1). Falha só faria sentido se houvesse limite de memória — fora do escopo.

### Trace manual — 10 zeros

```text
i=0, j sobe até 10 (count=10 < 255)
emite 0A 00
resultado:
  CHRLE | 0A 00 00 00 | 0A 00
tamanho comprimido = 5+4+2 = 11 bytes (melhor que 10? pior: 11>10)
```

RLE **aumenta** dados sem repetição (Caso 2 dos testes: `"ABCD"` → 4 runs de count=1 → 8 bytes de payload + 9 de header = 17). Isso é esperado.

### Invariantes
- `out` começa vazio a cada chamada (não concatenar encodes).
- Após encode bem-sucedido, `out.size() >= 9`.

### Bugs comuns
- Esquecer `out.clear()` e poluir encodes anteriores.
- Usar `int` signed para `len` e depois shifts negativos.
- Cap em 256 em vez de 255 (`j - i <= 255` com cast para uint8_t = 0).

## 6. Decoder — magic e expansão (`COMP-RLE-02`)

### O quê
`decode_rle` rejeita buffers pequenos ou magic errado; senão expande pares até atingir `len`.

### Como
```text
se size < 9 ou memcmp(magic) != 0 → false
ler len LE32 dos bytes [5..8]
p = 9
enquanto p+1 < size e out.size() < len:
  count = input[p++]; value = input[p++]
  repetir value `count` vezes (parando se out.size()==len)
```

### Por quê validar magic cedo
Evita interpretar lixo como length (ex.: buffer de imagem BMP lido por engano) e dá falha previsível no Caso 3 do teste (`enc[0]='X'`).

### Trace manual — decode de `"AAABBC"` packed

```text
len=6, p=9
par (3,A) → out=[A,A,A] size=3
par (2,B) → out=[A,A,A,B,B] size=5
par (1,C) → out=[A,A,A,B,B,C] size=6 == len → ok
```

### Invariantes
- Nunca ler `input[p+1]` se `p+1 >= input.size()`.
- Não ultrapassar `len` mesmo se count for grande demais.

### Bugs comuns
- Comparar magic com `strcmp` (NUL no meio do buffer).
- Assumir que o arquivo termina exatamente no fim do último par sem checar `len`.
- Usar `signed char` e sign-extend em `value`.

## 7. Truncamento e contrato de tamanho (`COMP-RLE-03`)

### O quê
Sucesso só se `out.size() == len` após consumir o que for possível do payload.

### Como
O loop já para em `out.size() < len`. No return: `return out.size() == len`.

### Por quê
Cenários:
1. Payload curto demais → `out.size() < len` → `false`.
2. Count excessivo no último par → o `for` interno corta em `len` → se a soma dos counts for ≥ len e magic ok, pode passar; se faltar byte no meio, falha.
3. Magic ok + len mentiroso maior que o expansível → `false`.

### Trace manual — payload truncado

```text
header: CHRLE + len=6
payload só: 03 41          (faltam runs de B e C)
após decode: out=[A,A,A], size=3 ≠ 6 → false
```

### Invariantes
- `true` ⟺ plaintext recuperado tem exatamente `orig_len` bytes.
- Buffer `< 9` bytes → sempre `false`.

### Bugs comuns
- Retornar `true` sempre que magic confere.
- `return out.size() <= len` (aceita truncado).
- Não `reserve(len)` — não é bug de corretude, mas mascara OOM em labs grandes.

## 8. Fluxo mental encode → decode

```text
bytes brutos
    │
    ▼
encode_rle  ──►  [CHRLE|LE32|runs]
    │
    ▼
decode_rle  ──►  bytes brutos (ou false)
```

Round-trip nos testes: zeros×10 e `"ABCD"` devem satisfazer `dec == in`.

## 9. Complexidade e quando RLE falha

| Caso | Comportamento |
|------|----------------|
| Muitos runs longos | Comprime bem (fax, máscaras) |
| Dados aleatórios / ASCII variado | Expande (~2× no payload) |
| Tempo | O(n) encode e decode |
| Espaço extra | O(1) além da saída |

## 10. Comparação com produção

| Este lab (CHRLE) | PackBits / TIFF RLE | BMP RLE8 |
|------------------|---------------------|----------|
| count+byte sempre | literais com contadores signed | escapes 00 |
| header próprio | embutido em formato maior | DIB |
| max run 255 | similar | similar |

O aprendizado transferível é o contrato header+payload e a rejeição defensiva — não o formato em si.

## 11. Passo a passo guiado (ordem dos TODOs)

1. `COMP-RLE-01` — header + runs em `starter/rle.cpp` → `encode_rle`.
2. `COMP-RLE-02` — magic + expansão em `decode_rle`.
3. `COMP-RLE-03` — `return out.size() == len`.
4. `cmake` + `ctest` até `OK rle`.

## 12. Como saber se está correto

- Caso 1: 10 zeros → encode/decode idêntico.
- Caso 2: `"ABCD"` round-trip (mesmo expandindo).
- Caso 3: magic corrompido → `decode_rle` retorna `false`.
- Hex do Caso 1: `43 48 52 4C 45 0A 00 00 00 0A 00`.

## 13. Invariantes globais do módulo

- APIs: `encode_rle` / `decode_rle` como em `rle.hpp`.
- Magic literal `CHRLE` (5 bytes no fio).
- Length always LE32.
- Runs `(count,byte)` com `1 ≤ count ≤ 255`.
- Decode falha em magic ruim ou `out.size() != len`.

## 14. Bugs comuns (checklist rápido)

| Sintoma | Causa típica |
|---------|----------------|
| `FAIL encode_rle(in, enc)` | stub ainda retorna `false` (`COMP-RLE-01`) |
| Round-trip quebra em run longa | cap 255 ausente |
| `!decode` em buffer bom | magic 6 bytes / LE errado |
| Aceita magic `XHRLE` | `memcmp` esquecido (`COMP-RLE-02`) |
| Aceita payload curto | sem `out.size()==len` (`COMP-RLE-03`) |
| Decode lê fora do buffer | loop sem `p+1 < size` |

## 15. Por quê este módulo existe

Conectar varredura linear simples a um **contrato binário verificável**. Cada TODO protege uma propriedade que, em compressores reais, vira CVE ou corrupção silenciosa se ignorada: header malformado, truncamento, contador overflow.
