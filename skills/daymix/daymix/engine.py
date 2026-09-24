"""Daymix v2.2: stable signs, expanded sourced corpora, and reality overlay."""
from __future__ import annotations

from datetime import date

from . import legacy_v21 as old
from . import v1

SCHEMA = 'daymix/2'
CAST_VERSION = 'v2.2'
SEED_VERSION = old.SEED_VERSION
DATA_VERSION = 'daoism-wikisource-1334973+christian-pairs-40-v1'
ROOT = old.ROOT
load = old.load
yijing = old.yijing
tarot = old.tarot
astrology = old.astrology
buddhism = old.buddhism
stoicism = old.stoicism
stream = old.stream
choose = old.choose


def daoism(day: date, tz: str, person: str):
    signs = load('daoism/verified-signs-v2.2.json')
    record = signs[choose(stream(day, tz, person, 'daoism.sign.v2.2'), len(signs))]
    historical = dict(record['historical'])
    grade = historical['grade']
    tone = {'上上': 1, '中上': 1, '中平': 0, '平平': 0,
            '中下': -1, '下下': -1}.get(grade, 0)
    # The daily layer is explicitly an editorial prompt, not a source gloss.
    short = ('把这首古签当作今天的提问，先看清手边真实的条件。'
             if historical['uncertainty'] else
             '借这首古签停一停：今天哪一步值得认真对待？')
    reflection = '把能核实、能行动的一件事写下来；签诗不保证结果。'
    return {
        'kind': 'historical_sign_modern_daily_draw', 'number': record['number'],
        'id': record['id'], 'historical': historical,
        'daymix': {'short_reading': short, 'reflection': reflection},
        'title': f"{historical['label']}·{historical['title']}",
        'grade': grade, 'verse': historical['verse'], 'reading': short,
        'source_url': historical['source_url'], 'tone': tone,
        'corpus_size': len(signs), 'historical_corpus_size': 365,
        'selection': '在已收录的365签中独立确定性抽取；十二时和五行只是原书编排，并非每日抽取仪轨。',
        'source_ids': ['xuan_zhen'],
    }


def christianity(day: date, tz: str, person: str):
    pool = load('christianity/watchwords-v2.2.json')
    item = dict(pool[choose(stream(day, tz, person, 'christianity.watchword.v2.2'), len(pool))])
    item.update(
        kind='daily_text_reflection',
        method='借鉴摩拉维亚弟兄会旧约 Watchword 配新约经文的方法；Daymix 独立选段并预先按主题编配，非官方序列或私人启示。',
        version='经节按公版 World English Bible 核对；中文转述与默想为项目原创。',
        reference=item['ot']['reference'],
        paraphrase=item['ot']['paraphrase'],
        pool_size=len(pool),
    )
    return item


def make(day: date, tz: str, person: str, weather=None, context=None):
    cal = v1.calendar(day, tz)
    four = {'yijing': yijing(day, tz, person), 'tarot': tarot(day, tz, person),
            'daoism': daoism(day, tz, person), 'astrology': astrology(day, tz)}
    three = {'buddhism': buddhism(day, tz, person),
             'christianity': christianity(day, tz, person),
             'stoicism': stoicism(four)}
    rating = old.synthesis(four)
    primary = v1.load('references/eastern/hexagrams.json')[four['yijing']['primary']['id'] - 1]
    dos, donts = v1.pick_actions(cal, primary)
    corrected = v1.reality(dos, donts, day, weather)
    focus = v1.unique([four['yijing']['primary']['theme'], four['yijing']['changed']['theme'],
                       '审势' if rating['conflict'] else '温故'])[:3]
    action = corrected['effective_dos'][0] if corrected['effective_dos'] else '处理手头事务'
    summary = (f'今天先复盘错题，再{action}。' if context == '备考'
               else f'今天先{action}，留意现实条件。')
    return {'schema': SCHEMA, 'cast_version': CAST_VERSION, 'seed_version': SEED_VERSION,
            'data_version': DATA_VERSION, 'date': cal, 'rating': rating,
            'four_signs': four, 'three_lenses': three, 'dos': dos, 'donts': donts,
            'focus': focus, 'reality': corrected, 'summary': {'text': summary},
            'personalization': {'context': context}}


def card(v):
    f, l, d, r = v['four_signs'], v['three_lenses'], v['date'], v['reality']
    c = l['christianity']
    return '\n'.join((
        f"Daymix · 今天呢｜{d['gregorian'][5:]} · {d['lunar']}",
        f"今天抽到 · {v['rating']['rating']}　{' · '.join(v['focus'])}",
        '宜　' + ' · '.join(r['effective_dos'][:2]),
        '不太建议　' + ' · '.join(r['effective_donts'][:2]),
        '四象',
        f"〉儒家·易　{f['yijing']['primary']['name']} → {f['yijing']['changed']['name']}",
        f"〉塔罗　{f['tarot']['name']} · {f['tarot']['orientation']}",
        f"〉道教　{f['daoism']['title']} · {f['daoism']['grade'] or '未标品第'}",
        f"〉星象　月亮{f['astrology']['positions']['moon']['zodiac_sign']} · 相位{len(f['astrology']['aspects'])}项",
        '三镜', f"〉佛教　今日察「{l['buddhism']['focus']}」",
        f"〉基督宗教　{c['ot']['reference']} ↔ {c['nt']['reference']}",
        '〉斯多葛　可控：行动',
        '〉现实复核　' + ('行动建议有调整' if r['adjustments'] else '暂无修正'),
        '今天先做　' + v['summary']['text'],
    ))


def detail(v, section):
    aliases = {'道家': 'daoism', '道教': 'daoism', '基督宗教': 'christianity'}
    key = aliases.get(section, section.lower())
    if key in ('all', '全部'):
        return '\n\n'.join(detail(v, k) for k in (*v['four_signs'], *v['three_lenses'], 'reality'))
    if key == 'daoism':
        x = v['four_signs']['daoism']; h = x['historical']; modern = x['daymix']
        note = '；'.join(h['uncertainty']) if h['uncertainty'] else '源页未记录字段异常；尚未与影印本逐字校勘。'
        return (f"道教｜第{x['number']}签 · {x['title']} · {h['grade'] or '未标品第'}\n"
                f"原签诗：{h['verse']}\n今天可以这样想：{modern['short_reading']}\n"
                f"{modern['reflection']}\n{x['selection']}\n版本：{h['edition']}\n"
                f"校录提示：{note}\n出处：{h['source_url']}")
    if key == 'christianity':
        x = v['three_lenses']['christianity']; ot, nt = x['ot'], x['nt']
        return (f"基督宗教｜旧约 {ot['reference']} · 新约 {nt['reference']}\n"
                f"旧约原创转述：{ot['paraphrase']}\n新约原创转述：{nt['paraphrase']}\n"
                f"今天想一想：{x['reflection']}\n{x['pairing']}\n{x['method']}\n"
                f"出处：{ot['source_url']}；{nt['source_url']}")
    return old.detail(v, section)
