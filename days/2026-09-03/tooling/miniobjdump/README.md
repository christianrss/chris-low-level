# Ordem de estudo deste módulo

1. Leia `TEORIA_PASSO_A_PASSO.md`.
2. Abra `starter/` e localize os TODOs.
3. Siga `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` sem pular etapas.
4. Compile/teste após cada etapa.
5. Só então compare com `solutions/`.

---

# MiniObjdump cross-platform - PE/ELF inspector + x86-64 decoder

O pacote anterior usava uma abordagem muito ligada ao ambiente Linux. Esta versão foi reescrita para compilar com MSVC, GCC e Clang sem depender de `<elf.h>`.

## Objetivo

Construir a base da sua futura suíte estilo objdump / PE-bear / IDA / Ghidra:

1. identificar PE ou ELF pelos bytes do arquivo;
2. listar sections de ELF64 little-endian;
3. listar sections de PE32/PE32+;
4. localizar `.text`;
5. percorrer bytes e decodificar um subconjunto de x86-64;
6. usar fallback `db 0xNN` para instruções ainda desconhecidas.

## Exercícios

- **Fácil:** complete `read_u16_le()` e `read_u32_le()` no starter.
- **Médio:** termine a listagem das sections PE ou ELF.
- **Difícil:** implemente `CALL rel32` e `JMP rel32` calculando o endereço-alvo.
- **Desafio:** construa basic blocks e um CFG mínimo a partir de branches conhecidos.

## Comparação com ferramentas reais

Depois de executar o seu programa em um binário próprio, compare com:

```bash
objdump -d <arquivo>
readelf -S <arquivo>
```

No Windows, compare também com `dumpbin /headers` e, opcionalmente, PE-bear em um executável próprio.

## Build

```bash
cmake -S solutions -B build
cmake --build build
```

No Visual Studio:

```bat
cmake -S solutions -B build-solution -A x64
cmake --build build-solution --config Release
```
