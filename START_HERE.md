# Start Here

## 1. Extract and enter repository
The delivered ZIP already contains the repository root. Do not commit the ZIP itself.

## 2. Validate before Git
```bash
python scripts/quality_check.py
python scripts/run_all_tests.py
```

## 3. Initialize Git
```bash
git init
git branch -M main
git add .
git status
git commit -m "chore: initialize low-level engineering research portfolio"
```

Create an empty GitHub repository, then:

```bash
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

## 4. Daily workflow
1. Open `days/YYYY-MM-DD/START_HERE.md` and follow the module order listed there.
2. Per module: `TEORIA_PASSO_A_PASSO.md` → `EXERCICIOS.md` → implement `TODO [ID]` in `starter/`.
3. Run module tests (look for `PEDAGOGY-TEST` markers).
4. Use `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` only when stuck (mapa starter→TODO + **Por que funciona?**).
5. Compare with `solutions/` only after your attempt.
6. Port the clean result into the corresponding `projects/` project.
7. Run `python scripts/pedagogy_check_unified.py --day YYYY-MM-DD`.
8. Run the full repository test suite and meaningful benchmarks.
9. Update `PROGRESS.md` and design/research notes.

Optional: export `Treino_LowLevel_Unificado_YYYY-MM-DD.docx` via `python scripts/build_day_docx.py --day YYYY-MM-DD`.

## 5. What belongs on GitHub
Commit source, tests, small fixtures, Markdown/CSV/JSON results, build scripts and docs. Do not commit build directories, compiler outputs, large checkpoints, VM disks or the daily ZIP. Use Releases/LFS/external model hosting only when there is a real reason.
