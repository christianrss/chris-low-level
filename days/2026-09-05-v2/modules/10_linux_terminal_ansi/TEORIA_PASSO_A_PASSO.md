# Teoria passo a passo

## 1. Terminal não é shell
O shell interpreta comandos; o terminal interpreta bytes de controle e exibe texto. ANSI/VT escape sequences alteram cor, cursor e outras propriedades. Esta separação é essencial antes de estudar PTY/TTY.

## 2. CSI
Uma sequência CSI começa com ESC + `[`, possui parâmetros e termina em um byte final. Hoje aceitamos `m` (SGR) e `H` (cursor position).

## 3. SGR mínimo
`0m` reseta atributos e `31m` seleciona vermelho no modelo didático (`fg=1`). Não é um emulador completo.

## 4. Cursor position
`H` usa linha/coluna 1-based. O estado interno usa 0-based, então subtraímos 1. Defaults são 1,1.

## 5. Parser incremental
O método `feed` percorre texto, acumula caracteres normais em `screen_text` e despacha CSI para `_apply_csi`. Ao depurar, imprima `repr(seq)` em vez de emitir ESC cru no terminal da sessão.

## 6. Próxima evolução
Depois entram PTY master/slave, termios, canonical/raw mode, resize, UTF-8 width e renderer de terminal.