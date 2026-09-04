# Experiment idea: decoder validation against an external reference

Generate a controlled corpus of instruction bytes that your decoder claims to support. Compare mnemonic/length with an external reference disassembler. Record mismatches by opcode class.

This is validation, not implementation-by-copying: the project decoder remains independent.
