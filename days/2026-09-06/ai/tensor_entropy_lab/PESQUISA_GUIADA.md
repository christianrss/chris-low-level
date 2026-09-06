# Pesquisa guiada — Tensor entropy lab

Leia sobre entropia de Shannon (Cover & Thomas, cap. 2) e RFC 1951 (DEFLATE). Perguntas:

1. Por que entropia empírica de uma amostra finita pode **subestimar** a entropia verdadeira da fonte?
2. Em quantização de pesos int8, como entropia do tensor informa escolha de escala?
3. Compare RLE em pares `(valor, count)` vs formato `(count, byte)` do módulo `systems/rle_byte_codec`.
4. Por que `gzip.compress` em payload de 1 byte quase sempre tem `ratio > 1`?
5. Leia documentação Python `gzip.compress` — qual overhead fixo o header `1F 8B` adiciona?

## Regra

Use as fontes para **entender e validar**. Não copie implementação pronta para preencher o starter. Registre em poucas linhas o que aprendeu e qual decisão do exercício a fonte ajuda a justificar.

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar por que 4 símbolos equiprováveis dão H=2.0 **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
