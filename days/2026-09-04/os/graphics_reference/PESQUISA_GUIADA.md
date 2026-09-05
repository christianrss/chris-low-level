# Pesquisa guiada — Graphics reference para o futuro chris-os

## Contexto
Hoje o código roda em user space como **referência de correção**. Ele não é ainda o framebuffer do kernel. Essa separação permite testar clipping/composição antes de carregar bugs para ring 0.

## Referências futuras
Virtio 1.2 define um GPU device e serve como referência para a futura integração em QEMU:
https://docs.oasis-open.org/virtio/virtio/v1.2/csd01/virtio-v1.2-csd01.pdf

Pesquise também:
- `framebuffer linear pixel buffer pitch stride`
- `Porter Duff source over alpha compositing`
- `damage tracking compositor`
- `virtio gpu resource create 2d transfer flush`

## Perguntas
1. Como `(x,y)` vira índice linear?
2. O que clipping evita quando um retângulo começa em coordenada negativa?
3. Qual a diferença entre surface, layer, compositor e display scanout?
4. Por que testar composição em CPU primeiro ajuda a futura implementação de driver/GPU?

## Registro do aluno

| Pergunta | Sua resposta (3–5 linhas) | Decisão no código |
|----------|---------------------------|-------------------|
| (preencha após ler as fontes acima) | | |

## Checkpoint

Antes de implementar o primeiro `TODO [ID]`, você deve conseguir explicar o conceito central **sem olhar a resolução**. Registre no Relatório de resolução se passou neste checkpoint.
