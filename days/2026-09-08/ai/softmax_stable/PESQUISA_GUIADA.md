# Pesquisa guiada — ai/softmax_stable

## Fontes âncora

1. Documentação / RFC / ISA ligada ao wire-format deste módulo (CLVM Dia 03, PE/COFF, WASM, evdev, Node streams, JSON RFC 8259, quantum notes, numerics).
2. Comparar com o módulo-irmão no mesmo dia (C↔Rust disasm, .NET↔redteam PE, ring↔duplex).
3. Nota de produção: como a ferramenta real (objdump, pe-parse, Qiskit, PyTorch) expõe o mesmo conceito.

## Perguntas (responda em 4–8 linhas cada)

1. Qual invariante quebra se o size/estado estiver off-by-one?
2. Onde o lab simplifica vs produção — e o que isso esconde?
3. Qual caso negativo do teste é o mais importante para segurança/robustez?
4. Como você portaria este mecanismo para `projects/chris-*`?

## Entregável

Uma página no caderno: diagrama do fluxo + três riscos + uma citação da fonte âncora com offset/fórmula.
