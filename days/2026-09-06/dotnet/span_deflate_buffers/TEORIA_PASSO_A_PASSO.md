# Teoria passo a passo — Span deflate buffers (DN-SPAN)

## 1. O que estamos construindo

Um parser **DEFLATE stored block** (RFC 1951, BTYPE=00) em C# com `ReadOnlySpan<byte>`: ler header (BFINAL/BTYPE + LEN/NLEN), validar complemento, copiar payload sem `MemoryStream`. APIs em `Program.cs`: `DeflateStored.ReadStoredHeader`, `DeflateStored.InflateStored`. O `Main` monta o bloco com `BuildStoredBlock` e asserta round-trip + truncamento.

TODOs: `DN-SPAN-01` (header), `DN-SPAN-02` (inflate via Span), `DN-SPAN-03` (LEN/NLEN).

## 2. Por que stored antes de fixed/dynamic

Stored é o bloco “copia literal” — layout fixo de 5 bytes + payload. Ensina alinhamento, endianness LE16, validação de complemento e zero-copy com `Span` sem Huffman. Gzip/zlib reais misturam stored e compressed; entender stored desbloqueia debugging de dumps hex.

## 3. Layout do bloco stored

```text
offset | tamanho | campo
-------|---------|---------------------------
0      | 1       | header bits: BFINAL | BTYPE
1..2   | 2       | LEN  (u16 little-endian)
3..4   | 2       | NLEN (u16 LE) = ~LEN (bit a bit)
5..    | LEN     | payload literal
```

No lab, `BuildStoredBlock` emite `block[0] = 0x01` → BFINAL=1, BTYPE=00.

### Trace — payload `"LOWLEVEL"` (8 bytes)

```text
LEN  = 8     → bytes 08 00
NLEN = ~8    → 0xFFF7 → bytes F7 FF
block =
  01 | 08 00 | F7 FF | 4C 4F 57 4C 45 56 45 4C
```

Checagem: `(ushort)(8 ^ 0xFFF7) == 0xFFFF`.

## 4. Header — `ReadStoredHeader` (`DN-SPAN-01` + parte de `DN-SPAN-03`)

### O quê
```csharp
int ReadStoredHeader(ReadOnlySpan<byte> input, out int dataOffset, out int length)
```
Define `dataOffset=5`, `length=LEN`; lança `InvalidDataException` se truncado, BTYPE≠00 ou LEN/NLEN inválidos. Retorno = `dataOffset` (como no gabarito).

### Como
```text
se input.Length < 5 → InvalidDataException("truncated stored header")
header ← input[0]
BTYPE ← (header >> 1) & 0x03
se BTYPE ≠ 0 → "not stored block"
LEN  ← input[1] | (input[2] << 8)
NLEN ← input[3] | (input[4] << 8)
se (ushort)(LEN ^ NLEN) ≠ 0xFFFF → "len/nlen mismatch"
dataOffset ← 5; length ← LEN
retornar dataOffset
```

### Por quê `(header >> 1) & 0x03`
Bit 0 = BFINAL; bits 1–2 = BTYPE. Máscara `header & 0x03` **errada** — pega BFINAL+bit1, não BTYPE puro. O gabarito usa shift.

### Por quê LEN ⊕ NLEN = 0xFFFF
RFC exige NLEN = complemento de um de LEN. Detecta corrupção de dois bytes sem checksum completo do bloco.

### Invariantes
- Precisa ≥ 5 bytes antes de ler LEN/NLEN.
- Só BTYPE stored (00).
- `dataOffset` sempre 5 neste subset (sem bit buffer multi-bloco).

### Bugs comuns
- `(header & 0x03)` em vez de `>> 1`.
- Big-endian em LEN.
- Aceitar header curto.

## 5. Inflate — `InflateStored` (`DN-SPAN-02` + `DN-SPAN-03`)

### O quê
Aloca `byte[length]`, copia `input.Slice(dataOffset, length)` via `CopyTo`. Lança se payload truncado.

### Como
```text
ReadStoredHeader → dataOffset, length
se input.Length < dataOffset + length → "truncated stored payload"
output ← new byte[length]
input.Slice(dataOffset, length).CopyTo(output)
retornar output
```

### Por quê Span
`ReadOnlySpan<byte>` permite passar `block.AsSpan(0,3)` no teste de truncamento sem alocar subarray. Uma alocação de saída — não há cópias intermediárias do input.

### Trace — truncamento

```text
InflateStored(block.AsSpan(0, 3))
Length=3 < 5 → InvalidDataException no header
Main captura e segue → "OK deflate stored"
```

### Invariantes
- Round-trip: inflate(BuildStoredBlock(p)) == p.
- Truncado → `InvalidDataException`, nunca sucesso silencioso.
- LEN/NLEN já validados no header antes da cópia.

### Bugs comuns
- Copiar sem checar `dataOffset + length`.
- Usar `ToArray()` no span inteiro (inclui header).
- Ignorar NLEN (aceita LEN mentiroso).

## 6. Fluxo mental

```text
BuildStoredBlock(payload)
        │
        ▼
ReadStoredHeader ──► dataOffset=5, length=LEN
        │              (+ valida BTYPE, LEN/NLEN)
        ▼
Slice + CopyTo ──► byte[] plaintext
```

## 7. Complexidade

| Operação | Tempo | Alocações |
|----------|-------|-----------|
| ReadStoredHeader | O(1) | 0 |
| InflateStored | O(LEN) | 1 array saída |

## 8. Comparação com produção

| Este lab | `System.IO.Compression` |
|----------|-------------------------|
| só stored | DeflateStream completo |
| Span manual | buffers internos |
| 1 bloco BFINAL | multi-bloco |

## 9. Passo a passo guiado

1. `DN-SPAN-01` — parse header + BTYPE.
2. `DN-SPAN-03` — checagem LEN/NLEN (no header).
3. `DN-SPAN-02` — Slice/CopyTo + truncamento de payload.
4. `dotnet run` em `starter/` → `OK deflate stored`.

## 10. Como saber se está correto

- Inflate de `"LOWLEVEL"` idêntico.
- Span de 3 bytes → `InvalidDataException`.
- NLEN corrompido (scratch) → mismatch.

## 11. Invariantes globais

- Namespace `Chris.IlLab`; TFM `net8.0`.
- Exceções: `InvalidDataException` (não `Exception` genérica no parser).
- `BuildStoredBlock` no `Program` já correto — não altere o fixture.

## 12. Bugs comuns (checklist)

| Sintoma | Causa |
|---------|--------|
| `not stored block` com `0x01` | máscara BTYPE errada |
| inflate mismatch | endian LEN ou offset ≠ 5 |
| truncado aceito | sem `Length < 5` / sem check payload |
| len/nlen mismatch no bom | comparou `!=` com tipo signed errado |

## 13. Por quê este módulo existe

Treinar **parse defensivo zero-copy** no mesmo formato que gzip usa por baixo. Cada TODO evita aceitar bloco truncado ou LEN mentiroso — classe de bug que vira CVE em parsers binários.
