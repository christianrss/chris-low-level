# Benchmark — hid_report_fuzz

## Procedimento

Cronometre 10_000× `validate_hid_boot_length` + `count_nonzero_key_slots` em fixtures válidas vs spam.

## Resultados observados

N/A em CI; no laptop esperado <1 ms total — triage é O(8) por relatório.
