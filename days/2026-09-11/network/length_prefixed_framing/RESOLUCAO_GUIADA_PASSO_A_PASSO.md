# Resolucao guiada — length_prefixed_framing

## Mapa exato starter → resolucao

| TODO | Arquivo | Funcao |
|------|---------|--------|
| `D9-NET-ENCODE` | `starter/length_prefixed_framing.py` | `encode` |
| `D9-NET-DECODE` | `starter/length_prefixed_framing.py` | `decode_one` |
| `D9-NET-FEED` | `starter/length_prefixed_framing.py` | `feed` |


## Baseline

```powershell
cd days/2026-09-11/network/length_prefixed_framing/starter
python test_length_prefixed_framing.py
```

**Esperado antes dos TODOs:** FAIL.


## D9-NET-ENCODE

### Onde colocar (D9-NET-ENCODE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/length_prefixed_framing.py` |
| Funcao | `encode` |
| Substituir | corpo sob `TODO [D9-NET-ENCODE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-NET-ENCODE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-NET-ENCODE`.

### Escreva o codigo

```python
        return struct.pack("<I", len(payload)) + payload
    def feed(self, data: bytes):
        self.buf.extend(data)
    def decode_one(self):
        if len(self.buf) < 4:
            return None
        (n,) = struct.unpack_from("<I", self.buf, 0)
        if len(self.buf) < 4 + n:
```

### Por que funciona?
Materializa o contrato numerico de `D9-NET-ENCODE`.

### Verifique
Baseline parcial; `D9-NET-ENCODE` PASS.

### Checkpoint
- [ ] `D9-NET-ENCODE` PASS

## D9-NET-DECODE

### Onde colocar (D9-NET-DECODE)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/length_prefixed_framing.py` |
| Funcao | `decode_one` |
| Substituir | corpo sob `TODO [D9-NET-DECODE]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-NET-DECODE` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-NET-DECODE`.

### Escreva o codigo

```python
        if len(self.buf) < 4:
            return None
        (n,) = struct.unpack_from("<I", self.buf, 0)
        if len(self.buf) < 4 + n:
            return None
        payload = bytes(self.buf[4:4+n])
        del self.buf[:4+n]
        return payload
```

### Por que funciona?
Materializa o contrato numerico de `D9-NET-DECODE`.

### Verifique
Baseline parcial; `D9-NET-DECODE` PASS.

### Checkpoint
- [ ] `D9-NET-DECODE` PASS

## D9-NET-FEED

### Onde colocar (D9-NET-FEED)

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/length_prefixed_framing.py` |
| Funcao | `feed` |
| Substituir | corpo sob `TODO [D9-NET-FEED]` |
| Nao mexer | assinatura / testes |

### O problema
Sem este passo o assert de `D9-NET-FEED` falha.

### Algoritmo / trace
Caso do TESTES_GUIADOS ligado a `D9-NET-FEED`.

### Escreva o codigo

```python
        self.buf.extend(data)
    def decode_one(self):
        if len(self.buf) < 4:
            return None
        (n,) = struct.unpack_from("<I", self.buf, 0)
        if len(self.buf) < 4 + n:
            return None
        payload = bytes(self.buf[4:4+n])
```

### Por que funciona?
Materializa o contrato numerico de `D9-NET-FEED`.

### Verifique
Baseline parcial; `D9-NET-FEED` PASS.

### Checkpoint
- [ ] `D9-NET-FEED` PASS

## Debug

| Sintoma | Causa | Correcao |
|---------|-------|----------|
| stub | corpo intacto | cole o bloco |
| off-by-one | size | refaca trace |

## Relatorio de resolucao

- TODOs:
- Saida:
- Invariantes:
- Benchmark: nao executado
