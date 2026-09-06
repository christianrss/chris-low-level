# Exercícios — Tensor entropy lab

## Fácil

- **AI-ENT-01 (vazio + constante):** Em `starter/entropy_lab.py`, faça `shannon_entropy` retornar `0.0` para `b""` e para `bytes([7]*100)`.  
  **Aceite:** REPL imprime `0.0` nos dois casos.

- **AI-ENT-01 (uniforme):** Complete a soma `-p log2 p` com `Counter`.  
  **Aceite:** `shannon_entropy(bytes([0,1,2,3]*25))` ≈ `2.0` (`abs(diff)<1e-6`).

## Médio

- **AI-ENT-02 (encode):** Implemente `tensor_rle_encode` com append do último run.  
  **Aceite:** `[7]*1000+[3]*500` → `[(7,1000),(3,500)]`.

- **AI-ENT-02 (ratio):** Implemente `compression_ratio_rle` usando os helpers de tamanho.  
  **Aceite:** mesmo tensor → ratio `< 0.01`.

## Difícil

- **AI-ENT-03:** Implemente `compression_ratio_gzip` e passe `test_gzip_vs_rle`.  
  **Aceite:** `python starter/test_entropy_lab.py` imprime `OK tensor entropy lab`.

## Desafio

- **AI-ENT-CH-01:** Para N∈{1,2,4,8,16,32,64,128,256}, construa `bytes(range(N))* (256//N)` (ou repetição que complete 256 bytes com N símbolos equiprováveis) e verifique `|H - log2(N)| < 1e-6`. Documente a tabela N→H.  
  **Aceite:** asserts passam para todos os N da lista; anote H observado para N=4 e N=256.
