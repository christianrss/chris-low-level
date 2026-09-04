# Safety Boundaries

This repository includes security and systems topics because understanding them is valuable for defensive engineering. The lab therefore uses explicit boundaries.

## Allowed practical environments
- binaries written for this repository;
- localhost services;
- disposable VMs/QEMU images owned by the learner;
- deliberately vulnerable educational targets with authorization;
- simulated fleets/peers/networks inside the repository.

## Red-team topics are redirected toward safe mechanisms
- botnet/C2 -> benign fleet orchestration + beacon/telemetry simulation;
- lateral movement -> trust-boundary labs, logging, segmentation and detection;
- process injection -> instrumentation/debugging in owned processes;
- obfuscation -> toy transformations on owned binaries + deobfuscation;
- stealth/evasion -> defensive detection signals, not operational bypass instructions.

No credential theft, third-party compromise, malware persistence, destructive payloads, anti-cheat bypass, stealth deployment or unauthorized access belongs in the portfolio.
