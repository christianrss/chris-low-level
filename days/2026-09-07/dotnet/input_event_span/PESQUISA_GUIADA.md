# Pesquisa guiada — input_event Span

Leia `man 3 input_event` (ou kernel doc `Documentation/input/input.rst`) e a doc Microsoft sobre `StructLayout`. Perguntas:

1. Por que x86_64 usa 24 bytes e não 16?
2. Qual diferença entre scancode evdev e usage HID USB?
3. Por que `BinaryPrimitives` é preferível a `BitConverter` com Span?
4. Como o kernel transforma pacote PS/2 em `EV_REL`?
5. Quando `Explicit` é obrigatório vs `Sequential`?

## Registro

| Pergunta | Resposta | Impacto no lab |
|----------|----------|----------------|
| (preencha) | | |

## Checkpoint

Desenhe o diagrama offset dos 24 bytes antes de `DN-INPUT-SPAN-02`.
