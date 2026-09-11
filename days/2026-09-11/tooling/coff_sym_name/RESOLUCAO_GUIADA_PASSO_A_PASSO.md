# Resolução guiada — coff_sym_name

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `TOOL-COFF-01` | `starter/coff_sym.asm` (ou `.S`) | `coff_name_is_long` |
| `TOOL-COFF-02` | `starter/coff_sym.asm` | `coff_name_is_short` |
| `TOOL-COFF-03` | `starter/coff_sym.asm` | `coff_short_name_len` |

## Baseline

```powershell
cd days/2026-09-11/tooling/coff_sym_name/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.

## TOOL-COFF-01

### Onde colocar (TOOL-COFF-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/coff_sym.asm` |
| Função | `coff_name_is_long` |
| Substituir | o corpo sob o comentário `TODO [TOOL-COFF-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

DWORD [rcx]==0 → 1.

### Algoritmo / trace

cmp dword; sete eax.

### Escreva o código

```asm
    cmp dword ptr [rcx], 0
    jne fail
    mov eax, 1
    ret
fail:
    xor eax, eax
    ret
```

### Por que funciona?

Convenção COFF de nome longo.

### Verifique

longn→1, shortn→0.

### Código completo alinhado ao solutions/ (TOOL-COFF-01)

```asm
PEDAGOGY-SOLUTION: TOOL-COFF-01
    cmp dword ptr [rcx], 0
    jne L0
    mov eax, 1
    ret
L0:
    xor eax, eax
    ret
coff_name_is_long ENDP
coff_name_is_short PROC
    ; 
```

## TOOL-COFF-02

### Onde colocar (TOOL-COFF-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/coff_sym.asm` |
| Função | `coff_name_is_short` |
| Substituir | o corpo sob o comentário `TODO [TOOL-COFF-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Inverso do long.

### Algoritmo / trace

se DWORD!=0 retorne 1.

### Escreva o código

```asm
    cmp dword ptr [rcx], 0
    je zero
    mov eax, 1
    ret
zero:
    xor eax, eax
    ret
```

### Por que funciona?

short e long são mutuamente exclusivos neste lab.

### Verifique

shortn→1.

### Código completo alinhado ao solutions/ (TOOL-COFF-02)

```asm
PEDAGOGY-SOLUTION: TOOL-COFF-02
    cmp dword ptr [rcx], 0
    je S0
    mov eax, 1
    ret
S0:
    xor eax, eax
    ret
coff_name_is_short ENDP
coff_short_name_len PROC
    ; 
```

## TOOL-COFF-03

### Onde colocar (TOOL-COFF-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/coff_sym.asm` |
| Função | `coff_short_name_len` |
| Substituir | o corpo sob o comentário `TODO [TOOL-COFF-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

main → 4.

### Algoritmo / trace

conte até NUL ou 8.

### Escreva o código

```asm
    xor eax, eax
loop1:
    cmp eax, 8
    jge done
    cmp byte ptr [rcx+rax], 0
    je done
    inc eax
    jmp loop1
done:
    ret
```

### Por que funciona?

strnlen ≤8 sem libc.

### Verifique

len==4.

### Código completo alinhado ao solutions/ (TOOL-COFF-03)

```asm
PEDAGOGY-SOLUTION: TOOL-COFF-03
    xor eax, eax
    mov rdx, rcx
L1:
    cmp eax, 8
    jge L2
    cmp byte ptr [rdx+rax], 0
    je L2
    inc eax
    jmp L1
L2:
    ret
coff_short_name_len ENDP
END

.global coff_name_is_long
.global coff_name_is_short
.global coff_short_name_len
.text
coff_name_is_long:
    # 
```

## Debug

| Sintoma | Correção |
|---------|----------|
| RCX errado | 1º arg Windows |

## Relatório de resolução

- TODOs: [ ]
