# Prompt Mestre — Treino Low-Level Unificado

Este repositório mantém o prompt em dois arquivos:

1. **[PROMPT_MESTRE_EXTREME_QUALITY.md](PROMPT_MESTRE_EXTREME_QUALITY.md)** — diretivas de qualidade extrema, reorganização, thresholds e workflow (seções 0, 41–50). **Leia primeiro.**

2. **[PEDAGOGY_STANDARD.md](PEDAGOGY_STANDARD.md)** — padrão O quê / Como / Por quê; MD modular como formato principal.

3. **Prompt base completo** — o arquivo original do usuário em `Prompt mestre — Treino Low-Level Diário.md` (seções 1–40): regra "não resuma", estrutura de módulos, trilhas permanentes, gate final.

## Uso para agentes (Cursor)

Ao gerar ou corrigir um dia:

```bash
python scripts/upgrade_module_quality.py --day YYYY-MM-DD
python scripts/generate_day_scaffold.py --day YYYY-MM-DD
python scripts/pedagogy_check_unified.py --day YYYY-MM-DD
python scripts/run_day_tests.py --day YYYY-MM-DD --mode solutions
python scripts/build_day_docx.py --day YYYY-MM-DD   # opcional
```

## Padrão mínimo por módulo

| Artefato | Mínimo |
|----------|--------|
| TEORIA_PASSO_A_PASSO.md | 120 linhas + diagrama + O quê/Como/Por quê |
| RESOLUCAO_GUIADA_PASSO_A_PASSO.md | 80–450 linhas + mapa starter + Relatório |
| EXERCICIOS.md | 4 níveis |
| DOCX por dia | opcional (export dos MD) |

## Retroatividade

Days 01, 02 e 03 devem obedecer as mesmas regras. Corrija dias anteriores quando novas diretivas surgirem.
