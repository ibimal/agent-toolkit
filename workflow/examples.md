# AI-native SDLC: playbook examples

Worked examples of every playbook in the workflow doc ([ai-native-sdlc.md](ai-native-sdlc.md)) and of the skills outside a playbook's fixed steps: the skills around the playbooks, the everyday skills and the data skills, all on one running product. The same examples play as animated walkthroughs in [walkthroughs.html](walkthroughs.html). This file and the page are generated: edit `src/examples_data.py`, then run `python3 workflow/src/build.py`.

---

## The running example

**Household finance app.** A web app that turns bank statements into a clear picture of where a household's money goes.

- **Users:** Individuals and couples in India running a household budget
- **Outcomes:** O1 Know where the money goes · O2 Stay within monthly budgets · O3 Catch unusual spending early
- **Guardrails:**
  - G1 Raw statements deleted after import; account numbers masked before any external call
  - G2 At least 90% of transactions need no category edit
  - G3 Monthly view loads in under 2 s (p95)
  - G4 Model calls cost at most ₹5 per active user per month
- **Riskiest assumption:** Auto-categorisation is accurate enough on Indian bank statements that people stop fixing categories by hand.
- **Milestones:** M1 (MVP) See your money: proves O1 · M2 Budgets: proves O2 · M3 Alerts: proves O3

---

## How each request reaches its playbook

| You bring | Router reasoning | Playbook |
|---|---|---|
| `/start I want to build a household finance app that shows people where their money goes` | Backlog: Empty repo, no product brief · Outcomes: Several: import, categorise, monthly view, budgets, alerts | New application |
| `/start Let couples manage their money together` | Backlog: No match: a new area · Outcomes: Several: invite a partner, combined view, split expenses · Repo: Existing product with a brief | Expansion variant |
| `/start Parse Bank E's new statement format` | Repo: Existing code, tests and CI; no docs/sdlc/config · Instruction files: A two-year-old CLAUDE.md; no AGENTS.md · Tracker: GitHub Issues, 23 open | Adoption |
| `/start Show amounts in Indian number format, like ₹1,24,560` | Backlog: Part of I-0003 Monthly spending · Outcomes: One · Type: Feature · Size: S: one formatter, a one-sentence diff | Feature S |
| `/start Show me all my recurring payments in one place` | Backlog: No match: new intent · Outcomes: One · Type: Feature · Size: M: one area (transactions) | Feature M |
| `/start Sync my bank accounts automatically instead of uploading statements` | Backlog: Related to I-0001, but a new outcome: new intent · Outcomes: One · Type: Feature · Size: L: external contract, consent and security, a new sync service · Sizing: Go, one bank first (docs/sdlc/sizing/bank-sync.md) | Feature L |
| `/start Payments late on 31 January show up in February` | Backlog: Breaks I-0003 Monthly spending · Type: Behaving wrongly | Bug fix |
| `/start Split the statement parser into one adapter per bank` | Source: Raised by architecture-health, started by the merge hook · Backlog: Serves I-0001: makes new banks cheaper · Type: Structure change, behaviour unchanged | Refactor |
| `/start Could a small local model replace the LLM fallback for categorising?` | Type: A question to answer · Serves: G4 cost and G1 privacy | Spike |
| `/start Alert: parse failures 31% (baseline 2%)` | Source: Sent by the alert hook; no one types it · Type: Incident | Incident |

The router also runs for each intent in a backlog, for each incident or review finding, and at each milestone.

## The skills outside the playbooks

Grouped by the moment you need them, as in the workflow doc's quick reference. Each starts its own way: you type it, the agent starts it, or a hook or another skill does. `/start` points you to the right one when your input is a need rather than work.

| Moment | Skill | How it starts | When | Example |
|---|---|---|---|---|
| Stay on track | `huh` | You type it, with nothing after it | You don't follow the agent's last message or the question it asks you. | A grilling question you can't parse |
| Stay on track | `huh` | You type it, with nothing after it | You come back to a long session and need to know what changed for you. | Back from lunch mid-session |
| Stay on track | `readback` | You type it | Before the agent builds, you want to be sure it understood you. | Check the goal before an AFK run |
| Stay on track | `handoff` | You type it; the agent suggests it when the context runs long | You stop part-way through a playbook, or the session's context is getting long. | Pause and switch devices |
| Stay on track | `afk` | /start loads afk | Nobody will watch the run: you say you're stepping away or type /afk, or a hook or scheduled task starts it. | Overnight MVP build |
| Understand | `how` | You type it | You need to know how code works, or where something belongs. | How a statement becomes transactions |
| Understand | `why` | You type it | You need to know why code is the way it is. | Why monthly totals are pre-aggregated |
| Understand | `explore-data` | You type it; the agent starts it when a new dataset arrives | A dataset arrives that nobody has looked at properly yet. | A new bank's export |
| Understand | `data-context` | The agent: before its first query, then whenever new facts about the data appear | The agent queries data that has no map yet, or any work brings new facts about the data. | Map the warehouse, then keep it current |
| Understand | `diagnose-metric` | You type it; Incidents and measure steps start it too | A metric moved and you need to know why before anyone acts on it. | Engagement fell 7 points in March |
| Understand | `write-notebook` | The agent, whenever it writes or touches a notebook | The agent writes a notebook, or touches an old Jupyter one. | The broken evaluation notebook |
| Understand | `look-up` | You type it; the agent and wayfinder start it too | A decision waits on a fact you'd have to read up on. | The aggregator's sync limits |
| Understand | `learn` | You type it, in a learning folder | You want to learn a topic properly, over several sessions. | Learning Postgres row-level security |
| Decide | `brainstorm` | You type it | You need ideas, not yet an idea: a new project, a feature area, an improvement plan. | More households back for a second month |
| Decide | `wayfinder` | You type it; Feature L suggested it | Open decisions need more than one session before a spec or design can be written. | Bank sync's open decisions |
| Decide | `size-impact` | You type it; milestone planning runs it too | Before deciding whether something is worth building, or when choosing between options at planning. | Is bank sync worth building? |
| Decide | `preregister` | You type it; Spike and experiments start it too | Before an experiment, A/B test or model comparison decides something. | Does a reminder raise account linking? |
| Share | `to-questionnaire` | You type it | You can't answer a question, but someone else can. | Token retention, asked of the privacy lead |
| Share | `technical-writing` | You type it | A doc, README, RFC or PR description is for people to read. | A PR description read in one pass |
| Share | `polish` | You type it, with your draft after it | A message, email, comment or post you wrote, before you send it as yourself. | The engagement finding, for the product lead |
| Share | `make-chart` | The agent, whenever it makes a chart; or you | Any chart: for a readout, a PR or a dashboard. | The engagement readout's chart |
| Check | `second-opinion` | You type it; review-change and review-plan run it too | You want another model family's view on a diff, a plan or an idea. | Is the de-duplication rule safe? |
| Check | `review-result` | The agent, before reporting the success metric | Before a number, chart or analysis is reported or decides anything. | Did bank sync hit its target? |
| Check | `review-model` | The agent, in the change that ships a model, before review-change | A change ships or replaces a model. | Adopting the local categoriser |
| Check | `review-dependency` | review-change, when the lockfile changes | A change adds or upgrades a package, or a release is being prepared. | A new package in the timezone fix |
| Check | `review-feedback` | You type it; the agent starts it on review-change findings | Review findings or PR comments arrive. | A teammate's PR comments |
| Check | `fix-ci` | The agent, inside ship; or you | A CI check fails. | A latency test fails only in CI |
| Improve | `architecture-health` | You; the merge hook (first); milestone reviews | The code is getting hard to change. | Structure review |
| Improve | `code-health` | You; the merge hook (second); milestone reviews | Code, docs, comments or names feel out of date. | Drift and decay check |
| Improve | `retro` | You type it | A long or messy session just ended. | After a slow session |
| Improve | `to-skill` | You type it | You keep asking for the same workflow and want it repeatable. | Monthly release notes as a skill |
| Improve | `review-skill` | Every skills sync and to-skill; or you | You adopt a skill, or sync your forks from upstream. | A monthly skills sync |

---

## 1. New application: Household finance app MVP

**When:** An empty repo and several outcomes.

**You bring:** `/start I want to build a household finance app that shows people where their money goes`

**Router:** Backlog: Empty repo, no product brief · Outcomes: Several: import, categorise, monthly view, budgets, alerts → **New application**

**Your decisions:** Brief · MVP intents, cut and order · Architecture · Skeleton spec and merge · each intent's own gates · Prod

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | setup | Setup, first pass | The repo has no docs/sdlc/config, so /start runs setup before anything else and asks one question: which tracker to use. It creates the docs layout, records local files as the tracker, detects the reachable models, writes the reviewer ladder and installs the destructive-command guard. No stack is chosen yet. | Choose the tracker: local files. | — |
| 2 | grilling + glossary → to-product | Product brief | Grills you in rounds, each question with a recommended answer: who it is for, what they can't do today, how you'd know it works, what it must never do. Creates GLOSSARY.md with its first terms: statement, transaction and category. | Answer, correct the draft, accept the brief. | Brief accepted |
| 3 | to-backlog | Propose the backlog | Splits the brief into capability intents, each something a user would notice, with dependencies and a milestone. Seeds a wayfinder map with the open technical decisions: categoriser, PDF parsing, data store. | — | — |
| 4 | grilling → to-intent | Grill each MVP intent | Grills I-0001 to I-0004 only, and each term they settle joins GLOSSARY.md. Budgets and alerts stay as one-line proposals until they are picked up. | Accept each MVP intent. | — |
| 5 | review-plan | Challenge the MVP scope | A reviewer from another model family challenges the cut (expand, hold or reduce). It proposes dropping PDF statements from the MVP; you keep them because most Indian banks email PDFs. | Decide the cut and the order. | MVP intents, cut and order |
| 6 | Spike ×3 → ADRs | Spike what is expensive to reverse | Throwaway prototypes for the categoriser (rules vs small model vs LLM on 2,000 labelled transactions), PDF parsing on statements from five banks, and the data store. Cheap choices such as the chart library get provisional ADRs. | — | — |
| 7 | grilling → to-design → review-plan | Write the architecture | First grills what the brief and the spikes leave open: where to host (in India, because statements are personal data) and how much the categoriser may cost per user (G4). Then writes architecture.md: web front end, Python API, parser adapters, categoriser service, Postgres, staging and prod. Every guardrail maps to a choice. Reviewed through the ladder. | Accept the architecture. | Architecture accepted |
| 8 | setup (stack pass) | Setup, second pass | With the stack chosen, the playbook runs setup's second pass: the AGENTS.md commands, format and lint hooks, the verify command, the health checks behind make health, REVIEW.md standards and CI. It only adds controls, so it needs no gate. | — | — |
| 9 | to-spec → implement → ship | Build the walking skeleton | The riskiest assumption is about the categoriser, an architecture question, so the skeleton runs through the target architecture: upload one bank's CSV, parse, categorise with a single rule, store, list on a page, deploy to staging. verify-app is written alongside it. | Approve the slice spec, then merge. | Spec, merge |
| 10 | agent-readiness check | Check the repo is agent-ready | A fresh agent session, given only the repo, states the commands, conventions and architecture and runs verify-app green. The check becomes the first eval case. Parallel work is now allowed. | — | — |
| 11 | start × 4 | Build the MVP intents | The router takes each MVP intent in dependency order: the rest of I-0001 (more banks, PDFs) as Feature M, I-0002 as Feature L because it is model behaviour, then I-0003 and I-0004 as Feature M in parallel worktrees. | — | Each playbook's gates |
| 12 | release-readiness → ship | Release the MVP | Checks every guardrail across the app: statements deleted, masking verified, 91.4% on the eval set, monthly view p95 1.4 s, a backup restored, rollback rehearsed, parse-failure alert live. Then a staged prod release. | Authorise prod. | Prod |
| 13 | milestone review | Review the milestone | Four weeks later: 64% of users uploaded a second month and 7% of transactions were edited, so G2 holds. review-result confirms the 64% counts only users old enough to have had a second month. Both -health skills run a full sweep and their findings join the backlog, size-impact sizes the candidates for M2 (bank sync among them; see its example), product.md is amended and M2 Budgets runs as the expansion variant. | — | — |

**Artifacts**

`docs/sdlc/config`
```
tracker: local files
reviewer rung 1: another model family via its CLI
reviewer rung 2: strongest same-family model, +1 effort
```
`docs/sdlc/product.md`
```
Users: individuals and couples running a household budget
O1 Know where the money goes
O2 Stay within monthly budgets
O3 Catch unusual spending early
G1 Statements deleted after import; numbers masked
Riskiest: auto-categorisation accurate enough to trust
M1 (MVP) proves O1
```
`docs/sdlc/INTENTS.md`
```
M1  I-0001 Import a bank statement
M1  I-0002 Auto-categorise transactions  ← I-0001
M1  I-0003 Monthly spending by category ← I-0002
M1  I-0004 Fix a category, remembered    ← I-0002
M2  I-0005 Monthly budgets          (proposed)
M3  I-0007 Unusual-spend alerts     (proposed)
```
`docs/sdlc/intents/I-0002-auto-categorise.md`
```
Serves: O1, G2
Outcome: most transactions arrive correctly categorised
Metric: 90% need no edit in a user's first month
Non-goals: categorising cash spending
```
`docs/sdlc/adr/0003-categoriser.md`
```
Decision: rules first, LLM fallback on masked text
Evidence: 91.4% on the eval set (rules alone 72%)
Cost: ₹2.10 per user per month (G4 allows ₹5)
Eval set and 90% threshold join verify-app
```
`docs/sdlc/architecture.md`
```
Upload → Parser → Categoriser → Postgres → Monthly view
G1 → statements deleted after parse; masking before LLM
G3 → monthly totals pre-aggregated
Verify: browser upload of fixtures + eval set
```
`docs/sdlc/changes/C-0001-skeleton/spec.md`
```
Intent: I-0001 (rev 2), thinnest slice
Given a Bank A CSV with 42 rows
When I upload it
Then I see 42 transactions, newest first
```

**What it shows:** A big build is a short series of gated decisions: brief, MVP, architecture, skeleton. After the skeleton, the router drains the backlog one intent at a time.

---

## 2. Expansion variant: Shared household accounts

**When:** A major new area in an existing product, or the next milestone.

**You bring:** `/start Let couples manage their money together`

**Router:** Backlog: No match: a new area · Outcomes: Several: invite a partner, combined view, split expenses · Repo: Existing product with a brief → **New application, expansion variant**

**Your decisions:** Brief amendment · Milestone intents, cut and order · Architecture · each intent's own gates · Prod

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | grilling → to-product | Amend the brief | Grills the new area and adds outcome O4 Manage money as a household, plus guardrail G5: each person chooses which accounts they share. Household, member and shared account join the glossary. | Accept the amendment. | Brief accepted |
| 2 | to-product | List the affected intents | Flags I-0003 (monthly view) and I-0005 (budgets): both assume one person per account. | Re-accept I-0003 as it is; amend I-0005 to allow shared budgets. | — |
| 3 | to-backlog → grilling | Backlog for the new area | Proposes and grills the milestone's intents. They take the place of the MVP. | Decide the cut and the order. | Milestone intents, cut and order |
| 4 | Spike → to-design | Architecture for the area | Needed here: the data model moves from one owner per account to households with members, which is expensive to reverse. A spike tests row-level security in Postgres; ADR 0009 records it and architecture.md is updated. | Accept the architecture. | Architecture accepted |
| 5 | start × 3 | Build the intents | I-0012 as Feature L (identity and permissions), then I-0013 and I-0014 as Feature M. | — | Each playbook's gates |
| 6 | release-readiness → ship | Release | Adds G5 to the readiness check: a test proves one partner cannot see the other's unshared accounts. | Authorise prod. | Prod |

**Artifacts**

`docs/sdlc/product.md`
```
+ Users: couples sharing a household
+ O4 Manage money as a household
+ G5 Each person controls what they share
+ Milestone Households proves O4
```
`docs/sdlc/INTENTS.md`
```
Households  I-0012 Invite a partner
Households  I-0013 Combined household view ← I-0012
Households  I-0014 Split shared expenses   ← I-0013
```

**What it shows:** An existing product grows by amending the brief, not by writing one giant spec. Setup and the skeleton are skipped because the repo is already agent-ready.

---

## 3. Adoption: The statement parser adopts the workflow

**When:** The first /start in a project that already has code but no docs/sdlc/config.

**You bring:** `/start Parse Bank E's new statement format`

**Router:** Repo: Existing code, tests and CI; no docs/sdlc/config · Instruction files: A two-year-old CLAUDE.md; no AGENTS.md · Tracker: GitHub Issues, 23 open → **Adoption through setup, then the request routes**

**Your decisions:** Tracker · Brief · Architecture · which health batches to pick · then the request's own gates

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | setup | Say what it adds | Lists what adoption adds and asks one question. The repo already uses GitHub Issues, so it stays the tracker and its 23 open issues stay there; none is converted. | Keep GitHub Issues. | — |
| 2 | setup | Merge the instruction files | The old CLAUDE.md names a test folder that no longer exists. Its content moves into AGENTS.md beside the commands setup found in the Makefile and CI, and CLAUDE.md now holds @AGENTS.md. The stale command is fixed, and the diff is in the setup report. | — | — |
| 3 | setup | Controls and standards | Installs the guard, and puts the ruff, mypy and pytest runs the repo already has behind make health. REVIEW.md starts from the baseline and records what the code already follows. Existing CI stays and gains a health job. | — | — |
| 4 | setup → verify-app | Prove it runs | Writes verify-app from the existing fixtures: it parses three sample statements end to end and checks their totals. It passes from a clean clone. | — | — |
| 5 | setup → grilling → to-product | Draft the brief from what exists | Drafts the brief from the README, the code and the open issues, describing the service as it is. The grilling settles statement, format version and adapter, which start the glossary. | Accept the brief. | Brief accepted |
| 6 | setup → grilling → to-design | Draft the architecture as it is | Drafts architecture.md from the code: a queue consumer, one adapter per bank behind a common interface, and a normaliser. The code cannot show intent, so the grilling asks two things: is Bank C's adapter, which skips the normaliser, deliberate (no, a workaround to remove), and must the consumer scale out (yes, at month end). Two existing decisions are hard to reverse and surprising, so they become ADRs. | Accept the architecture. | Architecture accepted |
| 7 | architecture-health → code-health | Baseline health sweep | Both run a full sweep, so the health ledger starts with every area at today's commit. Nothing is changed; the findings wait for your pick. | — | — |
| 8 | agent-readiness | Agent-readiness check | A fresh session, given only the repo, states the commands, conventions and architecture, and runs verify-app. It passes, but the service has no deploy command yet, so parallel worktrees and AFK runs wait; the setup report lists it. | — | — |
| 9 | start | Back to the request | Bank E's format is one new adapter behind the existing interface, so the router picks Feature S. The old issues still wait in GitHub; each becomes an intent or a Bug fix only when /start picks it up. | — | Feature S: merge |

**Artifacts**

`AGENTS.md`
```
Build: make build
Test: make test   (was: pytest tests/unit, folder removed)
Health checks: make health
Verify end to end: the verify-app skill
```
`docs/sdlc/config`
```
tracker = "github"
health_command = "make health"
verify_command = "make verify"
```
`docs/sdlc/product.md`
```
Users: the household app's import pipeline
O1 Every supported bank's statements parse without manual fixes
G1 Raw statements deleted after import
Non-goal: categorising transactions (the app does that)
```
`docs/sdlc/architecture.md`
```
Components: queue consumer → bank adapters → normaliser
Areas: consumer, adapters, normaliser, docs
ADR 0001 One format version per bank
ADR 0002 Raw files stay in memory, never on disk
Known workaround: Bank C bypasses the normaliser
```
`docs/sdlc/health-ledger.md`
```
adapters: six adapters copy the same date logic (escalated to architecture-health)
docs: the README lists a bank that is no longer supported
normaliser: two tests pass even if the function returns nothing
3 batches proposed, 0 picked
```

**What it shows:** Adoption describes the project as it is before anything changes: setup merges instead of overwriting, the brief and the architecture are drafted from the code for you to accept, and a full health sweep gives every later run a baseline. Then work routes as usual.

---

## 4. Feature S: Indian number format

**When:** One outcome; the diff fits in one sentence.

**You bring:** `/start Show amounts in Indian number format, like ₹1,24,560`

**Router:** Backlog: Part of I-0003 Monthly spending · Outcomes: One · Type: Feature · Size: S: one formatter, a one-sentence diff → **Feature S**

**Your decisions:** Merge

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | implement + tdd | Implement | A formatter seam exists, so the tests come first, then the change. | — | — |
| 2 | tidy | Tidy | Finds two older places that format money by hand and routes them through the formatter. One helper still used txn, a word the glossary says to avoid, so tidy renames it. | — | — |
| 3 | verify-app | Verify | Uploads the fixture statement and checks that every amount on the monthly view uses the new format. | — | — |
| 4 | review-change | Review | Two axes in separate subagents. Rung 1 runs through second-opinion, which asks Codex. One finding: negative amounts used a hyphen instead of a minus sign. Fixed. | — | — |
| 5 | ship | Ship | The PR body carries a one-line intent linked to I-0003, the evidence and the reviewer rung. | Merge. | Merge |
| 6 | codify | Record the lesson | Money was formatted in three places. The lesson becomes a lint rule: currency must go through format_inr. | — | — |

**Artifacts**

`tests/test_format_inr.py`
```
format_inr(124560)  → ₹1,24,560
format_inr(1000)    → ₹1,000
format_inr(-2500.5) → −₹2,500.50
```
`PR #71`
```
Intent: amounts readable in Indian format (I-0003)
Evidence: 14 tests, verify-app green, screenshot
Review: rung 1, other family; 1 finding fixed
```

**What it shows:** No intent or spec files. The PR carries a one-line intent and the evidence, and the lesson became a lint.

---

## 5. Feature M: Recurring payments

**When:** One outcome inside one area of the system.

**You bring:** `/start Show me all my recurring payments in one place`

**Router:** Backlog: No match: new intent · Outcomes: One · Type: Feature · Size: M: one area (transactions) → **Feature M**

**Your decisions:** Intent · Spec · Merge

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | grilling + glossary | Grill the intent | What counts as recurring? Why do you want it: to cancel things, or to plan the month? You say to plan the month, so cancelling becomes a non-goal. The two terms you settle go into the glossary at once. | — | — |
| 2 | to-intent | Write the intent | Writes the intent and links it to the product outcome it serves. | Accept the intent. | Intent accepted |
| 3 | to-spec | Draft the spec | Drafts the behaviour and acceptance criteria, pinned to the intent revision. | — | — |
| 4 | grilling (spec) | Grill the spec | Edge cases: electricity bills vary by more than 10%, some recurring payments come once a year, EMIs end. The spec gains a variable-amount rule and an end date for EMIs. | Approve the spec. | Spec approved |
| 5 | to-tickets | Slice it | Three vertical slices with their test seams. On Feature M the plan is a report, not a gate. | — | — |
| 6 | implement | Build slice by slice | For each slice: tests at the agreed seam, verify the slice, commit. | — | — |
| 7 | tidy | Tidy | Removes a duplicate merchant-normalising helper in favour of the one the categoriser already uses. | — | — |
| 8 | verify-app | Verify | Uploads six months of fixture statements and checks that Netflix, rent and an EMI appear and a one-off flight does not. | — | — |
| 9 | review-change | Review | The spec axis catches that EMIs past their end date still show. Fixed before merge. | — | — |
| 10 | ship | Ship | PR with intent, evidence and reviewer rung. | Merge. | Merge |
| 11 | codify | Record the lesson | The variable-amount rule will be needed again for budgets, so it is noted in docs/solutions/. | — | — |
| 12 | measure (review-result) | Measure the success metric | Two months after release, 43% of monthly users open the page each month. review-result counts every monthly user, as the intent's metric says, rather than only those with enough history to have a recurring payment, which would flatter the number; test accounts are excluded as data-context defines them. Target met, so I-0008 moves to done. | — | — |

**Artifacts**

`GLOSSARY.md`
```
**Recurring payment**:
A payment to the same payee at a regular interval, whatever its amount.
_Avoid_: subscription, repeat payment
**EMI**:
A fixed monthly instalment that repays a loan and ends on a known date.
_Avoid_: loan payment
```
`docs/sdlc/intents/I-0008-recurring-payments.md`
```
Serves: O1 Know where the money goes
Outcome: see every recurring payment and its next date
Metric: 40% of monthly users open it each month
Non-goals: cancelling recurring payments
```
`docs/sdlc/changes/C-0014-recurring/spec.md`
```
Intent: I-0008 (rev 1)
Given a merchant charged in 3+ consecutive months
  within ±10% of the same amount
Then it is listed as recurring with its next date
```
`docs/sdlc/changes/C-0014-recurring/plan.md`
```
1 Detect recurring payments (tdd at the detector)
2 Recurring list page          ← 1
3 Mark as not recurring        ← 2
```

**What it shows:** The two grilling passes do different jobs: the first settles why (planning, not cancelling); the second finds edge cases (variable bills, EMIs that end). The intent stays open until its metric has been measured and checked.

---

## 6. Feature L: Automatic bank sync

**When:** One outcome with several units, new architecture, or high risk.

**You bring:** `/start Sync my bank accounts automatically instead of uploading statements`

**Router:** Backlog: Related to I-0001, but a new outcome: new intent · Outcomes: One · Type: Feature · Size: L: external contract, consent and security, a new sync service · Sizing: Go, one bank first (docs/sdlc/sizing/bank-sync.md) → **Feature L**

**Your decisions:** Intent · Spec · Design + plan · Merge · Prod

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | grilling + glossary | Grill the intent | Pins down the terms that will matter: consent, linked account, sync window. All three go into GLOSSARY.md, each with the synonyms to avoid. | — | — |
| 2 | to-intent | Write the intent | Writes the intent with its outcome, metric and constraint. | Accept the intent. | Intent accepted |
| 3 | to-spec | Draft the spec | Covers linking an account, daily sync, de-duplication against uploaded statements and revoking consent. | — | — |
| 4 | grilling (spec) | Grill the spec | What if someone uploads a statement for a month that was already synced? The spec de-duplicates on date, amount and reference. | Approve the spec. | Spec approved |
| 5 | prototype | Answer the open questions | A throwaway script against the aggregator's sandbox shows merchant names arrive in a different shape than in statements, so the categoriser needs a normalising step. | — | — |
| 6 | to-design | Design the change | Writes the change's design, an ADR and, because the change handles bank credentials, a threat model. | — | — |
| 7 | to-tickets | Slice it | Vertical slices with blocking edges. | — | — |
| 8 | review-plan | Review design and plan | Only one model family is available in this harness, so rung 2 applies: the strongest same-family model at one effort level above the writer's. Scope challenge: reduce, one bank first. | Accept the design and plan. | Design + plan |
| 9 | implement (parallel) | Build in parallel | Slices 2 and 4 share no files, so they run in separate worktrees. | — | — |
| 10 | tidy → verify-app | Tidy and verify | verify-app links a sandbox account, runs a sync and checks that no transaction appears twice. | — | — |
| 11 | review-change | Review | The standards axis finds a consent token written to a debug log, fixed before merge. review-dependency passes the aggregator's SDK: published by the aggregator, maintained, no advisories. | — | — |
| 12 | ship (staged) | Ship in stages | Staging, then 10% of users, then everyone, with a post-deploy check at each stage. | Merge, then authorise prod. | Merge, prod |
| 13 | codify → measure (review-result) | Learn and measure | The logging slip becomes a hook that blocks logging any field named token. After 60 days the raw count says 47% have linked an account. review-result finds it includes users who have had sync for less than 60 days; counted fairly it is 53%, so I-0009 moves to done. The 53% lands inside the sizing's 30–60% adoption range and is recorded there. | — | — |

**Artifacts**

`GLOSSARY.md`
```
**Consent**:
Time-limited permission to read one bank account.
_Avoid_: permission, authorisation
**Linked account**:
A bank account the app is allowed to sync.
_Avoid_: connected bank, integration
```
`docs/sdlc/intents/I-0009-bank-sync.md`
```
Serves: O1, G1
Outcome: transactions arrive without uploading
Metric: 50% of active users link an account in 60 days
Constraint: consent can be revoked at any time
```
`docs/sdlc/changes/C-0020-bank-sync/design.md`
```
New: daily sync worker, consent store
Tokens encrypted at rest, never logged
Normaliser runs before the categoriser
Threat model: leaked token, consent not revoked in time, spoofed callback
ADR 0011: aggregator API, not screen scraping
```
`docs/sdlc/changes/C-0020-bank-sync/plan.md`
```
1 Link one sandbox account
2 Daily sync + normaliser  ← 1
3 De-duplicate vs uploads  ← 2
4 Revoke consent           ← 1
```

**What it shows:** Prototype before designing, review the design and plan together, release in stages, and keep the intent open until its metric is checked, and the check itself checked.

---

## 7. Bug fix: Month-end timezone bug

**When:** Something behaving wrongly.

**You bring:** `/start Payments late on 31 January show up in February`

**Router:** Backlog: Breaks I-0003 Monthly spending · Type: Behaving wrongly → **Bug fix**

**Your decisions:** Merge

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | diagnose-bug | Reproduce and narrow down | Reproduces on the same surface: uploads a statement with a payment at 23:10 IST on 31 Jan and opens January; it is missing. Minimises to the month-bucketing code and instruments it. | — | — |
| 2 | tdd | Write the failing test | A regression test for the 23:10 case fails for the expected reason, plus a property test: every transaction lands in exactly one month, in any timezone. Its path goes into docs/sdlc/locks, so the guard blocks edits to it until the fix is verified. | — | — |
| 3 | fix | Fix | The parser stores times with the statement's timezone, using the standard library's zoneinfo. The agent's first attempt added a timezone package; review-dependency turned it down (see its example). | — | — |
| 4 | diagnose-bug | Find other instances | Searches for the same cause elsewhere: the recurring-payment detector also builds naive datetimes, in two places. Both are fixed in the same change, each with a test. | — | — |
| 5 | verify-app | Verify | Re-uploads the fixture: the January total is now ₹48,920, matching the bank. | — | — |
| 6 | review-change | Review | The spec axis checks the must-not-change rule still holds. | — | — |
| 7 | ship | Ship | PR linked to I-0003 with the failing-then-passing test as evidence. | Merge. | Merge |
| 8 | codify + glossary | Record the lesson | A lint now rejects naive datetimes anywhere in the code, not just the parser. The cause was one word used two ways: the parser read a transaction's time as UTC, the monthly view as local time. The glossary settles it. | — | — |

**Artifacts**

`docs/sdlc/changes/C-0017-month-end/bugfix.md`
```
Current: 23:10 IST on 31 Jan counted in February
Expected: counted in January
Must not change: dates without a time keep their date
Cause: local times stored as UTC, then shifted +5:30
```
`GLOSSARY.md`
```
**Transaction time**:
When a transaction happened, in the statement's own timezone. It decides the month.
_Avoid_: timestamp
```

**What it shows:** Reproduce on the real surface first. The regression test is written and locked before the fix, and the same cause is hunted down everywhere else before shipping.

---

## 8. Refactor: One adapter per bank

**When:** Structure changes; behaviour must not.

**You bring:** `/start Split the statement parser into one adapter per bank`

**Router:** Source: Raised by architecture-health, started by the merge hook · Backlog: Serves I-0001: makes new banks cheaper · Type: Structure change, behaviour unchanged → **Refactor**

**Your decisions:** Merge

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | blast-radius | Check what could break | parse_statement is called from upload, the sync worker and two tests. 41 golden fixture outputs pin today's behaviour. | — | — |
| 2 | to-tickets | Plan behaviour-preserving steps | Small steps, each leaving the system working. | — | — |
| 3 | implement | Move one bank at a time | Every commit keeps all 41 golden outputs identical. Each adapter is named for the statement format it reads, the glossary's term. | — | — |
| 4 | verify-app | Prove nothing changed | All fixture statements parse to exactly the same output, and the monthly totals match. | — | — |
| 5 | review-change | Review | Here the spec axis means no behaviour change: it confirms no golden file was edited. | — | — |
| 6 | ship | Ship | PR linked to I-0001. | Merge. | Merge |

**Artifacts**

`docs/sdlc/changes/C-0022-bank-adapters/plan.md`
```
1 Introduce the BankAdapter interface
2 Move banks A–C behind it, one per commit
3 Migrate callers to the adapter registry
4 Delete the old parse_statement
```

**What it shows:** Golden outputs make 'behaviour unchanged' checkable. The payoff shows up in the incident example: adding a bank is now one file.

---

## 9. Spike: Local categoriser model

**When:** A question to answer or an option to explore.

**You bring:** `/start Could a small local model replace the LLM fallback for categorising?`

**Router:** Type: A question to answer · Serves: G4 cost and G1 privacy → **Spike**

**Your decisions:** The bar · The decision

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | grilling | Frame the question and agree the bar | The bar is set before any experiment: within 2 points of today's 91.4%, under ₹1 per user per month, under 300 ms per batch. | Agree the bar. | The bar |
| 2 | preregister | Write the plan before running anything | The answer is a number, so the plan is written down first, including whether the eval set can tell the models apart. | — | — |
| 3 | prototype | Run the experiment | A marimo notebook compares the current LLM fallback with a small local model on the 2,000-transaction eval set; write-notebook first converts the old evaluation notebook it starts from. | — | — |
| 4 | review-result | Check the numbers before trusting them | Checks the result against the preregistration. The merchant counts behind 'seen 5+ times' were built from all the data, eval set included, so the hybrid had seen the test. Rebuilt from the training months only and run three times as planned, it still clears the bar. Verdict: ready. | — | — |
| 5 | ADR + glossary | Record the finding | ADR 0014: use the local model for frequent merchants and keep the LLM for the rest. Frequent merchant joins the glossary: a merchant seen five or more times in the training months, so the eval set never shapes it. | — | — |
| 6 | decide | Decide | The hybrid clears the bar, so it re-enters as Feature M through a new intent, I-0010 Local categoriser for frequent merchants. | Decide: stop, share the findings, or re-enter as M or L. | The decision |

**Artifacts**

`docs/sdlc/changes/C-0025-local-model/preregistration.md`
```
Decision: replace the LLM fallback if all three bars are met
Design: the same 2,000 transactions for every model, three runs each
Power: a 2-point gap is detectable (0.89); a 1-point gap is not (0.35)
Analysis: paired comparison (McNemar); cost from real token counts
```
`docs/sdlc/changes/C-0025-local-model/findings.md`
```
LLM fallback:  91.4%, ₹2.10 per user per month
Local model:   88.9%, ₹0.20 per user per month
Hybrid (local for merchants seen 5+ times):
               92.1%, ₹0.70; 120 ms per batch
```
`docs/sdlc/changes/C-0025-local-model/findings.md`
```
Leak: merchant counts included the eval set
Fixed: counts from the training months only
Hybrid: 91.6% ± 0.3 over 3 runs (was 92.1%)
Still within 2 points of 91.4%; ₹0.70; 120 ms
Re-run from a clean start: same result; snapshot, commit and seeds recorded
```

**What it shows:** The plan is written before the experiment and the numbers are checked against it before the decision, so the result decides itself. Nothing from the notebook ships.

---

## 10. Incident: Bank changes its CSV format

**When:** An alert, failed pipeline or metric drift.

**You bring:** `/start Alert: parse failures 31% (baseline 2%)`

**Router:** Source: Sent by the alert hook; no one types it · Type: Incident → **Incident**

**Your decisions:** As routed: here, merge

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | detection | The alert fires | A threshold rule, not a model, sees parse failures at 31% against a 2% baseline on the 1st of the month. Its hook sends the alert to /start, which is why the router ran first. Nobody is watching at 06:10, so the run loads afk and every gate waits for you. | — | — |
| 2 | diagnose-bug (read-only) | Diagnose without changing anything | Reads logs and failed files only. Every failure comes from Bank B, whose CSV header changed overnight. | — | — |
| 3 | → Bug fix | Small fix through Bug fix | The Bug fix playbook runs: a failing test with the new header, then Bank B's adapter accepts both. Thanks to the refactor it is one file. The 212 files are re-parsed. | Merge. | Merge |
| 4 | → agent-raised intent | Raise the bigger problem | Banks change formats without notice. The agent raises I-0011 Detect format changes before users hit them, status proposed. The router will route it when it is picked up. | — | — |
| 5 | eval case | Keep the lesson | The new header joins the fixtures and the eval suite. | — | — |

**Artifacts**

`docs/sdlc/incidents/2026-03-01-bank-b.md`
```
When: 1 Mar, 06:10–09:40 IST
Impact: 212 Bank B uploads failed
Cause: header 'Value Date' renamed 'Value Dt'
Data: none lost; files can be re-parsed
```

**What it shows:** Detection is deterministic and diagnosis is read-only. The small fix goes through Bug fix; the bigger problem becomes a proposed intent.

---

## 11. `huh`: A grilling question you can't parse

**When:** You don't follow the agent's last message or the question it asks you.

**Typed:** `/huh`

**How it starts:** Trigger: You type it, with nothing after it · When: In the bank-sync de-duplication grilling · Router: Not involved: huh answers a need, not work · Skill: huh

Working the de-duplication ticket for bank sync, grilling's next round has one question: "Window semantics: should the de-duplication key be evaluated per sync window or across the account's full history, given late-posting transactions?" Grilling already said why it matters, and you still don't follow what is being decided.

**Your decisions:** Your answer to the question, once you understand it

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | huh | Find what is waiting on you | Nothing came after /huh, and the last reply asks you one question, so it explains that question. Had the round asked several, it would put each in a plain line or two, and /huh Q2 would go deeper on one. | — | — |
| 2 | huh | Explain the decision | Everyday words and the glossary's terms, with sync window defined once. The trade-off stays honest: neither answer is free. | — | — |
| 3 | grilling | Back to the round | You answer yes. Grilling records the decision and asks the next round. | Answer the simpler question. | — |

**Artifacts**

`huh: the question in plain words`
```
Deciding: how far back to look for a copy of a transaction
Why it matters: banks post some payments days late
A  This sync's dates only: fast; late payments show twice
B  Whole history: no doubles; each sync gets slower
Recommended: B, limited to the last 90 days
Asked again: look back 90 days for duplicates?
```

**What it shows:** With one question waiting, a bare /huh explains it as a decision you can make: what is being decided, why it matters, what each answer leads to, and a recommendation. Add a number only when a reply asks several.

---

## 12. `huh`: Back from lunch mid-session

**When:** You come back to a long session and need to know what changed for you.

**Typed:** `/huh`

**How it starts:** Trigger: You type it, with nothing after it · When: After lunch, during the recurring-payments Feature M · Router: Not involved · Skill: huh

While you were at lunch, three subagents finished, CI ran twice and a PR opened. You remember your last message and nothing after it. With nothing after it, /huh sees how much has happened since you last wrote and catches you up instead of re-explaining one reply.

**Your decisions:** The one call waiting on you

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | huh | Gather what changed | Reads only what happened since your last message: subagent reports, the CI runs and the PR. It changes nothing. | — | — |
| 2 | huh | Write one screen | What changed for you, not how the agent did it; the decision waiting on you comes first, with a recommendation. | — | — |
| 3 | you | Make the call | You merge PR #74. | Merge. | Merge |

**Artifacts**

`huh: catch-up`
```
One thing needs you.
Recurring payments: built and tested; PR #74 open
CI: one flaky test re-run, now passing
Needs you: merge PR #74 (recommend yes: verify-app green)
If you don't answer: it waits; nothing merges
```

**What it shows:** With nothing after it, /huh catches you up when a lot has happened in this session: what changed for you, with every decision waiting on you first. For everything in flight across all your work, type /start on its own.

---

## 13. `readback`: Check the goal before an AFK run

**When:** Before the agent builds, you want to be sure it understood you.

**Typed:** `/readback`

**How it starts:** Trigger: You type it · When: Before leaving the MVP build to run overnight · Router: Not involved · Skill: readback

You are about to leave I-0003 and I-0004 to an overnight AFK run. A misunderstanding now would cost a night of work, so you ask the agent to say the goal back first.

**Your decisions:** Correct anything it got wrong

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | readback | Say the goal back | In its own words, not a copy of the specs. | — | — |
| 2 | readback | Raise what it's unsure of | Re-categorising past months is a preference call, so it comes to you now instead of becoming an overnight default. | Answer: future months only. | — |
| 3 | → /start | Leave with the goal settled | The answer goes into the I-0004 spec. You type /start Build I-0003 and I-0004; I'm stepping away until morning, and the AFK run has one fewer default to pick. | — | — |

**Artifacts**

`readback`
```
Goal: finish the monthly view (I-0003) and corrections (I-0004)
Why: M1 must prove O1, know where the money goes
Done when: both PRs open, verify-app green, monthly view p95 < 2 s
Not doing: budgets (I-0005), merging
Unsure: should a correction re-categorise past months too?
```

**What it shows:** A readback costs one message and catches a misunderstanding before it costs a night of work.

---

## 14. `handoff`: Pause and switch devices

**When:** You stop part-way through a playbook, or the session's context is getting long.

**Typed:** `/handoff Finish slice 2 of recurring payments, then review`

**How it starts:** Trigger: You type it; the agent suggests it when the context runs long · When: Feature M paused mid-way; switching devices · Router: Comes after: /start resumes from the handoff · Skill: handoff

handoff is never a playbook step. You run it when you leave a playbook part-way: here Feature M for recurring payments, with slice 1 committed and slice 2 half built, and you are moving to another device. The agent also suggests it when the context is getting long.

**Your decisions:** What the next session focuses on

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | handoff | Write the handoff | Writes only what isn't already recorded. The spec, plan and commits are referenced by path, not copied, and secrets are redacted. | — | — |
| 2 | where it goes | Put it where the next session can read it | On the same device it would go to the temp folder. You are switching devices, so it goes into the change folder on the branch, which is pushed. | — | — |
| 3 | /start | Resume on the other device | In a fresh session, /start continue recurring payments matches change C-0014, reads the handoff and resumes Feature M at its next step: implement, slice 2. | Type /start continue recurring payments. | — |
| 4 | implement | Carry on | Slice 2 continues from its written tests; tidy, verify-app and review-change run as normal. | — | — |
| 5 | cleanup | Retire the handoff | When the change merges, the handoff is deleted. Everything worth keeping is already in the spec, plan and commits. | — | — |

**Artifacts**

`docs/sdlc/changes/C-0014-recurring/handoff.md`
```
Focus: finish slice 2, then tidy → verify → review
Done: slice 1 (a1c9e04); spec and plan in this folder
In progress: list-page tests written, UI not started
Watch: EMIs past their end date (spec rule 4)
Suggested skills: implement, tdd, verify-app
```

**What it shows:** A handoff carries only what isn't written down elsewhere, and /start uses it to resume the paused playbook.

---

## 15. `afk`: Overnight MVP build

**When:** Nobody will watch the run: you say you're stepping away or type /afk, or a hook or scheduled task starts it.

**Typed:** `/start Build I-0003 and I-0004; I'm stepping away until morning`

**How it starts:** Backlog: Resumes the MVP build: I-0003, I-0004 · Mode: AFK: you are stepping away · Trigger: /start loads afk · Skill: afk

You didn't ask for it by name. Because you are stepping away, /start resumes the MVP build under afk, so your absence never turns into a decision made for you. Typing /afk mid-session does the same, and every hook-started run loads it too. Both specs were approved before you left.

**Your decisions:** Morning review of the hand-back, then each PR's merge

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | afk | Check readiness | CI, a staging deploy, verify-app and the destructive-command guard have existed since the walking skeleton, so the run may go AFK. It opens .audit/mvp-overnight.tsv with a start row. | — | — |
| 2 | implement (parallel) | Work, picking and logging defaults | I-0003 and I-0004 run in parallel worktrees. With nobody to ask, each ambiguous choice gets the default the spec and ADRs point to, and one row with its evidence as a pointer, not prose. | — | — |
| 3 | afk | Hold the gate | Merging is a human gate, so the run parks both PRs instead of merging. There is no other unblocked work, so it stops. | — | — |
| 4 | audit the trail | Check the trail told the truth | Reads the run's transcript against the trail and finds an unlogged pivot: it swapped the chart library. It appends row 6 rather than editing history. | — | — |
| 5 | second-family review | Review the trail | A model from another family reads the trail and flags row 4: it claims verify-app passed for I-0004, but gives no evidence. | — | — |
| 6 | hand-back | Write the hand-back | Tops the trail with one screen for your return. | — | — |
| 7 | morning | Your morning review | You read the hand-back, re-run verify-app for I-0004, glance at the defaults, then merge both PRs. The trail is committed with the changes. | Read the hand-back, then merge. | Merge |

**Artifacts**

`.audit/mvp-overnight.tsv`
```
1 21:30 start | I-0003, I-0004 | specs approved | ready
2 22:10 default: pre-aggregate totals | G3 < 2 s | ADR 0006 | p95 1.4 s
3 01:20 default: corrections per merchant | spec rule 2 | 9f3e1d0 | green
4 02:40 I-0004 verify-app passed | — | — | done
5 03:05 gate held: merge | human gate | PR #61, #62 | waiting
```
`.audit/mvp-overnight.tsv (hand-back)`
```
Finished: I-0003, I-0004 built; PRs #61, #62 open
Waiting for you: merge both PRs
Check first: row 4, verify-app claim has no evidence
Defaults picked: rows 2, 3 · added by the audit: row 6
Proposed term for the glossary: merchant rule (row 3)
```

**What it shows:** An AFK run carries on with what you approved, picks and logs defaults instead of asking, holds every gate, and hands back one screen you can check in minutes.

---

## 16. `how`: How a statement becomes transactions

**When:** You need to know how code works, or where something belongs.

**Typed:** `/how does an uploaded statement become transactions`

**How it starts:** Trigger: You type it · When: Before reviewing the bank-adapter refactor · Router: Not involved · Skill: how

Agents wrote most of the import path. Before you review the bank-adapter refactor, you want a working picture of it.

**Your decisions:** None: it only explains

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | how | Judge the scope | The question crosses upload, the parser adapters, the categoriser and storage, so three explorers read in parallel, read-only. | — | — |
| 2 | how (explorers) | Explore three angles | Upload and deletion; the adapters and their registry; the categoriser's rules and model fallback. Each uses the codebase-design vocabulary and the glossary's terms. | — | — |
| 3 | how | Explain it one diagram at a time | An overview first, then one small diagram per stage instead of one diagram with everything. | — | — |

**Artifacts**

`how: statement → transactions`
```
Upload → registry picks the bank's adapter → rows
Rows → masking → categoriser (rules first, model if unsure)
Categorised rows → Postgres; raw file deleted (G1)
Gotcha: an adapter must never log raw rows
```

**What it shows:** how gives you a working mental model of code you didn't write, in the words the repo already uses.

---

## 17. `why`: Why monthly totals are pre-aggregated

**When:** You need to know why code is the way it is.

**Typed:** `/why are monthly totals pre-aggregated instead of computed on read`

**How it starts:** Trigger: You type it · When: Planning budgets, which read the same totals · Router: Not involved · Skill: why

Budgets will read the monthly totals. Before changing how they are stored, you want to know why they are pre-aggregated at all.

**Your decisions:** None: it only explains

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | why | Anchor on the code | Finds the aggregation job, blames its lines and follows the commit to its PR. | — | — |
| 2 | why | Follow the trail | From the PR to its change folder, the intent, the guardrail, architecture.md and the ADR, and to the run trail of the night it was built. | — | — |
| 3 | why | Keep known apart from inferred | Every known line cites its source. The one thing nobody wrote down is marked as inferred, not stated as fact. | — | — |

**Artifacts**

`why: pre-aggregated totals`
```
Known: G3 needs the monthly view under 2 s (p95)
Known: architecture.md maps G3 to pre-aggregated totals (ADR 0006)
Known: the overnight AFK run followed it, trail row 2: p95 1.4 s
Inferred: computing on read was never measured (not in the ADR)
```

**What it shows:** Because every change traces to an intent and every decision to an ADR or a trail row, why answers from evidence instead of guessing.

---

## 18. `explore-data`: A new bank's export

**When:** A dataset arrives that nobody has looked at properly yet.

**Typed:** `/explore-data samples/bank-d-export.csv`

**How it starts:** Trigger: You type it; the agent starts it when a new dataset arrives · When: Before writing the Bank D adapter · Router: Not involved · Skill: explore-data

Users want Bank D supported. Before anyone writes its adapter, you want to know what its export really contains, using an anonymised sample.

**Your decisions:** What the spec must handle

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | explore-data | Load it properly | Reads the file with DuckDB, which copes with large files and infers types: 18,412 rows covering 14 months. | — | — |
| 2 | explore-data | Profile every column | Shape, types, nulls, ranges, duplicates and patterns, written where the change can use them. | — | — |
| 3 | explore-data | Suggest what to settle | Three questions for the spec: which date format wins when a date is ambiguous, how to drop page-break copies, and whether the running balance becomes a parse check. Two columns, value date and narration, are words the glossary lacks, so the spec's grilling names them. | — | — |
| 4 | to-spec | Into the spec | The Bank D adapter spec now covers both date formats, the Dr/Cr sign, page-break copies and a balance check. | Approve the spec. | Spec approved |

**Artifacts**

`docs/sdlc/changes/C-0031-bank-d/profile.md`
```
Dates: DD/MM/YYYY until March, YYYY-MM-DD after
Amount: always positive; a Dr/Cr column gives the sign
Reference: empty in 12% of rows, all of them UPI payments
Duplicates: 37 exact copies, all at statement page breaks
Balance: a running balance with no gaps, usable as a check
Narration: holds payee names, so personal data: counts only, values hidden
```

**What it shows:** explore-data looks at the data before anyone builds on it, so the spec handles what the data really contains rather than what everyone assumed.

---

## 19. `data-context`: Map the warehouse, then keep it current

**When:** The agent queries data that has no map yet, or any work brings new facts about the data.

**Typed:** `/size-impact Automatic bank sync for M2`

**How it starts:** Trigger: The agent: before its first query, then whenever new facts about the data appear · When: size-impact needs the number of active households · Router: Not involved · Skill: data-context

Sizing bank sync needs one number from the product warehouse: how many households are active. There is no map of the warehouse yet, so before writing any SQL the agent builds one. From then on, the map keeps itself current.

**Your decisions:** What each metric means

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | data-context | Ask what matters | Rather than mapping all 140 tables, it asks for the 3 to 5 you use most. You name four: households, events, statements and transactions. | Name the tables. | — |
| 2 | data-context | Map grain and keys | Reads each table's schema and a sample, and writes down what one row means and how the tables join. | — | — |
| 3 | data-context | Agree the definitions | Each metric is written as SQL, dated, and linked to its glossary term. What a metric means is your call, so you confirm each one. | Confirm the definitions. | — |
| 4 | data-context | Record the traps | Traps are facts with evidence, so they go in without asking. | — | — |
| 5 | size-impact | Back to the sizing | The first query runs against the map: 8,680 active households last month, test accounts excluded. Every later query, and review-result's checks, start from the same definitions. | — | — |
| 6 | ship → data-context | Later: a merged change adds data | When bank sync merges, ship adds its new linked_accounts table and sync_completed event to the map, with the change as the source. They are facts, so nobody is asked. | — | — |
| 7 | data-context | Later: a definition needs you | With sync live, a household can look active without anyone opening the app. What "active" should count is a question of meaning, so the agent proposes an answer and /start lists it as waiting for you. Until you confirm, numbers say they used a proposed definition. | Confirm: background syncs don't count. | — |
| 8 | data-context | Later: the warehouse changes | A query touching events finds that a warehouse migration renamed ts to event_ts. The map is corrected on the spot and the old name kept as superseded, so the query and every later one keep working. | — | — |

**Artifacts**

`agent-skills/skills/data-context/map/product-warehouse.md`
```
households: one row per household; key household_id
events: one row per app event; household_id, event_name, ts (UTC)
statements: one row per upload; file deleted after import (G1), metadata kept
transactions: one row per transaction; key transaction_id
```
`product-warehouse.md (metrics)`
```
Active household (2025-06-02): uploaded a statement or opened the app in the month, in IST
Engaged rate: active households that opened the monthly view ÷ active households
Both exclude test accounts
```
`product-warehouse.md (traps)`
```
events arrive up to 48 h late: count a month only from the 3rd of the next
ts is UTC, but months are counted in IST (see Transaction time)
test accounts: is_test, plus every @example.com email
```
`data-context: changelog`
```
2025-06-02  created: 4 tables, 2 definitions, 3 traps (size-impact)
2025-10-14  + linked_accounts, sync_completed (C-0020 merged)
2025-10-16  Active household: background syncs don't count (you confirmed)
2026-04-20  ~ events.ts → event_ts (schema check on a query)
```

**What it shows:** data-context starts from the tables you actually use and then keeps itself current: facts from queries, profiles and merged changes go in on their own, with their source, and only what a metric means waits for you.

---

## 20. `diagnose-metric`: Engagement fell 7 points in March

**When:** A metric moved and you need to know why before anyone acts on it.

**Typed:** `/diagnose-metric Engaged rate fell from 64% to 57% in March`

**How it starts:** Trigger: You type it; Incidents and measure steps start it too · When: Before the monthly product review · Router: Not involved: a need, not work · Skill: diagnose-metric

The monthly dashboard shows the engaged rate, the share of active households that open the monthly view, down from 64% in February to 57% in March. Someone asks whether the March release broke something. You want the answer before the review.

**Your decisions:** What to do about it, once the cause is known

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | diagnose-metric | Rule out the data | Reads the engaged rate's definition in data-context, then checks the data before the world: every daily load ran, March was counted after its 48-hour late window, the definition last changed in October, before both months, and the March release kept the event's name. The drop is real. | — | — |
| 2 | diagnose-metric | Mix or rate? | Splits the move into a change in who is in the base and a change in how each group behaves. Households from February's referral campaign went from 5% of the base to 24%, and they open the monthly view far less. | — | — |
| 3 | diagnose-metric | Segments and calendar | Checks platform, bank and city: no segment moves beyond its usual range. Per-day rates fall the same way, so March's three extra days are not the cause. | — | — |
| 4 | review-result | Check the conclusion | Re-runs the decomposition from a clean start and checks the denominator: active households as data-context defines them, test accounts excluded. Verdict: ready. | — | — |
| 5 | diagnose-metric | Write the readout | Decision first, then the numbers, then what would change the conclusion. The trap goes into data-context: the blended engaged rate moves with the mix of new households, so it is reported per sign-up cohort. | — | — |

**Artifacts**

`diagnose-metric: mix and rate`
```
Existing households: 66.0% → 65.5% (flat)
Campaign households: 30% → 31% (flat)
Campaign share of the base: 5% → 24%
Mix explains 6.6 of the 7.0 points; rate 0.4
```
`Readout: engaged rate, March`
```
Nothing broke: each group's engagement is flat
The blended rate fell because campaign households rose to 24% of the base
From now on, report the engaged rate per sign-up cohort
Would change this: a fall within existing households next month
```

**What it shows:** diagnose-metric rules out the data before blaming the world, and separates mix from rate before blaming the product. Here a release was about to be blamed for a change in who the users are.

---

## 21. `write-notebook`: The broken evaluation notebook

**When:** The agent writes a notebook, or touches an old Jupyter one.

**Typed:** `/start Could a small local model replace the LLM fallback for categorising?`

**How it starts:** Trigger: The agent, whenever it writes or touches a notebook · When: The Spike's prototype step starts from the old evaluation notebook · Router: Inside the Spike playbook · Skill: write-notebook

The local-model Spike starts from notebooks/eval_categoriser.ipynb, the Jupyter notebook code-health flagged as broken. Before reusing it, the agent converts it to marimo, which refuses to run with the problems Jupyter quietly allowed.

**Your decisions:** None

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | write-notebook | Convert it | eval_categoriser.ipynb becomes eval_categoriser.py. The conversion stops at four problems Jupyter allowed. | — | — |
| 2 | write-notebook | Fix what it found | The import points at the current module, cutoff_date gets its own cell, and the data snapshot becomes a parameter instead of a path. marimo stores no outputs in the file, so no transactions get committed (G1). The notebook part of code-health's batch C is now done. | — | — |
| 3 | write-notebook | Run it like code | Cells re-run when what they depend on changes, the file runs top to bottom as a script, and the PR shows readable Python instead of JSON. | — | — |
| 4 | review-result | Re-run from a clean start | Later in the Spike, review-result re-runs the notebook from scratch with seeds 1 to 3, gets the same 91.6% ± 0.3, and records the snapshot, commit and seeds with its verdict. | — | — |

**Artifacts**

`write-notebook: conversion`
```
Imports a module that no longer exists (code-health's batch C)
Cell 14 uses cutoff_date, defined only in a deleted cell
A path into your Downloads folder: works on one laptop only
Saved outputs: 4 MB, including sample transactions with account numbers
```
`notebooks/eval_categoriser.py`
```
Runs as a script: python notebooks/eval_categoriser.py
No hidden state: every cell's inputs are explicit
Diff in the PR: the code, not 4 MB of JSON
```

**What it shows:** A marimo notebook is plain Python with no hidden state and no stored outputs, so the agent can diff it, review-result can re-run it, and no personal data reaches the repo.

---

## 22. `look-up`: The aggregator's sync limits

**When:** A decision waits on a fact you'd have to read up on.

**Typed:** `/look-up how often the aggregator lets us sync each account`

**How it starts:** Trigger: You type it; the agent and wayfinder start it too · When: Before choosing the daily sync schedule · Router: Not involved · Skill: look-up

The sync schedule depends on the aggregator's limits. Nobody should guess them, and you don't want to stop and read the docs yourself.

**Your decisions:** None: it brings facts

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | look-up | Hand it to a background agent | You keep working while it reads. | — | — |
| 2 | look-up | Read the primary sources | The aggregator's API reference and consent guide, not blog summaries. Each claim is followed back to the page that owns it. | — | — |
| 3 | look-up | Write a cited note | One file, every claim with its source, and the open question it couldn't settle. | — | — |

**Artifacts**

`docs/research/aggregator-sync-limits.md`
```
Q: How often may we sync each account?
A: 4 syncs per account per day [API reference, Rate limits]
A: Consent lasts 365 days, then the user re-consents [Consent guide]
Open: no published limit on history depth
```

**What it shows:** look-up answers from the source that owns the fact and leaves a cited note, so the next decision doesn't repeat the reading.

---

## 23. `learn`: Learning Postgres row-level security

**When:** You want to learn a topic properly, over several sessions.

**Typed:** `/learn Postgres row-level security`

**How it starts:** Trigger: You type it, in a learning folder · When: Before the shared-households expansion · Router: Not involved · Skill: learn

Shared households depend on row-level security, which you have never used. You start /learn in its own learning folder, not in the product repo.

**Your decisions:** What you want to be able to do

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | learn | Write the mission | Asks why you want this. The answer shapes every lesson. | Say why you're learning it. | — |
| 2 | learn | Find trusted sources | Collects primary sources before any lesson. | — | — |
| 3 | learn | Lesson 1 | One HTML lesson and an exercise on a scratch database: write a policy, then try to read another household's rows. | Do the exercise. | — |
| 4 | learn | Record what you learned | The non-obvious lesson gets a record, so the next session starts from it. | — | — |

**Artifacts**

`MISSION.md`
```
Why: review the households RLS design with confidence
Enough when: I can spot a policy that leaks rows
```
`RESOURCES.md`
```
PostgreSQL docs: Row Security Policies
PostgreSQL docs: CREATE POLICY, ALTER TABLE
```
`learning-records/0001-owners-bypass.md`
```
Table owners bypass RLS by default
FORCE ROW LEVEL SECURITY makes the owner follow the policies too
```

**What it shows:** learn builds understanding over several sessions from trusted sources, and keeps records so each session starts where the last one ended.

---

## 24. `brainstorm`: More households back for a second month

**When:** You need ideas, not yet an idea: a new project, a feature area, an improvement plan.

**Typed:** `/brainstorm how to get more households to upload a second month`

**How it starts:** Trigger: You type it · When: After the M1 review: 64% upload a second month · Router: Not involved: ideas come before work · Skill: brainstorm

The M1 review found that only 64% of households upload a second month. You don't have a fix in mind yet; you want a wide set of grounded options before picking one.

**Your decisions:** The frame and criteria · which ideas to pursue

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | brainstorm | Frame it | The goal is the share of households that upload a second month, now 64%. Off the table: anything that weakens G1. Ideas will be judged on likely effect, effort and risk. | Confirm the frame and the criteria. | — |
| 2 | brainstorm | Ground it | Reads the brief, the backlog and data-context before generating anything. Bank sync (I-0009) is already planned, a monthly digest email was tried and dropped, and a third of the households that never return had a failed parse on their first upload. | — | — |
| 3 | brainstorm → second-opinion | Generate before judging | Eighteen ideas from six angles, plus six from another model family through second-opinion, before any is judged. You add two of your own. | — | — |
| 4 | brainstorm | Critique every idea | Every idea is kept or cut with a reason, so nothing quietly disappears. | — | — |
| 5 | brainstorm | Rank the shortlist | The survivors are ranked against your criteria, each with the assumption that would sink it. | Pick what to pursue. | — |
| 6 | brainstorm | Hand each pick on | You pick 1 and 2. Idea 1 becomes a Spike, to check that those failures really drive the drop-off before fixing them; idea 2 goes to size-impact. Idea 3 stays on the list for the next brainstorm. | — | — |

**Artifacts**

`docs/sdlc/ideas/second-month-uploads.md`
```
Remind people on the day their bank usually sends the statement
A forward-to-import address: forward the bank's email, we import the file
Show one surprising finding right after the first upload
Fix first-upload parse failures before anything else
Bank sync · monthly digest email · pay people to return · do nothing
```
`second-month-uploads.md (cuts)`
```
Bank sync: already planned as I-0009
Monthly digest email: tried and dropped, low opens
Pay people to return: off the table (cost, and it doesn't serve O1)
Do nothing: kept as the baseline
```
`second-month-uploads.md (shortlist)`
```
1 Fix first-upload parse failures: assumes those failures cause people to leave
2 Statement-day reminder: assumes the first upload shows when the bank sends statements
3 Forward-to-import address: assumes attachments can be deleted right after import (G1)
```

**What it shows:** brainstorm widens before anything narrows: grounded in what exists, many ideas before any judging, every cut explained, and a short ranked list that hands each pick to the skill that tests it next.

---

## 25. `wayfinder`: Bank sync's open decisions

**When:** Open decisions need more than one session before a spec or design can be written.

**Typed:** `/wayfinder Automatic bank sync has too many open questions to design in one sitting`

**How it starts:** Trigger: You type it; Feature L suggested it · When: Five open decisions, several needing outside facts · Router: Not involved: wayfinder is not a playbook · Skill: wayfinder

In the Feature L example the open questions fitted one session. Here they don't: which aggregator, sandbox access, the consent screen, the de-duplication key and token retention need research and your input over several sessions. Feature L pauses after the intent is accepted and suggests /wayfinder.

**Your decisions:** The destination · each prototype, grilling and task ticket

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | grilling + glossary | Name the destination | Settles what the map is finding its way to before anything else, because the destination fixes the scope. | Agree the destination. | — |
| 2 | grilling (breadth-first) | Map the frontier | Fans out across the whole problem instead of going deep on one thread. Anything not yet sharp enough to become a ticket goes into the fog; anything beyond the destination is ruled out of scope. | — | — |
| 3 | chart the tickets | Create the decision tickets | One file per question, typed, labelled HITL (needs you) or AFK (the agent alone), and wired with blocking edges. These are decisions to make, not slices to build. | — | — |
| 4 | look-up (subagent) | AFK research runs on its own | Ticket 01 is AFK, so a subagent compares three aggregators' documentation and pricing in parallel and records the answer. Charting ends the first session; nothing else is resolved in it. | — | — |
| 5 | /wayfinder bank-sync | Session 2: a task ticket | The frontier is ticket 02, a HITL task: it needs you. The agent hands you a checklist to sign up for the sandbox, then records where the credentials live. | Sign up, then confirm. | — |
| 6 | /wayfinder bank-sync | Session 3: a prototype ticket | Ticket 03 is a rough consent screen to react to. You want the revoke button on the same screen, not buried in settings. That is the decision. | React to the prototype and decide. | — |
| 7 | /wayfinder bank-sync | Session 4: a grilling ticket | Ticket 04 settles de-duplication on date, amount and bank reference. The answer clears some fog: the retry policy is now sharp enough to become ticket 06. | Answer the grilling. | — |
| 8 | back to Feature L | Destination reached | Two more sessions settle tickets 05 and 06. With nothing left to decide, the map's decisions feed to-spec and to-design, and Feature L resumes where it paused. | — | Feature L's own gates |

**Artifacts**

`.scratch/bank-sync/map.md`
```
## Destination
An approved spec and design for I-0009 bank sync
## Notes
Every ticket: grilling + glossary; G1 applies
```
`.scratch/bank-sync/map.md`
```
## Not yet specified
Retry policy when a bank is down
## Out of scope
Credit-card accounts (a separate intent)
```
`.scratch/bank-sync/issues/`
```
01 Which aggregator?   research   AFK
02 Sandbox account     task       HITL  ← 01
03 Consent screen      prototype  HITL  ← 02
04 De-duplication key  grilling   HITL
05 Token retention     grilling   HITL  ← 01
```
`.scratch/bank-sync/issues/01-which-aggregator.md`
```
Type: research (AFK)   Status: resolved
## Answer
Aggregator A: sandbox, 14 banks, ₹0.40 per sync
Chosen: A; covers 9 of our top 10 banks
```
`.scratch/bank-sync/map.md`
```
## Decisions so far
Which aggregator?: A, covers 9 of the top 10 banks
Consent screen: revoke on the same screen
De-duplication key: date + amount + reference
```

**What it shows:** wayfinder plans; it never builds. One ticket per session, AFK research runs on its own, HITL tickets wait for you, and the decisions flow back into the playbook that paused.

---

## 26. `size-impact`: Is bank sync worth building?

**When:** Before deciding whether something is worth building, or when choosing between options at planning.

**Typed:** `/size-impact Automatic bank sync for M2`

**How it starts:** Trigger: You type it; milestone planning runs it too · When: Planning M2: bank sync would take about 6 engineer-weeks · Router: Not involved · Skill: size-impact

Bank sync keeps coming up in feedback, and it would cost about 6 engineer-weeks plus the aggregator's fees. Before it becomes an intent, you want to know whether it is likely to be worth that.

**Your decisions:** The bar · The verdict

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | size-impact | Frame it | The decision, the metric, the horizon and the bar. The bar is yours: the smallest impact that justifies the cost. | Set the bar. | The bar |
| 2 | size-impact | Break it into drivers | Each driver gets a range and a source: data first, then comparable launches, then judgment, labelled as such. | — | — |
| 3 | size-impact | Combine as a range | A simulation over the three ranges, rather than multiplying all the lows and all the highs, which compounds into extremes nobody believes. | — | — |
| 4 | size-impact | Find what matters most | Lift moves the answer from 121 to 250; adoption only from 143 to 205. Lift can't be measured before building. Adoption could be, with a fake door, but it matters less. | — | — |
| 5 | review-result | Check the arithmetic | Reach counts active households as data-context defines them, test accounts excluded, and the lift applies only to households who link, not to the whole base. Verdict: ready. | — | — |
| 6 | size-impact | Give the verdict | Go, with a thin slice first: one bank, so the lift can be measured before the rest is built. You accept, and bank sync becomes I-0009, linked to this sizing. | Accept the verdict. | The verdict |
| 7 | size-impact | Later: check the sizing | Sixty days after release, Feature L measures 53% of active users linked, inside the 30–60% adoption range. The actual goes into the sizing beside its range; the lift follows at 90 days. | — | — |

**Artifacts**

`docs/sdlc/sizing/bank-sync.md`
```
Decision: build bank sync in M2?
Metric: extra households still active after 90 days, per quarter
Horizon: the first quarter after release
Bar: 150 households a quarter
```
`bank-sync.md (drivers)`
```
Reach: 8,680 active households (data-context)
Adoption: 30–60% link an account within 60 days (comparable apps)
Lift: 2–8 points of 90-day retention for those who link (judgment)
```
`bank-sync.md (result)`
```
P10 115 · P50 176 · P90 259 households a quarter
Chance of clearing the bar: 69%
```

**What it shows:** size-impact turns "is this worth it?" into a range, names the assumption that matters most, and is checked against the actuals after release, so your sizings get better calibrated over time.

---

## 27. `preregister`: Does a reminder raise account linking?

**When:** Before an experiment, A/B test or model comparison decides something.

**Typed:** `/preregister A day-3 reminder email: does it raise bank linking?`

**How it starts:** Trigger: You type it; Spike and experiments start it too · When: Planning I-0015 Link reminder, before release · Router: Inside Feature M · Skill: preregister

A reminder email on day 3 might get more new users to link their bank. Before building it and splitting users into two groups, you write down what would count as success.

**Your decisions:** The bar: the smallest effect worth acting on

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | preregister | State the question and the decision | Ship the reminder to everyone if it raises linking by at least 5 points; otherwise drop it. | Agree the 5-point bar. | The bar |
| 2 | preregister | Design it and size it | The sample size comes from the smallest effect worth acting on, not from how long you are willing to wait. | — | — |
| 3 | preregister | Fix the stop rule and the analysis | Written before any data arrives, so the result can't be argued into the answer you hoped for. | — | — |
| 4 | review-result | Later: check the result against it | Seven weeks later, review-result checks the outcome against this plan: the right metric, the right users, no early stop. 44% of the reminder group linked within 14 days against 38% without it, so the reminder ships to everyone. | — | — |

**Artifacts**

`docs/sdlc/changes/C-0033-link-reminder/preregistration.md`
```
Metric: new users who link an account within 14 days (now 38%)
Design: new users split 50/50 at sign-up
Size: about 1,510 per group for 80% power at α = 0.05
Duration: five weeks of sign-ups (about 600 a week), then 14 days
```
`preregistration.md (continued)`
```
Stop rule: nobody looks at the metric early; stop only if unsubscribes double
Analysis: one two-proportion test on the primary metric
Everything else is reported as exploratory
```

**What it shows:** preregister fixes the question, the size and the analysis before the data arrives, so the result decides instead of being argued over.

---

## 28. `to-questionnaire`: Token retention, asked of the privacy lead

**When:** You can't answer a question, but someone else can.

**Typed:** `/to-questionnaire token retention for bank sync`

**How it starts:** Trigger: You type it · When: Wayfinder ticket 05 needs rules you don't know · Router: Not involved · Skill: to-questionnaire

The bank-sync map's ticket 05, token retention, needs retention rules that the privacy lead knows and you don't. A guess here would break G1.

**Your decisions:** Who it goes to and what you need back

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | to-questionnaire | Who is it for? | It asks only about the send: it goes to the privacy lead, who knows the rules but not this feature. | Name the recipient. | — |
| 2 | to-questionnaire | What do you need back? | Two decisions: how long a consent token may be kept, and what revoking consent must delete. | Say what you need. | — |
| 3 | to-questionnaire | Write the questionnaire | Most important question first, one idea per question, and a short context paragraph for someone who wasn't in the room. | — | — |
| 4 | wayfinder | Wait for the answers | Ticket 05 stays open, blocked on the questionnaire, and the map moves on to other tickets. | — | — |

**Artifacts**

`to-questionnaire-token-retention.md`
```
Purpose: decide token retention for bank sync (I-0009)
Q1 How long may we keep a consent token after the last sync?
Q2 On revoke, must stored transactions be deleted too?
Q3 Do the rules differ by bank?
```

**What it shows:** When the answer is in someone else's head, to-questionnaire asks them well, and the decision waits for them instead of a guess.

---

## 29. `technical-writing`: A PR description read in one pass

**When:** A doc, README, RFC or PR description is for people to read.

**Typed:** `/technical-writing the description of PR #74`

**How it starts:** Trigger: You type it · When: Before asking a teammate to review PR #74 · Router: Not involved · Skill: technical-writing

The recurring-payments PR description is accurate but padded and in the order the work happened. You want a teammate to review it in one pass.

**Your decisions:** None

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | technical-writing | Order it for the reader | What changed and why comes first, then how to verify it, then where to look closely. The story of how it was built goes. | — | — |
| 2 | unslop | Cut the AI tells | technical-writing runs unslop: the filler opening, stacked hedges and empty intensifiers go; every fact, number and file name stays. | — | — |
| 3 | technical-writing | Check it reads for its audience | Plain words, one idea per sentence, the glossary's terms. The reviewer can see what to check without opening the code first. | — | — |

**Artifacts**

`PR #74 description`
```
Before: This PR introduces a robust, comprehensive solution for…
After: Finds recurring payments in three months of history.
Before: It's worth noting that this may potentially…
After: Payments whose amount changes by over 20% are not grouped.
```

**What it shows:** technical-writing shapes a document for the person who reads it, and runs unslop to cut the tells while keeping every fact.

---

## 30. `polish`: The engagement finding, for the product lead

**When:** A message, email, comment or post you wrote, before you send it as yourself.

**Typed:** `/polish for Priya on Slack: Hi Priya, hope you're doing well! Just wanted to quickly circle back on the engagement dip…`

**How it starts:** Trigger: You type it, with your draft after it · When: Before sending the engagement finding to the product lead · Router: Not involved · Skill: polish

Your draft: "Hi Priya, hope you're doing well! Just wanted to quickly circle back on the engagement dip. So basically after digging into it, it's not really the March release at all — it's more of a mix thing. The referral campaign brought in a lot of new households who honestly don't open the monthly view much, and that pulled the average down. Existing households are pretty much flat (66% → 65.5%). I think going forward we should probably report it by cohort so this doesn't confuse people again. Let me know your thoughts!"

**Your decisions:** Whether to send it, and which suggestion to take

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | polish | Read the reader and the goal | Priya leads product and reads Slack between meetings. The goal is two things: she should know the release didn't cause the dip, and agree to report by cohort. | — | — |
| 2 | polish | Keep what you said | Every fact and ask stays: not the release, the campaign's households, existing households flat at 66% → 65.5%, and reporting by cohort. Nothing is added. | — | — |
| 3 | polish | Point first, plain words | The answer leads. The filler goes ("hope you're doing well", "just wanted to quickly circle back", "basically", "honestly", "pretty much"), and "let me know your thoughts" becomes a question she can answer with yes. | — | — |
| 4 | unslop | Cut the AI tells | The em dash and the chatbot sign-off go. Your plain, direct voice stays: professional, not stiff. | — | — |
| 5 | polish | Hand it back | Ready to paste. One fact from the readout would help, but you didn't write it, so it is offered below the rewrite rather than slipped in. | Send it, with or without the suggestion. | — |

**Artifacts**

`polish: for Priya on Slack`
```
Hi Priya, the engagement dip isn't the March release.
The referral campaign brought in many new households that rarely open the monthly view, which pulled the average down. Existing households are flat (66% → 65.5%).
From now on, I suggest we report engagement by sign-up cohort, so a change in the mix doesn't look like a drop. Does that work for you?
Could add: campaign households are now 24% of the base (from the readout)
```

**What it shows:** polish makes your own message clear and professional for its reader without changing what you said: every fact and ask stays, nothing is added behind your back, and the AI tells go.

---

## 31. `make-chart`: The engagement readout's chart

**When:** Any chart: for a readout, a PR or a dashboard.

**Typed:** `/diagnose-metric Engaged rate fell from 64% to 57% in March`

**How it starts:** Trigger: The agent, whenever it makes a chart; or you · When: The readout from diagnose-metric needs one chart · Router: Not involved · Skill: make-chart

The engagement readout says nothing broke: the mix of households changed. One chart has to make that obvious to people who will look at it for five seconds.

**Your decisions:** None

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | make-chart | Pick the form from the question | The question is "did behaviour change, or did the mix?", so it shows each group over time next to the blended rate, with the mix in its own panel, instead of one bar per month. | — | — |
| 2 | make-chart | Keep it honest | Rates on a 0–100% axis. The mix share gets its own panel rather than a second y axis, which would let the lines cross wherever the two scales happen to put them. | — | — |
| 3 | make-chart | Label and colour | Labels sit at the end of each line, so there is no legend to decode. The blended line is in the accent colour and the groups in muted tones, readable for colour-blind readers and in both themes. | — | — |
| 4 | make-chart | Title it with the claim | The title says what the chart shows, so the reader doesn't have to work it out. | — | — |
| 5 | review-result | Check the chart | Every plotted value matches the diagnosis, the axis starts at zero, and the title claims no more than the numbers show. Verdict: ready. | — | — |

**Artifacts**

`charts/engaged-rate-march.png`
```
Title: Each group is flat; the mix of households changed
Panel 1, weekly engaged rate: existing ≈ 66%, campaign ≈ 31%, blended 64% → 57%
Panel 2, campaign households' share of the base: 5% → 24%
Labels on the lines; no legend; 0–100% axis
```

**What it shows:** make-chart picks the chart from the question and puts the claim in the title; review-result then checks that the chart shows what the numbers say.

---

## 32. `second-opinion`: Is the de-duplication rule safe?

**When:** You want another model family's view on a diff, a plan or an idea.

**Typed:** `/second-opinion Is de-duplicating synced transactions on date, amount and reference safe?`

**How it starts:** Trigger: You type it; review-change and review-plan run it too · When: Before approving the bank-sync spec · Router: Not involved · Skill: second-opinion

The bank-sync spec de-duplicates on date, amount and bank reference. It looks right, but models from one family drafted it and grilled it. You want a different family's view before you approve it.

**Your decisions:** What to change in the spec

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | second-opinion | Prepare one input | Bundles the spec section, the prototype's de-duplication code and your question, so every model sees exactly the same thing. | — | — |
| 2 | second-opinion | Ask two other families | Sends it to Codex and to Google's Antigravity through their CLIs, as docs/sdlc/config lists them. Neither can edit anything. | — | — |
| 3 | second-opinion | Compare the findings | Shows where they agree and where only one of them saw a problem. Agreement is noted, never treated as proof. | — | — |
| 4 | grilling (spec) | Settle it | Real statements confirm both cases. The spec now also keys on the bank's transaction ID when there is one, and holds same-day duplicates with blank references for you to confirm. | Approve the amended spec. | Spec approved |

**Artifacts**

`second-opinion: de-duplication rule`
```
Both: two identical transfers on one day with blank references merge into one
Codex only: a refund reuses the payment's reference and could hide it
Antigravity only: nothing further
Next: check both cases against real statements
```

**What it shows:** second-opinion gets a genuinely different view by asking another model family, compares the answers without treating agreement as proof, and never changes anything itself.

---

## 33. `review-result`: Did bank sync hit its target?

**When:** Before a number, chart or analysis is reported or decides anything.

**Typed:** `/start continue bank sync: measure I-0009`

**How it starts:** Trigger: The agent, before reporting the success metric · When: Feature L's measure step, 60 days after release · Router: Resumes Feature L at measure · Skill: review-result

Bank sync's intent says 50% of active users link an account within 60 days. The raw query says 47%. Before that number keeps the intent open, the agent checks it.

**Your decisions:** None: the verdict follows the evidence

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | review-result | State the claim so it can fail | At least 50% of active users link an account within 60 days of sync reaching them. The raw query: 47%. | — | — |
| 2 | review-result | Check the denominator | Sync reached 10% of users first and everyone three weeks later. The query counted every active user, including those who have had sync for less than 60 days. | — | — |
| 3 | review-result | Rule out the rest | Counts active users as data-context defines them, which excludes staff and test accounts; checks that nobody is counted twice for linking two accounts (a join explosion); compares with the early 10% alone; and re-runs the query from a clean start. | — | — |
| 4 | to-intent | Close the intent | I-0009 moves from measuring to done, with the check attached so anyone can see how 53% was counted. | — | — |

**Artifacts**

`I-0009 note: result check`
```
Claim: ≥ 50% of active users link within 60 days
Raw: 47%, every active user
Fixed: only users with 60 days of sync: 53%
Early 10% alone: 54%; staff and test accounts excluded
Verdict: ready; target met
```

**What it shows:** review-result checks a number before it decides anything. Here the raw count would have kept a finished intent open.

---

## 34. `review-model`: Adopting the local categoriser

**When:** A change ships or replaces a model.

**Typed:** `/start continue I-0010 Local categoriser for frequent merchants`

**How it starts:** Trigger: The agent, in the change that ships a model, before review-change · When: Feature M for I-0010, before PR #83 is reviewed · Router: Inside Feature M · Skill: review-model

The Spike showed the hybrid categoriser clears the bar, and I-0010 is now built. Before the model takes over part of the LLM fallback for every user, review-model checks it the way it will be used.

**Your decisions:** Adopt, adopt with limits, or not yet

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | review-model | Check the split | The Spike's eval set sampled transactions at random, so the same household's merchants sat on both sides. The model will meet new households, so it re-splits by household and by time: 91.6% becomes 90.9%, still within 2 points of 91.4%. | — | — |
| 2 | review-model | Compare with baselines | On the new split, the current LLM fallback still scores 91.4% and rules alone 72%, as neither learns from the data; the local model alone drops to 88.2%, and the hybrid scores 90.9% at a third of the cost. | — | — |
| 3 | review-model | Look at slices | Results by bank and by amount are within about a point, except UPI transfers to people: 71%, because a person's name is not a merchant. | — | — |
| 4 | review-model | Calibrate and set the threshold | When the model says it is 90% sure, it is right 86% of the time. The threshold comes from what errors cost: below 0.8 confidence, the LLM decides. Accuracy rises to 91.8% and cost to ₹0.85 per user per month, still under ₹1. | — | — |
| 5 | review-model | Check training against serving | Training used merchant names from statements, but sync delivers them in another shape. The normaliser now runs before the model on both paths, and a test checks that both produce the same features. | — | — |
| 6 | review-model | Plan the monitoring | Weekly accuracy on 200 labelled transactions, and an alert if the share sent to the LLM leaves 15–35% or accuracy drops 2 points. | — | — |
| 7 | review-change | Then the usual review | review-change reviews the code with the verdict in the PR body, and review-feedback handles the comments. | Accept the limits, then merge. | Merge |

**Artifacts**

`docs/sdlc/changes/C-0026-local-categoriser/model-review.md`
```
By bank: 90–92%
Over ₹50,000: 90.1%
UPI to people: 71% → always sent to the LLM
```
`PR #83: model verdict`
```
Verdict: adopt with limits
UPI to people always goes to the LLM; threshold 0.8
Monitoring live before the rollout passes 10%
```

**What it shows:** review-model checks a model the way it will be used: a split that matches real users, the slices where it fails, a threshold set by what errors cost, and monitoring before the rollout.

---

## 35. `review-dependency`: A new package in the timezone fix

**When:** A change adds or upgrades a package, or a release is being prepared.

**Typed:** `/start Payments late on 31 January show up in February`

**How it starts:** Trigger: review-change, when the lockfile changes · When: Inside the month-end Bug fix · Router: Inside the Bug fix playbook · Skill: review-dependency

Fixing the month-end timezone bug, the agent added a package called tzfix-utils to convert times. review-change sees the lockfile change and runs review-dependency before anything merges.

**Your decisions:** None: the verdict goes in the PR

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | review-dependency | Measure the package | Scripts collect the facts rather than guessing them: registry data, maintainers, downloads and advisories. | — | — |
| 2 | review-dependency | Ask whether it is needed | Python's standard library has had zoneinfo since 3.9, and it does exactly this conversion. | — | — |
| 3 | review-dependency | Give the verdict | Rejected: a brand-new package with a look-alike name, for a job the standard library already does. The fix switches to zoneinfo, the package leaves the lockfile, and the verdict goes in the PR body. | — | — |
| 4 | ship | Back to the Bug fix | With no new dependency, review-change finishes and the fix ships. | Merge. | Merge |

**Artifacts**

`review-dependency: tzfix-utils`
```
First published 9 days ago; one maintainer with no other packages
41 downloads last week; no source repository linked
No advisories, because it is too new to have any
Name close to well-known timezone packages
```

**What it shows:** Agents add packages freely and sometimes pick look-alike names. review-dependency measures the package, asks whether it is needed at all, and records the verdict in the PR.

---

## 36. `review-feedback`: A teammate's PR comments

**When:** Review findings or PR comments arrive.

**Typed:** `/review-feedback PR #83`

**How it starts:** Trigger: You type it; the agent starts it on review-change findings · When: A teammate reviewed the local-categoriser PR · Router: Not involved · Skill: review-feedback

A teammate left three comments on PR #83, the local categoriser for frequent merchants, and a review bot left one.

**Your decisions:** The replies, before they are posted

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | review-feedback | Check each comment against the code | It verifies every claim before acting, the bot's included. | — | — |
| 2 | review-feedback | Draft the replies | One reply per thread: what changed, or the evidence for not changing it. Replies to people are messages, so they wait for you. | Approve the replies. | Messages to people |
| 3 | review-feedback | Post and confirm | Pushes the fixes, posts the replies and checks each thread shows its reply. | — | — |

**Artifacts**

`review-feedback: PR #83`
```
1 Cache never expires: valid; 24 h expiry and a test
2 Use a dict, not a list: valid; fixed
3 Model path hard-coded: not so; read from settings (line 41)
4 Bot: add type hints everywhere: outside this change; noted
```

**What it shows:** review-feedback neither agrees nor argues by reflex: each comment is checked against the code, and every reply carries its evidence.

---

## 37. `fix-ci`: A latency test fails only in CI

**When:** A CI check fails.

**Typed:** `/fix-ci`

**How it starts:** Trigger: The agent, inside ship; or you · When: CI on PR #83 goes red · Router: Not involved · Skill: fix-ci

ship pushes PR #83 and one check fails. ship hands the failure to fix-ci instead of retrying blindly.

**Your decisions:** None, unless three attempts fail

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | fix-ci | Read the failing check | Reads the log, not just the red badge: test_hybrid_latency fails only in CI, 410 ms against a 300 ms limit. | — | — |
| 2 | fix-ci | Reproduce and find the cause | With CI's settings locally, the first batch loads the model inside the timed section, because CI has no model cache. | — | — |
| 3 | fix-ci | Fix the cause, not the check | Loads the model in the test's setup, as production does at start-up. The 300 ms limit stays; nothing is skipped. | — | — |
| 4 | ship | Back to ship | With CI green, ship continues to the merge gate. | Merge. | Merge |

**Artifacts**

`CI, attempt 2`
```
test_hybrid_latency: 118 ms (limit 300 ms)
All checks green
```

**What it shows:** fix-ci fixes what made a check fail, never the check itself, and gives up with a report after three attempts instead of looping.

---

## 38. `architecture-health`: Structure review

**When:** The code is getting hard to change.

**Typed:** `/architecture-health`

**How it starts:** Trigger: You; the merge hook (first); milestone reviews · When: After about 20 merges; full sweep at milestones · Router: Comes after: your pick goes to /start · Skill: architecture-health

Merging C-0021 was the 20th change since the last health run, so the merge hook starts architecture-health, then code-health, as an AFK run. Neither looks at a window of recent changes: each picks about four areas from the health ledger. You can also type it any time, with an area or full. It never changes code itself. This is the run that produced the Refactor example.

**Your decisions:** Which candidate to pursue

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | coverage plan | Choose this run's areas | Reads the health ledger and the backlog, then fills a budget of four areas in priority order. No trouble signal has been raised since the last run, so that slot stays empty. | — | — |
| 2 | explore (subagent) | Look for friction | A subagent per area walks the code using the codebase-design vocabulary, GLOSSARY.md terms and the existing ADRs. In the parser, parse_statement is one 900-line function with a branch per bank, and its tests reach it only through upload. | — | — |
| 3 | report | Present candidates | Writes an HTML report outside the repo with a before-and-after diagram per candidate. | — | — |
| 4 | grilling + glossary | Grill your pick | You pick candidate 1. Grilling settles the interface: one BankAdapter per bank behind a registry. Adapter is design vocabulary and stays out of the glossary, but statement format, the layout each bank exports, is a project word and joins it. | Pick a candidate. | Your pick |
| 5 | → /start | Hand it to the router | The pick becomes /start Split the statement parser into one adapter per bank, which routes to Refactor. | — | — |
| 6 | health ledger | Record what was covered | Marks all four areas as reviewed at this commit, including the consent store, which had no candidates, and resets the merge count. Candidates 2 and 3 stay open, so later runs don't report them as new. | — | — |

**Artifacts**

`This run's areas (from the health ledger)`
```
1 monthly view    I-0005 budgets will build on it
2 none            no new trouble signals
3 consent store   G1; 2 merges since its last review
4 parser          most change: 14 merges since its last review
R upload          reviewed longest ago
```
`architecture-health.html (temp folder)`
```
1 parser: one adapter per bank             Strong
2 monthly view: merge two money helpers    Worth exploring
3 upload: one retry policy instead of 3    Speculative
  consent store: no candidates
Top recommendation: 1
```
`docs/sdlc/health-ledger.md (architecture-health)`
```
consent store   reviewed, no candidates
monthly view    candidate 2 open
parser          candidate 1 → Refactor
upload          candidate 3 open
Next in line: categoriser, sync worker
```

**What it shows:** architecture-health covers the whole codebase over time, whenever it runs: upcoming work, trouble signals, guardrails, change since each area's last review and a rotation slot share each run's budget. It finds structural work and never does it; your pick goes through the router like any other input.

---

## 39. `code-health`: Drift and decay check

**When:** Code, docs, comments or names feel out of date.

**Typed:** `/code-health`

**How it starts:** Trigger: You; the merge hook (second); milestone reviews · When: After about 20 merges; full sweep at milestones · Router: Comes after: each batch goes to /start · Skill: code-health

The same run continues with code-health. It runs the repo's health checks itself, so it needs no CI, then judges about four areas against REVIEW.md and checks them for drift. It skips the parser, which architecture-health has just sent to a Refactor. It changes nothing itself.

**Your decisions:** Which batches to pursue

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | health checks | Run the health checks | Runs make health itself across the whole repo, CI or not. Scripts are cheaper and more reliable than judgement for these. | — | — |
| 2 | coverage plan | Choose this run's areas | Reads the health ledger and fills a budget of four areas. The parser is skipped because it is about to be restructured, so its dead code is left to that Refactor. | — | — |
| 3 | drift check | Check docs, specs, comments and names | Reads each written description against the code it describes, in the chosen areas. | — | — |
| 4 | standards check | Judge the code against REVIEW.md | Clean-code standards, with the repo's precedence: a metric alone is never a reason to change code. | — | — |
| 5 | test audit | Audit the tests | Flags three snapshot tests of the monthly view that fail on every copy change and catch nothing verify-app doesn't. | — | — |
| 6 | escalate | Escalate structural causes | Two causes are structural. The categoriser and the sync worker each normalise merchant names their own way, and the monthly view reaches into the sync worker's internals, breaking the layers contract. Fixing either moves a boundary, so both go into the ledger as trouble signals for the next architecture-health run. | — | — |
| 7 | batch | Group findings into small batches | Each batch is small enough for one Feature S. Most touch one area; a rename touches every use. | — | — |
| 8 | → /start | Send your picks to the router | You pick A, B, D and E. Each goes in as /start and routes to Feature S; C stays open in the ledger. | Pick the batches. | Your pick |
| 9 | new health check | Make the lesson mechanical | A notebook that breaks silently is a mechanical problem that will recur, so code-health proposes a health check that runs every notebook. It is slow, so it runs per area. It goes in as its own Feature S. | — | — |
| 10 | health ledger | Record what was covered | Marks the four areas as reviewed at this commit, including the consent store, which had nothing to report, and records both escalations for architecture-health. | — | — |

**Artifacts**

`make health (whole repo)`
```
dead code: parser/legacy_csv_reader.py, 0 callers
README: make import-statement no longer exists
AGENTS.md: scripts/seed_db.py moved to tools/
naming: 14 names use txn (GLOSSARY.md says avoid)
imports: monthly_view uses sync_worker internals (layers contract)
complexity: categoriser _match_rule is 18 (REVIEW.md flags > 10)
```
`This run's areas (from the health ledger)`
```
1 monthly view    I-0005 budgets will build on it
2 categoriser     9 of the txn hits; 2 bug fixes since last run
3 consent store   G1; 2 merges since its last review
4 parser          skipped: Refactor raised in this run
R repo docs       reviewed longest ago
```
`drift`
```
runbook: still describes the old rollback script
monthly-view spec: lists CSV export, removed in C-0019
categoriser comment: 'rules run in file order', untrue since rules are sorted by priority
categoriser: says bucket where the glossary says category
notebooks/eval_categoriser.ipynb: imports a deleted module
```
`standards`
```
_score_merchant: 70 lines that normalise and score: split in two
_match_rule: ifs nested 5 deep: guard clauses
0.83 confidence threshold, unnamed, in two places: one named constant
get_txn_list(): one caller, adds nothing: inline it
build_totals(): 60 lines but one job: left as it is
```
`code-health report`
```
A Fix README, AGENTS.md and runbook
B Rename txn → transaction and bucket → category
C Categoriser: fix the comment; repair the notebook
D Categoriser: split, guard clauses, named threshold, inline wrapper
E Monthly view: update its spec; delete three snapshot tests
Escalated: merchant-name normalising; monthly view → sync internals
```
`docs/sdlc/health-ledger.md (code-health)`
```
categoriser     D picked; C open; escalation → architecture-health
consent store   reviewed, nothing found
monthly view    E picked; escalation → architecture-health
repo docs       A picked
Next in line: sync worker, upload
```

**What it shows:** code-health needs no CI: it runs the health checks itself, judges the chosen areas against the same standards review-change uses, checks docs, specs, comments, names and architecture for drift, and sends structural causes to architecture-health instead of patching them.

---

## 40. `retro`: After a slow session

**When:** A long or messy session just ended.

**Typed:** `/retro`

**How it starts:** Trigger: You type it · When: The recurring-payments session took most of a day · Router: Not involved · Skill: retro

The recurring-payments change was small, but the session dragged. codify captured what the change taught; you want to know why the work itself was slow.

**Your decisions:** Which fixes to make

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | retro | Read the session | Reads this session's transcript, using writing-for-agents for how any proposed text should read. | — | — |
| 2 | retro | Rank what slowed it down | Ranked by how much time each fix would have saved. | — | — |
| 3 | → /start | Act on your picks | You pick 1 and 3. The fast test command goes to /start as a Feature S; the AGENTS.md cut is checked by the agent-config evals. | Pick the fixes. | — |

**Artifacts**

`retro: recurring-payments session`
```
1 Full test suite after every edit, 12 min each: add make test-fast
2 Nine searches for where categories are defined: add a pointer
3 Three AGENTS.md lines change nothing: delete them
4 Read a 4 MB fixture file twice: exclude it from search
```

**What it shows:** retro learns from how the session went, while codify learns from what the change taught. Fixes favour a command or a check over more prose.

---

## 41. `to-skill`: Monthly release notes as a skill

**When:** You keep asking for the same workflow and want it repeatable.

**Typed:** `/to-skill draft user-facing release notes from the intents done this month`

**How it starts:** Trigger: You type it · When: The third month you asked for release notes by hand · Router: Not involved · Skill: to-skill

Every month you ask the agent for release notes from the intents that reached done. The prompts drift each time, so you want a skill.

**Your decisions:** The name, the trigger and the eval cases

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | to-skill | Check it should be a skill | It needs judgement about what users would notice, so a script can't do it, and no existing skill does. | — | — |
| 2 | to-skill | Name and trigger it | release-notes clashes with no harness name or naming rule. It is typed, because you want it monthly, not whenever the agent guesses. | Agree the name and trigger. | — |
| 3 | writing-for-agents | Write the body | Steps, a done condition and pointers to the intents, not copies of them. | — | — |
| 4 | to-skill | Write the evals | Three cases from earlier months, run with and without the skill. | — | — |
| 5 | review-skill | Check it before trusting it | No risky scripts or secrets; no harness reserves the name; and its description overlaps none of yours. The closest, technical-writing, shapes any document; this one decides what users would notice. | — | — |

**Artifacts**

`.claude/skills/release-notes/SKILL.md`
```
name: release-notes
description: Draft user-facing release notes from intents moved to done
disable-model-invocation: true
```
`evals/skills/release-notes/`
```
1 Three intents done → three plain bullets, no jargon
2 A dropped intent → not mentioned
3 A guardrail change → stated as what users gain
```

**What it shows:** to-skill makes a skill only when a check can't do the job, names it by the rules, ships it with evals so later edits are tested, and passes it through review-skill.

---

## 42. `review-skill`: A monthly skills sync

**When:** You adopt a skill, or sync your forks from upstream.

**Typed:** `/review-skill this month's upstream updates, and Anthropic's debug skill`

**How it starts:** Trigger: Every skills sync and to-skill; or you · When: Monthly sync of your forked skills · Router: Not involved · Skill: review-skill

This month's sync found upstream changes to six of your forked skills, and you are also considering Anthropic's debug skill. Nothing is adopted until review-skill passes it.

**Your decisions:** Whether to accept what it flags

| # | Skills | Step | What happens | You | Gate |
|---|---|---|---|---|---|
| 1 | review-skill | Scan the updates | A script checks each changed skill for prompt injection, risky commands and secrets; the agent judges what it flags. | — | — |
| 2 | review-skill | Check the newcomer for overlap | Compares the debug skill's description with yours. It reproduces, isolates and fixes bugs: the same moment as diagnose-bug. | — | — |
| 3 | you | Decide | You agree: diagnose-bug waits for a pinned version upstream, and the useful checklist lives on inside diagnose-bug. | Confirm both calls. | — |

**Artifacts**

`review-skill: upstream updates`
```
5 updates clean: synced to their new pins
diagnose-bug: a new step downloads and runs a tool without pinning its version
→ diagnose-bug stays at its old pin; the reason goes in its PROVENANCE
```
`review-skill: Anthropic debug`
```
Overlaps diagnose-bug: same trigger, something is broken
New in it: a 'works in staging, not in prod' checklist
→ not adopted; the checklist moves into diagnose-bug's local.md
```

**What it shows:** review-skill keeps your skills safe and free of duplicates: an unsafe update stays at its old pin, and a newcomer that does the same job as a skill you have is merged into it instead of added.
