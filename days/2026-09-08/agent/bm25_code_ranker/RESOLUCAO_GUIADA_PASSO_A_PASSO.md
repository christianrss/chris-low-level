# Resolução guiada passo a passo — BM25 code ranker

Edite `starter/bm25.py`.

### TODO D6-BM25-TOKENIZE
Use regex `[A-Za-z_][A-Za-z0-9_]*` e lowercase.

### TODO D6-BM25-INDEX
Para cada doc salve tokens, Counter e length. DF conta documentos contendo termo, não frequência total.
Calcule avgdl.

### TODO D6-BM25-SCORE
Para cada termo da query presente no doc, calcule idf e fórmula BM25. Retorne documentos ordenados por `(-score,path)`.

### TODO D6-BM25-EVAL
Implemente reciprocal rank: 1/rank do primeiro doc relevante ou 0. O teste tem queries com ground truth.
Execute `python starter/test_bm25.py` e depois benchmark sintético.
