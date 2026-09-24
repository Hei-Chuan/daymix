import { createServer } from 'node:http';
import { Readable } from 'node:stream';
import { timingSafeEqual } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { WebStandardStreamableHTTPServerTransport } from '@modelcontextprotocol/server';
import { registerAppResource, RESOURCE_MIME_TYPE } from '@modelcontextprotocol/ext-apps/server';
import { createDaymixServer, CARD_URI } from './core.mjs';

const withUi=process.env.DAYMIX_UI!=='0';
const server=createDaymixServer({withUi});
if(withUi){
  const here=path.dirname(fileURLToPath(import.meta.url));
  registerAppResource(server,'daymix-card',CARD_URI,{mimeType:RESOURCE_MIME_TYPE},async()=>({
    contents:[{uri:CARD_URI,mimeType:RESOURCE_MIME_TYPE,text:await readFile(path.join(here,'dist/card.html'),'utf8'),_meta:{ui:{prefersBorder:true}}}]
  }));
}
const transport=new WebStandardStreamableHTTPServerTransport({sessionIdGenerator:undefined,enableJsonResponse:true});
await server.connect(transport);
const host=process.env.HOST||'127.0.0.1',port=Number(process.env.PORT||3000);
const token=process.env.DAYMIX_MCP_TOKEN;
if(!['127.0.0.1','localhost','::1'].includes(host)&&!token)throw new Error('DAYMIX_MCP_TOKEN is required for a non-loopback listener');
const MAX_REQUEST=64*1024;
const listener=createServer(async(req,res)=>{
  if(req.url==='/healthz'&&req.method==='GET'){
    res.writeHead(200,{'content-type':'application/json','cache-control':'no-store'}).end('{"status":"ok"}');return;
  }
  if(req.url!=='/mcp'){res.writeHead(404).end();return}
  if(token){
    const supplied=req.headers.authorization||'',expected=`Bearer ${token}`;
    const a=Buffer.from(supplied),b=Buffer.from(expected);
    if(a.length!==b.length||!timingSafeEqual(a,b)){res.writeHead(401,{'www-authenticate':'Bearer'}).end();return}
  }
  if(Number(req.headers['content-length']||0)>MAX_REQUEST){res.writeHead(413).end();return}
  try{
    const url=`http://${host}:${port}/mcp`;
    const init={method:req.method,headers:req.headers};
    if(req.method!=='GET'&&req.method!=='HEAD'){
      const chunks=[];let bytes=0;
      for await(const chunk of req){bytes+=chunk.length;if(bytes>MAX_REQUEST){res.writeHead(413).end();return}chunks.push(chunk)}
      init.body=Buffer.concat(chunks);
    }
    const response=await transport.handleRequest(new Request(url,init));
    res.writeHead(response.status,Object.fromEntries(response.headers));
    if(response.body)Readable.fromWeb(response.body).pipe(res);else res.end();
  }catch{
    if(!res.headersSent)res.writeHead(400,{'content-type':'application/json'}).end('{"error":"Invalid MCP request"}');
    else res.end();
  }
});
listener.requestTimeout=30_000;
listener.headersTimeout=10_000;
listener.listen(port,host,()=>console.error(`Daymix MCP: http://${host}:${port}/mcp`));
