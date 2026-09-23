# 万象历 v1：资料与技术调查

调查日期：2026-09-23。以下判断限于所列版本、页面与第一版的“原创短卡 + 外部依赖”用法；若日后打包完整文本、图像或将产品商业化，需重新逐项复核。

| 对象 | 能力与发现 | 许可与取舍 |
| --- | --- | --- |
| [6tail/lunar-python](https://github.com/6tail/lunar-python) | 公历转农历、干支、节气、宜忌、彭祖百忌、黄道神煞、纳音；2026-09-23 实际调用验证。 | [MIT](https://github.com/6tail/lunar-python/blob/master/LICENSE)。作为外部 Python 依赖，不提取代码。黄历规则来自其实现，有不同流派或历书口径的可能。 |
| [《周易》索引](https://zh.wikisource.org/wiki/周易) | 提供 8×8 上下卦对应表和 64 卦序；据此校准 64 条卦名、爻序。 | 古籍原文公有领域；网站额外编排另依页面条款。只打包自编卦索引和短主题，不搬全文或注释。 |
| [A. E. Waite《The Pictorial Key to the Tarot》](https://en.wikisource.org/wiki/The_Pictorial_Key_to_the_Tarot) | RWS 78 张牌及基本体系。 | 原作在美国公有领域；各国期限有差异。不打包图像、原书全文或现代网站解释；78 条极短牌义为原创。 |
| [CBETA 版权页](https://cbeta.org/copyright) | 大量中文经典可用作校准，包括不同古代译本。 | 默认 CC BY-NC-SA 4.0 并有非商业、节录再传播和例外文献条件；仅参考，不把数据库文本/现代译注打包。 |
| [《心经》版本页](https://zh.wikisource.org/wiki/般若波羅蜜多心經)、[《金刚经》](https://zh.wikisource.org/wiki/金剛般若波羅蜜經) | 古代汉译文本作“观照／无住”概念核查。 | 古代底本公有领域；注意译本之间差异。只打包本项目原创转述。 |
| [《道德经》](https://zh.wikisource.org/wiki/道德經)、[《清静经》](https://zh.wikisource.org/wiki/太上老君說常清靜經) | 前者校准知止、不争；后者供道教清静视角核对。 | 古籍底本可用；《清静经》页面具体版本未经逐页审计，列 reference_only，不搬原文。 |
| [World English Bible 版权声明](https://ebible.org/eng-web/copr.htm) | 英文公共领域译本，足以核对“道路、光、种子、等待、风暴”的章节目。 | 出版方明确称 Public Domain。只打包原创中文说明与章节索引，避免误用受版权保护的中文译本。 |
| [Astronomy Engine](https://github.com/cosinekitty/astronomy) | 跨平台太阳、月亮位置；实际验证 Python 的 `MoonPhase` 与 `SunPosition`。 | MIT；第一版选为外部依赖，输出太阳黄经与月日黄经差。象征月相是本项目定义，不构成天文因果。 |
| [Skyfield](https://github.com/skyfielders/python-skyfield) | 高精度天体位置，往往需要另取星历文件。 | MIT；第一版无必要增加额外星历下载。 |
| [Swiss Ephemeris](https://github.com/aloistr/swisseph/blob/master/LICENSE)、[Kerykeion](https://github.com/g-battaglia/kerykeion) | 可做复杂占星盘。 | Swiss 为 AGPL/专业双许可，Kerykeion 为 AGPL-3.0；第一版不纳入，避免重型依赖与再分发复杂性。 |
| [xuanxue-engine](https://github.com/sxt9805/xuanxue-engine) | 确定性脚本与解释分离、固定 seed、统一结构的可行参考。 | MIT；只借鉴架构原则，没有复制代码或资料。 |
| [fortune-telling-skills](https://github.com/eamanc-lab/fortune-telling-skills) | 78 牌资料组织与体系化卡片可作参考；项目本身由多个 Skill 组成。 | README 标示 MIT；本项目保持单 Skill，不沿用其分 Skill 路由或复制文本。 |

## 核心设计判定

- `SHA-256(version, local day, stable user identifier, channel)` 分通道选卦、抽牌、定正逆；更改任一体系不会顺次改变其他抽取。安装标识留在本地私有配置。不是传统六爻或蓍草方法。
- `lunar-python` 负责民俗历法信息；`astronomy-engine` 负责可重算的真实天文角度。日间天气变动不改变原始评级。黄历古条目只做少数审慎现代映射，原词完整保留在 JSON。
- 64 个卦名及上下卦与 78 张塔罗均完整覆盖；tone 与简短主题是本项目解释规则，不能伪称古籍或 Waite 的原话。评分采用 `2×卦主题 + 牌语境 + 月相象征`，压到五档，最低“小凶”；是产品体验值，不是预测概率。
- 宗教与哲学资料不参与抽取或打分。知识卡有适用、可转化表达和禁止误读；不把跨传统视角当作宗教教义认可占卜。
- 天气由 Skill 查询明确地点并将来源、时间和灾害等级传给脚本，脚本只覆写有效行动列表。未提供可信天气时不调用网络或伪造实时天气。节假日与个人日历暂不引入。

## 仍需人工决定

1. 如果需要**跨设备**同一天同一张卡，选定一个不会变化且非敏感的个人标识，并在各设备配置相同 `--user-id`。当前默认仅本机稳定。
2. 希望默认使用哪个时区/常驻城市，以及是否允许每次查询当地天气；未明确地点时第一版不查天气。
3. 将来是否在中国或其他地区商业分发完整古籍/塔罗图片；需要按分发地重新审核具体底本与许可。
4. 黄历宜忌的具体流派、节气日界与现代词项是否要采用指定的历书规则；第一版如实标记 `lunar-python` 的数据源，不声称流派通用。

## Phase 6 公开发布审计（2026-09-23）

- 实际运行环境：Python 3.10+；固定依赖为 `lunar_python==1.4.8` 与 `astronomy-engine==2.1.19`。脚本只有命令行和标准 JSON/文本输出；没有 HTTP 客户端、天气 API、节假日表、出生星盘或图形折叠组件。Skill 可在地点明确时另行查询天气，再把带来源与时间的 JSON 交给脚本。
- 对照 `SKILL.md`、两个 README、`--help`、脚本、知识卡与 `sources.yaml` 检查公开能力。`--date`、`--timezone`、`--user-id`、`--context 备考`、`--weather-json`、`--format`、`--expand` 均实际存在；自然语言触发是 Skill 行为，不是独立 CLI 解析器。
- `references/sources.yaml` 的 14 条来源重新分类：外部来源没有全文打包；7 条 `adapted` 仅用于本项目原创索引或短卡，4 条 `reference_only`，3 条 `runtime_lookup`。`SOURCES.md` 与此一致。MIT 只覆盖本项目原创内容，不代替第三方依赖的许可证。
- 检查运行文本、知识卡和公开资料，没有发现针对信徒的概括性贬损、伪称经典原句、长篇现代译文或确定性灾祸断语。公开文件中对不在素材范围的传统仅作中性范围说明；运行参考不纳入相关资料。
- 本机运行 `python3 -m unittest discover -s tests -v`：11 项通过；`quick_validate.py`：Skill 有效；以 `--user-id demo --date 2026-09-23` 复跑两个 README 的示例，结果一致。

## Phase 7 distribution audit (2026-09-23)

The Phase 6 inventory above describes the historical pre-migration release. In version 0.1.0, the canonical root is `skills/wanxiangli/`. Two unmodified pinned MIT dependencies are now bundled with their respective license notices and SHA-256 source-tree digests; a matching installed version is preferred. The source inventory now marks these two packages `bundled`. The other source classifications and the core scoring and seed rules did not change.

Portable plugin discovery uses the root `plugin.json` and `skills/`; `.codex-plugin/plugin.json` is a consistent compatibility manifest. The standalone Skill archive uses a single `wanxiangli/` top-level folder. Hosted Python and Skill upload permissions depend on the destination platform; an ephemeral hosted environment uses a deterministic shared guest daily result without writing an installation identifier, with a user-supplied non-sensitive alias available for personal cross-session stability. Local Codex retains the private installation identifier. The script never downloads dependencies or fabricates missing data.

## v2 update

The v1 scoring and source decisions above are preserved to explain and reproduce old daily cards. The new mechanisms, source links, uncertainties, and implementation decisions are recorded in [RESEARCH_V2.md](RESEARCH_V2.md). In particular, the v1 label “Daoist interpretive lens” has been replaced in v2 with a verified historical sign subset; this does **not** imply that the project's daily deterministic selection is a documented historical ritual.
