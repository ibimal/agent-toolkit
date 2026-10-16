"""Tests for skills/setup/scripts/guard.py, the destructive-command guard.

Each test runs the script as Claude Code would: hook JSON on stdin,
exit 2 to block, exit 0 to allow.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parent.parent / "skills" / "setup" / "scripts" / "guard.py"


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name).resolve()

    def tearDown(self):
        self.tmp.cleanup()

    def run_guard(self, tool, tool_input):
        event = {"tool_name": tool, "tool_input": tool_input, "cwd": str(self.project)}
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project))
        return subprocess.run(
            [sys.executable, str(GUARD)], input=json.dumps(event),
            capture_output=True, text=True, env=env,
        )

    def assertBlocked(self, command):
        result = self.run_guard("Bash", {"command": command})
        self.assertEqual(result.returncode, 2, f"not blocked: {command}")

    def assertAllowed(self, command):
        result = self.run_guard("Bash", {"command": command})
        self.assertEqual(result.returncode, 0, f"blocked: {command}: {result.stderr}")

    def test_blocks_destructive_commands(self):
        for command in [
            "git push --force origin main",
            "git push -f",
            "git push --force-with-lease origin feature",
            "git push origin +main",
            "git push origin --delete old-branch",
            "git push origin :old-branch",
            "git reset --hard HEAD~1",
            "git branch -D feature",
            "git commit -n -m wip",
            "git commit --no-verify -m wip",
            "rm -rf /",
            "rm -rf ~",
            "rm -fr ../other-project",
            "cd build && rm -rf $HOME/tmp",
            "psql -c 'DROP TABLE users'",
            "sqlite3 db.sqlite 'truncate table events'",
        ]:
            self.assertBlocked(command)

    def test_allows_ordinary_commands(self):
        for command in [
            "git push origin feature",
            "git status && git log --oneline -5",
            "git commit -m 'Add parser'",
            "rm -rf build dist",
            "rm -f notes.txt",
            "python3 -m unittest",
            "echo 'drop shadows look nice'",
        ]:
            self.assertAllowed(command)

    def test_locked_paths_block_edits(self):
        locks = self.project / "docs" / "sdlc" / "locks"
        locks.parent.mkdir(parents=True)
        locks.write_text("# protected\ntests/test_regression.py\nmigrations/*\n")
        blocked = self.run_guard("Edit", {"file_path": str(self.project / "tests" / "test_regression.py")})
        self.assertEqual(blocked.returncode, 2)
        glob_blocked = self.run_guard("Write", {"file_path": "migrations/0001_init.sql"})
        self.assertEqual(glob_blocked.returncode, 2)
        allowed = self.run_guard("Edit", {"file_path": "src/app.py"})
        self.assertEqual(allowed.returncode, 0)

    def test_bad_input_is_not_a_block(self):
        result = subprocess.run([sys.executable, str(GUARD)], input="not json", capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
