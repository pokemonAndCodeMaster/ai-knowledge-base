import fs from 'fs';
import path from 'path';
import os from 'os';
import axios from 'axios';
import { NotebookLMClient } from '/home/yyh/project/llm_base/notebooklm-mcp/build/api-client.js';

// Load auth
const authPath = path.join(os.homedir(), '.notebooklm-mcp', 'auth.json');
const authData = JSON.parse(fs.readFileSync(authPath, 'utf8'));
const cookies = Object.entries(authData.cookies).map(([k, v]) => `${k}=${v}`).join("; ");
const csrfToken = authData.csrf_token;

const client = new NotebookLMClient({ cookies, csrfToken });

function findDownloadUrl(obj) {
  if (typeof obj === 'string' && obj.includes('contribution.usercontent.google.com')) {
    return obj;
  }
  if (Array.isArray(obj)) {
    for (const item of obj) {
      const res = findDownloadUrl(item);
      if (res) return res;
    }
  } else if (obj && typeof obj === 'object') {
    for (const key in obj) {
      const res = findDownloadUrl(obj[key]);
      if (res) return res;
    }
  }
  return null;
}

async function run() {
  console.log("Refreshing AT token...");
  await client.refreshAtToken();

  const notebookId = 'fc03a900-e886-44a5-85b0-73983c0efa41';
  
  console.log("Getting notebook details...");
  const notebook = await client.getNotebook(notebookId);
  
  const sources = notebook[0][1];
  if (sources.length > 0) {
    const firstSource = sources[0];
    const sourceId = firstSource[0][0];
    const sourceTitle = firstSource[1];
    console.log(`First source: "${sourceTitle}" (ID: ${sourceId})`);
    
    const params = [[sourceId], [2], [2]];
    const body = await client._buildRequestBody("hizoJc", params);
    const url = client._buildUrl("hizoJc", `/notebook/${notebookId}`);
    const response = await client.client.post(url, body);
    const rawData = client._parseBatchResponse(response.data);
    
    const downloadUrl = findDownloadUrl(rawData);
    if (downloadUrl) {
      console.log("Found download URL:", downloadUrl);
      console.log("Fetching content with manual cookie header...");
      const contentRes = await axios.get(downloadUrl, {
        headers: {
          'Cookie': cookies,
          'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
          'Referer': 'https://notebooklm.google.com/'
        }
      });
      const rawContent = contentRes.data;
      
      const strVal = typeof rawContent === 'string' ? rawContent : JSON.stringify(rawContent);
      console.log("\n=== START OF RAW DATA ===");
      console.log(strVal.substring(0, 500));
      console.log("=========================\n");
      
      fs.writeFileSync("temp_source_raw.json", strVal);
      console.log("Saved raw to temp_source_raw.json");
    } else {
      console.error("Could not find download URL in response:", JSON.stringify(rawData));
    }
  }
}

run().catch(console.error);
