# Exercícios — descriptor ring

## Fácil

- **RING-TRACE-01:** simule em papel capacidade 2 com submits 64, 128 e complete/reclaim passo a passo.
- **RING-SUBMIT-01:** implemente `submit` com checagem de ring cheio.

## Médio

- **RING-COMPLETE-01:** implemente `device_complete_one` preservando `count_`.
- **RING-RECLAIM-01:** implemente `reclaim` zerando o descriptor após leitura.

## Difícil

- **RING-WRAP-01:** prove com teste que `producer_` e `consumer_` fazem wrap corretamente após encher o ring.
- **RING-INV-01:** adicione asserts de invariante em debug e documente qual falha primeiro se complete for chamado duas vezes.

## Desafio

- **RING-PROD-01:** pesquise como NVMe ou virtio-net expõe filas separadas TX/RX e compare com este modelo unificado.
- **RING-LOCK-01:** esboce onde colocaria `memory_order_release/acquire` se múltiplos threads acessassem o ring.
