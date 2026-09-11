# Resolução guiada — Pipeline unificado de input

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-INP-KBD-01` | `starter/unified_input_pipeline.py` | `parse_keyboard_chunk` |
| `CAP-INP-MUX-02` | `starter/unified_input_pipeline.py` | `mux_streams` |
| `CAP-INP-XFM-03` | `starter/unified_input_pipeline.py` | `transform_events` |

> Raiz: `days/2026-09-10/systems/unified_input_pipeline/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/systems/unified_input_pipeline/starter
python -m pytest -q 2>$null; if (-not $?) { python test_unified_input_pipeline.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-INP-KBD-01

### Onde colocar (CAP-INP-KBD-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/unified_input_pipeline.py` |
| Função / âncora | `parse_keyboard_chunk` — comentário `TODO [CAP-INP-KBD-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-INP-KBD-01`, o Caso correspondente falha: kbd == [(1,30,1)].

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-INP-KBD-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def parse_keyboard_chunk(buf: bytes) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-INP-KBD-01
    out = []
    for off in range(0, len(buf) - EVENT_SIZE + 1, EVENT_SIZE):
        t, c, v = int.from_bytes(buf[off+16:off+18], "little"), int.from_bytes(buf[off+18:off+20], "little"), int.from_bytes(buf[off+20:off+24], "little", signed=True)
        if t == 1:
            out.append((t, c, v))
    return out
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-INP-KBD-01`: ele implementa exatamente o contrato do
teste (kbd == [(1,30,1)].), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-INP-KBD-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-INP-MUX-02

### Onde colocar (CAP-INP-MUX-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/unified_input_pipeline.py` |
| Função / âncora | `mux_streams` — comentário `TODO [CAP-INP-MUX-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-INP-MUX-02`, o Caso correspondente falha: mux inclui ambos.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-INP-MUX-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def mux_streams(kbd: list[tuple[int, int, int]], mouse: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    # PEDAGOGY-SOLUTION: CAP-INP-MUX-02
    return kbd + mouse
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-INP-MUX-02`: ele implementa exatamente o contrato do
teste (mux inclui ambos.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-INP-MUX-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-INP-XFM-03

### Onde colocar (CAP-INP-XFM-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/unified_input_pipeline.py` |
| Função / âncora | `transform_events` — comentário `TODO [CAP-INP-XFM-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-INP-XFM-03`, o Caso correspondente falha: transform KEY/REL.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-INP-XFM-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def transform_events(events: list[tuple[int, int, int]]) -> list[str]:
    # PEDAGOGY-SOLUTION: CAP-INP-XFM-03
    out = []
    for t, c, v in events:
        if t == 1:
            out.append(f"KEY:{c}")
        elif t == 2:
            out.append(f"REL:{c}={v}")
    return out
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-INP-XFM-03`: ele implementa exatamente o contrato do
teste (transform KEY/REL.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-INP-XFM-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 transform`):
