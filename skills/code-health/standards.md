# Baseline standards

Use these when the repo has no `REVIEW.md`. They are the same baseline
that `setup` writes into a new `REVIEW.md`.

## Precedence

When standards disagree, the repo's own rules win (AGENTS.md, REVIEW.md,
ADRs), then the deep-module vocabulary, then general guidance such as Clean
Code. Where "keep functions small" would produce shallow pass-through code,
deep modules win. A metric is a signal, never a reason on its own: split a
function because it does two jobs, not because it is long.

## Standards

| Topic | What to look for |
|---|---|
| Names | Names say what a thing is for; one term per concept, matching GLOSSARY.md; no vague names (data, tmp, helper, manager) and no names that lie |
| Functions | One job at one level of abstraction; no flag arguments; few parameters; no hidden side effects; guard clauses instead of deep nesting; named constants instead of magic numbers |
| Simplicity | No dead or commented-out code, speculative generality, one-caller wrappers, pass-through layers, or the same logic written three times |
| Modules | Deep modules with small interfaces; no feature envy, data clumps, primitive obsession or god modules |
| Architecture | Dependencies point inward: domain logic never imports frameworks, I/O or storage; a pure core with I/O at the edges; no import cycles; the boundaries architecture.md names |
| Errors and types | No swallowed errors or bare except; validation at system boundaries; typed public functions |
| Tests | Tests call the code the way its users do; no test that would pass if every function returned nothing; no flaky or long-skipped tests |
| Security | No secrets in code; credentials never held in types whose repr or dump is generated; no logging or tracing of whole objects; untrusted input validated at the boundary |
| Style | The language's standard style, enforced by its formatter and linter |

## Thresholds

These raise a signal, not a verdict: cyclomatic complexity over 10,
functions over about 50 lines, more than 5 parameters.
