# RESOLUÇÃO GUIADA — Linux /proc task snapshot

## Mapa exato starter → resolução

| TODO ID | Starter | Função |
|---------|---------|--------|
| `D5-PROC-PARSE` | `starter/proc_snapshot.py` | `parse_stat` |
| `D5-PROC-SCAN` | `starter/proc_snapshot.py` | `scan` |
| `D5-PROC-DELTA` | `starter/proc_snapshot.py` | `cpu_ticks_delta` |

Cada ID existe como `TODO [ID]` no starter, `PEDAGOGY-SOLUTION: ID` no gabarito e `PEDAGOGY-TEST: ID` em `starter/test_proc_snapshot.py`.

> Trabalhe em `days/2026-09-07/linux/proc_task_snapshot/starter/`. O gabarito fica em `solutions/` — use só depois da tentativa.

## Baseline

Antes de editar, confirme que o starter falha por causa dos TODOs:

```powershell
cd days/2026-09-07/linux/proc_task_snapshot/starter
python test_proc_snapshot.py
```

**Esperado:** `NotImplementedError` em `parse_stat` (ou falha no primeiro assert). Não prossiga até ver FAIL claro — ambiente OK.

---

## D5-PROC-PARSE — parser robusto de `stat`

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/proc_snapshot.py` |
| **Função / âncora** | comentário `TODO [D5-PROC-PARSE]` em `parse_stat` |
| **Substituir** | corpo com `raise NotImplementedError` |
| **Não mexer** | `Task`, `scan`, `cpu_ticks_delta` neste passo |

### 1. O problema

```python
def parse_stat(line):
    # TODO [D5-PROC-PARSE]: parseie /proc/<pid>/stat sem split ingênuo do comm.
    raise NotImplementedError
```

Com o raise, o teste `comm=="worker pool"` nunca executa.

### 2. Algoritmo

```text
lp ← line.find("("); rp ← line.rfind(")")
se lp<1 ou rp<lp: ValueError
pid ← int(line[:lp].strip())
comm ← line[lp+1:rp]
f ← line[rp+2:].split()
se len(f)<20: ValueError
retornar Task(pid, comm, f[0], int(f[1]), int(f[11]), int(f[12]), int(f[17]), int(f[19]))
```

### 3. Código completo

```python
def parse_stat(line):
    lp = line.find("(")
    rp = line.rfind(")")
    if lp < 1 or rp < lp:
        raise ValueError("bad stat")
    pid = int(line[:lp].strip())
    comm = line[lp + 1 : rp]
    f = line[rp + 2 :].split()
    if len(f) < 20:
        raise ValueError("short stat")
    return Task(
        pid,
        comm,
        f[0],
        int(f[1]),
        int(f[11]),
        int(f[12]),
        int(f[17]),
        int(f[19]),
    )
```

### 4. Por que funciona?

- `rfind(")")` pega o parêntese de fechamento do `comm`, não um `)` dentro do nome.
- `rp+2` salta `) ` — sem isso `f[0]` vira lixo.
- Índices 11/12/19 são relativos ao vetor **após** remover pid e comm.

### 5. Verifique

```powershell
python -c "import sys; sys.path.insert(0,'starter'); from proc_snapshot import parse_stat; from test_proc_snapshot import line; t=parse_stat(line(42,'worker pool',10,5,100)); print(t.comm, t.utime)"
```

**Esperado:** `worker pool 10`. Teste completo ainda falha em `D5-PROC-SCAN`.

---

## D5-PROC-SCAN — enumeração tolerante a races

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/proc_snapshot.py` |
| **Função / âncora** | comentário `TODO [D5-PROC-SCAN]` em `scan` |
| **Substituir** | `return {}` stub |
| **Não mexer** | `parse_stat` já implementado; não altere `cpu_ticks_delta` |

### 1. O problema

`scan` retorna dict vazio — fixture com PID 42 não aparece no mapa.

### 2. Algoritmo

```text
out ← {}
para p em Path(root).iterdir():
  se não p.name.isdigit(): continue
  try: parse_stat de (p/"stat"); out[pid]=task
  except FileNotFoundError, PermissionError, ProcessLookupError: pass
return out
```

### 3. Código completo

```python
def scan(root="/proc"):
    out = {}
    for p in Path(root).iterdir():
        if not p.name.isdigit():
            continue
        try:
            t = parse_stat((p / "stat").read_text())
            out[t.pid] = t
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            pass
    return out
```

### 4. Por que funciona?

- `isdigit()` filtra `.`, `self`, `thread-self` em `/proc` real.
- Exceções por processo isolam races sem abortar o snapshot.
- `out[t.pid]` usa PID do parse, não só nome do diretório.

### 5. Verifique

Rode `python test_proc_snapshot.py`. **Esperado:** parse e scan passam; delta ainda falha.

---

## D5-PROC-DELTA — identidade e ticks de CPU

### Onde colocar

| | |
|--|--|
| **Arquivo** | `starter/proc_snapshot.py` |
| **Função / âncora** | comentário `TODO [D5-PROC-DELTA]` em `cpu_ticks_delta` |
| **Substituir** | `return 0` stub |
| **Não mexer** | `parse_stat` e `scan` |

### 1. O problema

Stub retorna 0 — teste espera delta `6` entre snapshots com utime/stime maiores.

### 2. Algoritmo

```text
se a.pid≠b.pid ou a.starttime≠b.starttime: ValueError
return (b.utime+b.stime)-(a.utime+a.stime)
```

### 3. Código completo

```python
def cpu_ticks_delta(a, b):
    if a.pid != b.pid or a.starttime != b.starttime:
        raise ValueError("process identity changed")
    return (b.utime + b.stime) - (a.utime + a.stime)
```

### 4. Por que funciona?

- `starttime` distingue PID reuse — sem ele, delta mistura processos.
- Soma `utime+stime` cobre tempo user e kernel do grupo de threads.

### 5. Verifique

```powershell
python test_proc_snapshot.py
```

**Esperado:** `chris-proc-snapshot tests passed`.

---

## Debug / depuração

| Erro | Causa provável | Ação |
|------|----------------|------|
| `comm` truncado | `split()` na linha | volte ao parser com parênteses |
| `short stat` no fixture | helper `line()` incompleto | confira 20+ campos após `)` |
| scan vazio | path errado ou não `isdigit` | imprima `list(Path(td).iterdir())` |
| delta 0 com stub removido | ordem `a-b` invertida | use `(b)-(a)` |
| `identity changed` inesperado | `starttime` diferente no helper | mesmo `start` nos dois `line()` |

Imprima `repr(line)`, posições `(lp, rp)` e `f[:20]` no primeiro FAIL de parse.

---

## Relatório de resolução

Preencha após todos os testes passarem:

| Campo | Sua resposta |
|-------|----------------|
| Data | |
| `D5-PROC-PARSE` — maior dificuldade | |
| Índice que você errou primeiro (se houver) | |
| Race ignorada no scan real (contagem opcional) | |
| Tempo total | |
| Comando final | `python starter/test_proc_snapshot.py` |
| Resultado | PASS / FAIL |
