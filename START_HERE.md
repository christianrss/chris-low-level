# Start Here

## 1. Repository vs daily ZIP
The Git repository contains source, tests, benchmarks and textual documentation. The daily ZIP additionally contains the master DOCX and package manifest. Do not commit the ZIP itself.

## 2. Validate before Git
```bash
python scripts/quality_check.py
python scripts/run_all_tests.py
```

## 3. Daily workflow
1. Read the master DOCX from the daily ZIP and the matching Markdown theory in `days/YYYY-MM-DD/`.
2. Work in `days/YYYY-MM-DD/.../starter` without reading the solution first.
3. Write the requested tests.
4. Implement in small commits.
5. Compare with `solutions/` only after your attempt.
6. Port the clean result into the corresponding `projects/` project.
7. Run the full repository test suite.
8. Run only meaningful benchmarks; record environment and methodology.
9. Update `PROGRESS.md` and design/research notes.

## 4. What belongs on GitHub
Commit source, tests, small fixtures, Markdown/CSV/JSON results, build scripts and docs. Do not commit build directories, compiler outputs, large checkpoints, VM disks, the master DOCX or the daily ZIP. Keep daily binary/document packaging as delivery artifacts, not source-history churn.
