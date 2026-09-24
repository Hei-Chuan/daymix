# Daymix · 今天呢

**今天呢？** 每天打开一张小卡，看看四种象征刚好怎么组合，再选一个现实中能做的小动作。Daymix 是一个可复现的单 Agent Skill，也可在命令行和 MCP Apps 组件中运行。

它从历法与象征输入出发，让易、塔罗、道教签诗、星象各自给出线索；佛教、基督宗教与斯多葛提供三个不计分的反思视角。天气和现实条件最后修正行动建议。这里的“运势”是娱乐和文化探索，不预测未来，也不代替现实或专业判断。

```bash
python scripts/daymix.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo
```

上述固定示例在 v2.2 的短卡开头是：

```text
Daymix · 今天呢｜09-23 · 八月十三
今天抽到 · 中吉　愉悦 · 顺应 · 温故
宜　整理生活 · 整理资料
不太建议　草率定约 · 仓促搬动
```

`demo` 只用于公开示例。平时不提供 ID 可用 `--identity-mode hosted`；同一日期、时区、代号和版本会得到同一结果。

## 怎么用

- **Skill / Codex**：安装 [Daymix Skill 包](skills/daymix/SKILL.md)，说“今天呢？”或“查看今日运势”。
- **CLI**：运行 `python scripts/daymix.py --format json` 查看完整结果；`--expand daoism|christianity|all` 展开来源与解释。
- **ChatGPT 展开卡片**：部署并连接 [MCP Apps 服务](ui/README.md) 后，一次 `get_daily_card` 返回全部结果；点击展开、收起、全部展开均在组件本地完成。单独安装 Skill 时显示文本卡。
- **历史复算**：`--engine v1` 或 `--engine v2.1`；旧路径 `scripts/wanxiangli.py` 默认 v2.1。v2.2 是新语料版本，绝不冒称重放旧结果。

四象各取 -1/0/+1，透明合成象征评级；三镜不参与评分。天气等可靠现实信息只改有效“宜/不太建议”，不重抽原始结果。最新道教 corpus 按维基文库 365 个签页建档，4 页有字段异常，尚未与影印本逐字校勘；基督宗教是 40 组原创主题配对的旧约与新约经节，不是摩拉维亚弟兄会官方每日序列。

[语料完整度与已知问题](CORPUS_COMPLETENESS.md) · [来源与版权](SOURCES.md) · [研究边界](RESEARCH_V22.md) · [免责声明](DISCLAIMER.md) · [宗教内容规范](RELIGIOUS_CONTENT_POLICY.md) · [第三方许可](THIRD_PARTY_NOTICES.md) · [贡献指南](CONTRIBUTING.md) · [English](README.en.md)

构建与测试：`python -m unittest discover -s tests -v`、`npm ci --prefix ui && npm run build --prefix ui && npm test --prefix ui`、`python tools/build_release.py`。本项目按 [MIT](LICENSE) 许可发布；第三方材料各依其原许可。
