# Teoria passo a passo — CHRLE em Rust (RS-RLE)

## 1. O que estamos construindo

Um codec RLE **sem panics em bytes não confiáveis**: `encode(&[u8]) -> Vec<u8>`, `decode(&[u8]) -> Result<Vec<u8>, RleError>`, e um helper `round_trip_ok`. O wire format é idêntico ao lab C++ `systems/rle_byte_codec` (`CHRLE`), para você comparar ownership/`Result` com `bool` + `vector`.

TODOs: `RS-RLE-01` (encode), `RS-RLE-02` (decode), `RS-RLE-03` (round-trip + rejeição).

## 2. Por que Rust neste ponto do dia

Depois de implementar RLE em C++, o mesmo formato em Rust força:

- indexação só após `len` checks (sem UB se errar — panic ou `Err`, nunca silent OOB em safe Rust);
- API que **comunica falha** (`Result`) em vez de `false` opaco;
- slices emprestados (`&[u8]`) sem copiar o input até você decidir `push`.

## 3. Layout do frame CHRLE

```text
offset | size | campo
-------|------|------------------
0      | 5    | magic ASCII "CHRLE"
5      | 4    | original_len u32 little-endian
9      | 2*N  | runs: (count u8, value u8)*
```

Diagrama de um payload `AAAAB` (4×`A` + 1×`B`):

```text
+------+------+------+------+------+------+
| C H  | R L  | E    | len=5 LE32  | 04 41 | 01 42 |
|      |      |      |             | 4×A   | 1×B   |
+------+------+------+------+------+------+
 0    4      5      8             9     11 12   13
```

Hex esperado (após encode):

```text
43 48 52 4C 45   05 00 00 00   04 41   01 42
C  H  R  L  E   len=5         4×'A'  1×'B'
```

## 4. Encode — runs ≤ 255 (`RS-RLE-01`)

### O quê
Varra o input; agrupe bytes iguais com `count ∈ [1,255]`; escreva magic + LE32 + pares.

### Como
```text
out ← "CHRLE"
out ← le32(input.len())
i ← 0
enquanto i < len:
  j ← i+1
  enquanto j < len e input[j]==input[i] e (j-i) < 255:
    j++
  push (j-i) as u8, input[i]
  i ← j
```

### Por quê
Runs > 255 precisam de múltiplos pares (ex.: 300 zeros → `(255,0)+(45,0)`). Sem o teto, um `u8` overflowia.

### Trace manual — 10 zeros

```text
input = [0]*10
magic CHRLE
len LE32 = 0A 00 00 00
um único run: count=10, value=0
frame = 43 48 52 4C 45 0A 00 00 00 0A 00
```

### Invariantes
- Sempre 5 + 4 bytes de header, mesmo se `input` vazio (só magic+len=0).
- `count` nunca zero no encoder correto (loop avança pelo menos 1).

### Bugs comuns
- Escrever length big-endian.
- Esquecer o teto 255 e estourar `as u8`.
- Usar `String` em vez de bytes — magic é ASCII mas payload é binário.

## 5. Decode — bounds antes de indexar (`RS-RLE-02`)

### O quê
Validar magic e tamanho mínimo; ler `len`; expandir runs até `out.len() == len`.

### Como
```text
se input.len() < 9 → Truncated
se input[0..5] != b"CHRLE" → BadMagic
len ← u32::from_le_bytes(input[5..9])
p ← 9
enquanto p+1 < input.len() e out.len() < len:
  count, value ← input[p], input[p+1]; p += 2
  repetir count vezes (parando se out.len()==len): push value
se out.len() != len → LengthMismatch
Ok(out)
```

### Por quê
Bytes hostis podem mentir no `len` ou cortar o último par. Em C++ um `span` mal checado vira UB; em Rust safe, `input[p]` panica se `p` passar — por isso o guard `p + 1 < input.len()` **antes** de ler o par.

### Trace manual — magic corrompido

```text
frame válido; flip byte[0] para 'X'
decode → Err(BadMagic)
```

### Trace — truncado

```text
só 4 bytes → Err(Truncated)  (não tente ler magic[4])
```

### Invariantes
- Nunca indexar sem checar `len`.
- `LengthMismatch` se os runs expandem menos (ou você parou cedo) que `len`.

### Bugs comuns
- Comparar magic com `== "CHRLE"` (tipo errado) em vez de slice de bytes.
- Ignorar `LengthMismatch` e retornar `Ok` parcial.
- Usar `unwrap` em produção — o lab exige `Result`.

## 6. Round-trip (`RS-RLE-03`)

### O quê
`round_trip_ok(input) = decode(encode(input)) == Ok(input)`.

### Como
```text
enc ← encode(input)
match decode(&enc) {
  Ok(dec) => dec == input,
  Err(_) => false,
}
```

### Por quê
É o contrato de codec: se encode e decode discordam, o lab C++ e o Rust divergem e o portfolio quebra. Também documenta que decode falha em frames ruins **sem** panic.

### Trace
```text
round_trip_ok(b"AAAAABBBCC") → true
```

## 7. Ownership e empréstimo — por que `&[u8]`

`encode` e `decode` pegam **empréstimo** do buffer do caller. O `Vec` retornado é owned (caller libera). Isso evita:

- mover o input para dentro da função sem necessidade;
- lifetimes confusos — o output não aponta para o input.

### Por quê isso importa em compressão
Parsers de gzip/zlib/PNG leem janelas do mesmo buffer. O hábito de “checar bounds → fatiar → copiar só o necessário” é o mesmo padrão do lab seguinte (`gzip_member_parse`).

## 8. Tabela de erros

| Variante | Quando |
|----------|--------|
| `Truncated` | `< 9` bytes ou (conceitualmente) fim abrupto |
| `BadMagic` | primeiros 5 ≠ `CHRLE` |
| `LengthMismatch` | expandido ≠ `len` do header |

## 9. Relação com o lab C++

| C++ | Rust |
|-----|------|
| `bool encode_rle(span, vector&)` | `fn encode(&[u8]) -> Vec<u8>` |
| `bool decode_rle(...)` | `Result<Vec<u8>, RleError>` |
| magic `CHRLE_MAGIC[6]` C-string | `&[u8; 5]` sem NUL |

Mesmo algoritmo de runs; a diferença pedagógica é a superfície de erro.

## 10. Checkpoint antes de codar

No papel, monte o hex de `AAAAB` completo (14 bytes). Só então abra `starter/src/lib.rs`.

## 11. Resumo operacional

1. Encode escreve header + runs ≤255.
2. Decode valida magic/len e expande com guards.
3. Round-trip prova o contrato.
4. Nunca confie em `len` do header sem cruzar com bytes restantes.

## 12. Próximo módulo

`rust/gzip_member_parse` aplica o mesmo rigor a headers gzip reais (`1f 8b`), com flags opcionais e trailer CRC32/ISIZE.
