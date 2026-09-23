# v2 合参规则

1. `wanxiangli/2` 的 `four_signs` 是一次生成的原始四象；`three_lenses` 只供反思；`rating` 仅由四象得出。逐项说明评分贡献，不把象征分值当概率。
2. 展开由同一 JSON 完成。UI 使用原生折叠；CLI/Skill 无 UI 时复用 JSON 或用相同日期、时区、代号再次运行。保持 v1 seed 独立。
3. 星期与具来源的天气仅更改 `reality.effective_dos/donts`，不篡改原始象、`dos/donts`、评级。没有可信天气时不声称天气安全。备考 context 只改建议措辞。
4. 道教仅七条已核对签诗，原书365条；佛教只借身口意自省，基督宗教只借每日经文方法。都不得冒充机构认可或私人神谕。
5. 禁止疾病、死亡、灾祸或考试财富的确定预测、付费改运；真实安全信息优先。其他素材边界见 `RELIGIOUS_CONTENT_POLICY.md`。
