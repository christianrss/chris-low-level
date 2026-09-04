# Teoria passo a passo — Arena Allocator

## 1. O problema
`malloc`/`new` resolvem muitos casos, mas cada alocação pode envolver metadados, busca por blocos livres e sincronização. Quando muitos objetos possuem o mesmo lifetime, podemos reservar uma região grande e apenas avançar um cursor.

## 2. Endereço, offset e alinhamento
Uma arena tem `base`, `capacity` e `offset`. A próxima alocação precisa começar num endereço múltiplo de `alignment`. Para alinhamentos potência de dois, `aligned = (value + alignment - 1) & ~(alignment - 1)`.

## 3. Lifetime
A arena não libera objetos individualmente. `reset()` descarta tudo de uma vez. Isso é excelente para frames, parsers, requests e fases temporárias, mas ruim quando objetos morrem em momentos arbitrários.

## 4. Invariantes
- `used <= capacity`;
- ponteiros retornados respeitam o alinhamento;
- uma falha de capacidade nunca avança o cursor;
- `reset()` volta `used` a zero.

## 5. Exercícios
**Fácil:** calcule manualmente o padding de offsets 0, 3, 16 e 31 para alinhamento 16.  
**Médio:** implemente `align_up` e valide power-of-two.  
**Difícil:** implemente `allocate` sem overflow de `capacity - aligned_offset`.  
**Desafio:** adicione marker/rewind e escreva testes de regiões aninhadas.
