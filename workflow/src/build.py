import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_data import PRODUCT, PLAYBOOKS

here = os.path.dirname(os.path.abspath(__file__))
routed = [p for p in PLAYBOOKS if p.get("kind") != "skill"]
around = [p for p in PLAYBOOKS if p.get("kind") == "skill"]

# ---------- markdown doc ----------
md = []
md.append("# AI-native SDLC: playbook examples")
md.append("")
md.append("Worked examples of every playbook in the workflow doc ([ai-native-sdlc.md](ai-native-sdlc.md)) and of the skills outside a playbook's fixed steps: the skills around the playbooks, the everyday skills and the data skills, all on one running product. The same examples play as animated walkthroughs in [walkthroughs.html](walkthroughs.html). This file and the page are generated: edit `src/examples_data.py`, then run `python3 workflow/src/build.py`.")
md.append("")
md.append("---")
md.append("")
md.append("## The running example")
md.append("")
md.append(f"**{PRODUCT['name']}.** {PRODUCT['summary']}")
md.append("")
md.append(f"- **Users:** {PRODUCT['users']}")
md.append("- **Outcomes:** " + " · ".join(f"{k} {v}" for k, v in PRODUCT["outcomes"]))
md.append("- **Guardrails:**")
for k, v in PRODUCT["guardrails"]:
    md.append(f"  - {k} {v}")
md.append(f"- **Riskiest assumption:** {PRODUCT['riskiest']}")
md.append("- **Milestones:** " + " · ".join(f"{k} {v}" for k, v in PRODUCT["milestones"]))
md.append("")
md.append("---")
md.append("")
md.append("## How each request reaches its playbook")
md.append("")
md.append("| You bring | Router reasoning | Playbook |")
md.append("|---|---|---|")
for p in routed:
    reasoning = " · ".join(f"{k}: {v}" for k, v in p["router"] if k != "Playbook")
    md.append(f"| `{p['input']}` | {reasoning} | {p['name']} |")
md.append("")
md.append("The router also runs for each intent in a backlog, for each incident or review finding, and at each milestone.")
md.append("")
md.append("## The skills outside the playbooks")
md.append("")
md.append("Grouped by the moment you need them, as in the workflow doc's quick reference. Each starts its own way: you type it, the agent starts it, or a hook or another skill does. `/start` points you to the right one when your input is a need rather than work.")
md.append("")
md.append("| Moment | Skill | How it starts | When | Example |")
md.append("|---|---|---|---|---|")
for p in around:
    trig = dict(p["router"]).get("Trigger", "")
    md.append(f"| {p['group']} | `{p['name']}` | {trig} | {p['when']} | {p['example']} |")
md.append("")

for i, p in enumerate(PLAYBOOKS, 1):
    skill = p.get("kind") == "skill"
    md.append("---")
    md.append("")
    md.append(f"## {i}. {'`' + p['name'] + '`' if skill else p['name']}: {p['example']}")
    md.append("")
    md.append(f"**When:** {p['when']}")
    md.append("")
    md.append(f"**{'Typed' if skill else 'You bring'}:** `{p['input']}`")
    md.append("")
    if skill:
        md.append("**How it starts:** " + " · ".join(f"{k}: {v}" for k, v in p["router"]))
        md.append("")
        md.append(p["scene0"]["text"])
    else:
        md.append("**Router:** " + " · ".join(f"{k}: {v}" for k, v in p["router"][:-1]) + f" → **{p['router'][-1][1]}**")
    md.append("")
    md.append(f"**Your decisions:** {p['decisions']}")
    md.append("")
    md.append("| # | Skills | Step | What happens | You | Gate |")
    md.append("|---|---|---|---|---|---|")
    for j, s in enumerate(p["steps"], 1):
        md.append(f"| {j} | {s['skill']} | {s['title']} | {s['does']} | {s['you'] or '—'} | {s['gate'] or '—'} |")
    md.append("")
    arts = [s for s in p["steps"] if s["out"] and s["lines"]]
    if arts:
        md.append("**Artifacts**")
        md.append("")
        for s in arts:
            md.append(f"`{s['out']}`")
            md.append("```")
            md.extend(s["lines"])
            md.append("```")
        md.append("")
    md.append(f"**What it shows:** {p['takeaway']}")
    md.append("")

open(os.path.join(here, "..", "examples.md"), "w").write("\n".join(md))

# ---------- quick reference, read from the workflow doc (single source) ----------
import re
wf = open(os.path.join(here, "..", "ai-native-sdlc.md")).read()
qr_block = re.search(r"### 2\.1 What you type\n(.*?)\n### 2\.2", wf, re.S).group(1)
quickref, moment = [], ""
first_id = {}
for pb in PLAYBOOKS:
    if pb.get("kind") == "skill":
        first_id.setdefault(pb["name"], pb["id"])
first_id.setdefault("start", "feature-m")
for line in qr_block.splitlines():
    m = re.match(r"\|\s*([^|]*?)\s*\|\s*`(/[a-z0-9-]+)[^`]*`\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|", line)
    if not m:
        continue
    moment = m.group(1).strip() or moment
    name = m.group(2)[1:]
    when = re.sub(r"`([^`]*)`", r"\1", m.group(3).strip())
    quickref.append({"moment": moment, "cmd": m.group(2), "when": when, "often": m.group(4).strip(), "id": first_id.get(name)})
assert len(quickref) >= 15, len(quickref)

# ---------- page ----------
data = json.dumps({"product": PRODUCT, "playbooks": PLAYBOOKS, "quickref": quickref}, ensure_ascii=False).replace("</", "<\\/")
tpl = open(os.path.join(here, "template.html")).read()
assert "/*DATA*/" in tpl
open(os.path.join(here, "..", "walkthroughs.html"), "w").write(tpl.replace("/*DATA*/", data))
print("ok", len(routed), "playbooks,", len(around), "skills,", sum(len(p["steps"]) for p in PLAYBOOKS), "steps,", len(quickref), "typed commands,", sum(1 for q in quickref if q["id"]), "with examples")
