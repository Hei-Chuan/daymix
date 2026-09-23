---
name: wanxiangli
description: 生成《万象历》每日个人历卡；“查看今日运势”“今日运势”“查看塔罗”“查看易理”“查看星象”“展开佛教”“全部展开”触发。用历史筮法模拟、道教签书、塔罗及真实天文作四象，以佛教、每日经文与斯多葛作三镜，尊重现实信息。
---

# 万象历 v2

使用 `scripts/wanxiangli.py` 生成结果，优先 `--format json`，由 `wanxiangli/2` 完整 JSON 提供所有栏目。不要先编结论再推卦。默认用已明确的用户时区；未知时用 `Asia/Shanghai` 并在卡片注明。托管无持久存储时传 `--identity-mode hosted`；只有用户主动给出非敏感固定代号，才使用 `--user-id`。不使用姓名、邮件、电话作为代号，也不展示 ID。日期改变或换时区时明确标识。

若所在 ChatGPT 环境**已连接本项目 MCP 服务**，调用 `get_daily_card` 显示可点击组件；点击由组件从一次生成的 JSON 本地展开，无须再运行脚本。单独安装此 Skill 不会得到组件，使用 CLI 文本卡回退：`python3 scripts/wanxiangli.py --timezone Asia/Shanghai --identity-mode hosted --format card`。用户要求“展开儒家·易”“展开道教”“展开佛教”“展开基督宗教”“展开星象”“展开塔罗”“展开斯多葛”“展开现实复核”或“全部展开”时，优先复用本轮 JSON，再调用 `wanxiangli.engine.detail`；若 JSON 已不在会话中，用原日期、时区和同一稳定代号运行 `--expand yijing|daoism|buddhism|christianity|astrology|tarot|stoicism|reality|all`，绝不暗换当日结果。

四象只作透明象征评级；三镜只供自省，不进入评分。原始 `dos/donts` 与 `four_signs/rating` 不随天气或备考 context 改变；现实 `effective_dos/donts` 才是行动建议。地点可靠时可查询带来源和时间的天气，写临时 `--weather-json`；没有地点不猜。宗教内容不宣称私人启示、业报或预测，不替代医疗、法律、金融和实际安全判断。道教本版只含七条已核对签诗，原书365条；《占察经》只借身口意分类，未复现仪轨；摩拉维亚每日经文只借方法，独立十二经节池。具体来源和不确定性见 `references/sources.yaml`、仓库 `RESEARCH_V2.md`、`RELIGIOUS_CONTENT_POLICY.md`。旧日签用 `--engine v1` 复算。
