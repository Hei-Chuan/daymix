"""Maintenance helper: generate the complete, authored card indexes. Not used at runtime."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "skills" / "daymix" / "references"
TRIGRAMS = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
BITS = {"乾": "111", "兑": "110", "离": "101", "震": "100", "巽": "011", "坎": "010", "艮": "001", "坤": "000"}  # bottom -> top
# Rows are LOWER, columns UPPER. Collated from the public-domain Zhouyi index.
ROWS = [
    "乾 夬 大有 大壮 小畜 需 大畜 泰",
    "履 兑 睽 归妹 中孚 节 损 临",
    "同人 革 离 丰 家人 既济 贲 明夷",
    "无妄 随 噬嗑 震 益 屯 颐 复",
    "姤 大过 鼎 恒 巽 井 蛊 升",
    "讼 困 未济 解 涣 坎 蒙 师",
    "遁 咸 旅 小过 渐 蹇 艮 谦",
    "否 萃 晋 豫 观 比 剥 坤",
]
KING_WEN = "乾 坤 屯 蒙 需 讼 师 比 小畜 履 泰 否 同人 大有 谦 豫 随 蛊 临 观 噬嗑 贲 剥 复 无妄 大畜 颐 大过 坎 离 咸 恒 遁 大壮 晋 明夷 家人 睽 蹇 解 损 益 夬 姤 萃 升 困 井 革 鼎 震 艮 渐 归妹 丰 旅 巽 兑 涣 节 中孚 小过 既济 未济".split()
THEMES = "守正 承载 起步 求教 等待 辨明 协作 亲近 积累 审慎 通达 闭塞 同行 充实 谦逊 预备 顺应 整理 临事 观察 决断 修饰 收束 复始 守真 蓄力 养护 承压 守险 明辨 感应 持续 退守 推进 显明 藏锋 治家 求同 受阻 疏解 减负 增益 决口 相遇 聚合 上升 困守 修井 更新 鼎新 惊动 止步 渐进 审配 丰实 客行 入微 愉悦 离散 节制 守信 小步 收尾 未竟".split()
assert len(KING_WEN) == len(THEMES) == 64
assert len({n for row in ROWS for n in row.split()}) == 64
assert {n for row in ROWS for n in row.split()} == set(KING_WEN)
CAUTION = set("讼 否 噬嗑 剥 大过 坎 遁 明夷 睽 蹇 困 震 旅 未济".split())
FAVOR = set("泰 大有 谦 复 益 升 解 渐 丰 既济".split())
hexes = []
for low, row in zip(TRIGRAMS, ROWS):
    for high, name in zip(TRIGRAMS, row.split()):
        hexes.append({"id": KING_WEN.index(name) + 1, "name": name,
                      "lower": low, "upper": high, "lines_bottom_up": BITS[low] + BITS[high],
                      "theme": THEMES[KING_WEN.index(name)],
                      "tone": -1 if name in CAUTION else 1 if name in FAVOR else 0,
                      "source_id": "zhouyi"})
hexes.sort(key=lambda x: x["id"])
(ROOT / "eastern").mkdir(exist_ok=True)
(ROOT / "eastern" / "hexagrams.json").write_text(json.dumps(hexes, ensure_ascii=False, indent=2) + "\n")

MAJOR = "愚者 魔术师 女祭司 皇后 皇帝 教皇 恋人 战车 力量 隐者 命运之轮 正义 倒吊人 死神 节制 恶魔 高塔 星星 月亮 太阳 审判 世界".split()
M_THEME = "启程 施展 倾听 滋养 建立 求教 选择 前进 自持 独处 转机 衡量 暂停 转化 调和 诱惑 震荡 希望 迷雾 清明 回顾 完成".split()
M_TONE = [0,1,0,1,0,0,1,1,1,0,0,0,-1,-1,1,-1,-1,1,-1,1,0,1]
cards = [{"id": i, "name": n, "arcana": "major", "upright": M_THEME[i],
          "reversed": "留意" + M_THEME[i] + "的阻滞或失衡", "tone": M_TONE[i], "source_id": "waite"}
         for i,n in enumerate(MAJOR)]
SUITS = [("权杖", "行动"), ("圣杯", "情感"), ("宝剑", "判断"), ("星币", "资源")]
RANKS = [("王牌","开端"), ("二","权衡"), ("三","扩展"), ("四","安定"),
         ("五","摩擦"), ("六","调整"), ("七","应对"), ("八","推进"),
         ("九","积累"), ("十","收束"), ("侍从","消息"), ("骑士","出发"),
         ("王后","照料"), ("国王","统筹")]
for suit, realm in SUITS:
    for rank, step in RANKS:
        cards.append({"id": len(cards), "name": suit + rank, "arcana": "minor",
                      "upright": realm + "中的" + step,
                      "reversed": realm + "中的" + step + "遇到阻滞或失衡",
                      "tone": -1 if rank in ("五",) or (suit == "宝剑" and rank in ("九", "十")) else 1 if rank in ("六", "王牌") else 0,
                      "source_id": "waite"})
assert len(cards) == 78 and all(c["id"] == i for i,c in enumerate(cards))
(ROOT / "tarot").mkdir(exist_ok=True)
(ROOT / "tarot" / "tarot-78.json").write_text(json.dumps(cards, ensure_ascii=False, indent=2) + "\n")
