# 万象历 · Wanxiangli

[English](README.md) | **简体中文**

《万象历》是生成个人每日黄历的**单 Agent Skill**：**历法与象征输入 → 多种解释视角 → 现实修正 → 每日黄历**。真实历法与天文计算、可复现的易卦和塔罗抽取构成原始记录；少量可追溯的佛家、道家、基督宗教等知识卡提供不同读法。流程很认真，设定允许略带荒诞。

## 立即使用

安装 Skill 后，输入 **“查看今日运势”**。首个公开分发版本为 **0.1.0**。

下例由当前版本实际运行生成，可用 `python3 skills/wanxiangli/scripts/wanxiangli.py --date 2026-09-23 --timezone Asia/Shanghai --user-id demo --context 备考` 复现：

```text
万象历 · 9月23日｜八月十三 · 庚子日
今日：中吉
宜  整理生活 · 整理资料 · 梳理路径
忌  草率定约 · 仓促搬动 · 临时改作息
学业 ★★★★☆　财运 ★★★☆☆　人际 ★★★☆☆
备考提示：复盘错题 · 整理旧知识
今日象：渐进，望月期
诸说合参：易理取「渐进」，塔罗示「情感中的出发遇到阻滞或失衡」；佛家取无住，道家取知止，基督宗教借种子与等待之象。诸象合参；裁定中吉。
展开：易理／塔罗／星象／佛家／道家／基督宗教／现实修正
今日总结：今日先复盘错题，避免草率定约。
```

`demo` 仅供公开示例使用。不指定 `--user-id` 时，程序在本机保存私有安装标识；同一安装环境、日期与时区的核心结果稳定。跨设备复现需自行使用同一个非敏感标识。

## 安装

### ChatGPT（支持自定义 Skills 的环境）

从 GitHub Release 下载 `wanxiangli-skill.zip`，在支持自定义 Skill 上传的 ChatGPT 环境中创建或上传 Skill，然后输入 **查看今日运势**。ZIP 只有一层 `wanxiangli/` 顶层目录，包含 `SKILL.md`、脚本、参考卡与固定版本依赖。上传权限、Python 执行、天气工具与文件持久性取决于具体环境。若托管环境没有持久安装标识，Skill 使用同日共享的访客日签；你也可自愿指定一个固定、非敏感的代号，例如 `blue-fish`，供自己跨会话复现。请勿使用邮箱或真实身份信息。

### Codex / portable plugin

从 GitHub Release 下载 `wanxiangli-plugin.zip`，使用所在环境支持的插件上传或安装流程安装。根目录 `plugin.json` 自动发现 `skills/wanxiangli/`，`.codex-plugin/plugin.json` 提供兼容格式。本地 Codex 也可将 `skills/wanxiangli/` 放入 `$HOME/.agents/skills/`（或仓库的 `.agents/skills/`），再重新发现 Skill。运行需要 Python 3.10+ 和 IANA 时区数据。两种发布包共用一份 Skill 源码。

### 从源码运行（开发者）

```bash
git clone https://github.com/Hei-Chuan/wanxiangli.git
cd wanxiangli
python3 -m pip install -r requirements.txt
python3 skills/wanxiangli/scripts/wanxiangli.py --timezone Asia/Shanghai
python3 -m unittest discover -s tests -v
python3 tools/build_release.py
```

Skill 包内已有固定版本依赖；普通用户无须临时安装。`requirements.txt` 供源码开发使用，脚本不会自行下载软件或联网。

## 目前怎样工作

| 层次 | 已实现内容 |
| --- | --- |
| 历法 | [`lunar_python`](https://github.com/6tail/lunar-python) 给出农历、节气、干支和传统黄历宜忌。JSON 保留原词，仅将少数条目转成现代行动。 |
| 易理 | 按每日固定 seed 从 64 卦中抽一卦。它是本项目的“日签”，**不是**蓍草或六爻变卦推演；简短主题与评分由项目制定。 |
| 塔罗 | 从 78 张 Rider–Waite–Smith 体系牌中独立抽牌并定正逆位；短牌义为原创，不冒充原著引文。 |
| 天文 | [Astronomy Engine](https://github.com/cosinekitty/astronomy) 计算当地正午太阳视黄经与月日黄经差。粗分的月相只承载产品象征，不排出生星盘，也不宣称天体影响行为。 |
| 解释 | 少量原创知识卡提供不同视角，不参与抽取；各体系允许意见不同。 |
| 现实 | `--weather-json PATH` 接收外部天气数据。Skill 知道地点并找到可靠来源时可以查天气，但**脚本本身不联网**。恶劣天气只调整行动建议，不改原卦、原牌、原始宜忌或评级。没有节假日和用户日历接入。 |

`--format json` 输出结构化记录；`--context 备考` 只调整建议措辞。详情可用 `--expand 佛家`、`--expand 塔罗`、`--expand 易理`、`--expand 星象`、`--expand 道家`、`--expand 基督宗教`、`--expand 现实修正` 或 `--expand 全部`。作为 Skill 使用时也可说“展开佛家”，沿用当日结果。运行 `python3 -m unittest discover -s tests -v` 验证。

天气文件必须提供 `description`、`hazard`、`source`、`observed_at`，例如：

```json
{"description":"强降雨","hazard":"heavy_rain","source":"当地气象机构","observed_at":"2026-09-23T09:00:00+08:00"}
```

`hazard` 仅支持 `none`、`heavy_rain`、`storm`、`snow`、`extreme_heat`；地点或来源不明时跳过修正。评级是产品内部象征分值，并非发生概率或预测精度，最低显示“小凶”。默认短卡，详情按需展开。

## 边界

项目面向娱乐、文化探索、文本实验与自我反思。它不是宗教机构、宗教宣传或传教工具，不提供神学权威、宗教咨询或科学预测；不能替代医疗、法律、财务与安全判断，也不保证未来事件。各传统内部有不同流派，有限的概念卡不代表所有信徒，更不能解决教义争论。详见双语[免责声明](DISCLAIMER.md)和[宗教内容规范](RELIGIOUS_CONTENT_POLICY.md)。

伊斯兰宗教传统明确不属于本项目的内容范围。这一限制仅属于项目范围设计，旨在避免不准确呈现或无意冒犯，不构成对伊斯兰教、穆斯林或相关文化的任何评价。

## 来源、许可与参与

原创代码与短卡采用 [MIT 许可证](LICENSE)。仓库打包两项未经修改的 MIT 依赖及各自许可声明；不打包 CBETA 数据库文本、受版权保护的现代中文圣经译本、塔罗图像或来源著作全文。[SOURCES.md](SOURCES.md) 区分已打包软件、改写参考、只读参考和运行时数据；[`skills/wanxiangli/references/sources.yaml`](skills/wanxiangli/references/sources.yaml) 是逐条记录。网页能打开，不等于允许转载。

**第三方说明：** `lunar_python` 1.4.8 与 `astronomy-engine` 2.1.19 是固定版本的 MIT 依赖，包内提供后备副本（优先使用版本一致的外部安装）。版权声明与来源见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)；《周易》索引、怀特著作、World English Bible 及列出的古籍用于校准原创短卡。CBETA 只作研究参考。[`xuanxue-engine`](https://github.com/sxt9805/xuanxue-engine) 是架构参考，[`fortune-telling-skills`](https://github.com/eamanc-lab/fortune-telling-skills) 是研究参考；未复制两者代码或文案。列名不意味着作者、出版者参与或认可本项目。

提交内容前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)、[RELIGIOUS_CONTENT_POLICY.md](RELIGIOUS_CONTENT_POLICY.md) 和 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。调查记录见 [RESEARCH.md](RESEARCH.md)。
