# Wanxiangli · 万象历

**English** | [简体中文](README.zh-CN.md)

Wanxiangli is a **single Agent Skill** for a compact personal daily almanac: **calendrical and symbolic inputs → interpretive lenses → reality correction → daily almanac**. It combines real calendar and astronomical calculations with reproducible I Ching and tarot draws. Small source-aware cards offer Buddhist, Daoist, Christian, and Stoic perspectives without presenting those traditions as agreeing with one another. The machinery is deliberately serious; the premise is allowed to be a little absurd.

## Quick start

With the Skill installed, ask **“查看今日运势”**. The first public distribution version is **0.1.0**.

Actual output from this version, reproducible with `python3 skills/wanxiangli/scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo --context 备考`:

```text
万象历 · 9月23日｜八月十三 · 庚子日
今日：中吉
宜  整理生活 · 整理资料 · 梳理路径
忌  草率定约 · 仓促搬动 · 临时改作息
学业 ★★★★☆　财运 ★★★☆☆　人际 ★★★☆☆
备考提示：复盘错题 · 整理旧知识
今日象：渐进，望月期
诸说合参：易理取「渐进」，塔罗示「情感中的出发遇到阻滞或失衡」；佛家取无住，道家取知止，基督宗教借种子与等待之象。诸象合参；裁定中吉。
展开：易理／塔罗／星象／佛家／道家／基督宗教／现实修正
今日总结：今日先复盘错题，避免草率定约。
```

The public `demo` identifier is for reproduction. Without `--user-id`, a private local installation identifier is created. A day's result is stable within that installation, date, and time zone; across devices, provide the same non-sensitive identifier explicitly.

## Install

### ChatGPT (supported Skills environments)

Download `wanxiangli-skill.zip` from the GitHub release. In a ChatGPT environment that supports custom Skill uploads, create or upload a Skill with this ZIP, then ask **查看今日运势**. The archive has one top-level `wanxiangli/` directory containing `SKILL.md`, calculations, references, and pinned dependencies. Availability of uploads, Python execution, weather tools, and filesystem persistence depends on your environment. In a hosted environment without a persistent installation ID, the Skill uses a shared daily guest result; you may optionally give a fixed non-sensitive alias (for example `blue-fish`) for your own reproducible daily result. Do not use an email address or real identity.

### Codex / portable plugin

Download `wanxiangli-plugin.zip` from the GitHub release and install it using your environment's plugin upload or installation flow. The portable `plugin.json` discovers the one Skill under `skills/wanxiangli/`; `.codex-plugin/plugin.json` supports the compatibility format. For a local Codex Skill installation, place the `skills/wanxiangli/` directory in `$HOME/.agents/skills/` (or the repository `.agents/skills/` folder) and restart Skill discovery. The Python interpreter must support Python 3.10+ and IANA time-zone data. Both releases share exactly the same Skill source.

### From source (developers)

```bash
git clone https://github.com/Hei-Chuan/wanxiangli.git
cd wanxiangli
python3 -m pip install -r requirements.txt
python3 skills/wanxiangli/scripts/wanxiangli.py --timezone Asia/Shanghai
python3 -m unittest discover -s tests -v
python3 tools/build_release.py
```

The pinned packages are already bundled inside the Skill. Installing from `requirements.txt` is optional for ordinary Skill users and lets source developers use matching external packages. The script does not download software or make a network request.

## What actually runs

| Layer | Current implementation |
| --- | --- |
| Calendar | [`lunar_python`](https://github.com/6tail/lunar-python) provides lunar dates, solar terms, sexagenary dates, and traditional almanac entries. Original entries remain in JSON; only a few map to modern actions. |
| I Ching | A seeded daily draw from a 64-hexagram index. This is a project-defined daily draw, **not** a yarrow-stalk or changing-line reading; themes and scores are project-authored. |
| Tarot | An independent seeded draw from 78 Rider–Waite–Smith cards plus orientation; short meanings are original notes, not quotations. |
| Astronomy | [Astronomy Engine](https://github.com/cosinekitty/astronomy) calculates solar longitude and the Moon–Sun angle at local noon. Broad lunar-phase labels have symbolic product weight; no birth chart or causal claim is involved. |
| Interpretation | Limited original knowledge cards supply separate lenses. They do not alter a cast; disagreement is allowed. |
| Reality | `--weather-json PATH` accepts externally supplied weather. The Skill can query weather for a known location, but **the script itself has no network request**. Hazardous conditions can withdraw an action suggestion without rewriting source facts or the rating. No holiday or user-calendar integration exists. |

For structured output use `--format json`; for advice-only study wording, `--context 备考`. For details, use `--expand 佛家`, `--expand 塔罗`, `--expand 易理`, `--expand 星象`, `--expand 道家`, `--expand 基督宗教`, `--expand 现实修正`, or `--expand 全部`. Natural-language expansion works through the installed Skill. A weather file must contain `description`, `hazard`, `source`, and `observed_at`; accepted hazard values are `none`, `heavy_rain`, `storm`, `snow`, and `extreme_heat`. Run `python3 -m unittest discover -s tests -v` for verification.

The grade is a **product-defined symbolic score**, not a probability or forecast. The lowest grade is 小凶. Default output is short; detail is optional.

## Scope and responsibility

Wanxiangli is for entertainment, cultural exploration, textual experimentation, and reflection. It is not a religious institution, missionary tool, theological authority, religious counseling service, scientific prediction system, or decision tool for medical, legal, financial, or safety matters. It guarantees no future event. Traditions contain significant internal differences, which these limited notes cannot resolve or represent in full. Read the bilingual [disclaimer](DISCLAIMER.md) and [religious content policy](RELIGIOUS_CONTENT_POLICY.md).

Islamic traditions are intentionally outside the content scope of this project. This is a product-scope decision intended to avoid inaccurate representation or unintended offense, and does not express any judgment regarding Islam, Muslims, or related cultures.

## Sources, license, and contributions

Original code and short notes are [MIT licensed](LICENSE). Two unmodified MIT Python dependencies are bundled with their own license notices. No CBETA database text, copyrighted modern Chinese Bible translation, tarot image, or complete classical/religious text is bundled. [SOURCES.md](SOURCES.md) explains bundled software, adapted notes, research-only sources, and runtime inputs; [`skills/wanxiangli/references/sources.yaml`](skills/wanxiangli/references/sources.yaml) records each source. A publicly accessible page is not automatically reusable content.

**Third-party components and acknowledgements:** `lunar_python` 1.4.8 and `astronomy-engine` 2.1.19 are pinned MIT dependencies bundled as a fallback (matching external installations are preferred). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for their separate copyright notices and provenance. The ancient *Zhouyi* index, A. E. Waite's work, World English Bible, and listed classical works inform original short notes. CBETA is research-only. [`xuanxue-engine`](https://github.com/sxt9805/xuanxue-engine) is an architectural reference; [`fortune-telling-skills`](https://github.com/eamanc-lab/fortune-telling-skills) is a research reference. No code or prose was copied from those two projects. Listing a source does not imply participation or endorsement.

Read [CONTRIBUTING.md](CONTRIBUTING.md), [RELIGIOUS_CONTENT_POLICY.md](RELIGIOUS_CONTENT_POLICY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting new materials. The investigation is in [RESEARCH.md](RESEARCH.md).
