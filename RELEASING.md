# Releasing

1. Run `python3 -m unittest discover -s tests -v` and confirm the v1 golden digest, v2 reproducibility and data checks.
2. Run `npm ci --prefix ui && npm run build --prefix ui` and test `get_daily_card` and the `ui://wanxiangli/card-v2.1.html` resource with an MCP Apps host or inspector. Compare the JSON while opening sections.
3. Run `python3 tools/build_release.py`. The Skill ZIP has one `wanxiangli/` root; the plugin source ZIP contains the server, UI bundle and Python Skill. Neither ZIP deploys a public HTTPS MCP service or connects it to ChatGPT.
4. Review `RESEARCH_V2.md`, source identifiers, third-party licenses, religious policy and the changelog for any added text or mechanics.
5. Tag only after checks; connect a reachable service and verify the card in a ChatGPT developer environment before claiming the click UI is live.
