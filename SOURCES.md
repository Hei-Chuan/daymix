# Sources and redistribution / 资料来源与分发

This document describes the **current release**, not permission for every possible reuse. The authoritative item-level metadata (title, author, year, URL, license, copyright status, retrieval date, use, and notes) is [`references/sources.yaml`](references/sources.yaml), reviewed on 2026-09-23. For uncertain rights, the repository links to a source without distributing its text. Public accessibility does not equal a redistribution license.

此表记录当前版本的实际使用方式。逐条元数据见 [`references/sources.yaml`](references/sources.yaml)；版权不明时只保留研究链接，不打包原文。

## What the labels mean / 分类

- **bundled:** third-party expressive material actually included. **None in this release.** Our original scripts, summaries, and short cards are included under the project's [MIT license](LICENSE).
- **adapted:** facts, names, or broad ideas from a source informed **new project-authored** indexes and short explanations; the source's complete text, translation, or images are not copied.
- **reference_only:** consulted for research or verification, with no source text bundled.
- **runtime_lookup:** separately installed dependency or ephemeral external input; the repository does not vendor it.

## Inventory / 来源表

| ID and source | Use | Material in this repository and rights boundary |
| --- | --- | --- |
| `lunar_python` · [6tail/lunar-python](https://github.com/6tail/lunar-python) | runtime_lookup | Version 1.4.8 is a separately installed **MIT** dependency. The source library is not copied. It supplies the calendar and traditional almanac output at runtime. |
| `astronomy_engine` · [Astronomy Engine](https://github.com/cosinekitty/astronomy) | runtime_lookup | Version 2.1.19 is a separately installed **MIT** dependency. No library source is copied; our lunar-phase symbolic scoring is our own rule. |
| `zhouyi` · [《周易》索引](https://zh.wikisource.org/wiki/周易) | adapted | Ancient underlying work is public domain. `hexagrams.json` records 64 names, upper/lower trigrams, and project-authored short themes/scores. No scripture, commentary, or modern translation is reproduced. Website-specific contributions remain subject to their own terms. |
| `daodejing` · [《道德经》](https://zh.wikisource.org/wiki/道德經) | adapted | Ancient underlying work is public domain; `taoism/concepts.md` gives original short explanations rather than source text or modern commentary. |
| `qingjing` · [《清静经》](https://zh.wikisource.org/wiki/太上老君說常清靜經) | reference_only | Exact online edition and its terms need further review. Used as a bibliographic pointer for a short original “清静” concept; no page text is copied. |
| `heart_sutra` · [《心经》版本索引](https://zh.wikisource.org/wiki/般若波羅蜜多心經) | adapted | Ancient Chinese translation attributed to Xuanzang. The short “观照” explanation is original; the index contains multiple translation versions, which should not be conflated. |
| `diamond_sutra` · [《金刚经》](https://zh.wikisource.org/wiki/金剛般若波羅蜜經) | adapted | Ancient Chinese translation attributed to Kumārajīva; original “无住” note only, no extended quotation. |
| `cbeta` · [CBETA copyright statement](https://cbeta.org/copyright) | reference_only | CBETA's collection has non-commercial, redistribution, and work-specific conditions, including exceptions to its general CC BY-NC-SA 4.0 terms. **No CBETA corpus or edited text is bundled.** |
| `waite` · [*The Pictorial Key to the Tarot*](https://en.wikisource.org/wiki/The_Pictorial_Key_to_the_Tarot) | adapted | The work is public domain in the US; other jurisdictions may differ. `tarot-78.json` contains project-authored brief descriptions for 78 cards. No original plates, extended Waite prose, or modern commercial meanings are copied. |
| `web` · [World English Bible Classic](https://ebible.org/eng-web/copr.htm) | adapted | Publisher declares its English translation public domain. Our `christianity/symbols.md` contains passage references and original Chinese explanations; no modern Chinese Bible translation is redistributed. |
| `epictetus` · [*Enchiridion*](https://en.wikisource.org/wiki/Enchiridion) | adapted | Ancient underlying work is public domain; translator or edition rights may differ. Only an original short note on controllable action is included. |
| `xuanxue_engine` · [xuanxue-engine](https://github.com/sxt9805/xuanxue-engine) | reference_only | **MIT**, architectural reference for separating deterministic calculations and prose; no code or dataset copied. |
| `fortune_skills` · [fortune-telling-skills](https://github.com/eamanc-lab/fortune-telling-skills) | reference_only | **MIT** per its README, research reference for material organization; no code or prose copied, and its multi-Skill design was not adopted. |
| `weather` · caller-supplied or local weather source | runtime_lookup | Runtime JSON must identify source and observation time. Conditions may update effective actions, not the original draw. No weather feed, forecast text, or API is bundled. |

Names and links are attribution and audit aids. They do not mean the authors, publishers, translators, or institutions are affiliated with or endorse Wanxiangli. Before distributing third-party text, images, modified code, or a complete corpus in another edition or jurisdiction, review that material's license separately.
