# 资料来源与分发 / Sources and redistribution

逐项来源登记见 [`skills/daymix/references/sources.yaml`](skills/daymix/references/sources.yaml)，本页按 v2.2 于 2026-09-24 整理。这里的 `bundled` 指**材料实际随包分发**，`adapted` 指项目原创索引或短述参考了资料，`reference_only` 指仅用于研究或核对，`runtime_lookup` 指运行时由调用者提供。分类是使用方式，**不是一张通用转载许可证**；古籍原文、网站电子录文、现代译注和图片的权利应分别核对。

| 来源 | 实际用途 | 分发与限制 |
| --- | --- | --- |
| [lunar-python](https://github.com/6tail/lunar-python)、[Astronomy Engine](https://github.com/cosinekitty/astronomy) | `bundled` | 两个固定版本的 MIT 软件包随 Skill 分发，保留许可证与源码树摘要，见[第三方声明](THIRD_PARTY_NOTICES.md)。前者计算历法，后者计算天体位置；象征解释由项目制定。 |
| [《周易》](https://zh.wikisource.org/wiki/周易)与[卦爻辞记录](skills/daymix/references/eastern/zhouyi-text.json) | `bundled` | 收录 64 卦的古代卦辞、爻辞及项目原创索引/主题。卦爻辞曾以 CText 页面和机器数据核对；[CText API 说明](https://ctext.org/tools/api)提示使用限制，因此其数据使用条件与逐字底本核验仍需复核。不打包现代译注。 |
| [《玄真靈應寶籤》](https://zh.wikisource.org/wiki/玄真靈應寶籤) | `bundled` | v2.2 收录 365 页古签诗、原页 URL 和修订号；另保留七条旧记录供 v2.1 复算。4 页异常已标注；未与《正统道藏》影印本独立逐字校勘。不复制网页长篇解说或现代解签。 |
| [World English Bible](https://ebible.org/engwebp/copyright.htm) | `adapted` | 40 组项目自编旧约—新约配对中有 80 个 WEB 经节链接。出版方声明 WEB 属公版并对译本名称有使用要求；项目的中文短述不冒称 WEB 中文译本，也不打包现代版权中文圣经译文。 |
| [Moravian Daily Watchwords 历史资料](https://www.moravianchurcharchives.org/general/anniversary-of-moravian-daily-texts/) | `reference_only` | 借鉴旧约 Watchword 配新约伴读的总体形式；不复制官方年度序列、灵修文字或品牌，不暗示机构认可。 |
| [Waite《The Pictorial Key to the Tarot》](https://en.wikisource.org/wiki/The_Pictorial_Key_to_the_Tarot) | `adapted` | 参考历史牌义，78 张牌的短义由项目原创。不分发牌图、原书长段落或现代商业释义；原作公版状态因司法辖区而异。 |
| [《道德经》](https://zh.wikisource.org/wiki/道德經)、[《心经》](https://zh.wikisource.org/wiki/般若波羅蜜多心經)、[《金刚经》](https://zh.wikisource.org/wiki/金剛般若波羅蜜經)、[爱比克泰德《手册》](https://en.wikisource.org/wiki/Enchiridion) | `adapted` | 用于核对哲学概念；运行卡片为项目原创短述，不复制整部古籍或现代译本。译本和版本权利另论。 |
| [《清静经》](https://zh.wikisource.org/wiki/太上老君說常清靜經)、[CBETA 权利说明](https://cbeta.org/copyright)、[xuanxue-engine](https://github.com/sxt9805/xuanxue-engine)、[fortune-telling-skills](https://github.com/eamanc-lab/fortune-telling-skills) | `reference_only` | 仅供文本、权利或架构研究；不复制受限语料、代码或现代注释。 |
| 调用者提供的天气 | `runtime_lookup` | CLI 要求 `description`、`hazard`、`source`、`observed_at`，但不核验其真实性、地点或时效；不内置天气服务，MCP 工具也不接收天气。支持的预警类别只改有效行动建议。 |

登记表还分别列出 `xici`、`zhu_xi`、`dao_index`、`zhancha`、`ptolemy`、`babylonian_zodiac` 等来源。引用仅说明资料关系，不代表任何作者、译者、出版者或宗教机构认可 Daymix。对语料数量与异常见[完整度报告](CORPUS_COMPLETENESS.md)，对解释边界见[现行设计](DESIGN.md)和[免责声明](DISCLAIMER.md)。

**古籍与网页录文的权利不能合并判断。** 中文维基文库的[版权方针](https://zh.wikisource.org/wiki/Wikisource:版权信息)说明站点贡献按 CC BY-SA 4.0 等条件发布，而公有领域的古代底本本身不因网页展示失去公版地位。项目为签诗保留逐页 URL 与修订号，并从网页录文提取诗句和字段；可能具有独创性的网页编辑、编排贡献是否进入了随包数据，仍需逐页辨别。若使用了受 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.zh-hans) 保护的贡献，其署名、修改标记与相同方式共享要求须另行遵守；项目的 MIT 许可不能代替它。此项权利复核与影印本校勘是两项不同的未完成工作。

**English overview:** The registry distinguishes materials redistributed in the package (`bundled`), project-authored adaptations (`adapted`), research pointers (`reference_only`), and caller-supplied runtime data (`runtime_lookup`). These labels do not grant blanket reuse rights. Ancient works, electronic transcriptions, translations, images, and software retain distinct rights; see the linked source record and [third-party notices](THIRD_PARTY_NOTICES.md).
