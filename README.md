**简体中文** · [English](README.en.md)

# Daymix · 今天呢

> 今天呢？打开一张小卡，看看今天掉落了什么，再选一件现实中能做的事。

Daymix 是一个开源的 Agent capability：一套 Python 引擎和语料、一个标准 Skill、一个跨平台 MCP 工具，也提供命令行和可选的 ChatGPT 展开卡片。它把历法与四种象征来源放在一张卡上：易、塔罗、道教签诗和星象分别给出线索；佛教、基督宗教与斯多葛作为三个不计分的自省视角。最后，周末条件和用户提供的天气预警可以修正行动建议。这里的“运势”是娱乐与文化解释，不是未来预测。

## 先看一张卡

运行 `python scripts/daymix.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo`，会得到以下固定示例：

```text
Daymix · 今天呢｜09-23 · 八月十三
今天抽到 · 中吉　愉悦 · 顺应 · 温故
宜　整理生活 · 整理资料
不太建议　草率定约 · 仓促搬动
四象
〉儒家·易　兑 → 随
〉塔罗　圣杯王牌 · 正位
〉道教　辰時二十二·聞喜不喜 · 中平
〉星象　月亮水瓶 · 相位6项
三镜
〉佛教　今日察「意」
〉基督宗教　Deuteronomy 24:14 ↔ James 5:4
〉斯多葛　可控：行动
〉现实复核　暂无修正
今天先做　今天先整理生活，留意现实条件。
```

`demo` 是公开示例代号。完整 JSON 保留每条线索、评分依据、来源和原始建议；短卡默认只显示要点。

## 它怎么工作

| 层次 | 当前实现 | 作用与边界 |
| --- | --- | --- |
| 日期与历法 | 公历、农历、干支、节气和传统宜忌；以指定时区的日期为准 | 黄历条目保留原词，只将少数条目映射为日常行动；不同历书口径可能不同。 |
| 四象 | 49 策蓍筮程序化模拟与《周易》卦爻辞、78 张塔罗、365 页道教签诗录文、七颗古典天体的地心黄经与相位 | 各给 -1/0/+1 的**编辑性象征分**，合成五档评级；星象位置是计算值，星象解释与评分不是科学预测。 |
| 三镜 | 佛教身口意自省、40 组原创旧约—新约主题配对、斯多葛“可控之事”核对 | 只提供反思角度，不参与评分，也不代表任何宗教机构。 |
| 现实复核 | 周末规则；CLI 可接收用户提供的天气预警 JSON | 只改有效“宜/不太建议”和总结，不重抽卦、牌、签，不改天象与原评分。 |

易的蓍筮是确定性模拟，道教签与塔罗由独立种子抽取，星象按本地正午计算。四项可以有分歧；展开详情会显示各自依据，不强行说成同一种传统。原书的签页编排也不是 Daymix 的每日抽取仪轨。算法与文本来源的细节见[现行设计说明](DESIGN.md)。

## 怎么使用

- **命令行**：`python scripts/daymix.py --format json --identity-mode hosted` 看完整结果；用 `--expand daoism|christianity|all` 看解释和出处。`--help` 列出日期、时区、备考条件等参数。
- **Skill / Codex**：[Skill 源码](skills/daymix/SKILL.md)可用于安装，安装后说“今天呢？”或“查看今日运势”。运行 `python tools/build_release.py` 可生成 `dist/daymix-skill.zip` 和 `dist/daymix-plugin.zip`。
- **通用 MCP**：`node ui/stdio.mjs` 提供本地 stdio；`npm run start --prefix ui` 提供 Streamable HTTP `/mcp`。两者共用 `get_daily_card`、完整结构化结果、文本卡与出处；[平台状态与部署说明](COMPATIBILITY.md)区分实测和待验证。
- **网站**：运行 `python web/app.py`，打开 `http://127.0.0.1:8000/`。点击“看看今天”才生成并保存当天完整日卡；右上角“之前掉了什么”读取历史原始 ledger。无需注册，同步码可在新设备恢复同一匿名历史。网站只调用现有 Python 引擎；SQLite 仅保存匿名设备凭证哈希、同步码安全哈希、日期/时区/版本和完整日卡。`DAYMIX_WEB_DB` 可指定数据库位置，`Dockerfile` 可部署网站容器；持久化数据库需要单独备份，同步码不能替代服务端备份。
- **ChatGPT 展开卡片**：部署并连接 [MCP Apps 服务](ui/README.md) 后，`get_daily_card` 一次返回完整结果；展开、收起、全部展开都在卡片本地完成。Skill 单独安装时使用文本卡。ZIP 不会自动部署服务。

仓库和 CI 使用 Python 3.12、Node.js 24 验证。CLI 默认在本机保存私有安装标识以维持旧版结果；`--identity-mode hosted` 使用共享访客日签，不创建该标识。请勿把姓名、邮箱或电话用作 `--user-id`。

## 可复现与当前限制

当前默认引擎是 **v2.2**，输出标记为 `daymix/2`。`--engine v1`、`--engine v2.1` 保留旧版复算；旧命令 `scripts/wanxiangli.py` 默认 v2.1。原始四象由日期、时区、代号或安装标识、引擎及语料版本确定；**完整结果**还需要相同的备考条件和天气输入。改变语料必须另立版本，不能把新结果冒称旧结果。

CLI **不自动获取或核验天气**。只有传入 `--weather-json` 时才读取其中的 `description`、`hazard`、`source`、`observed_at`；程序不验证地点、来源真实性或观测时间是否过期。MCP 工具目前没有天气参数。没有可靠天气资料时，不作天气安全判断。CLI 和卡片的运行文案目前以中文为主；英文 README 是项目介绍，不是英文运行界面。

道教语料覆盖维基文库目录中的 **365/365** 个签页，4 页有已标注的字段或录文异常，但**尚无签页与影印本逐字校勘**；签诗下方的现代提示是项目原创的通用反思，并非 365 篇独立考据。基督宗教部分是 **40 组**项目原创的旧约—新约主题配对，不是摩拉维亚弟兄会官方每日经文序列。详情与核验口径见[语料完整度](CORPUS_COMPLETENESS.md)。

项目不隶属于宗教机构，不提供宗教指导、确定性预言或医疗、法律、财务、安全建议。现实资料和专业判断优先。完整边界见[免责声明](DISCLAIMER.md)与[宗教内容规范](RELIGIOUS_CONTENT_POLICY.md)。

## 文档与开发

[现行设计与依据](DESIGN.md)连续说明四象、三镜、现实复核；[兼容性](COMPATIBILITY.md)说明 Skill/MCP 宿主现状；[更新日志](CHANGELOG.md)只记录版本增量。[资料与权利](SOURCES.md)及[来源登记表](skills/daymix/references/sources.yaml)记录实际使用方式；[语料完整度](CORPUS_COMPLETENESS.md)记录数量与未核实项；[第三方许可](THIRD_PARTY_NOTICES.md)、[贡献指南](CONTRIBUTING.md)、[发布检查](RELEASING.md)分别覆盖依赖、投稿和发布。[v1](RESEARCH.md)、[v2.1](RESEARCH_V2.md) 与 [v2.2](RESEARCH_V22.md) 研究文件只作历史档案，不必从旧文件拼出现行项目介绍。

验证命令：`python -m unittest discover -s tests -v`、`npm ci --prefix ui && npm run build --prefix ui && npm test --prefix ui`、`python tools/build_release.py`（生成 Skill、插件和网站三个发行 ZIP）。项目原创代码按 [MIT](LICENSE) 许可发布；第三方材料遵循各自的权利声明。
