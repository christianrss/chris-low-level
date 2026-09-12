# Padrão didático — O quê, Como, Por quê

Todo módulo em `days/YYYY-MM-DD/<trilha>/<modulo>/` deve ensinar **o que fazer**, **como fazer** e **por que fazer** — sem lacunas operacionais.

## Perfis de publicação

- **Legado:** dias até 2026-09-11 mantêm o contrato com que foram
  publicados. Não os use como justificativa para gerar dezenas de novos
  módulos.
- **Depth-first:** todo dia posterior usa exatamente um projeto de
  6–8 horas e declara `profile: depth_first` em `day.contract.yaml`.
  Cobertura de trilhas ocorre em ciclos de 7–10 dias.

No perfil depth-first, “módulo” significa um projeto integrado. Funções
isoladas, três stubs independentes ou uma coleção de katas não formam um
projeto publicável.

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

## Contrato depth-first

Além dos arquivos canônicos, o dia contém:

- `day.contract.yaml`: perfil, 6–8 horas, lane e ciclo;
- `ASSESSMENT.yaml`: fonte de verdade para conceitos, marcos,
  comportamentos, falhas esperadas, mutantes e orçamento de autoria;
- `RUBRIC.md`: avaliação legível de engenharia e explicação.

### Resultado esperado

O aluno deve entregar um executável ou biblioteca integrável com:

1. entrada real ou fixture representativa;
2. transformação central não trivial;
3. saída observável;
4. erros e limites explícitos;
5. teste end-to-end;
6. benchmark com hipótese e interpretação.

### Marcos obrigatórios

`EXERCICIOS.md` deixa de ser uma lista “Fácil/Médio/Difícil/Desafio” e
passa a conter 6–10 marcos ordenados:

1. baseline e previsão de falhas;
2. modelo mental, invariantes e traces;
3. contratos e testes;
4. caminho mínimo end-to-end;
5. robustez e trust boundaries;
6. integração e ergonomia;
7. medição;
8. revisão e síntese.

Marcos podem ser combinados, mas construção, robustez e medição não
podem desaparecer.

### Starter quase vazio

Build, testes públicos, fixtures e assinaturas podem vir prontos. Os
arquivos listados em `student_owned` devem exigir que o aluno crie o
núcleo:

- no máximo 15% da lógica final já implementada no starter;
- delta esperado de pelo menos 250 linhas substantivas;
- nenhum TODO principal resolvível por retorno constante ou por até
  três linhas, salvo justificativa no assessment;
- cada TODO representa comportamento ou invariante, não preenchimento
  cosmético.

O limite de linhas é orçamento de autoria. Ele só é aceito junto com
testes adversos, integração e revisão pedagógica.

### Evidência semântica

Cada conceito obrigatório no assessment liga:

- definição e invariante;
- trace feliz e trace de falha;
- arquivo/função em que aparece;
- marco de implementação;
- comportamento testado;
- bug plausível e sintoma.

O projeto declara no mínimo 10 comportamentos, 4 modos de falha e um
caso end-to-end. Também inclui mutantes críticos, como remoção de bounds
check, off-by-one, endian invertido ou bypass de validação; os testes
devem rejeitá-los.

### Resolução em ajuda progressiva

Cada marco da `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` usa esta ordem:

1. pergunta diagnóstica;
2. invariante e pseudocódigo;
3. placement e checkpoint;
4. explicação do código completo.

O código final permanece em `solutions/`. A resolução não deve reduzir o
fluxo principal a transcrição antes de o aluno formular uma hipótese.

### Rubrica

A rubrica totaliza 100 pontos:

- 15: modelo mental, traces e invariantes;
- 30: implementação funcional;
- 20: robustez e limites;
- 15: testes e rejeição de mutantes;
- 10: integração e API;
- 5: benchmark e interpretação;
- 5: síntese técnica.

Aprovação exige 75 pontos e todos os hard gates. Excelência exige 90.
Teste obrigatório falhando, trust boundary ignorada ou execução não
realizada impede a publicação, mesmo com documentação completa.

## Estrutura obrigatória por artefato

### Regra de ouro (anti-resumo)

**Não resuma.** Cada passo deve ser reproduzível **sem abrir `solutions/`**. Proibido:

- Padding artificial (`Nota pedagógica N`, linhas repetidas, seções 11–30 genéricas só para bater linha mínima)
- Delegação: `copie solutions`, `veja solutions`, `como em solutions`, `compare com solutions`
- Stubs na RESOLUCAO: `implemente X` sem bloco de código completo copiável

Contagem de linhas mede **conteúdo substantivo**, não filler. Referência canônica: `days/2026-09-03/systems/clvm/`.

O checker rejeita filler de scaffold (`Anote no papel valores concretos`, "conceito central deste módulo", "satisfaz o caso documentado"). Cada módulo precisa do **formato real** (bytes/offsets ou fórmula), um **trace numérico igual ao teste** e código na RESOLUCAO **idêntico em comportamento** ao `solutions/`.

### TEORIA_PASSO_A_PASSO.md (≥120 linhas substantivas)

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
2. **Baseline** (obrigatório: `## Baseline`) — comandos de build/teste; saída **FAIL** esperada antes dos TODOs.
3. **Por TODO** (repetir para cada ID; ordem fixa):
   - **O problema** — o que quebra sem este passo
   - **Algoritmo / trace** — passos no papel ou hex/bytes
   - **Onde colocar** (obrigatório) — tabela com:
     - **Arquivo** — path sob `starter/...`
     - **Função / âncora** — nome da função ou comentário `TODO [ID]`
     - **Substituir** ou **Inserir** — o que exatamente editar (corpo, case, stub)
     - **Não mexer** — o que deixar quieto neste passo
   - Código a digitar (bloco completo, não "implemente X")
   - **Por que funciona?** — raciocínio, não só o resultado
   - Verificação manual (trace, assert, saída)
   - Checkpoint: rode teste parcial antes de avançar
4. **Debug** — mensagens de erro típicas e correções
5. **Relatório de resolução** — template para o aluno preencher

Referência de qualidade (placement): `days/2026-09-03/systems/clvm/RESOLUCAO_GUIADA_PASSO_A_PASSO.md`.  
Snippet: `docs/templates/RESOLUCAO_PLACEMENT_SNIPPET.md`.

O checker `scripts/pedagogy_check_unified.py` rejeita TODO sem bloco de placement na janela da RESOLUCAO.

### EXERCICIOS.md

Em dias legados, quatro níveis com enunciado, arquivo-alvo e critério
de aceite. Em dias `depth_first`, usar os 6–10 marcos do contrato acima.
Cada marco deve mapear a TODOs, comportamentos e critérios de aceite no
`ASSESSMENT.yaml`.

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

**Strict desde 2026-09-03:** `## Baseline`, placement por TODO, anti-delegação; repair batch: `scripts/repair_resolucao_strict.py`.

## Fluxo do aluno (START_HERE)

1. Leia `README.md` do dia e `START_HERE.md`.
2. Por módulo: TEORIA → EXERCICIOS → implemente em `starter/`.
3. Rode testes intermediários; use RESOLUCAO só ao travar.
4. Compare com `solutions/` após tentativa honesta.
5. Preencha Relatório de resolução e benchmark.

Ver também: [PORTING_GUIDE.md](PORTING_GUIDE.md), [LEARNING_PATHS.md](LEARNING_PATHS.md), [RESEARCH_NOTE_TEMPLATE.md](RESEARCH_NOTE_TEMPLATE.md).
