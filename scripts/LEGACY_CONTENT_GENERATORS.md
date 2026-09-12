# Geradores de conteúdo legado

Scripts com nomes `scaffold_day*`, `upgrade_*`, `repair_*`, `deepen_*`
ou `rewrite_days_*` foram usados para manter os dias até 2026-09-11.
Eles não são fonte pedagógica e não podem criar ou preencher teoria,
resolução ou exercícios de dias `depth_first`.

Para dias novos:

1. escreva a proposta OpenSpec;
2. copie apenas templates de contrato/assessment/rubrica;
3. produza o conteúdo específico do projeto manualmente;
4. use `generate_day_scaffold.py --manifest-only` somente para inventário.

Automação continua permitida para tarefas mecânicas verificáveis:
manifesto, formatação, execução de testes e validação dos contratos.
