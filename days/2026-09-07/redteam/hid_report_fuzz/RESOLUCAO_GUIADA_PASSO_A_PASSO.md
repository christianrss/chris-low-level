# Resolução guiada — hid_report_fuzz

## Mapa exato starter → resolução

| TODO ID | Arquivo starter | Função | Substituir |
|---------|-----------------|--------|------------|
| `RT-HID-MAGIC-01` | `starter/hid_fuzz.py` | `validate_hid_boot_length` | stub TODO |
| `RT-HID-BOUNDS-02` | `starter/hid_fuzz.py` | `count_nonzero_key_slots` | stub TODO |
| `RT-HID-STRINGS-03` | `starter/hid_fuzz.py` | `extract_hid_usage_hex` | stub TODO |

## Baseline

```powershell
cd days/2026-09-07/redteam/hid_report_fuzz/starter
python test_hid_fuzz.py
```

**Esperado:** FAIL com `NotImplementedError` até completar TODOs.

## Relatório de resolução

## RT-HID-MAGIC-01

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hid_fuzz.py` |
| Função | `validate_hid_boot_length` |

### 1. O problema

Relatório HID boot deve ter exatamente 8 bytes. Tamanho errado indica fuzz ou driver bug.

### Escreva o código

```python
def validate_hid_boot_length(raw: bytes) -> bool:
    return len(raw) == HID_BOOT_REPORT_LEN
```

### Por que funciona?

Boot keyboard protocol fixa 8 bytes no wire.

### Verifique

Caso 2: `report_short.raw` (7 bytes) → False.

### Debug

| Sintoma | Ação |
|---------|------|
| aceita 9 bytes | não use `>=` — use `==` |

---

## RT-HID-BOUNDS-02

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hid_fuzz.py` |
| Função | `count_nonzero_key_slots` |

### 1. O problema

Detectar key spam contando slots 2..7 não vazios.

### Escreva o código

```python
def count_nonzero_key_slots(raw: bytes) -> int:
    if len(raw) != HID_BOOT_REPORT_LEN:
        return -1
    return sum(1 for b in raw[2:8] if b != 0)
```

### Por que funciona?

Byte 1 reservado; até 6 teclas simultâneas no boot protocol.

### Verifique

Caso 3: seis usages → retorno 6.

---

## RT-HID-STRINGS-03

### Onde colocar

| Campo | Valor |
|-------|-------|
| Arquivo | `starter/hid_fuzz.py` |
| Função | `extract_hid_usage_hex` |

### 1. O problema

Formato estável para logs de triage (`usage:0xNN`).

### Escreva o código

```python
def extract_hid_usage_hex(raw: bytes) -> List[str]:
    if len(raw) != HID_BOOT_REPORT_LEN:
        return []
    return [f"usage:0x{b:02x}" for b in raw[2:8] if b != 0]
```

### Por que funciona?

Strings legíveis para diff em relatórios red team.

### Verifique

Caso 4: tecla A → `usage:0x04`.

### Resultado esperado

`python test_hid_fuzz.py` imprime `OK hid_fuzz`.
