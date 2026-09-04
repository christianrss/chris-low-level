# Teoria passo a passo - hash chain e Merkle tree

Blockchain combina varias ideias que devem ser separadas: serializacao deterministica, hash, encadeamento por `previous_hash`, agregacao Merkle, regras de validacao e algum protocolo de consenso. O Day 01 implementa apenas uma cadeia local com proof-of-work toy.

A funcao SHA-256 vem da biblioteca padrao. Nao implementamos criptografia caseira para proteger dinheiro. A dificuldade e um prefixo de zeros hexadecimais e existe apenas para visualizar busca por nonce.
