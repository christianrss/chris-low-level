## Mapa exato starter → resolução

| TODO ID | Starter |
|---------|--------|
| `TERM-ANSI-SGR-01` | `starter/ansi.py` |
| `TERM-CURSOR-02` | `starter/ansi.py` |

# Resolução guiada passo a passo

Abra `starter/ansi.py`.

## `_apply_csi`
Para final `m`, converta parâmetros vazios para 0. Em `0`, defina `fg=7`; em `31`, `fg=1`. Isso fecha `TERM-ANSI-SGR-01`.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/ansi.py` |
| **Função / âncora** | comentário `TODO [TERM-ANSI-SGR-01]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [TERM-ANSI-SGR-01]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |

Para final `H`, parseie `row;col`, usando default 1. Grave `self.row=row-1` e `self.col=col-1`. Isso fecha `TERM-CURSOR-02`.

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/ansi.py` |
| **Função / âncora** | comentário `TODO [TERM-CURSOR-02]` neste arquivo |
| **Substituir** | o stub / corpo / case marcado por `TODO [TERM-CURSOR-02]` |
| **Não mexer** | demais arquivos do starter até este ID passar nos testes |

## `feed`
Percorra o texto. Ao encontrar o prefixo `\x1b[`, avance até final `m` ou `H`, separe `params` e chame `_apply_csi`. Caso contrário, acrescente o caractere em `screen_text`.

Teste:
```bash
python3 starter/test_ansi.py
```

Debug seguro: `print(repr(seq), params, final)`. Não use `print(seq)` porque a sequência pode mover o cursor do terminal real.

## Mapa de consistência auditada
- `TERM-ANSI-SGR-01` - starter -> resolução -> teste -> solution.
- `TERM-CURSOR-02` - starter -> resolução -> teste -> solution.
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

Checkpoint: rode o teste do módulo após cada TODO.
