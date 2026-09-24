import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';
const freePort=()=>new Promise((resolve,reject)=>{const sock=createServer().listen(0,'127.0.0.1',()=>{const port=sock.address().port;sock.close(()=>resolve(port))});sock.on('error',reject)});
const port=await freePort();
const server=spawn(process.execPath,[fileURLToPath(new URL('./server.mjs',import.meta.url))],{env:{...process.env,PORT:String(port)},stdio:['ignore','ignore','pipe']});
let ready=false;server.stderr.on('data',data=>{if(String(data).includes('Daymix MCP:'))ready=true});
const url=`http://127.0.0.1:${port}/mcp`;
async function call(id,method,params){const response=await fetch(url,{method:'POST',headers:{'content-type':'application/json',accept:'application/json, text/event-stream'},body:JSON.stringify({jsonrpc:'2.0',id,method,params})});if(response.status!==200)throw Error(`MCP ${response.status}: ${await response.text()}`);return (await response.json()).result}
try{
 for(let n=0;!ready&&n<50;n++)await new Promise(ok=>setTimeout(ok,100));assert.ok(ready,'server did not start');
 const health=await fetch(`http://127.0.0.1:${port}/healthz`);assert.equal(health.status,200);assert.equal((await health.json()).status,'ok');
 const tools=await call(1,'tools/list',{});const tool=tools.tools.find(t=>t.name==='get_daily_card');assert.ok(tool);
 assert.equal(tool.outputSchema.properties.cast_version.const,'v2.2');
 assert.equal(tool._meta.ui.resourceUri,'ui://daymix/card-v2.2.html');
 const result=await call(2,'tools/call',{name:'get_daily_card',arguments:{date:'2026-09-23',timezone:'Asia/Shanghai',user_id:'demo'}});
 assert.equal(result.structuredContent.schema,'daymix/2');assert.match(result.content[0].text,/今日总结/);
 assert.match(result.content[0].text,/https:\/\/ebible.org/);
 const stdio=new Client({name:'daymix-parity-test',version:'1.0.0'});
 try{
   await stdio.connect(new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('./stdio.mjs',import.meta.url))]}));
   const same=await stdio.callTool({name:'get_daily_card',arguments:{date:'2026-09-23',timezone:'Asia/Shanghai',user_id:'demo'}});
   assert.deepEqual(same.structuredContent,result.structuredContent);
   assert.deepEqual(same.content,result.content);
 }finally{await stdio.close()}
 const invalid=await call(4,'tools/call',{name:'get_daily_card',arguments:{date:'2026-09-23',timezone:'Invalid/Zone'}});
 assert.equal(invalid.isError,true);assert.ok(!JSON.stringify(invalid).includes('Traceback'));
 const oversize=await fetch(url,{method:'POST',headers:{'content-type':'application/json'},body:'x'.repeat(65537)});assert.equal(oversize.status,413);
 const resource=await call(3,'resources/read',{uri:tool._meta.ui.resourceUri});assert.equal(resource.contents[0].mimeType,'text/html;profile=mcp-app');
 assert.ok(resource.contents[0].text.includes('<script type="module">'));
 console.log('MCP: tool discovery, complete ledger, text fallback and UI resource OK');
}finally{server.kill();}
const headlessPort=await freePort();
const headless=spawn(process.execPath,[fileURLToPath(new URL('./server.mjs',import.meta.url))],{env:{...process.env,PORT:String(headlessPort),DAYMIX_UI:'0'},stdio:['ignore','ignore','pipe']});
let headlessReady=false;headless.stderr.on('data',data=>{if(String(data).includes('Daymix MCP:'))headlessReady=true});
try{
 for(let n=0;!headlessReady&&n<50;n++)await new Promise(ok=>setTimeout(ok,100));assert.ok(headlessReady);
 const response=await fetch(`http://127.0.0.1:${headlessPort}/mcp`,{method:'POST',headers:{'content-type':'application/json',accept:'application/json, text/event-stream'},body:JSON.stringify({jsonrpc:'2.0',id:5,method:'tools/list',params:{}})});
 assert.equal(response.status,200);const tools=(await response.json()).result.tools;
 assert.equal(tools.find(t=>t.name==='get_daily_card')._meta?.ui,undefined);
}finally{headless.kill()}
