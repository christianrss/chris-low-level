# Gabarito — Node.js — Transform e Backpressure

Respostas esperadas (consulte `solutions/` para código completo).

1. StringDecoder + pending para linhas incompletas.
2. _flush emite pending final.
3. falseWrites > 0 e drains == falseWrites.
4. Writable com highWaterMark=8 força backpressure.
