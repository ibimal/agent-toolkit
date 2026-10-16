---
name: research
description: "Answers a question from primary sources outside the repo (official docs, source code, specs, first-party APIs) in a background agent and writes a cited note to docs/research/. Use when the user wants a fact researched, when a wayfinder research ticket needs resolving, or when a decision waits on an outside fact."
license: MIT
---

Read [local.md](local.md) first. It holds this repo's additions to the
instructions below, and it wins where the two differ. The instructions
below come from an upstream skill; `PROVENANCE` names it and lists the
changes.

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
