# Testes guiados - Boot sector BIOS de 512 bytes

## Regra de trabalho
### Caso 1: Escreva um teste do comportamento mais simples antes de adicionar a feature.
### Caso 2: Rode e observe a falha.
### Caso 3: Implemente apenas o necessario para esse teste.
### Caso 4: Adicione edge case/erro relevante.
### Caso 5: Quando encontrar um bug durante o exercicio, transforme-o em regression test antes de corrigir.

## Testes de referencia
A solucao limpa e seus testes estao em `solutions/` e em `projects/chris-boot/`. Leia os testes somente depois de tentar escrever sua propria versao.

## Evidencia para Git
Commits recomendados: `test(...): define ...` antes de `feat(...): implement ...`. Isso deixa visivel no historico que o comportamento foi especificado antes da solucao.

## Cobertura pedagógica auditada

Os IDs abaixo precisam ter um critério de verificação antes de o módulo ser considerado concluído.

- `BOOT-IMAGE-01` — coberto pela sequência de testes/validação descrita neste arquivo; a solução correspondente também é verificada pelo `pedagogy_check`.

Arquivos de teste automatizado presentes no starter:
- `starter/tests/test_boot.py`
## Execução real (opcional)

**Pré-requisitos:** NASM, QEMU (`qemu-system-x86_64`).

```bash
python scripts/run_real_env_checklist.py --module boot/legacy_bootsector --day 2026-09-03
```
