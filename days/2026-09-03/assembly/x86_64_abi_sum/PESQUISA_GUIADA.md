# Pesquisa guiada — x86-64 ABI

## Fontes
- System V AMD64 ABI, seção de calling convention.
- Intel Software Developer Manual para instruções `mov`, `add`, `cmp`, `jmp` e `ret`.

## Termos
`System V AMD64 integer arguments registers`, `callee saved caller saved`, `x86-64 loop assembly`.

## Perguntas
1. Em quais registradores chegam os primeiros argumentos inteiros?
2. Qual registrador transporta o retorno inteiro?
3. Quais registradores precisam ser preservados pelo callee?
4. Como um loop em C aparece em compare/branch?
5. O que mudaria na ABI Microsoft x64?

Use a ABI como contrato. O exercício deve ser derivado desse contrato, não copiado de uma função pronta.
