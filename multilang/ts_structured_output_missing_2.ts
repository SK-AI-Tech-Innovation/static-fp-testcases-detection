// ACE-EXPECT: detect
// CATEGORY: should_detect/structured_output_missing
// LANGUAGE: typescript
// ISSUE: A classification label is scraped out of model prose with a regex instead of using structured output, so any phrasing drift breaks parsing.
// EXPECTED-FINDING: Model output is parsed by a brittle regex with no structured-output enforcement (response_format/tool schema) or zod validation of the extracted value.
// EXPECTED-FIX: Request a json_schema / json_object response constraining the label to an enum, then validate with a zod enum schema instead of regex scraping.
// SEVERITY-HINT: warning
/** Classifies a support ticket priority by regex-scraping the model's text. */
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

export async function classifyPriority(ticket: string): Promise<string> {
  const message = await anthropic.messages.create({
    model: "claude-opus-4-20250514",
    max_tokens: 256,
    messages: [
      {
        role: "user",
        content: `Classify this ticket priority as one of low/medium/high.\n\n${ticket}`,
      },
    ],
  });

  const text = message.content
    .filter((block) => block.type === "text")
    .map((block) => (block as { text: string }).text)
    .join("");

  // Brittle: pull the label out of arbitrary prose with a regex, no schema.
  const match = text.match(/priority\s*[:=-]?\s*(low|medium|high)/i);
  const priority = match ? match[1].toLowerCase() : "unknown";
  return priority;
}
