# START HERE — Day 01 (2026-09-03)

Laboratório unificado de low-level: 13 módulos independentes cobrindo IA, CPU, assembly, blockchain, boot, gráficos, drivers, rede, P2P, reversing, VM, terminal e tooling.

## Ordem sugerida (8–12 h total)

1. `architecture/toy_cpu` — base mental de fetch/decode/execute.
2. `assembly/x86_64_abi_sum` — contrato ABI na prática.
3. `systems/clvm` ou `tooling/miniobjdump` — leitura de binários.
4. Escolha 2 trilhas de interesse: `ai/`, `graphics/`, `network/` + `p2p/`, ou `boot/` + `hardware/`.
5. Feche com `redteam/benign_reversing` aplicando strings/YARA no binário do lab.

## Fluxo por módulo

1. Leia `README.md` e `TEORIA_PASSO_A_PASSO.md` (≥120 linhas, diagramas ASCII).
2. Abra `EXERCICIOS.md` — quatro níveis: Fácil → Médio → Difícil → Desafio.
3. Implemente no `starter/` seguindo os `TODO [ID]` (veja `TODO_MAP.md`).
4. Rode testes — procure marcadores `PEDAGOGY-TEST [ID]` nos arquivos de teste.
5. Consulte `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar; ela inclui **Relatório de resolução**.
6. Compare com `solutions/` e registre benchmark em `BENCHMARK_GUIADO.md` → **Resultados observados**.

## Regras

- Preserve IDs de TODO ao editar; o checker pedagógico exige consistência starter → testes → resolução → solution.
- Misture dificuldades: exercícios fáceis constroem vocabulário para os difíceis do mesmo dia.
- Português nos artefatos; código e identificadores permanecem em inglês quando já estabelecidos.

## Validação

Veja `VALIDATION.md` para gates executados e limitações do ambiente.
