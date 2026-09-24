import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import { createDaymixServer } from './core.mjs';

// stdout is reserved for MCP JSON-RPC. The same core tool serves HTTP and stdio.
const server=createDaymixServer();
await server.connect(new StdioServerTransport());
