# Daymix：现行设计、依据与限度

当前实现：v2.2；最近核对：2026-09-24。本文件是**持续更新的现行设计说明**，不按版本另建一份总览。四象与三镜输出的 `source_ids` 可在[来源登记表](skills/daymix/references/sources.yaml)中查到；[语料完整度](CORPUS_COMPLETENESS.md)记录数量和异常。版本增量记在[更新日志](CHANGELOG.md)；[v1 调查](RESEARCH.md)、[v2.1 研究](RESEARCH_V2.md)与[v2.2 迁移记录](RESEARCH_V22.md)保留为历史档案。

Daymix 把**资料事实、程序规则、编辑性解释**分开：历法和天体位置由固定版本的软件计算；签诗、卦爻辞等保留出处；每日抽取、短评和 -1/0/+1 象征分是本项目规则。来源链接不意味着作者、网站或宗教机构认可本项目。

## 输入、版本与可复现性

- 日卡输入包括日期、时区、非敏感代号或本机安装标识。v2.2 的易、塔罗和道教签使用彼此独立的抽取通道，因此扩充一个语料池不会顺次推进其他通道。星象是按所选日期的本地正午计算，并非随机抽取。
- 输出记录 `schema=daymix/2`、`cast_version=v2.2`、`seed_version` 和 `data_version`。v1 与 v2.1 引擎及旧语料冻结；旧 `wanxiangli/2` 仅在历史复算与 UI 兼容路径中出现。改动语料须另立版本和复算样例。
- 完整 JSON 的复现还取决于相同的备考条件和天气输入；这两项只能改变建议或总结，不能改变原始四象和象征评级。托管访客模式共享一张日卡，本地模式保留旧版兼容的私有安装标识。

## 四象：来源与当前做法

| 模块 | 资料与实现 | 不应误解为 |
| --- | --- | --- |
| 儒家·易 | 参考[《系辞上》大衍章](https://ctext.org/book-of-changes/xi-ci-shang/zh)及[朱熹《周易本义·筮仪》](https://ctext.org/wiki.pl?chapter=862643&if=gb)：49 策程序化分堆，每爻三变，六爻形成本卦、动爻与之卦；卦爻辞来自古代文本录文。v2.1 已修正右堆挂一后可能为空的边界，v2.2 复用该机制。 | 复原西周原法、真人手筮，或把《周易》《易传》和后世儒家解释混成同一写作层。文字异体与版本异文尚未逐条校勘。 |
| 塔罗 | 78 张牌、独立正逆位通道和项目原创短义；[Waite 1910 年说明书](https://en.wikisource.org/wiki/The_Pictorial_Key_to_the_Tarot)用于历史参考。 | 将短义说成 Waite 原话，或将逆位机械变成相反吉凶；不分发牌图、原书长文或现代商业解读。 |
| 道教签诗 | 按[《玄真靈應寶籤》维基文库目录](https://zh.wikisource.org/wiki/玄真靈應寶籤)收录 365 个签页，保留原页标签、诗、品第、URL 与修订号；每日从固定快照确定性选一页。 | 原书规定了 Daymix 的每日抽签法。十二时和五行是书的编排；项目的 1—365 是目录顺序编号。4 页有异常，365 页均未与影印本逐字校勘。现代提示为通用原创反思，不是 365 篇独立解签。 |
| 星象 | Astronomy Engine 计算本地正午的地心太阳、月亮、水金火木土黄经；按热带黄道每宫 30° 标宫，列出合相及四种主要几何相位。±6° 是本项目显示阈值，评分仅概括日月参与的相位。 | 个人出生星盘、古代统一容许度，或天体位置决定个人行为。位置是计算值，象征释义是文化解释。 |

四项各映射为 -1/0/+1，合成五档**象征评级**；评分依据与分歧保留在 JSON 和展开卡中。它不是统计概率或现实结果的预测。[v2.1 记录](RESEARCH_V2.md)保留更细的算法缘起，但其中“道教仅 7 条”“基督宗教仅 12 条”只描述旧版。

## 三镜：反思而非评分

- **佛教：** 从[《占察善恶业报经》卷上](https://zh.wikisource.org/wiki/占察善惡業報經/卷01)的身、口、意分类提取一个日常自省问题；不复刻木轮仪轨，不判断业报、疾病或生死。该文本的归属与接受史存在争议。
- **基督宗教：** [Moravian Archives](https://www.moravianchurcharchives.org/general/anniversary-of-moravian-daily-texts/)及[教会介绍](https://www.moravian.org.uk/daily-watchwords/what-are-the-daily-watchwords)说明旧约 Watchword 配新约经文的历史做法。Daymix 自编 40 组固定主题配对，确定性选择**一组**，没有独立随机拼接两节，也不复制官方年度序列。80 个章节目链接按 [WEB 公版版本](https://ebible.org/engwebp/copyright.htm)核对；中文短述是项目原创，不代表任何教会或译本。
- **斯多葛：** 参考[爱比克泰德《手册》](https://en.wikisource.org/wiki/Enchiridion)中“可控之事”的区分，提示把注意力放回判断和行动；不抽签、不加分，也不把外在结果归咎于用户。

三镜之间、三镜与四象之间不必得出一致结论。项目不声称这些传统在教义上互相认可，也不以任何一种视角给用户发布权威命令。

## 现实复核与交互

当前现实层只处理周末规则和**用户提供的天气预警**。CLI 的 `--weather-json` 要求 `description`、`hazard`、`source`、`observed_at` 字段，并限制危险类别；它不自动联网，不核验来源真实性、地点或时效。MCP 工具目前没有天气参数。现实层只改有效行动建议与总结；原始建议、四象、三镜和象征评分保留。

MCP Apps 组件的 `get_daily_card` 一次返回完整 `structuredContent`，卡片在本地展开、收起和查看出处，不因点击而重抽。缺少可连接的 HTTPS MCP 服务时，Skill 和 CLI 仍可返回文字卡；ZIP 本身不会部署服务。UI 同时接受旧 `wanxiangli/2` 数据供历史显示。实际接入条件见 [UI 说明](ui/README.md)。

## 资料与权利边界

签诗和卦爻辞属于古代底本层；网页录文、现代译注与图片可能有另外的权利。维基文库网页贡献的 CC BY-SA 范围和 CText 数据使用条件仍待逐项复核，不能用项目 MIT 许可概括随包语料。项目不打包现代中文圣经译文、道教网站长篇解签或塔罗牌图。[SOURCES.md](SOURCES.md)区分随包分发、原创改写、仅作研究链接和运行时输入；[第三方声明](THIRD_PARTY_NOTICES.md)列明软件依赖。尚未核实之处应保留不确定性，不应把“已抓取 365 页”写成“已完成影印本校勘”。

**English overview:** Daymix v2.2 separates sourced text and astronomical calculations from its deterministic daily selection and editorial interpretation. Four signs are scored; three reflective lenses are not. Reality inputs affect actions only. The 365 Daoist pages have not been independently collated against scans, and the 40 Christian pairs are project-authored rather than an official Moravian sequence. See the [English README](README.en.md) for use and version boundaries.
