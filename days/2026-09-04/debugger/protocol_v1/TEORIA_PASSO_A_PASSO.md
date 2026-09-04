# Teoria passo a passo — Debug protocol v1

## Layout
Header fixo de 20 bytes:

```text
offset  size  campo
0       4     magic "CKD1"
4       2     version
6       2     command
8       4     request_id
12      4     payload_size
16      4     FNV-1a(payload)
20      N     payload
```

Inteiros são little-endian. O decoder deve rejeitar header truncado, magic/version incorretos, comprimento divergente e checksum inválido.

## Arquitetura futura
`chris-kd-stub` no kernel ↔ transporte serial/virtio/TCP ↔ protocolo ↔ cliente host `chris-debugger`. O parser precisa ser pequeno e defensivo porque no futuro estará próximo de código privilegiado.
