# Changelog

## 0.1.0 — 2026-09-23

- Publish one canonical Skill at `skills/wanxiangli/` for local Codex discovery and standalone Skill upload.
- Provide a portable plugin manifest with consistent Codex compatibility metadata.
- Bundle unmodified `lunar-python` 1.4.8 and `astronomy-engine` 2.1.19 under their MIT licenses as a fallback to matching external installations.
- Add `--identity-mode hosted` to avoid persisting an installation identifier in ephemeral hosted environments. The existing daily seed algorithm and local behavior remain unchanged.
- Build and validate separate Skill and plugin ZIP archives; test isolated execution and explicit failure without dependencies.
