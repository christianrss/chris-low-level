# Teoria passo a passo — Tensor entropy lab (AI-ENT)

## 1. O que estamos construindo

Um laboratório Python puro (stdlib) que mede **entropia de Shannon** em bytes, compacta um tensor 1D com **RLE** `(valor, contagem)` e compara a razão de tamanho com **gzip**. Sem NumPy, sem PyTorch — só `Counter`, `math.log2` e `gzip.compress`.

TODOs do lab: `AI-ENT-01` (Shannon), `AI-ENT-02` (RLE + ratio), `AI-ENT-03` (ratio gzip).

## 2. Por que entropia antes de “comprimir melhor”

Entropia responde: *quantos bits, em média, este alfabeto precisa?* RLE e gzip respondem: *quantos bytes o codec realmente gasta?* O gap entre \(H \times N\) e o tamanho comprimido revela estrutura (LZ77) ou overhead de formato — o mesmo raciocínio usado ao escolher quantização, dtype e codec de checkpoint.

## 3. Entropia de Shannon — bits por byte (`AI-ENT-01`)

### O quê
\[
H = -\sum_b p(b)\, \log_2 p(b)
\]
com \(p(b) = \text{count}(b) / N\). Resultado em **bits/byte**. Máximo teórico para bytes: 8.0 (uniforme sobre 256 símbolos).

### Como
1. Se `data` vazio → `0.0`.
2. `Counter(data)` → frequências só dos símbolos presentes.
3. Para cada `count`: `p = count / n`; acumule `-p * math.log2(p)`.
4. Não itere `range(256)` — símbolos ausentes têm \(p=0\) e não entram na soma.

### Por quê
H é limite inferior de compressão **sem memória** (só frequência marginal). Gzip pode ficar abaixo de \(H\times N/8\) em bytes quando há correlação espacial — isso não “quebra Shannon”; o modelo i.i.d. é incompleto.

### Trace manual — 4 símbolos equiprováveis

```text
data = [0,1,2,3] × 25   → N = 100
cada símbolo: count=25 → p=0.25
log2(0.25) = -2
contribuição por símbolo: -0.25 × (-2) = 0.5
H = 4 × 0.5 = 2.0 bits/byte
```

### Trace manual — run constante

```text
data = AAAA  (N=4, 1 símbolo)
p=1.0, log2(1)=0 → H=0.0
```

### Invariantes
- `0 ≤ H ≤ 8` para `bytes`.
- k símbolos exclusivos equiprováveis → `H = log2(k)`.
- Entrada vazia → `0.0` (convenção do lab; evita divisão por zero).

### Bugs comuns
- `math.log` (natural) em vez de `log2` → H escala errada.
- Iterar bytes ausentes e fazer `log2(0)` → `nan`.
- Dividir por 256 fixo em vez de `len(data)`.

## 4. RLE de tensor 1D (`AI-ENT-02`)

### O quê
`tensor_rle_encode(tensor: list[int]) → list[tuple[int,int]]` agrupa runs adjacentes em `(valor, contagem)`. Modelo de tamanho: raw = `len×4` (int32); RLE = `len(pairs)×8` (int32+int32).

### Como
```text
se tensor vazio → []
current ← tensor[0]; run ← 1
para cada value em tensor[1:]:
  se value == current: run++
  senão: emitir (current, run); current←value; run←1
emitir (current, run)   ← obrigatório após o loop
```

`compression_ratio_rle` = `tensor_rle_size_bytes / raw_tensor_size_bytes` (raw=0 → `1.0`).

### Por quê
Máscaras de segmentação, padding e one-hot esparsos são runs. RLE é o primeiro estágio em formatos médicos e em codecs de feature maps — barato de auditar e de comparar com DEFLATE.

### Trace manual — teste oficial

```text
tensor = [7]×1000 + [3]×500
pairs  = [(7,1000), (3,500)]
raw    = 1500 × 4 = 6000
rle    = 2 × 8 = 16
ratio  = 16/6000 ≈ 0.00267 < 0.01  ✓
```

### Trace — sem repetição (expansão)

```text
tensor = [1,2,3,4]
pairs  = 4 × (v,1) → 32 bytes vs raw 16 → ratio = 2.0
```

### Invariantes
- Soma das contagens = `len(tensor)`.
- Lista vazia → `[]` e ratio `1.0`.
- Runs só fundem **adjacentes** iguais.

### Bugs comuns
- Esquecer o `append` final → último run some.
- Ratio com denominador errado (`len(pairs)` sem ×8).
- Cap 255 estilo CHRLE — **este lab não limita** contagem (é `int`, não `uint8`).

## 5. Razão gzip (`AI-ENT-03`)

### O quê
`compression_ratio_gzip(data) = len(gzip.compress(data)) / len(data)` (vazio → `1.0`). Menor que 1 = ganho.

### Como
```text
compressed ← gzip.compress(data)   # 1F 8B + DEFLATE + CRC32 + ISIZE
return len(compressed) / len(data)
```

### Por quê
gzip é o envelope padrão em HTTP, logs e artefatos ML. Comparar com RLE no mesmo padrão mostra quando dicionário+Huffman vence contagem de runs — e quando o modelo de tamanho RLE (int32×2) é pessimista vs bytes brutos.

### Trace manual — teste `LOWLEVEL`×500

```text
payload = b"LOWLEVEL" × 500 → 4000 bytes
gzip.compress → tipicamente dezenas de bytes (header ~10 + bloco curto)
gz_ratio < 0.2
rle_ratio = compression_ratio_rle(list(payload))
  → cada byte vira int32; runs de 'L','O',... curtas
  → muitos pares × 8 → ratio bem maior que gzip
assert gz_ratio < rle_ratio
```

### Invariantes
- Vazio → `1.0`.
- Payload repetitivo do teste → `gz_ratio < 0.2` e `< rle_ratio`.

### Bugs comuns
- Retornar `len(data)/len(compressed)` (razão invertida).
- Comparar RLE em bytes sem `list(payload)` — o teste usa `list[int]`.
- Esquecer caso vazio e dividir por zero.

## 6. Fluxo mental

```text
bytes ──► shannon_entropy ──► H bits/byte (limite i.i.d.)
list[int] ──► tensor_rle_encode ──► pairs ──► ratio_rle
bytes ──► gzip.compress ──► ratio_gzip
```

## 7. Complexidade

| Função | Tempo | Espaço extra |
|--------|-------|--------------|
| `shannon_entropy` | O(n) | O(alfabeto) ≤ 256 |
| `tensor_rle_encode` | O(n) | O(#runs) |
| `compression_ratio_gzip` | O(n) DEFLATE | buffer gzip |

## 8. Comparação com produção

| Este lab | Produção ML |
|----------|-------------|
| `list[int]` + RLE toy | safetensors / zstd / blosc |
| Shannon empírico | estimadores em batches |
| `gzip.compress` one-shot | streaming / nível 1–9 |

O transferível é **medir antes de escolher codec**, não o formato RLE em si.

## 9. Passo a passo guiado (ordem dos TODOs)

1. `AI-ENT-01` — `shannon_entropy` em `starter/entropy_lab.py`.
2. `AI-ENT-02` — `tensor_rle_encode` + `compression_ratio_rle`.
3. `AI-ENT-03` — `compression_ratio_gzip`.
4. `python starter/test_entropy_lab.py` → `OK tensor entropy lab`.

## 10. Como saber se está correto

- Caso 1: `bytes([0,1,2,3]*25)` → `|H-2.0| < 1e-6`.
- Caso 2: pairs `[(7,1000),(3,500)]` e ratio `< 0.01`.
- Caso 3: `b"LOWLEVEL"*500` → gzip `< 0.2` e `<` RLE.

## 11. Invariantes globais do módulo

- APIs exatamente como em `starter/entropy_lab.py` / `solutions/entropy_lab.py`.
- Helpers `tensor_rle_size_bytes` / `raw_tensor_size_bytes` já implementados — use-os no ratio.
- Entradas vazias: H=`0.0`; ratios=`1.0`.

## 12. Bugs comuns (checklist)

| Sintoma | Causa típica |
|---------|----------------|
| `NotImplementedError` | stub ainda ativo |
| H≈1.386 em uniforme 4 | usou `log` natural |
| pairs sem último run | falta append pós-loop |
| ratio RLE ≥ 0.01 no Caso 2 | encode errado ou ratio invertido |
| gzip ≥ 0.2 | não chamou `gzip.compress` |

## 13. Por quê este módulo existe

Ligar teoria da informação a **implementações verificáveis** de compressão. Cada `TODO [ID]` protege uma propriedade que, em pipelines ML, vira métrica mentirosa ou escolha de codec sem evidência.
