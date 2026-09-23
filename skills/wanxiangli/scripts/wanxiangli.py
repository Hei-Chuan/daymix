#!/usr/bin/env python3
"""Wanxiangli: deterministic symbolic ledger, reality adjustment, JSON and card output."""
import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
import secrets
import sys
from datetime import date, datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "wanxiangli/1"
SALT_VERSION = "v1"  # keep unchanged across updates; changing it changes every day's draw
LABELS = ["小凶", "平", "小吉", "中吉", "大吉"]
MODERN = {"沐浴": "整理生活", "修饰垣墙": "整理资料", "平治道涂": "梳理路径", "入学": "温故",
          "会友": "主动联络", "会亲友": "主动联络", "习艺": "练习技能", "扫舍": "收拾桌面",
          "出行": "外出办事", "交易": "处理交易", "立券交易": "工作日内办手续",
          "开市": "推进新事", "纳财": "整理账目"}
DONTS = {"出行": "远行", "交易": "冲动消费", "嫁娶": "草率定约", "入宅": "仓促搬动",
         "安床": "临时改作息", "动土": "贸然开工", "开市": "仓促开新坑"}
THEME_ACTION = {"渐进": "按原计划推进", "止步": "暂停强推", "等待": "先作准备",
                "积累": "温故", "整理": "整理资料", "复始": "拾起旧事", "受阻": "先清障碍",
                "收束": "完成旧事", "审慎": "复核决定", "守信": "兑现约定"}


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def dependency(module, package, version):
    """Prefer the exact external release; use the audited bundled copy if absent."""
    try:
        installed = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        installed = None
    if installed == version:
        try:
            return importlib.import_module(module)
        except ImportError as exc:
            raise RuntimeError(f"{package} {version} 已安装但无法导入：{exc}") from exc
    vendor = ROOT / "vendor"
    if (vendor / module / "__init__.py").is_file():
        sys.path.insert(0, str(vendor))
        try:
            return importlib.import_module(module)
        except ImportError as exc:
            raise RuntimeError(f"内置 {package} {version} 无法导入：{exc}") from exc
    raise RuntimeError(f"缺少 {package} {version}，且 Skill 中没有可用内置依赖；无法计算，不能猜测历法或天文结果")


def installation_id():
    """Private local ID. Do not log or place it in output; user ID can override it."""
    folder = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "wanxiangli"
    path = folder / "installation.json"
    if path.exists():
        value = json.loads(path.read_text(encoding="utf-8"))["id"]
        if isinstance(value, str) and len(value) >= 16:
            return value
        raise ValueError("安装标识损坏，请手动修复，不自动更换当日结果")
    folder.mkdir(parents=True, exist_ok=True)
    value = secrets.token_hex(16)
    try:
        with path.open("x", encoding="utf-8") as f:
            os.chmod(path, 0o600)
            json.dump({"id": value}, f)
    except FileExistsError:
        return installation_id()
    return value


def draw(day, person, channel, modulo):
    token = f"{SALT_VERSION}\0{day.isoformat()}\0{person}\0{channel}".encode()
    return int.from_bytes(hashlib.sha256(token).digest()[:8], "big") % modulo


def calendar(day, tz):
    Solar = dependency("lunar_python", "lunar-python", "1.4.8").Solar
    l = Solar.fromYmd(day.year, day.month, day.day).getLunar()
    mid = datetime.combine(day, time(12), ZoneInfo(tz))
    terms = l.getJieQiTable()
    terms_today = sorted({name for name, moment in terms.items()
                          if datetime(moment.getYear(), moment.getMonth(), moment.getDay(),
                                      moment.getHour(), moment.getMinute(), moment.getSecond(),
                                      tzinfo=ZoneInfo("Asia/Shanghai")).astimezone(ZoneInfo(tz)).date() == day})
    return {"gregorian": day.isoformat(), "timezone": tz, "weekday": day.weekday(),
            "lunar": f"{l.getMonthInChinese()}月{l.getDayInChinese()}",
            "ganzhi": {"year": l.getYearInGanZhi(), "month": l.getMonthInGanZhiExact(),
                       "day": l.getDayInGanZhi(), "day_nayin": l.getDayNaYin()},
            "solar_terms_today": terms_today, "solar_term_reported": l.getJieQi() or None,
            "almanac": {"yi": l.getDayYi(), "ji": l.getDayJi(),
                        "day_officer": l.getZhiXing(), "spirit": l.getDayTianShen(),
                        "spirit_type": l.getDayTianShenType(),
                        "pengzu": [l.getPengZuGan(), l.getPengZuZhi()]},
            "reference_instant": mid.isoformat()}


def astronomy(day, tz):
    astro = dependency("astronomy", "astronomy-engine", "2.1.19")
    instant = datetime.combine(day, time(12), ZoneInfo(tz)).astimezone(timezone.utc)
    moment = astro.Time.Make(instant.year, instant.month, instant.day,
                             instant.hour, instant.minute, instant.second)
    phase = round(astro.MoonPhase(moment), 3)
    sun = round(astro.SunPosition(moment).elon, 3)
    stage = "新月期" if phase < 45 or phase >= 315 else "渐盈期" if phase < 135 else "望月期" if phase < 225 else "渐亏期"
    # Symbolic convention of this skill, not an empirical claim about behaviour.
    tone = 1 if stage == "渐盈期" else -1 if stage == "渐亏期" else 0
    return {"method": "geocentric ecliptic longitudes at local noon", "moon_sun_angle_deg": phase,
            "sun_ecliptic_longitude_deg": sun, "moon_stage": stage,
            "symbolic_tone": tone, "is_symbolic": True, "source_id": "astronomy_engine"}


def unique(items):
    return list(dict.fromkeys(x for x in items if x))


def pick_actions(cal, hexa):
    yi = [MODERN[x] for x in cal["almanac"]["yi"] if x in MODERN]
    ji = [DONTS[x] for x in cal["almanac"]["ji"] if x in DONTS]
    theme = THEME_ACTION.get(hexa["theme"], hexa["theme"] + "手头事务")
    if "外出办事" in yi and "出行" not in cal["almanac"]["ji"]:
        yi = ["外出办事"] + [x for x in yi if x != "外出办事"]
    return unique(yi + [theme, "复盘旧事"])[:3], unique(ji + ["冲动消费", "深夜开新坑", "临时改计划"])[:3]


def reality(base_dos, base_donts, day, weather):
    dos, donts = list(base_dos), list(base_donts)
    changes = []
    if day.weekday() >= 5 and "工作日内办手续" in dos:
        dos.remove("工作日内办手续")
        changes.append("周末，撤回工作日办手续建议")
    if weather:
        hazard = weather.get("hazard")
        if hazard not in ("none", "heavy_rain", "storm", "snow", "extreme_heat"):
            raise ValueError("天气 hazard 不在允许值中")
        if hazard != "none":
            travel = [x for x in dos if "外出" in x or "远行" in x]
            for x in travel:
                dos.remove(x)
            replacement = "避免非必要远行" if hazard in ("heavy_rain", "storm", "snow") else "避开高温时段外出"
            donts = unique([replacement] + donts)[:3]
            changes.append(("原判有出行之象，" if travel else "现实条件提示，") +
                           f"{weather['description']}；经复核调整行动建议")
    return {"observations": {"weekday": day.weekday(), "weather": weather},
            "adjustments": changes, "effective_dos": dos, "effective_donts": donts,
            "original_dos": base_dos, "original_donts": base_donts}


def make(day, tz, person, weather=None, context=None):
    cal = calendar(day, tz)
    hexes = load("references/eastern/hexagrams.json")
    cards = load("references/tarot/tarot-78.json")
    h = dict(hexes[draw(day, person, "hexagram", 64)])
    tarot = dict(cards[draw(day, person, "tarot", 78)])
    tarot["orientation"] = "正位" if draw(day, person, "orientation", 2) == 0 else "逆位"
    tarot["meaning"] = tarot["upright"] if tarot["orientation"] == "正位" else tarot["reversed"]
    # Reversal denotes obstruction. It does not automatically turn a hard card into good news.
    tarot["effective_tone"] = tarot["tone"] if tarot["orientation"] == "正位" else min(0, tarot["tone"])
    astro = astronomy(day, tz)
    # Day's canonical score depends on cast and noon astronomy alone, never context or weather.
    score = h["tone"] * 2 + tarot["effective_tone"] + astro["symbolic_tone"]
    level = 0 if score <= -3 else 1 if score <= -1 else 2 if score <= 1 else 3 if score <= 3 else 4
    rating = LABELS[level]
    dos, donts = pick_actions(cal, h)
    corrected = reality(dos, donts, day, weather)
    opposing = (h["tone"] > 0 and tarot["effective_tone"] < 0) or (h["tone"] < 0 and tarot["effective_tone"] > 0)
    status = "易理与塔罗有分歧，保留意见后综合裁定" if opposing else "经合参维持原判"
    patient = h["tone"] < 0 or tarot["effective_tone"] < 0 or h["theme"] in ("渐进", "等待", "止步")
    lenses = {
        "buddhism": {"kind": "interpretation_lens", "concept": "无住" if patient else "精进",
                     "reference": "references/buddhism/concepts.md"},
        "taoism": {"kind": "interpretation_lens", "concept": "知止" if patient else "不争与顺势",
                    "reference": "references/taoism/concepts.md"},
        "christianity": {"kind": "interpretation_lens", "concept": "种子与等待" if patient else "道路与光",
                         "reference": "references/christianity/symbols.md"},
    }
    study = max(1, min(5, 3 + h["tone"] + (1 if tarot["effective_tone"] > 0 else 0)))
    finance = max(1, min(5, 3 + tarot["effective_tone"]))
    social = max(1, min(5, 3 + astro["symbolic_tone"]))
    suggestions = {"study": "复盘错题、整理旧知识" if context == "备考" else "整理旧资料"}
    action = corrected["effective_dos"][0] if corrected["effective_dos"] else "先处理手头旧事"
    avoid = corrected["effective_donts"][0] if corrected["effective_donts"] else "仓促决定"
    summary = f"今日先复盘错题，避免{avoid}。" if context == "备考" else f"今日先{action}，避免{avoid}。"
    return {"schema": SCHEMA, "date": cal, "overall": {"rating": rating, "score": score,
            "formula": "2*hex_tone + tarot_effective_tone + lunar_phase_symbolic_tone",
            "scale": LABELS}, "dos": dos, "donts": donts,
            "areas": {"study": {"stars": study}, "finance": {"stars": finance}, "social": {"stars": social}},
            "symbol": {"text": h["theme"] + "，" + astro["moon_stage"], "source": ["yijing", "astronomy"]},
            "systems": {"yijing": h, "tarot": tarot, "astrology": astro, **lenses},
            "reality_correction": corrected, "synthesis": {"conflict": opposing, "statement": status},
            "personalization": {"context": context, "suggestions": suggestions if context else {}},
            "summary": summary}


def card(v):
    d, r, s = v["date"], v["reality_correction"], v["systems"]
    stars = lambda n: "★" * n + "☆" * (5 - n)
    marks = v["areas"]
    month_day = f"{int(d['gregorian'][5:7])}月{int(d['gregorian'][8:10])}日"
    conflict = "易理与塔罗意见有别；" if v["synthesis"]["conflict"] else "诸象合参；"
    correction = "\n现实复核：" + "；".join(r["adjustments"]) if r["adjustments"] else ""
    lines = [f"万象历 · {month_day}｜{d['lunar']} · {d['ganzhi']['day']}日", f"今日：{v['overall']['rating']}",
             "宜  " + " · ".join(r["effective_dos"]), "忌  " + " · ".join(r["effective_donts"]),
             f"学业 {stars(marks['study']['stars'])}　财运 {stars(marks['finance']['stars'])}　人际 {stars(marks['social']['stars'])}",
             "今日象：" + v["symbol"]["text"],
             "诸说合参：易理取「" + v["systems"]["yijing"]["theme"] + "」，塔罗示「" +
             v["systems"]["tarot"]["meaning"] + "」；佛家取" + s["buddhism"]["concept"] +
             "，道家取" + s["taoism"]["concept"] + "，基督宗教借" + s["christianity"]["concept"] +
             "之象。" + conflict + "裁定" + v["overall"]["rating"] + "。" + correction,
             "展开：易理／塔罗／星象／佛家／道家／基督宗教／现实修正",
             "今日总结：" + v["summary"]]
    if v["personalization"]["context"] == "备考":
        lines.insert(5, "备考提示：复盘错题 · 整理旧知识")
    return "\n".join(lines)


def detail(v, section):
    """Stable prose sections built from today's stored facts; no new draw."""
    s, r = v["systems"], v["reality_correction"]
    h, t, a = s["yijing"], s["tarot"], s["astrology"]
    if section == "易理":
        return (f"易理与黄历｜{h['name']}（下{h['lower']}上{h['upper']}，文王序第{h['id']}卦）\n"
                f"六爻自下而上：{h['lines_bottom_up']}。本项目日签主题：{h['theme']}。"
                f"日柱{v['date']['ganzhi']['day']}，纳音{v['date']['ganzhi']['day_nayin']}。"
                f"传统宜：{'、'.join(v['date']['almanac']['yi'][:5])}；"
                f"传统忌：{'、'.join(v['date']['almanac']['ji'][:5])}。今日原判宜{'、'.join(v['dos'])}。")
    if section == "塔罗":
        return (f"塔罗｜{t['name']} · {t['orientation']}\n固定基础牌义：{t['upright']}；"
                f"本日语境：{t['meaning']}。这张牌保留其独立意见，"
                f"综合评级仍为{v['overall']['rating']}。")
    if section == "星象":
        return (f"星象｜{a['moon_stage']}\n本地正午太阳视黄经{a['sun_ecliptic_longitude_deg']}°，"
                f"月日黄经差{a['moon_sun_angle_deg']}°。月相分段只用于象征性的节奏提示；"
                "没有出生时间地点，不推个人星盘。")
    if section == "佛家":
        concept = s["buddhism"]["concept"]
        return (f"佛家详解｜{concept}\n"
                f"从{concept}理解今日的{h['theme']}："
                + ("先做眼前可做的事，别把心力全压在结果上。" if concept == "无住" else "循序练习，把注意力放回稳定行动。")
                + "这是解释视角，不是对卦牌的宗教认可。")
    if section == "道家":
        concept = s["taoism"]["concept"]
        return (f"道家详解｜{concept}\n"
                + ("看清当下的势与限度：今天宜收束、留白；知止不等于放弃。" if concept == "知止"
                   else "今日可顺着已经具备的条件推进，不必为争快而强为。"))
    if section == "基督宗教":
        concept = s["christianity"]["concept"]
        return (f"基督宗教象征｜{concept}\n"
                + ("把已有的事照料好，等待其生长；并不要求停止现实行动。" if concept == "种子与等待"
                   else "留意眼前可辨的一步，无须假装已经知道整段道路。")
                + "作为文学与思想象征，不替任何人物宣告指令。")
    if section == "现实修正":
        weather = r["observations"]["weather"]
        evidence = f"天气：{weather['description']}（{weather['source']}，{weather['observed_at']}）。" if weather else "天气：无可靠当地数据，未作天气修正。"
        return (f"现实修正｜原判宜{'、'.join(r['original_dos'])}；忌{'、'.join(r['original_donts'])}。\n"
                + evidence + f"现行宜{'、'.join(r['effective_dos'])}；忌{'、'.join(r['effective_donts'])}。"
                + ("原始卦、牌与评级未变。" if r["adjustments"] else "维持原判。"))
    if section == "全部":
        return "\n\n".join(detail(v, x) for x in ("易理", "塔罗", "星象", "佛家", "道家", "基督宗教", "现实修正"))
    raise ValueError(f"未知栏目：{section}")


def main():
    p = argparse.ArgumentParser(description="万象历：查看今日运势")
    p.add_argument("--date", help="YYYY-MM-DD；默认按时区取今日")
    p.add_argument("--timezone", default="Asia/Shanghai")
    p.add_argument("--user-id", help="可选稳定标识；默认本机私有安装标识，勿用敏感信息")
    p.add_argument("--identity-mode", choices=["local", "hosted"], default="local",
                   help="local 使用私有本机标识；hosted 无持久账户标识时使用公开的访客日签，不写入配置")
    p.add_argument("--context", choices=["备考"], help="仅调整建议层，不参与核心推演")
    p.add_argument("--weather-json", help="具描述、hazard、source、observed_at的JSON文件")
    p.add_argument("--format", choices=["json", "card"], default="card")
    p.add_argument("--expand", choices=["易理", "塔罗", "星象", "佛家", "道家", "基督宗教", "现实修正", "全部"],
                   help="只展开指定栏目；沿用同一日期与 seed")
    a = p.parse_args()
    try:
        tz = ZoneInfo(a.timezone)
        today = date.fromisoformat(a.date) if a.date else datetime.now(tz).date()
        weather = json.loads(Path(a.weather_json).read_text()) if a.weather_json else None
        if weather and not all(weather.get(k) for k in ("description", "source", "observed_at", "hazard")):
            raise ValueError("天气数据必须包含 description、source、observed_at、hazard")
        person = a.user_id or ("guest" if a.identity_mode == "hosted" else installation_id())
        v = make(today, a.timezone, person, weather, a.context)
        print((detail(v, a.expand) + "\n今日总结：" + v["summary"]) if a.expand else
              json.dumps(v, ensure_ascii=False, indent=2) if a.format == "json" else card(v))
    except (ValueError, RuntimeError, KeyError) as exc:
        print(f"万象历：{exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
