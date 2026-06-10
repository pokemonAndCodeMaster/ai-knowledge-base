# 🦴 代码目录架构骨架 (Code Skeleton)

> 提取目标: `codegraph/src/`
> 共包含 124 个代码文件

## 📄 codegraph/src/bin/codegraph.ts
### 🔍 结构探测
- `import { Command } from 'commander';`
- `import * as path from 'path';`
- `import * as fs from 'fs';`
- `import { getCodeGraphDir, isInitialized } from '../directory';`
- `import { detectWorktreeIndexMismatch, worktreeMismatchWarning } from '../sync/worktree';`
- `import { createShimmerProgress } from '../ui/shimmer-progress';`
- `import { getGlyphs } from '../ui/glyphs';`
- `import { buildNode25BlockBanner, buildNodeTooOldBanner, MIN_NODE_MAJOR } from './node-version-check';`
- `import { relaunchWithWasmRuntimeFlagsIfNeeded } from '../extraction/wasm-runtime-flags';`
- `import { EXTRACTION_VERSION } from '../extraction/extraction-version';`
- `function main() {`
- `function resolveProjectPath(pathArg?: string): string {`
- `function formatNumber(n: number): string {`
- `function formatDuration(ms: number): string {`
- `function createVerboseProgress(): (progress: { phase: string; current: number; total: number; currentFile?: string }) => void {`
- `function success(message: string): void {`
- `function error(message: string): void {`
- `function info(message: string): void {`
- `function warn(message: string): void {`
- `type IndexResult = {`
- `function printIndexResult(clack: typeof import('@clack/prompts'), result: IndexResult, projectPath?: string): void {`
- `function writeErrorLog(projectPath: string, errors: Array<{ message: string; filePath?: string; severity: string; code?: string }>): void {`
- `function globToRegex(pattern: string): RegExp {`
- `function printFileTree(`
- `interface TreeNode {`
- `function isTestFile(filePath: string): boolean {`

---

## 📄 codegraph/src/bin/node-version-check.ts
### 🔍 结构探测
- `export function buildNode25BlockBanner(nodeVersion: string): string {`
- `export const MIN_NODE_MAJOR = 20;`
- `export function buildNodeTooOldBanner(nodeVersion: string): string {`

---

## 📄 codegraph/src/bin/uninstall.ts
> 无识别到的结构签名

---

## 📄 codegraph/src/context/formatter.ts
### 🔍 结构探测
- `import { Node, Edge, TaskContext, Subgraph } from '../types';`
- `import { isGeneratedFile } from '../extraction/generated-detection';`
- `export function formatContextAsMarkdown(context: TaskContext): string {`
- `export function formatContextAsJson(context: TaskContext): string {`
- `export function formatSubgraphTree(subgraph: Subgraph, entryPoints: Node[]): string {`
- `function formatNodeTree(`
- `function serializeNode(node: Node): Record<string, unknown> {`
- `function serializeEdge(edge: Edge): Record<string, unknown> {`
- `function truncate(str: string, maxLength: number): string {`
- `export function formatBytes(bytes: number): string {`

---

## 📄 codegraph/src/context/index.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import {`
- `import { QueryBuilder } from '../db/queries';`
- `import { GraphTraverser } from '../graph';`
- `import { formatContextAsMarkdown, formatContextAsJson } from './formatter';`
- `import { logDebug } from '../errors';`
- `import { validatePathWithinRoot, isConfigLeafNode } from '../utils';`
- `import { isTestFile, extractSearchTerms, scorePathRelevance, getStemVariants, isDistinctiveIdentifier } from '../search/query-utils';`
- `import { LOW_CONFIDENCE_MARKER } from './markers';`
- `function extractSymbolsFromQuery(query: string): string[] {`
- `export { LOW_CONFIDENCE_MARKER } from './markers';`
- `export class ContextBuilder {`
- `export function createContextBuilder(`
- `export { formatContextAsMarkdown, formatContextAsJson } from './formatter';`

---

## 📄 codegraph/src/context/markers.ts
### 🔍 结构探测
- `export const LOW_CONFIDENCE_MARKER = '### ⚠️ Low-confidence match';`

---

## 📄 codegraph/src/db/index.ts
### 🔍 结构探测
- `import { SqliteDatabase, SqliteBackend, createDatabase } from './sqlite-adapter';`
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { SchemaVersion } from '../types';`
- `import { runMigrations, getCurrentVersion, CURRENT_SCHEMA_VERSION } from './migrations';`
- `import { getCodeGraphDir } from '../directory';`
- `export { SqliteDatabase, SqliteBackend } from './sqlite-adapter';`
- `function configureConnection(db: SqliteDatabase): void {`
- `export class DatabaseConnection {`
- `export const DATABASE_FILENAME = 'codegraph.db';`
- `export function getDatabasePath(projectRoot: string): string {`

---

## 📄 codegraph/src/db/migrations.ts
### 🔍 结构探测
- `import { SqliteDatabase } from './sqlite-adapter';`
- `export const CURRENT_SCHEMA_VERSION = 5;`
- `interface Migration {`
- `export function getCurrentVersion(db: SqliteDatabase): number {`
- `function recordMigration(db: SqliteDatabase, version: number, description: string): void {`
- `export function runMigrations(db: SqliteDatabase, fromVersion: number): void {`
- `export function needsMigration(db: SqliteDatabase): boolean {`
- `export function getPendingMigrations(db: SqliteDatabase): Migration[] {`
- `export function getMigrationHistory(`

---

## 📄 codegraph/src/db/queries.ts
### 🔍 结构探测
- `import { SqliteDatabase, SqliteStatement } from './sqlite-adapter';`
- `import {`
- `import { safeJsonParse } from '../utils';`
- `import { kindBonus, nameMatchBonus, scorePathRelevance } from '../search/query-utils';`
- `import { parseQuery, boundedEditDistance } from '../search/query-parser';`
- `import { isGeneratedFile } from '../extraction/generated-detection';`
- `function isLowValueFile(filePath: string): boolean {`
- `interface NodeRow {`
- `interface EdgeRow {`
- `interface FileRow {`
- `interface UnresolvedRefRow {`
- `function rowToNode(row: NodeRow): Node {`
- `function rowToEdge(row: EdgeRow): Edge {`
- `function rowToFileRecord(row: FileRow): FileRecord {`
- `export class QueryBuilder {`

---

## 📄 codegraph/src/db/sqlite-adapter.ts
### 🔍 结构探测
- `export interface SqliteStatement {`
- `export interface SqliteDatabase {`
- `export type SqliteBackend = 'node-sqlite';`
- `class NodeSqliteAdapter implements SqliteDatabase {`
- `export function createDatabase(dbPath: string): { db: SqliteDatabase; backend: SqliteBackend } {`

---

## 📄 codegraph/src/directory.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `export function codeGraphDirName(): string {`
- `export const CODEGRAPH_DIR = codeGraphDirName();`
- `export function isCodeGraphDataDir(name: string): boolean {`
- `export function getCodeGraphDir(projectRoot: string): string {`
- `export function isInitialized(projectRoot: string): boolean {`
- `export function findNearestCodeGraphRoot(startPath: string): string | null {`
- `export function createDirectory(projectRoot: string): void {`
- `export function removeDirectory(projectRoot: string): void {`
- `export function listDirectoryContents(projectRoot: string): string[] {`
- `function walkDir(dir: string, prefix: string = ''): void {`
- `export function getDirectorySize(projectRoot: string): number {`
- `function walkDir(dir: string): void {`
- `export function ensureSubdirectory(projectRoot: string, subdirName: string): string {`
- `export function validateDirectory(projectRoot: string): {`

---

## 📄 codegraph/src/errors.ts
### 🔍 结构探测
- `export class CodeGraphError extends Error {`
- `export class FileError extends CodeGraphError {`
- `export class ParseError extends CodeGraphError {`
- `export class DatabaseError extends CodeGraphError {`
- `export class SearchError extends CodeGraphError {`
- `export class VectorError extends CodeGraphError {`
- `export class ConfigError extends CodeGraphError {`
- `export interface Logger {`
- `export const defaultLogger: Logger = {`
- `export const silentLogger: Logger = {`
- `export function setLogger(logger: Logger): void {`
- `export function getLogger(): Logger {`
- `export function logDebug(message: string, context?: Record<string, unknown>): void {`
- `export function logWarn(message: string, context?: Record<string, unknown>): void {`
- `export function logError(message: string, context?: Record<string, unknown>): void {`

---

## 📄 codegraph/src/extraction/dfm-extractor.ts
### 🔍 结构探测
- `import { Node, Edge, ExtractionResult, ExtractionError, UnresolvedReference } from '../types';`
- `import { generateNodeId } from './tree-sitter-helpers';`
- `export class DfmExtractor {`

---

## 📄 codegraph/src/extraction/extraction-version.ts
### 🔍 结构探测
- `export const EXTRACTION_VERSION = 14;`

---

## 📄 codegraph/src/extraction/generated-detection.ts
### 🔍 结构探测
- `export function isGeneratedFile(filePath: string): boolean {`

---

## 📄 codegraph/src/extraction/grammars.ts
### 🔍 结构探测
- `import * as path from 'path';`
- `import { Parser, Language as WasmLanguage } from 'web-tree-sitter';`
- `import { Language } from '../types';`
- `export type GrammarLanguage = Exclude<Language, 'svelte' | 'vue' | 'liquid' | 'razor' | 'yaml' | 'twig' | 'xml' | 'properties' | 'unknown'>;`
- `export const EXTENSION_MAP: Record<string, Language> = {`
- `export function isSourceFile(filePath: string): boolean {`
- `export function isShopifyLiquidJson(filePath: string): boolean {`
- `export function isPlayRoutesFile(filePath: string): boolean {`
- `export async function initGrammars(): Promise<void> {`
- `export async function loadGrammarsForLanguages(languages: Language[]): Promise<void> {`
- `export async function loadAllGrammars(): Promise<void> {`
- `export function isGrammarsInitialized(): boolean {`
- `export function getParser(language: Language): Parser | null {`
- `export function detectLanguage(filePath: string, source?: string): Language {`
- `function looksLikeCpp(source: string): boolean {`
- `function looksLikeObjc(source: string): boolean {`
- `export function isLanguageSupported(language: Language): boolean {`
- `export function isGrammarLoaded(language: Language): boolean {`
- `export function isFileLevelOnlyLanguage(language: Language): boolean {`
- `export function getSupportedLanguages(): Language[] {`
- `export function resetParser(language: Language): void {`
- `export function clearParserCache(): void {`
- `export function getUnavailableGrammarErrors(): Partial<Record<Language, string>> {`
- `export function getLanguageDisplayName(language: Language): string {`

---

## 📄 codegraph/src/extraction/index.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as fsp from 'fs/promises';`
- `import * as path from 'path';`
- `import * as crypto from 'crypto';`
- `import { execFileSync } from 'child_process';`
- `import {`
- `import { QueryBuilder } from '../db/queries';`
- `import { extractFromSource } from './tree-sitter';`
- `import { detectLanguage, isSourceFile, isLanguageSupported, isFileLevelOnlyLanguage, initGrammars, loadGrammarsForLanguages } from './grammars';`
- `import { isCodeGraphDataDir } from '../directory';`
- `import { logDebug, logWarn } from '../errors';`
- `import { validatePathWithinRoot, normalizePath } from '../utils';`
- `import ignore, { Ignore } from 'ignore';`
- `import { detectFrameworks } from '../resolution/frameworks';`
- `import type { ResolutionContext } from '../resolution/types';`
- `export interface IndexProgress {`
- `export interface IndexResult {`
- `export interface SyncResult {`
- `export function hashContent(content: string): string {`
- `function isValidUtf8(buf: Buffer): boolean {`
- `function readGitignorePatterns(giPath: string): string {`
- `export function buildDefaultIgnore(rootDir: string): Ignore {`
- `function collectGitFiles(repoDir: string, prefix: string, files: Set<string>): void {`
- `function getGitVisibleFiles(rootDir: string): Set<string> | null {`
- `interface GitChanges {`
- `function getGitChangedFiles(rootDir: string): GitChanges | null {`
- `export function scanDirectory(`
- `export async function scanDirectoryAsync(`
- `function scanDirectoryWalk(`
- `interface ScopedIgnore {`
- `function walk(dir: string, matchers: ScopedIgnore[]): void {`
- `export class ExtractionOrchestrator {`
- `function rejectAllPending(reason: string): void {`
- `function attachWorkerHandlers(w: import('worker_threads').Worker): void {`
- `function recycleWorker(): void {`
- `export { extractFromSource } from './tree-sitter';`
- `export { detectLanguage, isSourceFile, isLanguageSupported, isGrammarLoaded, getSupportedLanguages, initGrammars, loadGrammarsForLanguages, loadAllGrammars } from './grammars';`

---

## 📄 codegraph/src/extraction/languages/c-cpp.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getChildByField, getNodeText } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function findDeclaratorQualifiedId(declarator: SyntaxNode): SyntaxNode | undefined {`
- `function extractCppQualifiedMethodName(node: SyntaxNode, source: string): string | undefined {`
- `function extractCppReceiverType(node: SyntaxNode, source: string): string | undefined {`
- `export function normalizeCppReturnType(raw: string): string | undefined {`
- `function extractCppReturnType(node: SyntaxNode, source: string): string | undefined {`
- `export const cExtractor: LanguageExtractor = {`
- `export const cppExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/csharp.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `export function blankCsharpPreprocessorDirectives(source: string): string {`
- `function extractCsharpReturnType(node: SyntaxNode, source: string): string | undefined {`
- `export const csharpExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/dart.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function dartInnerSignature(node: SyntaxNode): SyntaxNode {`
- `function dartConstructorSignature(node: SyntaxNode): SyntaxNode | undefined {`
- `function dartEnclosingTypeName(node: SyntaxNode): string | undefined {`
- `function dartCtorInfo(node: SyntaxNode): { className: string; ctorName: string } | undefined {`
- `function extractDartReturnType(node: SyntaxNode, source: string): string | undefined {`
- `function dartCalleeOfArgPart(argPart: SyntaxNode): string | undefined {`
- `export const dartExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/go.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function extractGoReturnType(node: SyntaxNode, source: string): string | undefined {`
- `export const goExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/index.ts
### 🔍 结构探测
- `import { Language } from '../../types';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `import { typescriptExtractor } from './typescript';`
- `import { javascriptExtractor } from './javascript';`
- `import { pythonExtractor } from './python';`
- `import { goExtractor } from './go';`
- `import { rustExtractor } from './rust';`
- `import { javaExtractor } from './java';`
- `import { cExtractor, cppExtractor } from './c-cpp';`
- `import { csharpExtractor } from './csharp';`
- `import { phpExtractor } from './php';`
- `import { rubyExtractor } from './ruby';`
- `import { swiftExtractor } from './swift';`
- `import { kotlinExtractor } from './kotlin';`
- `import { dartExtractor } from './dart';`
- `import { pascalExtractor } from './pascal';`
- `import { scalaExtractor } from './scala';`
- `import { luaExtractor } from './lua';`
- `import { luauExtractor } from './luau';`
- `import { objcExtractor } from './objc';`
- `export const EXTRACTORS: Partial<Record<Language, LanguageExtractor>> = {`

---

## 📄 codegraph/src/extraction/languages/java.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function extractJavaReturnType(node: SyntaxNode, source: string): string | undefined {`
- `export const javaExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/javascript.ts
### 🔍 结构探测
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `export const javascriptExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/kotlin.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function extractKotlinReturnType(node: SyntaxNode, source: string): string | undefined {`
- `function isFunInterfaceNode(node: SyntaxNode): boolean {`
- `export const kotlinExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/lua.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function findDescendant(node: SyntaxNode, type: string): SyntaxNode | null {`
- `function requireModule(callNode: SyntaxNode, source: string): string | null {`
- `export const luaExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/luau.ts
### 🔍 结构探测
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `import { luaExtractor } from './lua';`
- `export const luauExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/objc.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getChildByField, getNodeText } from '../tree-sitter-helpers';`
- `import type { ExtractorContext, LanguageExtractor } from '../tree-sitter-types';`
- `function findCompoundStatement(node: SyntaxNode): SyntaxNode | null {`
- `function extractObjcMethodName(node: SyntaxNode, source: string): string | undefined {`
- `function extractObjcPropertyName(node: SyntaxNode, source: string): string | null {`
- `export const objcExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/pascal.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `export const pascalExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/php.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function phpStaticIncludePath(node: SyntaxNode, source: string): string | null {`
- `function extractPhpReturnType(node: SyntaxNode, source: string): string | undefined {`
- `export const phpExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/python.ts
### 🔍 结构探测
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `export const pythonExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/ruby.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `export const rubyExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/rust.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function extractRustReturnType(node: SyntaxNode, source: string): string | undefined {`
- `export const rustExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/scala.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function getValVarName(node: SyntaxNode, source: string): string | null {`
- `function emitScalaTypeRefs(typeNode: SyntaxNode, fromId: string, ctx: { addUnresolvedReference: (r: { fromNodeId: string; referenceName: string; referenceKind: 'references'; line: number; column: number }) => void }, source: string): void {`
- `function extractScalaReturnType(node: SyntaxNode, source: string): string | undefined {`
- `function extractVisibility(node: SyntaxNode): 'public' | 'private' | 'protected' {`
- `export const scalaExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/swift.ts
### 🔍 结构探测
- `import type { Node as SyntaxNode } from 'web-tree-sitter';`
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `function extractSwiftReturnType(node: SyntaxNode, source: string): string | undefined {`
- `export const swiftExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/languages/typescript.ts
### 🔍 结构探测
- `import { getNodeText, getChildByField } from '../tree-sitter-helpers';`
- `import type { LanguageExtractor } from '../tree-sitter-types';`
- `export const typescriptExtractor: LanguageExtractor = {`

---

## 📄 codegraph/src/extraction/liquid-extractor.ts
### 🔍 结构探测
- `import { Node, Edge, ExtractionResult, ExtractionError, UnresolvedReference } from '../types';`
- `import { generateNodeId } from './tree-sitter-helpers';`
- `export class LiquidExtractor {`

---

## 📄 codegraph/src/extraction/mybatis-extractor.ts
### 🔍 结构探测
- `import { Edge, ExtractionError, ExtractionResult, Node, UnresolvedReference } from '../types';`
- `import { generateNodeId } from './tree-sitter-helpers';`
- `export class MyBatisExtractor {`

---

## 📄 codegraph/src/extraction/parse-worker.ts
### 🔍 结构探测
- `import { parentPort } from 'worker_threads';`
- `import { extractFromSource } from './tree-sitter';`
- `import { detectLanguage, loadGrammarsForLanguages, resetParser } from './grammars';`
- `import type { Language, ExtractionResult } from '../types';`

---

## 📄 codegraph/src/extraction/razor-extractor.ts
### 🔍 结构探测
- `import { Node, Edge, ExtractionResult, ExtractionError, UnresolvedReference } from '../types';`
- `import { generateNodeId } from './tree-sitter-helpers';`
- `import { TreeSitterExtractor } from './tree-sitter';`
- `import { isLanguageSupported } from './grammars';`
- `export class RazorExtractor {`

---

## 📄 codegraph/src/extraction/svelte-extractor.ts
### 🔍 结构探测
- `import { Node, Edge, ExtractionResult, ExtractionError, UnresolvedReference, Language } from '../types';`
- `import { generateNodeId } from './tree-sitter-helpers';`
- `import { TreeSitterExtractor } from './tree-sitter';`
- `import { isLanguageSupported } from './grammars';`
- `export class SvelteExtractor {`

---

## 📄 codegraph/src/extraction/tree-sitter-helpers.ts
### 🔍 结构探测
- `import { Node as SyntaxNode } from 'web-tree-sitter';`
- `import * as crypto from 'crypto';`
- `import { NodeKind } from '../types';`
- `export function generateNodeId(`
- `export function getNodeText(node: SyntaxNode, source: string): string {`
- `export function getChildByField(node: SyntaxNode, fieldName: string): SyntaxNode | null {`
- `export function getPrecedingDocstring(node: SyntaxNode, source: string): string | undefined {`

---

## 📄 codegraph/src/extraction/tree-sitter-types.ts
### 🔍 结构探测
- `import { Node as SyntaxNode } from 'web-tree-sitter';`
- `import {`
- `export interface ImportInfo {`
- `export interface VariableInfo {`
- `export interface ExtractorContext {`
- `export interface LanguageExtractor {`

---

## 📄 codegraph/src/extraction/tree-sitter.ts
### 🔍 结构探测
- `import { Node as SyntaxNode, Tree } from 'web-tree-sitter';`
- `import * as path from 'path';`
- `import {`
- `import { getParser, detectLanguage, isLanguageSupported, isFileLevelOnlyLanguage } from './grammars';`
- `import { generateNodeId, getNodeText, getChildByField, getPrecedingDocstring } from './tree-sitter-helpers';`
- `import type { LanguageExtractor, ExtractorContext } from './tree-sitter-types';`
- `import { EXTRACTORS } from './languages';`
- `import { LiquidExtractor } from './liquid-extractor';`
- `import { RazorExtractor } from './razor-extractor';`
- `import { SvelteExtractor } from './svelte-extractor';`
- `import { DfmExtractor } from './dfm-extractor';`
- `import { VueExtractor } from './vue-extractor';`
- `import { MyBatisExtractor } from './mybatis-extractor';`
- `import {`
- `export { generateNodeId } from './tree-sitter-helpers';`
- `function extractName(node: SyntaxNode, source: string, extractor: LanguageExtractor): string {`
- `function scalaBaseTypeName(node: SyntaxNode | null, source: string): string | null {`
- `export class TreeSitterExtractor {`
- `export function extractFromSource(`

---

## 📄 codegraph/src/extraction/vue-extractor.ts
### 🔍 结构探测
- `import { Node, Edge, ExtractionResult, ExtractionError, UnresolvedReference, Language } from '../types';`
- `import { generateNodeId } from './tree-sitter-helpers';`
- `import { TreeSitterExtractor } from './tree-sitter';`
- `import { isLanguageSupported } from './grammars';`
- `function kebabToPascal(name: string): string {`
- `export class VueExtractor {`

---

## 📄 codegraph/src/extraction/wasm-runtime-flags.ts
### 🔍 结构探测
- `import { spawnSync } from 'child_process';`
- `export const WASM_RUNTIME_FLAGS: readonly string[] = ['--liftoff-only'];`
- `export const HOST_PPID_ENV = 'CODEGRAPH_HOST_PPID';`
- `export function processHasWasmRuntimeFlags(`
- `export function buildRelaunchArgv(`
- `export function relaunchWithWasmRuntimeFlagsIfNeeded(scriptPath: string): void {`

---

## 📄 codegraph/src/graph/index.ts
### 🔍 结构探测
- `export { GraphTraverser } from './traversal';`
- `export { GraphQueryManager } from './queries';`

---

## 📄 codegraph/src/graph/queries.ts
### 🔍 结构探测
- `import { Node, Edge, Context, Subgraph, EdgeKind } from '../types';`
- `import { QueryBuilder } from '../db/queries';`
- `import { GraphTraverser } from './traversal';`
- `export class GraphQueryManager {`

---

## 📄 codegraph/src/graph/traversal.ts
### 🔍 结构探测
- `import { Node, Edge, Subgraph, TraversalOptions, EdgeKind } from '../types';`
- `import { QueryBuilder } from '../db/queries';`
- `interface TraversalStep {`
- `export class GraphTraverser {`

---

## 📄 codegraph/src/index.ts
### 🔍 结构探测
- `import * as path from 'path';`
- `import {`
- `import { DatabaseConnection, getDatabasePath } from './db';`
- `import { QueryBuilder } from './db/queries';`
- `import {`
- `import {`
- `import {`
- `import { GraphTraverser, GraphQueryManager } from './graph';`
- `import { ContextBuilder, createContextBuilder } from './context';`
- `import { Mutex, FileLock } from './utils';`
- `import { FileWatcher, WatchOptions, PendingFile, LockUnavailableError } from './sync';`
- `import { EXTRACTION_VERSION } from './extraction/extraction-version';`
- `import { getCodeGraphDir } from './directory';`
- `import { deriveProjectNameTokens } from './search/query-utils';`
- `import { CodeGraphPackageVersion } from './mcp/version';`
- `export * from './types';`
- `export { getDatabasePath, DatabaseConnection } from './db';`
- `export { QueryBuilder } from './db/queries';`
- `export {`
- `export { IndexProgress, IndexResult, SyncResult } from './extraction';`
- `export { detectLanguage, isLanguageSupported, isGrammarLoaded, getSupportedLanguages, initGrammars, loadGrammarsForLanguages, loadAllGrammars } from './extraction';`
- `export { ResolutionResult } from './resolution';`
- `export {`
- `export { Mutex, FileLock, processInBatches, debounce, throttle, MemoryMonitor } from './utils';`
- `export { FileWatcher, WatchOptions, PendingFile, LockUnavailableError } from './sync';`
- `export { MCPServer } from './mcp';`
- `export interface InitOptions {`
- `export interface OpenOptions {`
- `export interface IndexOptions {`
- `export class CodeGraph {`
- `export default CodeGraph;`

---

## 📄 codegraph/src/installer/clack.d.ts
### 🔍 结构探测
- `export function intro(title?: string): void;`
- `export function outro(message?: string): void;`
- `export function cancel(message?: string): void;`
- `export function isCancel(value: unknown): value is symbol;`
- `export function confirm(opts: {`
- `export function select<Value>(opts: {`
- `export function multiselect<Value>(opts: {`
- `export function spinner(): {`
- `export function note(message: string, title?: string): void;`
- `export const log: {`

---

## 📄 codegraph/src/installer/config-writer.ts
### 🔍 结构探测
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import {`
- `import { readJsonFile } from './targets/shared';`
- `export type InstallLocation = 'global' | 'local';`
- `export function writeMcpConfig(location: InstallLocation): void {`
- `export function writePermissions(location: InstallLocation): void {`
- `export function hasMcpConfig(location: InstallLocation): boolean {`
- `export function hasPermissions(location: InstallLocation): boolean {`

---

## 📄 codegraph/src/installer/index.ts
### 🔍 结构探测
- `import { execSync } from 'child_process';`
- `import * as path from 'path';`
- `import * as fs from 'fs';`
- `import {`
- `import type { AgentTarget, Location, TargetId } from './targets/types';`
- `import { getGlyphs } from '../ui/glyphs';`
- `import { watchDisabledReason } from '../sync/watch-policy';`
- `import { isGitRepo, isSyncHookInstalled, installGitSyncHook } from '../sync/git-hooks';`
- `import { getCodeGraphDir, codeGraphDirName } from '../directory';`
- `export {`
- `export type { InstallLocation } from './config-writer';`
- `function formatNumber(n: number): string {`
- `function getVersion(): string {`
- `export interface RunInstallerOptions {`
- `export async function runInstaller(): Promise<void> {`
- `export async function runInstallerWithOptions(opts: RunInstallerOptions): Promise<void> {`
- `export interface RunUninstallerOptions {`
- `export type UninstallStatus = 'removed' | 'not-configured' | 'unsupported';`
- `export interface UninstallReport {`
- `export function uninstallTargets(`
- `export async function runUninstaller(opts: RunUninstallerOptions): Promise<void> {`
- `function tildify(p: string): string {`
- `export async function offerWatchFallback(`

---

## 📄 codegraph/src/installer/instructions-template.ts
### 🔍 结构探测
- `export const CODEGRAPH_SECTION_START = '<!-- CODEGRAPH_START -->';`
- `export const CODEGRAPH_SECTION_END = '<!-- CODEGRAPH_END -->';`

---

## 📄 codegraph/src/installer/targets/antigravity.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import { execSync } from 'child_process';`
- `import {`
- `import {`
- `function unifiedConfigDir(): string {`
- `function unifiedMcpConfigPath(): string {`
- `function legacyConfigDir(): string {`
- `function legacyMcpConfigPath(): string {`
- `function migratedMarkerPath(): string {`
- `function preferredMcpConfigPath(): string {`
- `function resolveCodegraphCommand(): string {`
- `function buildAntigravityEntry(): { command: string; args: string[] } {`
- `class AntigravityTarget implements AgentTarget {`
- `function writeMcpEntry(): WriteResult['files'][number] {`
- `function cleanupLegacyEntry(): WriteResult['files'][number] | null {`
- `function removeCodegraphFromFile(file: string): WriteResult['files'][number] {`
- `export const antigravityTarget: AgentTarget = new AntigravityTarget();`

---

## 📄 codegraph/src/installer/targets/claude.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import {`
- `import {`
- `import {`
- `function configDir(loc: Location): string {`
- `function mcpJsonPath(loc: Location): string {`
- `function legacyLocalMcpPath(): string {`
- `function settingsJsonPath(loc: Location): string {`
- `function instructionsPath(loc: Location): string {`
- `class ClaudeCodeTarget implements AgentTarget {`
- `export function writeMcpEntry(loc: Location): WriteResult['files'][number] {`
- `function cleanupLegacyLocalMcp(): WriteResult['files'][number] | null {`
- `function isLegacyCodegraphHookCommand(command: unknown): boolean {`
- `export function cleanupLegacyHooks(loc: Location): WriteResult['files'][number] {`
- `export function writePermissionsEntry(loc: Location): WriteResult['files'][number] {`
- `export function removeInstructionsEntry(loc: Location): WriteResult['files'][number] {`
- `export const claudeTarget: AgentTarget = new ClaudeCodeTarget();`

---

## 📄 codegraph/src/installer/targets/codex.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import {`
- `import {`
- `import {`
- `import { buildTomlTable, removeTomlTable, upsertTomlTable } from './toml';`
- `function configDir(): string {`
- `function tomlConfigPath(): string {`
- `function instructionsPath(): string {`
- `class CodexTarget implements AgentTarget {`
- `function buildCodegraphBlock(): string {`
- `function writeMcpEntry(): WriteResult['files'][number] {`
- `function removeInstructionsEntry(): WriteResult['files'][number] {`
- `export const codexTarget: AgentTarget = new CodexTarget();`

---

## 📄 codegraph/src/installer/targets/cursor.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import {`
- `import {`
- `import {`
- `function mcpJsonPath(loc: Location): string {`
- `function rulesPath(): string {`
- `class CursorTarget implements AgentTarget {`
- `function buildCursorMcpConfig(loc: Location): { type: string; command: string; args: string[] } {`
- `function writeMcpEntry(loc: Location): WriteResult['files'][number] {`
- `function removeRulesEntry(): WriteResult['files'][number] {`
- `export const cursorTarget: AgentTarget = new CursorTarget();`

---

## 📄 codegraph/src/installer/targets/gemini.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import {`
- `import {`
- `import {`
- `function configDir(loc: Location): string {`
- `function settingsJsonPath(loc: Location): string {`
- `function instructionsPath(loc: Location): string {`
- `class GeminiTarget implements AgentTarget {`
- `function writeMcpEntry(loc: Location): WriteResult['files'][number] {`
- `function removeInstructionsEntry(loc: Location): WriteResult['files'][number] {`
- `export const geminiTarget: AgentTarget = new GeminiTarget();`

---

## 📄 codegraph/src/installer/targets/hermes.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import {`
- `import { atomicWriteFileSync } from './shared';`
- `type LineRange = { start: number; end: number };`
- `class HermesTarget implements AgentTarget {`
- `function hermesHome(): string {`
- `function configPath(): string {`
- `function readText(file: string): string {`
- `function writeHermesConfig(): WriteResult['files'][number] {`
- `function ensureTrailingNewline(text: string): string {`
- `function splitLines(content: string): string[] {`
- `function joinLines(lines: string[]): string {`
- `function topLevelRange(lines: string[], key: string): LineRange | null {`
- `function childRange(lines: string[], parent: LineRange, child: string): LineRange | null {`
- `function listChildBlock(`
- `function escapeRegExp(value: string): string {`
- `function renderCodeGraphMcpChild(): string[] {`
- `function renderCodeGraphMcpBlock(): string[] {`
- `function hasCodeGraphMcpServer(content: string): boolean {`
- `function upsertCodeGraphMcpServer(content: string): string {`
- `function removeCodeGraphMcpServer(content: string): string {`
- `function upsertCodeGraphToolset(content: string): string {`
- `function removeCodeGraphToolset(content: string): string {`
- `function arrayEqual(a: string[], b: string[]): boolean {`
- `export const hermesTarget: AgentTarget = new HermesTarget();`

---

## 📄 codegraph/src/installer/targets/kiro.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import {`
- `import {`
- `function configDir(loc: Location): string {`
- `function mcpJsonPath(loc: Location): string {`
- `function steeringPath(loc: Location): string {`
- `class KiroTarget implements AgentTarget {`
- `function writeMcpEntry(loc: Location): WriteResult['files'][number] {`
- `function removeSteeringEntry(loc: Location): WriteResult['files'][number] {`
- `export const kiroTarget: AgentTarget = new KiroTarget();`

---

## 📄 codegraph/src/installer/targets/opencode.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as os from 'os';`
- `import { parse as parseJsonc, modify, applyEdits } from 'jsonc-parser';`
- `import {`
- `import {`
- `import {`
- `function globalConfigDir(): string {`
- `function configBaseDir(loc: Location): string {`
- `function configPath(loc: Location): string {`
- `function instructionsPath(loc: Location): string {`
- `function readConfigText(file: string): string {`
- `function parseConfig(text: string): Record<string, any> {`
- `function getOpencodeServerEntry(): { type: string; command: string[]; enabled: boolean } {`
- `class OpencodeTarget implements AgentTarget {`
- `function writeMcpEntry(loc: Location): WriteResult['files'][number] {`
- `function removeInstructionsEntry(loc: Location): WriteResult['files'][number] {`
- `export const opencodeTarget: AgentTarget = new OpencodeTarget();`

---

## 📄 codegraph/src/installer/targets/registry.ts
### 🔍 结构探测
- `import { AgentTarget, Location, TargetId } from './types';`
- `import { claudeTarget } from './claude';`
- `import { cursorTarget } from './cursor';`
- `import { codexTarget } from './codex';`
- `import { opencodeTarget } from './opencode';`
- `import { hermesTarget } from './hermes';`
- `import { geminiTarget } from './gemini';`
- `import { antigravityTarget } from './antigravity';`
- `import { kiroTarget } from './kiro';`
- `export const ALL_TARGETS: readonly AgentTarget[] = Object.freeze([`
- `export function getTarget(id: string): AgentTarget | undefined {`
- `export function listTargetIds(): TargetId[] {`
- `export function detectAll(loc: Location): Array<{`
- `export function resolveTargetFlag(value: string, loc: Location): AgentTarget[] {`

---

## 📄 codegraph/src/installer/targets/shared.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `export function getMcpServerConfig(): { type: string; command: string; args: string[] } {`
- `export function getCodeGraphPermissions(): string[] {`
- `export function readJsonFile(filePath: string): Record<string, any> {`
- `export function atomicWriteFileSync(filePath: string, content: string): void {`
- `export function writeJsonFile(filePath: string, data: Record<string, any>): void {`
- `export function jsonDeepEqual(a: unknown, b: unknown): boolean {`
- `export function replaceOrAppendMarkedSection(`
- `export function removeMarkedSection(`

---

## 📄 codegraph/src/installer/targets/toml.ts
### 🔍 结构探测
- `export function serializeTomlTableBody(values: Record<string, string | string[]>): string {`
- `function quoteString(s: string): string {`
- `export function buildTomlTable(header: string, values: Record<string, string | string[]>): string {`
- `export function upsertTomlTable(`
- `export function removeTomlTable(`
- `function findHeaderIndex(content: string, headerLine: string): number {`
- `function findNextTableHeader(content: string, from: number): number {`

---

## 📄 codegraph/src/installer/targets/types.ts
### 🔍 结构探测
- `export type Location = 'global' | 'local';`
- `export type TargetId = 'claude' | 'cursor' | 'codex' | 'opencode' | 'hermes' | 'gemini' | 'antigravity' | 'kiro';`
- `export interface DetectionResult {`
- `export interface WriteResult {`
- `export interface InstallOptions {`
- `export interface AgentTarget {`

---

## 📄 codegraph/src/mcp/daemon-paths.ts
### 🔍 结构探测
- `import * as crypto from 'crypto';`
- `import * as os from 'os';`
- `import * as path from 'path';`
- `import { getCodeGraphDir } from '../directory';`
- `function projectHash(projectRoot: string): string {`
- `export function getDaemonSocketPath(projectRoot: string): string {`
- `export function getDaemonPidPath(projectRoot: string): string {`
- `export interface DaemonLockInfo {`
- `export function encodeLockInfo(info: DaemonLockInfo): string {`
- `export function decodeLockInfo(raw: string): DaemonLockInfo | null {`

---

## 📄 codegraph/src/mcp/daemon.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as net from 'net';`
- `import * as path from 'path';`
- `import { MCPEngine } from './engine';`
- `import { MCPSession } from './session';`
- `import { SocketTransport } from './transport';`
- `import {`
- `import { CodeGraphPackageVersion } from './version';`
- `export interface DaemonHello {`
- `export interface DaemonClientHello {`
- `export interface DaemonStartResult {`
- `export class Daemon {`
- `export type AcquireResult =`
- `export function tryAcquireDaemonLock(projectRoot: string): AcquireResult {`
- `export function clearStaleDaemonLock(pidPath: string, expectedDeadPid?: number): boolean {`
- `export function isProcessAlive(pid: number): boolean {`
- `function resolveIdleTimeoutMs(): number {`
- `function resolveMaxIdleMs(): number {`
- `function resolveClientSweepMs(): number {`
- `export function parseClientHelloLine(`
- `export function peerIsDead(`
- `function readClientHello(`
- `export { MAX_HELLO_LINE_BYTES };`

---

## 📄 codegraph/src/mcp/engine.ts
### 🔍 结构探测
- `import type CodeGraph from '../index';`
- `import { findNearestCodeGraphRoot } from '../directory';`
- `import { watchDisabledReason } from '../sync';`
- `import { ToolHandler } from './tools';`
- `export interface MCPEngineOptions {`
- `export class MCPEngine {`
- `export function parseDebounceEnv(raw: string | undefined): number | undefined {`

---

## 📄 codegraph/src/mcp/index.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { spawn, StdioOptions } from 'child_process';`
- `import { findNearestCodeGraphRoot, getCodeGraphDir } from '../directory';`
- `import { StdioTransport } from './transport';`
- `import { MCPEngine } from './engine';`
- `import { MCPSession } from './session';`
- `import {`
- `import { connectWithHello, runLocalHandshakeProxy } from './proxy';`
- `import { getDaemonSocketPath } from './daemon-paths';`
- `import { supervisionLostReason } from './ppid-watchdog';`
- `import { HOST_PPID_ENV } from '../extraction/wasm-runtime-flags';`
- `function parsePpidPollMs(raw: string | undefined): number {`
- `function parseHostPpid(raw: string | undefined): number | null {`
- `function daemonOptOutSet(): boolean {`
- `function daemonInternalSet(): boolean {`
- `function resolveDaemonRoot(explicitPath: string | null): string | null {`
- `function spawnDetachedDaemon(root: string): void {`
- `export class MCPServer {`
- `function sleep(ms: number): Promise<void> {`
- `export { StdioTransport } from './transport';`
- `export { tools, ToolHandler } from './tools';`
- `export { Daemon } from './daemon';`
- `export { CodeGraphPackageVersion } from './version';`

---

## 📄 codegraph/src/mcp/ppid-watchdog.ts
### 🔍 结构探测
- `export interface SupervisionState {`
- `export function supervisionLostReason(state: SupervisionState): string | null {`

---

## 📄 codegraph/src/mcp/proxy.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as net from 'net';`
- `import { HOST_PPID_ENV } from '../extraction/wasm-runtime-flags';`
- `import { DaemonClientHello, DaemonHello, MAX_HELLO_LINE_BYTES } from './daemon';`
- `import { supervisionLostReason } from './ppid-watchdog';`
- `import { CodeGraphPackageVersion } from './version';`
- `import { SERVER_INFO, PROTOCOL_VERSION } from './session';`
- `import { SERVER_INSTRUCTIONS } from './server-instructions';`
- `import { getStaticTools } from './tools';`
- `import type { MCPEngine } from './engine';`
- `export function logAttachedDaemon(socketPath: string, hello: DaemonHello): void {`
- `export interface ProxyResult {`
- `export async function runProxy(`
- `export async function connectWithHello(`
- `function sendClientHello(socket: net.Socket): void {`
- `type JsonRpc = Record<string, unknown>;`
- `export interface LocalHandshakeDeps {`
- `export async function runLocalHandshakeProxy(deps: LocalHandshakeDeps): Promise<void> {`
- `function startPpidWatchdogNoSocket(onDeath: () => void): void {`
- `function readHelloLine(socket: net.Socket): Promise<DaemonHello> {`
- `function pipeUntilClose(socket: net.Socket): Promise<void> {`
- `function startPpidWatchdog(socket: net.Socket): void {`
- `function parsePollMs(raw: string | undefined): number {`
- `function parseHostPpid(raw: string | undefined): number | null {`
- `function isProcessAliveLocal(pid: number): boolean {`

---

## 📄 codegraph/src/mcp/server-instructions.ts
### 🔍 结构探测
- `export const SERVER_INSTRUCTIONS = `# Codegraph — code intelligence over an indexed knowledge graph`

---

## 📄 codegraph/src/mcp/session.ts
### 🔍 结构探测
- `import * as path from 'path';`
- `import { JsonRpcRequest, JsonRpcNotification, JsonRpcTransport, ErrorCodes } from './transport';`
- `import { MCPEngine } from './engine';`
- `import { tools } from './tools';`
- `import { SERVER_INSTRUCTIONS } from './server-instructions';`
- `import { CodeGraphPackageVersion } from './version';`
- `export const SERVER_INFO = {`
- `export const PROTOCOL_VERSION = '2024-11-05';`
- `function fileUriToPath(uri: string): string {`
- `function firstRootPath(result: unknown): string | null {`
- `export interface MCPSessionOptions {`
- `export class MCPSession {`

---

## 📄 codegraph/src/mcp/tools.ts
### 🔍 结构探测
- `import type CodeGraph from '../index';`
- `import { findNearestCodeGraphRoot } from '../directory';`
- `import {`
- `type WorktreeIndexMismatch,`
- `import type { PendingFile } from '../sync';`
- `import type { Node, Edge, SearchResult, Subgraph, NodeKind } from '../types';`
- `import { isTestFile, normalizeNameToken } from '../search/query-utils';`
- `import {`
- `import { clamp, validatePathWithinRoot, validateProjectPath, isConfigLeafNode, CONFIG_LEAF_LANGUAGES } from '../utils';`
- `import { isGeneratedFile } from '../extraction/generated-detection';`
- `import { resolve as resolvePath } from 'path';`
- `function lastQualifierPart(symbol: string): string {`
- `export function getExploreBudget(fileCount: number): number {`
- `export interface ExploreOutputBudget {`
- `export function getExploreOutputBudget(fileCount: number): ExploreOutputBudget {`
- `function exploreLineNumbersEnabled(): boolean {`
- `function adaptiveExploreEnabled(): boolean {`
- `function numberSourceLines(slice: string, firstLineNumber: number): string {`
- `export function formatStaleBanner(stale: PendingFile[]): string {`
- `export function formatStaleFooter(stale: PendingFile[]): string {`
- `export interface ToolDefinition {`
- `interface PropertySchema {`
- `export interface ToolResult {`
- `export const tools: ToolDefinition[] = [`
- `export function getStaticTools(): ToolDefinition[] {`
- `export class ToolHandler {`
- `interface TreeNode {`

---

## 📄 codegraph/src/mcp/transport.ts
### 🔍 结构探测
- `import * as readline from 'readline';`
- `import type { Socket } from 'net';`
- `export interface JsonRpcRequest {`
- `export interface JsonRpcResponse {`
- `export interface JsonRpcError {`
- `export interface JsonRpcNotification {`
- `export const ErrorCodes = {`
- `export type MessageHandler = (message: JsonRpcRequest | JsonRpcNotification) => Promise<void>;`
- `export interface JsonRpcTransport {`
- `export interface StdioTransportOptions {`
- `export class StdioTransport extends LineBasedJsonRpcTransport {`
- `export class SocketTransport extends LineBasedJsonRpcTransport {`

---

## 📄 codegraph/src/mcp/version.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `function readPackageVersion(): string {`
- `export const CodeGraphPackageVersion = readPackageVersion();`

---

## 📄 codegraph/src/resolution/callback-synthesizer.ts
### 🔍 结构探测
- `import type { Edge, Node, NodeKind } from '../types';`
- `import type { QueryBuilder } from '../db/queries';`
- `import type { ResolutionContext } from './types';`
- `import { isGeneratedFile } from '../extraction/generated-detection';`
- `import { stripCommentsForRegex } from './strip-comments';`
- `function kebabToPascal(s: string): string {`
- `function nuxtComponentName(filePath: string): string | null {`
- `function sliceLines(content: string, startLine?: number, endLine?: number): string | null {`
- `function registrarField(src: string): string | null {`
- `function dispatcherField(src: string): string | null {`
- `function enclosingFn(nodesInFile: Node[], line: number): Node | null {`
- `function fieldChannelEdges(queries: QueryBuilder, ctx: ResolutionContext): Edge[] {`
- `function closureCollectionEdges(queries: QueryBuilder, ctx: ResolutionContext): Edge[] {`
- `function eventEmitterEdges(ctx: ResolutionContext): Edge[] {`
- `function reactRenderEdges(queries: QueryBuilder, ctx: ResolutionContext): Edge[] {`
- `function flutterBuildEdges(queries: QueryBuilder, ctx: ResolutionContext): Edge[] {`
- `function cppOverrideEdges(queries: QueryBuilder): Edge[] {`
- `function goImplementsEdges(queries: QueryBuilder): Edge[] {`
- `function goCrossFileMethodContainsEdges(queries: QueryBuilder): Edge[] {`
- `function kmpKindsCompatible(a: string, b: string): boolean {`
- `function kotlinExpectActualEdges(queries: QueryBuilder): Edge[] {`
- `function interfaceOverrideEdges(queries: QueryBuilder): Edge[] {`
- `function goGrpcStubImplEdges(queries: QueryBuilder): Edge[] {`
- `function reactJsxChildEdges(ctx: ResolutionContext): Edge[] {`
- `function vueTemplateEdges(ctx: ResolutionContext): Edge[] {`
- `function rnEventEdges(ctx: ResolutionContext): Edge[] {`
- `function expoCrossPlatformEdges(queries: QueryBuilder): Edge[] {`
- `function rnCrossPlatformEdges(queries: QueryBuilder): Edge[] {`
- `function fabricNativeImplEdges(ctx: ResolutionContext): Edge[] {`
- `function mybatisJavaXmlEdges(queries: QueryBuilder): Edge[] {`
- `function goBalancedArgs(s: string, openIdx: number): string | null {`
- `function goSplitArgs(args: string): string[] {`
- `function goHandlerIdent(expr: string): string | null {`
- `function ginMiddlewareChainEdges(queries: QueryBuilder, ctx: ResolutionContext): Edge[] {`
- `function pascalFormEdges(ctx: ResolutionContext): Edge[] {`
- `function svelteKitLoadEdges(ctx: ResolutionContext): Edge[] {`
- `export function synthesizeCallbackEdges(queries: QueryBuilder, ctx: ResolutionContext): number {`

---

## 📄 codegraph/src/resolution/frameworks/cargo-workspace.ts
### 🔍 结构探测
- `import picomatch from 'picomatch';`
- `import { ResolutionContext } from '../types';`
- `function getSection(content: string, sectionName: string): string | null {`
- `function extractQuotedValues(valueList: string): string[] {`
- `function escapeRegExp(value: string): string {`
- `function getArrayValue(section: string, key: string): string | null {`
- `function parseWorkspaceMembers(cargoToml: string): string[] {`
- `function parsePackageName(cargoToml: string): string | null {`
- `function addCrateAlias(map: Map<string, string>, crateName: string, memberPath: string): void {`
- `function cleanPath(memberPath: string): string {`
- `function expandGlobMember(member: string, context: ResolutionContext): string[] {`
- `function walk(dir: string, depth: number): void {`
- `function expandMembers(members: string[], context: ResolutionContext): string[] {`
- `export function getCargoWorkspaceCrateMap(context: ResolutionContext): Map<string, string> {`

---

## 📄 codegraph/src/resolution/frameworks/csharp.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `export const aspnetResolver: FrameworkResolver = {`
- `function joinCsPath(prefix: string, sub: string): string {`
- `function extractCSharpTailIdent(expr: string): string | null {`
- `function resolveByNameAndKind(`

---

## 📄 codegraph/src/resolution/frameworks/drupal.ts
### 🔍 结构探测
- `import { generateNodeId } from '../../extraction/tree-sitter-helpers';`
- `import { Node } from '../../types';`
- `import { FrameworkResolver, ResolutionContext, ResolvedRef, UnresolvedRef } from '../types';`
- `function lastSegment(fqcn: string): string | null {`
- `function moduleNameFromPath(filePath: string): string | null {`
- `function extractDrupalRoutes(`
- `type PendingRoute = { name: string; lineNum: number };`
- `function isDrupalHookFile(filePath: string): boolean {`
- `function extractDrupalHooks(`
- `export const drupalResolver: FrameworkResolver = {`

---

## 📄 codegraph/src/resolution/frameworks/expo-modules.ts
### 🔍 结构探测
- `import type { Node } from '../../types';`
- `import {`
- `function isExpoModuleSource(source: string): boolean {`
- `function extractExpoMethods(filePath: string, source: string, language: 'swift' | 'kotlin'): Node[] {`
- `export const expoModulesResolver: FrameworkResolver = {`

---

## 📄 codegraph/src/resolution/frameworks/express.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `function extractTailIdent(expr: string): string | null {`
- `function matchDelim(s: string, open: number, oc: string, cc: string): number {`
- `export const expressResolver: FrameworkResolver = {`
- `function isMiddlewareName(name: string): boolean {`
- `function resolveMiddleware(`
- `function resolveControllerMethod(`
- `function resolveServiceMethod(`
- `function detectLanguage(filePath: string): 'typescript' | 'javascript' {`

---

## 📄 codegraph/src/resolution/frameworks/fabric.ts
### 🔍 结构探测
- `import type { Node } from '../../types';`
- `import {`
- `function deriveComponentNameFromManager(className: string): string {`
- `function isFabricSpec(source: string): boolean {`
- `function findNativePropsBody(source: string): string | null {`
- `function extractPropNames(body: string): string[] {`
- `function extractLegacyViewManagerNodes(filePath: string, source: string): Node[] {`
- `function extractJvmViewManagerNodes(filePath: string, source: string): Node[] {`
- `function extractFabricNodes(filePath: string, source: string): Node[] {`
- `export const fabricViewResolver: FrameworkResolver = {`

---

## 📄 codegraph/src/resolution/frameworks/go.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `export const goResolver: FrameworkResolver = {`
- `function extractGoTailIdent(expr: string): string | null {`
- `function resolveByNameAndKind(`

---

## 📄 codegraph/src/resolution/frameworks/index.ts
### 🔍 结构探测
- `import { FrameworkResolver, ResolutionContext } from '../types';`
- `import type { Language } from '../../types';`
- `import { drupalResolver } from './drupal';`
- `import { laravelResolver } from './laravel';`
- `import { expressResolver } from './express';`
- `import { nestjsResolver } from './nestjs';`
- `import { reactResolver } from './react';`
- `import { svelteResolver } from './svelte';`
- `import { vueResolver } from './vue';`
- `import { djangoResolver, flaskResolver, fastapiResolver } from './python';`
- `import { railsResolver } from './ruby';`
- `import { springResolver } from './java';`
- `import { playResolver } from './play';`
- `import { goResolver } from './go';`
- `import { rustResolver } from './rust';`
- `import { aspnetResolver } from './csharp';`
- `import { swiftUIResolver, uikitResolver, vaporResolver } from './swift';`
- `import { swiftObjcBridgeResolver } from './swift-objc';`
- `import { reactNativeBridgeResolver } from './react-native';`
- `import { expoModulesResolver } from './expo-modules';`
- `import { fabricViewResolver } from './fabric';`
- `export function getAllFrameworkResolvers(): FrameworkResolver[] {`
- `export function getFrameworkResolver(name: string): FrameworkResolver | undefined {`
- `export function detectFrameworks(context: ResolutionContext): FrameworkResolver[] {`
- `export function getApplicableFrameworks(`
- `export function registerFrameworkResolver(resolver: FrameworkResolver): void {`
- `export { drupalResolver } from './drupal';`
- `export { laravelResolver, FACADE_MAPPINGS } from './laravel';`
- `export { expressResolver } from './express';`
- `export { nestjsResolver } from './nestjs';`
- `export { reactResolver } from './react';`
- `export { svelteResolver } from './svelte';`
- `export { vueResolver } from './vue';`
- `export { djangoResolver, flaskResolver, fastapiResolver } from './python';`
- `export { railsResolver } from './ruby';`
- `export { springResolver } from './java';`
- `export { playResolver } from './play';`
- `export { goResolver } from './go';`
- `export { rustResolver } from './rust';`
- `export { aspnetResolver } from './csharp';`
- `export { swiftUIResolver, uikitResolver, vaporResolver } from './swift';`
- `export { swiftObjcBridgeResolver } from './swift-objc';`
- `export { reactNativeBridgeResolver } from './react-native';`
- `export { expoModulesResolver } from './expo-modules';`
- `export { fabricViewResolver } from './fabric';`

---

## 📄 codegraph/src/resolution/frameworks/java.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `export const springResolver: FrameworkResolver = {`
- `function isSpringConfigFile(filePath: string): boolean {`
- `function extractSpringConfig(`
- `function extractSpringValueBindings(`
- `function canonicalConfigKey(key: string): string {`
- `function parseMappingPath(args: string): string {`
- `function joinPath(prefix: string, sub: string): string {`
- `function resolveByNameAndKind(`

---

## 📄 codegraph/src/resolution/frameworks/laravel.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `export const FACADE_MAPPINGS: Record<string, string> = {`
- `export const laravelResolver: FrameworkResolver = {`
- `function extractLaravelHandler(expr: string): string | null {`
- `function resolveModelCall(`
- `function resolveControllerMethod(`

---

## 📄 codegraph/src/resolution/frameworks/nestjs.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import {`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `type JsLang = 'typescript' | 'javascript';`
- `export const nestjsResolver: FrameworkResolver = {`
- `interface DecoratorHit {`
- `function findDecorators(safe: string, names: string[]): DecoratorHit[] {`
- `function readArgs(s: string, openIndex: number): { args: string; end: number } | null {`
- `function methodNameAfter(safe: string, start: number): string | null {`
- `type ClassKind = 'controller' | 'resolver' | 'gateway' | 'other';`
- `interface ClassScope {`
- `function buildClassScopes(safe: string): ClassScope[] {`
- `function scopeFor(scopes: ClassScope[], index: number): ClassScope | null {`
- `function parseStringArg(args: string): string {`
- `function parseControllerPrefix(args: string): string {`
- `function parseGatewayNamespace(args: string): string {`
- `function parseGraphqlName(args: string, handler: string | null): string {`
- `function joinHttpPath(prefix: string, sub: string): string {`
- `function lineAt(safe: string, index: number): number {`
- `function detectLanguage(filePath: string): JsLang {`
- `function collectRouterModuleRegistrations(safe: string, out: Map<string, string>): void {`
- `interface RouteItem {`
- `function parseRoutesArray(args: string): RouteItem[] {`
- `function parseRouteObjects(s: string): RouteItem[] {`
- `function walkRoutesTree(`
- `function collectModuleControllers(safe: string, out: Map<string, string>): void {`
- `function parseControllersField(args: string): string[] {`
- `function classNameAfter(safe: string, start: number): string | null {`
- `function applyModulePrefix(route: Node, prefix: string): Node | null {`
- `function matchingClose(s: string, open: number): number {`
- `function splitTopLevelObjects(s: string): string[] {`
- `function parseStringField(obj: string, name: string): string {`
- `function parseIdentField(obj: string, name: string): string | null {`
- `function parseArrayField(obj: string, name: string): string | null {`

---

## 📄 codegraph/src/resolution/frameworks/play.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, ResolutionContext, ResolvedRef, UnresolvedRef } from '../types';`
- `import { isPlayRoutesFile } from '../../extraction/grammars';`
- `export const playResolver: FrameworkResolver = {`

---

## 📄 codegraph/src/resolution/frameworks/python.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolutionContext, FrameworkExtractionResult } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `export const djangoResolver: FrameworkResolver = {`
- `function resolveModelIterableIter(context: ResolutionContext): string | null {`
- `function resolveHandlerName(expr: string): { name: string; kind: 'references' | 'imports' } | null {`
- `export const flaskResolver: FrameworkResolver = {`
- `export const fastapiResolver: FrameworkResolver = {`
- `interface DecoratorRouteOpts {`
- `function extractDecoratorRoutes(filePath: string, content: string, opts: DecoratorRouteOpts): FrameworkExtractionResult {`
- `function extractFlaskRestful(filePath: string, safe: string): FrameworkExtractionResult {`
- `function resolveByNameAndKind(`

---

## 📄 codegraph/src/resolution/frameworks/react-native.ts
### 🔍 结构探测
- `import type { Node } from '../../types';`
- `import {`
- `interface NativeMethod {`
- `function defaultObjcModuleName(className: string): string {`
- `function parseObjcRNExports(`
- `function findObjcClassName(source: string): string | null {`
- `function parseJvmRNExports(`
- `function parseTurboModuleSpec(`
- `function buildRNMaps(context: ResolutionContext): { byJsName: Map<string, NativeMethod[]> } {`
- `export const reactNativeBridgeResolver: FrameworkResolver = {`

---

## 📄 codegraph/src/resolution/frameworks/react.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `export const reactResolver: FrameworkResolver = {`
- `function isPascalCase(str: string): boolean {`
- `function isBuiltInType(name: string): boolean {`
- `function resolveComponent(`
- `function resolveHook(name: string, context: ResolutionContext): string | null {`
- `function resolveContext(name: string, context: ResolutionContext): string | null {`
- `function filePathToRoute(filePath: string): string | null {`

---

## 📄 codegraph/src/resolution/frameworks/ruby.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `export const railsResolver: FrameworkResolver = {`
- `function pluralize(w: string): string {`
- `function camelize(s: string): string {`
- `function resolveControllerAction(ctrlPath: string, action: string, context: ResolutionContext): string | null {`
- `function resolveModel(name: string, context: ResolutionContext): string | null {`
- `function resolveController(name: string, context: ResolutionContext): string | null {`
- `function resolveHelper(name: string, context: ResolutionContext): string | null {`
- `function resolveService(name: string, context: ResolutionContext): string | null {`

---

## 📄 codegraph/src/resolution/frameworks/rust.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `import { getCargoWorkspaceCrateMap } from './cargo-workspace';`
- `function getCachedCargoWorkspaceCrateMap(context: ResolutionContext): Map<string, string> {`
- `export const rustResolver: FrameworkResolver = {`
- `function findMatchingParen(s: string, openIdx: number): number {`
- `function resolveByNameAndKind(`
- `interface ModuleResolution {`
- `function resolveModule(name: string, context: ResolutionContext): ModuleResolution | null {`

---

## 📄 codegraph/src/resolution/frameworks/svelte.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `export const svelteResolver: FrameworkResolver = {`
- `function isRuneReference(name: string): boolean {`
- `function isPascalCase(str: string): boolean {`
- `function resolveComponent(`
- `function getSvelteKitRouteInfo(fileName: string): string | null {`
- `function filePathToSvelteKitRoute(filePath: string): string | null {`

---

## 📄 codegraph/src/resolution/frameworks/swift-objc.ts
### 🔍 结构探测
- `import { FrameworkResolver, ResolutionContext, ResolvedRef, UnresolvedRef } from '../types';`
- `import type { Node } from '../../types';`
- `import {`
- `function buildObjcMap(context: ResolutionContext): Map<string, Node[]> {`
- `function declarationSourceWindow(node: Node, context: ResolutionContext): string {`
- `function resolveSwiftCallToObjc(`
- `function resolveObjcCallToSwift(`
- `export const swiftObjcBridgeResolver: FrameworkResolver = {`

---

## 📄 codegraph/src/resolution/frameworks/swift.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `import { stripCommentsForRegex } from '../strip-comments';`
- `export const swiftUIResolver: FrameworkResolver = {`
- `export const uikitResolver: FrameworkResolver = {`
- `export const vaporResolver: FrameworkResolver = {`
- `function resolveByNameAndKind(`

---

## 📄 codegraph/src/resolution/frameworks/vue.ts
### 🔍 结构探测
- `import { Node } from '../../types';`
- `import { FrameworkResolver, UnresolvedRef, ResolvedRef, ResolutionContext } from '../types';`
- `export const vueResolver: FrameworkResolver = {`
- `function isPascalCase(str: string): boolean {`
- `function resolveComponent(`
- `function filePathToNuxtRoute(normalized: string, afterPagesStart: number): string | null {`

---

## 📄 codegraph/src/resolution/go-module.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `export interface GoModule {`
- `export function loadGoModule(projectRoot: string): GoModule | null {`

---

## 📄 codegraph/src/resolution/import-resolver.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { Language, Node } from '../types';`
- `import { UnresolvedRef, ResolvedRef, ResolutionContext, ImportMapping, ReExport } from './types';`
- `import { applyAliases } from './path-aliases';`
- `import { resolveWorkspaceImport } from './workspace-packages';`
- `export function resolveImportPath(`
- `function isExternalImport(`
- `function resolveRelativeImport(`
- `function resolveAliasedImport(`
- `export function clearCppIncludeDirCache(): void {`
- `export function loadCppIncludeDirs(projectRoot: string): string[] {`
- `function loadCppIncludeDirsFromCompileDB(projectRoot: string): string[] | null {`
- `function shlexSplit(cmd: string): string[] {`
- `function loadCppIncludeDirsHeuristic(projectRoot: string): string[] {`
- `function resolveCppIncludePath(`
- `export function isPhpIncludePathRef(ref: UnresolvedRef): boolean {`
- `function resolvePhpIncludePath(`
- `export function extractImportMappings(`
- `function extractJSImports(content: string): ImportMapping[] {`
- `function extractPythonImports(content: string): ImportMapping[] {`
- `function extractGoImports(content: string): ImportMapping[] {`
- `function extractJavaImports(content: string): ImportMapping[] {`
- `function extractPHPImports(content: string): ImportMapping[] {`
- `function extractCppImports(content: string): ImportMapping[] {`
- `export function clearImportMappingCache(): void {`
- `function stripJsComments(content: string): string {`
- `export function extractReExports(content: string, language: Language): ReExport[] {`
- `export function resolveJvmImport(`
- `function pickClosestJvmCandidate(candidates: Node[], fromPath: string): Node {`
- `export function resolveViaImport(`
- `function resolvePythonModuleMember(`
- `function resolveLuaRequire(ref: UnresolvedRef, context: ResolutionContext): ResolvedRef | null {`
- `function resolveModuleImportToFile(`
- `function findPythonModuleFile(`
- `function resolvePythonAbsoluteModule(`
- `function resolveRustPathReference(`
- `function rustCrateRootDir(fromFileAbs: string, context: ResolutionContext): string | null {`
- `function rustSelfModuleDir(fromFileAbs: string): string {`
- `function resolveRustModuleFile(`
- `function resolveJavaImportedReference(`
- `function resolveGoCrossPackageReference(`
- `function findExportedSymbol(`

---

## 📄 codegraph/src/resolution/index.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { Node, UnresolvedReference, Edge } from '../types';`
- `import { QueryBuilder } from '../db/queries';`
- `import {`
- `import { matchReference, matchDottedCallChain, matchScopedCallChain, sameLanguageFamily, crossesKnownFamily } from './name-matcher';`
- `import { resolveViaImport, resolveJvmImport, extractImportMappings, extractReExports, loadCppIncludeDirs, isPhpIncludePathRef } from './import-resolver';`
- `import { detectFrameworks } from './frameworks';`
- `import { synthesizeCallbackEdges } from './callback-synthesizer';`
- `import { loadProjectAliases, type AliasMap } from './path-aliases';`
- `import { loadGoModule, type GoModule } from './go-module';`
- `import { loadWorkspacePackages, type WorkspacePackages } from './workspace-packages';`
- `import { logDebug } from '../errors';`
- `import type { ReExport } from './types';`
- `import { LRUCache } from './lru-cache';`
- `function resolveCacheLimit(): number {`
- `export * from './types';`
- `export class ReferenceResolver {`
- `export function createResolver(projectRoot: string, queries: QueryBuilder): ReferenceResolver {`

---

## 📄 codegraph/src/resolution/lru-cache.ts
### 🔍 结构探测
- `export class LRUCache<K, V> {`

---

## 📄 codegraph/src/resolution/name-matcher.ts
### 🔍 结构探测
- `import { Node } from '../types';`
- `import { UnresolvedRef, ResolvedRef, ResolutionContext } from './types';`
- `export function matchByFilePath(`
- `function pickClosestFileNode(candidates: Node[], ref: UnresolvedRef): Node {`
- `export function sameLanguageFamily(a: string, b: string): boolean {`
- `export function isKnownLanguageFamily(lang: string): boolean {`
- `export function crossesKnownFamily(a: string, b: string): boolean {`
- `function applyLanguageGate(candidates: Node[], ref: UnresolvedRef): Node[] {`
- `export function matchByExactName(`
- `export function matchByQualifiedName(`
- `function resolveMethodOnType(`
- `function normalizeCppTypeName(typeName: string): string | null {`
- `function buildDeclaratorRegex(escapedReceiver: string): RegExp {`
- `function inferCppReceiverType(`
- `function cppLastSegment(name: string): string {`
- `function lookupCalleeReturnType(`
- `function cppClassExists(name: string, ref: UnresolvedRef, context: ResolutionContext): boolean {`
- `function resolveCppCallResultType(`
- `function inferCppAutoInitializerType(`
- `export function matchCppCallChain(`
- `export function matchScopedCallChain(`
- `export function matchDottedCallChain(`
- `function importedFqnOf(`
- `function inferJavaFieldReceiverType(`
- `export function matchMethodCall(`
- `function splitCamelCase(str: string): string[] {`
- `function computePathProximity(filePath1: string, filePath2: string): number {`
- `function findBestMatch(`
- `export function matchFuzzy(`
- `export function matchReference(`

---

## 📄 codegraph/src/resolution/path-aliases.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { logDebug } from '../errors';`
- `export interface AliasPattern {`
- `export interface AliasMap {`
- `function stripJsonc(src: string): string {`
- `interface RawTsconfig {`
- `function readTsconfigLike(filePath: string): RawTsconfig | null {`
- `function splitWildcard(pattern: string): {`
- `export function loadProjectAliases(projectRoot: string): AliasMap | null {`
- `export function applyAliases(`

---

## 📄 codegraph/src/resolution/strip-comments.ts
### 🔍 结构探测
- `export type CommentLang =`
- `export function stripCommentsForRegex(content: string, lang: CommentLang): string {`
- `function blankRange(buf: string[], start: number, end: number, src: string): void {`
- `function stripPython(src: string): string {`
- `function stripRuby(src: string): string {`
- `function stripCStyle(src: string, allowSingleQuoteStrings: boolean): string {`
- `function stripPhp(src: string): string {`
- `function stripGo(src: string): string {`
- `function stripRust(src: string): string {`

---

## 📄 codegraph/src/resolution/swift-objc-bridge.ts
### 🔍 结构探测
- `function capFirst(s: string): string {`
- `function lowerFirst(s: string): string {`
- `export function objcSelectorForSwiftMethod(`
- `export function objcSelectorForSwiftInit(`
- `export function objcAccessorsForSwiftProperty(`
- `export function swiftBaseNamesForObjcSelector(selector: string): string[] {`
- `export function detectExplicitObjcName(sourceSlice: string): string | null {`
- `export function isObjcExposed(sourceSlice: string): boolean {`

---

## 📄 codegraph/src/resolution/types.ts
### 🔍 结构探测
- `import { EdgeKind, Language, Node } from '../types';`
- `export interface UnresolvedRef {`
- `export interface ResolvedRef {`
- `export interface ResolutionResult {`
- `export interface ResolutionContext {`
- `export interface FrameworkExtractionResult {`
- `export interface FrameworkResolver {`
- `export interface ImportMapping {`
- `export type ReExport =`

---

## 📄 codegraph/src/resolution/workspace-packages.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { logDebug } from '../errors';`
- `export interface WorkspacePackages {`
- `export function loadWorkspacePackages(projectRoot: string): WorkspacePackages | null {`
- `export function resolveWorkspaceImport(`
- `function readWorkspaceGlobs(projectRoot: string): string[] {`
- `function parsePnpmPackages(yaml: string): string[] {`
- `function expandWorkspaceGlob(projectRoot: string, pattern: string): string[] {`
- `function readPackageName(dirAbs: string): string | null {`

---

## 📄 codegraph/src/search/query-parser.ts
### 🔍 结构探测
- `import { NODE_KINDS, LANGUAGES } from '../types';`
- `import type { NodeKind, Language } from '../types';`
- `export interface ParsedQuery {`
- `function unquote(s: string): string {`
- `export function parseQuery(raw: string): ParsedQuery {`
- `export function boundedEditDistance(a: string, b: string, maxDist: number): number {`

---

## 📄 codegraph/src/search/query-utils.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { Node } from '../types';`
- `export function normalizeNameToken(raw: string): string {`
- `export function deriveProjectNameTokens(projectRoot: string): Set<string> {`
- `export const STOP_WORDS = new Set([`
- `export function getStemVariants(term: string): string[] {`
- `export function extractSearchTerms(query: string, options?: { stems?: boolean }): string[] {`
- `export function scorePathRelevance(`
- `export function isTestFile(filePath: string): boolean {`
- `function matchesNonProductionDir(lowerPath: string): boolean {`
- `export function nameMatchBonus(nodeName: string, query: string): number {`
- `export function kindBonus(kind: Node['kind']): number {`
- `export function isDistinctiveIdentifier(token: string): boolean {`

---

## 📄 codegraph/src/sync/git-hooks.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { execFileSync } from 'child_process';`
- `export type GitHookName = 'post-commit' | 'post-merge' | 'post-checkout';`
- `export const DEFAULT_SYNC_HOOKS: GitHookName[] = ['post-commit', 'post-merge', 'post-checkout'];`
- `export interface GitHookResult {`
- `export function isGitRepo(projectRoot: string): boolean {`
- `function gitHooksDir(projectRoot: string): string | null {`
- `function markerBlock(): string {`
- `function stripMarkerBlock(content: string): string {`
- `function isEffectivelyEmpty(content: string): boolean {`
- `function chmodExecutable(file: string): void {`
- `export function installGitSyncHook(`
- `export function removeGitSyncHook(`
- `export function isSyncHookInstalled(`

---

## 📄 codegraph/src/sync/index.ts
### 🔍 结构探测
- `export { FileWatcher, WatchOptions, PendingFile, LockUnavailableError } from './watcher';`
- `export { watchDisabledReason, detectWsl } from './watch-policy';`
- `export {`
- `type GitHookName,`
- `type GitHookResult,`
- `export {`
- `type WorktreeIndexMismatch,`

---

## 📄 codegraph/src/sync/watch-policy.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import { normalizePath } from '../utils';`
- `export function detectWsl(): boolean {`
- `function isWindowsDriveMount(projectRoot: string): boolean {`
- `export interface WatchProbe {`
- `export function watchDisabledReason(projectRoot: string, probe: WatchProbe = {}): string | null {`
- `export function __resetWslCacheForTests(): void {`

---

## 📄 codegraph/src/sync/watcher.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import type { Ignore } from 'ignore';`
- `import { isSourceFile, buildDefaultIgnore } from '../extraction';`
- `import { logDebug, logWarn } from '../errors';`
- `import { normalizePath } from '../utils';`
- `import { isCodeGraphDataDir } from '../directory';`
- `import { watchDisabledReason } from './watch-policy';`
- `function supportsRecursiveWatch(): boolean {`
- `function maxDirWatches(): number {`
- `export interface WatchOptions {`
- `export class LockUnavailableError extends Error {`
- `export interface PendingFile {`
- `export class FileWatcher {`
- `export function __emitWatchEventForTests(projectRoot: string, relPath: string): boolean {`

---

## 📄 codegraph/src/sync/worktree.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import { execFileSync } from 'child_process';`
- `export function gitWorktreeRoot(dir: string): string | null {`
- `export interface WorktreeIndexMismatch {`
- `export function detectWorktreeIndexMismatch(`
- `export function worktreeMismatchWarning(m: WorktreeIndexMismatch): string {`
- `export function worktreeMismatchNotice(m: WorktreeIndexMismatch): string {`
- `function realpath(p: string): string {`

---

## 📄 codegraph/src/types.ts
### 🔍 结构探测
- `export const NODE_KINDS = [`
- `export type NodeKind = (typeof NODE_KINDS)[number];`
- `export type EdgeKind =`
- `export const LANGUAGES = [`
- `export type Language = (typeof LANGUAGES)[number];`
- `export interface Node {`
- `export interface Edge {`
- `export interface FileRecord {`
- `export interface ExtractionResult {`
- `export interface ExtractionError {`
- `export interface UnresolvedReference {`
- `export interface Subgraph {`
- `export interface TraversalOptions {`
- `export interface SearchOptions {`
- `export interface SearchResult {`
- `export interface Context {`
- `export interface CodeBlock {`
- `export interface SchemaVersion {`
- `export interface GraphStats {`
- `export type TaskInput = string | { title: string; description?: string };`
- `export interface BuildContextOptions {`
- `export interface TaskContext {`
- `export interface FindRelevantContextOptions {`

---

## 📄 codegraph/src/ui/glyphs.ts
### 🔍 结构探测
- `export function supportsUnicode(): boolean {`
- `export interface Glyphs {`
- `export const UNICODE_GLYPHS: Glyphs = {`
- `export const ASCII_GLYPHS: Glyphs = {`
- `export function getGlyphs(): Glyphs {`
- `export function _resetGlyphsCache(): void {`

---

## 📄 codegraph/src/ui/shimmer-progress.ts
### 🔍 结构探测
- `import { Worker } from 'worker_threads';`
- `import * as path from 'path';`
- `export interface IndexProgress {`
- `export interface ShimmerProgress {`
- `export function createShimmerProgress(): ShimmerProgress {`

---

## 📄 codegraph/src/ui/shimmer-worker.ts
### 🔍 结构探测
- `import { parentPort, workerData } from 'worker_threads';`
- `import { writeSync } from 'fs';`
- `import { getGlyphs } from './glyphs';`
- `import type { ShimmerWorkerMessage } from './types';`
- `function writeStdout(s: string): void {`
- `function animFrame(): number {`
- `function lerp(a: number, b: number, t: number): number {`
- `function shimmerColor(frame: number): string {`
- `function formatNumber(n: number): string {`
- `function renderBar(frame: number, filled: number, empty: number): string {`
- `function render(): void {`
- `function finishPhase(): void {`

---

## 📄 codegraph/src/ui/types.ts
### 🔍 结构探测
- `export type ShimmerWorkerMessage =`
- `export type ShimmerMainMessage =`

---

## 📄 codegraph/src/upgrade/index.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `import * as https from 'https';`
- `import { spawnSync } from 'child_process';`
- `export const REPO = 'colbymchenry/codegraph';`
- `export const NPM_PACKAGE = '@colbymchenry/codegraph';`
- `export const INSTALL_SH_URL = `${RAW_BASE}/install.sh`;`
- `export type InstallMethod =`
- `export interface DetectInput {`
- `function toPosix(p: string): string {`
- `export function deriveInstallDir(`
- `export function detectInstallMethod(input: DetectInput): InstallMethod {`
- `export interface Semver {`
- `export function parseSemver(version: string): Semver | null {`
- `export function compareVersions(a: string, b: string): number {`
- `export function isUpdateAvailable(current: string, latest: string): boolean {`
- `export function normalizeVersion(v: string): string {`
- `export function stripV(v: string): string {`
- `export function parseLatestTagFromLocation(location: string | undefined): string | null {`
- `function httpsGet(`
- `export async function resolveLatestVersion(repo = REPO, timeoutMs = 12000): Promise<string> {`
- `export interface UpgradeOptions {`
- `export interface UpgradeDeps {`
- `export function reindexAdvisory(): string {`
- `export async function runUpgrade(opts: UpgradeOptions, deps: UpgradeDeps): Promise<number> {`
- `function upgradeUnixBundle(`
- `export function buildWindowsUpgradeScript(bundleRoot: string, version: string, arch: string): string {`
- `function upgradeWindowsBundle(`
- `function upgradeNpm(`
- `export function hasCommand(cmd: string): boolean {`
- `export function defaultRun(cmd: string, args: string[], env?: NodeJS.ProcessEnv): number {`

---

## 📄 codegraph/src/utils.ts
### 🔍 结构探测
- `import * as fs from 'fs';`
- `import * as path from 'path';`
- `export const CONFIG_LEAF_LANGUAGES: ReadonlySet<string> = new Set(['yaml', 'properties']);`
- `export function isConfigLeafNode(node: { kind: string; language?: string }): boolean {`
- `function isWithinDir(child: string, parent: string): boolean {`
- `export function validatePathWithinRoot(projectRoot: string, filePath: string): string | null {`
- `export function validateProjectPath(dirPath: string): string | null {`
- `export function safeJsonParse<T>(value: string, fallback: T): T {`
- `export function clamp(value: number, min: number, max: number): number {`
- `export function normalizePath(filePath: string): string {`
- `export class FileLock {`
- `export async function processInBatches<T, R>(`
- `export class Mutex {`
- `export async function* readFileInChunks(`
- `export function debounce<T extends (...args: unknown[]) => unknown>(`
- `export function throttle<T extends (...args: unknown[]) => unknown>(`
- `export function estimateSize(obj: unknown): number {`
- `function sizeOf(value: unknown): number {`
- `export class MemoryMonitor {`

---

## 📄 codegraph/src/web-tree-sitter.d.ts
### 🔍 结构探测
- `export interface Point {`
- `export interface Range {`
- `export interface Edit {`
- `export type ParseCallback = (index: number, position: Point) => string | undefined;`
- `export interface ParseOptions {`
- `export interface EmscriptenModule {`
- `export class Parser {`
- `export class Language {`
- `export class Tree {`
- `export class Node {`
- `export class TreeCursor {`

---
