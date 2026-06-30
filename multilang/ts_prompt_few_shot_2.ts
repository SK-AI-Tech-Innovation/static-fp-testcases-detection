// ACE-EXPECT: detect
// CATEGORY: should_detect/prompt_few_shot
// LANGUAGE: typescript
// ISSUE: A multi-label sentiment+intent classification prompt with a nuanced rubric provides no few-shot examples to demonstrate boundary cases.
// EXPECTED-FINDING: A nuanced multi-label classification prompt relies on rubric text alone with zero few-shot exemplars, leading to inconsistent labeling on ambiguous inputs.
// EXPECTED-FIX: Include several labeled examples covering ambiguous/mixed cases so the model learns the decision boundaries and exact label vocabulary.
// SEVERITY-HINT: suggestion
/** Classifies customer messages by sentiment and intent with no exemplars. */
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const RUBRIC = `Classify the customer message.
- sentiment: one of [very_negative, negative, neutral, positive, very_positive]
- intent: one of [complaint, question, cancellation, upsell_opportunity, praise]
- urgency: integer 1-5
Mixed sentiment should lean toward the dominant emotion of the closing sentence.
Sarcasm should be scored by the literal grievance, not the surface tone.`;

export async function classifyMessage(message: string) {
  // Nuanced rubric, but no few-shot examples to anchor the tricky rules above.
  const result = await anthropic.messages.create({
    model: "claude-opus-4-20250514",
    max_tokens: 300,
    system: RUBRIC,
    messages: [{ role: "user", content: message }],
  });

  const block = result.content[0];
  return block.type === "text" ? block.text : "";
}
