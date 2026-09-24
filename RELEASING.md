# Releasing Daymix

1. Run `python -m unittest discover -s tests -v`; inspect v1 and v2.1 golden replay, corpus records, and v2.2 determinism.
2. Run `npm ci --prefix ui && npm run build --prefix ui && npm test --prefix ui`. Verify the `get_daily_card` result and `ui://daymix/card-v2.2.html` resource; disclosure must not call the server again.
3. Run `python tools/build_release.py`. `dist/daymix-skill.zip` has one `daymix/` root. `dist/daymix-plugin.zip` includes the Skill, Python CLI, MCP server and UI bundle. Neither ZIP deploys a public HTTPS service or installs itself in ChatGPT.
4. Review [corpus completeness](CORPUS_COMPLETENESS.md), [source rights](SOURCES.md), [research limits](RESEARCH_V22.md), religious policy, third-party notices, and changelog. New source snapshots require a version and replay fixture.
5. Tag or announce only after checks. A clickable ChatGPT card requires a reachable HTTPS MCP server connected to the account and a host-side UI test; a local `127.0.0.1` port is a development endpoint.
