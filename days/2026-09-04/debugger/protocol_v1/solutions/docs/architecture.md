# Architecture

The debugger protocol is intentionally transport-independent. Day 02 validates framing and corruption detection on the host. Later the same packets can travel over a serial port, virtio-console or a controlled TCP transport.

Keeping the protocol separate from the kernel stub makes fuzzing and deterministic tests possible before privileged code is involved.
