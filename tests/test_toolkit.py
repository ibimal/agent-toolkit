"""Tests for bin/toolkit.

Each test copies bin/toolkit into a temporary repo that holds test skills,
a test config, and a test style file. The test then runs the copy as a
subprocess, with HOME set to a temporary folder. The real repo and the real
home folder are never touched.

Run from the repo root: python3 -m unittest discover -s tests
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REAL_REPO = Path(__file__).resolve().parent.parent
MARKER_START = "<!-- agent-toolkit:start -->"
MARKER_END = "<!-- agent-toolkit:end -->"

# Two harnesses, one for each instructions method. The "both" reader scans
# both skill folders, like VS Code scans ~/.claude/skills and ~/.copilot/skills.
CONFIG = """\
[harness.imp]
detect = "~/.imp"
skills_dir = "~/.imp/skills"
instructions_file = "~/.imp/RULES.md"
instructions_method = "import"

[harness.sym]
detect = "~/.sym"
skills_dir = "~/.sym/skills"
instructions_file = "~/.sym/rules.md"
instructions_method = "symlink"

[skill_readers]
both = ["~/.imp/skills", "~/.sym/skills"]
"""


def skill_md(name: str, description: str = "A test skill.", extra: str = "") -> str:
    return f"---\nname: {name}\ndescription: {description}\n{extra}---\n\n# {name}\n"


class ToolkitTestCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name).resolve()

        self.repo = root / "repo"
        (self.repo / "bin").mkdir(parents=True)
        shutil.copy2(REAL_REPO / "bin" / "toolkit", self.repo / "bin" / "toolkit")
        (self.repo / "config.toml").write_text(CONFIG)
        self.style = self.repo / "instructions" / "technical-clarity.md"
        self.style.parent.mkdir()
        self.style.write_text("# Style\n")
        for name in ("alpha", "beta"):
            self.add_skill(name, skill_md(name))

        self.home = root / "home"
        self.imp = self.home / ".imp"
        self.sym = self.home / ".sym"
        self.imp.mkdir(parents=True)
        self.sym.mkdir()
        self.rules_imp = self.imp / "RULES.md"
        self.rules_sym = self.sym / "rules.md"
        self.block = f"{MARKER_START}\n@{self.style}\n{MARKER_END}"

    def add_skill(self, folder: str, text: str) -> None:
        path = self.repo / "skills" / folder
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(text)

    def toolkit(self, *args: str, repo: Path | None = None) -> subprocess.CompletedProcess:
        script = (repo or self.repo) / "bin" / "toolkit"
        result = subprocess.run(
            [sys.executable, str(script), *args],
            env={**os.environ, "HOME": str(self.home)},
            capture_output=True,
            text=True,
        )
        self.assertNotIn("Traceback", result.stderr, result.stderr)
        return result

    def snapshot(self) -> dict[str, str]:
        """Describe every path under the temp home and repo, so a test can
        assert that a command changed nothing."""
        state = {}
        for base in (self.home, self.repo):
            for dirpath, dirnames, filenames in os.walk(base):
                for name in dirnames + filenames:
                    path = Path(dirpath) / name
                    key = f"{base.name}/{path.relative_to(base)}"
                    if path.is_symlink():
                        state[key] = "-> " + os.readlink(path)
                    elif path.is_file():
                        state[key] = path.read_text()
                    else:
                        state[key] = "<dir>"
        return state

    def assertLinked(self, link: Path, target: Path) -> None:
        self.assertTrue(link.is_symlink(), f"{link} is not a symlink")
        self.assertEqual(link.resolve(), target.resolve())

    def assertSkillsLinked(self, *names: str) -> None:
        for skills_dir in (self.imp / "skills", self.sym / "skills"):
            for name in names:
                self.assertLinked(skills_dir / name, self.repo / "skills" / name)


class InstallUninstallTest(ToolkitTestCase):
    def test_install_links_everything_and_is_idempotent(self):
        self.assertEqual(self.toolkit("install").returncode, 0)
        self.assertSkillsLinked("alpha", "beta")
        self.assertEqual(self.rules_imp.read_text(), self.block + "\n")
        self.assertLinked(self.rules_sym, self.style)

        before = self.snapshot()
        result = self.toolkit("install")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_uninstall_removes_only_what_install_added(self):
        self.rules_imp.write_text("MY RULES\n")
        self.toolkit("install")
        self.assertEqual(self.rules_imp.read_text(), "MY RULES\n\n" + self.block + "\n")

        self.assertEqual(self.toolkit("uninstall").returncode, 0)
        self.assertEqual(self.rules_imp.read_text(), "MY RULES\n")
        self.assertFalse(os.path.lexists(self.rules_sym))
        self.assertEqual(list((self.imp / "skills").iterdir()), [])
        self.assertEqual(list((self.sym / "skills").iterdir()), [])

    def test_uninstall_keeps_lines_added_around_the_block(self):
        self.toolkit("install")
        self.rules_imp.write_text("BEFORE\n\n" + self.rules_imp.read_text() + "AFTER\n")
        self.toolkit("uninstall")
        self.assertEqual(self.rules_imp.read_text(), "BEFORE\n\nAFTER\n")

    def test_dry_run_changes_nothing(self):
        self.rules_sym.write_text("ORIGINAL\n")
        before = self.snapshot()
        result = self.toolkit("install", "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertIn("link:", result.stdout)
        self.assertEqual(self.snapshot(), before)

        self.toolkit("install")
        before = self.snapshot()
        result = self.toolkit("uninstall", "--dry-run")
        self.assertEqual(result.returncode, 0)
        self.assertIn("restore backup:", result.stdout)
        self.assertEqual(self.snapshot(), before)

    def test_install_prunes_link_to_removed_skill(self):
        self.toolkit("install")
        shutil.rmtree(self.repo / "skills" / "beta")
        self.assertEqual(self.toolkit("install").returncode, 0)
        self.assertFalse(os.path.lexists(self.imp / "skills" / "beta"))
        self.assertFalse(os.path.lexists(self.sym / "skills" / "beta"))
        self.assertSkillsLinked("alpha")

    def test_install_replaces_repo_link_with_wrong_target(self):
        (self.imp / "skills").mkdir()
        (self.imp / "skills" / "alpha").symlink_to(self.repo / "skills" / "beta")
        self.assertEqual(self.toolkit("install").returncode, 0)
        self.assertSkillsLinked("alpha", "beta")

    def test_symlink_method_backs_up_and_restores_file(self):
        self.rules_sym.write_text("ORIGINAL\n")
        self.toolkit("install")
        self.assertEqual((self.sym / "rules.md.pre-toolkit").read_text(), "ORIGINAL\n")
        self.assertLinked(self.rules_sym, self.style)

        self.assertEqual(self.toolkit("uninstall").returncode, 0)
        self.assertFalse(self.rules_sym.is_symlink())
        self.assertEqual(self.rules_sym.read_text(), "ORIGINAL\n")
        self.assertFalse(os.path.lexists(self.sym / "rules.md.pre-toolkit"))

    def test_skills_folder_linked_into_repo_is_replaced(self):
        # An older setup linked the whole skills folder to the repo. Before
        # the fix, install renamed the repo's own skill folders.
        (self.imp / "skills").symlink_to(self.repo / "skills")
        self.assertEqual(self.toolkit("install").returncode, 0)
        repo_skills = sorted(p.name for p in (self.repo / "skills").iterdir())
        self.assertEqual(repo_skills, ["alpha", "beta"])
        self.assertFalse((self.repo / "skills" / "alpha").is_symlink())
        self.assertFalse((self.imp / "skills").is_symlink())
        self.assertSkillsLinked("alpha", "beta")

    def test_harness_without_detect_folder_is_skipped(self):
        shutil.rmtree(self.sym)
        result = self.toolkit("install")
        self.assertEqual(result.returncode, 0)
        self.assertIn("[skip] sym", result.stdout)
        self.assertFalse(self.sym.exists())


class ConflictTest(ToolkitTestCase):
    """install and uninstall must skip and report any path that did not
    come from this repo, and still handle the other paths."""

    def test_foreign_skill_is_skipped_not_backed_up(self):
        foreign = self.imp / "skills" / "alpha"
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text(skill_md("alpha", "Mine."))

        result = self.toolkit("install")
        self.assertEqual(result.returncode, 1)
        self.assertIn("conflict", result.stderr)
        self.assertFalse(foreign.is_symlink())
        self.assertEqual((foreign / "SKILL.md").read_text(), skill_md("alpha", "Mine."))
        self.assertFalse(os.path.lexists(self.imp / "skills" / "alpha.pre-toolkit"))
        # Everything else is still installed.
        self.assertLinked(self.imp / "skills" / "beta", self.repo / "skills" / "beta")
        self.assertLinked(self.sym / "skills" / "alpha", self.repo / "skills" / "alpha")
        self.assertIn(self.block, self.rules_imp.read_text())

    def test_link_from_old_clone_is_skipped(self):
        (self.imp / "skills").mkdir()
        old = self.imp / "skills" / "alpha"
        old.symlink_to("/nonexistent/old-clone/skills/alpha")

        result = self.toolkit("install")
        self.assertEqual(result.returncode, 1)
        self.assertIn("old clone", result.stderr)
        self.assertEqual(os.readlink(old), "/nonexistent/old-clone/skills/alpha")
        self.assertLinked(self.imp / "skills" / "beta", self.repo / "skills" / "beta")

    def test_second_backup_is_a_conflict(self):
        self.rules_sym.write_text("ORIGINAL\n")
        self.toolkit("install")
        self.rules_sym.unlink()
        self.rules_sym.write_text("WRITTEN AFTER INSTALL\n")

        result = self.toolkit("install")
        self.assertEqual(result.returncode, 1)
        self.assertIn("earlier backup", result.stderr)
        self.assertEqual(self.rules_sym.read_text(), "WRITTEN AFTER INSTALL\n")
        self.assertEqual((self.sym / "rules.md.pre-toolkit").read_text(), "ORIGINAL\n")

    def test_uninstall_keeps_file_written_after_install(self):
        self.rules_sym.write_text("ORIGINAL\n")
        self.toolkit("install")
        self.rules_sym.unlink()
        self.rules_sym.write_text("WRITTEN AFTER INSTALL\n")

        result = self.toolkit("uninstall")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.rules_sym.read_text(), "WRITTEN AFTER INSTALL\n")
        self.assertEqual((self.sym / "rules.md.pre-toolkit").read_text(), "ORIGINAL\n")

    def test_import_refuses_symlinked_file(self):
        dotfile = self.home / "dotfiles" / "RULES.md"
        dotfile.parent.mkdir()
        dotfile.write_text("MY GLOBAL RULES\n")
        self.rules_imp.symlink_to(dotfile)

        result = self.toolkit("install")
        self.assertEqual(result.returncode, 1)
        self.assertIn("will not write through it", result.stderr)
        self.assertLinked(self.rules_imp, dotfile)
        self.assertEqual(dotfile.read_text(), "MY GLOBAL RULES\n")
        self.assertFalse(os.path.lexists(self.imp / "RULES.md.pre-toolkit"))

    def test_import_accepts_symlinked_file_that_has_the_block(self):
        dotfile = self.home / "dotfiles" / "RULES.md"
        dotfile.parent.mkdir()
        dotfile.write_text("MY GLOBAL RULES\n\n" + self.block + "\n")
        self.rules_imp.symlink_to(dotfile)

        self.assertEqual(self.toolkit("install").returncode, 0)
        self.assertEqual(self.toolkit("doctor").returncode, 0)
        before = dotfile.read_text()
        self.assertEqual(self.toolkit("uninstall").returncode, 0)
        self.assertEqual(dotfile.read_text(), before)

    def test_broken_markers_are_left_alone(self):
        self.toolkit("install")
        text = self.rules_imp.read_text().replace(MARKER_END + "\n", "")
        self.rules_imp.write_text(text + "USER LINE A\nUSER LINE B\n")
        before = self.rules_imp.read_text()

        result = self.toolkit("install")
        self.assertEqual(result.returncode, 1)
        self.assertIn("exactly one", result.stderr)
        self.assertEqual(self.rules_imp.read_text(), before)

        self.assertEqual(self.toolkit("uninstall").returncode, 1)
        self.assertEqual(self.rules_imp.read_text(), before)

    def test_skills_folder_linked_elsewhere_is_refused(self):
        elsewhere = self.home / "dotfiles" / "skills"
        elsewhere.mkdir(parents=True)
        (self.imp / "skills").symlink_to(elsewhere)

        result = self.toolkit("install")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Replace it with a real folder", result.stderr)
        self.assertEqual(list(elsewhere.iterdir()), [])


class CheckTest(ToolkitTestCase):
    def test_real_repo_passes_check(self):
        result = self.toolkit("check", repo=REAL_REPO)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_style_file_fails_check_and_install(self):
        self.style.unlink()
        before = self.snapshot()
        result = self.toolkit("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("[FAIL] instructions/technical-clarity.md", result.stdout)
        self.assertEqual(self.toolkit("install").returncode, 1)
        self.assertEqual(self.snapshot(), before)

    def test_bad_config_fails_check_and_other_commands(self):
        (self.repo / "config.toml").write_text(
            '[harness.bad]\ninstructions_file = "~/x"\ninstructions_method = "copy"\n'
        )
        result = self.toolkit("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("is missing: detect", result.stdout)
        self.assertIn("not 'copy'", result.stdout)
        for command in ("doctor", "uninstall"):
            result = self.toolkit(command)
            self.assertEqual(result.returncode, 1)
            self.assertIn("config.toml cannot be used", result.stderr)

    def test_config_rejects_home_agents_md(self):
        # Claude Code would read these as AGENTS.md in every project under
        # the home folder, next to the import in ~/.claude/CLAUDE.md.
        for path in ("~/AGENTS.md", "~/.claude/AGENTS.md", "~/.claude/../AGENTS.md"):
            with self.subTest(path=path):
                (self.repo / "config.toml").write_text(
                    f'[harness.x]\ndetect = "~/.imp"\ninstructions_file = "{path}"\n'
                    'instructions_method = "symlink"\n'
                )
                result = self.toolkit("check")
                self.assertEqual(result.returncode, 1)
                self.assertIn("reads as AGENTS.md", result.stdout)
                self.assertEqual(self.toolkit("install").returncode, 1)
                self.assertFalse(os.path.lexists(self.home / "AGENTS.md"))

    def test_skill_rules(self):
        long_text = "x" * 1025
        self.add_skill("Bad_Name", skill_md("Bad_Name"))
        self.add_skill("mismatch", skill_md("other-name"))
        self.add_skill("long-description", skill_md("long-description", long_text))
        self.add_skill(
            "long-folded",
            f"---\nname: long-folded\ndescription: >-\n  {long_text}\n---\n",
        )
        self.add_skill("empty-folded", "---\nname: empty-folded\ndescription: >\n---\n")
        self.add_skill("short-folded", "---\nname: short-folded\ndescription: >\n  Fine.\n---\n")
        self.add_skill("extra-field", skill_md("extra-field", extra="version: 1\n"))
        self.add_skill(
            "with-metadata",
            skill_md("with-metadata", extra="metadata:\n  status: draft\n"),
        )

        result = self.toolkit("check")
        self.assertEqual(result.returncode, 1)
        out = result.stdout
        self.assertIn("[FAIL] Bad_Name", out)
        self.assertIn("does not match folder name 'mismatch'", out)
        self.assertIn("[FAIL] long-description", out)
        self.assertIn("[FAIL] long-folded", out)
        self.assertIn("[FAIL] empty-folded", out)
        self.assertIn("[OK]   short-folded", out)
        self.assertIn("non-spec fields: version", out)
        self.assertIn("[OK]   with-metadata", out)

    def test_values_that_break_yaml(self):
        # A YAML parser rejects or cuts short the first five. The last two
        # are valid, because quotes and block scalars may hold ': '.
        cases = {
            "colon": "description: Use when: the user is lost.\n",
            "trailing-colon": "description: Use when:\n",
            "comment": "description: Shorten it #fast\n",
            "indicator": "description: *starred\n",
            "continued-colon": "description: Restate it.\n  Use when: lost.\n",
            "quoted": 'description: "Use when: the user is lost."\n',
            "folded": "description: >\n  Use when: the user is lost.\n",
        }
        for name, description in cases.items():
            self.add_skill(name, f"---\nname: {name}\n{description}---\n")

        result = self.toolkit("check")
        self.assertEqual(result.returncode, 1)
        for name in ("colon", "trailing-colon", "comment", "indicator", "continued-colon"):
            self.assertIn(f"[FAIL] {name}", result.stdout)
        for name in ("quoted", "folded"):
            self.assertIn(f"[OK]   {name}", result.stdout)
        self.assertIn("Put the value in double quotes", result.stdout)

    def test_leak_scan(self):
        # Built from parts, so this file does not trip the real repo's scan.
        email = "alice" + "@" + "corp-mail.io"
        home = "/Us" + "ers/alice/notes"
        token = "gh" + "p_" + "a1B2" * 9
        (self.repo / "notes.md").write_text(
            f"Mail {email}.\nSee {home}.\nToken {token}\n"
            "Safe: git@github.com, 1+me@users.noreply.github.com, "
            "bob@example.com, ~/.config/home/x\n"
        )
        result = self.toolkit("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("notes.md:1 has what looks like an email address", result.stdout)
        self.assertIn("notes.md:2 has what looks like a home folder path", result.stdout)
        self.assertIn("notes.md:3 has what looks like an access token", result.stdout)
        self.assertNotIn("notes.md:4", result.stdout)
        # The report names the kind and place, never the matched text.
        for secret in (email, home, token):
            self.assertNotIn(secret, result.stdout)

    def test_references_and_links(self):
        self.add_skill("gamma", skill_md("gamma", "Not for this (use alpha or ghost)."))
        self.add_skill(
            "delta",
            skill_md("delta")
            + "See [ref](references/ref.md), [gone](missing.md), "
            "[up](../alpha/SKILL.md), and [web](https://example.com/page).\n",
        )
        (self.repo / "skills" / "delta" / "references").mkdir()
        (self.repo / "skills" / "delta" / "references" / "ref.md").write_text(
            "More in [deep](deep.md).\n"
        )
        self.add_skill("epsilon", skill_md("epsilon") + "See [ref](references/ref.md#part).\n")
        (self.repo / "skills" / "epsilon" / "references").mkdir()
        (self.repo / "skills" / "epsilon" / "references" / "ref.md").write_text("Done.\n")

        out = self.toolkit("check").stdout
        self.assertIn("refers to skill 'ghost'", out)
        self.assertNotIn("refers to skill 'alpha'", out)
        self.assertIn("link 'missing.md' points to a missing file", out)
        self.assertIn("link '../alpha/SKILL.md' points outside the skill folder", out)
        self.assertIn("'references/ref.md' links to more local files (deep.md)", out)
        self.assertNotIn("example.com", out)
        self.assertIn("[OK]   epsilon", out)


class DoctorTest(ToolkitTestCase):
    def test_clean_install_has_no_problems_and_notes_duplicates(self):
        self.toolkit("install")
        result = self.toolkit("doctor")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("note: both finds alpha, beta", result.stdout)

    def test_reports_missing_install(self):
        result = self.toolkit("doctor")
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not exist. Run install.", result.stdout)
        self.assertIn("RULES.md is missing", result.stdout)

    def test_reports_broken_link(self):
        self.toolkit("install")
        (self.imp / "skills" / "ghost").symlink_to("/nonexistent")
        result = self.toolkit("doctor")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ghost is a broken link", result.stdout)

    def test_reports_backup_in_scanned_folder(self):
        self.toolkit("install")
        backup = self.imp / "skills" / "alpha.pre-toolkit"
        backup.mkdir()
        (backup / "SKILL.md").write_text(skill_md("alpha"))
        result = self.toolkit("doctor")
        self.assertEqual(result.returncode, 1)
        self.assertIn("second skill", result.stdout)

    def test_reports_duplicate_with_different_content(self):
        foreign = self.sym / "skills" / "alpha"
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text(skill_md("alpha", "Mine."))
        self.toolkit("install")
        result = self.toolkit("doctor")
        self.assertEqual(result.returncode, 1)
        self.assertIn("both finds 'alpha'", result.stdout)


class RepoDocsTest(unittest.TestCase):
    """README.md and AGENTS.md state facts that the repo can confirm, such
    as its layout and its commands. These tests keep the docs in step."""

    readme = (REAL_REPO / "README.md").read_text()

    def section(self, heading: str) -> str:
        return self.readme.split(f"## {heading}\n", 1)[1].split("\n## ", 1)[0]

    def test_layout_paths_exist(self):
        block = self.section("Layout").split("```")[1]
        found, missing, stack = [], [], []
        for line in block.splitlines():
            m = re.match(r"^((?:│   |    )*)[├└]── (.+)$", re.sub(r"\s+#.*$", "", line))
            if not m:
                continue
            depth = len(m.group(1)) // 4
            stack = stack[:depth] + [m.group(2).strip().rstrip("/")]
            path = "/".join(stack)
            found.append(path)
            if not (REAL_REPO / path).exists():
                missing.append(path)
        self.assertGreaterEqual(len(found), 10)
        self.assertEqual(missing, [])

    def test_commands_match_the_cli(self):
        help_text = subprocess.run(
            [sys.executable, str(REAL_REPO / "bin" / "toolkit"), "--help"],
            capture_output=True,
            text=True,
        ).stdout
        commands = set(re.search(r"\{([a-z,]+)\}", help_text).group(1).split(","))
        table = set(re.findall(r"^\| `([a-z-]+)`", self.section("Commands"), re.M))
        self.assertEqual(table, commands)
        agents = (REAL_REPO / "AGENTS.md").read_text()
        for command in commands:
            self.assertIn(f"`{command}`", agents)


if __name__ == "__main__":
    unittest.main()
