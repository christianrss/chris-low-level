# Validação — 2026-09-08

```powershell
python scripts/pedagogy_check_unified.py --day 2026-09-08
python scripts/day_contract_check.py --day 2026-09-08
python scripts/run_day_tests.py --day 2026-09-08 --mode solutions
```

| Módulo | Linguagem | Gate |
|--------|-----------|------|
| clvm_disassembler | C | ctest |
| clvm_peephole_opt | C++ | ctest |
| input_event_ring_mux | C | ctest |
| clvm_disasm | Rust | cargo test |
| pe_export_span | .NET | dotnet test |
| shader_stage_fsm | C++ | ctest |
| pe_export_triage | Python | python |
| bell_state_prep | C++ | ctest |
| softmax_stable | C | ctest |
| duplex_event_pipe | JavaScript | node |
| json_rd_lexer | C | ctest |
| tool_protocol_fsm | Python | python |
| wasm_section_header | Assembly | ctest |
