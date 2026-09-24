# Daymix Agent 兼容性 / Agent compatibility

核对日期：2026-09-24。`supported` 表示本仓库实际跑过端到端测试；`MCP only` 表示目标宿主有官方 MCP 接入说明，但尚未在该宿主验证 Daymix；`experimental` 表示标准接入路径已确认，目标宿主实测待完成；`unverified` 表示产品身份、接入方式或实测证据不足。**协议测试不等于各平台上线。**

## 唯一实现与已验证范围

| 能力 | 状态 | 证据和边界 |
| --- | --- | --- |
| Python engine、365 条道教录文、40 组基督宗教配对、v1/v2.1/v2.2 replay | supported | Python 测试及固定复算；语料校勘限制见 [CORPUS_COMPLETENESS.md](CORPUS_COMPLETENESS.md)。 |
| Canonical Agent Skill | supported | 仅维护 [skills/daymix/SKILL.md](skills/daymix/SKILL.md)；发行 ZIP 从该目录生成。目标宿主的 Skill 发现仍需逐个实测。 |
| `get_daily_card`：stdio 与 Streamable HTTP | supported | Node MCP 客户端本地测试工具发现、完整 `daymix/2`、文本、来源、错误；两种传输调用同一 `ui/core.mjs`。 |
| ChatGPT MCP Apps 展开卡 | experimental | 本地 HTTP 工具和 UI 资源测试通过；未做 ChatGPT 线上连接、移动端及深色模式宿主实测。关闭 UI 时核心工具继续可用。 |

## 宿主平台

| 宿主 | 状态 | 官方接入依据；Daymix 实测情况 |
| --- | --- | --- |
| ChatGPT | experimental | [OpenAI MCP 工具先行、UI 可选](https://developers.openai.com/apps-sdk/build/mcp-server)；本地 Apps 资源测试通过，线上宿主未验证。 |
| Codex | experimental | [OpenAI Skills](https://developers.openai.com/plugins/concepts/skills) 和 [MCP 工具](https://developers.openai.com/plugins/build/mcp-server)；本环境能发现 Daymix Skill，尚未对本次发行包做宿主端到端测试。 |
| OpenCode | experimental | [Agent Skills](https://opencode.ai/docs/skills) 和 [stdio / 远程 MCP](https://opencode.ai/v2/docs/mcp-servers) 有官方说明；未在 OpenCode 中调用。注意版本不同的 MCP 配置层级不同，不随仓库提交平台配置副本。 |
| Qwen Code | experimental | [Agent Skills](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/) 与 [stdio / HTTP MCP](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/) 有官方说明；未在 Qwen Code 中调用。本项目尚未发布或验证 Qwen Extension。 |
| Qoder IDE / CLI | experimental | [Skill 导入](https://docs.qoder.com/qoder/skills)、[CLI 项目 Skill](https://docs.qoder.com/cli/Skills)、[MCP](https://docs.qoder.com/user-guide/chat/model-context-protocol) 有官方说明；未在 Qoder 中调用。 |
| QCoder | unverified | “QCoder”指向多个不同产品；尚未锁定本需求对应的官方客户端与配置规范。仅准备通用 MCP，绝不自造 QCoder Skill 格式。 |
| 火山引擎 AgentKit | MCP only | [官方 MCP 接入说明](https://docs.volcengine.com/docs/agentkit/MCP_Overview?lang=zh)；未创建资源或在云端验证。 |
| 豆包、Trae、扣子 | unverified | 本次没有足够证据证明各产品当前版本能直接接入本服务；优先尝试 HTTPS Remote MCP，不声称已支持，也不发布专用 Skill。 |
| 其他 Agent Skills / MCP 宿主 | unverified | 可按标准接口尝试接入，须分别验证工具发现、一次调用、完整结果及来源。 |

## 安装与部署入口

- 只需 Skill：将 `dist/daymix-skill.zip` 内唯一 `daymix/` 目录安装到宿主**官方** Skill 目录，或链接到仓库的 `skills/daymix/`。不要手工维护多份源文件。
- 本地 MCP：在仓库根目录先运行 `npm ci --prefix ui`，将 `node <仓库绝对路径>/ui/stdio.mjs` 配为 stdio 命令。Node.js 24 和 Python 3.12 是 CI 验证版本；`DAYMIX_PYTHON` 可指定 Python 路径。stdout 只供 MCP 协议使用。
- HTTP MCP：`npm run start --prefix ui` 默认监听 `127.0.0.1:3000/mcp`，`GET /healthz` 返回进程存活状态；部署验收还须实际调用工具。`DAYMIX_UI=0` 关闭 Apps 资源，只保留通用工具。跨机器接入需要 HTTPS 反向代理；非本机监听必须设置 `DAYMIX_MCP_TOKEN`，并通过 `Authorization: Bearer ...` 传入。令牌只放环境变量或密钥管理器，不写进仓库。公开部署仍须在入口层设置 TLS、访问控制和速率限制。
- `get_daily_card` 输入：可选 `date`（ISO 日期）、`timezone`（默认 `Asia/Shanghai`）、非敏感 `user_id`、`context=备考`。输出：`structuredContent` 的固定 `daymix/2` 字段，及含来源 URL 的文本卡。错误以 MCP `isError` 返回。安装包版本 **2.3.0** 不改变 `cast_version=v2.2` 或 `data_version`，旧日签不漂移。
- 网站：`python web/app.py` 在本机启动同一 Python engine 的轻量 API 和前端；匿名身份、历史及同步码保存在网站专用 SQLite adapter 中。`Dockerfile` 可部署该服务，但本仓库尚无公开服务 URL；公网部署需要 HTTPS、持久化数据库及入口限流。Codex Sites 当前不能直接运行 Python engine，不能把静态前端误报成已上线的网站。

English: One Python engine, one corpus, one canonical Skill, and one MCP tool serve every host. Local protocol tests pass for stdio and Streamable HTTP. Host-specific rows above are deliberately conservative; no paid cloud resources were created.
