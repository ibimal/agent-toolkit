"""Tests for bin/toolkit.

Each test copies bin/toolkit into a temporary repo that holds test skills,
a test config, and a test style file. The test then runs the copy as a
subprocess, with HOME set to a temporary folder. The real repo and the real
home folder are never touched.

Run from the repo root: python3 -m unittest discover -s tests
"""

import os
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


if __name__ == "__main__":
    unittest.main()
