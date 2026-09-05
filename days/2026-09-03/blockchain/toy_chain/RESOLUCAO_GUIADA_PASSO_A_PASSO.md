# Resolução guiada auditada — toy_chain

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `CHAIN-MERKLE-01` | `starter/toy_chain.py` | `merkle_root()` |
| `CHAIN-DIGEST-01` | `starter/toy_chain.py` | `Block.digest()` |
| `CHAIN-MINE-01` | `starter/toy_chain.py` | `Block.mine()` |
| `CHAIN-VALID-01` | `starter/toy_chain.py` | `ToyChain.valid()` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/blockchain/toy_chain/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Arquivo que você edita

```text
starter/toy_chain.py
```

Os quatro TODOs reais são: `merkle_root`, `Block.digest`, `Block.mine` e `ToyChain.valid`. Há ainda duas integrações obrigatórias sem TODO explícito: minerar o genesis e minerar cada bloco em `append`.

## 1. Baseline

```bash
python starter/tests/test_chain.py
```

A versão starter deve falhar porque a cadeia ainda não possui PoW/links validados corretamente.

## 2. Merkle root

No topo do arquivo, mantenha `sha256()` e substitua o TODO de `merkle_root` por:

```python
if not items:
    return sha256(b"")

level = [sha256(item.encode()) for item in items]

while len(level) > 1:
    if len(level) % 2:
        level.append(level[-1])

    level = [
        sha256((level[i] + level[i + 1]).encode())
        for i in range(0, len(level), 2)
    ]

return level[0]
```

A duplicação do último elemento evita deixar um nó sem par em nível ímpar.

## 3. Serialização canônica de `Block.digest`

Altere os imports para:

```python
from dataclasses import dataclass
import hashlib
import json
```

Dentro de `digest`, construa **sempre os mesmos campos e na mesma forma**:

```python
payload = {
    "index": self.index,
    "previous_hash": self.previous_hash,
    "transactions": self.transactions,
    "timestamp": self.timestamp,
    "nonce": self.nonce,
    "merkle_root": merkle_root(self.transactions),
}
```

Depois serialize deterministamente:

```python
encoded = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
).encode()

return sha256(encoded)
```

Por que `sort_keys=True`: dicionário semanticamente igual não pode produzir hash diferente por ordem textual de chaves.

## 4. Mining

Substitua o TODO de `mine` por:

```python
prefix = "0" * difficulty

while True:
    digest = self.digest()
    if digest.startswith(prefix):
        return digest

    self.nonce += 1
```

Para este laboratório `difficulty` é apenas quantidade de zeros hexadecimais iniciais. Não confunda com difficulty adjustment de Bitcoin.

## 5. Genesis — integração que a resolução antiga pulava

Em `ToyChain.__init__`, substitua:

```python
self.blocks = [Block(0, "0" * 64, ["genesis"], 0)]
```

por:

```python
genesis = Block(0, "0" * 64, ["genesis"], 0)
genesis.mine(difficulty)
self.blocks = [genesis]
```

Sem isso, `valid()` corretamente implementado rejeitaria o próprio genesis por não satisfazer PoW.

## 6. `append` também precisa minerar

Depois de criar `block`, antes de `append`:

```python
block.mine(self.difficulty)
```

A função completa fica conceitualmente:

```python
block = Block(
    len(self.blocks),
    self.blocks[-1].digest(),
    list(transactions),
    timestamp,
)
block.mine(self.difficulty)
self.blocks.append(block)
return block
```

## 7. Validação da cadeia

Substitua `valid()` por:

```python
prefix = "0" * self.difficulty

for i, block in enumerate(self.blocks):
    if not block.digest().startswith(prefix):
        return False

    if i == 0:
        if block.previous_hash != "0" * 64:
            return False
    elif block.previous_hash != self.blocks[i - 1].digest():
        return False

return True
```

Observe as duas propriedades separadas:

1. o bloco satisfaz PoW;
2. o `previous_hash` liga corretamente ao predecessor.

## 8. Teste de tampering

```python
chain = ToyChain(difficulty=1)
chain.append(["alice->bob:3"], 1)
assert chain.valid()

chain.blocks[1].transactions[0] = "alice->mallory:3000"
assert not chain.valid()
```

A transação muda → Merkle root muda → digest muda → PoW/link deixa de validar.

## 9. Execute

```bash
python starter/tests/test_chain.py
```

Depois rode o benchmark indicado no módulo somente quando correctness estiver verde.

## 10. Debugging

- mining não termina: reduza `difficulty` para 1 e observe `nonce`/`digest`.
- cadeia válida vira inválida logo no genesis: confirme `genesis.mine(difficulty)`.
- segundo bloco inválido imediatamente: confirme `block.mine(self.difficulty)` em `append`.
- hashes mudam sem dados mudarem: confira `sort_keys=True` e `separators=(",", ":")`.

A implementação final correspondente está em `solutions/toy_chain.py`.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `CHAIN-MERKLE-01` — `starter/toy_chain.py` → `solutions/toy_chain.py`.
- `CHAIN-DIGEST-01` — `starter/toy_chain.py` → `solutions/toy_chain.py`.
- `CHAIN-MINE-01` — `starter/toy_chain.py` → `solutions/toy_chain.py`.
- `CHAIN-VALID-01` — `starter/toy_chain.py` → `solutions/toy_chain.py`.

## Relatório de resolução

Checklist ao concluir:

- [ ] Merkle, digest canônico, mine e valid implementados.
- [ ] Genesis minerado; `append` chama `mine` antes de empilhar.
- [ ] `python starter/tests/test_chain.py` passa; tampering invalida cadeia.
- [ ] `sort_keys=True` e `separators=(",", ":")` confirmados no digest.

**Saída esperada:** `toy chain tests passed`.

**Depuração:** logue `nonce` e prefixo do digest com `difficulty=1` antes de escalar difficulty.

**Arquivos starter editados:** `starter/toy_chain.py`.
