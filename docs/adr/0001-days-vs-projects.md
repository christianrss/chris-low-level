# ADR 0001 - Separate daily learning material from cumulative projects

## Status
Accepted - 2026-09-03

## Context
Daily exercises need starter code, guided solutions and pedagogical duplication. A public portfolio project should instead show one coherent codebase and its engineering history.

## Decision
Keep immutable-ish teaching snapshots under `days/YYYY-MM-DD/` and maintain clean evolving software under `projects/`.

## Consequences
- the learning path remains reproducible;
- project READMEs stay professional;
- starter/solution duplication does not pollute the clean project tree;
- improvements must be intentionally integrated from a daily lab into a cumulative project.
