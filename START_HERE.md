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
1. Days through 2026-09-11 are legacy reference material; new days use one depth-first project.
2. Open `day.contract.yaml`, `ASSESSMENT.yaml` and the day's `START_HERE.md`.
3. Run the starter baseline and record the expected failures before coding.
4. Follow milestones M1–M6: model, tests, end-to-end core, robustness, integration and measurement.
5. Build the files marked `student_owned`; the starter should provide almost no final logic.
6. Use `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` progressively only after recording a hypothesis.
7. Compare with `solutions/`, run the benchmark and complete `RUBRIC.md`.
8. Port the clean result into the corresponding `projects/` project.
9. Run pedagogy, day contract, starter expected-fail, solutions and cycle gates.

Optional: export `Treino_LowLevel_Unificado_YYYY-MM-DD.docx` via `python scripts/build_day_docx.py --day YYYY-MM-DD`.

## 5. What belongs on GitHub
Commit source, tests, small fixtures, Markdown/CSV/JSON results, build scripts and docs. Do not commit build directories, compiler outputs, large checkpoints, VM disks or the daily ZIP. Use Releases/LFS/external model hosting only when there is a real reason.
