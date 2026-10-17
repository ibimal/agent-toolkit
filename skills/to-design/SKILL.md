---
name: to-design
description: "Writes design.md for one Feature L change from its spec and ADRs (structure, interfaces, data model, and a threat model when the change crosses a trust boundary); in system mode writes docs/sdlc/architecture.md for a new application; on archive, merges a change's structural changes into architecture.md. Use when a playbook reaches to-design, at New application step 4, or when an existing project adopts the workflow."
metadata:
  inspired-by: https://github.com/github/spec-kit, https://kiro.dev/docs/specs/ and https://github.com/openai/skills (security-threat-model)
---

# To design

Design the structure a change or an application needs. Use the
`codebase-design` vocabulary (module, interface, seam, depth) for structure
and the terms in `GLOSSARY.md` for the domain. When the design names a new
concept, settle the term through `glossary`.

## Change mode: design.md

Read the intent, the spec and the ADRs in `docs/sdlc/adr/`, then write
`design.md` in the change folder:

- **Structure:** the modules the change adds or changes, and where their
  seams sit.
- **Interfaces:** what each caller must know: signatures, invariants, error
  modes, ordering.
- **Data model:** new or changed entities, fields and contracts.
- **Threat model,** when the change crosses a trust boundary (money,
  credentials, personal data): the assets, who could attack them and how,
  and the control for each threat.
- **Decisions:** each choice that is hard to reverse, recorded as an ADR.

The design and the plan are accepted together at the Feature L gate.

## System mode: architecture.md

First, grill the user (`grilling`, with `glossary`) on the choices that the
brief, the backlog, the spikes and the ADRs leave open, such as hosting,
cost limits and which boundaries must stay stable. Settle every point you
would otherwise guess. Then, at New application step 4, write
`docs/sdlc/architecture.md`:

- components and their boundaries;
- the core data model;
- integrations;
- environments and deployment;
- the testing and verification approach;
- observability.

Every product constraint in `product.md` maps to a choice; refer to the
constraint instead of restating it. Every open decision is resolved by an
ADR or deferred with a reason. A sensible default that nobody spiked is
recorded as a provisional ADR. For a model or data component, fix the eval
set, the quality thresholds and the data contracts here; they become part
of `verify-app`. The user accepts the architecture at a gate.

**An existing project.** At adoption, describe the architecture as it is,
not as it should be, and grill the user on what the code cannot show, such
as whether an odd structure is deliberate or a workaround. Record an existing decision as an ADR only when it is
hard to reverse and surprising, and link existing decision records instead
of moving them.

## Archive mode

When `ship` archives a change and `architecture.md` exists, merge the
change's structural changes from its `design.md` into `architecture.md`, so
the architecture keeps describing the system as it is.
