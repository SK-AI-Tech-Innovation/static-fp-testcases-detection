// ACE-EXPECT: detect
// CATEGORY: should_detect/no_retry_fallback
// LANGUAGE: typescript
// ISSUE: An Anthropic call inside a loop over many items has no per-item try/catch, retry, or fallback, so one failure aborts the whole batch.
// EXPECTED-FINDING: LLM call lacks retry/backoff and error isolation; a single transient failure (overloaded_error/429) terminates the entire batch with no fallback.
// EXPECTED-FIX: Wrap each call in try/catch, add exponential-backoff retries for retryable errors, and continue with a fallback value so one failure doesn't fail the batch.
// SEVERITY-HINT: warning
/** Generates a tagline per product with no retry or fallback handling. */
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

export async function generateTaglines(products: string[]): Promise<string[]> {
  const results: string[] = [];

  for (const product of products) {
    // No retry, no try/catch, no fallback — first failure throws out of the loop.
    const message = await anthropic.messages.create({
      model: "claude-opus-4-20250514",
      max_tokens: 64,
      messages: [
        { role: "user", content: `Write a short marketing tagline for: ${product}` },
      ],
    });

    const block = message.content[0];
    const text = block.type === "text" ? block.text : "";
    results.push(text.trim());
  }

  return results;
}
