# Publishing version 0.1.0

The source of truth is `skills/wanxiangli/`. Do not edit a generated ZIP or maintain another Skill tree.

1. Run `python3 -m unittest discover -s tests -v` and `python3 tools/build_release.py` from the repository root. The tests execute the unpacked Skill without site-packages and confirm explicit failure if both dependency sources are absent.
2. Verify `git status --short` is clean and the manifest, changelog, and annotated tag all say `0.1.0` / `v0.1.0`.
3. Push the reviewed commit and tag: `git push origin main v0.1.0` (or merge a reviewed release branch before tagging).
4. On GitHub, create a release from tag `v0.1.0` and attach `dist/wanxiangli-skill.zip` and `dist/wanxiangli-plugin.zip`. ZIPs are excluded from Git; use the archive assets, not a binary commit.
5. Confirm both assets are downloadable and match the locally built SHA-256 hashes. Product-side ChatGPT Skills upload and permissions still require a supported environment; local archive tests do not establish those capabilities.

The Skill ZIP has exactly one top-level `wanxiangli/` folder. The plugin ZIP contains `plugin.json` at its root with `skills/wanxiangli/` and the compatibility manifest. Neither archive contains an installation ID or other local configuration.
