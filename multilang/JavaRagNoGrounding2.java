// ACE-EXPECT: detect
// CATEGORY: should_detect/rag_no_grounding
// LANGUAGE: java
// ISSUE: Retrieved chunks are concatenated into the prompt, but there is no instruction to answer only from context, no citation requirement, and no abstain path - so the model freely hallucinates beyond the sources.
// EXPECTED-FINDING: RAG prompt includes context yet lacks grounding constraints (answer-from-context-only, cite sources, abstain when unsupported).
// EXPECTED-FIX: Add explicit grounding instructions: restrict answers to the provided context, require source citations, and instruct the model to say it does not know when context is insufficient.
// SEVERITY-HINT: warning
/** Stuffs context but gives no grounding/citation/abstain instructions. */
package fp.testcases;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

import java.util.List;

public class JavaRagNoGrounding2 {

    private final AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    public String ask(String question, List<String> retrievedChunks) {
        StringBuilder sb = new StringBuilder();
        for (String chunk : retrievedChunks) {
            sb.append(chunk).append("\n\n");
        }
        // Context is present, but no "answer only from context", no citations, no abstain rule.
        String prompt = "Context:\n" + sb + "\nQuestion: " + question + "\nAnswer:";

        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_20250514)
                .maxTokens(512)
                .addUserMessage(prompt)
                .build();

        Message message = client.messages().create(params);
        return message.content().get(0).text().orElseThrow().text();
    }

    public static void main(String[] args) {
        JavaRagNoGrounding2 app = new JavaRagNoGrounding2();
        System.out.println(app.ask("What is the refund window?",
                List.of("Our return policy allows refunds within 30 days of purchase.")));
    }
}
