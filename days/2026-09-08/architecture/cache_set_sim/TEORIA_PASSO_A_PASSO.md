# Teoria passo a passo — Set-associative cache simulator

Uma cache é dividida em sets; cada set possui `ways` linhas. Endereço vira:
`block = address // line_size`,
`set = block % set_count`,
`tag = block // set_count`.

Hit ocorre quando uma line válida do set tem a tag. Em miss, escolhemos vítima LRU. O simulador ignora coerência,
write-back e latência real; objetivo é tornar index/tag/associativity observáveis.

Em cache direta, ways=1; conflito entre dois blocos do mesmo set causa eviction. Em 2-way, ambos podem coexistir.
LRU será implementado com contador monotônico `tick` por acesso.
