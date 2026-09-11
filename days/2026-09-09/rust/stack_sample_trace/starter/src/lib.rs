pub fn sample_stack(frames: &[u64], n: usize) -> Vec<u64> {
    // TODO [RS-STACK-SAMPLE-01]
    let _ = (frames, n);
    vec![]
}

pub fn resolve_frame(addr: u64, symbols: &std::collections::HashMap<u64, &str>) -> String {
    // TODO [RS-STACK-FRAME-02]
    let _ = (addr, symbols);
    String::new()
}

pub fn format_stack_report(
    samples: &[Vec<u64>],
    symbols: &std::collections::HashMap<u64, &str>,
) -> String {
    // TODO [RS-STACK-REPORT-03]
    let _ = (samples, symbols);
    String::new()
}
