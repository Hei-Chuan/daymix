# Daymix MCP Apps card

`get_daily_card` is read-only and returns the full `daymix/2` ledger once in `structuredContent`; `_meta.ui.resourceUri` is `ui://daymix/card-v2.2.html`. The HTML resource uses `text/html;profile=mcp-app`. Panels, sources, all-open and all-closed operate on the local result. The parser also accepts frozen `wanxiangli/2` ledgers for historical display. No disclosure redraws a sign or reruns the engine.

Tested with Node.js 24 and Python 3.12. From the repository root: `npm ci --prefix ui && npm run build --prefix ui && npm test --prefix ui`; start the local server with `npm run start --prefix ui`. It binds to `127.0.0.1:3000/mcp` by default; `HOST` and `PORT` can change that. `DAYMIX_PYTHON` chooses the Python interpreter, with `WANXIANGLI_PYTHON` accepted as a legacy environment variable. Hosted mode uses a shared guest seed unless a non-sensitive alias is provided; the server does not create a private local ID. Tool inputs are date, timezone, optional alias, and optional study context; there is no weather input or automatic weather lookup in this server.

For ChatGPT, deploy the server to a reachable HTTPS endpoint and connect its `/mcp` URL in the developer/plugin UI. The ZIP alone does not make the widget live. This repository supplies a local development server; a public deployment must add appropriate access control and request limits at the hosting layer. Before claiming an integration, invoke `get_daily_card` once, expand and collapse panels, check mobile and dark mode, and verify that the ledger and tool-call count remain unchanged. Clients without widget support can use the text fallback and CLI `--expand`.

## 中文说明

本服务提供只读工具 `get_daily_card` 和 `ui://daymix/card-v2.2.html` 展开卡。一次调用返回完整日卡；打开栏目、查看出处、全部展开和全部收起不再次调用工具。也接受 v2.1 的旧 JSON 作历史显示。

在仓库根目录运行上方的安装、构建、测试命令，再运行 `npm run start --prefix ui`。默认只监听本机 `127.0.0.1:3000/mcp`。接口可传日期、时区、非敏感代号和“备考”条件，**不接受天气数据，也不自动查询天气**；匿名访客共享相同日签。

ChatGPT 互动卡还需要可达的 HTTPS `/mcp` 服务与宿主连接；本地 ZIP 和本机端口不能代替部署。公开部署前须在托管层配置访问控制与请求限制，并在目标宿主实际检查一次工具调用、展开收起、移动端和深色模式。无组件支持时可用文本卡或 CLI。
