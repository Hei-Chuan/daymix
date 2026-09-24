#!/usr/bin/env python3
"""Portable CLI with explicit v1, v2.1, and v2.2 replay."""
import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from daymix import engine, legacy_v21, v1

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Preserve import-level access to old engine for external v1 consumers.
make_v1, card_v1, detail_v1 = v1.make, v1.card, v1.detail

def main():
    p=argparse.ArgumentParser(description='Daymix · 今天呢（支持 v1 / v2.1 历史复算）')
    p.add_argument('--engine',choices=['v1','v2','v2.1','v2.2'],default='v2.2')
    p.add_argument('--date');p.add_argument('--timezone',default='Asia/Shanghai')
    p.add_argument('--user-id');p.add_argument('--identity-mode',choices=['local','hosted'],default='local')
    p.add_argument('--context',choices=['备考']);p.add_argument('--weather-json')
    p.add_argument('--format',choices=['json','card'],default='card')
    p.add_argument('--expand',help='yijing/tarot/daoism/astrology/buddhism/christianity/stoicism/reality/all；可用中文别名')
    a=p.parse_args()
    try:
        today=date.fromisoformat(a.date) if a.date else datetime.now(ZoneInfo(a.timezone)).date()
        weather=json.loads(Path(a.weather_json).read_text(encoding='utf-8')) if a.weather_json else None
        if weather and not all(weather.get(x) for x in ('description','source','observed_at','hazard')):
            raise ValueError('天气需 description、source、observed_at、hazard')
        person=a.user_id or ('guest' if a.identity_mode=='hosted' else v1.installation_id())
        if a.engine=='v1':
            v=v1.make(today,a.timezone,person,weather,a.context)
            section={'yijing':'易理','tarot':'塔罗','astrology':'星象','buddhism':'佛家','daoism':'道家','christianity':'基督宗教','reality':'现实修正','all':'全部'}.get(a.expand,a.expand)
            output=(v1.detail(v,section)+'\n今日总结：'+v['summary']) if section else (json.dumps(v,ensure_ascii=False,indent=2) if a.format=='json' else v1.card(v))
        else:
            selected=legacy_v21 if a.engine in ('v2','v2.1') else engine
            v=selected.make(today,a.timezone,person,weather,a.context)
            output=(selected.detail(v,a.expand)+'\n今日总结：'+v['summary']['text']) if a.expand else (json.dumps(v,ensure_ascii=False,indent=2) if a.format=='json' else selected.card(v))
        print(output);return 0
    except (ValueError,RuntimeError,KeyError,AssertionError) as exc:
        print(f'Daymix：{exc}',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
