[简体中文](README.md) · **English**

# Daymix · 今天呢

**What is today like?** Open a small daily card: four symbolic signs, three reflective lenses, and one practical action adjusted for available conditions. Daymix has one reproducible Python engine and corpus, one canonical Agent Skill, one cross-platform MCP tool, a CLI, and an optional expandable MCP Apps card.

```bash
python scripts/daymix.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo
```

The card for that example begins `Daymix · 今天呢｜09-23 · 八月十三` and rates the four signs `中吉`. Use `--format json` for the complete ledger or `--expand all` for explanations and source links. A connected MCP host calls `get_daily_card` once; the widget expands locally. A Skill alone returns a text card.

Yi, tarot, Daoist signs, and astrology contribute -1/0/+1 editorial symbolic scores. Buddhist, Christian, and Stoic prompts do not score. Supplied weather alerts and the weekend rule can change effective actions but do not redraw signs. Reproducing a **complete result** requires the same date, timezone, identity alias or local installation ID, engine and corpus versions, study context, and weather input; the last two do not change the original signs. `--engine v1` and `--engine v2.1` replay historical Wanxiangli outputs; v2.2 uses a new corpus and `daymix/2` schema.

## Run and install

The repository and CI are tested with Python 3.12 and Node.js 24. The [Skill source](skills/daymix/SKILL.md) can be installed directly; `python tools/build_release.py` produces `dist/daymix-skill.zip` and `dist/daymix-plugin.zip`. Start local MCP with `node ui/stdio.mjs`, or Streamable HTTP with `npm run start --prefix ui`; both use the same `get_daily_card` contract. See [compatibility and deployment status](COMPATIBILITY.md) before claiming host support. For the CLI, run `python scripts/daymix.py --format json` or `--expand daoism|christianity|all`. The default local mode keeps a private installation ID for historical replay; `--identity-mode hosted` instead uses a shared guest card and does not create that ID.

The CLI never fetches weather automatically. `--weather-json` accepts caller-supplied `description`, `hazard`, `source`, and `observed_at`; it does not verify location, provenance, or freshness. The MCP tool currently has no weather argument. For an interactive ChatGPT card, deploy and connect the [MCP Apps server](ui/README.md); the ZIP alone does not deploy it.

For the website, run `python web/app.py` and open `http://127.0.0.1:8000/`. It uses the same Python engine, stores each actual full ledger in website-only SQLite storage, and offers anonymous history and a recovery code for another device. No email, phone number, account, or LLM API is involved. The recovery code is scrypt-hashed on the server; the database still needs durable storage and backups. `Dockerfile` packages the website service. Codex Sites cannot directly run this Python process, so a Sites frontend would require a separately deployed Daymix API; no public backend has been configured here.

The v2.2 Daoist collection follows 365 Wikisource sign pages, with four documented transcription or field anomalies and no page-by-page scan collation yet. Its Christian pool has 40 original thematic Old Testament–New Testament pairings, not the Moravian Church's official daily sequence. Chinese paraphrases are project-authored. These cultural and reflective outputs do not predict events or replace medical, legal, financial, safety, or religious advice.

[Chinese README](README.md) · [Current design and evidence](DESIGN.md) · [Compatibility](COMPATIBILITY.md) · [Version changes](CHANGELOG.md) · [Corpus report](CORPUS_COMPLETENESS.md) · [Sources and rights](SOURCES.md) · [Disclaimer](DISCLAIMER.md) · [Religious content policy](RELIGIOUS_CONTENT_POLICY.md) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)
