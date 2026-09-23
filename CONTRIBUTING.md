# Contributing / 参与贡献

## Before a pull request

1. Keep the project a single Skill. Describe an existing problem or a bounded improvement; do not promise new methods in the README before implementing and testing them.
2. For **every proposed religious, philosophical, calendrical, or divinatory source**, include: title, author or attribution, date or period, stable URL, license or public-domain basis and jurisdiction if relevant, why it belongs in the allowed scope, intended use (`adapted`, `reference_only`, `runtime_lookup`, or `bundled`), and which files depend on it. Record these fields in `skills/wanxiangli/references/sources.yaml` and update `SOURCES.md`.
3. If the license is uncertain, do not distribute the text, modern translation, image, or dataset. “Found online” is not a license. Unattributed internet claims do not belong in core references.
4. Follow [RELIGIOUS_CONTENT_POLICY.md](RELIGIOUS_CONTENT_POLICY.md): preserve context and attribution, do not impersonate religious authorities or target traditions or adherents. Proposals outside the project content boundary will not be accepted.
5. For changes affecting selection, scoring, or reality correction, retain separation between raw symbols and action advice. Add a test that would fail if the relevant invariant broke; run `python3 -m unittest discover -s tests -v`.
6. Update both README files when user-visible behaviour changes. Give a reproducible example and disclose limitations. Keep dependency versions and acknowledgements accurate.

Maintainers may ask for revised wording, more precise sources, or a narrower change before merging. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) during discussion.

## 提交前

新增宗教、哲学、历法或占卜资料时，必须提交：标题、作者或传统归属、年代、URL、许可证或公版依据（必要时说明地区）、与项目范围的关系、预期用途及受影响文件。先更新 `skills/wanxiangli/references/sources.yaml` 和 `SOURCES.md`。版权不清的全文、现代译文、图片与数据集不得打包；没有来源的“网上说法”不进入核心资料。

遵守[宗教内容规范](RELIGIOUS_CONTENT_POLICY.md)，不冒充宗教权威、不攻击任何传统或信徒，也不提交超出内容范围的资料。修改推演或现实修正规则时，要保证原始象与行动建议分层，补充有意义的测试。用户能看到的变化需同步更新两份 README，准确写出已实现能力与限制。
