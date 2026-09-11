# Resolução guiada — pe_export_triage

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `RT-PE-EXP-01` | `starter/pe_export_triage.py` | `validate_mz_pe` | corpo sob `TODO [RT-PE-EXP-01]` | assinaturas e testes |
| `RT-PE-EXP-02` | `starter/pe_export_triage.py` | `count_export_names` | corpo sob `TODO [RT-PE-EXP-02]` | assinaturas e testes |
| `RT-PE-EXP-03` | `starter/pe_export_triage.py` | `flag_suspicious_exports` | corpo sob `TODO [RT-PE-EXP-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/redteam/pe_export_triage/starter
python test_pe_export_triage.py
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## RT-PE-EXP-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pe_export_triage.py` |
| Função / âncora | `validate_mz_pe` / comentário `TODO [RT-PE-EXP-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem validate, bytes aleatórios passam.

### Algoritmo / trace

MZ + unpack e_lfanew + PE.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```python
def validate_mz_pe(data: bytes) -> bool:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-01
    if len(data) < 0x40 or data[0:2] != b"MZ":
        return False
    import struct
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    return pe_off + 4 <= len(data) and data[pe_off:pe_off + 2] == b"PE"
```

### Por que funciona?

A rotina `validate_mz_pe` materializa o contrato de `RT-PE-EXP-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `RT-PE-EXP-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `RT-PE-EXP-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## RT-PE-EXP-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pe_export_triage.py` |
| Função / âncora | `count_export_names` / comentário `TODO [RT-PE-EXP-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem count, a lista de nomes não é medida.

### Algoritmo / trace

validate; return len(names) ou -1.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```python
def count_export_names(data: bytes, names: list[str]) -> int:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-02
    if not validate_mz_pe(data):
        return -1
    return len(names)
```

### Por que funciona?

A rotina `count_export_names` materializa o contrato de `RT-PE-EXP-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `RT-PE-EXP-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `RT-PE-EXP-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## RT-PE-EXP-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/pe_export_triage.py` |
| Função / âncora | `flag_suspicious_exports` / comentário `TODO [RT-PE-EXP-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem flag, VirtualAlloc não é marcado.

### Algoritmo / trace

filter names ∈ SUSPICIOUS.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```python
def flag_suspicious_exports(names: list[str]) -> list[str]:
    # PEDAGOGY-SOLUTION: RT-PE-EXP-03
    flagged = []
    for n in names:
        if n in SUSPICIOUS:
            flagged.append(n)
    return flagged
```

### Por que funciona?

A rotina `flag_suspicious_exports` materializa o contrato de `RT-PE-EXP-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `RT-PE-EXP-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `RT-PE-EXP-03` PASS no starter
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
| `RT-PE-EXP-01` |  |  |  |
| `RT-PE-EXP-02` |  |  |  |
| `RT-PE-EXP-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
