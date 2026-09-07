# Pesquisa guiada — PS/2 mouse → InputEvent

Leia `Documentation/input/input-programming.rst`, o código de referência `drivers/input/mouse/psmouse-base.c` (visão geral), e a especificação PS/2 mouse packet (3 bytes, sign bits).

Perguntas:
1. Por que o bit 3 do byte 0 deve ser 1 em pacotes válidos?
2. Como o kernel diferencia PS/2 de ImPS/Explorer (wheel)?
3. Por que botões de mouse são `EV_KEY` e não um tipo separado?
4. Qual o papel de `serio` entre porta i8042 e driver de mouse?

## Regra
Fontes para entendimento — não para colar no starter.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| Bit sync byte 0 | | |
| ImPS vs bare PS/2 | | |
| EV_KEY para botões | | |
| serio layer | | |

## Checkpoint

Desenhe o pacote `08 05 03` anotando cada bit do byte 0 antes do primeiro TODO.
