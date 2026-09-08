# Teoria passo a passo — chris-xargs-lite

`xargs` transforma itens de stdin em argumentos de processos, reduzindo número de execuções por batching. O problema
central é framing de entrada e limite de batch, não shell parsing.

Para segurança pedagógica, nossa ferramenta recebe command já separado em argv e usa `subprocess.run(argv+batch,
shell=False)`. Não interpreta shell metacharacters.

Modo padrão separa whitespace; modo `-0` separa NUL, adequado para filenames com espaços/newlines. `-n N` limita
quantidade de itens por execução.

O teste nunca executa comandos destrutivos: usa um helper Python local que registra argv.
