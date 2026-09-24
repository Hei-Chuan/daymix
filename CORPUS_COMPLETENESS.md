# Daymix v2.2 corpus completeness

Snapshot checked 2026-09-24. Runtime data is committed and offline; `tools/import_daoism.py` is an explicit maintenance importer, never called during a daily draw.

## 《玄真靈應寶籤》

- [Wikisource index](https://zh.wikisource.org/wiki/玄真靈應寶籤) lists 365 distinct linked pages: 12 time groups × 30, then 5 elements. All 365 pages were fetched. `verified-signs-v2.2.json` holds 365 nonempty poems, original page labels, titles, source grades when present, page URLs and MediaWiki revision IDs.
- `number` is **Daymix's 1–365 index ordinal** in the Wikisource table of contents. The original labels (`子時第一`, etc.) are retained separately. It is not an original sequential 1–365 number printed on every sign.
- Four entries require source or print collation: **57** (`丑時二十七`) has unusual grade `有得`; **269** (`申時二十九`) lacks a grade; **297** (`酉時二十七`) has no paragraph break between poem and prose, so the first four punctuated clauses were segmented as verse; **327** (`戌時二十七`) has unusual grade `一下`. The unusual or missing grades receive neutral score; no grade was invented. Each issue is stored in the entry's `uncertainty` array.
- Missing index entries: **0**. Independently verified against a scanned *Zhengtong Daozang* print: **0/365**. The Wikisource page's own edition claim is recorded, not presented as a completed independent textual collation. Original long prose glosses are not bundled or treated as predictions.
- The daily `daymix` interpretation is deliberately a short **generic editorial reflection**, not a 365-entry critical commentary. The historical poem and modern prompt live in different fields in the generated result. Twelve-time and five-element grouping is historical arrangement, not evidence for Daymix's draw method.

## Christian paired texts

- `watchwords-v2.2.json` contains **40 fixed Old Testament–New Testament thematic pairs**. All **80 WEB chapter URLs and verse IDs** were checked against the publisher's [public-domain WEB edition](https://ebible.org/engwebp/). The links establish reference existence; the original Chinese paraphrases and the thematic connection remain editorial interpretations, not an official doctrinal review.
- Daymix draws one **prepaired record** with a deterministic channel. It never independently draws a random Old Testament text and then a random New Testament text. [Moravian Archives](https://www.moravianchurcharchives.org/general/anniversary-of-moravian-daily-texts/) describes an Old Testament watchword selected by lot from a much larger pool and a New Testament passage selected to accompany it. Daymix borrows this broad shape, not their current annual sequence or texts.
- v2.1's 12-item Old Testament-only pool remains frozen for replay. No modern copyrighted Chinese Bible translation or official Moravian daily sequence is bundled.

## Version boundary

`v1` and `v2.1` have frozen replay paths. `v2.2` records `schema`, `cast_version`, `seed_version`, and `data_version` in every ledger; the new corpora never masquerade as v2.1. A change to any source snapshot needs a new declared data/cast version and replay fixture.
