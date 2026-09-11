# Resolução guiada — ActivitySource e spans (.NET)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `DN-ACT-SOURCE-01` | `starter/ActivityLab.cs` | `DN-ACT-SOURCE-01` |
| `DN-ACT-SPAN-02` | `starter/ActivityLab.cs` | `CreateSource` |
| `DN-ACT-EXPORT-03` | `starter/ActivityLab.cs` | `StartWorkSpan` |

> Raiz: `days/2026-09-09/dotnet/activity_source_span/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-09/dotnet/activity_source_span/starter
dotnet test
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## DN-ACT-SOURCE-01

### Onde colocar (DN-ACT-SOURCE-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ActivityLab.cs` |
| Função / âncora | `DN-ACT-SOURCE-01` — comentário `TODO [DN-ACT-SOURCE-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `DN-ACT-SOURCE-01`, o Caso correspondente falha: Name == chris.lab.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `DN-ACT-SOURCE-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```csharp
    public static ActivitySource CreateSource(string name)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-SOURCE-01
        return new ActivitySource(name);
    }
```

### Por que funciona?

Por quê este corpo satisfaz `DN-ACT-SOURCE-01`: ele implementa exatamente o contrato do
teste (Name == chris.lab.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `DN-ACT-SOURCE-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## DN-ACT-SPAN-02

### Onde colocar (DN-ACT-SPAN-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ActivityLab.cs` |
| Função / âncora | `CreateSource` — comentário `TODO [DN-ACT-SPAN-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `DN-ACT-SPAN-02`, o Caso correspondente falha: tag module == activity_source_span.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `DN-ACT-SPAN-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```csharp
    public static Activity? StartWorkSpan(ActivitySource src, string op)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-SPAN-02
        var act = src.StartActivity(op);
        act?.SetTag("module", "activity_source_span");
        return act;
    }
```

### Por que funciona?

Por quê este corpo satisfaz `DN-ACT-SPAN-02`: ele implementa exatamente o contrato do
teste (tag module == activity_source_span.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `DN-ACT-SPAN-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## DN-ACT-EXPORT-03

### Onde colocar (DN-ACT-EXPORT-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/ActivityLab.cs` |
| Função / âncora | `StartWorkSpan` — comentário `TODO [DN-ACT-EXPORT-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `DN-ACT-EXPORT-03`, o Caso correspondente falha: export == work|activity_source_span.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `DN-ACT-EXPORT-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```csharp
    public static string ExportSpanSummary(Activity? act)
    {
        // PEDAGOGY-SOLUTION: DN-ACT-EXPORT-03
        if (act is null) return "null";
        return $"{act.OperationName}|{act.GetTagItem("module")}";
    }
```

### Por que funciona?

Por quê este corpo satisfaz `DN-ACT-EXPORT-03`: ele implementa exatamente o contrato do
teste (export == work|activity_source_span.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `DN-ACT-EXPORT-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 StartWorkSpan+Export`):
