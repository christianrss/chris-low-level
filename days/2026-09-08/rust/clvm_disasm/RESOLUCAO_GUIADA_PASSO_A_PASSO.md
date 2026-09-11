# Resolução guiada — clvm_disasm

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora | Substituir | Não mexer |
|---------|---------|-----------------|------------|-----------|
| `CLVM-RS-DIS-01` | `starter/src/lib.rs` | `opcode_name` | corpo sob `TODO [CLVM-RS-DIS-01]` | assinaturas e testes |
| `CLVM-RS-DIS-02` | `starter/src/lib.rs` | `instruction_size` | corpo sob `TODO [CLVM-RS-DIS-02]` | assinaturas e testes |
| `CLVM-RS-DIS-03` | `starter/src/lib.rs` | `disassemble` | corpo sob `TODO [CLVM-RS-DIS-03]` | assinaturas e testes |

## Baseline

```powershell
cd days/2026-09-08/rust/clvm_disasm/starter
cargo test
```

**Esperado antes dos TODOs:** FAIL (stub, NotImplemented, assert, ou retorno de erro).

Registre a mensagem de falha. Só avance quando souber qual TODO desbloqueia o Caso 1.

## CLVM-RS-DIS-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `opcode_name` / comentário `TODO [CLVM-RS-DIS-01]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem nomes, HALT/ADD não listam.

### Algoritmo / trace

match op → Some(nome) ou None.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```rust
pub fn opcode_name(op: u8) -> Option<&'static str> {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-01
    match op {
        0x02 => Some("ADD"),
        0x08 => Some("HALT"),
        0x09 => Some("JMP"),
        PUSH => Some("PUSH"),
        _ => None,
    }
}
```

### Por que funciona?

A rotina `opcode_name` materializa o contrato de `CLVM-RS-DIS-01`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-RS-DIS-01`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-RS-DIS-01` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## CLVM-RS-DIS-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `instruction_size` / comentário `TODO [CLVM-RS-DIS-02]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Size errado desalinha o walk Rust.

### Algoritmo / trace

PUSH→5; branch set→3; senão 1.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```rust
pub fn instruction_size(op: u8) -> usize {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-02
    if op == PUSH {
        5
    } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {
        3
    } else {
        1
    }
}
```

### Por que funciona?

A rotina `instruction_size` materializa o contrato de `CLVM-RS-DIS-02`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-RS-DIS-02`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-RS-DIS-02` PASS no starter
- [ ] Não quebrei TODOs anteriores
- [ ] Entendi o *porquê* do size/estado, não só o resultado

---

## CLVM-RS-DIS-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `disassemble` / comentário `TODO [CLVM-RS-DIS-03]` |
| Substituir | corpo do stub (mantenha a assinatura) |
| Não mexer | headers, testes, outros TODOs neste passo |

### O problema

Sem disassemble, Result não devolve PUSH 42.

### Algoritmo / trace

while pc: decode PUSH/branch/name; Err se truncado/unknown.

No papel, execute o Caso ligado a este TODO com os números de `TEORIA_PASSO_A_PASSO.md`
antes de digitar. Confirme size/estado/retorno esperado.

### Escreva o código

```rust
pub fn disassemble(code: &[u8]) -> Result<Vec<String>, String> {
    // PEDAGOGY-SOLUTION: CLVM-RS-DIS-03
    let mut out = Vec::new();
    let mut pc = 0usize;
    while pc < code.len() {
        let op = code[pc];
        if op == PUSH {
            if pc + 5 > code.len() {
                return Err("truncated PUSH".into());
            }
            let imm = u32::from_le_bytes(code[pc + 1..pc + 5].try_into().unwrap());
            out.push(format!("PUSH {}", imm));
            pc += 5;
        } else if matches!(op, 0x09 | 0x0A | 0x0B | 0x13) {
            if pc + 3 > code.len() {
                return Err("truncated branch".into());
            }
            let off = u16::from_le_bytes(code[pc + 1..pc + 3].try_into().unwrap());
            let name = opcode_name(op).unwrap_or("BR");
            out.push(format!("{} {}", name, off));
            pc += 3;
        } else if let Some(name) = opcode_name(op) {
            out.push(name.to_string());
            pc += 1;
        } else {
            return Err(format!("unknown op 0x{:02x}", op));
        }
    }
    Ok(out)
}
```

### Por que funciona?

A rotina `disassemble` materializa o contrato de `CLVM-RS-DIS-03`: os mesmos números do trace
da teoria aparecem no assert. Cada branch de erro (-1 / Err / false / ValueError)
corresponde a um caso negativo documentado em `TESTES_GUIADOS.md`.

### Verifique

1. Recompile/rode só o caminho que exerce `CLVM-RS-DIS-03`.
2. Confira o valor numérico (não só “passou”).
3. Se falhar, diff hex/estado com o trace da TEORIA.

### Checkpoint

- [ ] `CLVM-RS-DIS-03` PASS no starter
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
| `CLVM-RS-DIS-01` |  |  |  |
| `CLVM-RS-DIS-02` |  |  |  |
| `CLVM-RS-DIS-03` |  |  |  |

Síntese (3–5 linhas): o que o wire-format/estado deste módulo força você a respeitar
que uma API de alto nível esconderia.
