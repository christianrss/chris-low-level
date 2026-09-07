# Teoria — input event entropy

Par com `dotnet/input_event_span` e `tensor_entropy_lab` (Day 06).

## 1. InputEvent 24 bytes

Layout evdev simplificado — mesmo tema dos drivers Linux do dia.

## 2. Shannon (AI-EVT-ENT-01)

H em bits/byte sobre o stream bruto — teclas seguradas reduzem H.

## 3. RLE em codes (AI-EVT-RLE-02)

Sequência de `code` repetido → runs — útil antes de modelar ML.

## 4. gzip ratio (AI-EVT-RATIO-03)

Baseline de compressibilidade sem modelo.

## 5. Por quê AI neste dia?

Features de input podem alimentar modelos — entropia mede “quanto há para comprimir”.

## 6. Trace

```text
48× byte 0x01 → H=0
RLE [(1,48)]
gzip ratio << 1
```

## 7. Invariantes

0 ≤ H ≤ 8 para bytes.

## 8. Bugs

- log natural em vez de log2.
- RLE sem flush do último run.

## 9. Capstone

Insights portáveis para pipelines de telemetria.

## 10. Síntese

### Por quê três métricas?

H, RLE e gzip respondem perguntas diferentes sobre o mesmo stream.

### Por quê não neural net aqui?

Lab isolado mede fundamentos antes de embedding.

### Por quê ligar ao .NET?

Mesmo layout binário validado em duas linguagens.

## 11. Comparação Day 06

| tensor_entropy | input_event_entropy |
|----------------|---------------------|
| tensor ints | event bytes |

## 12. Próximo passo

Janela deslizante de entropia (fora do escopo).

## 13. Diagrama

```text
fixtures.bin → H → RLE → gzip ratio
```

## 14. Complexidade

O(N) por métrica.

## 15. Honestidade

Não é detecção de anomalia — só métricas.

## 16. Fixture

Reutilize `dotnet/input_event_span/starter/fixtures/*.bin`.

## 17. Por quê Counter?

Stdlib suficiente — sem NumPy.

## 18. Fechamento

Fecha trilha AI do Dia 07 ligada a input.

## 19. Paper-trace obrigatório

Calcule H manualmente para `[1,1,1,1]` antes do código.

## 20. Gate

`python test_input_entropy.py` no VALIDATION do dia.

## 21. Ordem sugerida

Após `dotnet/input_event_span` para reutilizar fixtures.

## 22. Honestidade

Não treina modelo — só mede estatísticas do stream.

## 23. Comparação com gzip lab

Mesma função `compression_ratio_gzip` do Day 06, aplicada a bytes de evento.

## 24. Fixture path

`../dotnet/input_event_span/starter/fixtures/event_stream.bin` — 24 bytes por evento.

## 25. Próximo passo

Compare métricas com `nodejs/input_event_transform` no mesmo fixture.

