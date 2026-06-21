#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import os from "node:os";

import { Server } from "/home/yyh/project/llm_base/notebooklm-mcp/node_modules/@modelcontextprotocol/sdk/dist/esm/server/index.js";
import { StdioServerTransport } from "/home/yyh/project/llm_base/notebooklm-mcp/node_modules/@modelcontextprotocol/sdk/dist/esm/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "/home/yyh/project/llm_base/notebooklm-mcp/node_modules/@modelcontextprotocol/sdk/dist/esm/types.js";

import { NotebookLMClient } from "/home/yyh/project/llm_base/notebooklm-mcp/build/api-client.js";
import { NotebookOrchestrator } from "/home/yyh/project/llm_base/notebooklm-mcp/build/orchestrator.js";

const PROJECT_ROOT = "/home/yyh/project/ai-knowledge-base";
const AUTH_PATH = path.join(os.homedir(), ".notebooklm-mcp", "auth.json");
const GET_SOURCE_RPC = "hizoJc";

let client = null;
let orchestrator = null;

function loadAuth() {
  if (!fs.existsSync(AUTH_PATH)) {
    throw new Error(`NotebookLM auth file not found: ${AUTH_PATH}`);
  }

  const data = JSON.parse(fs.readFileSync(AUTH_PATH, "utf8"));
  const cookies = Object.entries(data.cookies || {})
    .map(([key, value]) => `${key}=${value}`)
    .join("; ");

  if (!cookies) {
    throw new Error(`NotebookLM auth file has no cookies: ${AUTH_PATH}`);
  }

  return {
    cookies,
    csrfToken: data.csrf_token || "",
    updatedAt: data.updated_at || null,
  };
}

function getContext() {
  if (!client || !orchestrator) {
    const auth = loadAuth();
    client = new NotebookLMClient(auth);
    client.client.defaults.timeout = Number(process.env.NOTEBOOKLM_TIMEOUT_MS || 30000);
    orchestrator = new NotebookOrchestrator(client);
  }

  return { client, orchestrator };
}

function sanitizeFilename(name) {
  return String(name || "untitled")
    .replace(/[\/\\?%*:|"<>]/g, "_")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 160) || "untitled";
}

function findLeafTextSegments(value, result = []) {
  if (Array.isArray(value)) {
    if (
      value.length >= 3 &&
      typeof value[0] === "number" &&
      typeof value[1] === "number" &&
      Array.isArray(value[2]) &&
      typeof value[2][0] === "string"
    ) {
      result.push(value);
      return result;
    }

    for (const item of value) {
      findLeafTextSegments(item, result);
    }
    return result;
  }

  if (value && typeof value === "object") {
    for (const item of Object.values(value)) {
      findLeafTextSegments(item, result);
    }
  }

  return result;
}

function parseSourceText(rawData) {
  const leaves = findLeafTextSegments(rawData);
  leaves.sort((a, b) => a[0] - b[0]);

  return leaves
    .map((leaf) => leaf[2][0])
    .filter((text) => text && text !== "[cite_start]")
    .join("")
    .trim();
}

function parseSourcesFromNotebook(notebook) {
  const rawSources = Array.isArray(notebook?.[0]?.[1]) ? notebook[0][1] : [];

  return rawSources.map((source, index) => {
    const sourceId = Array.isArray(source?.[0]) ? source[0][0] : source?.[0];
    const title = source?.[1] || `source_${index + 1}`;
    const typeCode = source?.[2] ?? null;
    const rawUrl = findFirstUrl(source);

    return {
      index,
      id: sourceId,
      title,
      type_code: typeCode,
      url: rawUrl,
      raw: source,
    };
  }).filter((source) => source.id);
}

function findFirstUrl(value) {
  if (typeof value === "string" && /^https?:\/\//.test(value)) {
    return value;
  }

  if (Array.isArray(value)) {
    for (const item of value) {
      const found = findFirstUrl(item);
      if (found) return found;
    }
  } else if (value && typeof value === "object") {
    for (const item of Object.values(value)) {
      const found = findFirstUrl(item);
      if (found) return found;
    }
  }

  return null;
}

async function getSourceRaw(clientInstance, notebookId, sourceId) {
  await clientInstance.refreshAtToken();
  const body = await clientInstance._buildRequestBody(GET_SOURCE_RPC, [[sourceId], [2], [2]]);
  const url = clientInstance._buildUrl(GET_SOURCE_RPC, `/notebook/${notebookId}`);
  const response = await clientInstance.client.post(url, body);
  return clientInstance._parseBatchResponse(response.data);
}

async function getSourceContent(clientInstance, notebookId, sourceId) {
  const raw = await getSourceRaw(clientInstance, notebookId, sourceId);
  const text = parseSourceText(raw);

  return {
    notebook_id: notebookId,
    source_id: sourceId,
    char_count: text.length,
    text,
    raw,
  };
}

function textResult(value) {
  return {
    content: [
      {
        type: "text",
        text: typeof value === "string" ? value : JSON.stringify(value, null, 2),
      },
    ],
  };
}

const server = new Server(
  {
    name: "ai-kb-notebooklm-mcp",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "auth_status",
      description: "检查本地 NotebookLM 认证文件是否存在，并返回更新时间。不返回 cookie 内容。",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "notebook_list",
      description: "列出当前 Google 账号下的 NotebookLM 笔记本。",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "notebook_get",
      description: "获取指定 NotebookLM 笔记本原始结构。",
      inputSchema: {
        type: "object",
        properties: { notebook_id: { type: "string" } },
        required: ["notebook_id"],
      },
    },
    {
      name: "source_list",
      description: "列出指定笔记本中的 sources，返回 source id、标题、URL 等。",
      inputSchema: {
        type: "object",
        properties: { notebook_id: { type: "string" } },
        required: ["notebook_id"],
      },
    },
    {
      name: "source_get_content",
      description: "拉取指定 NotebookLM source 的原文内容。",
      inputSchema: {
        type: "object",
        properties: {
          notebook_id: { type: "string" },
          source_id: { type: "string" },
          include_raw: { type: "boolean", default: false },
        },
        required: ["notebook_id", "source_id"],
      },
    },
    {
      name: "source_export_all",
      description: "批量导出指定笔记本所有 sources 的原文到本仓库 raw/notebooklm_exports/<notebook_id>/。",
      inputSchema: {
        type: "object",
        properties: {
          notebook_id: { type: "string" },
          output_dir: {
            type: "string",
            description: "可选，必须位于当前项目目录内。默认 raw/notebooklm_exports/<notebook_id>/。",
          },
          delay_ms: { type: "number", default: 1000 },
        },
        required: ["notebook_id"],
      },
    },
    {
      name: "notebook_query",
      description: "基于指定 NotebookLM 笔记本中的 sources 进行问答。",
      inputSchema: {
        type: "object",
        properties: {
          notebook_id: { type: "string" },
          query: { type: "string" },
          conversation_id: { type: "string" },
        },
        required: ["notebook_id", "query"],
      },
    },
    {
      name: "generate_artifact",
      description: "生成 NotebookLM Studio 产物：audio、video、quiz、slides、infographic、report、mind_map。",
      inputSchema: {
        type: "object",
        properties: {
          notebook_id: { type: "string" },
          type: {
            type: "string",
            enum: ["audio", "video", "quiz", "slides", "infographic", "report", "mind_map"],
          },
          config: { type: "object" },
        },
        required: ["notebook_id", "type"],
      },
    },
    {
      name: "studio_list",
      description: "列出指定 NotebookLM 笔记本中的 Studio 生成产物。",
      inputSchema: {
        type: "object",
        properties: { notebook_id: { type: "string" } },
        required: ["notebook_id"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;

  try {
    if (name === "auth_status") {
      const exists = fs.existsSync(AUTH_PATH);
      if (!exists) {
        return textResult({ ok: false, auth_path: AUTH_PATH });
      }
      const data = JSON.parse(fs.readFileSync(AUTH_PATH, "utf8"));
      return textResult({
        ok: true,
        auth_path: AUTH_PATH,
        cookie_count: Object.keys(data.cookies || {}).length,
        updated_at: data.updated_at || null,
        has_csrf_token: Boolean(data.csrf_token),
      });
    }

    const ctx = getContext();

    if (name === "notebook_list") {
      return textResult(await ctx.client.listNotebooks());
    }

    if (name === "notebook_get") {
      return textResult(await ctx.client.getNotebook(args.notebook_id));
    }

    if (name === "source_list") {
      const notebook = await ctx.client.getNotebook(args.notebook_id);
      return textResult(parseSourcesFromNotebook(notebook));
    }

    if (name === "source_get_content") {
      const result = await getSourceContent(ctx.client, args.notebook_id, args.source_id);
      if (!args.include_raw) {
        delete result.raw;
      }
      return textResult(result);
    }

    if (name === "source_export_all") {
      const notebook = await ctx.client.getNotebook(args.notebook_id);
      const sources = parseSourcesFromNotebook(notebook);
      const delayMs = Number(args.delay_ms ?? 1000);
      const outputDir = args.output_dir
        ? path.resolve(PROJECT_ROOT, args.output_dir)
        : path.join(PROJECT_ROOT, "raw", "notebooklm_exports", args.notebook_id);

      const projectRootResolved = path.resolve(PROJECT_ROOT);
      if (!outputDir.startsWith(projectRootResolved + path.sep)) {
        throw new Error(`output_dir must be inside project root: ${PROJECT_ROOT}`);
      }

      fs.mkdirSync(outputDir, { recursive: true });

      const exported = [];
      const failed = [];
      for (const source of sources) {
        try {
          const result = await getSourceContent(ctx.client, args.notebook_id, source.id);
          const basename = `${String(source.index + 1).padStart(2, "0")}_${sanitizeFilename(source.title)}.md`;
          const filepath = path.join(outputDir, basename);
          const header = [
            "---",
            `notebook_id: ${JSON.stringify(args.notebook_id)}`,
            `source_id: ${JSON.stringify(source.id)}`,
            `title: ${JSON.stringify(source.title)}`,
            `source_url: ${JSON.stringify(source.url || "")}`,
            "source_type: notebooklm_source",
            "---",
            "",
          ].join("\n");

          fs.writeFileSync(filepath, `${header}${result.text}\n`, "utf8");
          exported.push({
            source_id: source.id,
            title: source.title,
            path: path.relative(PROJECT_ROOT, filepath),
            char_count: result.char_count,
          });
        } catch (error) {
          failed.push({
            source_id: source.id,
            title: source.title,
            error: error.message,
          });
        }

        if (delayMs > 0) {
          await new Promise((resolve) => setTimeout(resolve, delayMs));
        }
      }

      return textResult({
        notebook_id: args.notebook_id,
        output_dir: path.relative(PROJECT_ROOT, outputDir),
        total_sources: sources.length,
        exported_count: exported.length,
        failed_count: failed.length,
        exported,
        failed,
      });
    }

    if (name === "notebook_query") {
      return textResult(await ctx.client.query(args.notebook_id, args.query, args.conversation_id));
    }

    if (name === "generate_artifact") {
      return textResult(await ctx.orchestrator.generateArtifact(args.notebook_id, args.type, args.config || {}));
    }

    if (name === "studio_list") {
      return textResult(await ctx.client.listStudioArtifacts(args.notebook_id));
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("ai-kb NotebookLM MCP server running on stdio");
