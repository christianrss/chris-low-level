# Benchmark guiado
Ainda não otimize o parser. Primeiro crie uma hipótese: tempo de execução será dominado por parsing ou VM para um programa curto executado uma vez? Depois separe as duas fases: compile uma vez e execute o mesmo `Program` muitas vezes.

No próximo milestone, compare interpreter stack-based com um bytecode register-based simples. Registre instruções executadas, tempo e tamanho do bytecode.
