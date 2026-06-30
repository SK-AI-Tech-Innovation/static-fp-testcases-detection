// ACE-EXPECT: detect
// CATEGORY: should_detect/structured_output_missing
// LANGUAGE: typescript
// ISSUE: The model is asked to return JSON but the reply is parsed with raw JSON.parse() and no response_format / JSON mode / schema validation is used.
// EXPECTED-FINDING: Untrusted model text is fed directly into JSON.parse() with no structured-output enforcement (response_format) or schema (zod) validation.
// EXPECTED-FIX: Enforce structured output via response_format: { type: "json_object" } (or a json_schema) and validate the parsed object with a zod schema before use.
// SEVERITY-HINT: warning
/** Extracts invoice fields from free text and blindly JSON.parses the reply. */
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

interface Invoice {
  vendor: string;
  total: number;
  dueDate: string;
}

export async function extractInvoice(rawText: string): Promise<Invoice> {
  const completion = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      {
        role: "system",
        content: "Extract the invoice vendor, total and dueDate. Reply with JSON.",
      },
      { role: "user", content: rawText },
    ],
  });

  const content = completion.choices[0].message.content ?? "";
  // No response_format, no schema — just trust whatever the model emitted.
  const parsed = JSON.parse(content) as Invoice;
  return {
    vendor: parsed.vendor,
    total: parsed.total,
    dueDate: parsed.dueDate,
  };
}
