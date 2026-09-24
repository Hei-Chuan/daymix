# 更新日志 / Changelog

按版本记录新增与修正；连贯的当前设计统一维护在 [DESIGN.md](DESIGN.md)，不为每个新版本复制一份整体介绍。

## 2.3.0 · 网站与 Agent capability

- 将 `get_daily_card` 拆成共用核心；增加 stdio MCP，保留 Streamable HTTP 与可选的 MCP Apps UI。文本与结构化结果均含固定 v2.2 日签及来源；增加健康检查、输入/输出上限、子进程超时、受控错误和非本机监听的令牌门禁。
- 增加 [兼容性分级](COMPATIBILITY.md)与双传输测试。**发行包版本是 2.3.0；`cast_version=v2.2`、`data_version`、语料和 v1/v2.1 replay 没有改变。**
- 对四条道教异常建立影印本核查状态，对 40 组配对复核结构和主题；未有可靠底本时保持 unresolved，不改古文。
- 新增极简手机优先网站：当天日卡、只读历史、匿名同步码恢复。网站复用原 Python 引擎，SQLite 只属于状态层；日签完整 JSON 一经保存不随未来版本重算。加入网站发行包与可选容器部署入口。

## 2.2.0 · Daymix

- 当前版本中文概览：正式名称改为「Daymix · 今天呢」，保留 v1/v2.1 历史复算；道教签页扩至 365 条、基督宗教内容扩至 40 组项目自编旧约—新约配对。四象评分、三镜反思、现实只改行动和一次调用的展开卡架构保持不变。具体核验限度见[语料报告](CORPUS_COMPLETENESS.md)。

- Migrated the active Skill, Python package, CLI, MCP App, UI, manifests and release artifacts to Daymix · 今天呢.
- Added a source-linked 365-sign historical snapshot and 40 fixed Old Testament–New Testament thematic pairs. Four sign-page anomalies are explicitly recorded.
- Preserved v1 and v2.1 replay through frozen engines and data; v2.2 declares separate schema, cast, seed and data versions.
- Kept the four-sign score, unscored three lenses, reality-only effective actions and one-call local UI disclosure.

### 2026-09-24 文档与审视补充

- 中文首页补齐现行项目介绍；整体机制统一维护在 `DESIGN.md`，旧版研究只保留版本变化，`README.zh-CN.md` 改为中文首页入口。
- 说明完整结果的复现条件、天气输入的实际核验范围、语料校勘与网页录文的权利边界；缺失天气文件改为明确的 CLI 输入错误，并增加旧版 UI 展示测试。

## 2.0.0 (2026-09-23)

- The initial local v2 candidate permitted a one-stalk right heap; hanging that stalk left an empty heap. The finalized `cast_version` is `v2.1`, with nonempty heaps and unchanged seed domain for other channels. The repository's published v1 engine remains byte-for-byte stable.
- New `wanxiangli/2` ledger: independent four signs, three reflective lenses, explicit symbolic contributions and reality-only effective actions. No star ratings for study, wealth or social life.
- Simulate 49-stalk yarrow splitting through six lines, then derive primary/changed hexagrams and moving-line text. Add an original v2 tarot short-meaning table; preserve v1 card data.
- Add a sourced, **seven-entry** subset of the 365-sign Daoist *Xuanzhen lingying baoqian*. Remaining entries are not yet transcribed. Add seven classical planetary positions and major angular aspects.
- Add body/speech/mind prompts, an independent Bible-reference pool, and a Stoic control audit, without giving those lenses score weight.
- Add a mobile, dark-mode MCP Apps disclosure card and a read-only `get_daily_card` MCP tool. The UI requires a connected and deployed endpoint; the Skill remains usable as text.
- Default CLI now runs v2. Use `--engine v1` to reproduce v1 results; its salt and source remain unchanged. Changes to the schema and default results are intentional breaking changes.

## 0.1.0

Portable v1 Skill with fixed vendor dependencies and a plain-text card.
