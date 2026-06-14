const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const serverPath = '/home/yyh/project/llm_base/notebooklm-mcp/build/index.js';
console.log(`Spawning MCP server at: ${serverPath}`);

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
  console.log(`Server process exited with code ${code}`);
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

let step = 0;
const notebooks = [
  { id: 'cc35eccf-66a3-43f2-ac3b-ae6bac7b4c40', name: 'openharness' },
  { id: '0da4346f-29b3-4ab3-a1f9-fb9f0bcecae7', name: 'multimodal' }
];

function handleResponse(msg) {
  if (msg.id === 1) {
    // Handshake done
    send({
      jsonrpc: "2.0",
      method: "notifications/initialized"
    });
    
    // Fetch first notebook
    console.log(`Fetching notebook openharness (${notebooks[0].id})...`);
    send({
      jsonrpc: "2.0",
      id: 101,
      method: "tools/call",
      params: {
        name: "manage_notebook",
        arguments: {
          action: "get",
          notebook_id: notebooks[0].id
        }
      }
    });
  } else if (msg.id === 101) {
    if (msg.error) {
      console.error('Error fetching openharness:', msg.error);
    } else {
      const text = msg.result.content[0].text;
      fs.writeFileSync(path.join(__dirname, '../raw/openharness_details.json'), text);
      console.log('Saved openharness_details.json');
    }
    
    // Fetch second notebook
    console.log(`Fetching notebook multimodal (${notebooks[1].id})...`);
    send({
      jsonrpc: "2.0",
      id: 102,
      method: "tools/call",
      params: {
        name: "manage_notebook",
        arguments: {
          action: "get",
          notebook_id: notebooks[1].id
        }
      }
    });
  } else if (msg.id === 102) {
    if (msg.error) {
      console.error('Error fetching multimodal:', msg.error);
    } else {
      const text = msg.result.content[0].text;
      fs.writeFileSync(path.join(__dirname, '../raw/multimodal_details.json'), text);
      console.log('Saved multimodal_details.json');
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
      name: "fetch-client",
      version: "1.0.0"
    }
  }
});
