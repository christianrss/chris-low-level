# Resolução guiada — tool_barrier_join

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `AGENT-JOIN-01` | `starter/tool_barrier_join.py` | `__init__` |
| `AGENT-JOIN-02` | `starter/tool_barrier_join.py` | `arrive` |
| `AGENT-JOIN-03` | `starter/tool_barrier_join.py` | `snapshot` |

## Baseline

```powershell
// contexto: substitua o corpo sob o TODO
python days/2026-09-11/agent/tool_barrier_join/starter/test_tool_barrier_join.py
// fim do corpo; preserve a assinatura
```

**Esperado:** FAIL.

## AGENT-JOIN-01

### Onde colocar (AGENT-JOIN-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tool_barrier_join.py` |
| Função | `__init__` |
| Substituir | o corpo sob o comentário `TODO [AGENT-JOIN-01]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Guardar expected/results/done.

### Algoritmo / trace

ValueError se expected<=0.

### Escreva o código

```python
    if expected <= 0:
        raise ValueError("expected")
    self.expected = expected
    self.results = {}
    self.done = 0
```

### Por que funciona?

Estado inicial da barreira.

### Verifique

expected==2, done==0.

### Código completo alinhado ao solutions/ (AGENT-JOIN-01)

```python
PEDAGOGY-SOLUTION: AGENT-JOIN-01
        if expected <= 0:
            raise ValueError("expected")
        self.expected = expected
        self.results: dict[str, dict] = {}
        self.done = 0

    def arrive(self, tool_id: str, payload: dict) -> bool:
        # 
```

## AGENT-JOIN-02

### Onde colocar (AGENT-JOIN-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tool_barrier_join.py` |
| Função | `arrive` |
| Substituir | o corpo sob o comentário `TODO [AGENT-JOIN-02]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Só True quando done atinge expected.

### Algoritmo / trace

registre payload; incremente se novo id.

### Escreva o código

```python
    if tool_id in self.results:
        return self.done >= self.expected
    self.results[tool_id] = payload
    self.done += 1
    return self.done >= self.expected
```

### Por que funciona?

Join lógico sem threads neste lab.

### Verifique

False depois True.

### Código completo alinhado ao solutions/ (AGENT-JOIN-02)

```python
PEDAGOGY-SOLUTION: AGENT-JOIN-02
        if tool_id in self.results:
            return self.done >= self.expected
        self.results[tool_id] = payload
        self.done += 1
        return self.done >= self.expected

    def snapshot(self) -> dict:
        # 
```

## AGENT-JOIN-03

### Onde colocar (AGENT-JOIN-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/tool_barrier_join.py` |
| Função | `snapshot` |
| Substituir | o corpo sob o comentário `TODO [AGENT-JOIN-03]`. Mantenha a assinatura. |
| Não mexer | assinatura e outros TODOs neste passo |

### O problema

Expor done/expected/results.

### Algoritmo / trace

dict cópia rasa.

### Escreva o código

```python
    return {
        "done": self.done,
        "expected": self.expected,
        "results": dict(self.results),
    }
```

### Por que funciona?

Observabilidade do agente.

### Verifique

done==1 mid-flight.

### Código completo alinhado ao solutions/ (AGENT-JOIN-03)

```python
PEDAGOGY-SOLUTION: AGENT-JOIN-03
        return {"done": self.done, "expected": self.expected, "results": dict(self.results)}
```

## Debug

| Sintoma | Correção |
|---------|----------|
| True cedo | confira expected |

## Relatório de resolução

- TODOs: [ ]
