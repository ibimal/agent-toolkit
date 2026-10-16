---
name: handoff
description: "Writes a handoff note for the next session: what it needs that is not written down elsewhere, pointers to the spec, plan, commits and ADRs, and suggested skills. Use when the user stops part-way through work or switches devices."
license: MIT
disable-model-invocation: true
---

Read [local.md](local.md) first. It holds this repo's additions to the
instructions below, and it wins where the two differ. The instructions
below come from an upstream skill; `PROVENANCE` names it and lists the
changes.

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
