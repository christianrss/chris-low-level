# Teoria passo a passo — BM25 code ranker

BM25 é ranking lexical que pondera term frequency, raridade do termo e comprimento do documento. Para coding agent,
ele pode reranquear candidatos recuperados por grep/trigram antes de gastar tokens lendo arquivos.

Implementaremos tokenizer de identificadores simples, document frequency, IDF e score:
`idf=log(1+(N-df+0.5)/(df+0.5))`.
Com k1=1.2, b=0.75:
`score += idf * tf*(k1+1)/(tf+k1*(1-b+b*dl/avgdl))`.

Isso não entende semântica nem call graph. É uma camada lexical observável; o eval precisa medir MRR/recall@k em
ground truth pequeno, não apenas mostrar exemplos bonitos.
