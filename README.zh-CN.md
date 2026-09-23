# 万象历 v2

[English](README.md) | **简体中文**

《万象历》是可复现的个人日历实验：真实历法与天文数据、历史占验文本、每日经文传统、自省和现实条件共同组成一张当日卡。流程认真，结论是象征性的；它不预报未来。

输入“**查看今日运势**”，默认看到短卡。已连接本项目 MCP 组件的 ChatGPT 可直接点击四象、三镜与出处，在**同一张卡**中展开；单独安装 Skill、在 Codex 或 CLI 中运行时输出文本卡，可用 `--expand` 查看详情。**仅把 GitHub 仓库或 Skill ZIP 加入 ChatGPT，不会自动出现可点击组件**；组件必须有已连接的、可访问的 MCP 服务。

## 四象、三镜与现实

| 层 | 模块 | 当天怎样产生 |
| --- | --- | --- |
| 四象 | 儒家·易 | 用独立稳定字节流模拟《系辞》／朱熹筮仪的49策三变成爻；六爻、本卦、动爻、之卦与古代卦爻辞一次生成。 |
| 四象 | 塔罗 | 78张 Rider–Waite–Smith 体系牌，独立选牌与正逆位。短牌义由项目原创。 |
| 四象 | 道教 | 在已核对的《玄真灵应宝签》**七条签诗子集**中稳定取一条，展示原签诗与出处。原书有365条，但此版尚未全部录入；时辰是原书编排，不是本项目抽签仪轨。 |
| 四象 | 希腊化星象 | Astronomy Engine 计算当地正午的日月水金火木土地心黄经、黄道宫、主要相位；象征解释和天文事实分开。 |
| 三镜 | 佛教 | 借鉴《占察经》的身口意分类作自省，**不模拟木轮仪轨或判定业报**。 |
| 三镜 | 基督宗教 | 借鉴摩拉维亚弟兄会每日经文方法，从独立12条旧约经节池选择；原创中文转述，不复制官方序列。 |
| 三镜 | 斯多葛 | 审查行动、判断与结果之间的可控边界。 |
| 现实 | Reality Correction | 星期与可信、具来源时间的天气可改有效宜忌；不改原卦、牌、签、天象、原始宜忌或象征评级。 |

只有四象进入公开的 `symbolic-v2.1` 象征总评，各记 `-1/0/+1`，如有冲突则保留。没有学业、财运、人际星级。三镜不参与评分；`--context 备考`只调整建议。详细文献、版本取舍及不确定性见 [RESEARCH_V2.md](RESEARCH_V2.md)，逐条来源见 [SOURCES.md](SOURCES.md)。

## 立即运行

仓库根目录（Python 3.10+，内置固定版本依赖）：

```bash
python3 scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo
python3 scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo --format json
python3 scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo --expand yijing
python3 scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo --expand all
python3 scripts/wanxiangli.py --engine v1 --date 2026-09-23 --timezone Asia/Shanghai --user-id demo
```

`--engine v1` 复算旧版：旧 `SALT_VERSION="v1"` 与源脚本已保留，默认 v2 的结果标记 `CAST_VERSION="v2.1"`；分通道种子域仍是 `v2`。v2.1 修正蓍策分堆的边界情况，明确记录版本，不会暗改旧版结果。不传 `--user-id` 时本地生成私有安装标识；托管无持久状态可传 `--identity-mode hosted` 使用共享访客结果。跨设备想保持个人结果一致，可自选非敏感代号。**不要使用姓名、邮箱或电话。**

天气 JSON 可通过 `--weather-json PATH` 输入，必须含 `description`、`hazard`、`source`、`observed_at`，`hazard` 可取 `none/heavy_rain/storm/snow/extreme_heat`；程序不会自行查询天气。没提供可信地点和数据时不显示“天气安全”。

## ChatGPT 点击组件

`ui/` 是独立 MCP Apps 实现；与 Python 算法通过完整 `wanxiangli/2` JSON 解耦。已部署并连接 MCP 服务时，`get_daily_card` 运行一次，组件从该结果本地展开/收起、全部展开/收起、打开出处。手机版与暗色模式适配；组件开合状态使用可选的 ChatGPT widget state。展开不调用后端或 LLM。

本地开发：

```bash
npm ci --prefix ui
npm run build --prefix ui
npm run start --prefix ui
# MCP endpoint: http://127.0.0.1:3000/mcp
```

ChatGPT 连接需要把服务部署为稳定、可公开访问的 HTTPS MCP endpoint，并在对应的开发者环境连接；本地地址仅用于测试。该仓库**不包含现成托管服务、外部账号或已安装的 ChatGPT 连接**。单独上传 Skill ZIP 只提供文本回退。部署、域名验证与连接条件依 [OpenAI 当前插件文档](https://developers.openai.com/plugins/build/mcp-server)。`ui/README.md` 记录服务器和组件测试步骤。

## 发布、研究与边界

`python3 -m unittest discover -s tests -v` 测算法和包；`python3 tools/build_release.py` 产出 Skill 与插件候选 ZIP。代码包内保留固定版本 `lunar-python` 与 `astronomy-engine` 的 MIT 声明。项目原创部分按 [MIT](LICENSE)；具体古籍、译本、网站编排与第三方软件分别见 [SOURCES.md](SOURCES.md) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

宗教传统内部对占问的态度复杂；这里的自省、经文和签诗不代表宗教机构认可混合日历，不宣称私人神谕，不用于疾病、生死、考试必过、法律、金融或安全决策。现实证据具有最高行动优先级。见 [RELIGIOUS_CONTENT_POLICY.md](RELIGIOUS_CONTENT_POLICY.md) 与 [DISCLAIMER.md](DISCLAIMER.md)。
