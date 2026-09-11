# Adendo — Qualidade Extrema e Reorganização Unificada (v2 do prompt)

Este adendo complementa o prompt mestre base. **Toda entrega diária deve obedecer ambos.**

---

# 0. LAYOUT CANÔNICO DO REPOSITÓRIO

Taxonomia por trilha em `days/YYYY-MM-DD/<trilha>/<modulo>/` (não usar `modules/NN_`).

```text
days/YYYY-MM-DD/
├── README.md
├── START_HERE.md
├── TODO_MAP.md
├── VALIDATION.md
├── MANIFEST.json
├── Treino_LowLevel_Unificado_YYYY-MM-DD.docx   # OPCIONAL (export)
└── <trilha>/<modulo>/  (8 arquivos MD + starter + solutions)
```

**Formato principal de estudo:** Markdown modular por pasta de módulo. Ver [PEDAGOGY_STANDARD.md](PEDAGOGY_STANDARD.md).

Scripts unificados no repositório:
- `scripts/pedagogy_check_unified.py --day YYYY-MM-DD`
- `scripts/build_day_docx.py --day YYYY-MM-DD`  # export opcional
- `scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions|starter`
- `scripts/generate_day_scaffold.py --day YYYY-MM-DD`

---

# 41. THRESHOLDS MENSURÁVEIS (ANTI-SUPERFICIALIDADE)

| Artefato | Mínimo | Conteúdo obrigatório |
|----------|--------|----------------------|
| `TEORIA_PASSO_A_PASSO.md` | 120 linhas | diagrama/tabela, exemplo numérico, invariantes, bugs comuns |
| `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` | 80 linhas (100 complexos) | mapa starter→TODO, **Onde colocar** (Arquivo/Função/Substituir\|Inserir) por TODO, **Por que funciona?**, debugging |
| `EXERCICIOS.md` | 4 níveis | fácil, médio, difícil, desafio |
| DOCX (opcional) | export de todos os MD | gerado por `build_day_docx.py`, não fonte primária |

Módulos complexos: graphics, clvm, http_parser, bytecode VM, distro, kernel, matmul, miniobjdump.

Se RESOLUCAO > 450 linhas: criar `RESOLUCAO_APENDICE.md`.

---

# 42b. ONDE COLOCAR (OBRIGATÓRIO POR TODO)

Cada `TODO [ID]` na RESOLUCAO deve ter um bloco **Onde colocar** com Arquivo (`starter/...`), Função/âncora, Substituir ou Inserir, e Não mexer.

Snippet: `docs/templates/RESOLUCAO_PLACEMENT_SNIPPET.md`.  
Referência: `days/2026-09-03/systems/clvm/RESOLUCAO_GUIADA_PASSO_A_PASSO.md`.

---

# 42. ILUSTRAÇÕES OBRIGATÓRIAS POR TIPO

- **Binário/ELF/PE/CIL:** tabela de offsets byte-a-byte
- **Allocator/bitmap:** bitmap antes/depois, page→byte→bit
- **VM/bytecode:** trace `ip=… opcode=… stack=[…]`
- **Streams:** diagrama producer→buffer→consumer, estados drain/pause
- **GPU:** máquina de estados com transições válidas/inválidas
- **ANSI/CSI:** máquina de estados com bytes de exemplo
- **Matmul tiled:** blocos na memória e cache lines

No DOCX: embutir figuras ou tabelas formatadas; código monoespaçado legível.

---

# 43. RELATÓRIO DE RESOLUÇÃO (OBRIGATÓRIO)

Final de cada `RESOLUCAO_GUIADA_PASSO_A_PASSO.md`:

```text
## Relatório de resolução
- TODOs concluídos: [IDs]
- Testes passando: [comandos + output]
- Invariantes verificadas: [lista]
- Edge cases testados: [lista]
- Benchmark: [hipótese, resultado, interpretação]
- Não executado: [toolchain ausente]
```

---

# 44. ANTI-PADRÕES PROIBIDOS

- Starters minificados (linhas > 200 caracteres)
- `TESTES_GUIADOS.md` descrevendo casos inexistentes no código
- Validators que só checam string `TODO [ID]`
- DOCX gerado antes do Markdown completo
- "Veja a solution" / "o restante é semelhante" / "copie solutions" / "como em solutions"
- RESOLUCAO sem `## Baseline` ou sem código completo por TODO
- Padding: `Nota pedagógica N`, linhas duplicadas, blocos genéricos só para ≥120 linhas
- Scaffold preguiçoso: "Anote no papel valores concretos", "Valide compreensão básica", "satisfaz o caso documentado", "Leia README e fixtures", "Módulo X no dia N" sem wire format, algoritmo e trace numérico do teste real
- TEORIA/RESOLUCAO que repetem O quê/Como/Por quê sem bytes, offsets, invariantes ou código copiável alinhado ao `starter/` e aos asserts do teste
- Nome de classe divergente entre starter e teste
- Benchmark sem seção "Resultados observados" ou skip honesto
- Scripts (`upgrade_module_quality`, `repair_pedagogy_depth`) injetando placeholders no lugar de conteúdo real
- Marcar dia completo com `pedagogy_check` PASS mas `day_contract_check` FAIL (dia narrow vs tier-A)
- `generate_day_scaffold.py` sem `--manifest-only` em dias com START_HERE curado

---

# 45. WORKFLOW CURSOR (10 FASES)

0. **OpenSpec:** `/opsx:propose` — escopo, dia referência (`2026-09-06`), trilhas em `openspec/specs/day-contract/`
1. Scaffold starters + solutions
2. Pedagogia MD completa (teoria, resolução, exercícios)
3. Testes alinhados com TESTES_GUIADOS
4. `pedagogy_check_unified.py` → PASS (inclui módulos + day contract)
5. `day_contract_check.py` → PASS (pode rodar isolado para debug)
6. Executar solutions e starters (`run_day_tests`)
7. `build_day_docx.py`
8. QA visual do DOCX (PDF/páginas)
9. `VALIDATION.md` + MANIFEST (`--manifest-only`) + TODO_MAP curado
10. `/opsx:archive` — mover change para `openspec/changes/archive/`

Não avance de fase com gate falhando.

**Anti falso-done:** PASS pedagógico por módulo com dia incompleto (ex. Dia 07 só CLVM+GFX) é **proibido**. Ver `AGENTS.md`.

---

# 46. RETROATIVIDADE

Quando novas diretivas surgem, **dias anteriores devem ser corrigidos** — não apenas o dia atual.
Manter DOCX sincronizado com Markdown em todos os dias publicados.

---

# 47. PEDAGOGY-TEST E PEDAGOGY-SOLUTION

Todo `TODO [ID]` no starter exige:
- `PEDAGOGY-SOLUTION: ID` na solution
- `PEDAGOGY-TEST: ID` no código de teste (não só em TESTES_GUIADOS.md)
- Referência em RESOLUCAO e TODO_MAP.md

---

# 48. BENCHMARK — RESULTADOS

Cada `BENCHMARK_GUIADO.md` termina com `## Resultados observados`.
Gravar agregados em `benchmarks/results-YYYY-MM-DD.json` quando executável.

---

# 49. GATE UNIFICADO

```bash
python scripts/pedagogy_check_unified.py --day YYYY-MM-DD
python scripts/day_contract_check.py --day YYYY-MM-DD
python scripts/quality_check.py
python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
python scripts/run_day_tests.py --day YYYY-MM-DD --mode starter --expect-fail
```

`pedagogy_check_unified` executa `day_contract_check` ao final para o mesmo `--day`.

OpenSpec: `/opsx:verify` antes de arquivar change.

---

# 50. REGRA DE OURO (QUALIDADE EXTREMA)

Prefira **menos módulos extremamente bem ensinados** a muitos módulos superficiais.
Cada exercício deve ser abrível, seguível passo a passo, implementável, quebrável, depurável e testável **sem ChatGPT externo**.

**DOCX completo é obrigatório em todo dia — sem exceção.**
