import { App } from '@modelcontextprotocol/ext-apps';
const root=document.querySelector('#card');
const state=()=>window.openai?.widgetState?.privateContent?.open ?? [];
const el=(tag,cls,text)=>{const x=document.createElement(tag);if(cls)x.className=cls;if(text!=null)x.textContent=String(text);return x};
const add=(parent,tag,cls,text)=>{const x=el(tag,cls,text);parent.append(x);return x};
const section=(name)=>add(root,'div','section',name);
function sourceBlock(parent,lines,links=[]){const d=add(parent,'details','nested');add(d,'summary','','查看出处 / 考据');const wrap=add(d,'div','inside');for(const line of lines)add(wrap,'p','',line);for(const [label,url] of links){const p=add(wrap,'p','source');const a=add(p,'a','',label);a.href=url;a.rel='noopener noreferrer';a.target='_blank'}return d}
function panel(key,title,hint,render,source){const d=add(root,'details','panel');d.dataset.key=key;const s=add(d,'summary');add(s,'span','label',title);add(s,'span','hint',hint);const content=add(d,'div','inside');render(content);if(source)sourceBlock(content,source.lines,source.links);return d}
function p(parent,text){add(parent,'p','',text)}
function persist(){const open=[...root.querySelectorAll('details.panel[open]')].map(x=>x.dataset.key);window.openai?.setWidgetState?.({privateContent:{open},modelContent:`《Daymix · 今天呢》已展开栏目：${open.join('、')||'无'}`})}
function render(v){if(!v||!['daymix/2','wanxiangli/2'].includes(v.schema))return;root.replaceChildren();const f=v.four_signs,l=v.three_lenses,r=v.reality,d=v.date;
 add(root,'div','eyebrow','Daymix · 今天呢');add(root,'div','date',`${d.gregorian} · ${d.lunar} · ${d.ganzhi.day}日`);
 add(root,'h1','rating',`今天抽到 · ${v.rating.rating}`);add(root,'div','focus',v.focus.join(' · '));
 const actions=add(root,'div','actions');for(const [label,list] of [['宜',r.effective_dos],['不太建议',r.effective_donts]]){const box=add(actions,'div','action');add(box,'strong','',label);add(box,'span','',list.slice(0,2).join(' · '))}
 const controls=add(root,'div','controls');for(const [name,open] of [['全部展开',true],['全部收起',false]]){const b=add(controls,'button','',name);b.type='button';b.onclick=()=>{root.querySelectorAll('details').forEach(x=>x.open=open);persist()}}
 section('四象 · 象征原始记录');const y=f.yijing;
 panel('yijing','儒家·易',`${y.primary.name} → ${y.changed.name}`,box=>{p(box,`六爻自下而上：${y.line_values_bottom_up.join(' / ')}；动爻：${y.moving_lines.join('、')||'无'}`);p(box,`卦辞：${y.primary.judgment}`);for(const t of y.line_texts)p(box,`${t.position}爻：${t.text}`);p(box,y.reading)}, {lines:[y.method,'《周易》古层与儒家《易传》及后世义理分属不同历史层次；程序不声称复原西周筮法。'],links:[['查阅卦辞与爻辞',y.primary.source_url]]});
 const t=f.tarot;panel('tarot','塔罗',`${t.name} · ${t.orientation}`,box=>{p(box,`基础短义：${t.upright}`);p(box,`本日牌义：${t.meaning}`);p(box,t.reading)}, {lines:['Rider–Waite–Smith 图像体系：Pamela Colman Smith 绘制，A. E. Waite 撰写说明。短义为项目原创；不附牌图。'],links:[['Waite 公版文本','https://en.wikisource.org/wiki/The_Pictorial_Key_to_the_Tarot']]});
 const q=f.daoism;panel('daoism','道教',`${q.title} · ${q.grade||'未标品第'}`,box=>{p(box,`原签诗：${q.verse}`);p(box,`今天可以这样想：${q.daymix?.short_reading||q.reading}`);if(q.daymix)p(box,q.daymix.reflection)}, {lines:[q.selection,`入库 ${q.corpus_size} / ${q.historical_corpus_size} 条；${q.historical?.uncertainty?.join('；')||'源页未记录字段异常，尚未与影印本逐字校勘。'}`],links:[['《玄真灵应宝签》签页',q.source_url]]});
 const a=f.astrology;panel('astrology','希腊化星象',`月亮${a.positions.moon.zodiac_sign} · ${a.aspects.length}项相位`,box=>{p(box,`天文位置（${a.instant_utc}）：`);for(const x of Object.values(a.positions))p(box,`${x.name}：黄经 ${x.longitude_deg}° · ${x.zodiac_sign} ${x.degree_in_sign}°`);p(box,`主要相位：${a.aspects.map(z=>`${a.positions[z.a].name}${z.aspect}${a.positions[z.b].name}（${z.orb_deg}°）`).join('；')||'无阈值内相位'}`);p(box,a.reading)}, {lines:[a.frame,a.orb_policy,'经纬计算属于天文学，星象释义属于历史文化解释。'],links:[['托勒密《四书》','https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Ptolemy/Tetrabiblos/home.html']]});
 section('三镜 · 自省与约束');const b=l.buddhism;panel('buddhism','佛教',`今日察「${b.focus}」`,box=>{p(box,b.observation);p(box,`修正方向：${b.repair}`)}, {lines:[b.method,'《占察经》的文本归属和接受史存在争议；此处不测疾病、生死或业报。'],links:[['《占察善恶业报经》卷上','https://zh.wikisource.org/wiki/占察善惡業報經/卷01']]});
 const c=l.christianity;panel('christianity','基督宗教',c.ot?`${c.ot.reference} ↔ ${c.nt.reference}`:`今日箴言 · ${c.reference}`,box=>{if(c.ot){p(box,`旧约原创转述：${c.ot.paraphrase}`);p(box,`新约原创转述：${c.nt.paraphrase}`)}else p(box,`原创中文转述：${c.paraphrase}`);p(box,`今天想一想：${c.reflection}`)}, {lines:[c.method,c.pairing||'独立经节池，不复制摩拉维亚教会每日序列；不代表任何教会。'],links:[['旧约 WEB',c.ot?.source_url||'https://ebible.org/engwebp/'],['新约 WEB',c.nt?.source_url||'https://ebible.org/engwebp/'],['Moravian Daily Watchwords','https://www.moravian.org.uk/daily-watchwords/what-are-the-daily-watchwords']]});
 const s=l.stoicism;panel('stoicism','斯多葛','可控：行动',box=>{p(box,`你能控制：${s.can_control.join('、')}`);p(box,`你不能控制：${s.cannot_control.join('、')}`);p(box,`今日操练：${s.exercise}`)}, {lines:['《爱比克泰德·手册》第1、32节关于可控之事及占问的讨论；本镜不进入评分。'],links:[['Enchiridion','https://classics.mit.edu/Epictetus/epicench.html']]});
 section('现实与总评');panel('reality','现实复核',r.adjustments.length?'行动建议已调整':'暂无修正',box=>{p(box,`原宜：${r.original_dos.join('、')}`);p(box,`有效宜：${r.effective_dos.join('、')}`);p(box,`有效忌：${r.effective_donts.join('、')}`);p(box,r.adjustments.join('；')||'未取得需要修正的现实资料；没有天气数据不意味着天气安全。')},{lines:['现实仅调整有效行动，不改原始卦、牌、签、天象与象征评级。'],links:[]});
 const rate=v.rating;panel('synthesis','评分依据',`${rate.score} · ${rate.formula_version}`,box=>{p(box,rate.formula);for(const [key,item] of Object.entries(rate.contributions))p(box,`${key}: ${item.value>0?'+':''}${item.value} · ${item.basis}`);if(rate.conflict)p(box,'四象存在分歧，应保留各自观点。')});
 add(root,'div','closing',`今日总结　${v.summary.text}`);add(root,'div','notice','象征评级仅供自省；现实信息优先。');
 const saved=new Set(state());for(const x of root.querySelectorAll('details.panel'))x.open=saved.has(x.dataset.key);
}
root.addEventListener('toggle',e=>{if(e.target?.matches?.('details.panel'))persist()},true);
const app=new App({name:'Daymix Card',version:'2.2.0'});
app.ontoolresult=result=>{if(result.structuredContent)render(result.structuredContent)};
app.connect().catch(()=>{root.querySelector('.empty')?.replaceChildren('无法连接卡片宿主；可使用 CLI 或 Skill 文本卡。')});
// Host compatibility alias; the shared MCP Apps bridge above remains the primary path.
if(['daymix/2','wanxiangli/2'].includes(window.openai?.toolOutput?.schema))render(window.openai.toolOutput);
