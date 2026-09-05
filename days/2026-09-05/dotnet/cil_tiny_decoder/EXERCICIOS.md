# Exercícios — CIL tiny decoder

## Fácil — CLR-IL-OPCODE-01
Decodifique manualmente `{ 0x1F, 0x0A, 0x2A }` — quantas instruções? Quais offsets?

## Médio — CLR-IL-OPCODE-01
Implemente cases para `ldc.i4.s`, `add` e `ret` até o self-test passar.

## Médio — CLR-IL-OPERAND-02
Garanta que `0x1F 0xFF` decodifica operand `-1`, não `255`.

## Difícil
Adicione suporte a `ldc.i4.0` (0x16) sem operand e teste com `{ 0x16, 0x2A }`.

## Desafio
Use `ildasm` ou `dotnet ilverify` em um assembly real e compare offsets com seu decoder em método trivial.

## Reflexão
Por que o CLR usa stack de avaliação em vez de registradores virtuais como a JVM?
