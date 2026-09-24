# Third-party notices / 第三方软件声明

The packages below retain their own MIT licenses. Their source is bundled unchanged under `skills/daymix/vendor/` so that the Skill can run when an approved Python environment lacks these packages. The project's MIT license does not replace their copyright notices. Exact source-tree digests and versions are in `skills/daymix/vendor/versions.json`.

下列程序包保留各自的 MIT 许可证。为支持缺少预装包的 Python 环境，Skill 在 `skills/daymix/vendor/` 中分发未经修改的固定版本。项目自身的 MIT 许可不替代第三方版权声明；版本与源码树摘要见 `skills/daymix/vendor/versions.json`。

| 软件包 | 版本 | 用途 | 上游项目 | 许可文件 | 是否修改 |
| --- | --- | --- | --- | --- | --- |
| `lunar-python` (`lunar_python`) | 1.4.8 | 农历、干支、节气与黄历计算 | [6tail/lunar-python](https://github.com/6tail/lunar-python) | [`lunar-python-LICENSE`](skills/daymix/vendor/licenses/lunar-python-LICENSE) | 否 |
| `astronomy-engine` (`astronomy`) | 2.1.19 | v2 地心位置与相位；v1 太阳黄经与月日夹角 | [cosinekitty/astronomy](https://github.com/cosinekitty/astronomy) | [`astronomy-engine-LICENSE`](skills/daymix/vendor/licenses/astronomy-engine-LICENSE) | 否 |

The script first uses an installed package **only if its version matches** the pin; otherwise it loads the bundled copy. No third-party religious text, tarot illustrations, or research-only material is added by this distribution change.

## MCP Apps JavaScript 打包文件（v2）

`ui/dist/card.html` 由 `ui/card.js` 构建，版本记录在 `ui/package-lock.json`。运行时直接使用 `@modelcontextprotocol/ext-apps`、`@modelcontextprotocol/server`、`zod`；`esbuild` 和 `jsdom` 用于构建与测试。这五项直接依赖的安装包元数据标为 MIT。生成的卡片保留打包器输出的许可注释，但并非完整的许可证清单；单独再分发 UI 前须核对锁文件和实际安装依赖的声明。本次改动不影响 v1 内置 Python 源码树摘要。
