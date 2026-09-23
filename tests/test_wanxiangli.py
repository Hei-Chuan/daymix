import importlib.util
import json
import re
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "wanxiangli"
spec = importlib.util.spec_from_file_location("wanxiangli_engine", SKILL / "scripts/wanxiangli.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class DailyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.day = date(2026, 9, 23)
        cls.one = engine.make(cls.day, "Asia/Shanghai", "test-user")

    def test_same_day_reproducible(self):
        self.assertEqual(self.one, engine.make(self.day, "Asia/Shanghai", "test-user"))

    def test_next_day_changes_draw(self):
        other = engine.make(self.day + timedelta(days=1), "Asia/Shanghai", "test-user")
        self.assertNotEqual((self.one["systems"]["yijing"]["id"], self.one["systems"]["tarot"]["id"]),
                            (other["systems"]["yijing"]["id"], other["systems"]["tarot"]["id"]))

    def test_details_reuse_base_facts(self):
        again = engine.make(self.day, "Asia/Shanghai", "test-user", context="备考")
        for system in ("yijing", "tarot", "astrology"):
            self.assertEqual(self.one["systems"][system], again["systems"][system])
        for system in ("buddhism", "taoism", "christianity"):
            self.assertEqual(self.one["systems"][system]["kind"], "interpretation_lens")
        self.assertEqual(self.one["overall"], again["overall"])
        for section in ("佛家", "道家", "塔罗", "易理"):
            self.assertEqual(engine.detail(self.one, section), engine.detail(again, section))
        self.assertIn(self.one["systems"]["tarot"]["name"], engine.detail(again, "塔罗"))

    def test_conflict_is_represented(self):
        for n in range(60):
            item = engine.make(self.day + timedelta(days=n), "Asia/Shanghai", "test-user")
            if item["synthesis"]["conflict"]:
                self.assertIn("保留意见", item["synthesis"]["statement"])
                return
        self.fail("60 days did not contain a recorded conflict")

    def test_weather_only_adjusts_action(self):
        data = {"description": "强降雨", "hazard": "heavy_rain", "source": "test weather desk",
                "observed_at": "2026-09-23T12:00:00+08:00"}
        changed = engine.make(self.day, "Asia/Shanghai", "test-user", weather=data)
        for k in ("overall", "dos", "donts", "systems", "areas"):
            self.assertEqual(self.one[k], changed[k])
        self.assertEqual(changed["reality_correction"]["original_dos"], self.one["dos"])
        for n in range(365):
            d = self.day + timedelta(days=n)
            baseline = engine.make(d, "Asia/Shanghai", "test-user")
            if "外出办事" in baseline["dos"]:
                adjusted = engine.make(d, "Asia/Shanghai", "test-user", weather=data)
                self.assertNotIn("外出办事", adjusted["reality_correction"]["effective_dos"])
                self.assertIn("避免非必要远行", adjusted["reality_correction"]["effective_donts"])
                self.assertIn("原判有出行之象", adjusted["reality_correction"]["adjustments"][0])
                self.assertEqual(baseline["systems"], adjusted["systems"])
                return
        self.fail("未找到实际黄历宜出行日期")

    def test_card_length_and_summary(self):
        output = engine.card(self.one)
        self.assertLessEqual(len(output), 310)
        self.assertEqual(output.count("今日总结："), 1)
        self.assertTrue(output.splitlines()[-1].startswith("今日总结："))
        self.assertTrue(self.one["summary"].endswith("。"))
        self.assertLessEqual(len(self.one["summary"]), 40)
        personalized = engine.make(self.day, "Asia/Shanghai", "test-user", context="备考")
        self.assertIn("复盘错题", engine.card(personalized))

    def test_no_scary_predictions(self):
        for n in range(90):
            output = engine.card(engine.make(self.day + timedelta(days=n), "Asia/Shanghai", "test-user"))
            for forbidden in ("大凶", "血光之灾", "必过", "必得", "花钱消灾", "死亡预测"):
                self.assertNotIn(forbidden, output)

    def test_reversal_does_not_flip_negative_card_positive(self):
        for n in range(500):
            item = engine.make(self.day + timedelta(days=n), "Asia/Shanghai", "test-user")
            tarot = item["systems"]["tarot"]
            if tarot["orientation"] == "逆位" and tarot["tone"] < 0:
                self.assertLessEqual(tarot["effective_tone"], 0)
                return
        self.fail("未覆盖负向牌逆位")

    def test_bundled_source_coverage(self):
        sources = (SKILL / "references/sources.yaml").read_text(encoding="utf-8")
        ids = set(re.findall(r"^- id: (\w+)$", sources, re.M))
        self.assertTrue({"zhouyi", "waite", "heart_sutra", "diamond_sutra", "daodejing", "web"} <= ids)
        for file in ("references/eastern/hexagrams.json", "references/tarot/tarot-78.json"):
            cards = engine.load(file)
            self.assertEqual(len(cards), 64 if "hexagrams" in file else 78)
            self.assertTrue(all(card["source_id"] in ids for card in cards))

    def test_scope_boundary(self):
        # Check operational material; source audit and research legitimately discuss exclusions.
        paths = [SKILL / "SKILL.md", *list((SKILL / "references").rglob("concepts.md")),
                 *list((SKILL / "references").rglob("symbols.md"))]
        excluded = "\u4f0a\u65af\u5170"  # review boundary without incorporating the term into operational cards
        self.assertTrue(all(excluded not in p.read_text(encoding="utf-8") for p in paths))

    def test_date_and_calendar_provenance(self):
        self.assertEqual(self.one["date"]["gregorian"], "2026-09-23")
        self.assertEqual(self.one["date"]["ganzhi"]["day"], "庚子")
        self.assertEqual(len(self.one["systems"]["yijing"]["lines_bottom_up"]), 6)


if __name__ == "__main__":
    unittest.main()
