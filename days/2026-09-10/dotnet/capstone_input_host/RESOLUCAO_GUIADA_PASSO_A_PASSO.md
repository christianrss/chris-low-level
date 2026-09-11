# Resolução guiada — Host de input com Span (.NET)

## Mapa exato starter → resolução

| TODO ID | Arquivo | Função / âncora |
|---------|---------|-----------------|
| `CAP-DN-HOST-01` | `starter/InputHost.cs` | `CAP-DN-HOST-01` |
| `CAP-DN-HOST-02` | `starter/InputHost.cs` | `TryParse` |
| `CAP-DN-HOST-03` | `starter/InputHost.cs` | `CountEvents` |

> Raiz: `days/2026-09-10/dotnet/capstone_input_host/starter/`. Tente sozinho antes de usar esta página.

## Baseline

```powershell
cd days/2026-09-10/dotnet/capstone_input_host/starter
dotnet test
```

**Esperado antes dos TODOs:** FAIL (NotImplemented, stub, assert).


## CAP-DN-HOST-01

### Onde colocar (CAP-DN-HOST-01)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/InputHost.cs` |
| Função / âncora | `CAP-DN-HOST-01` — comentário `TODO [CAP-DN-HOST-01]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-DN-HOST-01`, o Caso correspondente falha: cria/host básico.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-DN-HOST-01` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```csharp
public static class InputHost
{
    public const int EventSize = 24;

    /// PEDAGOGY-SOLUTION: CAP-DN-HOST-01
    public static bool TryParse(ReadOnlySpan<byte> buffer, out InputEvent ev)
    {
        ev = default;
        if (buffer.Length < EventSize) return false;
        ev = new InputEvent(
            BitConverter.ToUInt16(buffer.Slice(16, 2)),
            BitConverter.ToUInt16(buffer.Slice(18, 2)),
            BitConverter.ToInt32(buffer.Slice(20, 4)));
        return true;
    }

    /// PEDAGOGY-SOLUTION: CAP-DN-HOST-02
    public static int CountEvents(ReadOnlySpan<byte> buffer)
    {
        return buffer.Length / EventSize;
    }

    /// PEDAGOGY-SOLUTION: CAP-DN-HOST-03
    public static string Summarize(ReadOnlySpan<byte> buffer)
    {
        int n = CountEvents(buffer);
        return $"events={n}";
    }
}
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-DN-HOST-01`: ele implementa exatamente o contrato do
teste (cria/host básico.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-DN-HOST-01`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-DN-HOST-02

### Onde colocar (CAP-DN-HOST-02)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/InputHost.cs` |
| Função / âncora | `TryParse` — comentário `TODO [CAP-DN-HOST-02]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-DN-HOST-02`, o Caso correspondente falha: parse Span.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-DN-HOST-02` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```csharp
    public static bool TryParse(ReadOnlySpan<byte> buffer, out InputEvent ev)
    {
        ev = default;
        if (buffer.Length < EventSize) return false;
        ev = new InputEvent(
            BitConverter.ToUInt16(buffer.Slice(16, 2)),
            BitConverter.ToUInt16(buffer.Slice(18, 2)),
            BitConverter.ToInt32(buffer.Slice(20, 4)));
        return true;
    }
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-DN-HOST-02`: ele implementa exatamente o contrato do
teste (parse Span.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-DN-HOST-02`. Esperado: este caso PASS; os TODOs
seguintes ainda podem FAIL.

## CAP-DN-HOST-03

### Onde colocar (CAP-DN-HOST-03)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/InputHost.cs` |
| Função / âncora | `CountEvents` — comentário `TODO [CAP-DN-HOST-03]` |
| Substituir | o **corpo** sob o TODO (mantenha a assinatura) |
| Não mexer | outros TODOs neste passo; arquivos de teste |

### O problema

Sem `CAP-DN-HOST-03`, o Caso correspondente falha: contagem do teste.

### Algoritmo / trace

Use o trace da TEORIA (seção 4) e o trecho de `CAP-DN-HOST-03` abaixo. Confira o número
no papel antes de colar.

### Escreva o código

```csharp
    public static int CountEvents(ReadOnlySpan<byte> buffer)
    {
        return buffer.Length / EventSize;
    }
```

### Por que funciona?

Por quê este corpo satisfaz `CAP-DN-HOST-03`: ele implementa exatamente o contrato do
teste (contagem do teste.), sem atalho que ignore o wire da TEORIA.

### Verifique

Rode o teste do starter focando `CAP-DN-HOST-03`. Esperado: este caso PASS; os TODOs
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
- Benchmark (`1e5 parse Span`):
