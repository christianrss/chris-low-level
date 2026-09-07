# Teoria — HID report fuzz (red team)

## 1. Contexto

Este lab tria relatórios **HID boot keyboard** de 8 bytes antes que cheguem ao parser do módulo `linux/hid_keyboard_boot`. Red team aqui é **defensivo**: validar wire format, limites e extrair evidência legível.

TODOs: `RT-HID-MAGIC-01`, `RT-HID-BOUNDS-02`, `RT-HID-STRINGS-03`.

## 2. Layout boot keyboard (8 bytes)

| Offset | Campo |
|--------|-------|
| 0 | modifiers |
| 1 | reservado (0) |
| 2..7 | até 6 key usages |

### Por quê validar tamanho primeiro?

Parsers C que indexam `raw[2]` sem checar `len` são vetores clássicos de over-read em fuzzing.

## 3. RT-HID-MAGIC-01

```text
fixture report_a.raw: 00 00 04 00 00 00 00 00  → len==8 OK
fixture report_short.raw: 7 bytes → FAIL
```

## 4. RT-HID-BOUNDS-02

Key spam: preencher todos os 6 slots com usages distintos. Contagem detecta flood sem simular driver completo.

## 5. RT-HID-STRINGS-03

Formato `usage:0xNN` para logs — mesmo espírito de `extract_ascii_strings` em `compressed_blob_triage`.

## 6. Ligação com drivers (Dia 07)

O ring buffer `HID-KBD-RING-03` assume relatórios já validados. Este lab é a camada **antes** do parse semântico.

## 7. Threat model simplificado

| Ataque | Mitigação no lab |
|--------|------------------|
| relatório curto | MAGIC-01 |
| 6 teclas + modifiers | BOUNDS-02 alerta |
| análise forense | STRINGS-03 |

## 8. Trace hex — tecla A

```text
raw[0]=0x00 modifiers
raw[2]=0x04 usage KEY_A
extract → ["usage:0x04"]
```

## 9. Por quê não fuzzar no kernel primeiro?

Userspace triage é mais rápido de iterar; o capstone `chris-binary-toolkit` agrega ELF + strings + triage.

## 10. Complexidade

O(1) por relatório — 8 bytes fixos.

## 11. Bugs comuns

- Contar byte 1 reservado como tecla.
- Aceitar `len >= 8` em vez de `== 8`.

## 12. Comparação com produção

| Lab | Produção |
|-----|----------|
| Python triage | eBPF + hidraw audit |
| fixtures .raw | captura Wireshark/usbmon |

## 13. Síntese pedagógica

### Por quê este módulo no Dia 07?

Conecta **input drivers** com mindset **red team** sem misturar código do parser já resolvido.

### Por quê três TODOs separados?

MAGIC, bounds e strings testam invariantes independentes — falha isolada é mais fácil de depurar.

### Por quê medir antes de portar?

Evidência em `test_hid_fuzz.py` vira teste de regressão em `projects/chris-binary-toolkit`.

## 14. Exercício de papel

Anote hex de `report_a.raw` antes de abrir o starter.

## 15. Checklist pré-código

- [ ] Sei que byte 1 é reservado
- [ ] Sei diferença MAGIC vs BOUNDS
- [ ] Li TESTES_GUIADOS Caso 1-4

## 16. Referências

USB HID boot keyboard spec (resumo no PESQUISA_GUIADA).

## 17. Anti-patterns

Não chame `hid_boot_parse_report` antes de MAGIC-01.

## 18. Integração CI

`python test_hid_fuzz.py` no gate do dia.

## 21. Linha do tempo

Faça este módulo após `linux/hid_keyboard_boot` e antes do bloco GFX opcional.

## 19. Port para projects/

`chris-binary-toolkit` — módulo triage HID.

## 20. Fechamento do módulo

Após PASS, revise um relatório real capturado com usbmon (opcional).

