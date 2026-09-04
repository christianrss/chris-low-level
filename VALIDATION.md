# Validation status - 2026-09-03

The generated repository was validated in a Linux x86-64 environment with GCC 14.2.0, Python 3.13.5 and CMake 3.31.6.

Portable validation completed successfully for:

- `chris-vm`: build + CTest integration test;
- `chris-autograd`: C convergence test + Python autograd tests;
- `chris-disassembler`: build + benign executable integration test;
- `chris-binary-toolkit`: build + ASCII scanner tests;
- `chris-renderer`: portable scene-core build + CTest.

The DOCX was rendered and visually reviewed page by page. The Win32/WGL render executables were not executed in this Linux validation environment. The included GitHub Actions Windows job is intended to catch MSVC/Windows-SDK build regressions after the repository is pushed.
