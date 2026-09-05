# Testes guiados — JavaScript runtime from scratch: branches em bytecode VM

`JSVM-JZ-01`: condição zero vai para bloco else; condição não zero continua. `JSVM-JMP-02`: branch then pula o else. `node starter/test.js` deve falhar no TODO; solution imprime `OK jsvm branches`.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
