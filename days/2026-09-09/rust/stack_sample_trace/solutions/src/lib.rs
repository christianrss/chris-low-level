pub fn sample_stack(frames: &[u64], n: usize) -> Vec<u64> {
    // PEDAGOGY-SOLUTION: RS-STACK-SAMPLE-01
    frames.iter().take(n).copied().collect()
}

pub fn resolve_frame(addr: u64, symbols: &std::collections::HashMap<u64, &str>) -> String {
    // PEDAGOGY-SOLUTION: RS-STACK-FRAME-02
    symbols.get(&addr).map(|s| s.to_string()).unwrap_or_else(|| format!("0x{addr:x}"))
}

pub fn format_stack_report(
    samples: &[Vec<u64>],
    symbols: &std::collections::HashMap<u64, &str>,
) -> String {
    // PEDAGOGY-SOLUTION: RS-STACK-REPORT-03
    let mut out = String::new();
    for (i, st) in samples.iter().enumerate() {
        out.push_str(&format!("sample {}:\n", i));
        for addr in st {
            out.push_str(&format!("  {}\n", resolve_frame(*addr, symbols)));
        }
    }
    out
}
