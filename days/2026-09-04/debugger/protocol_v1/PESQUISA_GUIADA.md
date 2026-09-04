# Pesquisa guiada — Protocolo remoto do chris-debugger

## Referência arquitetural
GNU GDB documenta o Remote Serial Protocol, usado para depurar alvos sobre diferentes transportes:
https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Remote-Protocol.html

Leia apenas para entender decisões de protocolo: framing, comandos, respostas, checksums, transporte. **Não copie o protocolo**; `chris-debugger` usa framing próprio.

## Pesquise
- `little endian serialize uint32 bytes`
- `debugger remote stub host target architecture`
- `FNV-1a 32 bit checksum`
- `framing length checksum protocol parser`

## Perguntas
1. Por que separar transporte (serial/TCP) de formato do pacote?
2. Por que incluir magic e version?
3. Por que payload length precisa ser validado antes de acessar payload?
4. Checksum aqui protege contra corrupção acidental ou é autenticação criptográfica? (Resposta: não é autenticação.)
5. Como isso evoluirá para `chris-kd-stub` dentro do kernel?
