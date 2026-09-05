# Exercícios — toy chain

## Fácil

- **CHAIN-MERKLE-01:** implemente `merkle_root` com duplicação do último nó em níveis ímpares.
- **CHAIN-DIGEST-01:** implemente `Block.digest()` com `json.dumps(sort_keys=True, separators=(",", ":"))`.

## Médio

- **CHAIN-MINE-01:** implemente `mine()` com loop de nonce até prefixo de zeros.
- **CHAIN-GENESIS-01:** mine o bloco genesis em `ToyChain.__init__` com a mesma `difficulty`.

## Difícil

- **CHAIN-VALID-01:** implemente `valid()` checando PoW e `previous_hash` encadeado.
- **CHAIN-TAMPER-01:** após testes verdes, altere uma transação e documente qual verificação falha primeiro.

## Desafio

- **CHAIN-ORDER-01:** prove com dois hashes que `merkle_root(["a","b"]) != merkle_root(["b","a"])`.
- **CHAIN-SCALE-01:** estime quantas tentativas médias para `difficulty=3` e compare com benchmark.
