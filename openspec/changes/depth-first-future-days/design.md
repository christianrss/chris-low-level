# Design: contrato depth-first

## Separação de responsabilidades

- `day.contract.yaml`: escopo, horas, projeto principal e ciclo.
- `ASSESSMENT.yaml`: conceitos, marcos, testes, falhas esperadas e rubrica.
- manifesto em `openspec/specs/day-contract/cycles/`: cobertura planejada.
- `day_contract_check.py`: estrutura de um dia.
- `cycle_contract_check.py`: amplitude ao longo do ciclo.
- `pedagogy_check_unified.py`: profundidade e autoria esperada.
- `run_day_tests.py`: evidência executável sem converter skip em sucesso.

## Compatibilidade

O tier-A histórico permanece data-driven. Dias anteriores ao início do
perfil não recebem regras novas implicitamente. Um `day.contract.yaml`
explícito sempre tem precedência.

## Unidade curricular

Um projeto continua armazenado em
`days/YYYY-MM-DD/<trilha>/<projeto>/`, para reutilizar runners e
inventário. “Um projeto” equivale a um módulo detectável no filesystem,
mas o material passa a descrevê-lo como um sistema integrado, não como
uma coleção de microtarefas.

## Medidas anti-gaming

Nenhuma métrica isolada decide qualidade. O gate combina:

1. delta de código em globs `student_owned`;
2. limite de lógica já pronta no starter;
3. marcos e comportamentos declarados;
4. testes felizes, adversos e end-to-end;
5. mutantes críticos que os testes devem rejeitar;
6. baseline exato do starter;
7. traces, invariantes e benchmark vinculados ao projeto.

Contagem de linhas é um orçamento de trabalho, não substituto para
revisão pedagógica.

## Ciclos

Um ciclo possui 7–10 dias e lanes curriculares. Enquanto `status` for
`planned`, o gate valida a programação. Em `active`, valida dias já
publicados e mantém a programação completa. Em `complete`, todos os
dias e contratos referenciados devem existir e passar.
