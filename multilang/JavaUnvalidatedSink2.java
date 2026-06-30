// ACE-EXPECT: detect
// CATEGORY: should_detect/unvalidated_output_to_sink
// LANGUAGE: java
// ISSUE: A model-generated WHERE clause is concatenated directly into a JDBC SQL string and executed via Statement, allowing SQL injection from a manipulated model response.
// EXPECTED-FINDING: Unvalidated LLM output concatenated into a SQL statement (SQL-injection sink) executed with java.sql.Statement.
// EXPECTED-FIX: Do not let the model produce raw SQL; map intents to parameterized queries (PreparedStatement) with validated, bound parameters.
// SEVERITY-HINT: critical
/** Builds and runs SQL from raw model text - SQL injection sink. */
package fp.testcases;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class JavaUnvalidatedSink2 {

    private final AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    public int countMatching(String question) throws Exception {
        MessageCreateParams params = MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_20250514)
                .maxTokens(128)
                .addUserMessage("Output only a SQL WHERE clause (no keyword) for: " + question)
                .build();

        Message message = client.messages().create(params);
        String whereClause = message.content().get(0).text().orElseThrow().text();

        // DANGER: model text concatenated straight into SQL and executed.
        String sql = "SELECT COUNT(*) FROM orders WHERE " + whereClause;
        try (Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost/shop", "app", "app");
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }

    public static void main(String[] args) throws Exception {
        JavaUnvalidatedSink2 app = new JavaUnvalidatedSink2();
        System.out.println(app.countMatching("orders placed last week over 100 dollars"));
    }
}
