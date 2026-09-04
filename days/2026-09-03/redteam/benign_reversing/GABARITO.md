# Gabarito - Red Team benigno

A função `verify_code` exige 8 bytes. Cada byte é transformado por `(input[i] XOR 0x2A) + i` e comparado com a tabela constante.

O foco do exercício não é descobrir o código por tentativa bruta, mas reconstruir a lógica pelo assembly e relacioná-la ao código C. Use somente o `lab_target` fornecido.
