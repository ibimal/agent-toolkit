"""Consistency checks for ai-native-sdlc.md: the catalog matches sections 2 and 2.3,
the typed-skill order matches 2.1, section references resolve, and principles are numbered."""
import re, sys
import os
DOC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai-native-sdlc.md")
doc = open(DOC).read()
def section(n):
    m = re.search(rf"^## {n}\..*?(?=^## \d+\.|\Z)", doc, re.S | re.M)
    return m.group(0) if m else ""
# catalog
cat = section(10)
catalog = []
for line in cat.splitlines():
    m = re.match(r"\| `([a-z0-9-]+)` \|", line)
    if m: catalog.append(m.group(1))
dups = sorted({c for c in catalog if catalog.count(c) > 1})
catalog_set = set(catalog)
print("catalog:", len(catalog), "dups:", dups)
s2 = section(2)
typed = re.findall(r"\| `/([a-z0-9-]+)", s2)
block = re.search(r"```(.*?)```", s2, re.S).group(1)
runs = []
for line in block.splitlines():
    parts = re.split(r"\s{2,}", line.strip(), maxsplit=1)
    if len(parts) == 2 and not parts[0].startswith("Playbooks"):
        runs += [n.strip() for n in parts[1].split("·") if n.strip()]
print("typed:", len(typed), "runs:", len(runs))
both = set(typed) & set(runs)
print("in both 2.1 and 2.2:", sorted(both))
print("catalog not in section 2:", sorted(catalog_set - set(typed) - set(runs)))
print("section 2 not in catalog:", sorted((set(typed) | set(runs)) - catalog_set))
# typed-only + agent-startable lists in 2.3
s23 = re.search(r"### 2\.3.*", s2, re.S).group(0)
typed_only = re.findall(r"`([a-z0-9-]+)`", re.search(r"Typed only:(.*?)\n", s23.split("Typed only:**",1)[1]).group(1)) if "Typed only:" in s23 else []
m = re.search(r"Typed only: (.*?)\.\n", s23)
typed_only = re.findall(r"`([a-z0-9-]+)`", m.group(1)) if m else []
agent_typed = re.findall(r"^  - `([a-z0-9-]+)`(?: and `([a-z0-9-]+)`)?", s23, re.M)
agent_typed = [x for pair in agent_typed for x in pair if x]
print("typed-only:", len(typed_only), "typed+agent:", len(agent_typed))
print("2.1 typed not classified in 2.3:", sorted(set(typed) - set(typed_only) - set(agent_typed)))
print("classified but not typed:", sorted((set(typed_only) | set(agent_typed)) - set(typed)))
# catalog order vs 2.1 order
cat_typed = catalog[:len(typed)]
print("catalog typed order matches 2.1:", cat_typed == typed)
# backticked skill-ish tokens not in catalog
ticks = set(re.findall(r"`/?([a-z][a-z0-9-]*)`", doc))
print("backticked not in catalog:", sorted(t for t in ticks if t not in catalog_set))
# old names
for old in ["ketchup", "`teach`", "`compound`", "skill-scanner", "Starter set", "agent-picked", "Picked by the agent", "everyday skill from"]:
    hits = [i+1 for i,l in enumerate(doc.splitlines()) if old in l]
    if hits: print("old name", old, "lines", hits)
# section refs
heads = set(re.findall(r"^###? (\d+(?:\.\d+)?)", doc, re.M))
refs = re.findall(r"(?<![\d.])(\d{1,2}\.\d)(?![\d%])", doc)
bad = sorted({r for r in refs if r not in heads and not r.startswith("0.") and r not in ("2.0","1.4","3.8","0.8")})
print("section-like refs not matching a heading:", bad)
# principles
pr = section(1)
nums = [int(n) for n in re.findall(r"^(\d+)\. \*\*", pr, re.M)]
print("principles ok:", nums == list(range(1, len(nums)+1)))
# playbook sequences words
pb = section(4).split("### 4.1")[0]
words=set()
for line in pb.splitlines():
    if line.startswith("| ") and not line.startswith("| Playbook") and not line.startswith("|---"):
        seq = re.sub(r"\([^)]*\)", "", line.split("|")[2])
        for tok in re.split(r"→|;|,", seq):
            m = re.match(r"\s*([a-z][a-z0-9-]+)", tok)
            if m: words.add(m.group(1))
print("playbook words not in catalog:", sorted(w for w in words if w not in catalog_set))
