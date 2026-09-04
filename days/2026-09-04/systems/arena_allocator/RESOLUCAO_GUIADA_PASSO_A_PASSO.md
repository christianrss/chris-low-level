# Resolução guiada passo a passo — Arena allocator

> Trabalhe em `days/2026-09-04/systems/arena_allocator/starter/`. `solutions/` é o gabarito final e só deve ser consultado depois da tentativa.

## 0. Preparar o projeto
No terminal, entre na raiz do repositório e execute:

```bash
cmake -S days/2026-09-04/systems/arena_allocator/starter -B days/2026-09-04/systems/arena_allocator/starter/build
cmake --build days/2026-09-04/systems/arena_allocator/starter/build
ctest --test-dir days/2026-09-04/systems/arena_allocator/starter/build --output-on-failure
```

O build deve funcionar. Os testes **devem falhar**, pois `src/arena.cpp` contém TODOs. Esse é o baseline.

## Exercício fácil — potência de dois
### Arquivo
Abra:

```text
starter/src/arena.cpp
```

Localize:

```cpp
bool Arena::is_power_of_two(std::size_t value) noexcept {
```

Substitua o corpo por:

```cpp
return value != 0 && (value & (value - 1)) == 0;
```

### Por que funciona?
Uma potência de dois tem apenas um bit 1: `8 = 1000b`. Subtrair 1 produz `0111b`; o `&` resulta zero. O teste `value != 0` é necessário porque zero também produziria zero na expressão bit a bit.

### Verificação manual
Calcule para 8, 16, 3 e 0 antes de continuar.

## Exercício médio — `align_up`
No mesmo arquivo, localize:

```cpp
std::size_t Arena::align_up(std::size_t value, std::size_t alignment)
```

Primeiro valide o parâmetro:

```cpp
if (!is_power_of_two(alignment)) {
    throw std::invalid_argument("alignment must be a power of two");
}
```

Logo abaixo, adicione:

```cpp
const std::size_t mask = alignment - 1;
return (value + mask) & ~mask;
```

### Trace no papel
Para `value=13` e `alignment=8`:

```text
mask = 7
13 + 7 = 20
20 & ~7 = 16
```

O resultado é múltiplo de 8 e não é menor que 13.

## Exercício difícil — `allocate`
Localize:

```cpp
void* Arena::allocate(std::size_t size, std::size_t alignment)
```

### Passo 1 — rejeitar tamanho zero
Digite no início:

```cpp
if (size == 0) {
    throw std::invalid_argument("allocation size must be non-zero");
}
```

### Passo 2 — obter o endereço base
Adicione:

```cpp
const std::size_t base = reinterpret_cast<std::uintptr_t>(storage_.data());
```

`storage_.data()` é ponteiro; convertemos para inteiro sem sinal suficientemente grande para fazer a aritmética de alinhamento.

### Passo 3 — alinhar o próximo endereço
Adicione:

```cpp
const std::size_t aligned_address = align_up(base + offset_, alignment);
const std::size_t aligned_offset = aligned_address - base;
```

Agora `aligned_offset` é a posição dentro do vetor.

### Passo 4 — verificar exaustão sem overflow
Adicione:

```cpp
if (aligned_offset > storage_.size() || size > storage_.size() - aligned_offset) {
    throw std::bad_alloc();
}
```

### Passo 5 — avançar cursor e retornar
Adicione:

```cpp
offset_ = aligned_offset + size;
return storage_.data() + static_cast<std::ptrdiff_t>(aligned_offset);
```

## Exercício final — reset
Localize:

```cpp
void Arena::reset() noexcept
```

O corpo completo é:

```cpp
offset_ = 0;
```

## Rode os testes novamente

```bash
cmake --build days/2026-09-04/systems/arena_allocator/starter/build
ctest --test-dir days/2026-09-04/systems/arena_allocator/starter/build --output-on-failure
```

Saída esperada contém:

```text
chris-arena tests passed
100% tests passed
```

## Como depurar se falhar
- `second % 32 != 0`: coloque breakpoint em `Arena::allocate`; observe `base`, `offset_`, `aligned_address`, `aligned_offset`.
- `std::bad_alloc` cedo demais: calcule `storage_.size() - aligned_offset` e compare com `size`.
- teste de alinhamento 3 não lança exceção: verifique `is_power_of_two(3)`.
- `reset` falha: observe `offset_` antes/depois.

No GDB:

```bash
gdb --args days/2026-09-04/systems/arena_allocator/starter/build/chris_arena_tests
```

No Visual Studio, abra o executável/test target, marque breakpoint em `Arena::allocate` e adicione as quatro variáveis acima ao Watch.

## Benchmark
Depois dos testes:

```bash
cmake -S days/2026-09-04/systems/arena_allocator/starter -B days/2026-09-04/systems/arena_allocator/starter/build-bench -DCHRIS_BUILD_BENCHMARKS=ON
cmake --build days/2026-09-04/systems/arena_allocator/starter/build-bench
./days/2026-09-04/systems/arena_allocator/starter/build-bench/chris_arena_benchmark
```

Antes de executar, escreva a hipótese: "para muitas alocações temporárias de tamanho fixo, a arena deve reduzir overhead em relação a várias alocações de heap". Não transforme um resultado local em regra universal.

## Solução final comentada
Compare seu arquivo com `solutions/src/arena.cpp`. Você deve conseguir justificar cada linha: validação, alinhamento, checagem de capacidade, avanço do cursor e reset.
