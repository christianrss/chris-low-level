# Teoria passo a passo — SPSC ring buffer

Um ring buffer single-producer/single-consumer é uma fila circular em que exatamente uma thread avança `head`
e exatamente uma thread avança `tail`. Essa restrição remove várias disputas que existiriam numa MPMC queue.

Usaremos capacidade lógica N com storage N+1: um slot fica sacrificado para distinguir cheio de vazio.

```text
vazio: head == tail
cheio: next(head) == tail
next(i) = (i + 1) % storage_size
```

O producer escreve o item antes de publicar o novo `head`; o consumer lê o item antes de publicar o novo `tail`.
Em implementação concorrente real, a ordem de memória é parte da correção. O laboratório primeiro fixa as
invariantes e depois usa `std::atomic<size_t>` com acquire/release.

Para push: leia head local, compute next. Se next == tail adquirido, cheio. Grave storage[head]; publique head com
release. Para pop: leia tail local; se tail == head adquirido, vazio. Leia storage[tail]; publique tail com release.

Acquire/release forma o happens-before necessário para que o consumer que observa o head publicado também observe
a escrita do item. Este laboratório não é uma MPMC queue e não deve ser generalizado para múltiplos producers.
