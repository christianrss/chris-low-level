# Teoria passo a passo — GC allocation probe

`GC.GetAllocatedBytesForCurrentThread()` permite observar bytes alocados pela thread desde um ponto do runtime.
O objetivo é comparar dois caminhos equivalentes: montar pequenos payloads criando arrays versus reutilizando
`ArrayPool<byte>`.

Allocated bytes não é memória viva e não é RSS. É contagem cumulativa de alocações gerenciadas atribuídas à thread.
JIT warm-up e infraestrutura do teste precisam ser separados da janela medida.

`ArrayPool<byte>.Rent(n)` pode retornar array maior que n. O consumidor deve respeitar o comprimento lógico e sempre
devolver em `finally`. `Span<byte>` é view; não possui o buffer.

O laboratório não tenta provar que pooling é sempre melhor: retenção de buffers grandes, limpeza e complexidade
também têm custo.
