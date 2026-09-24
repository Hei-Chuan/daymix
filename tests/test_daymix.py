"""Version boundaries, corpus provenance, and Daymix output contracts."""
import hashlib
import json
import re
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/daymix'))
from daymix import engine, legacy_v21


def digest(value):
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


class DaymixTests(unittest.TestCase):
    day = date(2026, 9, 23)

    def test_v21_replay_is_unchanged(self):
        fixtures = (
            (self.day, 'Asia/Shanghai', 'demo', '66486fb85593fb3c58fba9ef095093013e6266d0b513602323870733f94f3238'),
            (self.day + timedelta(days=1), 'Asia/Shanghai', 'demo', 'd8f12834f406bb4445e5ba5c91c6175928c77d4295bf22e65ffb843259e0fb6d'),
            (self.day, 'UTC', 'compat', 'f21dac854c4529ee59efce5628b8559ba16f54e157ee0429536992cbf8666888'),
        )
        for day, timezone, person, expected in fixtures:
            with self.subTest(day=day, timezone=timezone, person=person):
                self.assertEqual(digest(legacy_v21.make(day, timezone, person)), expected)

    def test_new_version_is_deterministic_and_branded(self):
        value = engine.make(self.day, 'Asia/Shanghai', 'demo')
        self.assertEqual(value, engine.make(self.day, 'Asia/Shanghai', 'demo'))
        self.assertEqual((value['schema'], value['cast_version']), ('daymix/2', 'v2.2'))
        self.assertIn('daoism-wikisource', value['data_version'])
        self.assertTrue(engine.card(value).startswith('Daymix · 今天呢'))
        self.assertNotIn('万象历', engine.card(value))
        self.assertNotEqual(value, engine.make(self.day, 'UTC', 'demo'))
        self.assertNotEqual(value, engine.make(self.day, 'Asia/Shanghai', 'other'))
        for key in ('yijing', 'tarot', 'astrology'):
            self.assertEqual(value['four_signs'][key], legacy_v21.make(self.day, 'Asia/Shanghai', 'demo')['four_signs'][key])

    def test_reality_only_changes_effective_action(self):
        base = engine.make(self.day, 'Asia/Shanghai', 'demo')
        rain = {'description': '暴雨红色预警', 'hazard': 'storm',
                'source': '气象机构', 'observed_at': '2026-09-23T10:00:00+08:00'}
        changed = engine.make(self.day, 'Asia/Shanghai', 'demo', rain)
        for key in ('four_signs', 'three_lenses', 'rating', 'dos', 'donts'):
            self.assertEqual(base[key], changed[key])
        self.assertNotEqual(base['reality'], changed['reality'])

    def test_daoism_complete_with_per_page_provenance(self):
        signs = engine.load('daoism/verified-signs-v2.2.json')
        self.assertEqual(len(signs), 365)
        self.assertEqual([x['number'] for x in signs], list(range(1, 366)))
        self.assertEqual(len({x['id'] for x in signs}), 365)
        self.assertEqual(len({x['historical']['source_url'] for x in signs}), 365)
        for item in signs:
            h = item['historical']
            self.assertTrue(all(h[field] for field in ('label', 'title', 'verse', 'source', 'source_url', 'edition')))
            self.assertTrue(h['source_revision'] > 0)
            self.assertTrue(h['source_url'].startswith('https://zh.wikisource.org/wiki/'))
            self.assertIsInstance(h['uncertainty'], list)
        self.assertEqual({x['number'] for x in signs if x['historical']['uncertainty']}, {57, 269, 297, 327})
        self.assertEqual(len(engine.load('daoism/verified-signs.json')), 7)

    def test_christian_pairs_are_complete_and_sourced(self):
        pairs = engine.load('christianity/watchwords-v2.2.json')
        self.assertEqual(len(pairs), 40)
        self.assertEqual(len({x['id'] for x in pairs}), 40)
        for pair in pairs:
            self.assertTrue(pair['theme'] and pair['reflection'] and pair['pairing'])
            self.assertEqual(pair['source_ids'], ['web', 'moravian'])
            for testament in ('ot', 'nt'):
                item = pair[testament]
                self.assertRegex(item['reference'], r'^[1-3]? ?[A-Za-z]+ \d+:\d+$')
                self.assertTrue(item['paraphrase'] and len(item['paraphrase']) < 100)
                self.assertRegex(item['source_url'], r'^https://ebible\.org/engwebp/[A-Z0-9]+\.htm#V\d+$')
        self.assertEqual(len(engine.load('christianity/watchwords.json')), 12)
        selected = engine.make(self.day, 'Asia/Shanghai', 'demo')['three_lenses']['christianity']
        self.assertEqual(selected['pool_size'], 40)
        self.assertIn('旧约', engine.detail(engine.make(self.day, 'Asia/Shanghai', 'demo'), 'christianity'))


if __name__ == '__main__':
    unittest.main()
