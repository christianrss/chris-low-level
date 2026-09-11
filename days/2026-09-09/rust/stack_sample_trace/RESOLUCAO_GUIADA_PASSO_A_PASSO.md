# Resolução guiada — Amostra de stack e resolução de símbolos (Rust)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `RS-STACK-SAMPLE-01` | `starter/src/lib.rs` | `sample_stack` |
| `RS-STACK-FRAME-02` | `starter/src/lib.rs` | `resolve_frame` |
| `RS-STACK-REPORT-03` | `starter/src/lib.rs` | `format_stack_report` |

> Raiz: `days/2026-09-09/rust/stack_sample_trace/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/rust/stack_sample_trace/starter
cargo test
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## RS-STACK-SAMPLE-01

### Onde colocar (RS-STACK-SAMPLE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `sample_stack` — comentário `TODO [RS-STACK-SAMPLE-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `RS-STACK-SAMPLE-01`, o Caso correspondente falha: sample == [0x1000, 0x2000].

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `RS-STACK-SAMPLE-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```rust
pub fn sample_stack(frames: &[u64], n: usize) -> Vec<u64> {
    // PEDAGOGY-SOLUTION: RS-STACK-SAMPLE-01
    frames.iter().take(n).copied().collect()
}
```

### Por que funciona?

Por quê este corpo satisfaz `RS-STACK-SAMPLE-01`: ele implementa exatamente o contrato do
teste (sample == [0x1000, 0x2000].), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `RS-STACK-SAMPLE-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## RS-STACK-FRAME-02

### Onde colocar (RS-STACK-FRAME-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `resolve_frame` — comentário `TODO [RS-STACK-FRAME-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `RS-STACK-FRAME-02`, o Caso correspondente falha: resolve_frame(0x1000)=="main".

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `RS-STACK-FRAME-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```rust
pub fn resolve_frame(addr: u64, symbols: &std::collections::HashMap<u64, &str>) -> String {
    // PEDAGOGY-SOLUTION: RS-STACK-FRAME-02
    symbols.get(&addr).map(|s| s.to_string()).unwrap_or_else(|| format!("0x{addr:x}"))
}
```

### Por que funciona?

Por quê este corpo satisfaz `RS-STACK-FRAME-02`: ele implementa exatamente o contrato do
teste (resolve_frame(0x1000)=="main".), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `RS-STACK-FRAME-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## RS-STACK-REPORT-03

### Onde colocar (RS-STACK-REPORT-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/src/lib.rs` |
| Função / âncora | `format_stack_report` — comentário `TODO [RS-STACK-REPORT-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `RS-STACK-REPORT-03`, o Caso correspondente falha: report contém main.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `RS-STACK-REPORT-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```rust
pub fn format_stack_report(
    samples: &[Vec<u64>],
    symbols: &std::collections::HashMap<u64, &str>,
) -> String {
    // PEDAGOGY-SOLUTION: RS-STACK-REPORT-03
    let mut out = String::new();
    for (i, st) in samples.iter().enumerate() {
        out.push_str(&format!("sample {}:\n", i));
        for addr in st {
            out.push_str(&format!("  {}\n", resolve_frame(*addr, symbols)));
        }
    }
    out
}
```

### Por que funciona?

Por quê este corpo satisfaz `RS-STACK-REPORT-03`: ele implementa exatamente o contrato do
teste (report contém main.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `RS-STACK-REPORT-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 resolve_frame`):
