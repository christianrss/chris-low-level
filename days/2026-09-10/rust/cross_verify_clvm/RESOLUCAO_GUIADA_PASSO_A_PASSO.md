# Resolução guiada — Cross-verify header CLVM (Rust)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-RS-XVFY-01` | `starter/src/lib.rs` | `fnv1a32` |
| `CAP-RS-XVFY-02` | `starter/src/lib.rs` | `_` |
| `CAP-RS-XVFY-03` | `starter/src/lib.rs` | `_` |

> Raiz: `days/2026-09-10/rust/cross_verify_clvm/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/rust/cross_verify_clvm/starter
cargo test
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-RS-XVFY-01

### Onde colocar (CAP-RS-XVFY-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `fnv1a32` — comentário `TODO [CAP-RS-XVFY-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-RS-XVFY-01`, o Caso correspondente falha: magic CLVM.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-RS-XVFY-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```rust
pub fn fnv1a32(data: &[u8]) -> u32 {
    let mut h = 0x811C_9DC5u32;
    for &b in data {
        h ^= u32::from(b);
        h = h.wrapping_mul(0x0100_0193);
    }
    h
}
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-RS-XVFY-01`: ele implementa exatamente o contrato do
teste (magic CLVM.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-RS-XVFY-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-RS-XVFY-02

### Onde colocar (CAP-RS-XVFY-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `_` — comentário `TODO [CAP-RS-XVFY-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-RS-XVFY-02`, o Caso correspondente falha: version 1.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-RS-XVFY-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```rust
pub fn validate_header(data: &[u8]) -> bool {
    data.len() >= 16 && data.starts_with(MAGIC) && data[4] == 1
}
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-RS-XVFY-02`: ele implementa exatamente o contrato do
teste (version 1.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-RS-XVFY-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-RS-XVFY-03

### Onde colocar (CAP-RS-XVFY-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `_` — comentário `TODO [CAP-RS-XVFY-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-RS-XVFY-03`, o Caso correspondente falha: FNV confere.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-RS-XVFY-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```rust
    let size = u32::from_le_bytes(data[8..12].try_into().unwrap()) as usize;
    if data.len() < 16 + size { return None; }
    /* contrato: mantenha a assinatura do starter */
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-RS-XVFY-03`: ele implementa exatamente o contrato do
teste (FNV confere.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-RS-XVFY-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 validates`):
