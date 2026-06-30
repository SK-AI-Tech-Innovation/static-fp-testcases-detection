// ACE-EXPECT: detect
// CATEGORY: should_detect/tool_schema_vague
// LANGUAGE: typescript
// ISSUE: An OpenAI function-calling tool declares a bare generic object parameter ("args": { type: "object" }) with no properties, descriptions, required list, or enums.
// EXPECTED-FINDING: Tool definition exposes an untyped freeform object parameter with no property schema or descriptions, giving the model no guidance and disabling validation.
// EXPECTED-FIX: Define explicit named properties with types, per-field descriptions, enums for constrained values, a required array, and additionalProperties: false.
// SEVERITY-HINT: warning
/** Defines a "create_ticket" tool whose parameters are an opaque object. */
import OpenAI from "openai";
import type { ChatCompletionTool } from "openai/resources/chat/completions";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const tools: ChatCompletionTool[] = [
  {
    type: "function",
    function: {
      name: "create_ticket",
      // No description of fields, no enum for status/priority, no required list.
      parameters: {
        type: "object",
        properties: {
          args: { type: "object" },
        },
      },
    },
  },
];

export async function runAgent(userMessage: string) {
  return client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: userMessage }],
    tools,
    tool_choice: "auto",
  });
}
