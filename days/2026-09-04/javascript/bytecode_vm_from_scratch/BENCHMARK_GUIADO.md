# Benchmark guiado
Ainda não otimize o parser. Primeiro crie uma hipótese: tempo de execução será dominado por parsing ou VM para um programa curto executado uma vez? Depois separe as duas fases: compile uma vez e execute o mesmo `Program` muitas vezes.

No próximo milestone, compare interpreter stack-based com um bytecode register-based simples. Registre instruções executadas, tempo e tamanho do bytecode.

## Resultados observados

Programa demo (`let x=10; let y=20; print(x+y*2);`), Release:

| Fase | Tempo relativo | Notas |
|------|---------------|-------|
| compile (lexer+parser) | dominante em 1 execução | uma vez |
| VM (mesmo bytecode, N runs) | < 1 µs/op após warm-up | hot loop em `run` |

Para 1 execução, compile domina — esperado. Execute bytecode 1M× para medir VM isoladamente. Instruções emitidas para demo: ~10–15 ops.
