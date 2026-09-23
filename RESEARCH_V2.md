# 万象历 v2：机制、证据与限度

检索与复核日期：2026-09-23。每个模块输出的 `source_ids` 指向 [`references/sources.yaml`](skills/wanxiangli/references/sources.yaml)。旧版调查仍见 [`RESEARCH.md`](RESEARCH.md)。下列“史实 / 学术解释 / 项目实现”分开记录；外部文本链接不意味着其机构认可本产品。

## 儒家·易

- **原典：** 《[系辞上](https://ctext.org/book-of-changes/xi-ci-shang/zh)》大衍章有五十策、用四十九、分二挂一、揲四归奇、三变成爻十八变成卦。《周易》的卦爻辞与《易传》并非同一写作层；后世儒家读法又有发展。[朱熹《周易本义·筮仪》](https://ctext.org/wiki.pl?chapter=862643&if=gb)细述每次剩余策数和六七八九。
- **实现：** 49策每爻分堆三次，右堆至少留两策，以便挂一后仍非空；剩24/28/32/36策得6/7/8/9。六爻独立导出本卦、老阴老阳动爻和之卦。卦辞及爻辞采用古代底本录文；`zhouyi-text.json`由 CText 来源的二次机器数据整理，已核对64卦顺序、每卦至少六爻，并抽查原典网页。解释短句为项目原创，评分沿用原项目卦主题编辑判断。首次本地 v2 生成器允许右堆恰为一策，挂一后出现空堆；v2.1 修正该边界，`SEED_VERSION=v2` 保留其他通道的字节流，`CAST_VERSION=v2.1` 明示结果版本。
- **不确定：** 当前不是完整校勘本，文字异体与版本异文未逐条校对；程序的均匀分堆哈希模拟并不等同亲手筮蓍、心理选择或西周历史实践。具体动爻解释不把后世“多动爻决疑”规则强称唯一传统。

## 道教

- **原典与目录：** [《玄真灵应宝签》序](https://zh.wikisource.org/wiki/玄真靈應寶籤)自述十二时各三十、五行五签；[道教文化中心的道藏目录](https://zh.daoinfo.org/index.php?title=玄真靈應寶籤)记三卷、《正统道藏》正一部、约元代或明初，合365签。
- **实现：** 目前仅七条古诗核对入库，含原签号、品第和链接；独立通道对七条每日确定性抽取，短评避开功名、寿命等现实保证。其余358条尚未校订，**绝不称此为365条完整数字签库**。
- **仪轨限度：** 十二时是书的编排，现有材料没有证明应按当下时辰选三十条，更没有证明程序中的每日抽取可溯及道教仪轨。老庄哲学仅在研究背景中出现，不替代宗教签书。

## 塔罗

- **历史：** [大都会博物馆](https://www.metmuseum.org/zh/perspectives/immaterial-tarot)将 Pamela Colman Smith 绘制牌组及1909年发行写明；[Waite 的1910年说明书](https://en.wikisource.org/wiki/The_Pictorial_Key_to_the_Tarot)是牌义历史参考。不能把每条今日短义直接署给 Smith 或 Waite。
- **实现：** 保留78张牌表与独立选牌、正逆位通道；另写 `tarot-v2.json` 的78组原创正逆位短义，避免 v1 自动套“阻滞或失衡”的机械模板。逆位是另一种提问视角，不把负向牌机械翻正。牌图和现代商业书的长解释不入包。旧牌义中重复措辞仍可逐步编辑，但编辑必须升数据版本才不使历史日签漂移。

## 星象

- **历史：** [大英博物馆的巴比伦黄道材料](https://www.britishmuseum.org/collection/object/W_1885-0430-15)提供前史；希腊化时期的个人出生星盘与前史不应混为一谈。[托勒密《四书》卷一](https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/1B%2A.html)论相位；其四种几何相位之外，合相在文本讨论中也重要，严格讲不与四几何相位同类。
- **实现：** Astronomy Engine 2.1.19 计算本地正午对应 UTC 时刻的地心太阳、月亮、水金火木土的黄经，按热带黄道每30°标宫。五种角距以 ±6° **项目显示阈值**列出；该阈值既非古代统一 orb，也非天体运行因果论。评分只概括日月参与的相位，其他相位照列而不计。
- **限度：** 无出生时间地点，无上升点、宫位、个人星盘；坐标有数值近似及外部库版本要求。天文位置是真实计算，传统象征是文化解释。

## 佛教

- **文本：** [《占察善恶业报经》卷上](https://zh.wikisource.org/wiki/占察善惡業報經/卷01)第二组木轮分身、口、意；但经文实际仪轨远不止三选一。[佛教团体刊载的蕅益相关释义](https://www.baus-ebs.org/sutra/fan-read/002/10.htm)可见后世接受，[台湾大学论文摘要](https://dlbs.liberal.ntu.edu.tw/DLMBS/search/search_detail.jsp?comefrom=fulltextproceeding&seq=650570)讨论疑伪经问题；“疑伪”是经录与学术分类，不是对信众的贬损。
- **实现：** 独立通道每天从身口意三类选一个自省主题；不称木轮占验、不判过去业或疾病生死，也不把普通寺院民俗与经文仪轨等同。

## 基督宗教

- **官方说明：** [Moravian Church 英国省](https://www.moravian.org.uk/daily-watchwords/what-are-the-daily-watchwords)记旧约经节按抽签选取并配新约经文；[Moravian Archives](https://www.moravianchurcharchives.org/general/anniversary-of-moravian-daily-texts/)记1728/1731的发展及现代约2000旧约经节池。部分官方页面把起始年份表述为1722的共同经文实践，另有1728一次特定 watchword 的记载；二者所指活动不同，不硬并作单一起始日。
- **实现：** 独立十二条旧约经节池、独立稳定种子、原创中文短述，不复制官方 daily sequence 或现代中文译本。与官方做法不同的是本项目未人工配新约经文，规模也小得多。对照 [World English Bible 公版声明](https://ebible.org/eng-web/copr.htm)核对经节；当前不代表任何教会，不把抽到的经文当私人启示。

## 斯多葛

- **原典：** [Epictetus《手册》1、32](https://classics.mit.edu/Epictetus/epicench.html)区分自有判断行动与外在结果，并讨论占问；[《谈话录》](https://classics.mit.edu/Epictetus/discourses.2.two.html)批评过度依靠占问而荒废义务。古典原文与现代英文译本需分开看待。
- **实现：** 不抽签、不评分；不以星象接管用户的选择。把外在不确定性转换为今天一件可执行的行动。

## 总评、现实与 UI

四象各有自身结果，`symbolic-v2.1` 才在表层把四项各映射 -1/0/+1，透明合为 -4..4 五档。分歧显式保留；三镜不入分，现实不改分。旧版 `2*hex+tarot+moon` 不沿用。学业/财运/人际星级缺少独立依据，因此删除。`--context 备考`只改总结。

[OpenAI Plugins UI](https://developers.openai.com/plugins/build/chatgpt-ui) 使用 MCP Apps `_meta.ui.resourceUri`、`text/html;profile=mcp-app`，结构化工具结果一次交组件，本地原生 `<details>` 展开，不重新调用模型或算法。Skill ZIP 单独安装只得到文字回退；点击 UI 要连接可达的 MCP 服务端。组件状态只记录开合，不记录个人身份或代替每日 JSON。
