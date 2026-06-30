// ACE-EXPECT: detect
// CATEGORY: should_detect/prompt_few_shot
// LANGUAGE: java
// ISSUE: A nuanced sentiment+intent classification prompt with many fine-grained labels is issued zero-shot, with no examples to disambiguate similar categories.
// EXPECTED-FINDING: Complex classification prompt over a fine-grained label set provided without any few-shot examples.
// EXPECTED-FIX: Include labeled example messages (one per ambiguous class) in the prompt to calibrate boundary cases.
// SEVERITY-HINT: suggestion
/** Zero-shot multi-label intent classification with no examples. */
package fp.testcases;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class JavaPromptFewShot2 {

    private final OpenAIClient client = OpenAIOkHttpClient.fromEnv();

    public String classify(String userMessage) {
        // Fine-grained labels that overlap, yet no examples are provided to disambiguate.
        String instruction = "Classify the customer message into exactly one of: "
                + "COMPLAINT, REFUND_REQUEST, CANCELLATION, PRAISE, FEATURE_REQUEST, "
                + "BILLING_QUESTION, SHIPPING_ISSUE, ACCOUNT_ACCESS. "
                + "Reply with only the label.";

        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model(ChatModel.GPT_4O)
                .addSystemMessage(instruction)
                .addUserMessage(userMessage)
                .build();

        ChatCompletion completion = client.chat().completions().create(params);
        return completion.choices().get(0).message().content().orElse("");
    }

    public static void main(String[] args) {
        JavaPromptFewShot2 app = new JavaPromptFewShot2();
        System.out.println(app.classify("I still haven't received my order and want my money back."));
    }
}
