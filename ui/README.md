# Daymix MCP Apps card

`get_daily_card` is read-only and returns the full `daymix/2` ledger once in `structuredContent`; `_meta.ui.resourceUri` is `ui://daymix/card-v2.2.html`. The HTML resource uses `text/html;profile=mcp-app`. Panels, sources, all-open and all-closed operate on the local result. The parser also accepts frozen `wanxiangli/2` ledgers for historical display. No disclosure redraws a sign or reruns the engine.

From the repository root: `npm ci --prefix ui && npm run build --prefix ui && npm test --prefix ui`; start the local server with `npm run start --prefix ui`. It binds to `127.0.0.1:3000/mcp` by default; `HOST` and `PORT` can change that. `DAYMIX_PYTHON` chooses the Python interpreter, with `WANXIANGLI_PYTHON` accepted as a legacy environment variable. Hosted mode uses a shared guest seed unless a non-sensitive alias is provided; the server does not create a private local ID.

For ChatGPT, deploy the server to a reachable HTTPS endpoint and connect its `/mcp` URL in the developer/plugin UI. The ZIP alone does not make the widget live. Before claiming an integration, invoke `get_daily_card` once, expand and collapse panels, check mobile and dark mode, and verify that the ledger and tool-call count remain unchanged. Clients without widget support can use the text fallback and CLI `--expand`.
