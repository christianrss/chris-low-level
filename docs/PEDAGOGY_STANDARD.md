# Padrão didático — O quê, Como, Por quê

Todo módulo em `days/YYYY-MM-DD/<trilha>/<modulo>/` deve ensinar **o que fazer**, **como fazer** e **por que fazer** — sem lacunas operacionais.

## Formato principal: Markdown modular

O estudo acontece **na pasta do módulo**, não em um DOCX monolítico.

```text
<modulo>/
├── README.md                      # visão geral e pré-requisitos
├── TEORIA_PASSO_A_PASSO.md        # conceitos + diagramas + invariantes
├── PESQUISA_GUIADA.md             # links e perguntas de investigação
├── EXERCICIOS.md                  # Fácil → Médio → Difícil → Desafio
├── RESOLUCAO_GUIADA_PASSO_A_PASSO.md  # passo a passo operacional
├── TESTES_GUIADOS.md              # casos de teste documentados
├── BENCHMARK_GUIADO.md            # medições e resultados observados
├── starter/                       # código com TODO [ID]
└── solutions/                     # gabarito com PEDAGOGY-SOLUTION: ID
```

DOCX (`Treino_LowLevel_Unificado_*.docx`) é **export opcional** via `scripts/build_day_docx.py`.

## Estrutura obrigatória por artefato

### TEORIA_PASSO_A_PASSO.md (≥120 linhas)

Para cada conceito central:

| Seção | Conteúdo |
|-------|----------|
| **O quê** | Definição precisa, vocabulário, papel no sistema |
| **Como** | Mecanismo interno, fluxo de dados, estruturas |
| **Por quê** | Motivação de design, trade-offs, comparação com produção |
| **Invariantes** | O que sempre deve ser verdade |
| **Bugs comuns** | Sintoma → causa → como depurar |
| **Trace manual** | Exemplo numérico ou byte-a-byte no papel |

Proibido: parágrafos genéricos como "consulte os TODOs em starter/" sem explicar o conceito.

### RESOLUCAO_GUIADA_PASSO_A_PASSO.md (≥80 linhas; ≥100 em módulos complexos)

1. **Mapa exato starter → resolução** — cada `TODO [ID]` com caminho de arquivo.
2. **Baseline** — comandos de build/teste; saída **FAIL** esperada antes dos TODOs.
3. **Por TODO** (repetir para cada ID):
   - Arquivo e função a abrir
   - Código a digitar (bloco completo, não "implemente X")
   - **Por que funciona?** — raciocínio, não só o resultado
   - Verificação manual (trace, assert, saída)
   - Checkpoint: rode teste parcial antes de avançar
4. **Debug** — mensagens de erro típicas e correções
5. **Relatório de resolução** — template para o aluno preencher

Referência de qualidade: `days/2026-09-04/systems/arena_allocator/RESOLUCAO_GUIADA_PASSO_A_PASSO.md`.

### EXERCICIOS.md

Quatro níveis com enunciado, arquivo-alvo e critério de aceite. Cada exercício deve mapear a pelo menos um `TODO [ID]` ou extensão documentada.

### TESTES_GUIADOS.md

Cada caso documentado deve existir como `PEDAGOGY-TEST: ID` no código de teste.

## Marcadores de consistência

| Local | Marcador |
|-------|----------|
| starter | `TODO [ID]` |
| testes | `PEDAGOGY-TEST: ID` |
| solutions | `PEDAGOGY-SOLUTION: ID` |
| RESOLUCAO | menção ao ID + caminho `starter/...` |

O checker `scripts/pedagogy_check_unified.py` valida esses vínculos e rejeita conteúdo superficial.

## Fluxo do aluno (START_HERE)

1. Leia `README.md` do dia e `START_HERE.md`.
2. Por módulo: TEORIA → EXERCICIOS → implemente em `starter/`.
3. Rode testes intermediários; use RESOLUCAO só ao travar.
4. Compare com `solutions/` após tentativa honesta.
5. Preencha Relatório de resolução e benchmark.

Ver também: [PORTING_GUIDE.md](PORTING_GUIDE.md), [LEARNING_PATHS.md](LEARNING_PATHS.md), [RESEARCH_NOTE_TEMPLATE.md](RESEARCH_NOTE_TEMPLATE.md).
