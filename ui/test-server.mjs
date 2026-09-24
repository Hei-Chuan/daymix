import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { fileURLToPath } from 'node:url';
const freePort=()=>new Promise((resolve,reject)=>{const sock=createServer().listen(0,'127.0.0.1',()=>{const port=sock.address().port;sock.close(()=>resolve(port))});sock.on('error',reject)});
const port=await freePort();
const server=spawn(process.execPath,[fileURLToPath(new URL('./server.mjs',import.meta.url))],{env:{...process.env,PORT:String(port)},stdio:['ignore','ignore','pipe']});
let ready=false;server.stderr.on('data',data=>{if(String(data).includes('Daymix MCP:'))ready=true});
const url=`http://127.0.0.1:${port}/mcp`;
async function call(id,method,params){const response=await fetch(url,{method:'POST',headers:{'content-type':'application/json',accept:'application/json, text/event-stream'},body:JSON.stringify({jsonrpc:'2.0',id,method,params})});if(response.status!==200)throw Error(`MCP ${response.status}: ${await response.text()}`);return (await response.json()).result}
try{
 for(let n=0;!ready&&n<50;n++)await new Promise(ok=>setTimeout(ok,100));assert.ok(ready,'server did not start');
 const tools=await call(1,'tools/list',{});const tool=tools.tools.find(t=>t.name==='get_daily_card');assert.ok(tool);
 assert.equal(tool._meta.ui.resourceUri,'ui://daymix/card-v2.2.html');
 const result=await call(2,'tools/call',{name:'get_daily_card',arguments:{date:'2026-09-23',timezone:'Asia/Shanghai',user_id:'demo'}});
 assert.equal(result.structuredContent.schema,'daymix/2');assert.match(result.content[0].text,/今日总结/);
 const resource=await call(3,'resources/read',{uri:tool._meta.ui.resourceUri});assert.equal(resource.contents[0].mimeType,'text/html;profile=mcp-app');
 assert.ok(resource.contents[0].text.includes('<script type="module">'));
 console.log('MCP: tool discovery, complete ledger, text fallback and UI resource OK');
}finally{server.kill();}
