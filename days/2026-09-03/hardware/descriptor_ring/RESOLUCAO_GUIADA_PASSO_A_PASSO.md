# Resolução guiada auditada — descriptor_ring

## Mapa exato starter → resolução

| TODO ID | Starter | Função/área |
|---------|---------|-------------|
| `RING-SUBMIT-01` | `starter/src/descriptor_ring.cpp` | `DescriptorRing::submit()` |
| `RING-COMPLETE-01` | `starter/src/descriptor_ring.cpp` | `DescriptorRing::device_complete_one()` |
| `RING-RECLAIM-01` | `starter/src/descriptor_ring.cpp` | `DescriptorRing::reclaim()` |

Cada ID acima existe como `TODO [ID]` no starter, como `PEDAGOGY-SOLUTION: ID` no gabarito e como `PEDAGOGY-TEST: ID` nos testes. Se um nome/caminho não bater, pare: a atividade está inconsistente.

> Trabalhe em `days/2026-09-03/hardware/descriptor_ring/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Edite

```text
starter/src/descriptor_ring.cpp
```

A classe/estado já está declarado em `starter/include/descriptor_ring.hpp`. Não crie novos índices: use `producer_`, `device_`, `consumer_`, `count_` e `device_pending_` existentes.

## 1. Baseline

```bash
cmake -S starter -B starter/build
cmake --build starter/build
ctest --test-dir starter/build --output-on-failure
```

O starter deve compilar e falhar porque `submit()` ainda retorna `false`.

## 2. `submit`

Troque a assinatura placeholder para usar o parâmetro:

```cpp
bool DescriptorRing::submit(std::uint32_t length) {
```

Implemente:

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

Invariante: descriptor submetido pertence ao device e ainda não está completed.

### Por que funciona?
`count_ == ring_.size()` detecta ring cheia sem ambiguidade. O produtor escreve no slot `producer_`, marca ownership no device e avança com módulo — reutilização circular. `device_pending_` separa “submetido ao hardware” de “ainda ocupando capacidade lógica” até o consumer reclamar.

## 3. `device_complete_one`

```cpp
if (device_pending_ == 0) {
    return false;
}

auto& desc = ring_[device_];
if (!desc.owned_by_device || desc.completed) {
    throw std::logic_error("ring ownership invariant broken");
}

desc.completed = true;
desc.owned_by_device = false;
device_ = (device_ + 1) % ring_.size();
--device_pending_;
return true;
```

O device não decrementa `count_`: o slot ainda não foi reclamado pelo software.

### Por que funciona?
O device só marca `completed` e libera ownership — o slot continua “ocupado” na fila até o software consumir. A exceção em invariante quebrada força você a não chamar `complete` em descriptor já devolvido ou nunca submetido.

## 4. `reclaim` — código que faltava na versão antiga

```cpp
if (count_ == 0) {
    return std::nullopt;
}

auto& desc = ring_[consumer_];
if (!desc.completed) {
    return std::nullopt;
}

const auto length = desc.length;
desc = Descriptor{};
consumer_ = (consumer_ + 1) % ring_.size();
--count_;
return length;
```

A atribuição `Descriptor{}` limpa ownership/completion/length antes de reutilizar o slot.

### Por que funciona?
`reclaim` só avança se o head está `completed` — ordem FIFO do consumer. `Descriptor{}` evita vazar estado sujo no próximo `submit`. `--count_` aqui (e não em `complete`) é o que libera capacidade para novo submit.

## 5. Teste de wrap-around

Com capacidade 2:

```text
submit 64   -> producer 1
submit 128  -> producer 0, ring cheia
submit 256  -> false
complete/reclaim 64 -> consumer 1
submit 256  -> reutiliza slot 0
complete/reclaim -> 128
complete/reclaim -> 256
```

Rode:

```bash
ctest --test-dir starter/build --output-on-failure
```

## 6. Debugging

Breakpoint em cada avanço de cursor. Registre:

```text
producer_ device_ consumer_ count_ device_pending_
```

- ordem 64→256→128: você avançou/reclamou o cursor errado;
- slot nunca libera: esqueceu `--count_` em `reclaim`;
- complete quebra invariante: confira `owned_by_device=true` em `submit`;
- divisão por zero: construtor deve continuar rejeitando capacity 0.

A solution correspondente está em `solutions/src/descriptor_ring.cpp`.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `RING-SUBMIT-01` — `starter/src/descriptor_ring.cpp` → `solutions/src/descriptor_ring.cpp`.
- `RING-COMPLETE-01` — `starter/src/descriptor_ring.cpp` → `solutions/src/descriptor_ring.cpp`.
- `RING-RECLAIM-01` — `starter/src/descriptor_ring.cpp` → `solutions/src/descriptor_ring.cpp`.

## Relatório de resolução

Checklist ao concluir:

- [ ] Submit/complete/reclaim respeitam ownership e ordem FIFO do consumer.
- [ ] Teste de wrap-around (capacidade 2) passa em `starter/tests/test_ring.cpp`.
- [ ] `count_` só decrementa em `reclaim`, não em `complete`.
- [ ] Trace manual 64→128→256 documentado.

**Saída esperada:** `ctest` 100% passed no teste de wrap-around.

**Depuração:** logue os cinco contadores após cada operação (ver seção 6 da resolução).

**Arquivos starter editados:** `starter/src/descriptor_ring.cpp`.
