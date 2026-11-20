// Execute the unmodified upstream JIT helper with a controlled manager.
import assert from "node:assert/strict";
import { writeFileSync } from "node:fs";
import { discoverJitContext, appendJitContext, appendJitContextToParts } from "../raw/sources/2026-11-18/J01.ts";

const calls: unknown[] = [];
const manager = { discoverContext(path: string, roots: string[]) {
  calls.push({path, roots});
  return "Run compatibility check";
}};
const config = {
  getMemoryContextManager: () => manager,
  getWorkspaceContext: () => ({getDirectories: () => ["/fixture"]})
};
const target = "/fixture/pkg/module.ts";
const note = await discoverJitContext(config as any, target);
assert.deepEqual(calls, [{path: target, roots: ["/fixture"]}]);
assert.match(appendJitContext("module body", note), /module body[\s\S]+Run compatibility check/);
assert.equal(appendJitContext("module body", ""), "module body");
assert.equal(appendJitContextToParts([{text:"body"}], note).length, 2);
const failing = {...config, getMemoryContextManager: () => ({discoverContext: () => { throw new Error("fixture"); }})};
assert.equal(await discoverJitContext(failing as any, target), "");
assert.equal(await discoverJitContext({getMemoryContextManager:()=>undefined} as any, target), "");
const result = {runtime:"Bun "+Bun.version, source:"J01", controlled_manager:true, assertions:6, outcome:"passed", calls, model_calls:0};
writeFileSync(new URL("../state/jit-check.json",import.meta.url),JSON.stringify(result,null,2));
console.log(result);
