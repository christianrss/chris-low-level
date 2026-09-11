# ATIVIDADES — 2026-09-09 (observabilidade multi-linguagem)

**Dia:** 13 módulos | **~24–32 h**  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel). Teste PASS sozinho não basta.

---

## Preparação (30 min)

- [ ] Ler `START_HERE.md` e `README.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-09
```

---

## Bloco 1 — Contadores e arena (C / C++) (4–6 h)

### Objetivo conceitual

Ver um **histograma de opcodes** e uma **arena com telemetria** cujo `allocs` sobrevive ao reset.

| Módulo | TODOs | Paper-trace obrigatório |
|--------|-------|-------------------------|
| `systems/clvm_trace_profiler` | CLVM-TRACE-01..03 | `02 02 08` → c[2]=2, hottest=2 |
| `systems/arena_telemetry` | ARENA-TEL-01..03 | alloc(8) ok; alloc(60) -1; reset mantém allocs=1 |

**Checkpoint conceitual:**

- [ ] Contei no papel os opcodes do fixture e marquei hottest
- [ ] Escrevi used/allocs/resets após init, alloc(8), alloc(60), reset
- [ ] Explico em uma frase: por que reset não zera allocs

**Depois:** implemente starters; `ctest` solutions deve PASS.

---

## Bloco 2 — Máscara causal (C) (2–3 h)

### Objetivo conceitual

Atenção causal: k>q é invisível; score vira −1e9; `visible_count(2)=3`.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `ai/attention_mask` | AI-ATTN-01..03 | q=2,k=2 visível; k=3 → −1e9; count=3 |

**Checkpoint conceitual:**

- [ ] Tabela q=2 × k=0..3 no papel
- [ ] Sei por que −1e9 e não 0

---

## Bloco 3 — Stack, spans e async (Rust / .NET / Node) (5–7 h)

### Objetivo conceitual

PC→nome, ActivitySource→tag→export, async_hooks init/before/after.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `rust/stack_sample_trace` | RS-STACK-* | 0x1000 → main |
| `dotnet/activity_source_span` | DN-ACT-* | `work\|activity_source_span` |
| `nodejs/async_hooks_trace` | ND-ASYNC-* | phase init presente; m.init≥1 |

**Checkpoint conceitual:**

- [ ] Escrevi PC→main
- [ ] Escrevi a string de export do Activity
- [ ] Listei as três fases async_hooks

---

## Bloco 4 — Perf, GPU timer, logfmt (3–5 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `linux/perf_event_open_lab` | LX-PERF-* | open(1,2)→fd; read 42; close remove |
| `graphics/gpu_timer_query` | GFX-GPU-* | handle 0; lap draw |
| `parsers/logfmt_lexer` | PR-LOGFMT-* | `a=1 b=2` → 2 tokens |

**Checkpoint conceitual:**

- [ ] Calculei fd = (1<<16)\|2
- [ ] Sei que o primeiro timer handle é 0
- [ ] Tokenizei logfmt no papel

---

## Bloco 5 — Quantum, YARA, agent, PDB (4–6 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `quantum/decoherence_noise` | Q-DECO-* | p0+p1≈1; len(trace)=4 |
| `redteam/yara_match_scan` | RT-YARA-* | pat [0xAA,None]; hit @1 |
| `agent/verify_replay_log` | AG-* | start+verify ok → DONE; hash 16 |
| `tooling/pdb_symbol_index` | TL-PDB-* | `1000 main` → (0x1000, main) |

**Checkpoint conceitual:**

- [ ] Normalizei um par de probs
- [ ] Parseiei AA ?? → [0xAA, None]
- [ ] Desenhei FSM IDLE→RUN→DONE
- [ ] Parseiei linha de símbolo

---

## Relatório do dia

| Bloco | Papel | Testes solutions |
|-------|-------|------------------|
| 1 C/C++ | ☐ | ☐ |
| 2 atenção | ☐ | ☐ |
| 3 Rust/.NET/JS | ☐ | ☐ |
| 4 perf/gfx/parse | ☐ | ☐ |
| 5 q/rt/ag/tool | ☐ | ☐ |

```powershell
python scripts/run_day_tests.py --day 2026-09-09 --mode solutions
```

---

## Caderno mestre do dia (2026-09-09)

Antes de cada bloco de código, preencha **no papel** (não no chat):

1. Bytes / offsets / estados do paper-trace da tabela do bloco.
2. Valor exato que o assert compara (string, inteiro, probabilidade).
3. Arquivo `starter/...` e nome da função do primeiro TODO do bloco.
4. Uma frase: o que quebra se o size/cursor/estado estiver off-by-one.

### Mini-lab de integração entre módulos

- [ ] Escrevi no papel um valor produzido pelo módulo 1 que o módulo 2 consome (mesmo número).
- [ ] Marquei qual linguagem de cada módulo da linha acima.
- [ ] Rodei `python scripts/run_day_tests.py --day 2026-09-09 --mode solutions` e anotei PASS/FAIL por trilha.

### Critério de fechamento do dia

Não basta `ctest` verde. O dia fecha quando:

- [ ] Todos os checkpoints conceituais das seções acima estão marcados.
- [ ] `pedagogy_check_unified.py --day 2026-09-09` PASS.
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

