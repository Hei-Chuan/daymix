# Daymix · 今天呢

每天看看今天呢。四象给线索，三镜换角度，最后用现实条件决定怎么做。先运行 `python scripts/daymix.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo`，或在已安装的 Skill 中说“今天呢？”。

这是一张娱乐、文化探索和自省小卡，不是未来预测。`demo` 是公开示例代号；不必提交姓名、邮箱或电话。

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

四象各有独立确定性抽取和公开象征分；三镜只作反思。天气与现实条件只调整有效行动，不改变原始签、牌、卦、天象或评分。v2.2 收录 365 条维基文库签页录文，4 页存在已标注的源页异常，仍待影印本复核；40 组旧约与新约经节由项目独立配对，中文为原创转述，不是摩拉维亚弟兄会官方每日序列。

`python scripts/daymix.py --format json` 查看完整数据；`--expand daoism|christianity|all` 查看解释与出处。`--engine v1` 和 `--engine v2.1` 复算历史结果；旧 `scripts/wanxiangli.py` 路径默认 v2.1。部署并连接 [MCP Apps 服务](ui/README.md) 后，ChatGPT 的 `get_daily_card` 一次返回全部内容，展开和收起都在本地组件完成；只有 Skill 时用文本卡。

[语料完整度](CORPUS_COMPLETENESS.md) · [资料和权利](SOURCES.md) · [研究记录](RESEARCH_V22.md) · [免责声明](DISCLAIMER.md) · [宗教内容规范](RELIGIOUS_CONTENT_POLICY.md) · [贡献指南](CONTRIBUTING.md) · [English](README.en.md)
