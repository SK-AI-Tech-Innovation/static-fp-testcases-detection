// ACE-EXPECT: detect
// CATEGORY: should_detect/unvalidated_output_to_sink
// LANGUAGE: typescript
// ISSUE: A model-produced shell command is passed straight to child_process.exec(), allowing command injection via the LLM output.
// EXPECTED-FINDING: LLM-generated text is concatenated/passed into child_process.exec() as a shell command with no validation or argument escaping — a command-injection sink.
// EXPECTED-FIX: Never run model output as a shell string; map intents to a fixed allowlist and use execFile()/spawn() with an argument array and validated parameters.
// SEVERITY-HINT: critical
/** Turns a request into a shell command and exec()s it directly. */
import Anthropic from "@anthropic-ai/sdk";
import { exec } from "node:child_process";
import { promisify } from "node:util";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const execAsync = promisify(exec);

export async function runOpsTask(request: string): Promise<string> {
  const message = await anthropic.messages.create({
    model: "claude-opus-4-20250514",
    max_tokens: 256,
    messages: [
      { role: "user", content: `Output only the shell command to: ${request}` },
    ],
  });

  const block = message.content[0];
  const command = block.type === "text" ? block.text.trim() : "";

  // Critical: untrusted model output run as a shell command.
  const { stdout } = await execAsync(command);
  return stdout;
}
