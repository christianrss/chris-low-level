# Teoria passo a passo — descriptor rings (produtor / device / consumidor)

## 1. O que estamos construindo

Um modelo software de fila circular de descriptors como em NICs, SSDs NVMe e GPUs: o produtor submete trabalho, o device processa, o consumidor reclama slots completos.

Sem DMA/MMIO real — apenas as invariantes de ownership e ordem.

## 2. Por que rings antes de drivers

Drivers reais falham de formas repetidas:

- slot reutilizado antes do device terminar;
- complete fora de ordem sem política clara;
- `count` inconsistente com cursores;
- reclaim de slot ainda owned pelo device.

Este lab isola essas regras em C++ testável.

## 3. Estrutura interna

```text
ring_[0..N-1]  cada Descriptor { length, owned_by_device, completed }

producer_  -> próximo slot a preencher
device_    -> próximo slot que o device deve completar
consumer_  -> próximo slot que o software pode reclamar
count_     -> slots ocupados (submetidos, não reclamados)
device_pending_ -> trabalhos ainda com o device
```

Diagrama com capacidade 2:

```text
       submit                complete           reclaim
producer --> [slot0][slot1] --> device --> consumer
              ^                      |
              +-------- count_ -------+
```

## 4. Exemplo numérico (capacidade 2)

```text
submit(64)   -> slot0, producer=1, count=1, dev_pend=1
submit(128)  -> slot1, producer=0, count=2, dev_pend=2
submit(256)  -> false (cheio)
complete     -> slot0 completed, device=1, dev_pend=1
reclaim      -> retorna 64, consumer=1, count=1
submit(256)  -> reutiliza slot0
```

## 5. Semântica das operações

**submit(length):** falha se `count == capacity`. Marca `owned_by_device=true`, `completed=false`, avança `producer_`, incrementa `count_` e `device_pending_`.

**device_complete_one():** falha se `device_pending_==0`. Marca `completed=true`, `owned_by_device=false`, avança `device_`, decrementa `device_pending_`. Não decrementa `count_`.

**reclaim():** falha se vazio ou slot ainda não `completed`. Retorna `length`, limpa descriptor, avança `consumer_`, decrementa `count_`.

## 6. Invariantes

- `0 <= count_ <= ring_.size()`.
- Slot submetido: `owned_by_device && !completed`.
- Após complete: `!owned_by_device && completed`.
- Após reclaim: descriptor zerado, slot livre.
- `device_pending_` nunca negativo.

## 7. Complexidade

- Cada operação: O(1) tempo, O(1) espaço extra.
- Throughput limitado pela capacidade do ring, não pela complexidade algorítmica.

## 8. Bugs comuns

- Decrementar `count_` em `complete` (errado — só em `reclaim`).
- Reclaim fora de ordem FIFO do consumer.
- Não zerar descriptor após reclaim (estado fantasma).
- `producer_` e `consumer_` divergem sem wrap `% size`.
- Aceitar `submit` quando `count_ == size`.

## 9. Comparação com produção

| Lab | virtio / NVMe / e1000 |
|-----|----------------------|
| struct C++ simples | descriptors em memória DMA |
| complete FIFO | às vezes out-of-order com tags |
| sem locks | producer/consumer com barriers atômicas |
| um thread | IRQ + NAPI + user space |

O padrão mental produtor→device→consumidor é o mesmo.

## 10. Passo a passo guiado

1. Implemente `submit` (`RING-SUBMIT-01`).
2. Implemente `device_complete_one` (`RING-COMPLETE-01`).
3. Implemente `reclaim` (`RING-RECLAIM-01`).
4. Trace manualmente o exemplo de capacidade 2.
5. `ctest --test-dir starter/build`.

## 11. Como saber se está correto

Teste de wrap-around: ordem de reclaim `64 → 128 → 256` após submits e completes conforme roteiro.
## 7. Ring buffer de descriptors

```text
     producer_idx          consumer_idx
          |                      |
   [D0][D1][D2][D3]  (máscara wrap)
```

## 8. Ownership

| Estado | Quem escreve payload |
|--------|---------------------|
| FREE | host (submit) |
| DEVICE | simulador (complete) |
| COMPLETED | host (reclaim) |

## 9. Invariantes

- Nunca submit se `(prod+1)%cap == cons` (cheio).
- Reclaim só em ordem do consumer.
- Descriptor reutilizado só após reclaim.

## 10. Bugs comuns

- Off-by-one no teste de ring cheio.
- Reclaim fora de ordem corrompe fila.
- Esquecer máscara `& (cap-1)` quando cap é potência de 2.

---

## Por quê — síntese pedagógica

### Por quê este módulo existe?
Conectar teoria de baixo nível a decisões de implementação verificáveis — não decorar API.

### Por quê estas invariantes?
Cada `TODO [ID]` protege uma propriedade que quebra silenciosamente em produção se ignorada (overflow, estado inválido, parsing parcial).

### Por quê medir e portar para `projects/`?
Lab isola o aprendizado; `projects/chris-*` consolida engenharia de portfólio com testes e benchmarks reproduzíveis.
