# Architecture

Day 01 maps normalized instruction text directly to known x86-64 encoding rules. `mov r64, imm64` demonstrates REX.W, opcode-register encoding and little-endian immediates. Later milestones replace direct pattern matching with tokenizer/parser/instruction tables.
