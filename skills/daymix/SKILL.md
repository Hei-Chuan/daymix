---
name: daymix
description: Daymix · 今天呢每日历卡。用户说“今天呢”“查看今日运势”“今日运势”“查看塔罗”“查看易理”“查看星象”“展开佛教”“展开道教”“全部展开”时使用。四象是可复现的象征阅读，三镜用于自省，现实条件优先。
---

# Daymix · 今天呢

先运行 `scripts/daymix.py --timezone Asia/Shanghai --identity-mode hosted --format json`，用结果生成历卡。已知用户时区时传实际时区；不确定时说明采用 `Asia/Shanghai`。只有用户主动提供**非敏感固定代号**，才传 `--user-id`；不要收集姓名、邮件或电话作为代号。不要先编结论再运行算法。

默认 `--engine v2.2`，完整结果为 `daymix/2`。如需历史复算，明确传 `--engine v1` 或 `--engine v2.1`；旧 `scripts/wanxiangli.py` 路径默认 v2.1。复现完整结果还须保持语料版本、备考条件和天气输入一致；后两项只影响建议，不改原始四象。版本转换可能改变当天内容，要向用户说明。

如果 ChatGPT **已经连接**本项目的 MCP 服务，调用一次 `get_daily_card` 获取完整 `structuredContent`，让 UI 从这一个结果本地展开、收起、全部展开和全部收起。只有 Skill 时使用脚本文本卡。用户说“展开现实复核”等栏目时，优先复用当前 JSON，用 `daymix.engine.detail`；如果当前 JSON 不在会话里，以同一日期、时区、代号、版本及原有备考/天气输入运行 `--expand yijing|tarot|daoism|astrology|buddhism|christianity|stoicism|reality|all`。不可暗中重抽。

四象（易、塔罗、道教、星象）各给 -1/0/+1 编辑性象征分；三镜（佛教、基督宗教、斯多葛）不计分。已输入的天气预警和周末条件只调整有效行动建议，不改四象、三镜和原评分。CLI 不自动获取或核验天气；MCP 工具不接受天气输入。没有可靠地点或天气数据就不猜。道教 v2.2 收录维基文库目录的 365 条签诗，4 页有录文异常提示，未逐字校勘影印本；原典编排不是 Daymix 抽签仪轨。基督宗教 v2.2 为自编 40 组旧约与新约主题配对，并非摩拉维亚弟兄会官方序列；中文为原创转述。具体来源与权利见 `references/sources.yaml` 和 `RELIGIOUS_CONTENT_POLICY.md`。

这是一种娱乐、文化探索和自我反思体验，不预测事实、疾病、财务或考试结果，不宣称宗教权威或私人启示。现实与专业判断优先。
