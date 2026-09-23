#!/usr/bin/env python3
"""Validate the canonical Skill and produce reproducible, minimal release archives."""
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "wanxiangli"
DIST = ROOT / "dist"
PLUGIN_FILES = (ROOT / "plugin.json", ROOT / ".codex-plugin/plugin.json",
                ROOT / "LICENSE", ROOT / "THIRD_PARTY_NOTICES.md",
                ROOT / "scripts/wanxiangli.py", ROOT / "ui/server.mjs", ROOT / "ui/package.json",
                ROOT / "ui/package-lock.json", ROOT / "ui/card.html", ROOT / "ui/card.js",
                ROOT / "ui/build.mjs", ROOT / "ui/dist/card.html", ROOT / "ui/test.mjs", ROOT / "ui/test-server.mjs", ROOT / "ui/README.md")
SKILL_REQUIRED = ("SKILL.md", "scripts/wanxiangli.py", "references/sources.yaml",
                  "references/eastern/hexagrams.json", "references/eastern/zhouyi-text.json",
                  "references/tarot/tarot-78.json", "references/tarot/tarot-v2.json",
                  "references/daoism/verified-signs.json", "references/christianity/watchwords.json",
                  "assets/icon.svg", "agents/openai.yaml", "LICENSE",
                  "RELIGIOUS_CONTENT_POLICY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
                  "THIRD_PARTY_NOTICES.md")
FORBIDDEN_NAMES = {".git", "__pycache__", ".pytest_cache", ".env", "installation.json",
                   "credentials", "cookies", "id_rsa", ".DS_Store"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".log", ".key"}
SECRET_PATTERNS = (rb"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----", rb"ghp_[A-Za-z0-9]{30,}",
                   rb"sk-[A-Za-z0-9]{30,}", rb"AKIA[A-Z0-9]{16}")


def check_file(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"non-regular file: {path}")
    if any(part in FORBIDDEN_NAMES or part.startswith(".env") for part in path.parts):
        raise ValueError(f"forbidden package path: {path}")
    if path.suffix in FORBIDDEN_SUFFIXES:
        raise ValueError(f"forbidden package extension: {path}")
    data = path.read_bytes()
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, data):
            raise ValueError(f"possible credential in: {path}")
    return data


def digest_tree(directory):
    h = hashlib.sha256()
    for path in sorted(directory.rglob("*.py")):
        h.update(path.relative_to(directory).as_posix().encode())
        h.update(b"\0")
        h.update(path.read_bytes())
    return h.hexdigest()


def validate():
    for name in SKILL_REQUIRED:
        check_file(SKILL / name)
    for p in PLUGIN_FILES:
        check_file(p)
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not re.search(r"^---\nname: wanxiangli\ndescription: .+\n---\n", skill_text):
        raise ValueError("Skill front matter missing or inconsistent")
    for name in re.findall(r"`((?:references|scripts|assets)/[^`\s]+|RELIGIOUS_CONTENT_POLICY\.md)`", skill_text):
        check_file(SKILL / name)
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    compatibility = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("unsupported portable plugin schema")
    if manifest["name"] != "wanxiangli" or not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
        raise ValueError("invalid plugin name or version")
    if "skills" in manifest or "mcpServers" in manifest:
        raise ValueError("portable manifest declares redundant or missing components")
    if compatibility["skills"] != "./skills/" or (ROOT / compatibility["skills"] / "wanxiangli/SKILL.md").resolve() != (SKILL / "SKILL.md").resolve():
        raise ValueError("compatibility skills path differs from canonical Skill")
    for field in ("name", "version", "description"):
        if manifest[field] != compatibility[field]:
            raise ValueError(f"manifest conflict: {field}")
    versions = json.loads((SKILL / "vendor/versions.json").read_text(encoding="utf-8"))
    if {(v["distribution"], v["version"]) for v in versions} != {("lunar-python", "1.4.8"), ("astronomy-engine", "2.1.19")}:
        raise ValueError("vendored dependency versions differ from audited pins")
    for entry in versions:
        package = SKILL / "vendor" / entry["module"]
        check_file(package / "__init__.py")
        check_file(SKILL / "vendor" / entry["license_file"])
        if entry["license"] != "MIT" or entry["modified"] or digest_tree(package) != entry["vendored_tree_sha256"]:
            raise ValueError(f"vendored package integrity mismatch: {entry['module']}")
    if (SKILL / "LICENSE").read_bytes() != (ROOT / "LICENSE").read_bytes():
        raise ValueError("Skill license differs from root")
    for name in ("RELIGIOUS_CONTENT_POLICY.md", "CONTRIBUTING.md"):
        expected = (ROOT / name).read_text(encoding="utf-8").replace("skills/wanxiangli/references/sources.yaml", "references/sources.yaml")
        if (SKILL / name).read_text(encoding="utf-8") != expected:
            raise ValueError(f"Skill {name} differs from root")
    if (SKILL / "CODE_OF_CONDUCT.md").read_bytes() != (ROOT / "CODE_OF_CONDUCT.md").read_bytes():
        raise ValueError("Skill code of conduct differs from root")
    expected = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8").replace("skills/wanxiangli/vendor/", "vendor/")
    if (SKILL / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8") != expected:
        raise ValueError("Skill third-party notices differ from root")
    files = sorted(path for path in SKILL.rglob("*") if path.is_file()
                   and not any(part in FORBIDDEN_NAMES or part.startswith(".env") for part in path.parts)
                   and path.suffix not in FORBIDDEN_SUFFIXES)
    for path in files:
        check_file(path)
    return files


def build_archive(destination, entries):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, name in sorted(entries, key=lambda item: item[1]):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, check_file(source), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main():
    files = validate()
    DIST.mkdir(exist_ok=True)
    skill_entries = [(p, "wanxiangli/" + p.relative_to(SKILL).as_posix()) for p in files]
    plugin_entries = [(p, p.relative_to(ROOT).as_posix()) for p in files + list(PLUGIN_FILES)]
    build_archive(DIST / "wanxiangli-skill.zip", skill_entries)
    build_archive(DIST / "wanxiangli-plugin.zip", plugin_entries)
    for name in ("wanxiangli-skill.zip", "wanxiangli-plugin.zip"):
        print(f"{DIST / name} ({(DIST / name).stat().st_size} bytes)")


if __name__ == "__main__":
    main()
