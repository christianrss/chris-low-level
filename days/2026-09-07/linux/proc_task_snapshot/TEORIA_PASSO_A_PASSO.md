# Teoria passo a passo — /proc task snapshot (D5-PROC)

## 1. O que estamos construindo

Um mini **chris-top** em Python puro: parser de `/proc/<pid>/stat`, scan tolerante a races e cálculo de **delta de CPU ticks** entre dois snapshots. Sem `psutil`, sem ctypes — só `pathlib`, `dataclass` e leitura de texto.

TODOs do lab: `D5-PROC-PARSE` (linha `stat`), `D5-PROC-SCAN` (enumeração), `D5-PROC-DELTA` (identidade + delta).

## 2. Por que `/proc` antes de bibliotecas de alto nível

`/proc` é um **pseudo-filesystem** montado pelo kernel Linux. Cada processo expõe arquivos textuais (`stat`, `status`, `cmdline`) que mudam enquanto você lê. Ferramentas como `htop` e `top` não “chamam uma API estável”: elas parseiam texto, toleram processos que somem e reconciliam identidade de PID ao longo do tempo. Este milestone ensina o mecanismo que essas ferramentas escondem.

## 3. Formato de `/proc/<pid>/stat`

### O quê

Uma linha com dezenas de campos separados por espaço. O campo `comm` (nome do executável) fica **entre parênteses** e pode conter espaços, parênteses internos e caracteres especiais — por isso `split()` na linha inteira é incorreto.

Layout canônico (simplificado):

```text
pid (comm) state ppid pgrp session tty_nr tpgid flags minflt cminflt majflt cmajflt
utime stime cutime cstime priority nice num_threads itrealvalue starttime ...
```

### Como

1. Leia a linha como string única.
2. `lp = line.find("(")` — primeiro `(` após o PID.
3. `rp = line.rfind(")")` — último `)` antes dos campos numéricos.
4. `pid = int(line[:lp].strip())`, `comm = line[lp+1:rp]`.
5. Campos após `) ` viram lista `f = line[rp+2:].split()`.
6. Mapeie índices relativos: `f[0]`=state, `f[1]`=ppid, `f[11]`=utime, `f[12]`=stime, `f[17]`=num_threads, `f[19]`=starttime.

### Por quê

O kernel documenta índices **absolutos** na linha original (campo 14 = utime). Depois de extrair `pid` e `comm`, os índices deslocam: utime/stime passam de 14/15 para 11/12 no vetor `f`. Confundir os dois esquemas é o bug #1 em parsers caseiros de `stat`.

### Trace manual — comm com espaço

```text
line = '42 (worker pool) S 1 42 42 0 -1 4194560 120 0 0 0 10 5 0 0 20 0 2 0 100 0 ...'
lp=3, rp=16 → comm='worker pool'
f[0]='S', f[1]='1', f[11]='10', f[12]='5', f[19]='100'
Task(pid=42, comm='worker pool', state='S', ppid=1, utime=10, stime=5, ..., starttime=100)
```

### Invariantes (`D5-PROC-PARSE`)

- `comm` preserva espaços internos.
- Linha malformada (`(` ausente, `)` antes de `(`) → `ValueError`.
- Menos de 20 campos em `f` → `ValueError("short stat")`.

### Bugs comuns

| Sintoma | Causa | Correção |
|---------|-------|----------|
| `comm == "worker"` | `split()` na linha inteira | use `find`/`rfind` nos parênteses |
| `utime` sempre 0 | índice absoluto 14 em vez de 11 | recalcule após extrair comm |
| `ValueError` em fixture válido | `rp+1` em vez de `rp+2` | após `)` há espaço antes do state |

## 4. Scan de processos (`D5-PROC-SCAN`)

### O quê

`scan(root="/proc") → dict[int, Task]` enumera diretórios cujo nome é só dígitos, lê `<pid>/stat` e agrega `Task` por PID.

### Como

```text
out ← {}
para cada entrada p em Path(root).iterdir():
  se p.name não é all-digit: continue
  try:
    t ← parse_stat((p/"stat").read_text())
    out[t.pid] ← t
  except FileNotFoundError, PermissionError, ProcessLookupError:
    pass   # processo sumiu ou sem permissão
return out
```

### Por quê

Entre `iterdir()` e `read_text()`, o processo pode terminar — isso é **condição normal**, não falha do seu programa. Ignorar por PID evita abortar o snapshot inteiro por uma race. Em produção, `htop` faz o mesmo: conta ignorados e continua.

### Diagrama — race no scan

```text
iterdir() ──► vê /proc/9999/
                    │
                    ▼ (processo exit)
read_text() ──► FileNotFoundError ──► skip, seguir scan
```

### Invariantes

- Chave do dict = `Task.pid` (não o nome do diretório — devem coincidir).
- Fixture em diretório temporário deve funcionar sem `/proc` real.
- Erro de **parse** em fixture controlado não deve ser silenciado (diferente de race).

### Bugs comuns

- Propagar `FileNotFoundError` e derrubar o scan inteiro.
- Usar `p.name` como chave sem validar contra `t.pid`.
- Assumir que `root` sempre é `/proc` nos testes — use `TemporaryDirectory`.

## 5. Delta de CPU e identidade (`D5-PROC-DELTA`)

### O quê

`cpu_ticks_delta(a, b)` retorna `(b.utime + b.stime) - (a.utime + a.stime)` em **ticks de relógio do scheduler** (USER_HZ, tipicamente 100 Hz no Linux), somando tempo em user e kernel space do processo.

### Como

```text
se a.pid ≠ b.pid ou a.starttime ≠ b.starttime:
  raise ValueError("process identity changed")
return (b.utime + b.stime) - (a.utime + a.stime)
```

### Por quê

PIDs são **reutilizados**. PID 42 às 10:00 e PID 42 às 10:05 podem ser processos diferentes. O campo `starttime` (jiffies desde boot) funciona como “serial” do processo: se mudou, o delta de ticks seria um número absurdo (milhões) e distorceria `%CPU`. `top` e `systemd-cgtop` usam heurísticas semelhantes.

### Trace manual — delta válido

```text
a = Task(..., utime=10, stime=5, starttime=100)
b = Task(..., utime=14, stime=7, starttime=100)   # mesmo processo
delta = (14+7) - (10+5) = 6 ticks
```

### Trace manual — PID reuse rejeitado

```text
a.starttime=100, b.starttime=200  → ValueError
(mesmo pid=42, processos diferentes)
```

### Invariantes

- Delta ≥ 0 em processo vivo normal (relógios monotônicos por thread group).
- `starttime` congelado na vida do processo (campo 22 no `stat` original).

### Bugs comuns

- Comparar só `pid` e aceitar delta gigante após reuse.
- Usar só `utime` e ignorar `stime` (threads em syscall aparecem “paradas”).
- Subtrair na ordem errada (`a - b`).

## 6. Fluxo mental do snapshot

```text
/proc ──► scan() ──► {pid: Task@t0}
   │                      │
   │ sleep Δt             │
   ▼                      ▼
/proc ──► scan() ──► {pid: Task@t1}
                           │
                           ▼
              cpu_ticks_delta(t0[pid], t1[pid])  → uso relativo de CPU
```

## 7. Tabela de campos usados neste milestone

| Campo `stat` | Índice em `f` | Uso no lab |
|--------------|---------------|------------|
| state | `f[0]` | `Task.state` (R/S/D/Z/T…) |
| ppid | `f[1]` | processo pai |
| utime | `f[11]` | ticks user |
| stime | `f[12]` | ticks kernel |
| num_threads | `f[17]` | threads no grupo |
| starttime | `f[19]` | identidade vs PID reuse |

## 8. Complexidade

| Função | Tempo | Espaço |
|--------|-------|--------|
| `parse_stat` | O(campos) | O(1) |
| `scan` | O(P × tamanho stat) | O(P) processos |
| `cpu_ticks_delta` | O(1) | O(1) |

## 9. Comparação com produção

| Este lab | `htop` / `ps` / eBPF |
|----------|----------------------|
| Um arquivo `stat` | múltiplas fontes (`status`, cgroup, perf) |
| `starttime` para identidade | também boot_id, start_time_ns em `/proc/pid` |
| Scan single-thread | buffers e amostragem estatística |
| Python texto | parsers C + cache |

O transferível é **parse defensivo + identidade + delta**, não reimplementar `htop`.

## 10. Passo a passo guiado (ordem dos TODOs)

1. `D5-PROC-PARSE` — `parse_stat` em `starter/proc_snapshot.py`.
2. `D5-PROC-SCAN` — `scan` com tolerância a races.
3. `D5-PROC-DELTA` — `cpu_ticks_delta` com guard de identidade.
4. `python starter/test_proc_snapshot.py` → `chris-proc-snapshot tests passed`.

## 11. Como saber se está correto

- Caso parse: `comm == "worker pool"` com utime=10.
- Caso scan: fixture temporário retorna PID 42.
- Caso delta: segundo snapshot utime=14, stime=7 → delta=6.
- Caso reuse: `starttime` diferente → `ValueError`.

## 12. Invariantes globais do módulo

- `Task` é `frozen=True` — snapshots imutáveis.
- APIs exatamente como em `starter/proc_snapshot.py`.
- Testes usam fixture; não dependem de `/proc` do host.

## 13. Por quê este módulo existe

Observabilidade de sistema começa em **texto do kernel**, não em dashboards. Cada `TODO [ID]` protege uma propriedade que ferramentas de produção assumem silenciosamente: comm com espaços, races no scan e PID reuse no delta.
