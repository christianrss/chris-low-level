# Teoria passo a passo — WASM binary triage

WebAssembly binário começa com 8 bytes: magic `00 61 73 6d` e versão little-endian `01 00 00 00`.
Depois há seções: `id:u8`, `payload_len:ULEB128`, payload. O parser precisa ser defensivo porque lengths vêm da entrada.

ULEB128 codifica 7 bits por byte; bit 7 indica continuação. Um decoder precisa limitar quantidade de bytes para
evitar integer abuse e detectar EOF. Para u32, no máximo 5 bytes.

O laboratório usa apenas fixtures sintéticos. Não executa módulos e não interpreta código. Objetivo: validar header,
percorrer seções, preservar offsets e rejeitar truncation, tamanho fora do arquivo e ULEB128 longo.
