# Pesquisa guiada — o que um debugger realmente mostra

Não implemente um x64dbg nativo neste dia. Use as fontes abaixo para
nomear as views que você está construindo na CLVM.

## Fontes

1. [x64dbg documentation](https://help.x64dbg.com/) — CPU view = hex +
   disasm + registros. Qual painel corresponde a `hex`, `disasm` e
   `regs` na CLVM?
2. GDB `stepi` / `x/16xb` / `info registers` — o contrato de “executar
   **uma** instrução” vs `continue`.
3. `days/2026-09-03/systems/clvm/docs/FORMAT.md` — header 16 B e FNV-1a.
4. `days/2026-09-04/systems/clvm_extended/docs/FORMAT.md` — CALL/RET e
   mem 256 B.
5. FNV-1a (IETF / Wikipedia) — por que checksum de integridade não é
   criptografia.

## Perguntas

- Se PC=0 na VM, qual offset no **arquivo** você aponta no hex dump?
  (Resposta esperada: 0x10.)
- Por que CALL usa uma call stack separada em vez de empilhar o retorno
  na data stack, como uma JVM faz com frames?
- Qual é o último endereço legal para um STORE de i32 em 256 bytes?
  Mostre a conta `addr+4 <= 256`.
- Em x64dbg, um breakpoint no endereço atual precisa de um “passo de
  saída”. Onde isso aparece em `Session::cont`?

## Entrega

Uma página no Relatório de resolução: tabela “view x64dbg → comando
clvm-xdbg → invariante testada”.
