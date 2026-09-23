"""Wanxiangli v2: independent historical signs, reflective lenses and reality overlay."""
from __future__ import annotations
import hashlib
import json
from datetime import date, datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from . import v1

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 'wanxiangli/2'
CAST_VERSION = 'v2.1'
SEED_VERSION = 'v2'
LABELS = v1.LABELS
TRIGRAMS = {x['lines_bottom_up'][:3]:x['lower'] for x in v1.load('references/eastern/hexagrams.json') if x['lower']==x['upper']}
SIGNS = '白羊 金牛 双子 巨蟹 狮子 处女 天秤 天蝎 射手 摩羯 水瓶 双鱼'.split()
BODIES = [('sun','太阳','Sun'),('moon','月亮','Moon'),('mercury','水星','Mercury'),('venus','金星','Venus'),('mars','火星','Mars'),('jupiter','木星','Jupiter'),('saturn','土星','Saturn')]
ASPECTS = [(0,'合相'),(60,'六分'),(90,'四分'),(120,'三分'),(180,'对冲')]


def load(path):
    return json.loads((ROOT / 'references' / path).read_text(encoding='utf-8'))


def stream(day:date, tz:str, person:str, channel:str):
    """Domain-separated SHA-256 counter stream; a new channel never advances another."""
    base = '\0'.join((SEED_VERSION, day.isoformat(), tz, person, channel)).encode('utf-8')
    counter = 0
    while True:
        yield int.from_bytes(hashlib.sha256(base + b'\0' + counter.to_bytes(8,'big')).digest(), 'big')
        counter += 1


def choose(words, n):
    if n <= 0: raise ValueError('empty choice')
    limit = (1 << 256) - ((1 << 256) % n)
    for value in words:
        if value < limit: return value % n


def yarrow_line(words):
    """49 stalks; three changes. The deterministic split substitutes for hand separation."""
    stalks = 49
    steps = []
    for _ in range(3):
        # The right heap must still contain a stalk after hanging one aside.
        left = choose(words, stalks - 2) + 1
        right = stalks - left
        right -= 1  # hang one from the right heap
        a = left % 4 or 4
        b = right % 4 or 4
        removed = 1 + a + b
        stalks -= removed
        steps.append({'split_left':left, 'removed':removed, 'remaining':stalks})
    if stalks not in (24,28,32,36): raise AssertionError('invalid yarrow simulation')
    return stalks // 4, steps


def yijing(day, tz, person):
    index = {h['lines_bottom_up']:h for h in v1.load('references/eastern/hexagrams.json')}
    texts = {x['id']:x for x in load('eastern/zhouyi-text.json')}
    lines, procedures = [], []
    for i in range(6):
        value, steps = yarrow_line(stream(day,tz,person,f'yijing.line.{i+1}'))
        lines.append(value); procedures.append(steps)
    bits = ''.join('1' if x in (7,9) else '0' for x in lines)
    changed = ''.join('1' if x in (6,7) else '0' for x in lines)
    original, future = index[bits], index[changed]
    moving = [i+1 for i,x in enumerate(lines) if x in (6,9)]
    text = texts[original['id']]
    return {'kind':'historical_cast_simulation','method_version':'yarrow-v2.1','method':'《系辞》大衍章的后世蓍筮程序化模拟；分堆由独立确定性字节流代替',
            'line_values_bottom_up':lines,'procedure':procedures,'moving_lines':moving,
            'primary':{'id':original['id'],'name':original['name'],'theme':original['theme'],'judgment':text['judgment'],'source_url':text['source_url']},
            'line_texts':[{'position':n,'text':text['lines'][n-1]} for n in moving],
            'changed':{'id':future['id'],'name':future['name'],'theme':future['theme']},
            'reading':f"由「{original['theme']}」观察处境，动爻提示变化；「{future['theme']}」仅作后续参照。",
            'tone':original['tone'], 'source_ids':['xici','zhouyi','zhu_xi']}


def tarot(day,tz,person):
    cards=load('tarot/tarot-v2.json')
    item=dict(cards[choose(stream(day,tz,person,'tarot.card'),len(cards))])
    item['orientation']='正位' if choose(stream(day,tz,person,'tarot.orientation'),2)==0 else '逆位'
    # Reversal qualifies the theme; it does not logically invert good into bad.
    item['meaning']=item['upright'] if item['orientation']=='正位' else item['reversed']
    item['tone']=item['tone'] if item['orientation']=='正位' else min(0,item['tone'])
    item['reading']=f"留意「{item['meaning']}」，将它用于提问而非预测。"
    item['source_ids']=['waite']
    return item


def daoism(day,tz,person):
    signs=load('daoism/verified-signs.json')
    item=dict(signs[choose(stream(day,tz,person,'daoism.sign'),len(signs))])
    item.update(kind='historical_sign_modern_daily_draw',corpus_size=len(signs),historical_corpus_size=365,
                selection='从已核对的签文子集中独立确定性抽取；签号的时辰只是原书编排，不按当前时辰抽取',
                tone=1 if item['grade']=='上上' else -1 if item['grade']=='下下' else 0,source_ids=['xuan_zhen'])
    return item


def astrology(day,tz):
    astro=v1.dependency('astronomy','astronomy-engine','2.1.19')
    instant=datetime.combine(day,time(12),ZoneInfo(tz)).astimezone(timezone.utc)
    moment=astro.Time.Make(instant.year,instant.month,instant.day,instant.hour,instant.minute,instant.second)
    positions={}
    for key,name,body in BODIES:
        if key=='sun': lon=astro.SunPosition(moment).elon
        elif key=='moon': lon=astro.EclipticGeoMoon(moment).lon
        else: lon=astro.Ecliptic(astro.GeoVector(getattr(astro.Body,body),moment,True)).elon
        positions[key]={'name':name,'longitude_deg':round(lon,3),'zodiac_sign':SIGNS[int(lon//30)%12],
                        'degree_in_sign':round(lon%30,3)}
    aspects=[]
    for i,(a,_,_) in enumerate(BODIES):
        for b,_,_ in BODIES[i+1:]:
            sep=abs(positions[a]['longitude_deg']-positions[b]['longitude_deg'])
            sep=min(sep,360-sep)
            for angle,label in ASPECTS:
                orb=abs(sep-angle)
                if orb<=6: aspects.append({'a':a,'b':b,'aspect':label,'angle_deg':angle,'separation_deg':round(sep,3),'orb_deg':round(orb,3)});break
    aspects.sort(key=lambda x:(x['orb_deg'],x['a'],x['b']))
    # A declared modern editorial convention, not an ancient universal orb or scientific forecast.
    salient=[x for x in aspects if (x['a'] in ('sun','moon') or x['b'] in ('sun','moon'))]
    cues=[(1 if x['aspect'] in ('六分','三分') else -1 if x['aspect'] in ('四分','对冲') else 0) for x in salient]
    tone=1 if sum(cues)>0 else -1 if sum(cues)<0 else 0
    return {'kind':'astronomical_observation_and_historical_symbolism','instant_utc':instant.isoformat(),
            'frame':'地心视黄经、当日黄道坐标；热带黄道十二宫，每宫30°','positions':positions,
            'aspects':aspects,'orb_policy':'每相位±6°，仅为本项目显示阈值，非统一古典规则',
            'reading':'相位为古典星象的象征语言；天体位置本身是计算事实，不推出个人行为的因果结论。',
            'tone':tone,'source_ids':['astronomy_engine','ptolemy']}


def buddhism(day,tz,person):
    focus=['身','口','意'][choose(stream(day,tz,person,'buddhism.focus'),3)]
    prompts={'身':('留意今天的身体行动是否妥当。','做错可修正，疲惫也应休息。'),
             '口':('说话前核实事实，留意是否伤人。','有失言就澄清或道歉。'),
             '意':('观察冲动与执着，不急于把念头当事实。','先停顿，再作选择。')}
    return {'kind':'reflection','focus':focus,'observation':prompts[focus][0], 'repair':prompts[focus][1],
            'method':'借鉴《占察善恶业报经》身口意分类的现代自省提示；未模拟木轮仪轨或判断业报',
            'source_ids':['zhancha']}


def christianity(day,tz,person):
    pool=load('christianity/watchwords.json'); item=dict(pool[choose(stream(day,tz,person,'christianity.watchword'),len(pool))])
    item.update(kind='daily_text_reflection',method='借鉴 Moravian Daily Texts 每日经文方法；非其官方序列，非私人启示',
                version='原创中文转述；经节按 World English Bible 核对',source_ids=['moravian','web'])
    return item


def stoicism(four):
    return {'kind':'control_audit','can_control':['行动','判断','准备','回应'],
            'cannot_control':['最终结果','他人行为','已经发生的事','偶然条件'],
            'exercise':'选择今天可做的一步，完成后再评估结果。',
            'reading':'即使四象的提示有启发，也不把外在结果当作个人意志能保证的事。',
            'source_ids':['epictetus']}


def synthesis(four):
    contributions={k:{'value':four[k]['tone'],'basis':{'yijing':'本卦主题的项目短评','tarot':'牌义与正逆位的项目短评','daoism':'所选历史签的原有品第映射','astrology':'日月相关主要相位的显示约定'}[k]}
                   for k in ('yijing','tarot','daoism','astrology')}
    score=sum(x['value'] for x in contributions.values())
    index=0 if score<=-3 else 1 if score<=-1 else 2 if score==0 else 3 if score<=2 else 4
    return {'score':score,'rating':LABELS[index],'scale':LABELS,'contributions':contributions,
            'formula_version':'symbolic-v2.1','formula':'四象各取 -1/0/+1 并列相加；-4..4 映射五档。仅为公开的编辑性象征标尺，不是预测概率。',
            'conflict':min(x['value'] for x in contributions.values())<0<max(x['value'] for x in contributions.values())}


def make(day:date,tz:str,person:str,weather=None,context=None):
    cal=v1.calendar(day,tz)
    four={'yijing':yijing(day,tz,person),'tarot':tarot(day,tz,person),
          'daoism':daoism(day,tz,person),'astrology':astrology(day,tz)}
    three={'buddhism':buddhism(day,tz,person),'christianity':christianity(day,tz,person),'stoicism':stoicism(four)}
    rating=synthesis(four)
    primary=v1.load('references/eastern/hexagrams.json')[four['yijing']['primary']['id']-1]
    dos,donts=v1.pick_actions(cal,primary)
    corrected=v1.reality(dos,donts,day,weather)
    keywords=v1.unique([four['yijing']['primary']['theme'],four['yijing']['changed']['theme'],
                        '审势' if rating['conflict'] else '温故'])[:3]
    action=corrected['effective_dos'][0] if corrected['effective_dos'] else '处理手头事务'
    summary=(f'今天先复盘错题，再{action}。' if context=='备考' else f'今天先{action}，留意现实条件。')
    return {'schema':SCHEMA,'cast_version':CAST_VERSION,'date':cal,'rating':rating,
            'four_signs':four,'three_lenses':three,'dos':dos,'donts':donts,
            'focus':keywords,'reality':corrected,'summary':{'text':summary},
            'personalization':{'context':context}}


def card(v):
    f=v['four_signs']; l=v['three_lenses']; d=v['date']; r=v['reality']
    return '\n'.join((f"万象历 · {d['gregorian'][5:]}｜{d['lunar']} · {d['ganzhi']['day']}日",
       f"今日 · {v['rating']['rating']}　{' · '.join(v['focus'])}",
       '宜　'+' · '.join(r['effective_dos'][:2]),'忌　'+' · '.join(r['effective_donts'][:2]),
       '四象',f"〉儒家·易　{f['yijing']['primary']['name']} → {f['yijing']['changed']['name']}",
       f"〉塔罗　{f['tarot']['name']} · {f['tarot']['orientation']}",
       f"〉道教　{f['daoism']['title']} · {f['daoism']['grade']}",
       f"〉星象　月亮{f['astrology']['positions']['moon']['zodiac_sign']} · 相位{len(f['astrology']['aspects'])}项",
       '三镜',f"〉佛教　今日察「{l['buddhism']['focus']}」",
       f"〉基督宗教　今日箴言 · {l['christianity']['reference']}",
       '〉斯多葛　可控：行动','〉现实复核　'+('有调整' if r['adjustments'] else '未见需调整的条件'),
       '今日总结　'+v['summary']['text']))


def detail(v,section):
    f=v['four_signs']; l=v['three_lenses']; r=v['reality']; k=section.lower()
    aliases={'易理':'yijing','儒家·易':'yijing','佛家':'buddhism','道家':'daoism','星象':'astrology',
             '塔罗':'tarot','道教':'daoism','佛教':'buddhism','基督宗教':'christianity','斯多葛':'stoicism','现实修正':'reality','现实复核':'reality'}
    k=aliases.get(section,k)
    if k=='all' or section=='全部':return '\n\n'.join(detail(v,x) for x in (*f,*l,'reality'))
    if k=='yijing':
        x=f[k]; lines='；'.join(f"{t['position']}爻：{t['text']}" for t in x['line_texts']) or '无动爻'
        return f"儒家·易｜{x['primary']['name']} → {x['changed']['name']}\n六爻：{x['line_values_bottom_up']}；动爻：{x['moving_lines'] or '无'}\n卦辞：{x['primary']['judgment']}\n{lines}\n{x['reading']}\n出处：{x['primary']['source_url']}；{x['method']}"
    if k=='tarot':
        x=f[k];return f"塔罗｜{x['name']}·{x['orientation']}\n基础短义：{x['upright']}；逆位提示：{x['reversed']}\n{x['reading']}\n依据：Waite 1910；中文短义为项目原创。"
    if k=='daoism':
        x=f[k];return f"道教｜{x['title']}·{x['grade']}\n原签诗：{x['verse']}\n今日解读：{x['reading']}\n{x['selection']}\n出处：{x['source_url']}"
    if k=='astrology':
        x=f[k]; positions='；'.join(f"{p['name']}{p['zodiac_sign']}{p['degree_in_sign']}°（黄经{p['longitude_deg']}°）" for p in x['positions'].values())
        aspects='；'.join(f"{x['positions'][a['a']]['name']}{a['aspect']}{x['positions'][a['b']]['name']}（容许度{a['orb_deg']}°）" for a in x['aspects']) or '无阈值内主要相位'
        return f"星象｜{x['instant_utc']}\n天文位置：{positions}\n主要相位：{aspects}\n{x['reading']}\n{x['orb_policy']}"
    if k=='buddhism':
        x=l[k];return f"佛教｜今日察「{x['focus']}」\n{x['observation']}\n修正：{x['repair']}\n{x['method']}"
    if k=='christianity':
        x=l[k];return f"基督宗教｜{x['reference']}\n原创转述：{x['paraphrase']}\n默想：{x['reflection']}\n{x['method']}；不预测未来，不代表教会。"
    if k=='stoicism':
        x=l[k];return f"斯多葛｜可控：{'、'.join(x['can_control'])}\n不可控：{'、'.join(x['cannot_control'])}\n今日操练：{x['exercise']}"
    if k=='reality':
        return f"现实复核｜原宜：{'、'.join(r['original_dos'])}；原忌：{'、'.join(r['original_donts'])}\n实际宜：{'、'.join(r['effective_dos'])}；实际忌：{'、'.join(r['effective_donts'])}\n"+('；'.join(r['adjustments']) if r['adjustments'] else '未取得需要修正的现实条件；天气数据缺席不代表天气安全。')
    raise ValueError(f'未知栏目：{section}')
