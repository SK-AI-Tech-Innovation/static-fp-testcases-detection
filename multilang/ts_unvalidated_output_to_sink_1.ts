// ACE-EXPECT: detect
// CATEGORY: should_detect/unvalidated_output_to_sink
// LANGUAGE: typescript
// ISSUE: Model-generated JavaScript is executed via eval() (and new Function()) with no validation or sandboxing — arbitrary code execution.
// EXPECTED-FINDING: Raw LLM output flows into eval()/new Function() as executable code with no validation, allowlist, or sandbox — a code-injection / RCE sink.
// EXPECTED-FIX: Never eval model output; constrain to a safe DSL or whitelisted operations, or run in an isolated sandbox (e.g. isolated-vm/worker) with strict validation.
// SEVERITY-HINT: critical
/** Asks the model to write a JS expression and eval()s the result. */
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function computeFromPrompt(naturalLanguageMath: string): Promise<number> {
  const completion = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "Return a single JavaScript expression that computes the answer." },
      { role: "user", content: naturalLanguageMath },
    ],
  });

  const expr = completion.choices[0].message.content ?? "0";

  // Critical: model output executed directly as code.
  // eslint-disable-next-line no-eval
  const viaEval = eval(expr);
  const viaFunction = new Function(`return (${expr});`)();
  return Number(viaEval ?? viaFunction);
}
