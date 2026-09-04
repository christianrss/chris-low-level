# Resolucao guiada

1. Crie um vetor fixo de descriptors e tres indices: producer, device, consumer.
2. `submit` falha se a fila estiver cheia; marca ownership do device.
3. `device_complete_one` so pode completar descriptor que pertence ao device e ainda nao foi completado.
4. `reclaim` so devolve um descriptor ja concluido.
5. Todos os indices avancam com modulo `capacity`; isso produz wrap-around.
6. O teste principal usa capacidade 2, enche, confirma falha, completa/reclama, insere novamente e verifica ordem.
7. Benchmark descriptors/s. Mais tarde compare polling, batch e interrupt simulation.

## Etapa de código 1 - submit

```cpp
if (count_ == ring_.size()) {
    return false;
}
auto& desc = ring_[producer_];
desc.length = length;
desc.owned_by_device = true;
desc.completed = false;
producer_ = (producer_ + 1) % ring_.size();
++count_;
++device_pending_;
return true;
```

## Etapa de código 2 - completion

```cpp
auto& desc = ring_[device_];
if (!desc.owned_by_device || desc.completed) {
    throw std::logic_error("ring ownership invariant broken");
}
desc.completed = true;
desc.owned_by_device = false;
device_ = (device_ + 1) % ring_.size();
--device_pending_;
```

## Etapa de código 3 - reclaim

O software só pode reutilizar o descriptor no cursor consumer quando `completed=true`. Depois limpe o descriptor e avance com módulo da capacidade.

## Teste de wrap-around

Use capacidade 2: submeta 64 e 128, confirme que 256 falha, complete/reclame 64, submeta 256 e depois confirme a ordem 128 -> 256. Esse teste detecta erros de producer/consumer que aparecem apenas no wrap.

A solução final está em `solutions/src/descriptor_ring.cpp`.

