# ATIVIDADES — 2026-09-10 (integração multi-trilha / capstone)

**Dia:** 13 módulos | **~28–36 h**  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel). Teste PASS sem o papel não conta.

---

## Preparação (30 min)

- [ ] `START_HERE.md` + `README.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-10
```

---

## Bloco 1 — Bytecode CLVM (systems + rust) (5–7 h)

### Objetivo conceitual

Disasm → peephole (apaga `PUSH 0; ADD`) → verify de stack; e o mesmo header validado em Rust.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/clvm_pipeline_integration` | CAP-CLVM-* | listing PUSH1/2 ADD HALT; fold → `01 05 08` |
| `rust/cross_verify_clvm` | CAP-RS-XVFY-* | magic CLVM; version 1; FNV @ offset 12 |

**Checkpoint conceitual:**

- [ ] Escrevi as 4 linhas do disasm antes do editor
- [ ] Sei por que `01 00 02` some e `01 05` fica
- [ ] Desenhei header offsets 0/4/12

**Depois:** solutions PASS (`pytest` / `cargo test`).

---

## Bloco 2 — Input unificado (systems / linux / .NET) (5–7 h)

### Objetivo conceitual

Eventos `(type,code,value)` → mux → `KEY:`/`REL:`; device `composite0` fecha com SYN `(0,0,0)`; host .NET conta via Span.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/unified_input_pipeline` | CAP-INP-* | (1,30,1) → KEY:30 |
| `linux/composite_input_driver` | CAP-LNX-* | name composite0; frame[-1]=(0,0,0) |
| `dotnet/capstone_input_host` | CAP-DN-HOST-* | inteiro literal do HostTests |

**Checkpoint conceitual:**

- [ ] Traduzi (1,30,1) → KEY:30
- [ ] Expliquei SYN_REPORT
- [ ] Anotei o número do assert .NET

---

## Bloco 3 — Gráficos, triage, quantum, AI (5–7 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `graphics/pipeline_state_object` | CAP-GFX-PSO-* | UNINITIALIZED→VERTEX_SHADER; READY→RECORDING |
| `redteam/capstone_triage` | CAP-RT-FMT-* | ELF/PE/WASM magics; min_size PE=2 |
| `quantum/capstone_measurement` | CAP-Q-MEAS-* | \|0.5+0.5j\|²=0.5; sample 0.75→1 |
| `ai/capstone_tokenizer` | CAP-AI-TOK-* | aaab → [97×3,98]; vocab 2 |

**Checkpoint conceitual:**

- [ ] Listei 2 arestas da FSM de PSO
- [ ] Escrevi magics ELF/PE/WASM
- [ ] Calculei Born de 0.5+0.5j
- [ ] RLE de aaab → [(97,3),(98,1)]

---

## Bloco 4 — Node, parsers, agent, tooling (5–7 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `nodejs/capstone_stream_pipeline` | CAP-ND-PIPE-* | out HELLO; chunks=1 |
| `parsers/capstone_query_eval` | CAP-PRATT-* | lex 3 tokens; AND/OR True |
| `agent/capstone_agent_loop` | CAP-AGENT-* | state DONE; replay True |
| `tooling/capstone_format_detect` | CAP-TOOL-DET-* | PNG; confidence 1.0 |

**Checkpoint conceitual:**

- [ ] Anotei HELLO e chunks=1
- [ ] Lexei `a:1 AND b:2` em 3 tokens
- [ ] Desenhei loop até DONE
- [ ] Magic PNG em hex (89 50 4E 47…)

---

## Relatório do dia

| Bloco | Papel | Testes |
|-------|-------|--------|
| 1 bytecode | ☐ | ☐ |
| 2 input | ☐ | ☐ |
| 3 gfx/rt/q/ai | ☐ | ☐ |
| 4 node/parse/ag/tool | ☐ | ☐ |

```powershell
python scripts/run_day_tests.py --day 2026-09-10 --mode solutions
```

---

## Caderno mestre do dia (2026-09-10)

Antes de cada bloco de código, preencha **no papel** (não no chat):

1. Bytes / offsets / estados do paper-trace da tabela do bloco.
2. Valor exato que o assert compara (string, inteiro, probabilidade).
3. Arquivo `starter/...` e nome da função do primeiro TODO do bloco.
4. Uma frase: o que quebra se o size/cursor/estado estiver off-by-one.

### Mini-lab de integração entre módulos

- [ ] Escrevi no papel um valor produzido pelo módulo 1 que o módulo 2 consome (mesmo número).
- [ ] Marquei qual linguagem de cada módulo da linha acima.
- [ ] Rodei `python scripts/run_day_tests.py --day 2026-09-10 --mode solutions` e anotei PASS/FAIL por trilha.

### Critério de fechamento do dia

Não basta `ctest` verde. O dia fecha quando:

- [ ] Todos os checkpoints conceituais das seções acima estão marcados.
- [ ] `pedagogy_check_unified.py --day 2026-09-10` PASS.
- [ ] Você consegue explicar o Caso 1 de cada módulo em 60 segundos sem abrir o editor.

### Horas sugeridas por trilha (planejamento)

| Trilha | Horas | Entrega |
|--------|-------|---------|
| systems | 4–6 | bytecode / arena / pipeline |
| linux / tooling | 3–4 | anel / header / símbolos |
| rust / dotnet | 3–4 | Result / Span |
| graphics / quantum / ai | 4–5 | FSM / amplitudes / norm |
| parsers / agent / node / redteam | 4–5 | lexer / FSM / pipe / triage |

**Total planejado:** use o README do dia; se passar de 40 h, priorize systems + uma trilha adjacente no mesmo dia e retome o resto no dia seguinte com o mesmo caderno.

