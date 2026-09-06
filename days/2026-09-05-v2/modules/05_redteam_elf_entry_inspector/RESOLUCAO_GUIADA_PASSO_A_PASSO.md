## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| `RT-ELF-HDR-01` | `starter/elf_entry.py` |
| `RT-ELF-ENTRY-02` | `starter/elf_entry.py` |

# Resolução guiada passo a passo

Abra `starter/elf_entry.py`.

## `parse_ident` - RT-ELF-HDR-01

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/elf_entry.py` |
| **Função / âncora** | comentário `TODO [RT-ELF-HDR-01]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [RT-ELF-HDR-01]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |
Exija no mínimo 16 bytes. Confira `data[:4] == b"\x7fELF"`, `data[4] == 2` (ELF64) e `data[5] == 1` (little-endian). Em erro, levante `ValueError`.

## `parse_elf64` - RT-ELF-ENTRY-02

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/elf_entry.py` |
| **Função / âncora** | comentário `TODO [RT-ELF-ENTRY-02]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [RT-ELF-ENTRY-02]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |
Exija no mínimo 64 bytes, chame `parse_ident(data)` e extraia:
```python
e_type, e_machine, e_version, e_entry = struct.unpack_from("<HHIQ", data, 16)
```
Retorne um dict com esses campos.

Teste:
```bash
python3 starter/test_elf_entry.py
```

Debug: use `data[:16].hex()` e `hex(e_entry)`. Não passe a fixture para `subprocess` nem tente executá-la.

## Mapa de consistência auditada
- `RT-ELF-HDR-01` - starter -> resolução -> teste -> solution.
- `RT-ELF-ENTRY-02` - starter -> resolução -> teste -> solution.
## Relatório de resolução

- **TODOs concluídos:** (liste os IDs implementados)
- **Comandos de teste:**
  ```bash
  # cole aqui o comando exato usado
  ```
- **Saída esperada:** PASS nos testes do módulo
- **Invariantes verificadas:** (liste)
- **Edge cases testados:** (liste)
- **Benchmark:** hipótese + resultado ou declaração honesta de skip
- **Toolchain não executada:** (se aplicável)

### 4. Por que funciona

O stub no âncora TODO é substituído pelo comportamento testado.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.

Checkpoint: rode o teste do módulo após cada TODO.
