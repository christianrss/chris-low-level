# Pesquisa guiada — ELF program headers

## Fontes primárias / técnicas

- [System V ABI — ELF](https://refspecs.linuxbase.org/elf/elf.pdf) — layout Ehdr/Phdr.
- `man 5 elf` no Linux — resumo operacional.
- Ferramenta: `readelf -l` em binário local (compare com seu parser).

## Perguntas antes de implementar

1. Qual diferença entre **section header table** e **program header table**?
2. Por que `p_memsz` pode ser **maior** que `p_filesz` em PT_LOAD?
3. Quais três campos do Phdr exigem validação contra `len(file)`?
4. O que significa `p_align` para o loader?

## Investigação prática

1. Hex dump dos primeiros 64 bytes de um ELF64 real — marque `e_phoff`, `e_phnum`.
2. Liste riscos de parser que decodifica PHDR **antes** de validar bounds da tabela.
3. Compare `PT_LOAD` vs `PT_GNU_RELRO` — por que triage começa em LOAD?

## Depois da implementação

Documente simplificações do lab, invariante principal (`p_offset+p_filesz ≤ len`) e métrica de robustez (ex.: % inputs malformados rejeitados antes de loop).
