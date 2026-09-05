# Teoria passo a passo — .NET/CLR: tiny CIL decoder

CIL é uma linguagem intermediária baseada em stack. Instruções como `ldc.i4.s` empilham um inteiro pequeno; `add` consome dois valores e empilha a soma; `ret` encerra o método. Hoje implementamos um decoder didático, não um runtime CLR completo.

O projeto C# usa `ReadOnlySpan<byte>` e retorna uma lista de `Instruction(offset,name,operand)`. O ambiente desta entrega não contém o SDK .NET, portanto o código é revisado estruturalmente e acompanhado de fixture/documentação, mas não executado aqui.
