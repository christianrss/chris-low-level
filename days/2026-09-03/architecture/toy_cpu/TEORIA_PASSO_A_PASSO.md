# Teoria passo a passo - CPU toy

Uma CPU arquitetural pode ser entendida como estado + transicoes. Estado: registradores, PC e memoria. Cada `step()` busca um opcode em `memory[PC]`, incrementa PC, decodifica operandos e altera o estado.

A codificacao desta CPU e propositalmente pequena. `MOVI` demonstra imediato little-endian; `ADD` demonstra registradores; `LOAD/STORE` conectam CPU e memoria; `JNZ` demonstra controle de fluxo; `HALT` encerra execucao.

O objetivo nao e imitar x86. E construir um modelo mental que depois sera comparado com RISC-V e com o decoder x86-64.
