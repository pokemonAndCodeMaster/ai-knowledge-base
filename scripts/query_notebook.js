const { spawn } = require('child_process');

const serverPath = '/home/yyh/project/llm_base/notebooklm-mcp/build/index.js';

const args = process.argv.slice(2);
if (args.length < 2) {
  console.log("Usage: node query_notebook.js <notebook_id> <query>");
  process.exit(1);
}

const notebookId = args[0];
const query = args.slice(1).join(" ");

console.error(`Spawning MCP server at: ${serverPath}`);
console.error(`Notebook ID: ${notebookId}`);
console.error(`Query: ${query}\n`);

const child = spawn('node', [serverPath], {
  env: {
    ...process.env,
    http_proxy: '',
    https_proxy: '',
    all_proxy: '',
    HTTP_PROXY: '',
    HTTPS_PROXY: '',
    ALL_PROXY: ''
  }
});

let buffer = '';
child.stdout.on('data', (data) => {
  buffer += data.toString();
  processBuffer();
});

child.stderr.on('data', (data) => {
  console.error(`[Server Stderr]: ${data.toString().trim()}`);
});

child.on('close', (code) => {
  console.error(`Server process exited with code ${code}`);
});

function send(msg) {
  const json = JSON.stringify(msg) + '\n';
  child.stdin.write(json);
}

function processBuffer() {
  const lines = buffer.split('\n');
  buffer = lines.pop();
  
  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const response = JSON.parse(line);
      handleResponse(response);
    } catch (e) {
      console.error('Failed to parse line:', line, e);
    }
  }
}

function handleResponse(msg) {
  if (msg.id === 1) {
    // Handshake done
    send({
      jsonrpc: "2.0",
      method: "notifications/initialized"
    });
    
    // Call query_notebook
    send({
      jsonrpc: "2.0",
      id: 201,
      method: "tools/call",
      params: {
        name: "query_notebook",
        arguments: {
          notebook_id: notebookId,
          query: query
        }
      }
    });
  } else if (msg.id === 201) {
    if (msg.error) {
      console.error('Error querying notebook:', msg.error);
    } else {
      const content = msg.result.content[0].text;
      console.log(content);
    }
    child.kill();
  }
}

// Start handshake
send({
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: {
      name: "query-client",
      version: "1.0.0"
    }
  }
});
