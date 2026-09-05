# Porting guide — days/ → projects/

Cada módulo em `days/YYYY-MM-DD/<trilha>/<modulo>/` é um **laboratório isolado**. O objetivo de portfólio é consolidar o código limpo em `projects/chris-*`.

## Quando portar

Porte **depois** de:
1. Todos os `TODO [ID]` implementados no `starter/`
2. Testes com `PEDAGOGY-TEST` passando
3. Relatório de resolução preenchido
4. Benchmark registrado (ou skip honesto documentado)

Não porte código ainda quebrado ou copiado direto da `solutions/` sem entender.

## Como portar (5 passos)

1. **Identifique o projeto** — veja a seção `## Portar para projects/` no `README.md` do módulo.
2. **Extraia a API pública** — funções/classes que os testes exercitam; deixe harness de lab no `days/`.
3. **Copie/refatore** para `projects/<nome>/src/` seguindo o estilo do projeto (CMake, package.json, etc.).
4. **Replique testes críticos** — fragmentation, negative cases, edge cases do `TESTES_GUIADOS.md`.
5. **Rode o test suite do projeto** e atualize `MILESTONES.md` + `PROGRESS.md`.

## O que NÃO portar

- Arquivos `test_*.py` / `test.js` do lab verbatim (adapte para o framework do projeto)
- TODOs e marcadores `PEDAGOGY-*` no código de produção
- Scripts de scaffold (`build_rootfs.sh` de demo) sem hardening

## Checklist no Relatório de resolução

```text
Portei para projects/? [ ] Sim  [ ] Não
Projeto: projects/chris-...
Evidência: ctest / npm test / pytest — saída OK
Commit: feat(...): port X from dayYY lab
```

## Mapa completo

Consulte [`scripts/module_project_map.py`](scripts/module_project_map.py) para o mapeamento de todos os 34 módulos.

## Trilhas verticais

Após portar módulos de uma trilha, veja [`LEARNING_PATHS.md`](LEARNING_PATHS.md) para capstones que unem 2+ dias.
