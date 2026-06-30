// ACE-EXPECT: detect
// CATEGORY: should_detect/prompt_few_shot
// LANGUAGE: typescript
// ISSUE: A complex multi-field entity-extraction prompt gives only instructions and zero few-shot examples to anchor format and edge cases.
// EXPECTED-FINDING: A complex extraction task is driven by instructions alone with no few-shot examples, hurting format consistency and edge-case handling.
// EXPECTED-FIX: Add 2-3 representative input/output few-shot examples (including a tricky case) before the user input to demonstrate the exact expected format.
// SEVERITY-HINT: suggestion
/** Extracts structured contact records from messy text with no examples. */
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const SYSTEM_PROMPT = `You are an information extraction engine.
From the user's text, extract every person mentioned and produce a JSON array.
For each person include: fullName, role, company, email, phone, and confidence (0-1).
Normalize phone numbers to E.164. Leave fields null when not present.
Resolve coreferences (e.g. "she", "the CTO") to the correct person.`;

export async function extractContacts(text: string) {
  // No few-shot examples for a non-trivial multi-field, coreference task.
  const completion = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: SYSTEM_PROMPT },
      { role: "user", content: text },
    ],
  });

  return completion.choices[0].message.content ?? "[]";
}
