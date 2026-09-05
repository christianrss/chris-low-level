# Teoria passo a passo

## 1. Por que bitmap
Um allocator de páginas precisa representar se cada página está livre ou ocupada. Um booleano por página é simples, mas um bitmap usa apenas 1 bit por página. Para página `p`, o byte é `p / 8` e o bit interno é `p % 8`.

## 2. Máscaras de bit
`1u << (p % 8)` cria uma máscara com apenas o bit da página. OR marca o bit; AND com complemento limpa. O método `is_used` faz AND e compara com zero.

## 3. First-fit
`allocate()` percorre páginas de 0 até `page_count - 1`, retorna a primeira livre e a marca. Quando nenhuma existe, retorna `-1`. É simples e determinístico, mas pode ser O(n).

## 4. Free seguro
`free_page()` deve rejeitar índice fora da faixa e double-free. Detectar double-free cedo é importante porque liberar duas vezes pode corromper estruturas mais complexas.

## 5. Relação com sistemas reais
Kernels usam estruturas mais sofisticadas (buddy allocator, zones, per-CPU caches), mas o bitmap ensina representação compacta, invariantes e operações atômicas que reaparecem nesses sistemas.