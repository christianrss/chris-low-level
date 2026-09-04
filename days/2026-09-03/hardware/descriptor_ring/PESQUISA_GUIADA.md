# Pesquisa guiada — descriptor rings e filas de dispositivos

## Fontes
- Virtio specification, conceitos de descriptor/available/used rings.
- Datasheets públicos de NICs apenas para comparar head/tail, ownership e completion.

## Termos
`NIC descriptor ring head tail ownership`, `virtio queue descriptor available used`, `DMA ring buffer wrap around`.

## Perguntas
1. Quem é dono de um descriptor em cada estado?
2. O que distingue `complete()` de `reclaim()`?
3. Por que head/tail precisam de aritmética circular?
4. Como distinguir ring cheio de ring vazio?
5. Que invariantes impedem reutilizar um descriptor cedo demais?

O simulador não faz DMA real; use specs para entender o modelo, não para fingir acesso a hardware.
