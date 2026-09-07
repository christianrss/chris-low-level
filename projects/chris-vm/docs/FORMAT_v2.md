# CLVM FORMAT v2 (experimental)

See the didactic lab: [`days/2026-09-07/systems/clvm_v2_strings`](../../days/2026-09-07/systems/clvm_v2_strings/README.md).

- **v1** (Dia 01/04 / `clvm.exe` atual): `version == 1`, checksum sobre **code only**.
- **v2** (lab N4): `version == 2`, string pool after code, opcode `PRINTS` (`0x21`), checksum over **code \|\| pool**.

The production C++ loader in this repo remains **v1-only** until a deliberate dual-load milestone.
