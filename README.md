# Wanxiangli · 万象历 v2

[简体中文](README.zh-CN.md) | **English**

A reproducible daily calendar experiment: real calendar and astronomical data, historical divination texts, a daily scripture tradition, reflective prompts, and a reality check. The ratings are editorial symbols, not forecasts.

**Four signs:** a deterministic simulation of the later yarrow procedure described in the *Xici* and Zhu Xi's *Yijing* writings, Rider–Waite–Smith tarot, a **verified seven-sign subset** of the 365-sign Daoist *Xuanzhen lingying baoqian*, and geocentric positions of seven classical heavenly bodies. **Three lenses:** Buddhist body/speech/mind self-observation, an independent Moravian-inspired daily Bible reference pool, and a Stoic control audit. Only the four signs contribute to a transparent five-level symbolic rating. Weather and weekday can change effective actions, never the original signs or rating. See [research and limits](RESEARCH_V2.md).

## Run

```bash
python3 scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo
python3 scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo --format json
python3 scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo --expand yijing
python3 scripts/wanxiangli.py --engine v1 --date 2026-09-23 --timezone Asia/Shanghai --user-id demo
```

The default engine is v2. The immutable v1 engine, seed salt, and old results are preserved behind `--engine v1`. Local runs use a private installation ID unless you supply a stable, non-sensitive alias; hosted ephemeral runs use `--identity-mode hosted`. Do not use real names or contact details as IDs. Bundled pinned Python dependencies keep the Skill functional without a runtime package installation.

## Clickable ChatGPT card

The separate `ui/` MCP Apps component accepts the entire `wanxiangli/2` JSON on one `get_daily_card` call. Native disclosure controls expand each section and its sources without another tool call or LLM request; all-open/all-closed, mobile layout, dark mode, and optional widget state are supported. Without a UI host, the tool and the Skill have a text fallback.

```bash
npm ci --prefix ui
npm run build --prefix ui
npm run start --prefix ui
```

The local endpoint is `http://127.0.0.1:3000/mcp`. To use the component **inside ChatGPT**, it still needs deployment to a stable public HTTPS MCP endpoint and connection in a supported developer environment. A GitHub repository or uploaded Skill alone cannot install a clickable ChatGPT widget. This repository does not include hosting credentials or an active ChatGPT connection. See [the UI instructions](ui/README.md) and [current OpenAI documentation](https://developers.openai.com/plugins/build/chatgpt-ui).

## Trust and distribution

`python3 -m unittest discover -s tests -v` validates deterministic results, legacy reproduction and package structure; `python3 tools/build_release.py` makes release candidates. [Source inventory](SOURCES.md), [research record](RESEARCH_V2.md), [religious-content policy](RELIGIOUS_CONTENT_POLICY.md), and [third-party notices](THIRD_PARTY_NOTICES.md) describe provenance and rights. The seven Daoist verses are a curated subset: no claim is made that the remaining 358 signs are available. The Buddhist focus does not reproduce a full ritual; the Bible selection is neither an official Losungen sequence nor a private revelation. Neither symbols nor religion override real medical, legal, financial, or safety information.
