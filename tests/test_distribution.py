"""Validate actual release archives in isolated execution environments."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_release import build_archive, validate, SKILL, PLUGIN_FILES


class DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.place = Path(cls.temp.name)
        files = validate()
        build_archive(cls.place / "skill.zip", [(p, "wanxiangli/" + p.relative_to(SKILL).as_posix()) for p in files])
        build_archive(cls.place / "plugin.zip", [(p, p.relative_to(ROOT).as_posix()) for p in files + list(PLUGIN_FILES)])
        with zipfile.ZipFile(cls.place / "skill.zip") as z:
            z.extractall(cls.place / "standalone")
        cls.entry = cls.place / "standalone/wanxiangli/scripts/wanxiangli.py"

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_skill_package_structure_and_frontmatter(self):
        with zipfile.ZipFile(self.place / "skill.zip") as z:
            self.assertIsNone(z.testzip())
            paths = z.namelist()
            self.assertTrue(paths)
            self.assertTrue(all(p.startswith("wanxiangli/") for p in paths))
            self.assertEqual(paths.count("wanxiangli/SKILL.md"), 1)
            text = z.read("wanxiangli/SKILL.md").decode()
            self.assertTrue(text.startswith("---\nname: wanxiangli\ndescription:"))
            for path in ("references/sources.yaml", "scripts/wanxiangli.py", "vendor/versions.json",
                         "vendor/licenses/lunar-python-LICENSE", "vendor/licenses/astronomy-engine-LICENSE",
                         "RELIGIOUS_CONTENT_POLICY.md", "THIRD_PARTY_NOTICES.md"):
                self.assertIn("wanxiangli/" + path, paths)
            self.assertFalse(any("__pycache__" in p or ".git/" in p or "installation.json" in p for p in paths))

    def test_plugin_manifest_and_compatibility(self):
        with zipfile.ZipFile(self.place / "plugin.zip") as z:
            self.assertIsNone(z.testzip())
            portable = json.loads(z.read("plugin.json"))
            compatibility = json.loads(z.read(".codex-plugin/plugin.json"))
            self.assertEqual(portable["name"], "wanxiangli")
            self.assertEqual(portable["version"], "0.1.0")
            self.assertEqual(compatibility["version"], portable["version"])
            self.assertEqual(compatibility["skills"], "./skills/")
            self.assertIn("skills/wanxiangli/SKILL.md", z.namelist())
            self.assertNotIn("mcpServers", portable)

    def run_skill(self, isolated=False, vendor=True, hosted=False, expand=None):
        command = [sys.executable]
        if isolated:
            command.append("-S")  # suppress site-packages even if installed in the test environment
        command += [str(self.entry), "--date", "2026-09-23", "--timezone", "Asia/Shanghai",
                    "--format", "json"]
        if hosted:
            command += ["--identity-mode", "hosted"]
        else:
            command += ["--user-id", "demo"]
        if expand:
            command += ["--expand", expand]
        env = dict(os.environ, PYTHONPATH="", XDG_CONFIG_HOME=str(self.place / "hosted-config"))
        return subprocess.run(command, cwd=self.place, env=env, text=True, capture_output=True)

    def test_installed_packages_from_other_cwd(self):
        r = self.run_skill()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["date"]["gregorian"], "2026-09-23")

    def test_vendored_packages_without_site_packages(self):
        a = self.run_skill(isolated=True)
        b = self.run_skill(isolated=True)
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)
        ledger = json.loads(a.stdout)
        self.assertEqual(ledger["schema"], "wanxiangli/1")
        self.assertIn("yijing", ledger["systems"])
        for section in ("佛家", "塔罗"):
            expanded = self.run_skill(isolated=True, expand=section)
            self.assertEqual(expanded.returncode, 0, expanded.stderr)
            self.assertIn("今日总结：", expanded.stdout)
            if section == "塔罗":
                self.assertIn(ledger["systems"]["tarot"]["name"], expanded.stdout)

    def test_missing_packages_fail_explicitly(self):
        vendor = self.entry.parents[1] / "vendor"
        moved = self.place / "vendor-temporarily-disabled"
        vendor.rename(moved)
        try:
            r = self.run_skill(isolated=True)
            self.assertEqual(r.returncode, 2)
            self.assertEqual(r.stdout, "")
            self.assertIn("无法计算", r.stderr)
        finally:
            moved.rename(vendor)

    def test_hosted_guest_does_not_write_installation_id(self):
        r = self.run_skill(isolated=True, hosted=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.place / "hosted-config/wanxiangli/installation.json").exists())
        self.assertNotIn("guest", r.stdout)

    def test_trigger_and_policy_stay_with_skill(self):
        text = (SKILL / "SKILL.md").read_text()
        for trigger in ("查看今日运势", "今日运势", "展开佛家", "展开道家", "查看塔罗", "查看易理",
                        "查看星象", "查看现实修正", "查看今日推演详情"):
            self.assertIn(trigger, text)
        root_policy = (ROOT / "RELIGIOUS_CONTENT_POLICY.md").read_text()
        self.assertEqual((SKILL / "RELIGIOUS_CONTENT_POLICY.md").read_text(),
                         root_policy.replace("skills/wanxiangli/references/sources.yaml", "references/sources.yaml"))


if __name__ == "__main__":
    unittest.main()
