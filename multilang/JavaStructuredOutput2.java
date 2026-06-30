// ACE-EXPECT: detect
// CATEGORY: should_detect/structured_output_missing
// LANGUAGE: java
// ISSUE: A classification label is scraped out of the model's prose using a regex, with no schema, no enum constraint, and no structured-output mode; any phrasing drift breaks the match.
// EXPECTED-FINDING: Model output coerced into a category via brittle regex pattern matching instead of an enforced schema/enum.
// EXPECTED-FIX: Constrain the response with a tool call or JSON-schema enum (langchain4j enum return type, or Anthropic tool with an enum field) so the label is guaranteed valid.
// SEVERITY-HINT: warning
/** Classifies support tickets by regex-scraping the model's free text. */
package fp.testcases;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class JavaStructuredOutput2 {

    private final AnthropicClient client = AnthropicOkHttpClient.fromEnv();
    private static final Pattern LABEL = Pattern.compile("(?i)category\\s*[:=]\\s*(\\w+)");

    public String classifyTicket(String ticketBody) {
        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_20250514)
                .maxTokens(256)
                .addUserMessage("Classify this ticket as BILLING, TECHNICAL, or ACCOUNT.\n" + ticketBody)
                .build();

        Message message = client.messages().create(params);
        String text = message.content().get(0).text().orElseThrow().text();

        // No JSON schema, no enum enforcement - just hope the prose matches the regex.
        Matcher m = LABEL.matcher(text);
        if (m.find()) {
            return m.group(1).toUpperCase();
        }
        return "UNKNOWN";
    }

    public static void main(String[] args) {
        JavaStructuredOutput2 app = new JavaStructuredOutput2();
        System.out.println(app.classifyTicket("My card was charged twice this month."));
    }
}
