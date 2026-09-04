# Gabarito - MiniObjdump

A solução demonstra:

- leitura little-endian independente do host;
- identificação de ELF64 e PE;
- enumeração de sections sem headers específicos do sistema operacional;
- localização de `.text`;
- decoder mínimo x86-64 com fallback seguro para bytes desconhecidos;
- cálculo de destino para `CALL rel32` e `JMP rel32` relativo ao endereço da próxima instrução.

- extensão auditada do decoder para `INT3` (`0xCC`) e `LEAVE` (`0xC9`).
