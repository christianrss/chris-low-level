# Resolução guiada — Duplex stream pipeline

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-ND-PIPE-01` | `starter/capstone_stream_pipeline.js` | `CAP-ND-PIPE-01` |
| `CAP-ND-PIPE-03` | `starter/capstone_stream_pipeline.js` | `CAP-ND-PIPE-03` |
| `CAP-ND-PIPE-02` | `starter/capstone_stream_pipeline.js` | `t` |

> Raiz: `days/2026-09-10/nodejs/capstone_stream_pipeline/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/nodejs/capstone_stream_pipeline/starter
node --test test.js 2>$null; if (-not $?) { node test.js }
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-ND-PIPE-01

### Onde colocar (CAP-ND-PIPE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_stream_pipeline.js` |
| Função / âncora | `CAP-ND-PIPE-01` — comentário `TODO [CAP-ND-PIPE-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-ND-PIPE-01`, o Caso correspondente falha: HELLO.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-ND-PIPE-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```javascript
        // PEDAGOGY-SOLUTION: CAP-ND-PIPE-01
        this.chunks++;
        this.push(Buffer.from(String(chunk).toUpperCase()));
        cb();
    }
    metrics() {
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-ND-PIPE-01`: ele implementa exatamente o contrato do
teste (HELLO.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-ND-PIPE-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-ND-PIPE-03

### Onde colocar (CAP-ND-PIPE-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_stream_pipeline.js` |
| Função / âncora | `CAP-ND-PIPE-03` — comentário `TODO [CAP-ND-PIPE-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-ND-PIPE-03`, o Caso correspondente falha: flush regra.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-ND-PIPE-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```javascript
        // PEDAGOGY-SOLUTION: CAP-ND-PIPE-03
        return { chunks: this.chunks };
    /* contrato: mantenha a assinatura do starter */
    _keep_signature = True  # não altere a assinatura

```

### Por que funciona?

Por quê este corpo satisfaz `CAP-ND-PIPE-03`: ele implementa exatamente o contrato do
teste (flush regra.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-ND-PIPE-03`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-ND-PIPE-02

### Onde colocar (CAP-ND-PIPE-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/capstone_stream_pipeline.js` |
| Função / âncora | `t` — comentário `TODO [CAP-ND-PIPE-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-ND-PIPE-02`, o Caso correspondente falha: metrics/chunks.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-ND-PIPE-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```javascript
    const t = new CapstoneTransform();
    // PEDAGOGY-SOLUTION: CAP-ND-PIPE-02
    return t;
}
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-ND-PIPE-02`: ele implementa exatamente o contrato do
teste (metrics/chunks.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-ND-PIPE-02`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e4 chunks`):
