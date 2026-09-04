# Testing methodology

Tests are part of the implementation, not an afterthought.

## Types used in this repository

- **Unit test:** isolates a small function or invariant.
- **Integration test:** checks multiple components together, such as assembler -> file -> VM.
- **Regression test:** records behavior that previously failed so the bug cannot silently return.
- **Smoke test:** asks whether the essential workflow works at all.
- **Golden test:** compares structured output with a known expected output.
- **Property test:** checks an invariant over many generated inputs.
- **Fuzz test:** repeatedly gives unusual inputs to a parser/decoder to find crashes or invariant violations.

## Guided test design

For every feature, answer four questions before writing code:

1. What behavior must be true?
2. What is the smallest positive example?
3. What invalid or boundary input should be rejected?
4. What bug would be easy to reintroduce later?

A strong project usually contains all four categories.
