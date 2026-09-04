# Teoria passo a passo

## 1. O problema de produção
Serviços de rede frequentemente precisam montar headers pequenos. Criar `byte[]` novo para cada mensagem aumenta a taxa de alocação e a pressão sobre o GC. O exercício separa três ideias: **ownership** do buffer, **view** temporária e **encoding** binário.

## 2. `Span<T>` não é dono da memória
`Span<byte>` descreve uma região contígua. Ele pode apontar para array, `stackalloc` ou memória nativa, mas não gerencia o lifetime do backing store. Isso explica por que `Span<T>` é `ref struct`.

## 3. `ArrayPool<T>`
O pool troca alocação frequente por reutilização. O custo passa a ser disciplina de ownership: cada `Rent` precisa de exatamente um `Return`, e código não pode usar a memória depois do retorno.

## 4. Endianness
O frame deste laboratório tem 8 bytes: quatro para comprimento e quatro para tipo, ambos `int32 little-endian`. `BinaryPrimitives` deixa a representação explícita.

## 5. Senioridade
A pergunta não é “ArrayPool é mais rápido?”. A pergunta correta é: qual é o perfil de alocações, qual é o tamanho/vida dos buffers, há risco de retenção, limpeza de dados sensíveis é necessária, e o pool realmente melhora o workload medido?
