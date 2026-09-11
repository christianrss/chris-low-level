# Resolução guiada — Telemetria de arena bump (C++)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `ARENA-TEL-01` | `starter/arena.cpp` | `arena_init` |
| `ARENA-TEL-02` | `starter/arena.cpp` | `arena_alloc` |
| `ARENA-TEL-03` | `starter/arena.cpp` | `arena_reset` |

> Raiz: `days/2026-09-09/systems/arena_telemetry/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cmake -S days/2026-09-09/systems/arena_telemetry/starter -B days/2026-09-09/systems/arena_telemetry/starter/build_ci -G "Visual Studio 17 2022" -A x64
cmake --build days/2026-09-09/systems/arena_telemetry/starter/build_ci --config Release
ctest --test-dir days/2026-09-09/systems/arena_telemetry/starter/build_ci -C Release --output-on-failure
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## ARENA-TEL-01

### Onde colocar (ARENA-TEL-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/arena.cpp` |
| Função / âncora | `arena_init` — comentário `TODO [ARENA-TEL-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `ARENA-TEL-01`, o Caso correspondente falha: Após init, used==0 e allocs==0.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `ARENA-TEL-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```cpp
void arena_init(Arena *a) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-01
    a->used = 0; a->allocs = 0; a->resets = 0;
}
```

### Por que funciona?

Por quê este corpo satisfaz `ARENA-TEL-01`: ele implementa exatamente o contrato do
teste (Após init, used==0 e allocs==0.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `ARENA-TEL-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## ARENA-TEL-02

### Onde colocar (ARENA-TEL-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/arena.cpp` |
| Função / âncora | `arena_alloc` — comentário `TODO [ARENA-TEL-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `ARENA-TEL-02`, o Caso correspondente falha: alloc(8) ok; alloc(60) retorna -1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `ARENA-TEL-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```cpp
int arena_alloc(Arena *a, size_t n, char **out) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-02
    if (!a || !out || a->used + n > 64) return -1;
    *out = a->buf + a->used;
    a->used += n;
    a->allocs++;
    return 0;
}
```

### Por que funciona?

Por quê este corpo satisfaz `ARENA-TEL-02`: ele implementa exatamente o contrato do
teste (alloc(8) ok; alloc(60) retorna -1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `ARENA-TEL-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## ARENA-TEL-03

### Onde colocar (ARENA-TEL-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/arena.cpp` |
| Função / âncora | `arena_reset` — comentário `TODO [ARENA-TEL-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `ARENA-TEL-03`, o Caso correspondente falha: Após reset: used==0, resets==1, allocs==1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `ARENA-TEL-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```cpp
void arena_reset(Arena *a) {
    // PEDAGOGY-SOLUTION: ARENA-TEL-03
    if (!a) return;
    a->used = 0;
    a->resets++;
}
```

### Por que funciona?

Por quê este corpo satisfaz `ARENA-TEL-03`: ele implementa exatamente o contrato do
teste (Após reset: used==0, resets==1, allocs==1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `ARENA-TEL-03`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.


## Debug

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| NotImplemented / stub | corpo não substituído | cole o bloco do TODO |
| número/string diferente | trace errado no papel | refaça a seção 4 da TEORIA |
| caso seguinte quebra | mudou assinatura ou estado global | restaure o que “Não mexer” pede |
| listener/null (.NET) | sem ActivityListener | veja TESTES_GUIADOS |

## Checkpoint intermediário de integração

Depois do primeiro TODO que compila:

1. Rode o teste do módulo a partir de `starter/` (ou o comando do Baseline).
2. Confirme que o Caso 1 ainda falha **só** nos TODOs restantes (não por link quebrado).
3. Anote a mensagem de assert: ela aponta o próximo ID.

## Passo a passo de edição (operacional)

Para cada TODO restante, repita:

1. Abra o arquivo da tabela **Onde colocar**.
2. Localize o comentário `TODO [ID]` — não busque pelo nome do módulo na pasta pai.
3. Substitua **apenas** o corpo indicado; preserve assinatura e includes.
4. Compile; se o erro for de tipo/assinatura, você editou demais.
5. Só então avance ao próximo ID.

## Tabela de regressão rápida

| Depois de | Deve passar | Ainda pode falhar |
|-----------|-------------|-------------------|
| 1º TODO | asserts só desse ID | IDs seguintes |
| 2º TODO | IDs 1–2 | IDs seguintes |
| último TODO | suite inteira | — |

## Armadilhas específicas deste starter

- Mudar o teste para “passar” invalida o lab.
- Criar um segundo `.c`/`.py` com o mesmo símbolo gera link duplicado ou import errado.
- Reset ausente entre casos deixa estado (anel, FSM, arena) contaminado.

## Relatório — campos extras

Além do template padrão, anote:

- Tempo até o primeiro Caso 1 verde:
- Quantas vezes o endianness/size foi a causa:
- Um invariante que você quase violou:

## Relatório de resolução

- TODOs concluídos:
- Comando de teste:
- Saída observada:
- Invariantes checadas:
- Edge cases:
- Benchmark (`1e6 alloc(8)+reset ciclos`):
