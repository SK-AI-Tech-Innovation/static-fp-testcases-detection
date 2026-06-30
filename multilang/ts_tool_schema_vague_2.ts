// ACE-EXPECT: detect
// CATEGORY: should_detect/tool_schema_vague
// LANGUAGE: typescript
// ISSUE: An Anthropic tool's input_schema uses a single freeform string "query" with no description and a catch-all object "options" with no properties or enums.
// EXPECTED-FINDING: Tool schema has no field descriptions, no enums for constrained options, and an untyped freeform options object — the model cannot reliably populate it.
// EXPECTED-FIX: Add a clear tool description, per-property descriptions, enums for bounded choices, explicit option fields with types, and a required array.
// SEVERITY-HINT: warning
/** Anthropic "search_db" tool with a vague schema and no descriptions. */
import Anthropic from "@anthropic-ai/sdk";
import type { Tool } from "@anthropic-ai/sdk/resources/messages";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const tools: Tool[] = [
  {
    name: "search_db",
    description: "search",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string" },
        options: { type: "object" },
      },
    },
  },
];

export async function search(userPrompt: string) {
  return anthropic.messages.create({
    model: "claude-opus-4-20250514",
    max_tokens: 1024,
    tools,
    messages: [{ role: "user", content: userPrompt }],
  });
}
