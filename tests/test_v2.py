import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/wanxiangli'))
from wanxiangli import engine, v1

class V2Tests(unittest.TestCase):
    day=date(2026,9,23)
    @classmethod
    def setUpClass(cls):cls.base=engine.make(cls.day,'Asia/Shanghai','demo')

    def test_determinism_and_channel_independence(self):
        self.assertEqual(self.base,engine.make(self.day,'Asia/Shanghai','demo'))
        self.assertEqual(self.base['schema'],'wanxiangli/2')
        self.assertEqual(self.base['cast_version'],'v2.1')
        self.assertEqual(self.base['four_signs']['tarot'],engine.tarot(self.day,'Asia/Shanghai','demo'))
        self.assertNotEqual(self.base['four_signs']['tarot'],engine.tarot(self.day,'Asia/Shanghai','other'))
        other_tz=engine.make(self.day,'UTC','demo')
        self.assertNotEqual(self.base['four_signs']['yijing']['procedure'],other_tz['four_signs']['yijing']['procedure'])
        self.assertEqual(self.base['rating'],engine.make(self.day,'Asia/Shanghai','demo',context='备考')['rating'])
        self.assertEqual(self.base['four_signs'],engine.make(self.day,'Asia/Shanghai','demo',context='备考')['four_signs'])

    def test_yarrow_procedure(self):
        for n in range(48):
            x=engine.yijing(self.day+timedelta(days=n),'Asia/Shanghai','demo')
            vals=x['line_values_bottom_up']
            self.assertEqual(len(vals),6)
            self.assertTrue(set(vals)<={6,7,8,9})
            self.assertEqual(x['moving_lines'],[i+1 for i,v in enumerate(vals) if v in (6,9)])
            self.assertEqual(len(x['line_texts']),len(x['moving_lines']))
            for steps,val in zip(x['procedure'],vals):
                self.assertEqual(len(steps),3)
                for step_index,step in enumerate(steps):
                    stalks=49 if step_index==0 else steps[step_index-1]['remaining']
                    self.assertGreaterEqual(stalks-step['split_left'],2)
                self.assertIn(steps[0]['removed'],(5,9))
                self.assertTrue(all(s['removed'] in (4,8) for s in steps[1:]))
                self.assertEqual(steps[-1]['remaining'],val*4)

    def test_sources_and_corpora(self):
        h=engine.load('eastern/hexagrams.json');tx=engine.load('eastern/zhouyi-text.json')
        self.assertEqual(len(h),len(tx));self.assertEqual(len(h),64)
        self.assertEqual({x['lines_bottom_up'] for x in h},{format(i,'06b')[::-1] for i in range(64)})
        for n,(item,old) in enumerate(zip(tx,h),1):
            self.assertEqual((item['id'],old['id']),(n,n))
            self.assertEqual(len(item['lines']),6)
            self.assertTrue(item['judgment'] and all(item['lines']))
        cards=engine.load('tarot/tarot-v2.json');self.assertEqual(len(cards),78)
        self.assertFalse(any('阻滞或失衡' in c['reversed'] for c in cards))
        signs=engine.load('daoism/verified-signs.json');self.assertEqual(len(signs),7)
        self.assertTrue(all(s['verse'] and s['source_url'] and s['grade'] for s in signs))
        pool=engine.load('christianity/watchwords.json');self.assertEqual(len(pool),12)
        self.assertTrue(all(x['reference'] and x['paraphrase'] for x in pool))

    def test_astronomy_sanity_and_separate_meaning(self):
        x=self.base['four_signs']['astrology']
        self.assertEqual(len(x['positions']),7)
        self.assertTrue(all(0<=p['longitude_deg']<360 for p in x['positions'].values()))
        # 2026 autumn equinox: Sun close to the tropical Libra 0-degree boundary.
        self.assertLess(abs(x['positions']['sun']['longitude_deg']-180),2)
        for aspect in x['aspects']:
            self.assertLessEqual(aspect['orb_deg'],6)
            self.assertIn(aspect['angle_deg'],(0,60,90,120,180))

    def test_reality_context_and_no_redraw(self):
        rain={'description':'暴雨红色预警','hazard':'storm','source':'气象机构','observed_at':'2026-09-23T10:00:00+08:00'}
        changed=engine.make(self.day,'Asia/Shanghai','demo',rain,'备考')
        for key in ('four_signs','three_lenses','rating','dos','donts'):
            self.assertEqual(self.base[key],changed[key])
        self.assertEqual(self.base['reality']['original_dos'],changed['reality']['original_dos'])
        self.assertNotEqual(self.base['summary'],changed['summary'])
        snapshot=copy.deepcopy(self.base)
        for panel in ('yijing','daoism','astrology','buddhism','christianity','stoicism','all'):
            self.assertTrue(engine.detail(self.base,panel))
        self.assertEqual(self.base,snapshot)

    def test_safe_text_and_score_bound(self):
        for n in range(28):
            ledger=engine.make(self.day+timedelta(days=n),'Asia/Shanghai','demo')
            self.assertEqual(ledger['rating']['score'],sum(c['value'] for c in ledger['rating']['contributions'].values()))
            self.assertTrue(-4<=ledger['rating']['score']<=4)
            self.assertEqual(set(ledger['rating']['contributions']),set(ledger['four_signs']))
            for forbidden in ('考试必过','财富必得','死亡预测','患病预言','上帝告诉你','改运付费'):
                self.assertNotIn(forbidden,engine.card(ledger)+ledger['summary']['text'])

    def test_v1_golden_bytes(self):
        cmd=[sys.executable,str(ROOT/'scripts/wanxiangli.py'),'--engine','v1','--date','2026-09-23',
             '--timezone','Asia/Shanghai','--user-id','demo','--format','json']
        result=subprocess.check_output(cmd)
        self.assertEqual(hashlib.sha256(result).hexdigest(),'39a6225e7ff56fb303fe59ee657392db25210c0c09ba160bb2e98ce455fc7344')
        self.assertEqual(json.loads(result)['schema'],'wanxiangli/1')

if __name__=='__main__':unittest.main()
