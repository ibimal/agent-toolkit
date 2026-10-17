# AI-native SDLC workflow

Living reference for how development work runs with AI agents, skills and coding assistants. It states the current rules only; when a rule changes, edit it in place.

Companions: worked examples of every playbook and of the skills outside them in [examples.md](examples.md), played as animated walkthroughs in [walkthroughs.html](walkthroughs.html) (open it in a browser). Both are generated from `src/`; see [README.md](README.md).

Last updated: 2026-10-17

---

## 1. Guiding principles

1. **Align before building.** Every non-trivial change starts by grilling: the agent asks only the questions it can ask now, each with its recommended answer, round by round until every branch is resolved. Every term it settles goes straight into the glossary.
2. **You own the why; the agent drafts the rest.** The product brief and intents are yours. Architecture, specs, designs, plans and code are drafted by the agent and judged by you.
3. **The repo is the memory and the audit trail.** Each step writes a committed artifact that the next step reads. Every PR traces to a change, every change to an intent, and every intent to a product outcome.
4. **Depth follows the work.** The router picks a playbook by the number of outcomes, the work type and the size. No ceremony by habit.
5. **Humans decide preferences and irreversible actions.** Everything reversible proceeds and reports evidence.
6. **Experiment before asking.** A throwaway prototype answers design questions; you are asked only for calls no experiment can settle.
7. **Vertical slices, never layers.** An application grows from a walking skeleton, capabilities are outcomes a user would notice, and changes are small end-to-end slices that each end in a check.
8. **Done means evidence.** Proof comes from the real artifact (tests, runs, outputs), never from the agent's assertion.
9. **The writer never approves its own work.** Review happens in a fresh context, by another model family when one is available.
10. **Subtract before adding.** Prefer deletion and the smallest change; tidy before review.
11. **Must-hold rules are deterministic.** Hooks and CI enforce what must always be true; skills guide what should be true.
12. **Agent-ready before autonomous.** Agents run in parallel or AFK (with nobody watching) only once CI, deploy and `verify-app` can catch their mistakes and a guard blocks destructive commands.
13. **Every change makes the next one easier.** Lessons become lints, tests, hooks or skill edits before they become prose.
14. **Close on outcomes, not merges.** An intent is done when its success metric has been checked after release; a milestone is reviewed against the product metrics.
15. **Skills are small, composable and portable.** They work across harnesses; you own their names and triggers.

---

## 2. How you use it

You type 23 skills, but three cover most days: `/start` for any piece of work, `/huh` when something doesn't land, and `/polish` before you send anything. When what you bring is a need rather than work, `/start` names the skill that meets it, so you never have to remember the rest. Everything else runs for you, inside a playbook or when the agent needs it.

### 2.1 What you type

| Moment | Type | When | How often |
|---|---|---|---|
| Start | `/start <request>` | Any piece of work. On its own, it shows what is in progress, what waits for you and what to do next | Daily |
| Stay on track | `/huh` | You don't follow the last message or the question it asks you (`/huh Q2` picks one of several), or you are back and need catching up | Daily |
| | `/readback` | Before the agent builds something big, to check it understood you | Weekly |
| | `/handoff` | You stop part-way through, or switch devices | Weekly |
| | `/afk` | You are stepping away and want the work to carry on | Weekly |
| Understand | `/how` | How code works, or where something belongs: the answer is in the code | Weekly |
| | `/why` | Why code is the way it is: the answer is in the history (commits, PRs, intents, ADRs) | Weekly |
| | `/explore-data` | What a dataset holds before anyone uses it: the answer is in the data | Weekly in data work |
| | `/diagnose-metric` | Why a metric moved: the answer is in the data, once the data itself is ruled out | Weekly in data work |
| | `/look-up` | A fact from outside the repo: docs, APIs, specs | Weekly |
| | `/learn` | A topic you want to master over several sessions | Now and then |
| Decide | `/brainstorm` | You need ideas, not yet an idea: a new project, a feature area, an improvement plan | Weekly |
| | `/wayfinder` | Open decisions need more than one session | Now and then |
| | `/size-impact` | Before deciding whether something is worth building, or when choosing between options at planning | Weekly at planning |
| | `/preregister` | Before an experiment, A/B test or model comparison decides something | Per experiment |
| Share | `/to-questionnaire` | Someone else holds the answer | Now and then |
| | `/technical-writing` | A doc, README, RFC or PR description for people | Weekly |
| | `/polish` | A message, email, comment or post you wrote, before you send it as yourself | Daily |
| Check | `/second-opinion` | You want another model family's view on a diff, a plan or an idea | Weekly |
| Improve | `/architecture-health` | The code is getting hard to change | Now and then |
| | `/code-health` | Code, docs, comments or names feel out of date | Now and then |
| | `/retro` | A long or messy session just ended | Weekly |
| | `/to-skill` | You keep asking for the same workflow | Now and then |

**Choosing within a moment:**

| Moment | Pick by |
|---|---|
| Stay on track | You don't follow the agent → `huh`. The agent may not follow you → `readback`. You'll pick the work up in a later session → `handoff`. The work should carry on without you → `afk`. `/huh` catches you up on this session; `/start` on its own shows all your work |
| Understand | Where the answer lives: the code → `how`; its history → `why`; a dataset → `explore-data`; a number that moved → `diagnose-metric`; outside the repo → `look-up`; a whole topic → `learn` |
| Decide | No idea yet → `brainstorm`. Is an idea worth it → `size-impact`. How to test it → `preregister`. Too many open decisions for one session → `wayfinder`. Once you have an idea, `/start` grills it into shape. `brainstorm` finds what you could do; `look-up` finds what is true |
| Share | A message you'll send as yourself → `polish`. A document people will read → `technical-writing`. A question only someone else can answer → `to-questionnaire` |
| Improve | The code's structure → `architecture-health`. Its hygiene and drift → `code-health`. How a session went → `retro`. A workflow you keep repeating → `to-skill` |

### 2.2 What runs for you

```
Playbook writers   to-product · to-backlog · to-intent · to-spec · to-design · to-tickets
Playbook steps     setup · review-plan · implement · ship · release-readiness · codify
Agent helpers
  Align            grilling · glossary · codebase-design · prototype
  Build            tdd · diagnose-bug · tidy · fix-ci
  Prove            verify-app · review-change · review-feedback · blast-radius · review-result · review-dependency · review-skill · review-model
  Write            writing-for-agents · unslop
  Data             data-context · write-notebook · make-chart

Playbooks (loaded by /start)
  New application · Feature S · Feature M · Feature L · Bug fix · Refactor · Spike · Incident
```

You can type any of these yourself, for example to redo a step, but you never need to.

### 2.3 How a skill starts

- **Typed only:** a slash command with plain text after it and no quotes, for example `/start Show me all my recurring payments`. It never starts on its own (in Claude Code, `disable-model-invocation: true`), so its description costs no context until you type it. Typed only: `start`, `huh`, `readback`, `handoff`, `how`, `why`, `learn`, `brainstorm`, `wayfinder`, `to-questionnaire`, `technical-writing`, `polish`, `retro`, `to-skill`.
- **Agent-startable:** the agent starts it when a task fits its description, when a playbook step needs it, or when another skill calls it; you can type it too. Any skill a playbook or another skill runs must be agent-startable. Its description loads in every session, so it has to earn that (10.3). Nine of the skills you type are agent-startable as well, and their descriptions name the only moments they start without you:
  - `afk`, when a run will have nobody watching;
  - `architecture-health` and `code-health`, from the merge hook or a milestone review;
  - `preregister`, before an experiment decides something;
  - `explore-data`, when a new dataset arrives;
  - `diagnose-metric`, inside an Incident for metric drift, or when a measured success metric misses or moves unexpectedly;
  - `size-impact`, at milestone planning and when intents compete for a cut (4.1); for an idea whose value is unclear, `/start` suggests it and you type it;
  - `second-opinion`, inside `review-change`, `review-plan` and `brainstorm`;
  - `look-up`, from a `wayfinder` ticket or when a decision needs an outside fact.
- **Hooks:** the merge hook starts `architecture-health`, then `code-health`, once enough changes have merged (4.3); an alert hook sends alerts to `/start`. Every run a hook or scheduled task starts loads `afk`, and so does `/start` when you say you are stepping away, so a run nobody watches never depends on the agent noticing.

---

## 3. Routing

`start` classifies every input, checks it against the product brief and the intent backlog, and picks a playbook. You can override.

| The input brings | Playbook |
|---|---|
| Several new outcomes in an empty repo (a new product) | New application |
| Several new outcomes in an existing product, or the next milestone | New application, expansion variant |
| One new or changed outcome | Feature S, M or L by size |
| Something behaving wrongly | Bug fix |
| A structure change with behaviour unchanged | Refactor |
| A question to answer, an option to explore, or an analysis whose answer decides something | Spike |
| An alert, failed pipeline or metric drift | Incident |

**Feature size:**

| Size | Test |
|---|---|
| S | The diff can be described in one sentence and the blast radius is small |
| M | A feature inside one area of the system |
| L | Several units, new architecture, or high risk: security, money, data contracts, model behaviour |

**Intake:**
- **A repo that isn't set up yet** (no `docs/sdlc/config`) is set up first, so `/start` is the only command a new repo needs: `start` runs `setup`, says what it will add, and asks one question, which tracker to use. In a repo that already has code, `setup` runs the adoption path (4.6) once, and the request then routes as usual. On a device or harness the config doesn't list yet, it runs setup's model check the same way.
- Every input is matched against existing intents and becomes a new intent, an amendment, a duplicate, or a replacement for an older intent. You confirm.
- When a product brief exists, an input that serves no product outcome or guardrail is flagged as possible scope creep.
- Input about work already in progress, for example `/start continue recurring payments`, resumes that change's playbook at its next step and reads its handoff if there is one.
- **On its own**, `/start` lists the work in progress with each one's next step, what waits at a gate for you, open health batches, `data-context` proposals and the next backlog intent, then suggests one thing to do.
- **Needs, not work.** When the input asks for understanding, ideas or a judgement rather than a change, `start` names the skill from 2.1 instead of loading a playbook: "I don't follow" or "what happened while I was away" → `huh`; "why is this built like that" → `why`; "why did this number drop" → `diagnose-metric` (an Incident runs it itself when an alert caught the drift); "give me ideas for" → `brainstorm`; an idea whose value is unclear → `size-impact`, before it becomes an intent.

---

## 4. Playbooks

A playbook is a fixed sequence of skills. `start` copies its steps into the task list, and a skipped step stays in the list with a one-line reason. New application is composite: its steps run other playbooks. The skills around the playbooks (`wayfinder`, `handoff`, `afk` and the two `-health` skills) are never a route of their own; 4.2 to 4.4 say how they work, and 4.5 holds the rules for every other skill outside the playbooks. 4.6 says how an existing project adopts the workflow.

| Playbook | Sequence | Human gates | Artifacts |
|---|---|---|---|
| New application | See 4.1 | Brief, MVP intents and cut, architecture, skeleton spec and merge, per-playbook gates, prod | `product.md`, backlog, `architecture.md`, ADRs, skeleton, runbook |
| Feature S | implement (tdd where a seam exists) → tidy → verify-app → review-change → ship → codify if there is a lesson | Merge | PR body with one-line intent and evidence |
| Feature M | grilling (intent) → to-intent → to-spec → grilling (spec) → to-tickets → implement → tidy → verify-app → review-change → ship → codify → measure the success metric (review-result) | Intent, spec, merge | Intent, `spec.md`, `plan.md`, PR |
| Feature L | grilling (intent) → to-intent → to-spec → grilling (spec) → prototype (open questions) → to-design (with a threat model when the change crosses a trust boundary) → to-tickets → review-plan → implement in parallel worktrees → tidy → verify-app → review-change → ship (staged) → codify → measure the success metric (review-result) | Intent, spec, design + plan, merge, prod | Full chain; one intent may span several changes; a `/wayfinder` map when open decisions span sessions (4.2) |
| Bug fix | diagnose-bug (reproduce on the same surface, minimise, hypothesise, instrument) → failing regression test → fix → find other instances of the same cause → verify-app → review-change → ship → codify | Merge | `bugfix.md`, regression test |
| Refactor | blast-radius → to-tickets (behaviour-preserving steps; migrate callers, then delete the old API) → implement → verify-app (behaviour unchanged) → review-change → ship | Merge | `plan.md` |
| Spike | grilling (frame the question; agree the bar) → explore-data (when data is involved) → preregister (when the answer is a number) → prototype (a throwaway marimo notebook through write-notebook, or a branch) → review-result → findings or ADR → decide: stop, share the findings, or re-enter as M or L | The bar, the decision | `findings.md` or ADR, plus `profile.md` and `preregistration.md` when used; nothing ships |
| Incident | deterministic detection, whose hook sends the alert to start → diagnose-bug (read-only), or diagnose-metric when a metric drifted → small fix via Bug fix, or an agent-raised intent | As routed | Incident note, new eval case |

- `implement` works per slice: tdd at the agreed seams → verify the slice → commit.
- **Every grilling runs `glossary` alongside it**, so a term settled in conversation lands in `GLOSSARY.md` at once. Every playbook reads the glossary; the table below says where each one changes it (lifecycle in 6.5).
- **Review** runs as section 8 says: `review-model` first when the change ships a model, then `review-change`, which runs `second-opinion` for rung 1 and `review-dependency` when packages change.
- **Data work reads `data-context` before any query and writes back what it learns** (6.6); `ship` adds the tables, columns, events and metric queries a merged change introduces.
- An intent already accepted, for example in a New application backlog, starts its Feature M or L playbook at to-spec. If a product amendment has flagged it, it is re-grilled first.

**The glossary in each playbook:**

| Playbook | Glossary |
|---|---|
| New application | Created while grilling the product brief, with its first settled terms; grows with every grilling after that |
| Expansion variant | The new area's terms are added while the brief is amended |
| Feature S | Read only. If the change needs a new term, `glossary` proposes it and you confirm it before merge |
| Feature M | Updated while grilling the intent and the spec |
| Feature L | Updated while grilling the intent and the spec, and when `to-design` or a `wayfinder` ticket names a new concept |
| Bug fix | Read. If the cause was one word used two ways, `codify` settles the word in the glossary |
| Refactor | Read. A rename changes the glossary first; the old word moves to _Avoid_ |
| Spike | Updated while framing the question, and when the findings name something new |
| Incident | Read; the incident note uses its terms |

### 4.1 New application

**When:** a new product: an empty repo and several outcomes. **Ends:** at the first milestone release. Each later milestone runs as the expansion variant; single-outcome work routes normally.

| Step | Skills | Exit criteria | Gate |
|---|---|---|---|
| 1 Setup, first pass | setup (stack-agnostic) | Docs layout, tracker decision and reviewer ladder committed; `AGENTS.md`, `CLAUDE.md` and `REVIEW.md` stubs exist; destructive-command guard active; no empty glossary is created | — |
| 2 Product brief | grilling (product level) → to-product | `product.md` states vision, users, problems, outcomes with metrics, guardrails, constraints, non-goals, riskiest assumptions and milestones, with the MVP defined by the outcome it proves; `GLOSSARY.md` created with the first resolved terms | Brief accepted |
| 3 Backlog | to-backlog → size-impact (when intents compete for the cut) → grilling and to-intent for each MVP intent → review-plan (scope challenge on the MVP) | Every MVP intent accepted, traced to a product outcome, with a success metric and its dependencies; later intents proposed with a one-line outcome; open technical decisions listed, and charted with `/wayfinder` when they need more than one session | MVP intents, cut and order |
| 4 Architecture | Spike, or the `/wayfinder` map's tickets, for each decision that is expensive to reverse → ADR; to-design (system) → review-plan | Every open decision resolved by an ADR or deferred with a reason; `architecture.md` covers components and boundaries, core data model, integrations, environments and deployment, testing and verification approach, and observability; every product constraint maps to a choice | Architecture accepted |
| 5 Walking skeleton | setup (stack pass) → to-spec (thinnest slice of the first MVP intent) → to-tickets → implement (one stream; writes `verify-app`) → tidy → verify-app → review-change → ship to staging | One command builds and tests from a clean clone; CI green; staging deploy and rollback each run once; hooks active; agent-readiness check passes | Spec, merge |
| 6 Build | start for each MVP intent in dependency order → Feature S, M or L | All MVP intents merged; living specs and `architecture.md` current | Per playbook |
| 7 Release | release-readiness → ship to prod (staged) → measure (review-result) | Readiness check passes; post-deploy check passes; MVP intents move to measuring; milestone review scheduled | Prod |

**Rules:**
- **Outcomes, not layers.** Each capability intent is something a user or operator would notice once it's done. "Build the API" is not an intent.
- **Size before cutting.** When intents compete for the MVP or a milestone, `size-impact` sizes each the same way and the cut uses the ranges.
- **Detail just in time.** Only MVP intents are grilled up front. Later intents stay proposed with a one-line outcome and are grilled when picked up.
- **Backlog before architecture.** Intents describe outcomes and don't depend on the architecture; the architecture is chosen to serve the MVP intents.
- **Spike only what is expensive to reverse:** runtime and framework, primary data store and core data model, identity and tenancy, hosting and deployment, external contracts, and any model component. Everything else gets a sensible default recorded as a provisional ADR.
- **Model and data components:** the architecture step fixes the eval set, quality thresholds and data contracts. They become part of `verify-app`.
- **Setup runs twice, as playbook steps.** The first pass needs no stack. The second runs once the stack is chosen and fills in commands, format and lint hooks, the verify command, the health checks, the `REVIEW.md` standards and CI where wanted.
- **The skeleton is a real slice.** It is the thinnest slice of the first MVP intent, built and deployed end to end, not a throwaway hello-world.
- **The riskiest assumption picks the skeleton.** If it is about the architecture, build a walking skeleton through the target architecture. If it is about value, build a skeleton on crutches: the real interface over stand-in services, replaced behind the interface later.
- **Agent-readiness check:** a fresh agent session, given only the repo, states the commands, conventions and architecture and runs `verify-app` successfully. The check is kept as the first case in the eval suite.
- **Parallel only after the skeleton.** In step 6, independent intents run in parallel worktrees, capped by how many you can review properly. Intents that need the same new foundation are sequenced by a dependency, and the foundation is built inside the first of them.
- **Hardening is a check, not a phase.** NFRs are in every spec from the start; `release-readiness` verifies them across the whole application.
- **After the release:** the milestone review (section 9) measures the product metrics and amends `product.md` and the backlog; the next milestone runs as the expansion variant.

**Expansion variant** (a major new area in an existing product, or the next milestone): step 2 as an amendment to `product.md` → step 3 for the new area or milestone, whose intents take the place of the MVP → step 4 only if the area needs new architecture → steps 6 and 7. If the repo has no product brief, `setup` drafts one from the code and docs first.

### 4.2 Skills around the playbooks

These are not routes. The router never picks them; they start the way the table says and hand their result back to a playbook or to `/start`.

| Skill | Trigger | Use it when | Produces | Hands back to |
|---|---|---|---|---|
| `wayfinder` | You type it; Feature L and New application suggest it | Open decisions need more than one session before a spec or design can be written | A map with a destination, decisions so far, fog and out-of-scope, plus one ticket per open decision (research, prototype, grilling or task) | The paused playbook's next writer, usually to-spec or to-design |
| `handoff` | You type it; the agent suggests it when the context runs long | You stop part-way through a playbook or switch devices | A note of what the next session needs that is not written down elsewhere, plus suggested skills | `/start continue …`, which resumes the playbook |
| `architecture-health` | You type it, any time; the merge hook runs it first; each milestone review runs a full sweep | The code's structure is making change hard: where module boundaries sit, whether each module hides enough behind a simple interface, how tightly modules depend on each other, conflicts with ADRs or with the architecture standards in `REVIEW.md` | Ranked restructuring candidates with before-and-after diagrams, then grilling on the one you pick; it never changes code | `/start` with your pick, usually a Refactor, or a Feature L if contracts or data change |
| `code-health` | You type it, any time; the merge hook runs it second; each milestone review runs a full sweep | The code no longer meets the standards in `REVIEW.md`, or its docs, specs, comments, names or architecture have drifted from it (4.4) | Findings grouped into small batches, plus proposed health checks for mechanical problems that recur; it never changes code | `/start` with each batch you pick, usually a Feature S or a Refactor |
| `afk` | You type `/afk` or say you are stepping away; `/start`, hooks and scheduled tasks load it for every run nobody watches | Nobody will watch the run | A readiness check, work that holds every human gate, and a run trail: one row per default picked and gate held, with evidence, audited against the transcript, reviewed by another model family, and topped by a hand-back | You, when you return: the hand-back lists what finished, what waits at which gate, and which rows to check first |

**Rules:**
- **`wayfinder` plans; it doesn't build.** It works one ticket per session, except AFK research tickets, which `look-up` resolves in parallel. The map is done when nothing is left to decide before the playbook can continue.
- **Every `wayfinder` ticket is HITL or AFK.** HITL tickets (grilling, prototype) are worked with you and resolve only in a live exchange; the agent never answers its own questions. AFK tickets (research) are driven by the agent alone. A task ticket is AFK when the agent can do it, otherwise HITL with a checklist for you.
- **A handoff never copies.** It points at the spec, plan, commits and ADRs by path and redacts secrets. It is deleted once the change merges.
- **`afk` starts with readiness.** It runs only when CI, deploy, `verify-app` and the destructive-command guard exist (principle 12); otherwise it reports what is missing and stops.
- **`afk` holds every gate.** It never approves on your behalf, and a HITL ticket counts as a gate. At a gate it parks that task and moves to other unblocked work; when none is left, it stops.
- **Defaults instead of questions.** With nobody to ask, the agent picks the default for each ambiguous choice and logs it with its evidence, so review moves to the end instead of disappearing. A preference call or an irreversible action (section 5) is a gate, never a default, and so is what a word or a metric means: a term or definition that needs settling waits in the hand-back (6.5, 6.6).
- **The trail is checked before you see it.** An audit against the transcript appends any decision the log missed, never editing earlier rows, and a model from another family flags rows whose evidence is missing.
- **Structure or hygiene:** if fixing a finding would move a module boundary or change an interface, it belongs to `architecture-health`; anything else belongs to `code-health`. `code-health` escalates structural causes, such as the same logic duplicated across modules, instead of patching them.
- **Two skills, one run:** when the merge hook or a milestone starts them, `architecture-health` runs first, so `code-health` skips code that is about to be restructured. 4.3 says when they run and what they look at.
- **`code-health` needs no CI.** It runs the repo's health checks itself and adds the judgement scripts can't make (4.4). CI or git hooks may run the same checks between runs; that only finds problems sooner.

### 4.3 When the `-health` skills run and what they look at

Neither skill is scoped by time. Whenever one runs, whether you type it, the merge hook starts it or a milestone review runs it, it reads the health ledger and picks its areas from the state of the code, never from a window of recent changes. Scoping to recent changes misses three things: cold code is where dead code, stale docs and broken notebooks pile up; upcoming work often lands in code that is cold today; and guardrail code is expensive to get wrong. A deep review of everything on every run is also wrong: it costs too much and buries you in findings. So each run splits the work:

- **Mechanical checks cover the whole repo, every run.** They are the repo's health checks, which `code-health` runs itself; they cost almost nothing.
- **Judgement covers a few areas per run**, a budget of about four, chosen in this order:

| Priority | Areas | Why |
|---|---|---|
| 1 | Areas the next intents in the backlog will touch | Improve the ground before building on it |
| 2 | Areas with trouble signals raised since the last run: health-check hits, incidents, repeated bug fixes, escalations from `code-health` | Evidence that something is wrong |
| 3 | Guardrail areas (privacy, money, security, model behaviour) changed at all since their last review | A miss costs the most there, so even a small change earns a look |
| 4 | Other areas with the most change since their last review | Drift grows with change |
| Reserved | The area reviewed longest ago | Cold code is never skipped for long |

Change since an area's last review is counted from the commit the ledger recorded for that review, so it is the same whenever the skill runs.

**When they run:**
- **You, any time.** Name an area, for example `/code-health categoriser`, or ask for `full`.
- **The merge hook:** after each merge, `ship` counts the merges on main since the commit the ledger recorded. The count comes from git, so every merge counts however it was made; a post-merge git hook, or a CI job where there is CI, can run the same count. At about 20, it starts `architecture-health`, then `code-health`, as an AFK run; the report waits for your pick. Drift grows with change, not with time, so busy periods get more runs and quiet periods get none. Tune the number so each report stays small.
- **Each milestone review:** both skills do a full sweep with no budget, and their findings feed backlog refinement for the next milestone.
- **Adoption:** when an existing project adopts the workflow, both skills do a full sweep, so the health ledger starts with every area (4.6).

**Rules:**
- **Coverage is guaranteed by runs, not dates.** The reserved slot reaches every area within as many runs as there are areas, and the milestone sweep covers everything once per milestone.
- **Areas** are the components named in `architecture.md`, plus repo-level docs as one area; without an `architecture.md`, the top-level folders.
- **The health ledger records coverage:** for each area and each skill, the commit of its last review, what was found and what is still open, plus the merge count since the last run. Each run marks every area it reviewed, including those with no findings. Findings you didn't pick stay open, so later runs don't report them as new.
- **Upstream difference:** upstream's architecture skill looks first at recently changed code. Our overlay replaces that with this plan, and change becomes one input among five, measured per area since its last review.

### 4.4 What `code-health` checks

`code-health` works the same with or without CI. Each run checks the code against shared standards and checks every kind of written description of the code for drift.

**The run:**
1. **Health checks, whole repo.** It runs the command named in `docs/sdlc/config` (`make health` by default). If the repo has none yet, it runs the language's standard tools directly and reports the missing command as a finding. For Python, for example: ruff, a type checker, vulture, import-linter, deptry and a secrets scanner. Slow checks, such as running notebooks or documented commands, run only for the chosen areas.
2. **Choose areas** by the coverage plan (4.3).
3. **Judge each area** against the standards below, and check it for the drift in the table after them.
4. **Sort the findings.** A fix that would move a boundary or change an interface escalates to `architecture-health`. A mechanical problem that recurs becomes a new health check. Everything else goes into small batches, one area each.
5. **Record coverage** in the health ledger.

**Standards.** They live in `REVIEW.md`. `setup` starts it from this baseline and the repo tunes it. `tidy` and the standards axis of `review-change` read the same file, so new code and old code are judged alike.

| Topic | What `code-health` looks for | Source |
|---|---|---|
| Names | Names that say what a thing is for; one term per concept, matching `GLOSSARY.md`; no vague names (`data`, `tmp`, `helper`, `manager`) and no names that lie | Clean Code; the glossary |
| Functions | One job at one level of abstraction; no flag arguments; few parameters; no hidden side effects; guard clauses instead of deep nesting; named constants instead of magic numbers | Clean Code; Fowler's code smells |
| Simplicity | Dead and commented-out code; speculative generality; one-caller wrappers and pass-through layers; the same logic written three times | Fowler; *A Philosophy of Software Design* |
| Modules | Deep modules with small interfaces; no feature envy, data clumps, primitive obsession or god modules | *A Philosophy of Software Design*; `codebase-design` |
| Architecture | Dependencies point inward: domain logic never imports frameworks, I/O or storage; a pure core with I/O at the edges; no import cycles; the boundaries `architecture.md` names | Clean Architecture's dependency rule |
| Errors and types | No swallowed errors or bare `except`; validation at system boundaries; typed public functions | Clean Code; PEP 484 |
| Tests | Tests call the code the way its users do; no test that would pass if every function returned nothing; no flaky or long-skipped tests | gstack `test-audit`; pstack principles |
| Security | No secrets in code; credentials never held in types whose `repr` or dump is generated; no logging or tracing of whole objects; untrusted input validated at the boundary | Sentry `secret-serialization` |
| Style | The language's standard style, enforced by its formatter and linter | For Python, PEP 8 and the Google Python Style Guide |

`REVIEW.md` also sets the thresholds that raise a signal. The defaults are cyclomatic complexity over 10, functions over about 50 lines, and more than 5 parameters.

**When standards disagree:** the repo's own rules win (`AGENTS.md`, `REVIEW.md`, ADRs), then the deep-module vocabulary, then general guidance such as Clean Code. Where "keep functions small" would produce shallow pass-through code, deep modules win. A metric is a signal, never a reason on its own: split a function because it does two jobs, not because it is long.

**Drift:**

| Drift | Compared | Health checks catch | Judgement catches |
|---|---|---|---|
| Docs | README, runbook, `AGENTS.md`, docstrings vs the code | Referenced files, symbols and links that no longer exist; documented commands that fail | Text that no longer describes what the code does |
| Living specs | Each requirement vs the code's behaviour | — | Requirements the code contradicts or no longer meets, and behaviour no spec describes |
| Comments | Each comment vs the code beside it | Commented-out code; stale TODOs | Comments describing old behaviour or restating the code; a missing "why" where the code is not obvious |
| Architecture | The code vs `architecture.md` and the ADRs | Import contracts: layers, forbidden imports, cycles | Responsibilities in the wrong module; ADR decisions not followed. Fixes escalate to `architecture-health` |
| Naming | Identifiers vs `GLOSSARY.md` and the style guide | Synonyms the glossary says to avoid; style-guide naming | One term for two concepts; new concepts missing from the glossary |
| Dependencies | Declared vs imported | Unused and missing dependencies | — |
| Notebooks | Notebooks vs the current code | Notebooks that no longer run (per area) | Results that no longer match what the code now produces |
| Metrics | Queries, dashboards and notebooks vs the definitions in `data-context` | — | A metric computed differently from its definition; a definition nothing uses any more |

### 4.5 Everyday skills

2.1 says when to type each one. These rules say how they behave, grouped by the same moments, and how the skills that run for you behave outside a playbook step.

- **Fold the rule, keep the skill.** Where a habit belongs inside a workflow step, the step carries it, and the skill stays for when you need it on its own:
  - grilling gives every question a one-line "why it matters" and ends with a readback;
  - `review-change` runs `second-opinion` for rung 1 and `review-dependency` when packages change, and the writer acts on its findings through `review-feedback`;
  - `ship` hands a failing check to `fix-ci`;
  - `technical-writing` and `polish` run `unslop`;
  - Spike runs `explore-data`, `preregister` and `review-result`, and every success-metric measurement runs `review-result`;
  - every data skill reads `data-context` before it queries and writes back the facts it learns; notebooks are written by `write-notebook` and charts by `make-chart`;
  - `to-skill` and every skills sync run `review-skill`.

**Stay on track**

- **`huh` explains; it never re-decides.** It keeps every caveat, adds no claim the original didn't make, and says so when the original was wrong. With `Q2`, a passage, a file or a link after it, it explains just that. With nothing after it, it explains what is waiting on you, checking in this order:
  1. a lot has happened since you last wrote: a catch-up, with what changed for you, then each decision waiting on you with a recommendation;
  2. the last reply asks you one question: that question, with what is being decided, why it matters, what each answer leads to, and the recommendation;
  3. it asks several: each in a plain line or two, numbered as asked, so you can pick the one to go deeper on with `/huh Q2`;
  4. it asks nothing: the last reply in plain words.

  `/huh` covers this session since your last message; `/start` on its own covers all your work.
- **Questions are numbered** whenever a reply asks more than one, so `/huh Q2` can point at one. Grilling does it by design. For every other reply the rule sits in the `AGENTS.md` that `setup` writes, because `huh` loads only when you type it.
- **`readback`** restates your goal, the problem, the constraints and what done looks like, and flags what it is unsure of; any preference call it finds goes to you before work starts.

**Understand**

- **Understand skills never change code.** `how` explains the code with the `codebase-design` vocabulary. `why` follows the history (commits, PRs, change folders, intents, ADRs, run trails) and keeps what is known apart from what is inferred. `look-up` reads primary sources outside the repo (official docs, source code, specs, first-party APIs, never a write-up of them) and writes a cited note to `docs/research/`, or into the `wayfinder` ticket that asked. `learn` runs in its own folder, never inside a product repo.
- **`explore-data` profiles before anyone analyses or builds:** shape, types, nulls, ranges, distributions, duplicates and quality issues, plus the questions worth asking next. Large local files go through DuckDB. Columns holding personal data are flagged and their values never printed; the profile shows only counts and patterns for them. What it learns about grain, keys and traps goes into `data-context`. When it serves a change, the profile is saved as `profile.md` in the change folder.
- **`diagnose-metric` rules out the data before the world.** In order:
  1. the data: pipeline runs, late or missing rows, and changes to logging or to the definition in `data-context`;
  2. the decomposition: mix versus rate first, then segments, then calendar effects (month length, holidays, seasonality);
  3. hypotheses, ranked and each tested against data;
  4. `review-result` on the conclusion.

  It ends with the drivers, each with its share of the move, written as a readout. The readout goes where the question came from: the incident note for an alert, a note on the intent whose metric moved, or the conversation when you simply asked. A data or code fault goes to `/start` as a Bug fix, and a trap it uncovered goes into `data-context`. It differs from `diagnose-bug`, which finds why code misbehaves, and from `why`, which traces how code came to be.

**Decide**

- **`brainstorm` widens before anything narrows.** You give it a goal, a problem or an area (`/brainstorm how to get more households to upload a second month`), then:
  1. frames it: the goal, what is off the table, and how ideas will be judged;
  2. grounds it in what exists, so ideas build on it instead of repeating it: the product brief, the backlog with its dropped intents and their reasons, `data-context`, past idea files and `docs/solutions/`; for a new project with no repo yet, `look-up` checks what already exists outside;
  3. generates many ideas from several angles before judging any (the user's problem, the data, cost, removing something, automating it, the bold version, the contrarian one, and doing nothing), with `second-opinion` adding ideas from another model family, because different models miss different things; you add yours;
  4. critiques every idea: each is kept or cut with a reason, such as already tried, breaks a guardrail, or serves no outcome;
  5. ranks the survivors against your criteria, each with its riskiest assumption, and hands each pick on: to `size-impact` (is it worth it?), a Spike (will it work?) or `/start` (a proposed intent).

  It never writes plans or code. In a product repo the whole list is saved in `docs/sdlc/ideas/`, so the next brainstorm starts from it. Ideas for the code's own structure and hygiene come from the `-health` skills, and ideas for how the agent works come from `retro`.
- **`size-impact` gives a range, never a point.** In order:
  1. frame the decision, the metric, the horizon and the bar, the smallest impact that justifies the cost (the bar is yours);
  2. break the impact into drivers that can each be estimated;
  3. give each driver a range, sourced from data through `data-context` first, then a comparable past launch, then judgment labelled as such;
  4. combine the ranges by simulation into P10, P50 and P90 and the chance of clearing the bar, never by multiplying lows and highs;
  5. name the driver that moves the answer most, and whether it can be measured cheaply before building: a query, a fake door, a `to-questionnaire` survey or a thin slice;
  6. give a verdict: go, no-go, or measure first. `review-result` checks the arithmetic.

  The sizing is saved in `docs/sdlc/sizing/`, and an intent that follows links to it. After release, the measure step writes each measured driver's actual beside its range, so sizing improves: about 8 in 10 actuals should land inside P10–P90, and `size-impact` reports the hit rate and widens its ranges when they run narrow.
- **`preregister` before the data decides:** the hypothesis and the decision it drives; the primary metric; the unit, design and randomisation; the sample size from the smallest effect worth acting on, with its power; the duration and stop rule; the analysis plan; and, for paid model evaluations, the cost before anything runs. **Without randomisation** (an observational question such as "did the redesign raise retention?"), the plan also names the causal graph, how the effect will be identified (difference-in-differences, synthetic control, regression discontinuity or matching), and the checks that could prove it wrong, such as pre-trends and placebo outcomes. It is saved as `preregistration.md` in the change folder, and `review-result` later checks the result against it.

**Share**

- **`polish` is for what you send as yourself:** a Slack message, an email, a PR comment or a post. It works out the reader, the channel and what you want from them (or you name them: `/polish for Priya on Slack: …`), then:
  1. keeps every fact, number, name, ask and commitment you wrote, and adds none: no claim, promise, apology or warmth you didn't write. A fact it thinks would help is suggested below the rewrite, never slipped in;
  2. puts the point or the ask first, and turns a vague ask ("let me know your thoughts") into one the reader can answer;
  3. cuts filler and hedges, one idea per sentence, at the length the channel expects;
  4. runs `unslop` for AI tells, without polishing your voice away: professional, not stiff. If your skills repo holds a style file, it follows that.

  It returns the rewrite ready to paste, and a second version only when the tone is a real choice (firmer or softer). It never sends anything.
- **An analysis readout leads with the decision,** then the number with its uncertainty, then what would change the conclusion. `diagnose-metric`, `size-impact` and Spike findings write their results in this shape themselves; type `/technical-writing` to apply it to an analysis you wrote.

**Check and prove**

- **`second-opinion` reports; it never fixes.** It sends the same input to each other model family whose CLI `docs/sdlc/config` lists, and shows where they agree and disagree without treating agreement as proof.
- **`review-result` before you trust a result,** whether a number, a chart or a whole analysis:
  1. state the claim so it can fail: condition, metric and threshold;
  2. compare with a baseline under the same conditions;
  3. record the run count and the spread;
  4. name what limits the number;
  5. rule out what else it could be measuring: errors, caching, skipped work, leakage, train/test contamination, selection and survivorship bias, multiple comparisons, join explosions, incomplete periods, an unfair or shifting denominator;
  6. confirm it measures what the intent's success metric or the preregistration says, computed the way `data-context` defines it;
  7. re-run it from a clean start (a notebook top to bottom) and get the same answer.

  It ends with a verdict (ready, share with caveats, or needs revision), recorded with the result in the findings, the PR body or the intent's note, together with the data snapshot, commit and seed that reproduce it.
- **`review-model` before a model is adopted,** in the change that ships or replaces it. It checks that the evaluation split matches how the model will be used (by time, and by household or user, so none appears on both sides); that nothing leaks; baselines, including the system it replaces; results per slice; calibration; a threshold set by what each kind of error costs; that features are computed the same way in training and serving; and a monitoring plan with alerts. Its numbers go through `review-result`; its verdict (adopt, adopt with limits, or not yet) goes in the PR body and `model-review.md`.
- **`review-dependency` before a package lands.** It checks that the package exists and is the one intended rather than a look-alike name, who maintains it, how widely it is used, its advisories and licence, and whether the standard library or an existing dependency already does the job. Its verdict goes in the PR body. `release-readiness` runs it across the whole lockfile. Unused or missing dependencies are `code-health`'s job (4.4).
- **`review-feedback` never agrees by reflex.** It checks each comment against the code before acting, and says so when a comment is wrong. Replies to people are messages, so they wait for your OK (section 5).
- **`fix-ci` fixes causes, not checks.** It never disables, skips or deletes a check to get green. After three failed attempts it stops and reports.

**Data helpers**

- **`make-chart` makes; `review-result` judges.** The form follows the question (change over time, comparison, distribution, relationship); uncertainty is shown; axes don't exaggerate (bars start at zero, no dual axes); labels sit on the data instead of in a legend where they can; colours stay readable for colour-blind readers and in both light and dark themes. The title states the chart's claim.
- **`write-notebook` writes marimo notebooks:** plain `.py` files with no hidden state that run top to bottom as a script, diff cleanly in a PR and store no outputs, so `review-result` can re-run them and no personal data is committed. It converts a Jupyter notebook the first time one is touched.

**Improve**

- **`retro` is not `codify`.** `codify` turns what a change taught into structure; `retro` looks at how the session went: navigation, missing checks, instructions that change nothing, costly tool calls, information the agent couldn't reach.
- **`to-skill` makes a skill only when a check can't do the job.** It names and triggers it by 10.3, writes the body with `writing-for-agents`, adds eval cases in `evals/skills/<name>/`, runs `review-skill`, and for a fork changes only `local.md`.
- **`review-skill` before a skill is trusted.** It scans for prompt injection, risky scripts and secrets, checks that the description doesn't overlap a skill you already have, and that the name follows 10.3 and no harness reserves it. An upstream update that fails stays unsynced; a new skill that overlaps one you have is rejected or merged into it.

**Built-ins**

- **Built-ins in Claude Code:** `/btw` for a side question that shouldn't enter the conversation, `/recap` for a one-line summary, `/deep-research` for a broad survey across many web sources (`look-up` stays the tool for one fact a decision needs, from its primary source), `/autofix-pr` to watch a PR from the cloud, `/insights` across sessions, `/skill-doctor` for each skill's context cost and use. The skills above stay portable to other harnesses.

### 4.6 Adopting the workflow in an existing project

**When:** the first `/start` in a repo that already has code but no `docs/sdlc/config`. **Ends:** when the agent-readiness check has run; the request that started it then routes as usual. Adoption is not a route: `setup` runs it once, and from then on the router routes work.

| Step | Skills | Exit criteria | Gate |
|---|---|---|---|
| 1 Setup, both passes | setup | Tracker linked, with existing issues left where they are; models and reviewer ladder in `docs/sdlc/config`; guard active; existing instruction files merged into `AGENTS.md`, with `CLAUDE.md` holding `@AGENTS.md`; the health command wraps the tools the repo already runs; `REVIEW.md` starts from the baseline and records the conventions the code already follows; existing CI kept | — |
| 2 Verify | setup → verify-app | `verify-app` written from the existing test and run commands, and passing from a clean clone, or its gaps listed | — |
| 3 Product brief | setup (draft) → grilling (product level) → to-product | `product.md` drafted from the README, docs, code and open issues, describing the product as it is; `GLOSSARY.md` created with the first settled terms | Brief accepted |
| 4 Architecture | setup (draft) → to-design (system) | `architecture.md` describes the components as they are; existing decisions that are hard to reverse and surprising recorded as ADRs; existing decision records linked, not moved | Architecture accepted |
| 5 Baseline health | architecture-health → code-health, full sweep | The health ledger records every area at the current commit; findings batched; nothing changed | — (findings wait for your pick) |
| 6 Agent-readiness check | a fresh session, given only the repo | It states the commands, conventions and architecture and runs `verify-app`; missing controls (CI, deploy, `verify-app`, guard) listed in the setup report | — |

**Rules:**
- **Describe what is, not what should be.** The brief and the architecture describe the project as it is today. What should change becomes intents, and Refactor or Feature work through `/start`.
- **Merge, never overwrite.** `setup` keeps every existing file. The content of an existing `CLAUDE.md` moves into `AGENTS.md`, its stale facts (commands that fail, files that are gone) are fixed or flagged, and the diff goes in the setup report. Existing CI, hooks and decision records stay.
- **Link the tracker; don't import it.** Open issues stay in the tracker. An issue becomes an intent, or a Bug fix, when `/start` picks it up.
- **No retrofits by default.** Existing code is not rewritten to meet `REVIEW.md`, and missing tests are not added all at once. The baseline sweep proposes small batches, and you pick them. New and changed code meets the standards through `tidy` and `review-change`.
- **Autonomy follows readiness, as always.** Parallel worktrees and AFK runs wait until CI, deploy, `verify-app` and the guard exist; the setup report says which are missing.
- **The glossary grows from conversation.** Terms come from grilling the drafted brief, not from scraping identifiers.

---

## 5. Gates and autonomy

**A human gate exists only for:**
1. **Preference calls** no experiment can settle: product brief accepted, MVP cut, intent accepted, spec approved, architecture accepted (new application), design and plan accepted (Feature L), the bar an experiment must clear and the decision a Spike ends with (Spike, `preregister`), and a sizing's bar and verdict (`size-impact`).
2. **Irreversible or shared-state actions:** merge to main, prod deploy, migrations, data deletion, messages to people, and loosening or removing any of the agent's own controls (the destructive-command guard, hooks, permissions, CI checks). Adding a control needs no gate, which is why `setup` runs without you typing it.

Everything else proceeds and reports evidence. On Feature M the plan is a report, not a gate. Confirmations inside a step are not separate gates: you confirm a glossary term or a metric definition as it is written (6.5, 6.6), and an AFK run leaves them for the hand-back.

**Deterministic controls (hooks and CI):**
- Protected paths cannot be edited: the guard blocks edits to every path listed in `docs/sdlc/locks`.
- Format and lint run after edits.
- Tests named as the regression test cannot be edited while a fix is in progress: `diagnose-bug` adds the test to `docs/sdlc/locks` and removes it once the fix is verified.
- Production deploy requires authorisation.
- Destructive commands are blocked: force-push, `reset --hard`, deleting branches, `rm -rf` outside the worktree, dropping tables, and skipping git hooks with `--no-verify`. `setup` installs the guard.
- The agent's own configuration (`CLAUDE.md`/`AGENTS.md`, skills, hooks) is regression-tested by an eval suite whenever it changes.
- Health checks, behind the command named in `docs/sdlc/config` (`make health` by default), installed by `setup` and extended by `codify` and `code-health`: format and lint, type check, complexity, dead code, import contracts from `architecture.md`, unused or missing dependencies, committed secrets, docs that point at files, functions or commands that no longer exist, `AGENTS.md` commands that fail, and names that use a synonym `GLOSSARY.md` says to avoid. `code-health` runs them every time; CI or git hooks run them too where they exist.

**Autonomy follows readiness:** parallel worktrees and AFK runs start only once CI, deploy, `verify-app` and the destructive-command guard exist. On a new application that is after the walking skeleton.

**AFK runs** are runs nobody watches: you said you are stepping away, or a hook or scheduled task started them. They load `afk`, which checks readiness, picks and logs defaults instead of asking, holds every human gate, and hands back a checked trail (4.2).

**Release autonomy by environment:** dev runs freely, staging is assisted, prod is authorised by you. Rollback is a single rehearsed command. After deploy, a post-deploy check confirms health. Milestone releases also pass `release-readiness`.

---

## 6. Artifacts

### 6.1 What each artifact is for

| Artifact | Answers | Owner | Lives until |
|---|---|---|---|
| Product brief | Vision; users; problems; product outcomes and their metrics; guardrails (quality, reliability, cost); constraints; non-goals; riskiest assumptions; milestones | You (the agent drafts from grilling) | Permanent; amended in place |
| Architecture | Components and boundaries; core data model; integrations; environments and deployment; testing and verification approach; observability | Agent drafts, you approve | Permanent; updated when a change alters structure |
| Intent | Why; outcome; success metric; constraints; non-goals; open questions | You (the agent drafts from grilling) | Success metric checked after release |
| Spec | Exact behaviour; acceptance criteria (Given/When/Then); NFRs; risks; which part of the intent this change delivers | Agent drafts, you approve | Change archived; its deltas merge into living specs |
| Design | Structure, interfaces and data model for one Feature L change; a threat model when the change crosses a trust boundary (money, credentials, personal data) | Agent drafts, you approve | Change archived; its structural changes merge into `architecture.md` when one exists |
| Plan | Vertical slices, order, blocking edges, TDD seams, risks, options rejected | Agent | Change archived |
| Bugfix | Current, expected and must-not-change behaviour | Agent | Change archived |
| Findings | What a spike learned and what was decided, with each result's `review-result` verdict | Agent | Permanent, or promoted to an ADR |
| Data profile | What a dataset holds: shape, types, nulls, ranges, distributions, quality issues, questions worth asking | Agent (`explore-data`) | Change archived |
| Preregistration | Hypothesis, decision, primary metric, design, sample size and power, stop rule and analysis plan (with the causal graph and identification strategy when there is no randomisation), written before the data is seen | Agent, from the bar you agreed | Permanent, beside the findings |
| Ideas | One brainstorm: the frame, every idea with its keep-or-cut reason, the ranked shortlist with riskiest assumptions, and where each pick went | Agent (`brainstorm`), from the frame and criteria you set | Permanent; read by the next brainstorm |
| Sizing | One decision's impact as a range: drivers and their sources, P10/P50/P90, the bar and the chance of clearing it, the driver to measure first, the verdict; later, each measured actual | Agent (`size-impact`), from the bar you set | Permanent; linked from the intent that follows |
| Model review | Split, leakage, baselines, slices, calibration, threshold, training-serving parity, monitoring, verdict | Agent (`review-model`) | Change archived; the verdict stays in the PR |
| Research note | A question, its answer and the primary source behind each claim | Agent | Permanent; a superseded note is marked |
| Incident note | When, impact, cause, data affected, and what was routed where | Agent | Permanent |
| Living specs | How the system behaves now | Updated on archive | Permanent |
| ADRs | A decision and why; provisional ones are marked | Agent drafts, you approve | Permanent |
| Glossary | Each project-specific term: what it is in one or two sentences, and the synonyms to avoid | You decide what words mean; `glossary` writes them (6.5) | Permanent; created with the first settled term |
| Data context | Where each dataset lives, its grain and keys, each metric's definition as SQL linked to its glossary term, and the known traps | You decide what a metric means; `data-context` keeps the facts current on its own (6.6) | Permanent; created with the first query against a warehouse and kept current by every data task |
| Runbook | How to deploy, roll back, restore data and respond to alerts | Agent | Permanent; checked by `release-readiness` |
| Solutions | Lessons recorded by `codify` | Agent | Permanent |
| Evals | Regression cases from incidents, agent-config changes, each skill and the agent-readiness check | Agent | Permanent |
| Wayfinder map | Destination, decisions so far, fog and out-of-scope, with one HITL or AFK ticket file per open decision | Agent; you on HITL tickets | Until the destination is reached |
| Handoff | What the next session needs that is not written down elsewhere, plus suggested skills | Agent | Until the change merges |
| Run trail | For one AFK run: one row per default picked, pivot, check and gate held (what, why, evidence, result), topped by the hand-back | Agent | Committed with the run's changes |
| Health ledger | For each area and each `-health` skill: the commit of its last review, what was found and what is still open; plus merges since the last run and what is next in line | Agent | Permanent |

`product.md` and `architecture.md` are required on a new application, and `setup` drafts both from the code and docs when an existing project adopts the workflow (4.6). A handoff goes to the device's temp folder; when you switch devices it goes into the change folder on the branch instead.

### 6.2 Product, intent and spec rules

```
product outcome  ←  intent  ←  change (spec, design, plan)  ←  PR
```

- **Boundaries:** the product brief and intents never name a solution; the architecture refers to product constraints instead of restating them; a spec never redefines the outcome. If grilling at a lower level shows a higher level is wrong, amend the higher level explicitly.
- **Traceability:** when a product brief exists, every intent names the product outcome or guardrail it serves. An intent that serves none is either out of scope or a sign that the brief needs amending; you decide.
- **Product amendments:** when `product.md` changes, the agent lists the intents that may be affected, and you re-accept, amend or drop them.
- **Intent and spec are separate files.** An intent outlives the changes that deliver it and never merges into living specs; a spec belongs to one change.
- **Pinning:** a spec records the intent revision it was written against. If the intent changes after the spec is approved, the spec is flagged stale and re-grilled.
- **Loaded together:** `to-spec` and the spec axis of `review-change` always read the intent with the spec. The spec opens with the intent ID and a one-line reference to the outcome, not a copy.
- **Feature S** creates no intent or spec files. The intent is one line in the PR body, linked to an existing intent when one applies.

### 6.3 Intent backlog

- One file per intent in `docs/sdlc/intents/`, with ID, status, source (you, agent, external), product outcome served, milestone, dependencies, outcome, success metric, notes and linked changes.
- **Lifecycle:** proposed → accepted → active → measuring → done. Exits: dropped, superseded.
- **Communication** (messages, meetings, review findings) attaches to an existing intent as a note. It becomes a new intent only when it introduces a new outcome.
- `INTENTS.md` is a generated index by milestone and status. When a tracker is linked, intents mirror to tickets.

### 6.4 Where artifacts live

Local files in the repo by default. `setup` can link a repo to a tracker (GitHub Issues, Jira, Linear); linked items carry IDs both ways (ticket ID in the artifact, commit SHA in the ticket).

```
AGENTS.md, CLAUDE.md               standing context, under a page; CLAUDE.md holds @AGENTS.md
GLOSSARY.md                        the project's words (6.5); GLOSSARY-MAP.md lists one per context in a multi-context repo
REVIEW.md                          code standards, thresholds and precedence (4.4); review axes and severity definitions
.claude/skills/verify-app/         project-local verification skill
.claude/agents/                    verifier and reviewer definitions
.claude/settings.json              hooks, including the destructive-command guard
.claude/hooks/guard.py             the guard: blocks destructive commands and edits to locked paths
docs/runbook.md
docs/sdlc/config                   tracker link, reachable models, reviewer ladder, health command
docs/sdlc/locks                    protected paths and the regression test of a fix in progress
docs/sdlc/product.md               product brief
docs/sdlc/architecture.md
docs/sdlc/intents/I-NNNN-<slug>.md
docs/sdlc/INTENTS.md               generated index
docs/sdlc/changes/C-NNNN-<slug>/   spec.md or bugfix.md, design.md, plan.md, findings.md, profile.md, preregistration.md, model-review.md, handoff.md
docs/sdlc/changes/archive/
docs/sdlc/incidents/YYYY-MM-DD-<slug>.md
docs/sdlc/specs/                   living specs
docs/sdlc/health-ledger.md         coverage record for the -health skills
docs/sdlc/sizing/<slug>.md         impact ranges, and their actuals once measured
docs/sdlc/ideas/<slug>.md          brainstorms: every idea, kept or cut with a reason
docs/sdlc/adr/
docs/research/<slug>.md            research notes with cited sources
docs/solutions/
evals/                             incident, agent-config and agent-readiness cases; evals/skills/<name>/ per skill
.scratch/<effort>/                 wayfinder map.md and issues/NN-<slug>.md (local tracker)
.audit/<slug>.tsv                  run trail for an AFK run
```

`data-context` lives outside the product repo, as a skill in your skills repo (10.2), because one warehouse serves many repos.

### 6.5 Glossary

`GLOSSARY.md` holds the project's own words: each term in one or two sentences, and the synonyms to avoid. Specs, code, tests, PRs and docs all use these words, so a reader never has to guess which "account" or "month" is meant.

| Stage | When | Who |
|---|---|---|
| Created | With the first term settled in conversation: on a new application, while grilling the product brief; on an existing project, while grilling the brief drafted at adoption (4.6). Never as an empty file | `glossary`, alongside grilling |
| Written | The moment a term is settled, in any grilling, `wayfinder` ticket or `architecture-health` session, or when `to-design` names a new concept. Never batched for later | `glossary` drafts the entry; you confirm it, because the meaning is yours |
| Read | Before a skill writes words that will last: the writers, `implement` and `tdd` (names in code and tests), `tidy`, `ship` (the PR), `technical-writing`; and whenever `huh`, `how`, `why`, `explore-data` or `diagnose-metric` explain something | Every skill, as a habit |
| Checked | On every change, `review-change` checks new names against it; on every `code-health` run, the health checks catch avoided synonyms and judgement catches one word used two ways | `review-change`, `code-health` |
| Changed | When a term is renamed or redefined: the glossary changes first, the old word moves to _Avoid_, and the code follows through a Feature S batch or a Refactor | `glossary`, then the playbook `/start` picks |

**Rules:**
- **Project words only.** A term belongs if it is specific to this product. General programming words (timeout, cache, retry), design vocabulary (module, seam, adapter) and implementation details stay out.
- **Opinionated and short.** One word per concept; the others go under _Avoid_. One or two sentences saying what the thing is, not what it does.
- **One meaning per word.** When two areas need the same word for different things, the repo splits into contexts: one `GLOSSARY.md` per context, and a `GLOSSARY-MAP.md` at the root that lists them and how they relate.
- **AFK runs read it, never change it.** A term that needs settling is logged in the run trail as proposed and listed in the hand-back for you.
- **The glossary says what a word means; an ADR says why a decision was made.** `glossary` offers an ADR only when a decision is hard to reverse, surprising without context and a real trade-off.

### 6.6 Data context

`data-context` holds how your data is laid out and how each metric is computed: the tables or files that matter, each one's grain and keys, each metric's definition as SQL, and the traps (late rows, test accounts, timezones, duplicates). Its reference files hold the map, one per warehouse or domain, so the agent loads only the part a query needs.

It is never finished. The map starts small and keeps itself current as the work touches data: facts go in on their own, and only what a metric means waits for you.

| Stage | When | Who |
|---|---|---|
| Created | The first time the agent queries a warehouse or dataset that has no map: it asks for the 3–5 tables you use most, reads their schemas and samples, and maps them. Never as an empty map | `data-context` |
| Grows | Automatically, whenever new facts about the data appear: a table a query touches for the first time is mapped; `ship` adds the tables, columns, events and metric queries a merged change introduces; `explore-data`, `diagnose-metric`, `review-result`, `review-model` and `size-impact` add what they learn (grain, keys, freshness, traps); a fact you mention in passing is recorded; descriptions are imported from dbt docs or a data catalog when one exists. Never batched for later | `data-context`, with no question asked |
| Corrected | Automatically, each time a query touches a table: its live schema is compared with the map, and a renamed, dropped or retyped column is updated. Any fact that new evidence contradicts is replaced the same way; the old entry is kept, marked superseded with its date | `data-context`, with no question asked |
| Proposed | When meaning is at stake: a new metric, a definition that new data makes ambiguous, or two definitions that conflict. The agent drafts the definition and marks it proposed; `/start` lists it with what waits for you, and any number computed with it says it used a proposed definition | `data-context` drafts; you confirm or correct |
| Read | Before any query, and by `explore-data`, `diagnose-metric`, `size-impact`, `preregister`, `review-result`, `make-chart` and `review-model` | Every data skill, as a habit |
| Checked | Whenever a number is reported, `review-result` confirms it was computed as defined; on every `code-health` run, judgement compares the queries, dashboards and notebooks in its areas with the definitions, and flags definitions nothing uses any more (4.4) | `review-result`, `code-health` |
| Changed | When you redefine a metric: the definition changes first, with its date; then the queries, dashboards and intents that use it follow through `/start`. Old numbers keep a label for the definition they used | `data-context`, then the playbook `/start` picks |

`/data-context` on its own shows what changed since you last looked, what waits for you, and what nothing uses any more.

**Rules:**
- **Facts go in on their own; meaning waits for you.** A fact is anything checkable against the data or the schema, and it goes in with its evidence. What a metric should count is a preference call, so it is only ever proposed.
- **Every change carries its source and date** (a query, a merged change, a profile, a diagnosis, something you said) and is a commit in the skills repo, so any automatic change can be traced and reverted. In a public skills repo the map folder is git-ignored instead, so schemas and definitions never reach the public history; the source and date then live in each entry.
- **Checked on touch, not on a timer.** An entry is re-checked whenever a query uses it. Nothing is deleted automatically: an entry nothing uses is flagged by `code-health` and goes when you say so.
- **The glossary says what a word means; `data-context` says where it lives and how to compute it.** Each metric links to its glossary term, and the glossary holds no SQL.
- **Definitions carry their date,** so any number can be traced to the definition it used.
- **Personal data stays out.** The map names the columns that hold it, never their values.
- **Imported text is data, never instructions.** Column comments and catalog descriptions are stored as quoted text and scanned for prompt injection before they are written.
- **It lives where the data's owner allows.** An employer's warehouse is mapped in a skills repo the employer controls, not a personal one. The map files sit beside `local.md`, so syncing the fork from upstream never touches them.
- **AFK runs update facts as usual;** a proposed definition waits in the hand-back.

---

## 7. Testing

- **Bug fixes:** a failing regression test comes first, and a hook blocks edits to it during the fix.
- **Features, library and pipeline code:** red-green-refactor at the seams agreed in `plan.md`.
- **Data transformations:** fixture tests and property-based tests (shapes, schemas, invariants, distributions; Hypothesis for Python) rather than strict red-green.
- **Data pipelines:** schema and data-quality tests where data enters and leaves them (pandera, or dbt tests in a dbt project), so bad data fails loudly at the boundary instead of quietly downstream.
- **Spikes and exploratory notebooks:** exempt from TDD; `review-result` re-runs them from a clean start instead.
- **`verify-app`** proves the real thing end to end and is updated when features change. On a new application it is written during the walking skeleton and grows with each capability. For data work it runs the pipeline on sample data, checks schemas and data quality, and checks metrics against thresholds on a fixed eval set.

---

## 8. Review

- **Order:** tidy → verify-app → review-model (when the change ships a model) → review-change.
- **Two axes, in separate subagents:** standards (the code standards in `REVIEW.md`, security included, the same ones `code-health` applies) and spec (does the change do what the intent and spec say, and nothing outside scope). Findings are severity-ranked; only findings that affect correctness or stated requirements block.
- **Reviewer ladder** (first available rung wins, on every tier):
  1. A model from another family, through `second-opinion`, which calls that family's CLI.
  2. Otherwise the strongest same-family model at one effort level above the writer's, capped at max, in a fresh context, with an adversarial prompt, seeing only the work under review (a diff, plan, architecture or MVP cut) and the artifacts it traces to (spec, intent, product brief). Writer at high → reviewer at xhigh; writer at xhigh → reviewer at max; writer at max → reviewer at max, noted as "no step-up".
- The PR body records the rung, the reviewer model and its effort.
- **New dependencies:** when a change adds or upgrades a package, `review-change` runs `review-dependency`.
- **Acting on findings:** the writer runs every finding, from `review-change` or from people on the PR, through `review-feedback`: check it against the code, then fix it or answer it with evidence.
- `review-plan` uses the same ladder and adds a scope challenge (expand, hold or reduce). It runs on Feature L plans, and on a new application's MVP cut and architecture.
- `setup` detects the models reachable on each device and harness, maps each harness's effort scale, and writes the ladder to `docs/sdlc/config`.
- **Tuning:** if review slows small work, Feature S drops to rung 2.

---

## 9. Learning and upkeep

- **`codify` ends every change that taught something.** In order of preference, the lesson becomes a lint (a Semgrep rule when the linter can't express it), hook or test; a glossary entry when the lesson is about what a word means; a skill or `AGENTS.md` edit; or a note in `docs/solutions/`.
- **Repeated mistakes:** a mistake made twice gets a structural fix or an `AGENTS.md` line.
- **Session retros:** after a long or messy session, `/retro` proposes fixes to the agent's environment. Accepted fixes become, in order of preference, a check or command, a skill edit through `to-skill`, or an `AGENTS.md` line.
- **Archive:** a finished change moves to `changes/archive/`. Its spec deltas merge into living specs, its structural changes merge into `architecture.md` when one exists, and its intent moves to measuring.
- **Milestone review:** after each milestone release, the product metrics are measured against `product.md` and checked with `review-result` (with `diagnose-metric` for any that moved unexpectedly), both `-health` skills run a full sweep, the brief and the backlog are amended with what they all found, `size-impact` sizes the candidates for the next milestone, and the next milestone runs as the New application expansion variant.
- **Incidents** become eval cases.
- **Sizing calibration:** each measure step writes the actuals into the sizing it came from; `size-impact` reports how often actuals land inside P10–P90 and widens its ranges when they run narrow.
- **Skills upkeep:** every skill you adopt or sync passes `review-skill` first (10.2).
- **Codebase health:** the `-health` skills keep existing code in shape whenever they run (4.2 to 4.4). Neither changes code; each finding you pick goes to `/start`, and a mechanical problem that recurs becomes a health check.

---

## 10. Skills

### 10.1 Catalog

**Skills you type** (2.1), in the same order:

| Skill | Trigger | Purpose | Source |
|---|---|---|---|
| `start` | You; alert hooks send to it | Route work by outcomes, work type and size; match it against the product brief and intent backlog; resume work in progress; load the playbook into the task list; on its own, report what is in progress, what waits for you and what is next; point a need to the skill that meets it | Write (pattern: pstack `poteto-mode`) |
| `huh` | You | Explain what is waiting on you in plain words and glossary terms: a catch-up when a lot has happened since you last wrote, else the question the last reply asks (`/huh Q2` picks one of several), else the reply itself; or a passage, file or link you name | Fork: compound `wtf`; `local.md` adds `wait-what`'s plain-English and glossary rule, the question mode and the catch-up mode (pattern: pstack `ketchup`). Replaces `bro`, `wait-what` and `ketchup` |
| `readback` | You | Restate your goal, the problem, the constraints and what done looks like, flagging what is unsure | Fork: pstack `in-your-own-words` |
| `handoff` | You; the agent suggests it when the context runs long | Write what the next session needs that is not written down elsewhere, with suggested skills | Fork: mattpocock `handoff` |
| `afk` | You; `/start`, hooks and scheduled tasks load it for every run nobody watches | Run with nobody watching: readiness check, defaults instead of questions, every gate held, a trail audited against the transcript and reviewed by another family, a hand-back | Fork: pstack `show-me-your-work` (the trail); `local.md` adds readiness, gates, defaults and the hand-back, using mattpocock's AFK/HITL terms |
| `how` | You | How code works and where things belong, built up diagram by diagram; read-only | Fork: pstack `how` (`local.md` takes models from `docs/sdlc/config` instead of pstack's model rule) |
| `why` | You | Why code is the way it is, traced through commits, PRs, change folders, intents, ADRs and run trails; known kept apart from inferred | Fork: pstack `why` (same overlay) |
| `explore-data` | You; the agent when a new dataset arrives | Profile a table or file before anyone analyses or builds on it; DuckDB for large local files; personal-data columns flagged, never printed; `profile.md` in the change folder | Fork: Anthropic data plugin `explore-data` (pattern: DuckDB `read-file`, `query`) |
| `diagnose-metric` | You; the agent in an Incident for metric drift and when a measured success metric misses or moves unexpectedly | Find why a metric moved: rule out the data, decompose into mix and rate, segments and calendar, test each hypothesis, and rank the drivers by their share of the move; verdict through `review-result` | Write (patterns: Anthropic `analyze`, `variance-analysis`, `metrics-review`) |
| `look-up` | You; the agent for `wayfinder` research tickets or an outside fact a decision needs | A background agent answers a question from primary sources and writes a cited note | Fork: mattpocock `research` |
| `learn` | You, in a learning folder | Learn a topic over several sessions in a separate learning workspace | Fork: mattpocock `teach` |
| `brainstorm` | You | Widen before narrowing: frame the goal, ground it in the brief, backlog, data and past ideas, generate many ideas from several angles (with `second-opinion` for another family's), critique every one, and rank a shortlist with riskiest assumptions; hands picks to `size-impact`, a Spike or `/start`; never plans or code | Write (patterns: compound `ce-ideate`, Anthropic `product-brainstorming`, K-Dense `scientific-brainstorming`) |
| `wayfinder` | You; Feature L and New application suggest it | Chart work too foggy for one session as a map of decision tickets, then work one ticket per session | Fork: mattpocock `wayfinder` |
| `size-impact` | You; the agent at milestone planning and when intents compete for a cut; `/start` suggests it for an idea whose value is unclear | Size a decision's impact as a range before building: drivers with sources, P10/P50/P90, the chance of clearing your bar, the driver to measure first, a verdict; reports its own calibration | Write (pattern: K-Dense `what-if-oracle`) |
| `preregister` | You; the agent in Spike and before any experiment decides something | Write the experiment plan before the data is seen: hypothesis, decision, metric, design, sample size and power, stop rule, analysis plan, and the cost of paid evaluations; for observational questions, the causal graph, identification strategy and falsification checks | Fork: K-Dense `experimental-design` (`statistical-power` as a reference; pattern: gstack `eval-plan`) |
| `to-questionnaire` | You | Turn a question you can't answer into a questionnaire for whoever can | Fork: mattpocock `to-questionnaire` |
| `technical-writing` | You | Layered writing standard for docs, RFCs, READMEs, PR descriptions and analysis readouts (decision first, then the number with its uncertainty, then what would change it); runs `unslop` | Fork: pstack `technical-writing` |
| `polish` | You | Rewrite a message, email, comment or post you will send as yourself: clear, professional and human, for its reader and channel, with every fact and ask kept and nothing added; runs `unslop` | Fork: compound `ce-noslop` (its edit mode and your-own-writing register; `local.md` adds reader, channel and ask) |
| `second-opinion` | You; `review-change` and `review-plan` for rung 1; `brainstorm` for ideas from other families | Send a diff, plan or idea to each other model family's CLI and report where they agree and disagree; never fixes | Fork: Trail of Bits `second-opinion` |
| `architecture-health` | You; the merge hook and the milestone review | Survey the structure of the areas the coverage plan picks for restructuring candidates, then grill your pick; full sweep at milestones; never changes code | Fork: mattpocock `improve-codebase-architecture` (the overlay replaces its recent-changes-first scoping) |
| `code-health` | You; the merge hook and the milestone review | Run the health checks itself (no CI needed), then judge the areas the coverage plan picks against `REVIEW.md` and check docs, specs, comments, names and architecture for drift; batch the findings; escalate structural causes; propose health checks; never changes code | Write (patterns: gstack `test-audit`, `document-release`, `deslop-shared-libs`; pstack `no-comments`; Trail of Bits `spec-to-code-compliance`) |
| `retro` | You | After a session, propose fixes to the agent's environment, ranked; never edits by itself | Fork: mattpocock `retro` |
| `to-skill` | You | Draft or change a skill: name and trigger by 10.3, body by `writing-for-agents`, eval cases in `evals/skills/`, then `review-skill`; forks change only `local.md` | Fork: Anthropic `skill-creator` |

**Skills that run for you** (2.2):

| Skill | Trigger | Purpose | Source |
|---|---|---|---|
| `to-product` | Playbook step, or you | Grilled vision → `product.md`; amend it and list the intents an amendment affects | Write (pattern: BMAD product brief, gstack office-hours) |
| `to-backlog` | Playbook step, or you | Product brief → proposed capability intents with dependencies and milestones; lists open technical decisions for `/wayfinder` | Write (pattern: AI-DLC units, BMAD epics, mattpocock to-tickets) |
| `to-intent` | Playbook step, or you | Grilled problem → intent file; attach notes; move status | Write |
| `to-spec` | Playbook step, or you | Accepted intent → `spec.md` | Fork: mattpocock `to-spec` |
| `to-design` | Playbook step, or you | Spec and ADRs → `design.md` for one change, with a threat model when the change crosses a trust boundary; system mode writes `architecture.md`; on archive, merges a change's structural changes into it | Write (patterns: AI-DLC domain and logical design, Spec Kit plan, Kiro design, OpenAI `security-threat-model`) |
| `to-tickets` | Playbook step, or you | Spec → vertical slices with blocking edges and TDD seams in `plan.md` | Fork: mattpocock `to-tickets` |
| `setup` | `/start`, when the repo isn't set up (in an existing project, through the adoption path in 4.6), at New application steps 1 and 5, or on a device or harness the config doesn't list yet; or you | Docs layout, tracker link, reachable models and reviewer ladder, the destructive-command guard, `AGENTS.md` and `CLAUDE.md` stubs (`AGENTS.md` asks for numbered questions whenever a reply asks more than one); once the stack is known, commands, hooks, the verify command, the baseline health checks, `REVIEW.md` standards (4.4) and CI where wanted, with uv, ruff and a type checker for Python. In an existing project it runs the adoption path: merges existing instruction files, drafts `product.md` and `architecture.md` from code and docs, and starts the health ledger with a full sweep | Write (patterns: mattpocock `setup`, pstack `setup`, Astral `uv`/`ruff`/`ty`, Trail of Bits `modern-python`) |
| `review-plan` | Playbook step, or you | Scope challenge and engineering review of a plan, an MVP cut or an architecture, via the reviewer ladder | Write (patterns: gstack `plan-ceo-review`, `plan-eng-review`) |
| `implement` | Playbook step, or you | Per slice: tdd → verify → commit; worktrees for independent slices | Fork: mattpocock `implement` |
| `ship` | Playbook step, or you | PR with intent, evidence, reviewer rung and merge-danger call → CI (a failing check goes to `fix-ci`) → deploy gate → post-deploy check; after merge, adds new tables, columns, events and metric queries to `data-context` | Fork: mattpocock `pr` (pattern: gstack `ship`) |
| `release-readiness` | Playbook step, or you | Before a milestone release: NFRs from specs and the brief verified, security review, `review-dependency` across the lockfile, alerts in place, backups and migrations rehearsed, rollback rehearsed, runbook current | Write (pattern: BMAD readiness check, gstack `cso`, `canary`) |
| `codify` | Playbook step, or you | Turn what a change taught into the most structural fix available: a lint or Semgrep rule, hook or test; a glossary entry when the lesson is about what a word means; then a skill or `AGENTS.md` edit; then a note | Write (patterns: compound `ce-compound`, Trail of Bits `semgrep-rule-creator`) |
| `grilling` | Agent | Rounds of numbered questions, each with a recommended answer and why it matters, until every branch is resolved; runs `glossary` alongside it; ends with a readback | Fork: mattpocock `grilling` |
| `glossary` | Agent, alongside every grilling; or you | Challenge fuzzy or conflicting terms, write each settled term to `GLOSSARY.md` at once (6.5), and offer an ADR when a decision earns one | Fork: mattpocock `domain-modeling` (`local.md` keeps ADRs in `docs/sdlc/adr/`) |
| `codebase-design` | Agent | Shared vocabulary for deep modules, seams and interfaces; used by `architecture-health`, `to-design` and `review-change` | Fork: mattpocock `codebase-design` |
| `prototype` | Agent | Answer a design question by experiment | Fork: mattpocock `prototype` |
| `tdd` | Agent | Red-green-refactor at agreed seams; fixture and property-based tests for data code; schema and data-quality tests at pipeline boundaries | Fork: mattpocock `tdd` (pattern: Trail of Bits `property-based-testing`) |
| `diagnose-bug` | Agent | Reproduce → minimise → hypothesise → instrument → fix → regression test → find other instances of the same cause | Fork: mattpocock `diagnosing-bugs` (pattern: Trail of Bits `variant-analysis`) |
| `tidy` | Agent | Per-change cleanup against `REVIEW.md`: delete before adding, remove needless code and comments, clearer names | Fork: compound `ce-simplify-code` |
| `fix-ci` | Agent when a check fails, `ship`, or you | Read the failing check, reproduce, fix the cause, push, re-check; at most three attempts; never skips a check | Fork: cursor-team-kit `fix-ci` (pattern: `loop-on-ci`) |
| `verify-app` | Agent | Prove this app or pipeline works end to end | Write per repo (pattern: pstack verification skills) |
| `review-change` | Agent | Two-axis review via the reviewer ladder; runs `second-opinion` for rung 1 and `review-dependency` when packages change | Fork: mattpocock `code-review` |
| `review-feedback` | Agent when findings or PR comments arrive, or you | Check each comment against the code, fix valid ones, answer wrong ones with evidence; replies to people wait for your OK | Write (patterns: compound `ce-resolve-pr-feedback`, superpowers `receiving-code-review`) |
| `blast-radius` | Agent | What else could break, and why it is safe | Fork: pstack `blast-radius` |
| `review-result` | Agent before a result is reported or acted on, in Spike and measure steps; or you | Check a number, chart or analysis before it decides anything (4.5), including that it was computed as `data-context` defines it and re-runs from a clean start; give a verdict (ready, share with caveats, or needs revision) with the snapshot, commit and seed | Fork: Anthropic data plugin `validate-data` (patterns: pstack `principle-explain-the-number`, `benchmark-checklist`; cursor-team-kit `verify-this`) |
| `review-dependency` | Agent when a change adds or upgrades a package, and in `release-readiness`; or you | Is the package real and the one intended, maintained, widely used, free of advisories, acceptably licensed, and needed at all | Fork: Trail of Bits `supply-chain-risk-auditor` |
| `review-skill` | Agent in `to-skill` and every skills sync; or you | Scan a skill for injection, risky scripts and secrets; check its description for overlap with your skills, and its name against 10.3 and harness-reserved names | Fork: Sentry `skill-scanner` |
| `review-model` | Agent in the change that ships or replaces a model; or you | Before a model is adopted: split, leakage, baselines, slices, calibration, a threshold from error costs, training-serving parity, monitoring; verdict in the PR body | Write (patterns: K-Dense `shap`, `scientific-critical-thinking`) |
| `writing-for-agents` | Agent when writing a skill, `CLAUDE.md` or `AGENTS.md` | How to write text that agents read and follow | Fork: mattpocock `writing-for-agents` |
| `unslop` | Agent, inside `technical-writing` and `polish` | Cut AI tells from prose and keep every fact; nothing else changes. You reach it through `/polish` or `/technical-writing` | Fork: pstack `unslop` |
| `data-context` | Agent before any query, after any data skill learns something, and in `ship`; or you, to see what changed and what waits | The map of your data: tables, grain, keys, each metric as SQL linked to its glossary term, and traps. Created on first use, then kept current on its own: facts go in with their source, schema changes are caught on touch, and new or ambiguous definitions are proposed for you to confirm (6.6) | Fork: Anthropic data plugin `data-context-extractor` (pattern: `sql-queries`) |
| `write-notebook` | Agent whenever a notebook is written or touched | marimo notebooks: plain `.py`, no hidden state, no stored outputs, runnable as a script; converts Jupyter notebooks | Fork: marimo `marimo-notebook` (pattern: `jupyter-to-marimo`) |
| `make-chart` | Agent whenever a chart is made; or you | Chart form from the question, uncertainty shown, honest axes, direct labels, accessible colours, the claim as the title | Fork: K-Dense `scientific-visualization` (pattern: Anthropic `data-visualization`) |

**Adoption order:**
- **Day one:** `setup`, `grilling`, `to-spec`, `implement` with `tdd`, `verify-app`, `review-change`, `huh` and `polish`, plus a short `AGENTS.md`, one check command, format and lint hooks, and the guard.
- **Weeks two to four:** `start`, `ship`, `codify`, `to-intent`, `to-tickets`, `diagnose-bug`, `look-up`, `review-result`, `second-opinion` and `review-dependency`; with data work, `data-context`, `explore-data`, `write-notebook`, `make-chart`, `diagnose-metric` and `preregister`; with planning, `brainstorm` and `size-impact`.
- **When the need appears:** the rest, and `review-model` with the first model you ship. Add a skill the second time you feel the problem it solves; a typed skill costs nothing until you use it.
- **A new application** also needs `to-product`, `to-backlog`, `to-design`, `review-plan`, `size-impact` and `release-readiness`.

### 10.2 Sourcing forked skills

- **Ownership:** upstream owns the method (the `SKILL.md` body). You own the folder name, `name`, `description`, the trigger setting, and additions in `local.md`, which `SKILL.md` loads and sync never merges.
- **Provenance per skill:** upstream repo and path, the upstream authors and licence, pinned commit, state, and a changelog of your edits with reasons. The upstream licence file stays in the fork's folder.
- **Rename map:** one file maps upstream names to yours. It applies to `SKILL.md` only; licences, credits and other supporting files stay verbatim. Sync applies it to both upstream versions before comparing, so renames never show up as changes or conflicts.
- **Sync** compares the pinned base, the new upstream and yours:
  - only upstream changed → take it, record a new pin;
  - only you changed → nothing to do;
  - both changed → three-way merge of the body; overlapping edits are explained by the agent and resolved by you; new pin;
  - too far apart → mark Owned: no more syncing, but sync still shows upstream diffs to borrow from.
- **States:** Pristine (matches pin) · Behind (upstream moved) · Ahead (you edited) · Diverged (both) · Owned (detached).
- **Keep edits additive** in `local.md` so most syncs are simple updates. Generic improvements go upstream as PRs.
- **`review-skill` gates every adoption and sync.** An upstream update that fails stays at the old pin; a new skill that overlaps one you have is rejected or merged into it.
- **A fork brings its dependencies.** Before adopting a fork, list every skill its body calls and add each one, renamed through the map: `wayfinder` needs `look-up`, `prototype`, `grilling` and `glossary`; `architecture-health` needs `codebase-design`, `grilling` and `glossary`; `technical-writing` and `polish` need `unslop`; `brainstorm` needs `second-opinion` and `look-up`; `retro` and `to-skill` need `writing-for-agents`, and `to-skill` also needs `review-skill`; `review-change` needs `second-opinion` and `review-dependency`; `diagnose-metric` and `size-impact` need `data-context` and `review-result`; `review-model` needs `review-result`. A skill that another skill or a playbook runs must be agent-startable (2.3).

```
agent-skills/
  skills/<your-name>/
    SKILL.md        your frontmatter + upstream body
    local.md        your additions
    PROVENANCE      upstream, authors, licence, pin, state, changelog
    LICENSE         the upstream licence
  rename-map
```

### 10.3 Naming and triggers

- **A name that pairs an action with its object leads with the verb:** `review-change`, `explore-data`, `diagnose-metric`, `diagnose-bug`, `size-impact`, `make-chart`, `write-notebook`, `fix-ci`, `verify-app`. Knowledge the agent reads keeps a noun (`glossary`, `data-context`, `codebase-design`, `writing-for-agents`), and so do reports on what already exists (`-health`).
- **`review-` judges something before it is accepted** (merged, reported or adopted): `review-plan`, `review-change`, `review-feedback`, `review-result`, `review-dependency`, `review-skill`, `review-model`.
- **`-health` examines what already exists, not just what changed, and only reports:** `architecture-health`, `code-health`.
- **`to-` writes an artifact:** `to-product`, `to-intent`, `to-spec` and the rest.
- **Other names say what you get, in plain words:** the moment you reach for it (`huh`, `afk`, `readback`) or the job it does (`how`, `why`, `look-up`, `learn`, `codify`, `polish`, `brainstorm`, `preregister`). A metaphor stays only when it is the common term (`blast-radius`) or a well-known upstream name (`wayfinder`).
- **A name never promises the opposite of what the skill does.** In Copilot CLI and other assistants `autopilot` means "keeps going without stopping for you", so the skill that holds every gate while you are away is `afk`, after the AFK/HITL split upstream already uses.
- **Never reuse a name a harness reserves.** Check its command list before naming a skill. Claude Code, for example, reserves `/review`, `/code-review`, `/simplify`, `/verify`, `/plan`, `/doctor`, `/checkup` and `/security-review`; Copilot CLI reserves `/research`, `/diagnose`, `/review`, `/plan` and `/delegate`.
- **Upstream names stay in the rename map**, so a renamed fork still syncs: `wtf` → `huh`, `teach` → `learn`, `skill-scanner` → `review-skill`, `ce-noslop` → `polish`, `validate-data` → `review-result`, `data-context-extractor` → `data-context`, `research` → `look-up`, `diagnosing-bugs` → `diagnose-bug`, and the rest.
- **One skill per job.** Before adding a skill, `review-skill` checks its description against the ones you have; two skills that answer the same moment merge into one.
- **Typed skills are free until used; agent-startable skills are not.** A typed skill's description stays out of context until you type it, so a narrow skill you reach for now and then earns its place. An agent-startable skill's description loads in every session and competes with the others for triggering, so it must be used often or be run by a playbook or another skill. Check both with `/skill-doctor` in Claude Code.

---

## 11. References

| Source | Used for |
|---|---|
| [The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook) — Anthropic | Committed artifact chain, skills vs hooks, evals on agent config, prod gate, incident → intent loop |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) — Anthropic | Explore → plan → implement, verification, fresh-context review, lean `CLAUDE.md` |
| [AI-DLC whitepaper](https://github.com/fabriqaai/specs.md/blob/main/resources/aidlc.pdf), [blog](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/), [aidlc-workflows](https://github.com/awslabs/aidlc-workflows) — AWS | Intent, decomposition into loosely coupled units, AI proposes / human approves, adaptive stages, brownfield model recovery |
| [specs.md](https://specs.md/methodology/sdlc-reimagined) | Adaptive checkpoints |
| [Building an AI-native engineering team](https://learn.chatgpt.com/guides/build-ai-native-engineering-team) — OpenAI | Delegate / review / own |
| [Spec Kit](https://github.com/github/spec-kit) | Clarification markers, constitution |
| [Kiro specs](https://kiro.dev/docs/specs/) | Bugfix spec, quick spec |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | Change folders, archive into living specs |
| [BMAD Method](https://docs.bmad-method.org/) | Product brief → requirements → architecture order, readiness check, adversarial review |
| [mattpocock/skills](https://github.com/mattpocock/skills), [AI Hero dictionary: AFK](https://www.aihero.dev/ai-coding-dictionary/afk) | Grilling, glossary, to-spec, to-tickets, tdd, two-axis review, handoff, wayfinder, architecture survey, deep-module vocabulary, AFK/HITL split, research (our `look-up`), teach (our `learn`), retro, to-questionnaire, writing for agents, wait-what |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) | Router and playbooks, reversible vs irreversible, verification skill, structural lessons, comment review, decision trail, how, why, catch-up (in our `huh`), in-your-own-words, unslop, technical writing, explaining a number |
| [Cursor team kit](https://github.com/cursor/plugins/tree/main/cursor-team-kit) | CI fix loop, verifying a claim with baseline and treatment |
| [gstack](https://github.com/garrytan/gstack) | Product questioning, plan reviews with scope challenge, ship → deploy → canary, test and documentation audits, eval preregistration, destructive-command guard |
| [Claude Code commands](https://code.claude.com/docs/en/commands), [skills](https://code.claude.com/docs/en/skills) | Names Claude Code reserves, built-ins to use instead, which skill descriptions load into context |
| [Compound engineering](https://github.com/EveryInc/compound-engineering-plugin) | Per-change cleanup pass (our `tidy`), compounding lessons (patterns in `codify`), plain-language explanations (our `huh`), plain rewriting of your own writing (the base of `polish`), grounded idea generation (patterns in `brainstorm`), resolving PR feedback (patterns in `review-feedback`) |
| [Anthropic knowledge-work plugins](https://github.com/anthropics/knowledge-work-plugins) | Product brainstorming as a thinking partner (patterns in `brainstorm`), data profiling (our `explore-data`), analysis validation (the base of `review-result`), warehouse context (the base of `data-context`), metric investigation and variance decomposition (patterns in `diagnose-metric`) |
| [Trail of Bits skills](https://github.com/trailofbits/skills) | Second opinions from other model families, supply-chain review (our `review-dependency`), property-based testing, variant analysis, Semgrep rules, spec-to-code compliance. Licensed CC BY-SA 4.0: forks keep the attribution and the licence |
| [Sentry skills](https://github.com/getsentry/skills) | Skill scanning (the base of `review-skill`), secrets leaking through serialisation |
| [K-Dense scientific skills](https://github.com/K-Dense-AI/claude-scientific-skills) | Experimental design and power analysis (our `preregister`), truthful figures (the base of `make-chart`), scenario framing (in `size-impact`), model explanation and evidence appraisal (in `review-model`), independent idea generation (in `brainstorm`) |
| [marimo skills](https://github.com/marimo-team/skills) | Reactive Python notebooks with no hidden state (our `write-notebook`) |
| [Causal Inference: The Mixtape](https://mixtape.scunning.com/) — Scott Cunningham | Causal graphs and identification strategies for observational questions in `preregister` |
| *How to Measure Anything* — Douglas Hubbard | Ranges instead of points, calibration and the value of information in `size-impact` |
| [DuckDB skills](https://github.com/duckdb/duckdb-skills), [Astral plugins](https://github.com/astral-sh/claude-code-plugins), [OpenAI skills](https://github.com/openai/skills), [wshobson/agents](https://github.com/wshobson/agents) | Large local files in `explore-data`; uv, ruff and ty in `setup`; threat models in `to-design`; blocking `--no-verify` in the guard |
| [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) — Robert C. Martin; [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) | Naming, functions and error-handling standards; the dependency rule |
| [Code smells](https://martinfowler.com/bliki/CodeSmell.html) — Martin Fowler, *Refactoring* | The smell catalogue behind the simplicity and module standards |
| [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/book.php) — John Ousterhout | Deep modules; why deep modules win over "keep functions small" |
| [PEP 8](https://peps.python.org/pep-0008/), [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | Baseline Python style |
| [Superpowers](https://github.com/obra/superpowers) | Small tasks, TDD discipline, verification before completion, receiving code review |
| [anthropics/skills](https://github.com/anthropics/skills) | Skill authoring with evals (our `to-skill`) |
| [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — Anthropic | Descriptions, conciseness, progressive disclosure and evaluation rules in `writing-for-agents` |
| [HumanLayer skills](https://github.com/humanlayer/skills) | The PR summary visuals in `ship`, from `show-me` by way of mattpocock `pr` |
| [Start with a walking skeleton](https://oreilly.com/library/view/97-things-every/9780596800611/ch60.html) — 97 Things Every Software Architect Should Know | Walking skeleton (Cockburn): minimal end-to-end implementation linking all main components |
| [Forget the walking skeleton, put it on crutches](https://gojko.net/2014/06/09/forget-the-walking-skeleton-put-it-on-crutches/) — Gojko Adzic | Skeleton on crutches when the riskiest assumption is about value |
| [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/), [Harper Reed](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/) | Spec first, small chunks, commit often |
| [Böckeler on SDD tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), [Thoughtworks Radar](https://www.thoughtworks.com/en-in/radar/techniques/spec-driven-development) | Limits of heavy spec-driven development |
