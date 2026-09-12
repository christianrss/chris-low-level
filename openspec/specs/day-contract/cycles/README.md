# Ciclos depth-first

Cada manifesto agenda de 7 a 10 dias. Um dia possui uma única
`primary_lane`; a cobertura ampla é verificada na soma do ciclo.

Estados:

- `planned`: a agenda deve estar completa, mas os dias podem não existir;
- `active`: dias marcados `published: true` devem existir e corresponder;
- `complete`: todos os dias devem estar publicados e válidos.

Um novo `day.contract.yaml` referencia o ciclo por `cycle` e a lane por
`primary_lane`. O caminho real do projeto deve pertencer a um dos
`paths` da lane em `../tracks.yaml`.

Validação:

```powershell
python scripts/cycle_contract_check.py --cycle depth-core-01
```
