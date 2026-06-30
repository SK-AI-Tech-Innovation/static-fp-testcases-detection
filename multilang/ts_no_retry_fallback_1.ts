// ACE-EXPECT: detect
// CATEGORY: should_detect/no_retry_fallback
// LANGUAGE: typescript
// ISSUE: A batch of articles is summarized in a loop where each OpenAI call has no try/catch, no retry on transient errors (429/5xx), and no per-item isolation or fallback.
// EXPECTED-FINDING: A single transient rate-limit/5xx on any item throws out of the loop and aborts the entire batch; there is no retry/backoff, no fallback, and no per-item error isolation.
// EXPECTED-FIX: Wrap each call in try/catch with bounded exponential-backoff retries on retryable errors, isolate failures per item, and provide a graceful fallback/degraded result.
// SEVERITY-HINT: warning
/** Summarizes a batch of articles; one transient failure aborts the whole job. */
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function summarizeOne(article: string): Promise<string> {
  // One shot per item: no retry, no try/catch, no fallback.
  const completion = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "Summarize the article in three sentences." },
      { role: "user", content: article },
    ],
    temperature: 0.3,
  });
  return completion.choices[0].message.content ?? "";
}

export async function summarizeBatch(articles: string[]): Promise<string[]> {
  const summaries: string[] = [];
  // Sequential loop with no per-item error isolation: a 429 on item 7 of 500
  // throws here and discards every summary computed so far.
  for (const article of articles) {
    summaries.push(await summarizeOne(article));
  }
  return summaries;
}
