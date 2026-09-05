# Teoria passo a passo — hash chain, Merkle e proof-of-work toy

## 1. O que estamos construindo

Uma blockchain local educacional: blocos encadeados por hash, árvore Merkle sobre transações, serialização determinística e proof-of-work com prefixo de zeros hex.

Não protegemos dinheiro real. Separamos conceitos que em produção coexistem com rede, consenso e economia.

## 2. Componentes internos

```text
Block
  index, previous_hash, transactions[], timestamp, nonce
       |
       v
  digest() = SHA256(json_canônico)
       |
       v
  mine(): incrementa nonce até digest começar com N zeros

ToyChain
  blocks[] + difficulty
  append() -> novo bloco ligado ao digest anterior
  valid() -> PoW + links
```

## 3. Merkle root — exemplo numérico simplificado

Transações `["a", "b"]`:

```text
h0 = SHA256("a")
h1 = SHA256("b")
root = SHA256( hex(h0) + hex(h1) )   # concatenação textual do lab
```

Ordem importa: `["b","a"]` produz root diferente.

Com três folhas ímpares, duplicamos a última antes do próximo nível.

## 4. Serialização canônica (CHAIN-DIGEST-01)

```python
json.dumps(payload, sort_keys=True, separators=(",", ":"))
```

Sem `sort_keys`, o mesmo dicionário pode gerar bytes diferentes. Sem separadores fixos, espaços alteram o hash.

## 5. Proof-of-work toy (CHAIN-MINE-01)

`difficulty=1` exige um dígito hex `0` no início do digest (não é difficulty do Bitcoin).

```text
nonce=0 -> digest abcdef...
nonce=1 -> digest 0a3f2c...  OK
```

Complexidade esperada: O(16^d) tentativas para d zeros hex (média).

## 6. Validação (CHAIN-VALID-01)

Para cada bloco `i`:

1. `digest().startswith("0"*difficulty)`
2. se `i==0`: `previous_hash == "0"*64`
3. senão: `previous_hash == blocks[i-1].digest()`

Alterar uma transação muda Merkle → digest → invalida PoW e links.

## 7. Diagrama de cadeia

```text
Genesis                Block 1                 Block 2
[tx: genesis]   -->    [alice->bob:3]   -->   [...]
prev: 000..0          prev: H(genesis)        prev: H(block1)
nonce mined           nonce mined             nonce mined
```

## 8. Invariantes

- Genesis deve ser minerado com a mesma `difficulty` da cadeia.
- `append` sempre chama `mine` antes de empilhar.
- `merkle_root` de lista vazia é hash de string vazia (definido no lab).
- `valid()` não confunde link quebrado com PoW inválido — ambos falham.

## 9. Bugs comuns

- Esquecer `genesis.mine(difficulty)`.
- `append` sem minerar o novo bloco.
- Merkle sem duplicar último elemento em nível ímpar.
- JSON sem `sort_keys=True`.
- Comparar `previous_hash` com bloco errado após tampering.

## 10. Comparação com produção

| Toy chain | Bitcoin / Ethereum |
|-----------|-------------------|
| SHA256 local | SHA256d / Keccak |
| d zeros hex | target de bits |
| sem rede | gossip + consensus |
| sem UTXO/account model | estado global |

O encadeamento por hash e a sensibilidade a dados são reais; o resto é simplificado.

## 11. Passo a passo guiado

1. Implemente `merkle_root`.
2. Implemente `digest` canônico.
3. Implemente `mine` e integre no genesis e `append`.
4. Implemente `valid` e teste tampering.
5. Rode `python starter/tests/test_chain.py`.

## 12. Como saber se está correto

Testes passam; bloco com `difficulty=1` tem digest começando com `0`; alterar transação torna `valid()` falso.
## 8. Estrutura do bloco (diagrama)

```text
+----------+----------+----------+----------+
| index    | prev_hash| timestamp| nonce    |
+----------+----------+----------+----------+
| merkle_root (hex)  | transactions[]        |
+----------+----------+----------+----------+
| digest = SHA256(canonical_json)             |
+---------------------------------------------+
```

## 9. Proof-of-work didático

Prefixo de `n` zeros hex significa `digest.startswith('0'*n)`. Complexidade ~16^n tentativas esperadas para hash uniforme.

## 10. Merkle pairwise

```text
txA txB txC txD
  \ /    \ /
  H1      H2
    \    /
      root
```

Lista ímpar duplica o último elemento — documente essa escolha.

## 11. Invariantes de validação

- `digest` recalculado bate com armazenado.
- `prev_hash` do bloco N = `digest` do bloco N-1.
- Índices monotônicos.

## 12. Bugs comuns

- JSON não determinístico (ordem de chaves).
- Esquecer nonce na serialização.
- Merkle com ordem de transações trocada.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
