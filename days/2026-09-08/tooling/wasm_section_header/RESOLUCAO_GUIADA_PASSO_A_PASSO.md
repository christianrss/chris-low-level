# Resolução guiada — wasm_section_header

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `TOOL-WASM-01` | `starter/wasm_section.asm` | `wasm_magic_ok` | corpo sob `TODO [TOOL-WASM-01]` | assinaturas e testes |
| `TOOL-WASM-02` | `starter/wasm_section.asm` | `wasm_version_is_1` | corpo sob `TODO [TOOL-WASM-02]` | assinaturas e testes |
| `TOOL-WASM-03` | `starter/wasm_section.asm` | `section_class` | corpo sob `TODO [TOOL-WASM-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/tooling/wasm_section_header/starter
cmake -S . -B build_ci -A x64
cmake --build build_ci --config Release
ctest --test-dir build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## TOOL-WASM-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/wasm_section.asm` |
| Função / âncora | `wasm_magic_ok` / comentário `TODO [TOOL-WASM-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem magic_ok, \0asm não é aceito.

### Algoritmo / trace

4 cmp byte [rcx+i]; EAX=1/0.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```asm
wasm_magic_ok PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-01
    cmp byte ptr [rcx], 00h
    jne fail1
    cmp byte ptr [rcx+1], 61h
    jne fail1
    cmp byte ptr [rcx+2], 73h
    jne fail1
    cmp byte ptr [rcx+3], 6Dh
    jne fail1
    mov eax, 1
    ret
fail1:
    xor eax, eax
    ret
wasm_magic_ok ENDP
```

### Por que funciona?

A rotina `wasm_magic_ok` materializa o contrato de `TOOL-WASM-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `TOOL-WASM-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `TOOL-WASM-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## TOOL-WASM-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/wasm_section.asm` |
| Função / âncora | `wasm_version_is_1` / comentário `TODO [TOOL-WASM-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem version, dword≠1 passa indevido.

### Algoritmo / trace

eax=[rcx+4]; cmp 1.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```asm
wasm_version_is_1 PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-02
    mov eax, dword ptr [rcx+4]
    cmp eax, 1
    jne fail2
    mov eax, 1
    ret
fail2:
    xor eax, eax
    ret
wasm_version_is_1 ENDP
```

### Por que funciona?

A rotina `wasm_version_is_1` materializa o contrato de `TOOL-WASM-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `TOOL-WASM-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `TOOL-WASM-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## TOOL-WASM-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/wasm_section.asm` |
| Função / âncora | `section_class` / comentário `TODO [TOOL-WASM-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem section_class, id 9 não devolve 0.

### Algoritmo / trace

CL→1/2/0.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```asm
section_class PROC
    ; PEDAGOGY-SOLUTION: TOOL-WASM-03
    movzx eax, cl
    cmp al, 1
    je one
    cmp al, 2
    jne zero
    mov eax, 2
    ret
one:
    mov eax, 1
    ret
zero:
    xor eax, eax
    ret
section_class ENDP
```

### Por que funciona?

A rotina `section_class` materializa o contrato de `TOOL-WASM-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `TOOL-WASM-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `TOOL-WASM-03` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| FAIL no Caso 1 | stub intacto / endian errado | releia o trace da TEORIA e o bloco do primeiro TODO |
| PASS parcial | size/estado desalinhado no TODO do meio | imprima pc/head/estado antes do assert |
| Crash / panic | bounds | valide Length/len antes de indexar |
| Diff de string | snprintf/format | compare caractere a caractere com o esperado |

## Relatório de resolução

| TODO | Horas | Maior bug | O que aprendia de novo |
|------|-------|-----------|------------------------|
| `TOOL-WASM-01` |  |  |  |
| `TOOL-WASM-02` |  |  |  |
| `TOOL-WASM-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
