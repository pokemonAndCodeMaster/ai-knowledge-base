const { spawn } = require('child_process');

console.log('Spawning chrome-devtools-mcp server...');
const child = spawn('node', ['/home/yyh/.npm/_npx/15c61037b1978c83/node_modules/chrome-devtools-mcp/build/src/bin/chrome-devtools-mcp.js', '--browserUrl=http://172.31.192.1:9223']);

let buffer = '';
child.stdout.on('data', (data) => {
  buffer += data.toString();
  processBuffer();
});

child.stderr.on('data', (data) => {
  console.error(`[Server Stderr]: ${data.toString().trim()}`);
});

child.on('close', (code) => {
  console.log(`Server process exited with code ${code}`);
});

function send(msg) {
  const json = JSON.stringify(msg) + '\n';
  child.stdin.write(json);
  console.log(`[Client Sent]: ${json.trim()}`);
}

function processBuffer() {
  const lines = buffer.split('\n');
  buffer = lines.pop(); // Keep the last incomplete line
  
  for (const line of lines) {
    if (!line.trim()) continue;
    console.log(`[Client Received]: ${line.trim()}`);
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
    // 1. Handshake initialized, send initialized notification
    send({
      jsonrpc: "2.0",
      method: "notifications/initialized"
    });
    
    // 2. Request list of tools
    console.log('\n--- Step 1: List available tools ---');
    send({
      jsonrpc: "2.0",
      id: 2,
      method: "tools/list"
    });
  } else if (msg.id === 2) {
    // 3. Process tools list
    console.log('\n=== TOOLS LIST ===');
    if (msg.error) {
      console.error('Error listing tools:', msg.error);
    } else {
      const tools = msg.result && msg.result.tools;
      if (tools) {
        console.log(`Found ${tools.length} tools:`);
        tools.forEach((t, idx) => {
          console.log(`${idx + 1}. ${t.name}: ${t.description}`);
        });
        
        // Find a tool to list tabs or screenshot
        const listTabsTool = tools.find(t => t.name.includes('tab') || t.name.includes('list') || t.name.includes('get_page_content'));
        if (listTabsTool) {
          console.log(`\n--- Step 2: Call ${listTabsTool.name} ---`);
          send({
            jsonrpc: "2.0",
            id: 3,
            method: "tools/call",
            params: {
              name: listTabsTool.name,
              arguments: {}
            }
          });
          return;
        }
      }
    }
    child.kill();
  } else if (msg.id === 3) {
    console.log('\n=== TOOL CALL RESULT ===');
    if (msg.error) {
      console.error('Error calling tool:', msg.error);
    } else {
      console.log('Result:', JSON.stringify(msg.result, null, 2));
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
      name: "test-client",
      version: "1.0.0"
    }
  }
});
