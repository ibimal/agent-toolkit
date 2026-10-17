# Playbooks

## Contents
- Rules for every playbook
- Feature S, Feature M, Feature L
- Bug fix, Refactor, Spike, Incident
- New application and its expansion variant
- The glossary in each playbook

## Rules for every playbook

- `implement` works per slice: `tdd` at the agreed seams, verify the slice,
  commit.
- Every grilling runs `glossary` alongside it, so a settled term lands in
  `GLOSSARY.md` at once.
- Review order: `tidy`, `verify-app`, `review-model` (when the change ships a
  model), then `review-change`, which runs `second-opinion` for rung 1 and
  `review-dependency` when packages change.
- Data work reads `data-context` before any query and writes back what it
  learns; `ship` adds what a merged change introduces.
- Parallel worktrees and AFK runs start only once CI, deploy, `verify-app`
  and the destructive-command guard exist.
- The change folder is `docs/sdlc/changes/C-NNNN-<slug>/`, numbered after
  the highest existing one.

## Feature S

Steps: `implement` (`tdd` where a seam exists) → `tidy` → `verify-app` →
`review-change` → `ship` → `codify` if there is a lesson.

Gate: merge. Artifact: the PR body, with a one-line intent and evidence. No
intent or spec files.

## Feature M

Steps: `grilling` (intent) → `to-intent` → `to-spec` → `grilling` (spec) →
`to-tickets` → `implement` → `tidy` → `verify-app` → `review-change` →
`ship` → `codify` → measure the success metric (`review-result`).

Gates: intent, spec, merge. The plan is a report, not a gate. Artifacts:
intent, `spec.md`, `plan.md`, PR.

## Feature L

Steps: `grilling` (intent) → `to-intent` → `to-spec` → `grilling` (spec) →
`prototype` (open questions) → `to-design` (with a threat model when the
change crosses a trust boundary) → `to-tickets` → `review-plan` →
`implement` in parallel worktrees → `tidy` → `verify-app` → `review-change`
→ `ship` (staged) → `codify` → measure the success metric (`review-result`).

Gates: intent, spec, design and plan, merge, production. One intent may
span several changes. Suggest `/wayfinder` when open decisions span
sessions; its map hands back to `to-spec` or `to-design`.

## Bug fix

Steps: `diagnose-bug` (reproduce on the same surface, minimise, hypothesise,
instrument) → a failing regression test → fix → find other instances of the
same cause → `verify-app` → `review-change` → `ship` → `codify`.

While the fix is in progress, add the regression test's path to
`docs/sdlc/locks`, so the guard blocks edits to it; remove the line once the
fix is verified. Gate: merge. Artifacts: `bugfix.md`, the regression test.

## Refactor

Steps: `blast-radius` → `to-tickets` (behaviour-preserving steps: migrate
callers, then delete the old API) → `implement` → `verify-app` (behaviour
unchanged) → `review-change` → `ship`.

Gate: merge. Artifact: `plan.md`.

## Spike

Steps: `grilling` (frame the question and agree the bar) → `explore-data`
(when data is involved) → `preregister` (when the answer is a number) →
`prototype` (a throwaway marimo notebook through `write-notebook`, or a
branch) → `review-result` → findings or an ADR → decide: stop, share the
findings, or re-enter as Feature M or L.

Gates: the bar, the decision. Artifacts: `findings.md` or an ADR, plus
`profile.md` and `preregistration.md` when used. Nothing ships.

## Incident

Steps: an alert from deterministic detection reaches `/start` → `diagnose-bug`
(read-only), or `diagnose-metric` when a metric drifted → a small fix
through Bug fix, or an agent-raised intent.

Gates: as routed. Artifacts: an incident note in
`docs/sdlc/incidents/YYYY-MM-DD-<slug>.md`, and a new eval case.

## New application

For a new product: an empty repo and several outcomes. It ends at the first
milestone release.

| Step | Skills | Exit criteria | Gate |
|---|---|---|---|
| 1 Setup, first pass | `setup` | Docs layout, tracker and reviewer ladder committed; `AGENTS.md`, `CLAUDE.md` and `REVIEW.md` stubs; guard active; no empty glossary | — |
| 2 Product brief | `grilling` (product level) → `to-product` | `product.md` complete, with the MVP defined by the outcome it proves; `GLOSSARY.md` created with the first settled terms | Brief accepted |
| 3 Backlog | `to-backlog` → `size-impact` (when intents compete for the cut) → `grilling` and `to-intent` for each MVP intent → `review-plan` (scope challenge on the MVP) | Every MVP intent accepted, traced to an outcome, with a success metric and dependencies; later intents proposed in one line; open technical decisions listed | MVP intents, cut and order |
| 4 Architecture | a Spike, or `/wayfinder` tickets, for each decision expensive to reverse → ADR; `to-design` (system) → `review-plan` | Every open decision resolved by an ADR or deferred with a reason; `architecture.md` complete; every product constraint maps to a choice | Architecture accepted |
| 5 Walking skeleton | `setup` (stack pass) → `to-spec` (thinnest slice of the first MVP intent) → `to-tickets` → `implement` (one stream; writes `verify-app`) → `tidy` → `verify-app` → `review-change` → `ship` to staging | One command builds and tests from a clean clone; CI green; staging deploy and rollback each run once; hooks active; agent-readiness check passes | Spec, merge |
| 6 Build | `/start` for each MVP intent in dependency order → Feature S, M or L | All MVP intents merged; living specs and `architecture.md` current | Per playbook |
| 7 Release | `release-readiness` → `ship` to production (staged) → measure (`review-result`) | Readiness check passes; post-deploy check passes; MVP intents move to measuring; milestone review scheduled | Production |

Rules:
- Each capability intent is an outcome a user or operator would notice.
  "Build the API" is not an intent.
- Only MVP intents are grilled up front; later intents stay proposed with a
  one-line outcome.
- The backlog comes before the architecture, and the architecture serves the
  MVP intents.
- Spike only what is expensive to reverse: runtime and framework, primary
  data store and core data model, identity and tenancy, hosting and
  deployment, external contracts, and any model component. Everything else
  gets a sensible default recorded as a provisional ADR.
- The skeleton is the thinnest real slice of the first MVP intent, deployed
  end to end. If the riskiest assumption is about the architecture, build it
  through the target architecture; if it is about value, put the real
  interface over stand-in services.
- Agent-readiness check: a fresh session, given only the repo, states the
  commands, conventions and architecture and runs `verify-app`. Keep it as
  the first eval case.
- In step 6, independent intents run in parallel worktrees, capped by how
  many the user can review properly.
- After the release, the milestone review measures the product metrics,
  runs both `-health` skills as a full sweep, amends `product.md` and the
  backlog, and sizes the next milestone's candidates with `size-impact`.

**Expansion variant** (a major new area, or the next milestone): step 2 as
an amendment to `product.md` → step 3 for the new area → step 4 only if the
area needs new architecture → steps 6 and 7. If the repo has no product
brief, `setup` drafts one from the code and docs first.

## The glossary in each playbook

| Playbook | Glossary |
|---|---|
| New application | Created while grilling the brief; grows with every grilling |
| Expansion variant | The new area's terms are added while the brief is amended |
| Feature S | Read only; a needed new term is proposed and confirmed before merge |
| Feature M | Updated while grilling the intent and the spec |
| Feature L | Updated while grilling, and when `to-design` or a wayfinder ticket names a new concept |
| Bug fix | Read; if the cause was one word used two ways, `codify` settles the word |
| Refactor | Read; a rename changes the glossary first, and the old word moves to _Avoid_ |
| Spike | Updated while framing the question, and when the findings name something new |
| Incident | Read; the incident note uses its terms |
