# Pesquisa guiada — CLVM extended

1. Em CPUs reais, onde fica o return address (stack vs registrador `ra`/`lr`)? Compare com a call stack deste lab.
2. Por que Wasm e JVM separam *operand stack* de *locals*/memória linear?
3. Como `JL`/`JNE` em x86 diferem de `LT`+`JNZ` em duas instruções?
4. O que um bytecode verifier checaria sobre `CALL`/`RET` e profundidade de stack antes de executar?
5. Leia `docs/FORMAT.md` e liste cada opcode novo com efeito de stack em notação Forth (`a b -- c`).
