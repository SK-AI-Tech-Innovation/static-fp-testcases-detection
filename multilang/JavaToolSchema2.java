// ACE-EXPECT: detect
// CATEGORY: should_detect/tool_schema_vague
// LANGUAGE: java
// ISSUE: A langchain4j @Tool method exposes a generic "args" string with no @P descriptions and no @Tool description, so the LLM cannot infer parameter meaning or format.
// EXPECTED-FINDING: @Tool annotation with empty description and an untyped/undescribed generic "args" parameter.
// EXPECTED-FIX: Give @Tool a descriptive value and annotate each parameter with @P(...) describing its meaning and format; split generic args into typed fields.
// SEVERITY-HINT: warning
/** A langchain4j tool whose only parameter is an undocumented generic string. */
package fp.testcases;

import dev.langchain4j.agent.tool.Tool;

public class JavaToolSchema2 {

    // No @Tool description, generic "args", no @P annotations - the model is flying blind.
    @Tool
    public String runQuery(String args) {
        String[] parts = args.split(",");
        if (parts.length < 2) {
            return "error: bad args";
        }
        String table = parts[0].trim();
        String filter = parts[1].trim();
        return "rows from " + table + " where " + filter;
    }

    @Tool
    public String doAction(String args) {
        return "executed: " + args;
    }

    public static void main(String[] args) {
        JavaToolSchema2 app = new JavaToolSchema2();
        System.out.println(app.runQuery("users, active=true"));
    }
}
