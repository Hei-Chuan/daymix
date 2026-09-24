#!/usr/bin/env python3
"""Import the public-domain historical verses from Wikisource with page revisions.

The index ordering is preserved. Source anomalies are recorded, never repaired
silently. Run deliberately; release builds use the committed snapshot offline.
"""
import json
import re
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'skills/daymix/references/daoism/verified-signs-v2.2.json'
API = 'https://zh.wikisource.org/w/api.php'
BOOK = '玄真靈應寶籤'
USER_AGENT = 'DaymixSourceAudit/2.2 (https://github.com/Hei-Chuan/daymix)'


def pages(titles):
    response = requests.get(API, params={
        'action': 'query', 'prop': 'revisions', 'rvprop': 'content|ids|timestamp',
        'rvslots': 'main', 'titles': '|'.join(titles), 'format': 'json',
        'formatversion': 2,
    }, headers={'User-Agent': USER_AGENT}, timeout=45)
    response.raise_for_status()
    result = response.json()['query']['pages']
    if any('missing' in page or 'revisions' not in page for page in result):
        raise ValueError('a source page is missing')
    return result


def content(page):
    return page['revisions'][0]['slots']['main']['content']


def parse(page, ordinal):
    raw = content(page)
    match = re.match(r'^===([^=]+)===[ \t]*\n+', raw)
    if not match:
        raise ValueError(f'missing heading: {page["title"]}')
    heading = [field.strip() for field in re.split(r'[\u3000\t]+', match.group(1)) if field.strip()]
    if len(heading) not in (2, 3):
        raise ValueError(f'unexpected heading: {page["title"]}: {heading}')
    label, title = heading[:2]
    grade = heading[2] if len(heading) == 3 else None
    body = raw[match.end():].strip()
    paragraphs = re.split(r'\n\s*\n', body)
    uncertainty = []
    if len(paragraphs) == 1:
        # This page joins four verse lines and a prose gloss with no separator.
        # Four punctuation-terminated clauses constitute the verse on this page.
        pieces = re.findall(r'[^，。！？]+[，。！？]', paragraphs[0])
        if len(pieces) < 8:
            raise ValueError(f'cannot isolate verse: {page["title"]}')
        verse = ''.join(pieces[:8])
        uncertainty.append('源页诗文与后文未分段；仅按前四句标点切分，待底本复核。')
    else:
        verse = paragraphs[0].strip()
    if not verse or len(verse) > 150:
        raise ValueError(f'unexpected verse: {page["title"]}')
    if grade is None:
        uncertainty.append('源页标题未标品第；保持空值，不推断。')
    elif grade not in {'上上', '中上', '中平', '平平', '中下', '下下'}:
        uncertainty.append('源页品第写法异于常见分级；原样保留，不推断象征分值。')
    if label not in page['title']:
        raise ValueError(f'heading/page mismatch: {page["title"]}')
    return {
        'number': ordinal,
        'id': f'xz-{ordinal:03d}',
        'historical': {
            'label': label, 'title': title, 'grade': grade, 'verse': verse,
            'group': '五行' if ordinal > 360 else '十二时',
            'source': '《正統道藏》正一部《玄真靈應寶籤》；維基文庫校錄',
            'source_url': 'https://zh.wikisource.org/wiki/' + quote(page['title']),
            'edition': '維基文庫所标《正統道藏》正一部底本；未与影印本逐字校勘',
            'source_revision': page['revisions'][0]['revid'],
            'uncertainty': uncertainty,
        },
    }


def main():
    index = pages([BOOK])[0]
    names = re.findall(r'^\*\[\[/([^|\]]+)', content(index), re.M)
    if len(names) != 365 or len(set(names)) != 365:
        raise ValueError(f'index is not 365 unique entries: {len(names)}')
    found = {}
    for start in range(0, len(names), 50):
        for page in pages([f'{BOOK}/{name}' for name in names[start:start + 50]]):
            found[page['title']] = page
    if len(found) != 365:
        raise ValueError(f'fetched {len(found)} distinct pages')
    records = []
    for n, name in enumerate(names, 1):
        title = f'{BOOK}/{name}'
        if title not in found:
            raise ValueError(f'missing index target: {title}')
        records.append(parse(found[title], n))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(records)} signs; {sum(bool(x["historical"]["uncertainty"]) for x in records)} with recorded uncertainty; index revision {index["revisions"][0]["revid"]}')


if __name__ == '__main__':
    main()
