# Architecture
The first slice deliberately skips a full AST and compiles recursive-descent expressions directly to a tiny stack bytecode. This keeps the entire pipeline visible: characters → tokens → parser precedence → bytecode → operand stack → globals → output. Future milestones will split AST and bytecode compiler, add functions/closures/objects, then GC/type feedback/JIT/deoptimization.
