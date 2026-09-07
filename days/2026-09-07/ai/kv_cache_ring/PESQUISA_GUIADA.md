# Pesquisa guiada — KV cache

## Fontes primárias / técnicas

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — origem de K/V na atenção.
- Documentação vLLM / papers de **paged attention** — como produção pagina blocos de KV.
- FlashAttention docs — reordenação IO-aware (contraste com ring educacional).

## Perguntas antes de implementar

1. Em autoregressão, o que exatamente é reutilizado entre tokens — Q, K, V ou combinações?
2. Por que um tag lógico por slot evita **stale read** após wrap do ring?
3. Como **paged attention** mapeia posição lógica → bloco físico sem perder detecção de eviction?
4. Qual diferença entre janela deslizante (sliding window) e ring com capacity fixo?

## Investigação prática

1. Desenhe capacity=8 com 12 appends; marque quais posições `window(0,12)` deve rejeitar.
2. Leia uma API de cache em Hugging Face (`past_key_values`) e liste três campos que este lab **não** modela.
3. Estime memória: `batch × layers × heads × seq × head_dim × 2 (K+V)` para um modelo pequeno.

## Depois da implementação

Explique três simplificações do laboratório, o invariante que protege correção (tag lógico) e qual métrica você mediria antes de otimizar (ex.: bytes de KV por token, taxa de cache hit na janela).
