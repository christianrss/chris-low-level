# Resolucao guiada

1. Crie `sha256(bytes)` e confirme que a mesma entrada sempre produz o mesmo digest.
2. Implemente Merkle tree duplicando o ultimo hash quando um nivel tiver quantidade impar.
3. Um bloco deve serializar campos em ordem canonica; por isso usamos JSON com `sort_keys=True`.
4. `mine()` incrementa nonce ate o digest atender ao prefixo.
5. `ToyChain.append` usa o digest do bloco anterior.
6. Teste tampering: altere uma transacao depois de minerar; `valid()` deve falhar.
7. Benchmark dificuldades 1,2,3 e observe a variancia. Nao interprete 20 amostras como uma lei exata.

## Etapa de código 1 - Merkle

```python
level = [sha256(x.encode()) for x in items]
while len(level) > 1:
    if len(level) % 2:
        level.append(level[-1])
    level = [
        sha256((level[i] + level[i + 1]).encode())
        for i in range(0, len(level), 2)
    ]
return level[0]
```

## Etapa de código 2 - proof-of-work toy

```python
prefix = "0" * difficulty
while True:
    digest = self.digest()
    if digest.startswith(prefix):
        return digest
    self.nonce += 1
```

## Etapa de teste - tampering

```python
chain = ToyChain(difficulty=1)
chain.append(["alice->bob:3"], 1)
assert chain.valid()
chain.blocks[1].transactions[0] = "alice->mallory:3000"
assert not chain.valid()
```

O ponto do teste não é segurança monetária; é provar que o hash do bloco e o link anterior tornam alteração detectável. A solução final está em `solutions/toy_chain.py`.

