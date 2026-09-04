# Start here

## 1. Extract the ZIP

The extracted directory is already the repository root. Do not move the modules around.

## 2. Create the Git repository

```bash
git init
git branch -M main
git add .
git status
git commit -m "chore: initialize low-level engineering portfolio"
```

Then create an empty repository on GitHub and connect it:

```bash
git remote add origin <YOUR-REPOSITORY-URL>
git push -u origin main
```

Do **not** commit the original ZIP, compiler build directories, executables, PDB files, virtual environments or benchmark dumps larger than necessary.

## 3. How to study Day 01

Open:

`days/2026-09-03/Treino_LowLevel_Unificado_2026-09-03.docx`

Recommended order:

1. Systems - CLVM
2. AI - linear model and scalar autograd
3. Safe reverse engineering
4. MiniObjdump / disassembler
5. 3D + physics + animation

For each module:

1. read `TEORIA_PASSO_A_PASSO.md`;
2. attempt the code under `starter/`;
3. write the guided tests before opening the final solution;
4. use `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` when blocked;
5. compare with `solutions/`;
6. run the tests;
7. run the benchmark and record your machine in the result file;
8. update the related clean project in `projects/`.

## 4. A useful commit strategy

Do not commit all exercises as a single giant change. Suggested Day 01 commits:

```text
docs(day01): add low-level theory and lab plan
test(vm): add CLVM format and execution tests
feat(vm): implement checksum and bytecode execution
feat(ai): implement manual linear regression training
test(ai): add gradient and autograd checks
feat(tooling): parse executable sections and decode first opcodes
test(tooling): add binary inspection regression tests
feat(graphics): add portable math and physics core
test(graphics): add transform and physics regression tests
bench(day01): record first portable baselines
```

This produces a Git history that communicates engineering progress.
