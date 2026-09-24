# Daymix · 今天呢

**What is today like?** Open a small daily card: four independent symbolic signs, three reflective lenses, and one practical action checked against real conditions. Daymix is a reproducible single Agent Skill with a CLI and an optional expandable MCP Apps card.

```bash
python scripts/daymix.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo
```

The card for that example begins `Daymix · 今天呢｜09-23 · 八月十三` and rates the four signs `中吉`. Use `--format json` for the complete ledger or `--expand all` for explanations and source links. A connected MCP host calls `get_daily_card` once; the widget expands locally. A Skill alone returns a text card.

Yi, tarot, Daoist signs, and astrology contribute -1/0/+1 editorial symbolic scores. Buddhist, Christian, and Stoic prompts do not score. Verified weather and other real conditions can change effective actions but do not redraw signs. With the same date, timezone, non-sensitive identity alias, and engine version, results repeat. `--engine v1` and `--engine v2.1` replay historical Wanxiangli outputs; v2.2 uses a new corpus and `daymix/2` schema.

The v2.2 Daoist collection follows 365 Wikisource sign pages, with four documented transcription or field anomalies and no page-by-page scan collation yet. Its Christian pool has 40 original thematic Old Testament–New Testament pairings, not the Moravian Church's official daily sequence. Chinese paraphrases are project-authored. These cultural and reflective outputs do not predict events or replace medical, legal, financial, safety, or religious advice.

[Chinese README](README.md) · [Corpus report](CORPUS_COMPLETENESS.md) · [Sources and rights](SOURCES.md) · [Research](RESEARCH_V22.md) · [Disclaimer](DISCLAIMER.md) · [Religious content policy](RELIGIOUS_CONTENT_POLICY.md) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)
