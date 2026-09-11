# Resolução guiada — Agent loop capstone

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-AGENT-01` | `starter/capstone_agent_loop.py` | `step` |
| `CAP-AGENT-02` | `starter/capstone_agent_loop.py` | `verify` |
| `CAP-AGENT-03` | `starter/capstone_agent_loop.py` | `replay` |

> Raiz: `days/2026-09-10/agent/capstone_agent_loop/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/agent/capstone_agent_loop/starter
python -m pytest -q 2>$null; if (-not $?) { python test_capstone_agent_loop.py 2>$null; if (-not $?) { Get-ChildItem test*.py | ForEach-Object { python $_.FullName } } }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-AGENT-01

### Onde colocar (CAP-AGENT-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_agent_loop.py` |
| Função / âncora | `step` — comentário `TODO [CAP-AGENT-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-AGENT-01`, o Caso correspondente falha: estado DONE.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-AGENT-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def step(self, event: str) -> str:
        # PEDAGOGY-SOLUTION: CAP-AGENT-01
        key = (self.state, event)
        if key not in TRANSITIONS:
            return self.state
        self.state = TRANSITIONS[key]
        self.trace.append(self.state)
        return self.state
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-AGENT-01`: ele implementa exatamente o contrato do
teste (estado DONE.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-AGENT-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-AGENT-02

### Onde colocar (CAP-AGENT-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_agent_loop.py` |
| Função / âncora | `verify` — comentário `TODO [CAP-AGENT-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-AGENT-02`, o Caso correspondente falha: trace preenchido.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-AGENT-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def verify(self, passed: bool) -> str:
        # PEDAGOGY-SOLUTION: CAP-AGENT-02
        self.state = "VERIFY"
        return self.step("pass" if passed else "fail")
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-AGENT-02`: ele implementa exatamente o contrato do
teste (trace preenchido.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-AGENT-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-AGENT-03

### Onde colocar (CAP-AGENT-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_agent_loop.py` |
| Função / âncora | `replay` — comentário `TODO [CAP-AGENT-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-AGENT-03`, o Caso correspondente falha: replay True.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-AGENT-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```python
def replay(trace: list[str]) -> bool:
    # PEDAGOGY-SOLUTION: CAP-AGENT-03
    return len(trace) >= 1 and trace[-1] == "DONE"
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-AGENT-03`: ele implementa exatamente o contrato do
teste (replay True.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-AGENT-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e4 loops`):
