const { spawn } = require('child_process');

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
  console.log(`[Client Sent]: ${json.trim()}`);
}

function processBuffer() {
  const lines = buffer.split('\n');
  buffer = lines.pop();
  
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

let tempNotebookId = null;

function handleResponse(msg) {
  if (msg.id === 1) {
    // 1. Handshake initialized
    send({
      jsonrpc: "2.0",
      method: "notifications/initialized"
    });
    
    // 2. Create a temporary notebook
    console.log('\n--- Step 1: Create verification notebook ---');
    send({
      jsonrpc: "2.0",
      id: 2,
      method: "tools/call",
      params: {
        name: "manage_notebook",
        arguments: {
          action: "create",
          title: "Antigravity Verification Run"
        }
      }
    });
  } else if (msg.id === 2) {
    // 3. Process creation response
    if (msg.error) {
      console.error('Error creating notebook:', msg.error);
      child.kill();
      return;
    }
    
    try {
      const resData = JSON.parse(msg.result.content[0].text);
      tempNotebookId = resData.id;
      console.log(`Successfully created notebook. ID: ${tempNotebookId}`);
    } catch (e) {
      console.error('Failed to parse creation response:', msg.result.content[0].text);
      child.kill();
      return;
    }
    
    // 4. List notebooks
    console.log('\n--- Step 2: List notebooks ---');
    send({
      jsonrpc: "2.0",
      id: 3,
      method: "tools/call",
      params: {
        name: "manage_notebook",
        arguments: {
          action: "list"
        }
      }
    });
  } else if (msg.id === 3) {
    // 5. Process list response
    console.log('\n=== RESULT ===');
    if (msg.error) {
      console.error('Error listing notebooks:', msg.error);
    } else {
      const content = msg.result && msg.result.content;
      if (content && content[0] && content[0].text) {
        try {
          const notebooks = JSON.parse(content[0].text);
          console.log(`Total notebooks found: ${notebooks.length}`);
          notebooks.forEach((nb, idx) => {
            console.log(`${idx + 1}. ${nb.title} (ID: ${nb.id})`);
          });
        } catch (e) {
          console.log('Raw result text:', content[0].text);
        }
      } else {
        console.log('Result:', JSON.stringify(msg.result, null, 2));
      }
    }
    console.log('==============\n');
    
    // 6. Delete temporary notebook
    if (tempNotebookId) {
      console.log('\n--- Step 3: Delete verification notebook ---');
      send({
        jsonrpc: "2.0",
        id: 4,
        method: "tools/call",
        params: {
          name: "manage_notebook",
          arguments: {
            action: "delete",
            notebook_id: tempNotebookId
          }
        }
      });
    } else {
      child.kill();
    }
  } else if (msg.id === 4) {
    // 7. Process deletion response
    console.log('\n--- Step 4: Cleanup Verification ---');
    if (msg.error) {
      console.error('Error deleting notebook:', msg.error);
    } else {
      console.log('Successfully deleted the temporary notebook.');
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
