# Resolução guiada — GPU timer query (simulação headless)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `GFX-GPU-TIMER-01` | `starter/gpu_timer.py` | `begin_query` |
| `GFX-GPU-LAP-02` | `starter/gpu_timer.py` | `end_query` |
| `GFX-GPU-BENCH-03` | `starter/gpu_timer.py` | `lap_times` |

> Raiz: `days/2026-09-09/graphics/gpu_timer_query/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/graphics/gpu_timer_query/starter
python -m pytest -q 2>$null; if (-not $?) { python test_gpu_timer.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## GFX-GPU-TIMER-01

### Onde colocar (GFX-GPU-TIMER-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/gpu_timer.py` |
| Função / âncora | `begin_query` — comentário `TODO [GFX-GPU-TIMER-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `GFX-GPU-TIMER-01`, o Caso correspondente falha: primeiro handle == 0.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `GFX-GPU-TIMER-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def begin_query(self, name: str) -> int:
        # PEDAGOGY-SOLUTION: GFX-GPU-TIMER-01
        h = self._next
        self._next += 1
        self._starts[h] = (name, self._clock())
        return h
```

### Por que funciona?

Por quê este corpo satisfaz `GFX-GPU-TIMER-01`: ele implementa exatamente o contrato do
teste (primeiro handle == 0.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `GFX-GPU-TIMER-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## GFX-GPU-LAP-02

### Onde colocar (GFX-GPU-LAP-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/gpu_timer.py` |
| Função / âncora | `end_query` — comentário `TODO [GFX-GPU-LAP-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `GFX-GPU-LAP-02`, o Caso correspondente falha: ms >= 0.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `GFX-GPU-LAP-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def end_query(self, handle: int) -> float:
        # PEDAGOGY-SOLUTION: GFX-GPU-LAP-02
        name, t0 = self._starts.pop(handle)
        ms = (self._clock() - t0) * 1000.0
        self._laps[name] = ms
        return ms
```

### Por que funciona?

Por quê este corpo satisfaz `GFX-GPU-LAP-02`: ele implementa exatamente o contrato do
teste (ms >= 0.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `GFX-GPU-LAP-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## GFX-GPU-BENCH-03

### Onde colocar (GFX-GPU-BENCH-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/gpu_timer.py` |
| Função / âncora | `lap_times` — comentário `TODO [GFX-GPU-BENCH-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `GFX-GPU-BENCH-03`, o Caso correspondente falha: "draw" in lap_times.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `GFX-GPU-BENCH-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def lap_times(self) -> dict[str, float]:
        # PEDAGOGY-SOLUTION: GFX-GPU-BENCH-03
        return dict(self._laps)
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `GFX-GPU-BENCH-03`: ele implementa exatamente o contrato do
teste ("draw" in lap_times.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `GFX-GPU-BENCH-03`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.


## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| NotImplemented / stub | corpo não substituído | cole o bloco do TODO |
| número/string diferente | trace errado no papel | refaça a seção 4 da TEORIA |
| caso seguinte quebra | mudou assinatura ou estado global | restaure o que “Não mexer” pede |
| listener/null (.NET) | sem ActivityListener | veja TESTES_GUIADOS |

## Checkpoint intermediário de integração

Depois do primeiro TODO que compila:

1. Rode o teste do módulo a partir de `starter/` (ou o comando do Baseline).
2. Confirme que o Caso 1 ainda falha **só** nos TODOs restantes (não por link quebrado).
3. Anote a mensagem de assert: ela aponta o próximo ID.

## Passo a passo de edição (operacional)

Para cada TODO restante, repita:

1. Abra o arquivo da tabela **Onde colocar**.
2. Localize o comentário `TODO [ID]` — não busque pelo nome do módulo na pasta pai.
3. Substitua **apenas** o corpo indicado; preserve assinatura e includes.
4. Compile; se o erro for de tipo/assinatura, você editou demais.
5. Só então avance ao próximo ID.

## Tabela de regressão rápida

| Depois de | Deve passar | Ainda pode falhar |
|-----------|-------------|-------------------|
| 1º TODO | asserts só desse ID | IDs seguintes |
| 2º TODO | IDs 1–2 | IDs seguintes |
| último TODO | suite inteira | — |

## Armadilhas específicas deste starter

- Mudar o teste para “passar” invalida o lab.
- Criar um segundo `.c`/`.py` com o mesmo símbolo gera link duplicado ou import errado.
- Reset ausente entre casos deixa estado (anel, FSM, arena) contaminado.

## Relatório — campos extras

Além do template padrão, anote:

- Tempo até o primeiro Caso 1 verde:
- Quantas vezes o endianness/size foi a causa:
- Um invariante que você quase violou:

## Relatório de resolução

- TODOs concluídos:
- Comando de teste:
- Saída observada:
- Invariantes checadas:
- Edge cases:
- Benchmark (`ms do lap draw (3 corridas)`):
