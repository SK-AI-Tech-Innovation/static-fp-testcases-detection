// ACE-EXPECT: detect
// CATEGORY: should_detect/rag_no_grounding
// LANGUAGE: typescript
// ISSUE: Retrieved chunks are concatenated into the prompt but the instructions never require grounding/citations and there is no abstain path when context lacks the answer.
// EXPECTED-FINDING: RAG prompt includes context yet does not constrain the model to answer only from it, request citations, or provide an "I don't know"/abstain path — invites hallucination.
// EXPECTED-FIX: Instruct the model to answer strictly from the provided context, cite the source chunk ids, and explicitly abstain when the answer is not supported by the context.
// SEVERITY-HINT: warning
/** Stuffs context but never enforces grounding, citations, or abstain. */
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

declare function vectorSearch(query: string): Promise<{ id: string; content: string }[]>;

export async function ragAnswer(question: string): Promise<string> {
  const chunks = await vectorSearch(question);
  const context = chunks.map((c) => c.content).join("\n\n");

  const message = await anthropic.messages.create({
    model: "claude-opus-4-20250514",
    max_tokens: 800,
    messages: [
      {
        role: "user",
        // Context is provided but no grounding constraint, no citation, no abstain rule.
        content: `Context:\n${context}\n\nQuestion: ${question}\n\nAnswer the question.`,
      },
    ],
  });

  const block = message.content[0];
  return block.type === "text" ? block.text : "";
}
