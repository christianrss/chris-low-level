# Resolução guiada — Pipeline CLVM: disasm + peephole + verify

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-CLVM-DIS-01` | `starter/clvm_pipeline_integration.py` | `disasm` |
| `CAP-CLVM-PEEP-02` | `starter/clvm_pipeline_integration.py` | `peephole` |
| `CAP-CLVM-VFY-03` | `starter/clvm_pipeline_integration.py` | `verify_stack` |

> Raiz: `days/2026-09-10/systems/clvm_pipeline_integration/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/systems/clvm_pipeline_integration/starter
python -m pytest -q 2>$null; if (-not $?) { python test_clvm_pipeline_integration.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-CLVM-DIS-01

### Onde colocar (CAP-CLVM-DIS-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_pipeline_integration.py` |
| Função / âncora | `disasm` — comentário `TODO [CAP-CLVM-DIS-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-CLVM-DIS-01`, o Caso correspondente falha: listing PUSH 1/2 ADD HALT.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-CLVM-DIS-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def disasm(code: bytes) -> list[str]:
    # PEDAGOGY-SOLUTION: CAP-CLVM-DIS-01
    out: list[str] = []
    i = 0
    while i < len(code):
        op = code[i]
        if op == PUSH:
            out.append(f"PUSH {code[i+1]}")
            i += 2
        elif op == ADD:
            out.append("ADD")
            i += 1
        elif op == HALT:
            out.append("HALT")
            i += 1
        else:
            return []
    return out
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-CLVM-DIS-01`: ele implementa exatamente o contrato do
teste (listing PUSH 1/2 ADD HALT.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-CLVM-DIS-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-CLVM-PEEP-02

### Onde colocar (CAP-CLVM-PEEP-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_pipeline_integration.py` |
| Função / âncora | `peephole` — comentário `TODO [CAP-CLVM-PEEP-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-CLVM-PEEP-02`, o Caso correspondente falha: folded == 01 05 08.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-CLVM-PEEP-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def peephole(code: bytes) -> bytes:
    # PEDAGOGY-SOLUTION: CAP-CLVM-PEEP-02
    out = bytearray()
    i = 0
    while i < len(code):
        if i + 3 <= len(code) and code[i] == PUSH and code[i+1] == 0 and code[i+2] == ADD:
            i += 3
            continue
        out.append(code[i])
        i += 1
    return bytes(out)
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-CLVM-PEEP-02`: ele implementa exatamente o contrato do
teste (folded == 01 05 08.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-CLVM-PEEP-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-CLVM-VFY-03

### Onde colocar (CAP-CLVM-VFY-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/clvm_pipeline_integration.py` |
| Função / âncora | `verify_stack` — comentário `TODO [CAP-CLVM-VFY-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-CLVM-VFY-03`, o Caso correspondente falha: verify_stack True.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-CLVM-VFY-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def verify_stack(code: bytes) -> bool:
    # PEDAGOGY-SOLUTION: CAP-CLVM-VFY-03
    depth = 0
    i = 0
    while i < len(code):
        op = code[i]
        if op == PUSH:
            if i + 1 >= len(code):
                return False
            depth += 1
            i += 2
        elif op == ADD:
            if depth < 2:
                return False
            depth -= 1
            i += 1
        elif op == HALT:
            return depth >= 0
        else:
            return False
    return False
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-CLVM-VFY-03`: ele implementa exatamente o contrato do
teste (verify_stack True.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-CLVM-VFY-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e4 disasm+peep`):
