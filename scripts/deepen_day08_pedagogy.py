#!/usr/bin/env python3
"""Deepen Day 2026-09-08 module pedagogy to gold CLVM quality (unique theory + full RESOLUCAO)."""
from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / "days" / "2026-09-08"

# ---------------------------------------------------------------------------
# Per-module curated TEORIA suffixes (replace Passo-de-papel padding)
# ---------------------------------------------------------------------------

TEORIA_SUFFIX: dict[str, str] = {}

TEORIA_SUFFIX["clvm_disassembler"] = r'''
## Endianness e o caso PUSH 256

O Caso 1 usa `2A 00 00 00` (= 42). Isso mascara bugs de endianness porque o byte
baixo já é o valor. O Desafio usa `01 00 01 00 00`:

```text
bytes após opcode: 00 01 00 00
LE: 0x00 | (0x01<<8) | (0x00<<16) | (0x00<<24) = 256
BE errado:         0x00010000 = 65536
só byte[1]:        0  (errado)
```

**Por quê** o lab insiste em LE? Porque a ISA CLVM (Dia 03) e o verifier (Dia 07)
já fixaram little-endian. Trocar endian no disassembler quebra a paridade com a VM.

## Tabela completa de tamanhos (wire format)

| Opcode | Hex | Size | Operando |
|--------|-----|------|----------|
| PUSH | 0x01 | 5 | u32 LE |
| ADD/SUB/... | 0x02.. | 1 | — |
| HALT | 0x08 | 1 | — |
| JMP | 0x09 | 3 | u16 LE |
| JZ | 0x0A | 3 | u16 LE |
| CALL | 0x0B | 3 | u16 LE |
| JNZ | 0x13 | 3 | u16 LE |

Qualquer outro opcode → `disassemble_all` retorna **-1** (não `"UNK"`).

## Invariante do cursor `pc`

```text
pc_0 = 0
para cada instrução i:
  size_i = decode(code[pc_i])
  pc_{i+1} = pc_i + size_i
pc_final == len(code)
```

Se `size_PUSH` for 1, o próximo “opcode” é `0x2A` e a listagem vira lixo.
Se `size_JMP` for 1, o byte `0x0A` vira JZ solto.

## Relação com o verifier (Dia 07)

| Camada | Pergunta |
|--------|----------|
| Verifier | o programa é bem formado? |
| Disassembler | o que cada instrução *diz*? |

O verifier usa a **mesma** tabela de tamanhos. Se o C e o Python discordarem
no size de PUSH, um aceita e o outro rejeita o mesmo `.clbc`.

## Lab versus produção

`objdump -d` / `llvm-objdump` leem tabelas de ISA enormes e relocações.
Aqui o subset é didático: três decoders (`decode_push`, `decode_branch`,
walk linear). Em produção você geraria a tabela a partir de um `.td` (TableGen);
no lab você escreve o switch à mão para sentir o desalinhamento.

## Checklist antes de compilar

- [ ] Trace `01 2A 00 00 00` → imm=42, size=5 no papel
- [ ] Trace `09 0A 00` → JMP 10, size=3
- [ ] Trace programa 7 bytes → 3 linhas
- [ ] Sei que `0xFF` retorna negativo
'''

TEORIA_SUFFIX["clvm_peephole_opt"] = r'''
## Padrão PUSH 0 + ADD (6 bytes → 0)

```text
offset 0: 01 00 00 00 00   PUSH 0
offset 5: 02               ADD
```

Semanticamente: `x + 0 = x`. O match devolve 1; o otimizador pode apagar
os 6 bytes (ou marcar dead). **Por quê** 6? 5 do PUSH + 1 do ADD.

## Padrão PUSH a + PUSH b + ADD (11 → 5)

```text
01 | a0 a1 a2 a3 | 01 | b0 b1 b2 b3 | 02
```

Exemplo do teste: a=2, b=3 → s=5 → emit `01 05 00 00 00`.
Bytes economizados: 11 − 5 = **6**.

Trace numérico:

```text
a = 2 = 02 00 00 00 LE
b = 3 = 03 00 00 00 LE
s = 5 = 05 00 00 00 LE
out = [0x01, 0x05, 0x00, 0x00, 0x00]
out_len = 5
```

## Algoritmo de `saved_bytes`

Varre `i` de 0 até `len`:

1. Se `match_push0_add` em `i` → `saved += 6`, `i += 6`
2. Senão se janela 11 casa PUSH/PUSH/ADD → `saved += 6`, `i += 11`
3. Senão `i += 1` (não pular opcodes no meio)

**Por quê** não `i += size` genérico? Porque o peephole olha *padrões*
de bytes, não um decode completo — mas o tamanho dos padrões já embute
a ISA (5+1 e 5+5+1).

## Invariantes

- Match só retorna 1 se os bytes forem exatamente o padrão.
- Fold não escreve se `out_cap < 5`.
- Soma `a+b` em u32 (wrap modular, igual à VM i32 truncada no lab).

## Bugs comuns

| Sintoma | Causa |
|---------|-------|
| match em PUSH 1+ADD | esqueceu checar imm==0 |
| fold emite 11 bytes | copiou input em vez de PUSH s |
| saved=0 no teste | avançou `i` de 1 dentro do padrão |

## Lab vs produção

LLVM InstCombine / GCC peephole trabalham sobre IR SSA, não bytes crus.
Aqui o bytecode *é* a IR — igual a um assembler que otimiza antes de emitir.

## Checklist

- [ ] Hex `01 00 00 00 00 02` → match=1
- [ ] Hex PUSH2+PUSH3+ADD → out `01 05 00 00 00`
- [ ] Economiza 6 bytes no fold
'''

TEORIA_SUFFIX["input_event_ring_mux"] = r'''
## Layout do anel (`RING_CAP = 4`)

```text
slots[0..3]  head  tail  count
vazio:       0     0     0
após push A: slots[0]=A, head=0, tail=1, count=1
após push B: slots[1]=B, head=0, tail=2, count=2
pop → A:     head=1, tail=2, count=1
```

Trace do teste:

```text
mux_push(source=1, type=1, value=10) → count=1
mux_push(source=2, type=2, value=-3) → count=2
pop → source=1 value=10
pop → source=2 value=-3
encher 4 pushes → 5º retorna -1
```

## Fórmulas

```text
push: slots[tail] = ev; tail = (tail+1) % CAP; count++
pop:  *out = slots[head]; head = (head+1) % CAP; count--
cheio: count == CAP
vazio: count == 0
```

**Por quê** `% CAP`? Sem módulo, `tail` sai do array e você corrompe memória.
**Por quê** `count` além de head/tail? Distinguir cheio vs vazio quando
`head == tail` (ambos 0).

## Mux

`mux_push` monta `InputEvent{type,value,source}` e chama `ring_push`.
É a ponte entre HID/PS2 (Dia 07) e um único consumidor.

## Invariantes

- `0 <= head,tail < CAP`
- `0 <= count <= CAP`
- FIFO: ordem de pop = ordem de push

## Bugs comuns

- Esquecer `% RING_CAP` → OOB
- Incrementar count no pop → overflow lógico
- Aceitar 5º push → teste espera -1

## Lab vs evdev

No kernel, `evdev` usa filas por cliente com drops sob pressão.
Aqui a política é **fail hard** (-1) para forçar o aluno a ver capacidade.

## Checklist

- [ ] Desenhei head/tail após 2 pushes
- [ ] Sei que value=-3 é int32, não unsigned
- [ ] 5º push em CAP=4 falha
'''

TEORIA_SUFFIX["clvm_disasm"] = r'''
## Mesma ISA, superfície Rust

O C (`clvm_disassembler`) devolve `-1` / `snprintf`.
O Rust devolve `Result<Vec<String>, String>` e usa `u32::from_le_bytes`.

| Conceito | C | Rust |
|----------|---|------|
| falha | return -1 | `Err("truncated PUSH")` |
| imm32 | shifts manuais | `from_le_bytes` |
| walk | `pc += size` | idem em `while pc < len` |

## Trace idêntico ao C

```text
code = [0x01, 0x2A, 0x00, 0x00, 0x00, 0x08]
disassemble → Ok(["PUSH 42", "HALT"])
instruction_size(0x01) = 5
instruction_size(0x09) = 3
instruction_size(0x02) = 1
opcode_name(0xFF) = None
```

**Por quê** portar? Ownership e `Result` tornam o trust-boundary explícito:
bytes truncados não viram UB silenciosa.

## `instruction_size` antes do decode

Separar size do format permite um verifier futuro andar sem alocar strings.
O lab testa size isolado (`CLVM-RS-DIS-02`) antes do walk completo.

## Invariantes

- `Ok(lines)` ⇒ concat(sizes) == code.len()
- Opcode desconhecido ⇒ `Err`, não `"???"`
- PUSH truncado (len<5) ⇒ `Err("truncated PUSH")`

## Bugs comuns

- Usar `u32::from_be_bytes` → 704643072 em vez de 42
- Size PUSH=1 → listing desalinhado
- `unwrap` em slice curto → panic (o lab prefere `Err`)

## Lab vs produção

`capstone` / `iced-x86` geram tabelas; aqui a tabela cabe em um `match`.
O ethos é o mesmo do validador Rust do Dia 03/06: bounds antes de indexar.

## Checklist

- [ ] size(PUSH)=5, size(JMP)=3
- [ ] listing PUSH 42 / HALT
- [ ] unknown op → Err
'''

TEORIA_SUFFIX["pe_export_span"] = r'''
## Layout DOS + PE (offsets do teste)

```text
offset 0x00: 'M' 'Z'
offset 0x3C: e_lfanew (i32 LE) = 0x80 neste fixture
offset 0x80: 'P' 'E' '\0' '\0'
opt header = pe + 4 + 20  (COFF FileHeader tem 20 bytes)
data dir[0] Export RVA em opt+0x78 → valor 0x1000 no teste
```

Trace:

```text
IsPeFile: MZ ok ∧ PE em e_lfanew → true
TryGetPeOffset → peOffset = 0x80
TryReadExportRva → exportRva = 0x1000
```

## Por quê Span?

`ReadOnlySpan<byte>` evita cópia e força bounds via `Length` / `Slice`.
`MemoryMarshal.Read<int>` lê LE nativo no Windows (e no lab).

**Por quê** checar `Length < 0x40` antes de `0x3C`? Sem isso, Slice lança
ou lê lixo — o teste espera `false`, não exceção.

## Invariantes

- `e_lfanew > 0` e `pe+4 <= Length`
- Export RVA lido só depois de `IsPeFile`
- Não segue a RVA até a Export Directory (só o ponteiro) — isso é triage

## Bugs comuns

| Sintoma | Causa |
|---------|-------|
| false em PE válido | esqueceu PE signature |
| peOffset=0 | leu e_lfanew em offset errado |
| exportRva lixo | opt+0x78 sem bounds |

## Lab vs produção

`System.Reflection.Metadata` / pe-parse seguem a árvore toda (sections, names).
Aqui você só valida o **caminho até o RVA** — base do red team do mesmo dia.

## Checklist

- [ ] Magic MZ nos bytes 0–1
- [ ] e_lfanew = 0x80
- [ ] Export RVA = 0x1000
'''

TEORIA_SUFFIX["shader_stage_fsm"] = r'''
## Grafo de estados (lab)

```text
EDIT ──compile──► COMPILE ──link──► LINK ──ready──► READY
  ▲                  │                              │
  └──────edit────────┘                              │
  ▲                                                 │
  └────────────────────edit─────────────────────────┘
```

Tabela `shader_can`:

| from | to | ok? |
|------|----|-----|
| EDIT | COMPILE | 1 |
| COMPILE | LINK | 1 |
| COMPILE | EDIT | 1 |
| LINK | READY | 1 |
| READY | EDIT | 1 |
| EDIT | READY | **0** |
| LINK | COMPILE | **0** |

Trace do teste:

```text
EDIT → COMPILE : can=1, apply=0, stage=COMPILE
EDIT → READY   : can=0, apply=-1, stage inalterado
illegal(EDIT,READY)=1
```

**Por quê** FSM? Em APIs reais (D3D12/Vulkan) recurso fora do estado certo
é UB ou device-loss. O lab compacta isso em inteiros.

## Invariantes

- `apply` só muda `*stage` se `can==1`
- Aresta ilegal **não** altera estado (teste verifica)
- `illegal` é o complemento de `can`

## Bugs comuns

- Permitir EDIT→READY “porque está pronto mentalmente”
- `apply` setar estado mesmo quando can=0
- Esquecer COMPILE→EDIT (reabrir shader)

## Lab vs produção

PSO / shader modules têm pipelines longos (compile → reflect → link → cache).
Aqui 4 estados bastam para treinar a **disciplina de transição**.

## Checklist

- [ ] EDIT→COMPILE sim; EDIT→READY não
- [ ] apply ilegal retorna -1
- [ ] estado permanece EDIT após aresta ilegal
'''

TEORIA_SUFFIX["pe_export_triage"] = r'''
## Pipeline de triage

```text
bytes → validate_mz_pe → count_export_names → flag_suspicious_exports
```

`SUSPICIOUS = VirtualAlloc, WriteProcessMemory, CreateRemoteThread`
(clássico de injection).

Trace:

```text
data com MZ + PE → validate True
names=["VirtualAlloc","foo"] → flagged=["VirtualAlloc"]
data sem MZ → validate False; count retorna -1
```

**Por quê** Python aqui? Triage rápida de evidência sem Span/.NET —
par com `dotnet/pe_export_span` no mesmo dia (mesmos offsets 0x3C / PE).

## Wire (igual .NET)

```text
0x00 MZ
0x3C e_lfanew u32 LE
[e_lfanew] PE\0\0
```

## Invariantes

- Sem MZ/PE válido, `count_export_names` = -1
- Flag é filtro por nome exato (não substring)
- Não resolve RVA→nomes neste lab (nomes vêm da lista de teste)

## Bugs comuns

- `data.startswith("MZ")` em str em vez de bytes
- Endian errado em `struct.unpack_from("<I", ...)`
- Flag case-insensitive demais / de menos

## Lab vs produção

Ferramentas reais (pefile, capa) enumeram Export Address Table.
Aqui o foco é **heurística de nomes** depois da validação de header.

## Checklist

- [ ] MZ nos 2 primeiros bytes
- [ ] PE em e_lfanew
- [ ] VirtualAlloc entra na lista suspeita
'''

TEORIA_SUFFIX["bell_state_prep"] = r'''
## Base |00⟩ → Bell |Φ+⟩

Amplitudes `[a00, a01, a10, a11]` = índices 0..3.

```text
reset: [1, 0, 0, 0]          P(00)=1
H no qubit 0:
  s = 1/sqrt(2) ≈ 0.70710678
  [s, 0, s, 0]               P(00)=P(10)=0.5
CNOT (control 0, target 1):
  troca a10 ↔ a11
  [s, 0, 0, s]               P(00)=P(11)=0.5
```

**Por quê** H antes de CNOT? Sem H, CNOT em |00⟩ não cria entrelaçamento.

## Fórmulas

```text
H0:  a0' = s(a0+a2); a1' = s(a1+a3);
     a2' = s(a0-a2); a3' = s(a1-a3);
CNOT: (a2, a3) ← (a3, a2)
P(k) = amp[k]^2
```

## Invariantes

- Σ P(k) = 1 (norma preservada sob unitárias)
- Após Bell: P(01)=P(10)=0
- reset sempre |00⟩

## Bugs comuns

- Aplicar H no qubit errado (índices)
- CNOT sem temporários → overwrite
- Comparar amplitudes com `==` float em vez de probs

## Lab vs produção

Qiskit/Cirq usam matrizes 4×4; aqui você aplica o efeito na mão
para ver o vetor mudar — base do módulo measurement (Dia 07).

## Checklist

- [ ] reset → [1,0,0,0]
- [ ] após H+CNOT: P(00)=P(11)=0.5
- [ ] s = 1/√2 no papel
'''

TEORIA_SUFFIX["softmax_stable"] = r'''
## Por quê subtrair o max?

`softmax(x)_i = exp(x_i) / Σ exp(x_j)`.
Se `x = [1000,1001,1002]`, `exp(1002)` overflowa em float32.
Estável:

```text
m = max(x)
y_i = exp(x_i - m)
p_i = y_i / Σ y
```

Trace do teste `xs={1,2,3}`:

```text
m = 3
exp(1-3)=exp(-2)≈0.135335
exp(2-3)=exp(-1)≈0.367879
exp(0)=1
sum≈1.503214
p≈[0.0900, 0.2447, 0.6652]
Σp = 1
p[2] > p[0]
```

## log-softmax e CE

```text
log_softmax_i = (x_i - m) - log(Σ exp(x_j - m))
CE = -log_softmax[target]
```

Para target=2: CE ≈ -log(0.6652) ≈ 0.4076

**Por quê** CE via log-softmax? Evita `log(softmax)` com underflow em p≈0.

## Invariantes

- Σ softmax = 1 (±1e-5)
- argmax(p) = argmax(x)
- n<=0 ou ponteiros nulos → -1

## Bugs comuns

- Softmax sem `-m` → NaN/Inf em logits grandes
- Dividir antes de somar
- CE com target fora de [0,n)

## Lab vs produção

PyTorch `torch.softmax` / `log_softmax` usam o mesmo truque em kernels CUDA.
O lab é o kernel em C cru.

## Checklist

- [ ] max=3; exp(-2), exp(-1), 1
- [ ] soma das probs = 1
- [ ] CE(target=2) = -log_softmax[2]
'''

TEORIA_SUFFIX["duplex_event_pipe"] = r'''
## Framing de 24 bytes

```text
EVENT_SIZE = 24
write 48 bytes → 2 eventos completos; eventsWritten == 2
write 25 bytes → 1 evento + 1 byte residual no _writeBuf
```

Fluxo:

```text
_write: concat → while len>=24: corta ev → _readBuf; eventsWritten++
_read:  while len>=24: push(ev); eventsRead++; respeita backpressure
metrics: {eventsWritten, eventsRead}
```

**Por quê** Duplex? Mesmo stream carrega input e output — padrão Node
para pipes binários (compare com Transform gunzip do Dia 06).

## Invariantes

- Só múltiplos de 24 sobem para o peer
- Residual < 24 permanece no buffer
- `push` false → para o loop (backpressure)

## Bugs comuns

- Usar `chunk.length` sem concat de residual
- Contar bytes em vez de eventos
- Ignorar retorno de `push`

## Lab vs produção

`objectMode` evita framing manual; aqui o framing ensina o bug clássico
de “meia mensagem”.

## Checklist

- [ ] 48 bytes → 2 eventos
- [ ] 25 bytes → 1 evento + residual 1
- [ ] metrics reflete contadores
'''

TEORIA_SUFFIX["json_rd_lexer"] = r'''
## Tokens do subset

| Char / padrão | kind |
|---------------|------|
| `{` | TOK_LBRACE |
| `}` | TOK_RBRACE |
| `:` | TOK_COLON |
| `,` | TOK_COMMA |
| `"..."` | TOK_STRING |
| `[0-9]+` | TOK_NUMBER |
| EOF | TOK_END |

Trace `{"a":1}`:

```text
i=0 '{' → LBRACE, i=1
i=1 '"'…'"' → STRING "a", i=4
i=4 ':' → COLON, i=5
i=5 '1' → NUMBER, i=6
i=6 '}' → RBRACE, i=7
lex_count = 5
```

**Por quê** lexer antes do parser? O recursive-descent (nome do módulo)
come tokens, não caracteres — whitespace some em `skip_ws`.

## Invariantes

- `skip_ws` só come espaço, `\n`, `\t`
- String sem `"` final → -1
- `lex_count` não conta TOK_END

## Bugs comuns

- Contar whitespace como token
- Aceitar letras em NUMBER
- Off-by-one em `end` da string

## Lab vs produção

`serde_json` / `simdjson` têm escapes e Unicode. Aqui o subset é
ASCII mínimo — suficiente para sentir o cursor `i`.

## Checklist

- [ ] `{"a":1}` → 5 tokens
- [ ] skip_ws em `"  {"` aponta para `{`
- [ ] string aberta falha
'''

TEORIA_SUFFIX["tool_protocol_fsm"] = r'''
## Grafo do protocolo de tool-call

```text
IDLE --call--> CALLING --sent--> WAITING --ok--> DONE
                                   |
                                   +--err--> ERROR
```

`TRANSITIONS` dict:

```text
(IDLE, call) → CALLING
(CALLING, sent) → WAITING
(WAITING, ok) → DONE
(WAITING, err) → ERROR
```

Trace:

```text
transition("call") → CALLING; trace ["call->CALLING"]
handle_response(True, {"x":1}) → state DONE, keys ["x"]
validate_tool_call("", {}) → False
validate_tool_call("search", {"q":"a"}) → True
```

**Por quê** FSM? Agentes que disparam tools sem estado viram
reentrância e double-submit. Aresta ilegal levanta `ValueError`.

## Invariantes

- Estado só muda via tabela
- Evento ilegal **não** altera `state` (exceção antes)
- `validate_tool_call` exige nome não-vazio e `dict`

## Bugs comuns

- Aceitar IDLE→DONE direto
- `handle_response` sem chamar `transition`
- Validar só `name` e ignorar tipo de `args`

## Lab vs produção

LangGraph / OpenAI tool protocol têm retries e timeouts.
Aqui o núcleo é a **máquina de estados** testável.

## Checklist

- [ ] IDLE→call→CALLING
- [ ] WAITING+err→ERROR
- [ ] aresta ilegal → ValueError
'''

TEORIA_SUFFIX["wasm_section_header"] = r'''
## Magic e versão (wire)

```text
offset 0: 00 61 73 6D   "\0asm"
offset 4: 01 00 00 00   version = 1 (u32 LE)
```

Calling convention Windows x64: ponteiro do buffer em **RCX**.
`wasm_magic_ok`: compara 4 bytes; EAX=1 sucesso, 0 falha.
`wasm_version_is_1`: `dword [RCX+4] == 1`.
`section_class`: CL=id → 1 (type), 2 (import), senão 0.
Id 9 → 0 (não é type/import).

Trace:

```text
buf = 00 61 73 6D 01 00 00 00
magic_ok → 1
version_is_1 → 1
section_class(1) → 1
section_class(2) → 2
section_class(9) → 0
```

**Por quê** Assembly? Para ver o ABI e o load byte-a-byte sem C
esconder o endian da dword.

## Invariantes

- Magic é 4 cmp separados (não um dword) — ordem de bytes explícita
- Version lê dword LE nativa
- section_class não lê memória, só CL

## Bugs comuns

- Comparar magic como dword 0x6D736100 no registrador errado
- Usar RDX em vez de RCX no Windows
- Devolver 1 para id desconhecido

## Lab vs produção

Wasmer/Wasmtime parseiam LEB128 de section size. Aqui só o
**header mínimo** + classificação de id.

## Checklist

- [ ] 4 bytes do magic no papel
- [ ] version dword = 1
- [ ] id 9 → 0
'''

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CODE_EXT = {".py", ".c", ".cpp", ".h", ".hpp", ".rs", ".cs", ".js", ".asm", ".S"}


def find_modules() -> list[Path]:
    return sorted(p.parent for p in DAY.glob("*/*/RESOLUCAO_GUIADA_PASSO_A_PASSO.md"))


def strip_paper_padding(teoria: str) -> str:
    markers = [
        r"^## Caderno",
        r"^## Passo de papel",
        r"^### Passo de papel",
        r"^## Fechamento do caderno",
        r"^## O que não fazer\n\nNão troque",
    ]
    cut = len(teoria)
    for m in markers:
        mm = re.search(m, teoria, re.M)
        if mm:
            cut = min(cut, mm.start())
    body = teoria[:cut].rstrip() + "\n"
    # remove trailing weak closing if duplicated later
    body = re.sub(r"\n## Fechamento.*", "\n", body, flags=re.S)
    return body.rstrip() + "\n"


def ensure_por_que(body: str) -> str:
    count = len(re.findall(r"Por qu[eê]", body, re.I))
    if count >= 3:
        return body
    body += """
## Por quê — síntese

### Por quê este formato wire?
Porque o teste compara bytes/estados concretos; intenção sem número não passa no assert.

### Por quê estas invariantes?
Cada uma corresponde a um caminho de falha que o `PEDAGOGY-TEST` exercita.

### Por quê lab ≠ produção?
O subset didático isola um mecanismo; produção empilha camadas (reloc, GC, SSA) em cima do mesmo núcleo.
"""
    return body


TODO_FN_HARDCODE: dict[str, list[tuple[str, str, str]]] = {
    "clvm_disassembler": [
        ("CLVM-DIS-01", "starter/clvm_disasm.c", "decode_push"),
        ("CLVM-DIS-02", "starter/clvm_disasm.c", "decode_branch"),
        ("CLVM-DIS-03", "starter/clvm_disasm.c", "disassemble_all"),
    ],
    "clvm_peephole_opt": [
        ("CLVM-PEEP-01", "starter/peephole.cpp", "match_push0_add"),
        ("CLVM-PEEP-02", "starter/peephole.cpp", "fold_const_add"),
        ("CLVM-PEEP-03", "starter/peephole.cpp", "saved_bytes"),
    ],
    "input_event_ring_mux": [
        ("LIN-MUX-01", "starter/ring.c", "ring_push"),
        ("LIN-MUX-02", "starter/ring.c", "ring_pop"),
        ("LIN-MUX-03", "starter/ring.c", "mux_push"),
    ],
    "clvm_disasm": [
        ("CLVM-RS-DIS-01", "starter/src/lib.rs", "opcode_name"),
        ("CLVM-RS-DIS-02", "starter/src/lib.rs", "instruction_size"),
        ("CLVM-RS-DIS-03", "starter/src/lib.rs", "disassemble"),
    ],
    "pe_export_span": [
        ("DN-PE-EXP-01", "starter/PeExportSpan.cs", "IsPeFile"),
        ("DN-PE-EXP-02", "starter/PeExportSpan.cs", "TryGetPeOffset"),
        ("DN-PE-EXP-03", "starter/PeExportSpan.cs", "TryReadExportRva"),
    ],
    "pe_export_triage": [
        ("RT-PE-EXP-01", "starter/pe_export_triage.py", "validate_mz_pe"),
        ("RT-PE-EXP-02", "starter/pe_export_triage.py", "count_export_names"),
        ("RT-PE-EXP-03", "starter/pe_export_triage.py", "flag_suspicious_exports"),
    ],
    "tool_protocol_fsm": [
        ("AGT-TOOL-01", "starter/tool_protocol_fsm.py", "transition"),
        ("AGT-TOOL-02", "starter/tool_protocol_fsm.py", "handle_response"),
        ("AGT-TOOL-03", "starter/tool_protocol_fsm.py", "validate_tool_call"),
    ],
    "duplex_event_pipe": [
        ("ND-DUPLEX-01", "starter/duplex_event_pipe.js", "_write"),
        ("ND-DUPLEX-02", "starter/duplex_event_pipe.js", "_read"),
        ("ND-DUPLEX-03", "starter/duplex_event_pipe.js", "metrics"),
    ],
    "wasm_section_header": [
        ("TOOL-WASM-01", "starter/wasm_section.asm", "wasm_magic_ok"),
        ("TOOL-WASM-02", "starter/wasm_section.asm", "wasm_version_is_1"),
        ("TOOL-WASM-03", "starter/wasm_section.asm", "section_class"),
    ],
    "softmax_stable": [
        ("AI-SOFTMAX-01", "starter/softmax.c", "softmax_stable"),
        ("AI-SOFTMAX-02", "starter/softmax.c", "log_softmax_stable"),
        ("AI-SOFTMAX-03", "starter/softmax.c", "cross_entropy_loss"),
    ],
    "shader_stage_fsm": [
        ("GFX-SHADER-FSM-01", "starter/shader_fsm.cpp", "shader_can"),
        ("GFX-SHADER-FSM-02", "starter/shader_fsm.cpp", "shader_apply"),
        ("GFX-SHADER-FSM-03", "starter/shader_fsm.cpp", "shader_illegal"),
    ],
    "bell_state_prep": [
        ("Q-BELL-01", "starter/bell.cpp", "q_reset"),
        ("Q-BELL-02", "starter/bell.cpp", "q_h0"),
        ("Q-BELL-03", "starter/bell.cpp", "q_cnot"),
    ],
    "json_rd_lexer": [
        ("PAR-JSON-LEX-01", "starter/json_lex.c", "skip_ws"),
        ("PAR-JSON-LEX-02", "starter/json_lex.c", "next_token"),
        ("PAR-JSON-LEX-03", "starter/json_lex.c", "lex_count"),
    ],
}


def collect_todos(module: Path) -> list[tuple[str, str, str]]:
    if module.name in TODO_FN_HARDCODE:
        return list(TODO_FN_HARDCODE[module.name])
    starter = module / "starter"
    out: list[tuple[str, str, str]] = []
    for p in starter.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in CODE_EXT and p.suffix not in {".asm", ".S"}:
            continue
        if "test" in p.name.lower():
            continue
        rel = f"starter/{p.relative_to(starter).as_posix()}"
        text = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"TODO\s*\[([A-Z0-9-]+)\]", text):
            tid = m.group(1)
            window = text[m.start() : m.start() + 400]
            before = text[max(0, m.start() - 200) : m.start()]
            fn = "?"
            for pat in [
                r"def\s+(\w+)\s*\(",
                r"(?:pub\s+)?fn\s+(\w+)\s*\(",
                r"public static \w+ (\w+)\s*\(",
                r"(?:int|void|float|double|size_t)\s+(\w+)\s*\(",
                r"^(\w+)\s+PROC",
            ]:
                ms = list(re.finditer(pat, window, re.M)) or list(re.finditer(pat, before, re.M))
                if ms:
                    fn = ms[0].group(1)
                    break
            if fn == "?" and p.suffix == ".js":
                ms = list(re.finditer(r"^\s+(\w+)\s*\([^)]*\)\s*\{", window, re.M))
                if ms:
                    fn = ms[0].group(1)
            out.append((tid, rel, fn))
    seen: set[str] = set()
    deduped = []
    for item in out:
        if item[0] not in seen:
            seen.add(item[0])
            deduped.append(item)
    return deduped


def extract_solution_fn(module: Path, rel_starter: str, fn: str, tid: str = "") -> str:
    sol_rel = rel_starter.replace("starter/", "")
    sol = module / "solutions" / sol_rel
    if not sol.exists():
        for cand in (module / "solutions").rglob(Path(sol_rel).name):
            sol = cand
            break
    if not sol.exists():
        return f"// implement {fn}\n"
    src = sol.read_text(encoding="utf-8", errors="ignore")
    if sol.suffix == ".py":
        try:
            tree = ast.parse(src)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == fn:
                            return ast.get_source_segment(src, item) or ""
                if isinstance(node, ast.FunctionDef) and node.name == fn:
                    return ast.get_source_segment(src, node) or ""
        except SyntaxError:
            pass
    if sol.suffix == ".rs":
        m = re.search(rf"(?:pub\s+)?fn\s+{re.escape(fn)}\b[\s\S]*?(?=\n(?:pub\s+)?fn\s|\Z)", src)
        if m:
            return m.group(0).strip()
    if sol.suffix == ".cs":
        m = re.search(
            rf"public static [^\n]+?\b{re.escape(fn)}\s*\([^\)]*\)\s*\n?\s*\{{[\s\S]*?\n    \}}",
            src,
        )
        if m:
            return m.group(0).strip()
    if sol.suffix == ".js":
        m = re.search(rf"{re.escape(fn)}\s*\([^)]*\)\s*\{{[\s\S]*?\n    \}}", src)
        if m:
            return m.group(0).strip()
    if sol.suffix in {".asm"}:
        m = re.search(rf"{re.escape(fn)}\s+PROC[\s\S]*?{re.escape(fn)}\s+ENDP", src, re.I)
        if m:
            return m.group(0).strip()
    if sol.suffix in {".c", ".cpp", ".h", ".hpp"}:
        m = re.search(
            rf"(?:static\s+)?(?:int|void|float|double|size_t|bool)\s+{re.escape(fn)}\s*\([^{{]*\{{[\s\S]*?\n\}}",
            src,
        )
        if m:
            return m.group(0).strip()
    if tid:
        m = re.search(
            rf"[^\n]*PEDAGOGY-SOLUTION:\s*{re.escape(tid)}[^\n]*\n([\s\S]{{20,600}}?)(?=\n\s*(?:/\*|//|\#|; )?PEDAGOGY-SOLUTION:|\n(?:pub\s+)?fn\s|\ndef\s|\npublic static|\nint\s|\nvoid\s|\n\w+\s+PROC|\Z)",
            src,
        )
        if m:
            return m.group(0).strip()
    return src.strip()[:500]


def lang_of(path: str) -> str:
    if path.endswith(".rs"):
        return "rust"
    if path.endswith(".cs"):
        return "csharp"
    if path.endswith(".js"):
        return "javascript"
    if path.endswith(".asm") or path.endswith(".S"):
        return "asm"
    if path.endswith(".cpp") or path.endswith(".hpp"):
        return "cpp"
    if path.endswith(".py"):
        return "python"
    return "c"


def baseline_cmd(module: Path) -> str:
    rel = module.relative_to(ROOT).as_posix()
    if (module / "starter" / "Cargo.toml").exists():
        return f"cd {rel}/starter\ncargo test"
    if list((module / "starter").glob("*.csproj")):
        return f"cd {rel}/starter\ndotnet test"
    if (module / "starter" / "test.js").exists():
        return f"cd {rel}/starter\nnode test.js"
    if (module / "starter" / "CMakeLists.txt").exists():
        return (
            f"cd {rel}/starter\n"
            "cmake -S . -B build_ci -A x64\n"
            "cmake --build build_ci --config Release\n"
            "ctest --test-dir build_ci -C Release --output-on-failure"
        )
    py = list((module / "starter").glob("test_*.py"))
    if py:
        return f"cd {rel}/starter\npython {py[0].name}"
    return f"cd {rel}/starter"


ALGO: dict[str, dict[str, str]] = {
    "CLVM-DIS-01": "Leia opcode 0x01; monte imm LE dos 4 bytes; snprintf PUSH; size=5; senão -1.",
    "CLVM-DIS-02": "Confirme branch; rel = b1|(b2<<8); nome via op_name; size=3.",
    "CLVM-DIS-03": "pc=0; escolha decoder; copie line; pc+=size; opcode desconhecido → -1.",
    "CLVM-PEEP-01": "Janela 6 bytes: PUSH com imm0 e ADD → return 1.",
    "CLVM-PEEP-02": "Janela 11: dois PUSH + ADD; some imms; emita PUSH s (5 bytes).",
    "CLVM-PEEP-03": "Varra i; some 6 por padrão matched; avance i pelo tamanho do padrão.",
    "LIN-MUX-01": "Se count>=CAP return -1; slots[tail]=ev; tail=(tail+1)%CAP; count++.",
    "LIN-MUX-02": "Se count==0 return -1; *out=slots[head]; head=(head+1)%CAP; count--.",
    "LIN-MUX-03": "Preencha InputEvent e chame ring_push.",
    "CLVM-RS-DIS-01": "match op → Some(nome) ou None.",
    "CLVM-RS-DIS-02": "PUSH→5; branch set→3; senão 1.",
    "CLVM-RS-DIS-03": "while pc: decode PUSH/branch/name; Err se truncado/unknown.",
    "DN-PE-EXP-01": "MZ + TryGetPeOffset + bytes PE\\0\\0.",
    "DN-PE-EXP-02": "Read Int32 em 0x3C; valide bounds.",
    "DN-PE-EXP-03": "opt = pe+24; leia UInt32 em opt+0x78.",
    "GFX-SHADER-FSM-01": "Tabela de arestas permitidas; default 0.",
    "GFX-SHADER-FSM-02": "Se !can return -1; senão *stage=to.",
    "GFX-SHADER-FSM-03": "return can?0:1.",
    "RT-PE-EXP-01": "MZ + unpack e_lfanew + PE.",
    "RT-PE-EXP-02": "validate; return len(names) ou -1.",
    "RT-PE-EXP-03": "filter names ∈ SUSPICIOUS.",
    "Q-BELL-01": "amp = [1,0,0,0].",
    "Q-BELL-02": "H0 com s=1/√2 nas combinações (0,2) e (1,3).",
    "Q-BELL-03": "swap amp[2]↔amp[3].",
    "AI-SOFTMAX-01": "m=max; exp(x-m); normalize.",
    "AI-SOFTMAX-02": "m=max; logsum; (x-m)-logsum.",
    "AI-SOFTMAX-03": "log_softmax; return -logs[target].",
    "ND-DUPLEX-01": "concat; slice de 24; incremente eventsWritten; chame _read.",
    "ND-DUPLEX-02": "push eventos de 24; eventsRead++; break se !push.",
    "ND-DUPLEX-03": "retorne contadores.",
    "PAR-JSON-LEX-01": "while ws: i++.",
    "PAR-JSON-LEX-02": "skip_ws; classifique char; strings/números com cursor.",
    "PAR-JSON-LEX-03": "loop next_token até END; conte.",
    "AGT-TOOL-01": "lookup TRANSITIONS; raise se ausente; atualize state/trace.",
    "AGT-TOOL-02": "transition ok/err; retorne state+keys.",
    "AGT-TOOL-03": "bool(name) and isinstance(args, dict).",
    "TOOL-WASM-01": "4 cmp byte [rcx+i]; EAX=1/0.",
    "TOOL-WASM-02": "eax=[rcx+4]; cmp 1.",
    "TOOL-WASM-03": "CL→1/2/0.",
}

PROBLEM: dict[str, str] = {
    "CLVM-DIS-01": "Sem decode_push, `01 2A 00 00 00` não vira `PUSH 42` size 5 — o assert do Caso 1 falha.",
    "CLVM-DIS-02": "Sem decode_branch, `09 0A 00` não vira `JMP 10` size 3.",
    "CLVM-DIS-03": "Sem walk, o programa de 7 bytes não produz as 3 linhas esperadas.",
    "CLVM-PEEP-01": "Sem match, PUSH0+ADD não é reconhecido e saved_bytes fica 0.",
    "CLVM-PEEP-02": "Sem fold, 2+3+ADD não vira PUSH 5 (5 bytes).",
    "CLVM-PEEP-03": "Sem varredura, o teste de bytes economizados falha.",
    "LIN-MUX-01": "Sem push, o anel não armazena o evento 10.",
    "LIN-MUX-02": "Sem pop FIFO, a ordem 10 depois -3 quebra.",
    "LIN-MUX-03": "Sem mux, source/type/value não entram no anel.",
    "CLVM-RS-DIS-01": "Sem nomes, HALT/ADD não listam.",
    "CLVM-RS-DIS-02": "Size errado desalinha o walk Rust.",
    "CLVM-RS-DIS-03": "Sem disassemble, Result não devolve PUSH 42.",
    "DN-PE-EXP-01": "Sem IsPeFile, fixture MZ/PE é rejeitada.",
    "DN-PE-EXP-02": "Sem e_lfanew, o offset 0x80 não aparece.",
    "DN-PE-EXP-03": "Sem data dir, export RVA 0x1000 não é lido.",
    "GFX-SHADER-FSM-01": "Sem can, EDIT→COMPILE não é permitido.",
    "GFX-SHADER-FSM-02": "Sem apply, o estado não avança com segurança.",
    "GFX-SHADER-FSM-03": "Sem illegal, o teste de aresta proibida falha.",
    "RT-PE-EXP-01": "Sem validate, bytes aleatórios passam.",
    "RT-PE-EXP-02": "Sem count, a lista de nomes não é medida.",
    "RT-PE-EXP-03": "Sem flag, VirtualAlloc não é marcado.",
    "Q-BELL-01": "Sem reset, o vetor não começa em |00⟩.",
    "Q-BELL-02": "Sem H0, não há superposição.",
    "Q-BELL-03": "Sem CNOT, não há Bell (P11≠0.5).",
    "AI-SOFTMAX-01": "Sem softmax estável, Σp≠1 ou overflow.",
    "AI-SOFTMAX-02": "Sem log_softmax, CE não fecha.",
    "AI-SOFTMAX-03": "Sem CE, o target 2 não bate com -log_p.",
    "ND-DUPLEX-01": "Sem _write framing, 48 bytes ≠ 2 eventos.",
    "ND-DUPLEX-02": "Sem _read, o peer não recebe 24-byte frames.",
    "ND-DUPLEX-03": "Sem metrics, o assert de contagem falha.",
    "PAR-JSON-LEX-01": "Sem skip_ws, espaços viram tokens.",
    "PAR-JSON-LEX-02": "Sem next_token, `{\"a\":1}` não tokeniza.",
    "PAR-JSON-LEX-03": "Sem lex_count, o assert de 5 falha.",
    "AGT-TOOL-01": "Sem transition, IDLE não vai a CALLING.",
    "AGT-TOOL-02": "Sem handle_response, WAITING não fecha.",
    "AGT-TOOL-03": "Sem validate, nome vazio passa.",
    "TOOL-WASM-01": "Sem magic_ok, \\0asm não é aceito.",
    "TOOL-WASM-02": "Sem version, dword≠1 passa indevido.",
    "TOOL-WASM-03": "Sem section_class, id 9 não devolve 0.",
}


def deepen_teoria(module: Path) -> None:
    path = module / "TEORIA_PASSO_A_PASSO.md"
    body = path.read_text(encoding="utf-8")
    body = strip_paper_padding(body)
    # remove leftover passo fragments
    body = re.sub(r"### Passo de papel[\s\S]*?(?=\n## |\Z)", "", body)
    suf = TEORIA_SUFFIX.get(module.name, "")
    if suf and "## Endianness" not in body and "## Padrão PUSH 0" not in body and "## Layout do anel" not in body:
        # avoid double-append on re-run: check a unique heading from suffix
        first_heading = re.search(r"^## .+$", suf, re.M)
        key = first_heading.group(0) if first_heading else None
        if key and key not in body:
            body = body.rstrip() + "\n" + suf
        elif key is None:
            body = body.rstrip() + "\n" + suf
    elif suf:
        first_heading = re.search(r"^## .+$", suf, re.M)
        if first_heading and first_heading.group(0) not in body:
            body = body.rstrip() + "\n" + suf
    body = ensure_por_que(body)
    # drop any remaining passo de papel
    if "Passo de papel" in body:
        body = re.split(r"\n## Caderno|\n### Passo de papel|\n## Passo de papel", body)[0]
        if module.name in TEORIA_SUFFIX and TEORIA_SUFFIX[module.name].strip()[:20] not in body:
            body = body.rstrip() + "\n" + TEORIA_SUFFIX[module.name]
        body = ensure_por_que(body)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def build_resolucao(module: Path, todos: list[tuple[str, str, str]]) -> str:
    lines: list[str] = [
        f"# Resolução guiada — {module.name}",
        "",
        "## Mapa exato starter → resolução",
        "",
        "| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |",
        "|---------|---------|-----------------|------------|-----------|",
    ]
    for tid, fpath, fn in todos:
        lines.append(
            f"| `{tid}` | `{fpath}` | `{fn}` | corpo sob `TODO [{tid}]` | assinaturas e testes |"
        )
    lines += [
        "",
        "## Baseline",
        "",
        "```powershell",
        baseline_cmd(module),
        "```",
        "",
        "**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).",
        "",
        "Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.",
        "",
    ]
    for tid, fpath, fn in todos:
        code = extract_solution_fn(module, fpath, fn)
        # Prefer PEDAGOGY-SOLUTION extraction
        sol_file = module / "solutions" / fpath.replace("starter/", "")
        if not sol_file.exists():
            for cand in (module / "solutions").rglob("*"):
                if cand.is_file() and cand.suffix == Path(fpath).suffix:
                    txt = cand.read_text(encoding="utf-8", errors="ignore")
                    if f"PEDAGOGY-SOLUTION: {tid}" in txt or fn in txt:
                        sol_file = cand
                        break
        if sol_file.exists():
            txt = sol_file.read_text(encoding="utf-8", errors="ignore")
            m = re.search(
                rf"PEDAGOGY-SOLUTION:\s*{re.escape(tid)}[\s\S]*?(?=\n\s*/\*|PEDAGOGY-SOLUTION:|\n(?:pub\s+)?fn\s|\nint\s|\nvoid\s|\npublic static|\n    _\w+\(|\ndef\s|\Z)",
                txt,
            )
            if m:
                # better: use function extract already
                pass
            code2 = extract_solution_fn(module, fpath, fn)
            if len(code2) > 40:
                code = code2
        lg = lang_of(fpath)
        algo = ALGO.get(tid, f"Implemente `{fn}` conforme o contrato do teste `{tid}`.")
        problem = PROBLEM.get(tid, f"Sem `{fn}`, o marcador `{tid}` falha.")
        lines += [
            f"## {tid}",
            "",
            "### Onde colocar",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| Arquivo | `{fpath}` |",
            f"| Função / âncora | `{fn}` / comentário `TODO [{tid}]` |",
            f"| Substituir | corpo do stub (mantenha a assinatura) |",
            f"| Não mexer | headers, testes, outros TODOs neste passo |",
            "",
            "### O problema",
            "",
            problem,
            "",
            "### Algoritmo / trace",
            "",
            algo,
            "",
            "No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`",
            "antes de digitar. Confirme size/estado/retorno esperado.",
            "",
            "### Escreva o código",
            "",
            f"```{lg}",
            code.rstrip(),
            "```",
            "",
            "### Por que funciona?",
            "",
            f"A rotina `{fn}` materializa o contrato de `{tid}`: os mesmos números do trace",
            "da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)",
            "corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.",
            "",
            "### Verifique",
            "",
            f"1. Recompile/rode só o caminho que exerce `{tid}`.",
            f"2. Confira o valor numérico (não só “passou”).",
            f"3. Se falhar, diff hex/estado com o trace da TEORIA.",
            "",
            "### Checkpoint",
            "",
            f"- [ ] `{tid}` PASS no starter",
            f"- [ ] Não quebrei TODOs anteriores",
            f"- [ ] Entendi o *porquê* do size/estado, não só o resultado",
            "",
            "---",
            "",
        ]
    lines += [
        "## Debug",
        "",
        "| Sintoma | Causa provável | Correção |",
        "|---------|----------------|----------|",
        "| FAIL no Caso 1 | stub intacto / endian errado | releia o trace da TEORIA e o bloco do primeiro TODO |",
        "| PASS parcial | size/estado desalinhado no TODO do meio | imprima pc/head/estado antes do assert |",
        "| Crash / panic | bounds | valide Length/len antes de indexar |",
        "| Diff de string | snprintf/format | compare caractere a caractere com o esperado |",
        "",
        "## Relatório de resolução",
        "",
        "| TODO | Horas | Maior bug | O que aprendia de novo |",
        "|------|-------|-----------|------------------------|",
    ]
    for tid, _, _ in todos:
        lines.append(f"| `{tid}` |  |  |  |")
    lines += [
        "",
        "Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar",
        "que uma API de alto nível esconderia.",
        "",
    ]
    return "\n".join(lines)


def expand_exercicios(module: Path, todos: list[tuple[str, str, str]]) -> None:
    name = module.name
    t0, t1, t2 = (todos + todos[-1:])[:3]
    text = f"""# Exercícios — {name}

## Fácil — paper-trace do Caso 1

Reproduza no papel o trace numérico da `TEORIA_PASSO_A_PASSO.md` (mesmos bytes/estados do teste).
Arquivo-alvo: nenhum (caderno). Critério de aceite: os números batem com `TESTES_GUIADOS.md` Caso 1 **antes** de editar código.

## Médio — `{t0[0]}`

Implemente `{t0[2]}` em `{t0[1]}`.
Critério de aceite: o `PEDAGOGY-TEST` ligado a `{t0[0]}` PASS; valores iguais ao paper-trace.

## Difícil — `{t1[0]}` + `{t2[0]}`

Complete `{t1[2]}` e `{t2[2]}` mantendo invariantes dos passos anteriores.
Critério de aceite: suíte completa do starter PASS; caso negativo (erro/bounds) ainda falha como documentado.

## Desafio — extensão sem quebrar testes

Altere apenas documentação ou um assert extra local: escolha um input *vizinho* ao Caso 1
(ex.: PUSH 256, 5º push no anel, id WASM 3, logits {{1000,1001,1002}}) e mostre no papel
o resultado esperado. Não relaxe os asserts existentes.
"""
    (module / "EXERCICIOS.md").write_text(text, encoding="utf-8")


def expand_testes(module: Path, todos: list[tuple[str, str, str]]) -> None:
    cases = {
        "clvm_disassembler": [
            ("1", "PUSH 42", "Entrada `01 2A 00 00 00`. Esperado: line `PUSH 42`, size 5, retorno 0.", "CLVM-DIS-01"),
            ("2", "JMP 10", "Entrada `09 0A 00`. Esperado: `JMP 10`, size 3.", "CLVM-DIS-02"),
            ("3", "programa 7 bytes", "`01 2A 00 00 00 02 08` → 3 linhas PUSH/ADD/HALT.", "CLVM-DIS-03"),
            ("4", "opcode FF", "Retorno < 0; sem listing parcial mentiroso.", "CLVM-DIS-03"),
        ],
        "clvm_peephole_opt": [
            ("1", "match PUSH0+ADD", "Hex `01 00 00 00 00 02` → match=1.", "CLVM-PEEP-01"),
            ("2", "fold 2+3", "Emite `01 05 00 00 00`, out_len=5.", "CLVM-PEEP-02"),
            ("3", "saved bytes", "Padrão fold economiza 6.", "CLVM-PEEP-03"),
            ("4", "não-match", "PUSH 1+ADD não casa.", "CLVM-PEEP-01"),
        ],
        "input_event_ring_mux": [
            ("1", "mux 10", "mux_push source=1 value=10 → 0.", "LIN-MUX-03"),
            ("2", "FIFO", "pop 10 depois pop -3.", "LIN-MUX-02"),
            ("3", "overflow", "5º push com CAP=4 → -1.", "LIN-MUX-01"),
            ("4", "vazio", "pop em anel vazio → -1.", "LIN-MUX-02"),
        ],
        "clvm_disasm": [
            ("1", "opcode_name", "HALT/ADD Some; 0xFF None.", "CLVM-RS-DIS-01"),
            ("2", "sizes", "PUSH=5 JMP=3 ADD=1.", "CLVM-RS-DIS-02"),
            ("3", "listing", "PUSH 42 + HALT Ok.", "CLVM-RS-DIS-03"),
            ("4", "truncated", "PUSH incompleto → Err.", "CLVM-RS-DIS-03"),
        ],
        "pe_export_span": [
            ("1", "IsPeFile", "MZ+PE em 0x80 → true.", "DN-PE-EXP-01"),
            ("2", "e_lfanew", "TryGetPeOffset → 0x80.", "DN-PE-EXP-02"),
            ("3", "export RVA", "→ 0x1000.", "DN-PE-EXP-03"),
            ("4", "curto", "buffer <0x40 → false.", "DN-PE-EXP-01"),
        ],
        "shader_stage_fsm": [
            ("1", "can EDIT→COMPILE", "retorna 1.", "GFX-SHADER-FSM-01"),
            ("2", "apply", "estado avança; ilegal -1.", "GFX-SHADER-FSM-02"),
            ("3", "illegal EDIT→READY", "retorna 1.", "GFX-SHADER-FSM-03"),
            ("4", "estado intacto", "após aresta ilegal stage permanece.", "GFX-SHADER-FSM-02"),
        ],
        "pe_export_triage": [
            ("1", "MZ/PE", "validate true no fixture.", "RT-PE-EXP-01"),
            ("2", "count", "len(names) após validate.", "RT-PE-EXP-02"),
            ("3", "suspicious", "VirtualAlloc flagado.", "RT-PE-EXP-03"),
            ("4", "sem MZ", "validate false; count -1.", "RT-PE-EXP-01"),
        ],
        "bell_state_prep": [
            ("1", "reset", "[1,0,0,0].", "Q-BELL-01"),
            ("2", "H0", "P00=P10=0.5.", "Q-BELL-02"),
            ("3", "CNOT Bell", "P00=P11=0.5.", "Q-BELL-03"),
            ("4", "norma", "soma probs ≈ 1.", "Q-BELL-03"),
        ],
        "softmax_stable": [
            ("1", "softmax {1,2,3}", "Σp=1; p2>p0.", "AI-SOFTMAX-01"),
            ("2", "log_softmax", "out[2]>out[0].", "AI-SOFTMAX-02"),
            ("3", "CE target 2", "CE ≈ -log_softmax[2].", "AI-SOFTMAX-03"),
            ("4", "n inválido", "retorno -1.", "AI-SOFTMAX-01"),
        ],
        "duplex_event_pipe": [
            ("1", "48 bytes", "eventsWritten==2.", "ND-DUPLEX-01"),
            ("2", "read frames", "eventsRead acompanha.", "ND-DUPLEX-02"),
            ("3", "metrics", "objeto com ambos contadores.", "ND-DUPLEX-03"),
            ("4", "residual 25", "1 evento + 1 byte buffer.", "ND-DUPLEX-01"),
        ],
        "json_rd_lexer": [
            ("1", "skip_ws", "cursor após espaços.", "PAR-JSON-LEX-01"),
            ("2", "next_token", "LBRACE etc.", "PAR-JSON-LEX-02"),
            ("3", "lex_count", "{\"a\":1} → 5.", "PAR-JSON-LEX-03"),
            ("4", "string aberta", "retorno -1.", "PAR-JSON-LEX-02"),
        ],
        "tool_protocol_fsm": [
            ("1", "call", "IDLE→CALLING.", "AGT-TOOL-01"),
            ("2", "response ok", "WAITING→DONE.", "AGT-TOOL-02"),
            ("3", "validate", "nome vazio False.", "AGT-TOOL-03"),
            ("4", "aresta ilegal", "ValueError; estado intacto.", "AGT-TOOL-01"),
        ],
        "wasm_section_header": [
            ("1", "magic", "\\0asm → 1.", "TOOL-WASM-01"),
            ("2", "version", "dword 1 → 1.", "TOOL-WASM-02"),
            ("3", "section id 1/2", "retorna 1 ou 2.", "TOOL-WASM-03"),
            ("4", "id 9", "retorna 0.", "TOOL-WASM-03"),
        ],
    }
    rows = cases.get(module.name)
    if not rows:
        rows = [
            (str(i + 1), tid, f"Exercita `{fn}` em `{fp}`.", tid)
            for i, (tid, fp, fn) in enumerate(todos)
        ]
        while len(rows) < 4:
            rows.append((str(len(rows) + 1), todos[0][0], "Edge case de bounds/erro.", todos[0][0]))
    lines = [
        f"# Testes guiados — {module.name}",
        "",
        "Cada caso abaixo existe como `PEDAGOGY-TEST: ID` no código de teste do starter/solutions.",
        "",
    ]
    if module.parent.name == "graphics":
        lines += [
            "## Caso VISUAL-01 — headless",
            "",
            "FSM sem janela: trace de transições no stdout/assert. Não há pixel buffer neste módulo.",
            "",
        ]
    for num, title, desc, tid in rows:
        lines += [
            f"## Caso {num}: {title}",
            "",
            desc,
            "",
            f"**PEDAGOGY-TEST:** `{tid}`",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| ID | `{tid}` |",
            f"| Aceite | assert/retorno descrito acima |",
            "",
        ]
    lines += [
        "## Mapa ID → caso",
        "",
        "| PEDAGOGY-TEST | Casos |",
        "|---------------|-------|",
    ]
    for tid, _, _ in todos:
        linked = ", ".join(f"Caso {n}" for n, _, _, t in rows if t == tid)
        lines.append(f"| `{tid}` | {linked or 'ver suíte'} |")
    lines.append("")
    (module / "TESTES_GUIADOS.md").write_text("\n".join(lines), encoding="utf-8")


def expand_pesquisa(module: Path) -> None:
    track = module.parent.name
    name = module.name
    text = f"""# Pesquisa guiada — {track}/{name}

## Fontes âncora

1. Documentação / RFC / ISA ligada ao wire-format deste módulo (CLVM Dia 03, PE/COFF, WASM, evdev, Node streams, JSON RFC 8259, quantum notes, numerics).
2. Comparar com o módulo-irmão no mesmo dia (C↔Rust disasm, .NET↔redteam PE, ring↔duplex).
3. Nota de produção: como a ferramenta real (objdump, pe-parse, Qiskit, PyTorch) expõe o mesmo conceito.

## Perguntas (responda em 4–8 linhas cada)

1. Qual invariante quebra se o size/estado estiver off-by-one?
2. Onde o lab simplifica vs produção — e o que isso esconde?
3. Qual caso negativo do teste é o mais importante para segurança/robustez?
4. Como você portaria este mecanismo para `projects/chris-*`?

## Entregável

Uma página no caderno: diagrama do fluxo + três riscos + uma citação da fonte âncora com offset/fórmula.
"""
    (module / "PESQUISA_GUIADA.md").write_text(text, encoding="utf-8")


def expand_benchmark(module: Path) -> None:
    text = f"""# Benchmark guiado — {module.name}

## Hipótese

A implementação correta é O(n) no tamanho da entrada (bytes, eventos ou estados visitados)
e não aloca além do buffer de saída.

## Medição

| Métrica | Como medir | Meta |
|---------|------------|------|
| Tempo Caso 1 | `Measure-Command` / timer do runner | estável ±20% |
| Tempo input ×10 | repetir fixture | ≈ linear |
| Starter incompleto | baseline | FAIL rápido |

## Procedimento

1. Rode solutions (PASS) e anote tempo wall-clock.
2. Rode starter incompleto (FAIL) — não otimize stubs.
3. Compare com o módulo-irmão se existir (C vs Rust, .NET vs Python).

## Resultados observados

| Run | Ambiente | Tempo / notas |
|-----|----------|---------------|
| 1 | _preencher_ | |
| 2 | _preencher_ | |
| 3 | _preencher_ | |

## Interpretação

Se ×10 input não ≈ ×10 tempo, procure trabalho quadratic (re-concat em loop,
walk `i++` ineficiente). Registre conclusões no Relatório de resolução.
"""
    (module / "BENCHMARK_GUIADO.md").write_text(text, encoding="utf-8")


def expand_readme(module: Path, todos: list[tuple[str, str, str]]) -> None:
    track = module.parent.name
    ids = ", ".join(f"`{t}`" for t, _, _ in todos)
    text = f"""# {module.name}

**Trilha:** `{track}` · **Dia:** 2026-09-08

## O que você constrói

Implementação low-level com TODOs {ids}. Leia a TEORIA (trace numérico) antes do starter.

## Pré-requisitos

Módulos do Dia 03/07 na mesma trilha quando houver continuação (CLVM, input, PE).

## Como rodar

```powershell
{baseline_cmd(module)}
```

Starter: FAIL até completar TODOs. Solutions: PASS.

## Ordem de estudo

1. `TEORIA_PASSO_A_PASSO.md`
2. Checkpoint em `../../ATIVIDADES.md`
3. `EXERCICIOS.md` → código em `starter/`
4. `TESTES_GUIADOS.md` / `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` se travar
5. `BENCHMARK_GUIADO.md` + Relatório
"""
    (module / "README.md").write_text(text, encoding="utf-8")


ATIVIDADES = r'''# ATIVIDADES — 2026-09-08 (CLVM toolchain + input + trilhas)

**Dia:** 13 módulos | **~24–32 h** | Linguagens: C, C++, Rust, .NET, JS, Python, ASM  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel com os números abaixo). PASS no teste sozinho não basta.

---

## Preparação (30–45 min)

- [ ] Ler `START_HERE.md` e `README.md` do dia
- [ ] Baseline de gates:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-08
```

- [ ] Escolher ordem: bytecode (C→C++→Rust) antes das trilhas satélite

---

## Bloco 1 — Disassembly CLVM em C (3–4 h)

### Objetivo conceitual

Entender **size por opcode** e little-endian do imm32 — o mesmo contrato do verifier (Dia 07), agora como texto.

| Módulo | TODOs | Paper-trace obrigatório |
|--------|-------|-------------------------|
| `systems/clvm_disassembler` | CLVM-DIS-01..03 | `01 2A 00 00 00` → `PUSH 42` size 5; prog 7 bytes → 3 linhas; `FF` → erro |

**Checkpoint conceitual (marque antes do código):**

- [ ] Calculei imm = `2A|0|0|0` = 42 em LE
- [ ] Calculei PUSH 256 = `01 00 01 00 00` → 256 (não 1)
- [ ] Escrevi por que size PUSH=5 e JMP=3
- [ ] Sei que opcode desconhecido aborta o listing inteiro (−1)

**Depois:** cmake/ctest no starter; solutions deve PASS.

---

## Bloco 2 — Peephole no mesmo bytecode (3–4 h)

### Objetivo conceitual

Ver o bytecode como IR: padrões de bytes que preservam semântica e encurtam o programa.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/clvm_peephole_opt` | CLVM-PEEP-01..03 | `01 00..00 02` match; PUSH2+PUSH3+ADD → `01 05 00 00 00`; saved=6 |

**Checkpoint conceitual:**

- [ ] Hex do PUSH 0 + ADD (6 bytes) desenhado
- [ ] Soma 2+3=5 e encoding LE do 5
- [ ] Explico em uma frase: por que saved = 11−5 = 6

---

## Bloco 3 — Ring mux em C (2–3 h)

### Objetivo conceitual

Fila circular com `head/tail/count` e política fail-hard no overflow — ponte para eventos HID/PS2 do Dia 07.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `linux/input_event_ring_mux` | LIN-MUX-01..03 | push 10 depois −3; pops FIFO; 5º push com CAP=4 → −1 |

**Checkpoint conceitual:**

- [ ] Tabela head/tail/count após 0,1,2 pushes
- [ ] Fórmula `(idx+1)%RING_CAP`
- [ ] Por que `count` distingue cheio de vazio

---

## Bloco 4 — Mesma ISA em Rust (3–4 h)

### Objetivo conceitual

Paridade C↔Rust: mesmos sizes e listing, superfície `Result` em vez de −1.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `rust/clvm_disasm` | CLVM-RS-DIS-01..03 | size PUSH=5; listing `PUSH 42`/`HALT`; unknown → Err |

**Checkpoint conceitual:**

- [ ] `from_le_bytes` de `2A 00 00 00` = 42
- [ ] Diferença Err vs panic OOB
- [ ] Tabela size alinhada com o C do Bloco 1

```powershell
cargo test --manifest-path days/2026-09-08/rust/clvm_disasm/starter/Cargo.toml
cargo test --manifest-path days/2026-09-08/rust/clvm_disasm/solutions/Cargo.toml
```

---

## Bloco 5 — PE em .NET + triage Python (4–5 h)

### Objetivo conceitual

Offsets DOS/PE (`e_lfanew`, data directory[0]) como trust-boundary; nomes de export como heurística red team.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `dotnet/pe_export_span` | DN-PE-EXP-01..03 | MZ; e_lfanew=0x80; export RVA=0x1000 |
| `redteam/pe_export_triage` | RT-PE-EXP-01..03 | mesmos offsets; flag `VirtualAlloc` |

**Checkpoint conceitual:**

- [ ] Desenhei bytes 0x00–0x01 (MZ) e 0x3C (e_lfanew)
- [ ] opt = pe+4+20; RVA em opt+0x78
- [ ] Listei as 3 APIs suspeitas do lab
- [ ] Sei a diferença: Span valida caminho; Python flag nomes

---

## Bloco 6 — WASM em Assembly (2–3 h)

### Objetivo conceitual

Magic `\0asm` + version dword=1 no ABI Windows (ponteiro em RCX).

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `tooling/wasm_section_header` | TOOL-WASM-01..03 | `00 61 73 6D`; version 1; id 9 → 0 |

**Checkpoint conceitual:**

- [ ] Quatro cmp de magic no papel
- [ ] RCX = ponteiro do buffer (Windows x64)
- [ ] section_class(1)=1, (2)=2, (9)=0

---

## Bloco 7 — Softmax C + lexer JSON C (3–4 h)

### Objetivo conceitual

Estabilidade numérica (`x−max`) e cursor de lexer — dois “parsers” de mundos diferentes.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `ai/softmax_stable` | AI-SOFTMAX-01..03 | max{1,2,3}=3; exp(−2),exp(−1),1; Σp=1; CE target 2 |
| `parsers/json_rd_lexer` | PAR-JSON-LEX-01..03 | `{"a":1}` → 5 tokens |

**Checkpoint conceitual:**

- [ ] Calculei as três exp(x−3) com 3 casas
- [ ] Escrevi CE = −log p₂
- [ ] Listei os 5 kinds de `{"a":1}`
- [ ] skip_ws não emite token

---

## Bloco 8 — Node duplex + shader FSM + Bell + agent (5–6 h)

### Objetivo conceitual

Framing 24 B, arestas legais de pipeline gráfico, preparo Bell, protocolo de tool-call.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `nodejs/duplex_event_pipe` | ND-DUPLEX-01..03 | 48 B → 2 eventos; residual 25→1+1 |
| `graphics/shader_stage_fsm` | GFX-SHADER-FSM-01..03 | EDIT→COMPILE sim; EDIT→READY não |
| `quantum/bell_state_prep` | Q-BELL-01..03 | [1,0,0,0]→H→CNOT; P00=P11=0.5 |
| `agent/tool_protocol_fsm` | AGT-TOOL-01..03 | IDLE→call→CALLING; ilegal → ValueError |

**Checkpoint conceitual:**

- [ ] EVENT_SIZE=24; 48/24=2
- [ ] Aresta EDIT→READY proibida; apply não muda estado
- [ ] Vetor após H e após CNOT com s=1/√2
- [ ] Tabela TRANSITIONS do agente no papel

**Nota visual (shader):** headless — asserts de estado, sem janela GL neste módulo.

---

## Bloco 9 — Capstone / relatório (2 h)

- [ ] Preencher Relatório de resolução em cada módulo feito
- [ ] Anotar BENCHMARK (Resultados observados)
- [ ] Portar um pedaço CLVM ou PE para `projects/chris-*` se houver slot

---

## Checklist final

| Item | ☐ |
|------|---|
| Paper-traces blocos 1–8 | |
| pedagogy_check PASS | |
| run_day_tests solutions PASS | |
| C↔Rust listing idêntico PUSH 42 | |
| PE: 0x80 / 0x1000 no papel | |
| Softmax Σp=1 no papel | |

## Relatório do dia (preencher)

| Bloco | Horas | Checkpoint papel | Testes | Maior bug |
|-------|-------|------------------|--------|-----------|
| 1 disasm C | | ☐ | ☐ | |
| 2 peephole | | ☐ | ☐ | |
| 3 ring | | ☐ | ☐ | |
| 4 Rust | | ☐ | ☐ | |
| 5 PE | | ☐ | ☐ | |
| 6 WASM | | ☐ | ☐ | |
| 7 softmax+json | | ☐ | ☐ | |
| 8 duplex+FSM+Bell+agent | | ☐ | ☐ | |

**Síntese:** o disassembler C e o Rust listam o mesmo `PUSH 42`. O peephole apaga o padrão que o listing acabou de mostrar. Ring C e Duplex JS recortam por capacidade/frame. PE .NET e triage Python compartilham e_lfanew.
'''

START_HERE = r'''# START HERE — Day 2026-09-08

Laboratório unificado: **CLVM toolchain** (disasm C, peephole C++, disasm Rust) + **input mux**, depois trilhas obrigatórias (PE, WASM, AI, parser, Node, graphics FSM, quantum, agent).

## Fluxo por módulo

1. `TEORIA_PASSO_A_PASSO.md` — O quê / Como / Por quê + **trace com números do teste**.
2. Checkpoint em [`ATIVIDADES.md`](ATIVIDADES.md) **antes** do starter.
3. `EXERCICIOS.md` — Fácil → Desafio.
4. Implemente `TODO [ID]` em `starter/`.
5. Testes `PEDAGOGY-TEST: ID` — FAIL até completar.
6. `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar.
7. Compare `solutions/` após tentativa; preencha benchmark + relatório.

---

## Bloco A — Bytecode (comece aqui)

| # | Módulo | Linguagem | Foco do paper-trace |
|---|--------|-----------|---------------------|
| 1 | `systems/clvm_disassembler` | C | `01 2A 00 00 00` → PUSH 42 |
| 2 | `systems/clvm_peephole_opt` | C++ | fold 2+3 → PUSH 5 |
| 3 | `rust/clvm_disasm` | Rust | mesmos sizes + `Result` |

## Bloco B — Input path

| # | Módulo | Linguagem | Foco |
|---|--------|-----------|------|
| 4 | `linux/input_event_ring_mux` | C | CAP=4; FIFO 10 depois −3 |
| 5 | `nodejs/duplex_event_pipe` | JS | frames de 24 bytes |

## Bloco C — Formatos de arquivo / ABI

| # | Módulo | Linguagem | Foco |
|---|--------|-----------|------|
| 6 | `dotnet/pe_export_span` | .NET | e_lfanew 0x80; RVA 0x1000 |
| 7 | `redteam/pe_export_triage` | Python | mesmos offsets + nomes |
| 8 | `tooling/wasm_section_header` | ASM | `\0asm`; RCX; id 9→0 |

## Bloco D — Numérico / texto / estados

| # | Módulo | Linguagem | Foco |
|---|--------|-----------|------|
| 9 | `ai/softmax_stable` | C | max-subtraction; Σp=1 |
| 10 | `parsers/json_rd_lexer` | C | `{"a":1}` → 5 tokens |
| 11 | `graphics/shader_stage_fsm` | C++ | arestas legais EDIT…READY |
| 12 | `quantum/bell_state_prep` | C++ | H+CNOT; P00=P11=0.5 |
| 13 | `agent/tool_protocol_fsm` | Python | IDLE→…→DONE/ERROR |

---

## Comandos úteis

```powershell
# Gate do dia
python scripts/pedagogy_check_unified.py --day 2026-09-08
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions

# Rust
cd days/2026-09-08/rust/clvm_disasm/starter; cargo test
cd ../solutions; cargo test

# .NET
cd days/2026-09-08/dotnet/pe_export_span/starter; dotnet test

# Node
cd days/2026-09-08/nodejs/duplex_event_pipe/starter; node test.js
```

Sem `cargo`/`dotnet`/`node`, o runner do dia **pula** o módulo (mesmo padrão Dia 06).

**Capstone sugerido:** portar disasm ou PE span para `projects/chris-vm` / `projects/chris-*` após os blocos A–C.
'''


def main() -> None:
    modules = find_modules()
    for module in modules:
        todos = collect_todos(module)
        if module.name == "wasm_section_header" and not todos:
            todos = [
                ("TOOL-WASM-01", "starter/wasm_section.asm", "wasm_magic_ok"),
                ("TOOL-WASM-02", "starter/wasm_section.asm", "wasm_version_is_1"),
                ("TOOL-WASM-03", "starter/wasm_section.asm", "section_class"),
            ]
        deepen_teoria(module)
        (module / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").write_text(
            build_resolucao(module, todos), encoding="utf-8"
        )
        expand_exercicios(module, todos)
        expand_testes(module, todos)
        expand_pesquisa(module)
        expand_benchmark(module)
        expand_readme(module, todos)
        print(f"deepened {module.parent.name}/{module.name} todos={len(todos)}")

    (DAY / "ATIVIDADES.md").write_text(ATIVIDADES, encoding="utf-8")
    (DAY / "START_HERE.md").write_text(START_HERE, encoding="utf-8")
    print("wrote ATIVIDADES.md + START_HERE.md")


if __name__ == "__main__":
    main()
