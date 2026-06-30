// ACE-EXPECT: detect
// CATEGORY: should_detect/rag_no_grounding
// LANGUAGE: typescript
// ISSUE: Documents are retrieved but never injected into the prompt; the model answers from parametric memory with no grounding, citations, or abstain path.
// EXPECTED-FINDING: A RAG flow retrieves context but discards it (not passed to the model), and there is no citation requirement nor an abstain/"not in context" path.
// EXPECTED-FIX: Inject retrieved chunks into the prompt, instruct the model to answer only from context and cite sources, and abstain when the context is insufficient.
// SEVERITY-HINT: warning
/** Retrieves docs then ignores them and answers ungrounded. */
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

declare function retrieveDocs(query: string, k: number): Promise<{ id: string; text: string }[]>;

export async function answerQuestion(question: string): Promise<string> {
  // Retrieval happens but the result is never used in the prompt.
  const docs = await retrieveDocs(question, 5);
  void docs;

  const completion = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "Answer the user's question helpfully." },
      { role: "user", content: question },
    ],
  });

  // No grounding, no citations, no abstain when context is missing.
  return completion.choices[0].message.content ?? "";
}
