import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { Client } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';

const client=new Client({name:'daymix-test',version:'1.0.0'});
const transport=new StdioClientTransport({command:process.execPath,args:[fileURLToPath(new URL('./stdio.mjs',import.meta.url))]});
try{
  await client.connect(transport);
  const tools=await client.listTools();
  const card=tools.tools.find(tool=>tool.name==='get_daily_card');
  assert.ok(card);
  assert.equal(card._meta?.ui,undefined,'stdio core must not require MCP Apps UI');
  const result=await client.callTool({name:'get_daily_card',arguments:{date:'2026-09-23',timezone:'Asia/Shanghai',user_id:'demo'}});
  assert.equal(result.structuredContent.schema,'daymix/2');
  assert.match(result.content[0].text,/今日总结/);
  assert.match(result.content[0].text,/https:\/\/ebible.org/);
  const bad=await client.callTool({name:'get_daily_card',arguments:{date:'2026-09-23',timezone:'Invalid/Zone'}});
  assert.equal(bad.isError,true);
  assert.ok(!JSON.stringify(bad).includes('Traceback'));
  console.log('MCP stdio: discovery, full ledger, text sources and graceful errors OK');
}finally{await client.close()}
