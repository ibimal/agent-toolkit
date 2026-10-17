---
name: start
description: "Routes any piece of work: classifies the request, matches it against the product brief and intent backlog, picks a playbook (New application, Feature S, M or L, Bug fix, Refactor, Spike, Incident) and loads its steps into the task list; resumes work in progress; points a need to the skill that meets it. On its own, reports what is in progress, what waits for the user and what to do next. Use for /start with a request, or /start alone."
disable-model-invocation: true
metadata:
  inspired-by: https://github.com/cursor/plugins/tree/main/pstack/skills/poteto-mode
---

# Start

Route every piece of work to the right depth: a playbook for work, a skill
for a need. [playbooks.md](playbooks.md) holds each playbook's steps.

## 1. Set up the repo if needed

If `docs/sdlc/config` does not exist, run `setup` first. Say what it will
add, and ask one question: which tracker to use. If the config does not
list this device or harness, run only setup's model check. A new repo needs
no other command. In a repo that already has code, setup runs its
adoption path first; [playbooks.md](playbooks.md) lists its steps. Then route
the request as usual.

## 2. With no request: report and suggest

`/start` on its own lists, briefly:

- each piece of work in progress, with its next step;
- what waits at a gate for the user;
- open health batches from `code-health` and `architecture-health`;
- proposed definitions in `data-context`;
- the next intent in the backlog (`docs/sdlc/INTENTS.md`).

End by suggesting one thing to do.

## 3. A need, not work: name the skill

When the request asks for understanding, ideas or a judgement rather than a
change, name the skill instead of loading a playbook:

| The user brings | Skill |
|---|---|
| "I don't follow", or "what happened while I was away" | `huh` |
| How code works, or where something belongs | `how` |
| Why code is the way it is | `why` |
| What a dataset holds | `explore-data` |
| Why a number moved | `diagnose-metric` (an Incident runs it itself when an alert caught the drift) |
| A fact from outside the repo | `look-up` |
| Ideas, not yet an idea | `brainstorm` |
| An idea whose value is unclear | `size-impact`, before it becomes an intent |
| A message to send as themselves | `polish` |
| A document for people | `technical-writing` |
| "I'm stepping away" | `afk`, loaded for the rest of the run |

## 4. Work: classify and route

Match the request against the intents in `docs/sdlc/intents/`. It becomes a
new intent, an amendment, a duplicate, or a replacement for an older intent.
Show which, and let the user confirm. When `docs/sdlc/product.md` exists, flag
a request that serves no product outcome or guardrail as possible scope
creep; the user decides.

| The request brings | Playbook |
|---|---|
| Several new outcomes in an empty repo (a new product) | New application |
| Several new outcomes in an existing product, or the next milestone | New application, expansion variant |
| One new or changed outcome | Feature S, M or L, by size |
| Something behaving wrongly | Bug fix |
| A structure change with behaviour unchanged | Refactor |
| A question to answer, an option to explore, or an analysis whose answer decides something | Spike |
| An alert, a failed pipeline or metric drift | Incident |

Feature size:

| Size | Test |
|---|---|
| S | The diff fits in one sentence and the blast radius is small |
| M | A feature inside one area of the system |
| L | Several units, new architecture, or high risk: security, money, data contracts, model behaviour |

The user can override the route. State the route and the reason in one line.

**Resuming.** A request about work in progress, such as
`/start continue recurring payments`, resumes that change's playbook at its
next step, after reading its `handoff.md` if there is one. An intent already
accepted starts its Feature M or L playbook at `to-spec`; if a product
amendment has flagged it, grill it again first.

## 5. Load the playbook

Copy the playbook's steps from [playbooks.md](playbooks.md) into the task
list, in order. A step you skip stays in the list with a one-line reason.
Stop at each human gate the playbook names and wait for the user, unless the
run is AFK, in which case `afk` parks the gate.

A human gate exists only for preference calls no experiment can settle and
for irreversible or shared-state actions: merge to `main`, a production
deploy, migrations, data deletion, messages to people, and loosening any of
the agent's own controls. Everything else proceeds and reports evidence.

## Alerts

An alert hook sends its alert here. Route it to the Incident playbook.
