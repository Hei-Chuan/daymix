---
name: wanxiangli
description: 生成《万象历》每日个人黄历；用户说“查看今日运势”“今日运势”“展开佛家”“展开道家”“查看塔罗”“查看易理”“查看星象”“查看现实修正”或“查看今日推演详情”时使用。以历法、确定性卦牌和天文计算为原始象，以概念卡作解释视角，输出简短卡片与按需详情。
---

# 万象历

保持一个 Skill 运行，不创建宗教角色或多 Agent。原始计算必须来自 `scripts/wanxiangli.py`，不可先写结论再补牌。提醒读者这些分数与象征是仪式性的行动提示，不是可验证的未来事件预测；自然融入需要时的解释，避免每天重复长免责声明。

## 每日触发

1. 根据用户已明确的时区决定当地“今日”；未知时先使用 `Asia/Shanghai` 并在需要时允许用户指定。本地 Codex 默认使用私有安装标识。无持久文件保证的托管环境传 `--identity-mode hosted`：无用户标识时采用同一天共享的访客结果，不写配置；用户自愿提供固定且非敏感的代号（如 `blue-fish`）时传 `--user-id`。不要使用或收集邮箱、电话、真实姓名等标识，不展示任何标识、salt、hash 或路径。不同托管会话若采用不同标识，结果可能不同。
2. 在本 Skill 根目录执行 `python3 scripts/wanxiangli.py --timezone Asia/Shanghai --format json`，托管环境加 `--identity-mode hosted`。脚本优先使用环境中版本匹配的 `lunar-python` 1.4.8 与 `astronomy-engine` 2.1.19，缺少时使用本 Skill 的合法内置版本；若两者都不可用，明确报错。没有 Python 执行能力时说明不能完成确定性推演，不猜测农历、节气、星位或黄历数据；不要临时从网络安装软件。
3. 保留当日完整 JSON 作为唯一原始记录。字段：`date`、`overall`、`dos`、`donts`、`areas`、`symbol`、`systems`、`reality_correction`、`synthesis`、`summary`。`dos/donts` 是核心原判，`effective_dos/donts` 才是行动建议；总评级恒取 `overall.rating`。
4. 若用户提供明确城市或对话中已有可靠当前所在地，可查询实时天气或当地可靠天气预报，标记来源与观测时间，写成临时 JSON：`{"description":"午后强降雨","hazard":"heavy_rain","source":"...","observed_at":"2026-09-23T09:00:00+08:00"}`，然后传入 `--weather-json`。没有地理信息或可信天气就跳过，不猜城市；有出行、安全相关建议时优先查询。节假日第一版尚无可靠来源，不能伪称查询过。
5. 个性化如备考只可传 `--context 备考` 并改写建议措辞。严禁改卦、牌、星象、评级或核心宜忌。
6. 默认将同参数的 `--format card` 输出作为卡片骨架，最多润色一句“诸说合参”；依 `references/wanxiangli/rules.md` 控制长度和安全边界。实际出行禁忌应优先遵循真实预警与事实。

## 按需读取

需要卦爻或黄历口径时读 `references/eastern/interpretation.md`、`references/eastern/hexagrams.json`；塔罗详情读 `references/tarot/interpretation.md`、`references/tarot/tarot-78.json`；星象读 `references/astrology/symbols.md`。展开佛家读 `references/buddhism/concepts.md`，展开道家读 `references/taoism/concepts.md`，展开基督宗教象征读 `references/christianity/symbols.md`；斯多葛视角仅在用户要求时读 `references/stoicism/concepts.md`。查出处读 `references/sources.yaml`，实际联网查询新来源前先检查能否使用与打包。

详情优先复用本会话已有的完整 JSON；否则只取同一日期、时区及稳定标识重新计算，即使隔日回看也传原日期。不同栏目按各自侧重点写：易理显示卦名、上下卦及主题；塔罗显示牌名、正逆位及固定短语；佛家谈心态；道家谈行止；基督宗教谈象征和处境；现实复核列原判与更改及数据来源。不要套统一段落模板，不让宗教人物直接讲话。可以诚实呈现体系冲突。

## 表达边界

默认约一屏，最后始终是很短的“今日总结”。使用“经复核”“保留意见”等官僚语汇要节制。禁止恐吓、付费改运、疾病死亡预言、决定性考试或投资保证。遵守 `references/wanxiangli/rules.md` 第 8 条的素材范围及 `RELIGIOUS_CONTENT_POLICY.md` 的尊重规则；搜索结果无关时跳过。
