# Testes guiados - Drivers: descriptor rings

## Regra de trabalho
1. Escreva um teste do comportamento mais simples antes de adicionar a feature.
2. Rode e observe a falha.
3. Implemente apenas o necessario para esse teste.
4. Adicione edge case/erro relevante.
5. Quando encontrar um bug durante o exercicio, transforme-o em regression test antes de corrigir.

## Testes de referencia
A solucao limpa e seus testes estao em `solutions/` e em `projects/chris-driver-lab/`. Leia os testes somente depois de tentar escrever sua propria versao.

## Evidencia para Git
Commits recomendados: `test(...): define ...` antes de `feat(...): implement ...`. Isso deixa visivel no historico que o comportamento foi especificado antes da solucao.

## Cobertura pedagógica auditada

Os IDs abaixo precisam ter um critério de verificação antes de o módulo ser considerado concluído.

- `RING-SUBMIT-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `RING-COMPLETE-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.
- `RING-RECLAIM-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.

Arquivos de teste automatizado presentes no starter:
- `starter/tests/test_ring.cpp`
