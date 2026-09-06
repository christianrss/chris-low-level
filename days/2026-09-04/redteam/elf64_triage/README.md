# Red Team seguro: triagem ELF64

Você analisa fixtures sintéticos/benignos e o lab target próprio. Objetivo: parsing defensivo de Ehdr, program headers, section headers (com nomes) e símbolos dinâmicos — sem malware e sem execução de binários desconhecidos.

## Projeto cumulativo
`projects/chris-binary-toolkit`

## Fluxo sugerido
1. Leia `TEORIA_PASSO_A_PASSO.md` (tabelas Phdr/Shdr).
2. Siga `EXERCICIOS.md` / TODOs no `starter/tools/`.
3. Implemente antes de consultar `solutions/`.
4. Rode `TESTES_GUIADOS.md`.
5. Execute o benchmark e registre ambiente/resultados.

## TODOs

| ID | Função |
|----|--------|
| `D2-ELF-STRINGS` | `extract_ascii_strings` |
| `D2-ELF-HEADER` | `parse_elf64_header` |
| `D2-ELF-PHDR` | `parse_program_headers` |
| `D2-ELF-SHDR` | `parse_section_headers` |
| `D2-ELF-DYNSYM` | `list_dynamic_symbols` |

## Portar para projects/

| Item | Detalhe |
|------|---------|
| Projeto | `projects/chris-binary-toolkit` |
| O que levar | ELF64 triage (Ehdr+Phdr+Shdr+Dynsym+strings) |
| Testes a replicar | `test_elf64.py`, `elf64_benchmark.py` |
| Milestone | MILESTONES.md — ELF triage |
| Commit sugerido | `feat(toolkit): port elf64 triage from day02 lab` |

Após portar, marque no **Relatório de resolução**: *Portei para projects/? Sim/Não — evidência: comando de teste que passou*.
