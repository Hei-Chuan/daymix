const $=id=>document.getElementById(id);
const TOKEN_KEY='daymix.device.v1';
let token=localStorage.getItem(TOKEN_KEY);
let historyItems=[];

async function api(path,{method='GET',body,authorized=true}={}){
  const headers={};
  if(body!==undefined)headers['Content-Type']='application/json';
  if(authorized&&token)headers.Authorization=`Bearer ${token}`;
  const response=await fetch(path,{method,headers,body:body===undefined?undefined:JSON.stringify(body),cache:'no-store'});
  const data=await response.json();
  if(!response.ok)throw Error(data.error||'连接暂时没有回应');
  return data;
}
async function session(){
  if(token)return;
  const data=await api('/api/session',{method:'POST',body:{},authorized:false});
  token=data.token;
  localStorage.setItem(TOKEN_KEY,token);
}
function element(tag,className,text){const node=document.createElement(tag);if(className)node.className=className;if(text!==undefined)node.textContent=String(text);return node}
function row(parent,label,text){const p=element('p');p.append(element('strong','',label+'　'),document.createTextNode(text||'—'));parent.append(p);return p}
function detail(title){const outer=element('details');outer.append(element('summary','',title));const body=element('div','detail-body');outer.append(body);return [outer,body]}
function sourceUrls(value,found=new Map()){
  if(Array.isArray(value)){for(const item of value)sourceUrls(item,found)}
  else if(value&&typeof value==='object')for(const [key,item] of Object.entries(value)){
    if(key==='source_url'&&typeof item==='string'&&item.startsWith('https://')){
      try{const url=new URL(item);found.set(url.href,url.hostname)}catch{}
    }else sourceUrls(item,found);
  }
  return found;
}
function link(url,label){const a=element('a','',label);a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a}
function showLedger(ledger,{historical=false}={}){
  const region=$('card-region');region.replaceChildren();region.hidden=false;
  document.body.classList.add('has-card');
  $('intro-title').textContent=historical?'那天掉落了什么？':'今天掉落了什么？';
  const card=element('article','daily-card is-new');
  const top=element('div','card-overline');
  top.append(element('span','',`${ledger.date.gregorian} · ${ledger.date.lunar||''}`),element('span','saved',historical?'那天的卡':'今日掉落'));
  card.append(top);
  const rating=element('div','rating-row');rating.append(element('span','rating-mark','✦'),element('h2','',ledger.rating.rating));card.append(rating);
  card.append(element('p','keywords',(ledger.focus||[]).join(' · ')));
  const actions=element('div','action-grid');
  for(const [heading,items,kind] of [['宜',ledger.reality.effective_dos,'do'],['不太建议',ledger.reality.effective_donts,'dont']]){
    const box=element('div',`action-box ${kind}`);box.append(element('h3','',heading),element('p','',(items||[]).slice(0,3).join(' · ')||'照顾好眼前的事'));actions.append(box);
  }
  card.append(actions);
  const step=element('div','first-step');step.append(element('strong','','今天先做'),document.createTextNode(ledger.summary.text));card.append(step);
  const details=element('div','card-details');

  const [four,fourBody]=detail('四象 · 看看掉了什么');
  const f=ledger.four_signs;
  row(fourBody,'易',`${f.yijing.primary.name} → ${f.yijing.changed.name}；动爻 ${f.yijing.moving_lines.join('、')||'无'}`);
  row(fourBody,'塔罗',`${f.tarot.name} · ${f.tarot.orientation}。${f.tarot.reading||''}`);
  row(fourBody,'道教',`${f.daoism.title} · ${f.daoism.grade||'品第未标'}`);
  fourBody.append(element('p','verse',f.daoism.verse));
  if(f.daoism.historical?.uncertainty?.length)row(fourBody,'校录提示',f.daoism.historical.uncertainty.join('；'));
  row(fourBody,'星象',`月亮${f.astrology.positions.moon.zodiac_sign}；主要相位 ${f.astrology.aspects.length} 项。${f.astrology.reading||''}`);
  details.append(four);

  const [three,threeBody]=detail('三镜 · 换个角度');const lens=ledger.three_lenses;
  row(threeBody,'佛教',`今日察「${lens.buddhism.focus}」。${lens.buddhism.observation||''}`);
  const christian=lens.christianity;
  row(threeBody,'基督宗教',`${christian.ot.reference} ↔ ${christian.nt.reference}`);
  row(threeBody,'旧约转述',christian.ot.paraphrase);
  row(threeBody,'新约转述',christian.nt.paraphrase);
  row(threeBody,'反思',christian.reflection);
  row(threeBody,'斯多葛',lens.stoicism.reading||lens.stoicism.exercise||'把注意力放在可控的行动。');
  details.append(three);

  const [reality,realityBody]=detail('现实复核');
  row(realityBody,'调整',(ledger.reality.adjustments||[]).join('；')||'今天没有额外调整。');
  row(realityBody,'原始宜',(ledger.reality.original_dos||[]).join(' · '));
  row(realityBody,'原始不太建议',(ledger.reality.original_donts||[]).join(' · '));
  details.append(reality);

  const [sources,sourcesBody]=detail('来源');const list=element('div','source-list');
  const named=[['易原文',f.yijing.primary.source_url],['道教签页',f.daoism.source_url],['旧约经节',christian.ot.source_url],['新约经节',christian.nt.source_url]];
  const used=new Set();
  for(const [label,url] of named)if(url&&url.startsWith('https://')&&!used.has(url)){list.append(link(url,`${label} ↗`));used.add(url)}
  for(const [url,host] of sourceUrls(ledger))if(!used.has(url))list.append(link(url,`${host} ↗`));
  list.append(link('https://github.com/Hei-Chuan/daymix/blob/main/SOURCES.md','项目来源与权利说明 ↗'));
  sourcesBody.append(list);details.append(sources);
  card.append(details,element('p','card-note','这是一张象征阅读卡，供娱乐、文化探索与自省；不预测现实结果。'));
  region.append(card);
  requestAnimationFrame(()=>region.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'}));
}
async function dropToday(){
  const button=$('drop-button'),status=$('status');button.disabled=true;status.textContent='正在打开今天这张…';
  try{
    await session();
    const timezone=Intl.DateTimeFormat().resolvedOptions().timeZone||'Asia/Shanghai';
    const {ledger}=await api('/api/drop',{method:'POST',body:{timezone}});
    showLedger(ledger);status.textContent='';
  }catch(error){status.textContent=error.message;button.disabled=false}
}
function renderHistory(items){
  const list=$('history-list');list.replaceChildren();
  if(!items.length){
    const empty=element('div','history-empty');empty.append(element('strong','','还没有以前。'),element('p','','今天这张会成为第一张。'));list.append(empty);return;
  }
  for(const item of items){
    const button=element('button','history-item');button.type='button';
    button.append(element('span','',item.date),element('span','',`${item.rating}　↗`));
    button.addEventListener('click',async()=>{
      button.disabled=true;
      try{const {ledger}=await api(`/api/drop?date=${encodeURIComponent(item.date)}`);$('history-dialog').close();showLedger(ledger,{historical:true})}
      catch(error){$('sync-status').textContent=error.message;button.disabled=false}
    });list.append(button);
  }
}
async function refreshHistory(){historyItems=(await api('/api/history')).items;renderHistory(historyItems)}
async function openHistory(){
  $('history-dialog').showModal();$('history-list').replaceChildren(element('p','','正在翻看…'));
  try{await session();await refreshHistory()}
  catch(error){$('history-list').replaceChildren(element('p','',error.message+'。可以用同步码恢复。'))}
}
async function createSync(){
  const status=$('sync-status'),button=$('sync-create');button.disabled=true;status.textContent='';
  try{await session();const {code}=await api('/api/sync',{method:'POST',body:{}});$('sync-code').textContent=code;$('sync-code-wrap').hidden=false;status.textContent='新同步码已生成，旧码现已失效。'}
  catch(error){status.textContent=error.message}finally{button.disabled=false}
}
async function restoreSync(){
  const status=$('sync-status'),button=$('sync-restore'),code=$('sync-input').value.trim();
  if(!code){status.textContent='请先粘贴同步码。';return}
  if(historyItems.length&& !confirm('恢复后，此设备会切换到同步码对应的历史。请先保存当前历史的同步码。继续吗？'))return;
  button.disabled=true;status.textContent='正在恢复…';
  try{
    const data=await api('/api/restore',{method:'POST',body:{code},authorized:false});
    token=data.token;localStorage.setItem(TOKEN_KEY,token);$('sync-input').value='';$('sync-code-wrap').hidden=true;
    status.textContent='已恢复，之前的日子回来了。';await refreshHistory();
  }catch(error){status.textContent=error.message}finally{button.disabled=false}
}

$('drop-button').addEventListener('click',dropToday);
$('history-open').addEventListener('click',openHistory);
$('history-close').addEventListener('click',()=>$('history-dialog').close());
$('history-dialog').addEventListener('click',event=>{if(event.target===$('history-dialog'))$('history-dialog').close()});
$('sync-create').addEventListener('click',createSync);
$('sync-restore').addEventListener('click',restoreSync);
$('sync-copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('sync-code').textContent);$('sync-status').textContent='已复制。'}catch{$('sync-status').textContent='请手动复制同步码。'}});
session().catch(error=>{$('status').textContent=error.message});
