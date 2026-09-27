# Glossary

Use these terms in this repo's docs, code comments, and skills. Each row
names one concept. Do not use the words in the "Avoid" column for it,
because a second name makes the reader wonder whether it means something
different.

| Term | Meaning | Avoid |
|---|---|---|
| harness | An agent tool that loads skills or instructions, such as Claude Code, Copilot CLI, or code-puppy. Each harness is a `[harness.<name>]` table in `config.toml`. | agent tool |
| device | One computer where the repo is cloned and `install` runs. | machine |
| detect folder | The folder whose presence means that a harness is used on a device, such as `~/.claude`. Config key: `detect`. | |
| skill | A folder under `skills/` that holds a `SKILL.md` and follows the Agent Skills specification. | |
| skills folder | The folder where a harness looks for personal skills, such as `~/.claude/skills`. Config key: `skills_dir`. | skills directory |
| skill reader | A tool that scans one or more skills folders, such as VS Code. `doctor` uses the `[skill_readers]` table in `config.toml` to find duplicate skill names. | |
| style file | `instructions/technical-clarity.md`, the one file that holds the style rules. | |
| style rules | The rules in the style file, titled "Response style: technical plain English". They are always on: each harness loads them in every session. | technical-clarity rules |
| instructions file | A harness's global instructions file, such as `~/.claude/CLAUDE.md`. Config key: `instructions_file`. | |
| instructions method | How `install` connects the style file to an instructions file. `import` adds a managed block, and `symlink` replaces the file with a link. | link method |
| managed block | The lines between the `agent-toolkit:start` and `agent-toolkit:end` markers, which `install` owns inside an instructions file. | marker block |
| conflict | A path that `install` or `uninstall` does not change, because it did not come from this repo. The command reports it, skips it, and exits 1. | |
| backup | A file that `install` renamed with the suffix `.pre-toolkit` before replacing it. `uninstall` restores it. | |
| rewrite skills | `plain-restate`, `condense`, and `deepen`. Each rewrites the previous response in one direction and names the other two. | |
| previous response | The agent's last message, which a rewrite skill works on. | |
