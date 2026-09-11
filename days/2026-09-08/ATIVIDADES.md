# ATIVIDADES — 2026-09-08 (CLVM toolchain + input + trilhas)

**Dia:** 22 módulos (13 core + 9 trilha GitHub) | **~24–32 h** | Linguagens: C, C++, Rust, .NET, JS, Python, ASM  
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

---

## Trilha paralela A — GitHub (concorrência, cache, ranking) (10–14 h)

Estas pastas vieram do remote e **também estão no dia**. São um eixo diferente (SPSC/cache/BM25/NFA),
não substituto do toolchain CLVM acima. Faça depois do Bloco 1–4 ou em paralelo se já dominar bytecode.

| Módulo | Linguagem | Paper-trace / foco |
|--------|-----------|-------------------|
| `systems/spsc_ring_buffer` | C++ | push até cheio; pop FIFO — SPSC ring push/pop/size |
| `architecture/cache_set_sim` | C++ | set/tag decode → hit → evict — cache set decode/hit/evict |
| `ai/online_softmax` | Python | mesmo contrato numérico estável — online softmax stats/normalize |
| `redteam/wasm_binary_triage` | Python | magic \0asm + uleb — WASM header/ULEB/sections |
| `parsers/nfa_to_dfa` | Python | NFA→DFA no papel — ε-closure / subset / match |
| `agent/bm25_code_ranker` | Python | rank docs=score — BM25 tokenize/index/score |
| `unix/xargs_lite` | Python | batch sem shell=True — split/batch/run |
| `nodejs/worker_transfer` | JS | ArrayBuffer transfer — worker transferables |
| `dotnet/gc_allocation_probe` | .NET | contagem de alocações — alloc/new/pool probe |

**Checkpoint conceitual (trilha A):**

- [ ] Desenhei SPSC cheio vs vazio (índices head/tail)
- [ ] Decodei set/tag de um endereço no cache sim
- [ ] Tracei ε-closure de um NFA mínimo no papel
- [ ] Sei por que `xargs_lite` usa `shell=False`
- [ ] Diferencio `softmax_stable` (C, dia core) de `online_softmax` (Python, trilha A)

**Gate trilha A:**

```powershell
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions
```

(os módulos novos devem aparecer no runner junto com o core)

### Por que manter as duas trilhas

- **Core (local):** ISA CLVM + ABI + PE + trilhas obrigatórias tier-A multilíngue — melhor para o fio pedagógico Dias 07→11.
- **Trilha A (GitHub):** laboratórios clássicos (SPSC, cache, NFA→DFA, BM25) com benchmarks — melhor para sistemas/IR/search.
- Juntas: **22 módulos**. Não é redundância: `softmax_stable` ≠ `online_softmax`; ring mux ≠ SPSC; wasm asm ≠ wasm triage.

