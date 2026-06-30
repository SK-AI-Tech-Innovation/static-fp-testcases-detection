// ACE-EXPECT: detect
// CATEGORY: should_detect/no_retry_fallback
// LANGUAGE: java
// ISSUE: A single synchronous LLM call is made with no try/catch, no retry on transient errors (429/5xx/timeout), and no fallback path; any provider hiccup propagates as an unhandled exception.
// EXPECTED-FINDING: Unguarded one-shot LLM call with no retry/backoff or fallback handling.
// EXPECTED-FIX: Wrap the call with bounded retries + exponential backoff (e.g. Resilience4j Retry) and a fallback response or graceful degradation.
// SEVERITY-HINT: warning
/** Summarizes a document with a single unguarded model call. */
package fp.testcases;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class JavaNoRetryFallback1 {

    private final OpenAIClient client = OpenAIOkHttpClient.fromEnv();

    public String summarize(String document) {
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model(ChatModel.GPT_4O)
                .addSystemMessage("Summarize the document in three sentences.")
                .addUserMessage(document)
                .build();

        // Single call, no try/catch, no retry, no fallback. A 429 or timeout just blows up.
        ChatCompletion completion = client.chat().completions().create(params);
        return completion.choices().get(0).message().content().orElse("");
    }

    public static void main(String[] args) {
        JavaNoRetryFallback1 app = new JavaNoRetryFallback1();
        System.out.println(app.summarize("A long quarterly report about revenue and growth."));
    }
}
