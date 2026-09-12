# Resolução guiada — clvm_xdbg

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `XDBG-LOAD-01` | `starter/src/session.cpp` | `Session::load` |
| `XDBG-HEX-01` | `starter/src/session.cpp` | `Session::hex_dump` |
| `XDBG-DISASM-01` | `starter/src/session.cpp` | `Session::disasm` |
| `XDBG-REGS-01` | `starter/src/session.cpp` | `Session::regs` |
| `XDBG-MEM-01` | `starter/src/session.cpp` | `Session::mem_view` |
| `XDBG-STEP-01` | `starter/src/session.cpp` | `Session::step` (apêndice) |
| `XDBG-BREAK-01` | `starter/src/session.cpp` | `set_break` / `cont` |
| `XDBG-ERR-01` | `starter/src/session.cpp` | mensagens em `step` |

Não edite `host/` nem `tools/assemble.py`. Helpers (`read_i32_le`,
`mem_in_bounds`, `hex_byte`) podem viver no mesmo `session.cpp`.

## Baseline

```powershell
cmake -S days/2026-09-12/systems/clvm_xdbg/starter -B days/2026-09-12/systems/clvm_xdbg/starter/build_ci
cmake --build days/2026-09-12/systems/clvm_xdbg/starter/build_ci
ctest --test-dir days/2026-09-12/systems/clvm_xdbg/starter/build_ci --output-on-failure
```

Esperado: **FAIL**. `load` devolve `not implemented`; o processo sai
com `parse error` antes do REPL. Guarde essa saída.

## XDBG-LOAD-01 — parse e PC inicial

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `Session::load` — `TODO [XDBG-LOAD-01]` |
| **Substituir** | o corpo que grava `not implemented` |
| **Não mexer** | `host/clvm_loader.c` (já valida magic/FNV) |

### O problema

Sem copiar `file` e chamar `clvm_parse`, nenhuma view tem imagem.
Imagens curtas precisam ecoar `file too small`.

### Algoritmo / trace

```text
file = bytes copiados
clvm_parse(file) → image.code aponta para file+16
pc = image.entry   # 0 em add2
mem[] = 0; stacks vazias
```

### Escreva o código

```cpp
bool Session::load(const std::uint8_t* data, std::size_t n) {
    file.assign(data, data + n);
    mem.fill(0);
    data_stack.clear();
    call_stack.clear();
    prints.clear();
    steps = 0;
    last_error.clear();
    char error[128]{};
    if (!clvm_parse(file.data(), file.size(), &image, error, sizeof(error))) {
        last_error = error;
        status = DbgStatus::Error;
        return false;
    }
    pc = image.entry;
    loaded = true;
    status = DbgStatus::Ready;
    return true;
}
```

### Por que funciona

O vetor `file` é o owner. `image.code` permanece válido. O loader já
conhece o contrato Dia 01; você só propaga `error`.

### Verifique

Caso 1 e caso 11: `ready pc=0` em add2; 8 bytes → `file too small`.

## XDBG-HEX-01 — dump com tags

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `Session::hex_dump` — `TODO [XDBG-HEX-01]` |
| **Substituir** | o `return {}` |
| **Não mexer** | a RAM (`mem_view` é outro comando) |

### O problema

Sem offsets e sem a palavra `header`, o teste não distingue os 16
primeiros bytes do code.

### Algoritmo / trace

```text
offset 0x00: 16 bytes, tag header, começa 43 4C 56 4D
offset 0x10: code, começa 01 03 00 00 00  (PUSH 3)
```

### Escreva o código

```cpp
std::string Session::hex_dump() const {
    std::ostringstream out;
    for (std::size_t offset = 0; offset < file.size(); offset += 16) {
        out << hex_offset(offset) << "  ";
        const std::size_t end = std::min(offset + 16, file.size());
        for (std::size_t i = offset; i < end; ++i) {
            if (i != offset) out << ' ';
            out << hex_byte(file[i]);
        }
        out << "  " << (offset < 16 ? "header" : "code") << '\n';
    }
    return out.str();
}
```

(`hex_offset` / `hex_byte`: 4 e 2 dígitos hex uppercase, zero-pad.)

### Por que funciona

Offset de arquivo, não PC. A tag depende de `offset < 16`, não do
conteúdo ASCII.

### Verifique

Caso 2: `43 4C 56 4D`, `header`, `code`, `0000`, `0010`.

## XDBG-DISASM-01 — PUSH i32 e CALL i16

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `Session::disasm` — `TODO [XDBG-DISASM-01]` |
| **Substituir** | o `return {}` |
| **Não mexer** | `pc` (disasm é read-only) |

### O problema

Decoder que ignora 4 bytes de PUSH lê o `03` seguinte como ADD
(mutante OPSIZE). CALL precisa do i16 com sinal.

### Algoritmo / trace

```text
pc=0  opcode 0x01 → PUSH, i32 LE = 3
pc=10 opcode 0x0B → CALL, i16 LE = +2
```

### Escreva o código

```cpp
std::string Session::disasm() const {
    std::ostringstream out;
    out << "pc=" << pc << ' ' << mnemonic(op_at_pc);
    if (width == 4) out << ' ' << read_i32_le(image.code + pc + 1);
    if (width == 2) out << ' ' << std::showpos << read_i16_le(image.code + pc + 1);
    return out.str();
}
```

Complete `op_at_pc` / `width` com a tabela da teoria. Truncamento do
operando: sufixo ` <truncated>`.

### Por que funciona

O i16 é relativo ao PC **após** o operando; o dump mostra o
displacement cru (`+2`), não o label `add2`.

### Verifique

Casos 3 e 4.

## XDBG-REGS-01 — snapshot

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `Session::regs` — `TODO [XDBG-REGS-01]` |
| **Substituir** | o `return {}` |
| **Não mexer** | o formato `data=[3,5]` (sem espaços) |

### O problema

Sem este texto o teste não vê CALL empilhar 13.

### Algoritmo / trace

Após três steps de add2: `pc=15`, `data=[3,5]`, `call=[13]`.

### Escreva o código

```cpp
std::string Session::regs() const {
    std::ostringstream out;
    out << "pc=" << pc << '\n';
    out << "status=" << status_name(status) << '\n';
    out << "data=" << format_i32_list(data_stack) << '\n';
    out << "call=" << format_size_list(call_stack) << '\n';
    out << "prints=" << format_i32_list(prints) << '\n';
    out << "steps=" << steps << '\n';
    return out.str();
}
```

### Por que funciona

Duas listas distintas. RET vazio não aparece aqui — aparece como erro.

### Verifique

Caso 6. Checkpoint: `call=[13]` só depois do CALL, não depois do RET.

## XDBG-MEM-01 — dump da RAM

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `Session::mem_view` — `TODO [XDBG-MEM-01]` |
| **Substituir** | o `return {}` |
| **Não mexer** | `hex_dump` (arquivo ≠ RAM) |

### O problema

STORE 42 em 0 tem de ser visível como `2A 00 00 00`. Sem dump, o aluno
só acredita no PRINT.

### Algoritmo / trace

```text
pop addr=0, pop value=42
mem[0]=0x2A, mem[1]=0, mem[2]=0, mem[3]=0
```

### Escreva o código

```cpp
std::string Session::mem_view(std::size_t addr, std::size_t len) const {
    if (addr >= 256) return {};
    if (len > 256 - addr) len = 256 - addr;
    std::ostringstream out;
    for (std::size_t off = 0; off < len; off += 16) {
        out << hex_offset(addr + off) << "  ";
        /* bytes mem[addr+off ...] como em hex_dump */
        out << '\n';
    }
    return out.str();
}
```

O STORE em si vive em `step` (apêndice) e **deve** chamar
`mem_in_bounds`.

### Por que funciona

Little-endian explícito: 42 cabe num byte; os outros três são zero.
254 falha porque 254+4>256.

### Verifique

Caso 7 e caso 14.

## XDBG-BREAK-01 — continue com pouso

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `set_break` e `cont` — `TODO [XDBG-BREAK-01]` |
| **Substituir** | `return false` / `return step()` |
| **Não mexer** | a ISA dentro de `step` |

### O problema

`continue` que chama um `run()` opaco nunca para no PRINT. `continue`
que testa o breakpoint **antes** do primeiro step não sai do PC atual.

### Algoritmo / trace

```text
break 13
first step always runs
depois, se pc está em breaks → status=breakpoint, NÃO executa
add2 para em PRINT com prints=[]
```

### Escreva o código

```cpp
bool Session::set_break(std::size_t at) {
    breaks.insert(at);
    return true;
}

DbgStatus Session::cont() {
    if (status == DbgStatus::Breakpoint) status = DbgStatus::Ready;
    bool first = true;
    while (status == DbgStatus::Ready) {
        if (!first && breaks.count(pc)) {
            status = DbgStatus::Breakpoint;
            return status;
        }
        first = false;
        step();
    }
    return status;
}
```

### Por que funciona

O “passo de saída” (`first=true`) é o mesmo contrato de gdb. Sem
breakpoints o loop cai em HALT ou `Error`.

### Verifique

Casos 8 e 9.

## XDBG-ERR-01 — strings estáveis

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/src/session.cpp` |
| **Função / âncora** | `TODO [XDBG-ERR-01]` dentro de `step` |
| **Substituir** | qualquer `cerr` improvisado; use `last_error` |
| **Não mexer** | as frases abaixo (os testes buscam substring) |

### O problema

Erro sem `return` (Dia 04 `bad CALL`) continua executando. Mensagem
errada (`stack underflow` no RET nua) ensina a pilha errada.

### Algoritmo / trace

| Situação | `last_error` |
|----------|----------------|
| parse curto | `file too small` (via loader) |
| opcode 0xFF | `unknown opcode` |
| PRINT nua | `stack underflow` |
| STORE 254 | `memory out of bounds` |
| RET nua | `return stack underflow` |

### Escreva o código

```cpp
DbgStatus fail(Session& s, const char* msg) {
    s.last_error = msg;
    s.status = DbgStatus::Error;
    return s.status;
}
// default: return fail(*this, "unknown opcode");
// RET vazio: return fail(*this, "return stack underflow");
```

O switch completo, com `need(4)` no PUSH e `mem_in_bounds` em
LOAD/STORE, está no apêndice `XDBG-STEP-01`.

### Por que funciona

Uma função `fail` evita cair no `default` depois de um erro. As
strings são o contrato com `test_xdbg.py`.

### Verifique

Casos 11–15. Mutantes: `python tests/run_mutant_check.py MUTANT-NO-BOUNDS`
e `MUTANT-OPSIZE`.

## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| `parse error: not implemented` | `load` ainda stub | XDBG-LOAD-01 |
| hex sem `header` | dump só de `image.code` | iterar `file` |
| `CALL` vira lixo | PUSH sem `pc += 4` | operand_bytes=4 |
| `prints=[8]` cedo demais no break | continue executa o PC marcado | flag `first` |
| AV no STORE 254 | sem `mem_in_bounds` | predicar addr+4 |
| `stack underflow` no RET | uma pilha só | call_stack.empty() |

## Relatório de resolução

- Paper-trace de add2 (PCs e as duas pilhas):
- Falha que você viu no baseline:
- Mutante que seus testes matam e por quê:
- Limitação consciente (sem GUI, sem símbolos):
