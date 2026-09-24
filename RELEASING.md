# Releasing Daymix

1. Run `python -m unittest discover -s tests -v`; inspect v1 and v2.1 golden replay, corpus records, and v2.2 determinism.
2. Run `npm ci --prefix ui && npm run build --prefix ui && npm test --prefix ui`. Verify the common `get_daily_card` contract on stdio and HTTP, the optional `ui://daymix/card-v2.2.html` resource, and `/healthz`; disclosure must not call the server again.
3. Run `python tools/build_release.py`. `dist/daymix-skill.zip` has one `daymix/` root. `dist/daymix-plugin.zip` includes the Skill, Python CLI, MCP server and UI bundle. `dist/daymix-web.zip` includes the website, canonical engine/corpus and Dockerfile. These ZIPs do not deploy a public HTTPS service or install themselves in ChatGPT.
4. Review [compatibility statuses](COMPATIBILITY.md), [corpus completeness](CORPUS_COMPLETENESS.md), [source rights](SOURCES.md), [current design and limits](DESIGN.md), religious policy, third-party notices, and changelog. New source snapshots require a data/cast version and replay fixture; packaging alone does not.
5. Tag or announce only after checks. A clickable ChatGPT card requires a reachable HTTPS MCP server connected to the account and a host-side UI test; a local `127.0.0.1` port is a development endpoint. Add access control and request limits before exposing this development server publicly.

## 中文发布检查

按上方顺序运行 Python 测试、UI 构建与测试、发布包构建；核对 v1/v2.1 历史复算、v2.2 语料数量与来源、[语料报告](CORPUS_COMPLETENESS.md)、[权利说明](SOURCES.md)和版本号。两个 ZIP 是候选产物，不会自动在 ChatGPT 安装或部署 HTTPS MCP 服务。公开服务需先配置访问控制和请求限制，并在实际宿主检查展开卡。
