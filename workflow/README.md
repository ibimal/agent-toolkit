# AI-native SDLC workflow

The design for an AI-native development workflow: the playbooks, the
skills they use, and the rules that connect them. The skills it names are
built into `skills/` over time. Until a skill exists there, this design is
its spec.

## Files

| File | What it holds | Edit it? |
|---|---|---|
| `ai-native-sdlc.md` | The workflow doc. It states the current rules only. | Yes |
| `src/examples_data.py` | The one source for every worked example | Yes |
| `src/template.html` | The layout of the walkthrough page | Yes |
| `src/build.py` | Generates `examples.md` and `walkthroughs.html` | Yes |
| `src/check_doc.py` | Checks the workflow doc for consistency | Yes |
| `examples.md` | The worked examples, as text | No, generated |
| `walkthroughs.html` | The worked examples as step-by-step walkthroughs. Open it in a browser, or on the site. | No, generated |

## The site

The design is published at <https://ibimal.github.io/agent-toolkit/>.
`.github/workflows/pages.yml` regenerates the files, makes the workflow
doc the homepage, and deploys on each push to `main` that changes
`workflow/`. CI fails a change whose generated files are out of date.

## After a change

Run these from the repo root:

```
python3 workflow/src/build.py
python3 workflow/src/check_doc.py
bin/toolkit check
```

When a playbook or skill changes in the doc, update its example in
`src/examples_data.py` in the same commit.

`check_doc.py` also prints the backticked names that are not in the
catalog. That list is for information only: it holds upstream skill names
and harness commands, which the doc names on purpose.
