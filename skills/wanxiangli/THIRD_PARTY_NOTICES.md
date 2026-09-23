# Third-party notices / 第三方软件声明

The packages below retain their own MIT licenses. Their source is bundled unchanged under `vendor/` so that the Skill can run when an approved Python environment lacks these packages. The project's MIT license does not replace their copyright notices. Exact source-tree digests and versions are in `vendor/versions.json`.

下列程序包保留各自的 MIT 许可证。为支持缺少预装包的 Python 环境，Skill 在 `vendor/` 中分发未经修改的固定版本。项目自身的 MIT 许可不替代第三方版权声明；版本与源码树摘要见 `vendor/versions.json`。

| Package | Version | Purpose | Upstream | License notice | Modified |
| --- | --- | --- | --- | --- | --- |
| `lunar-python` (`lunar_python`) | 1.4.8 | Lunar, sexagenary, solar-term and almanac calculations | [6tail/lunar-python](https://github.com/6tail/lunar-python) | [`lunar-python-LICENSE`](vendor/licenses/lunar-python-LICENSE) | No |
| `astronomy-engine` (`astronomy`) | 2.1.19 | Solar longitude and Moon–Sun angle | [cosinekitty/astronomy](https://github.com/cosinekitty/astronomy) | [`astronomy-engine-LICENSE`](vendor/licenses/astronomy-engine-LICENSE) | No |

The script first uses an installed package **only if its version matches** the pin; otherwise it loads the bundled copy. No third-party religious text, tarot illustrations, or research-only material is added by this distribution change.
