// ACE-EXPECT: detect
// CATEGORY: should_detect/no_retry_fallback
// LANGUAGE: java
// ISSUE: A Bedrock Converse call runs once inside a request handler with no retry, no circuit breaker, and no fallback; transient ThrottlingException / ModelTimeoutException surfaces directly to the caller.
// EXPECTED-FINDING: One-shot Bedrock invocation lacking retry/backoff and fallback for throttling or timeout errors.
// EXPECTED-FIX: Configure AWS SDK retry policy or wrap with Resilience4j retry + a cached/degraded fallback answer.
// SEVERITY-HINT: warning
/** Answers a user question via a single Bedrock Converse call. */
package fp.testcases;

import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.ContentBlock;
import software.amazon.awssdk.services.bedrockruntime.model.ConversationRole;
import software.amazon.awssdk.services.bedrockruntime.model.ConverseRequest;
import software.amazon.awssdk.services.bedrockruntime.model.ConverseResponse;
import software.amazon.awssdk.services.bedrockruntime.model.Message;

public class JavaNoRetryFallback2 {

    private final BedrockRuntimeClient client = BedrockRuntimeClient.create();
    private static final String MODEL_ID = "anthropic.claude-3-5-sonnet-20241022-v2:0";

    public String answer(String question) {
        Message userMessage = Message.builder()
                .role(ConversationRole.USER)
                .content(ContentBlock.fromText(question))
                .build();

        ConverseRequest request = ConverseRequest.builder()
                .modelId(MODEL_ID)
                .messages(userMessage)
                .build();

        // No retry config, no try/catch, no fallback - throttling kills the request path.
        ConverseResponse response = client.converse(request);
        return response.output().message().content().get(0).text();
    }

    public static void main(String[] args) {
        JavaNoRetryFallback2 app = new JavaNoRetryFallback2();
        System.out.println(app.answer("What is the capital of France?"));
    }
}
