// ACE-EXPECT: detect
// CATEGORY: should_detect/structured_output_missing
// LANGUAGE: java
// ISSUE: The model is asked to return JSON, but the free-form text response is parsed with Jackson ObjectMapper.readTree without any schema enforcement, JSON mode, or structured-output / tool-call constraint.
// EXPECTED-FINDING: LLM text output parsed as JSON (ObjectMapper) with no schema/JSON-mode guarantee; malformed or hallucinated fields will throw or silently produce nulls.
// EXPECTED-FIX: Use a structured-output mechanism (langchain4j AiServices typed return, OpenAI response_format json_schema, or a tool/function call) so the provider guarantees a schema-conformant payload.
// SEVERITY-HINT: warning
/** Extracts an invoice total from a model's free-form JSON-looking reply. */
package fp.testcases;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class JavaStructuredOutput1 {

    private final OpenAIClient client = OpenAIOkHttpClient.fromEnv();
    private final ObjectMapper mapper = new ObjectMapper();

    public double extractInvoiceTotal(String invoiceText) throws Exception {
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model(ChatModel.GPT_4O)
                .addSystemMessage("Return the invoice total as JSON: {\"total\": <number>, \"currency\": \"<iso>\"}")
                .addUserMessage(invoiceText)
                .build();

        ChatCompletion completion = client.chat().completions().create(params);
        String raw = completion.choices().get(0).message().content().orElse("");

        // No response_format json_schema, no validation: trust the model's text blindly.
        JsonNode node = mapper.readTree(raw);
        return node.get("total").asDouble();
    }

    public static void main(String[] args) throws Exception {
        JavaStructuredOutput1 app = new JavaStructuredOutput1();
        System.out.println(app.extractInvoiceTotal("Invoice #42, amount due 199.99 USD"));
    }
}
