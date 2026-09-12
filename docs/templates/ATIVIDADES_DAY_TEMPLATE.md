# ATIVIDADES — YYYY-MM-DD

**Perfil:** `depth_first` | **1 projeto** | **6–8 h**
**Regra:** não avance sem evidência do checkpoint. Testes PASS sozinhos
não demonstram entendimento.

---

## M1 — Baseline e previsão (30 min)

- [ ] Ler `START_HERE.md` e `README.md`
- [ ] Executar o starter e registrar as falhas previstas no assessment:

```powershell
python scripts/run_day_tests.py --day YYYY-MM-DD --mode starter --expect-fail
```

## M2 — Modelo mental e testes (60–75 min)

- [ ] Produzir um trace feliz e um trace de falha.
- [ ] Explicar as invariantes com palavras próprias.
- [ ] Relacionar cada trust boundary a um caso de teste.

## M3 — Caminho mínimo end-to-end (2–3 h)

- [ ] Construir entrada → núcleo → saída observável.
- [ ] Rodar o teste end-to-end antes de otimizar.

## M4 — Robustez (60–90 min)

- [ ] Tratar os quatro modos de falha do `ASSESSMENT.yaml`.
- [ ] Confirmar que os mutantes críticos são rejeitados.

## M5 — Integração e ergonomia (45–60 min)

- [ ] Usar somente a API pública entre componentes.
- [ ] Documentar limitações e não objetivos.

## M6 — Medição e síntese (45–60 min)

- [ ] Registrar hipótese antes do benchmark.
- [ ] Guardar dados, mediana, p95 e interpretação.
- [ ] Preencher `RUBRIC.md` com evidências.
