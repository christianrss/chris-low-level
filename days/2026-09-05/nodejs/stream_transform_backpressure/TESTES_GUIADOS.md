# Testes guiados — Node.js: Transform stream + backpressure observável

`NODE-XFORM-01`: linhas fragmentadas, linha vazia e caractere UTF-8 dividido entre chunks. `NODE-BACKPRESSURE-02`: Writable lento/highWaterMark pequeno deve produzir ao menos um `write() === false` e emitir `drain`. Execute `node starter/test.js`; solution deve imprimir `OK node streams`.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
