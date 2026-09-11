// PEDAGOGY-TEST: RS-STACK-SAMPLE-01
// PEDAGOGY-TEST: RS-STACK-FRAME-02
// PEDAGOGY-TEST: RS-STACK-REPORT-03
// Caso 1: 2 frames
// Caso 2: resolve main
// Caso 3: report contém main
use stack_sample_trace::*;
use std::collections::HashMap;

#[test]
fn stack_trace_cases() {
    let frames = vec![0x1000u64, 0x2000, 0x3000];
    let sample = sample_stack(&frames, 2);
    assert_eq!(sample, vec![0x1000, 0x2000]);
    let mut syms = HashMap::new();
    syms.insert(0x1000, "main");
    assert_eq!(resolve_frame(0x1000, &syms), "main");
    let rep = format_stack_report(&[sample], &syms);
    assert!(rep.contains("main"));
}
