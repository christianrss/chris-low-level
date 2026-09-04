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
1. Read the DOCX/theory.
2. Work in `days/YYYY-MM-DD/.../starter` without reading the solution first.
3. Write the requested tests.
4. Implement in small commits.
5. Compare with `solutions/` only after your attempt.
6. Port the clean result into the corresponding `projects/` project.
7. Run the full repository test suite.
8. Run only meaningful benchmarks; record environment and methodology.
9. Update `PROGRESS.md` and design/research notes.

## 5. What belongs on GitHub
Commit source, tests, small fixtures, Markdown/CSV/JSON results, build scripts and docs. Do not commit build directories, compiler outputs, large checkpoints, VM disks or the daily ZIP. Use Releases/LFS/external model hosting only when there is a real reason.
