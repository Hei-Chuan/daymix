# Daymix v2.2 语料完整度与已知问题

核对快照：2026-09-24。运行语料已提交到仓库，日常抽取**离线进行**；`tools/import_daoism.py` 只供显式维护，不会在生成日卡时访问网络。具体来源和分发方式见 [SOURCES.md](SOURCES.md)。

## 《玄真靈應寶籤》：目录 365/365，影印本校勘 0/365

- [维基文库目录](https://zh.wikisource.org/wiki/玄真靈應寶籤)有 365 个不同的签页链接：十二时各三十签，另有五行五签。维护脚本抓取了全部页面；`verified-signs-v2.2.json` 收录 **365 条非空签诗**，并保留原页标签、标题、原有品第、签页 URL 和 MediaWiki 修订号。
- 数据中的 `number=1..365` 是**项目按目录建立的顺序号**，不应说成原书每签都印有的连续编号；原始标签如 `子時第一` 另存。日卡用独立确定性通道从 365 条中抽取，十二时与五行仅是原书编排，**不是本项目抽签仪轨的历史依据**。
- **4 页需要继续校勘：** 第 57 条（`丑時二十七`）品第为异例 `有得`；第 269 条（`申時二十九`）未见品第；第 297 条（`酉時二十七`）诗和解说无分段，脚本以首四个标点分句作诗；第 327 条（`戌時二十七`）品第为异例 `一下`。这些情形记录在 `uncertainty`；异例或缺失品第使用中性象征分，没有编造品第。
- **缺少目录条目：0。与《正统道藏》影印本逐字独立核对：0/365。** 项目记录的是网页自述底本与页面修订号，不能据此宣称完成版本校勘。网页长篇解说没有打包；`daymix.short_reading` 是简短的**通用原创反思**，不是 365 篇逐签考据。
- 古籍诗文的公版状态与维基文库网页贡献的许可范围不同；页面录文是否包含需额外遵守 CC BY-SA 的编辑贡献，尚待逐页权利复核，见[资料与权利](SOURCES.md)。

### 四条异常的影印本核查状态（2026-09-24）

已定位可能相关的[国家图书馆藏《道藏》影印 PDF](https://commons.wikimedia.org/wiki/File:NLC892-411999005947-9582_%E9%81%93%E8%97%8F_%E7%AC%AC4372%E5%86%8A.pdf)及[道教文化中心版本索引](https://zh.daoinfo.org/wiki/玄真靈應寶籤)，但本次未能把四条准确定位到可读的影印页并逐字核验。另一份[中国哲学书电子化计划录文](https://ctext.org/wiki.pl?if=gb&res=573285)只能作为电子异本线索，不能代替影印本。**影印本已校勘：仍为 0/365；以下四条均为 unresolved，运行语料未改。**

| 项目序号 | 待核问题 | 下一步核对影印页的目标 |
| --- | --- | --- |
| 57 | `有得` 是品第还是题名字段错位？另一电子录文的索引呈现 `平平／有得`，提示字段分界需复核。 | 看原页标题与品第的版式，核对 `平平`、`有得` 的位置。 |
| 269 | 来源网页未见品第。 | 看原页是否确实缺项，不按邻签猜补。 |
| 297 | 网页诗与解说未分段，当前诗句切分为程序推断。 | 看原页诗文行界和解说起点。 |
| 327 | `一下` 为品第异例。 | 看原页原字与版式，不自动改成常见品第。 |

## 基督宗教：40 组项目配对

- `watchwords-v2.2.json` 有 **40 组固定旧约—新约主题配对**。所指向的 **80 个 [WEB 公版版本](https://ebible.org/engwebp/)章节目链接与节号**已逐一检查存在；这只证明引用位置存在，不能代替对中文转述和主题关联的独立神学审核。
- 程序从已配好的记录中确定性选择**一组**，并非分别随机抽旧约、新约后拼接。[Moravian Archives](https://www.moravianchurcharchives.org/general/anniversary-of-moravian-daily-texts/)所述旧约 Watchword 与新约伴读提供方法启发；Daymix 没有采用教会官方年度序列或复制其灵修文字，也不声称教会认可。
- 中文转述、主题连接和反思均为项目编辑内容，没有打包现代版权中文圣经译文。v2.1 的 **12 条旧约池**保留，只用于历史复算。

### 40 组配对 QA（2026-09-24）

本次用 eBible 发布的 [WEB 逐节纯文本包](https://ebible.org/Scriptures/engwebp_vpl.zip) 对照 40 组共 80 个引用位置：**80/80 节可定位**；并逐组阅读原文、中文转述、主题和反思。引用存在不等于转述准确。初审发现以下待处理项：

- **经节与转述明显不合：** `pair-036` 引 [Galatians 5:22](https://ebible.org/engwebp/GAL05.htm#V22)，但中文所说的“温柔与节制”在 **5:23**；`pair-029` 把 [Matthew 5:6](https://ebible.org/engwebp/MAT05.htm#V6) 的“得饱足”写成“被看见”；`pair-012` 把 [Psalm 37:3](https://ebible.org/engwebp/PSA037.htm#V3) 的“安居其地、享用安稳牧场”写成“照看所居之地”，增添了原节没有的照料动作。这三处应在新的语料版本中优先修订。
- **省略或改写原文信仰语境：** `pair-008` 把 [James 4:15](https://ebible.org/engwebp/JAS04.htm#V15) 的“若主愿意”改述为“未可控条件”；`pair-010`、`pair-013`、`pair-031`、`pair-039` 的转述分别弱化或略去原节中的上帝、上帝同在、赐新心、赐智慧等主语或对象。作为开放给不同读者的反思可以另写，但经节转述应忠于原文，并把应用与原文分开。
- **主题属于项目联想：** `pair-026` 把 [Genesis 2:15](https://ebible.org/engwebp/GEN02.htm#V15) 的园中耕种与看守和 [Romans 8:22](https://ebible.org/engwebp/ROM08.htm#V22) 的受造界叹息联成“照料创造”；这不是经文之间的直接互引，应继续标作项目主题编选。

上述是文本与主题初审，**不是独立神学专家审稿**。v2.2 语料和既有日签保持不变；修订必须另立 data/cast 版本并加入旧版复算测试，不能原地改写冻结的 `watchwords-v2.2.json`。

## 版本边界

v1、v2.1 有冻结的历史复算路径。v2.2 的每份 JSON 都记录 `schema`、`cast_version`、`seed_version`、`data_version`；新语料不能冒称 v2.1。未来改动来源快照，需要新的数据或抽取版本及复算样例。

**English summary:** The v2.2 Daoist snapshot covers 365 of 365 Wikisource index pages, with four recorded field or transcription anomalies and **zero pages independently collated against a print scan**. The Christian pool contains 40 original OT–NT thematic pairs with 80 checked WEB verse links; it is not an official Moravian sequence. Historical v1 and v2.1 data stay frozen.
