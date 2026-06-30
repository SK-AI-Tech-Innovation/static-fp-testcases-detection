// ACE-EXPECT: detect
// CATEGORY: should_detect/unvalidated_output_to_sink
// LANGUAGE: java
// ISSUE: The model is asked to emit a shell command and the raw output string is passed straight to Runtime.getRuntime().exec, enabling arbitrary command execution from a prompt-injected response.
// EXPECTED-FINDING: Unvalidated LLM output flows into Runtime.exec (command-injection / RCE sink).
// EXPECTED-FIX: Never execute model text directly; restrict to an allow-listed action set, parse into validated parameters, and avoid a shell sink entirely.
// SEVERITY-HINT: critical
/** Runs whatever shell command the model returns - direct RCE sink. */
package fp.testcases;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

public class JavaUnvalidatedSink1 {

    private final OpenAIClient client = OpenAIOkHttpClient.fromEnv();

    public String runFromInstruction(String naturalLanguage) throws Exception {
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model(ChatModel.GPT_4O)
                .addSystemMessage("Translate the user's request into a single bash command. Output only the command.")
                .addUserMessage(naturalLanguage)
                .build();

        ChatCompletion completion = client.chat().completions().create(params);
        String command = completion.choices().get(0).message().content().orElse("");

        // DANGER: model output executed directly as a shell command.
        Process process = Runtime.getRuntime().exec(new String[]{"bash", "-c", command});
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            return reader.lines().collect(Collectors.joining("\n"));
        }
    }

    public static void main(String[] args) throws Exception {
        JavaUnvalidatedSink1 app = new JavaUnvalidatedSink1();
        System.out.println(app.runFromInstruction("list the files in my home directory"));
    }
}
