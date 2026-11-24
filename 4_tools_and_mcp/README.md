# Week 4: Tools & MCP (Advanced)

**Theme:** connect Claude to systems beyond the filesystem, and design tools a model can use well.
**Week budget:** $6

| Day | Lab | You'll practise | Cap |
|---|---|---|---|
| 16 | [Connect an MCP server](1_lab1_connect_mcp.md) | `claude mcp add`, scopes, `.mcp.json`, `${VAR}` secrets, `/mcp` | $0.80 |
| 17 | [Build an MCP server for TaskForge](2_lab2_build_mcp_server.md) | Python `MCPServer`, tool design: names, descriptions, schemas, errors | $1.20 |
| 18 | [Resources, prompts and MCP security](3_lab3_resources_prompts_security.md) | resources, resource templates, prompts, tool poisoning, least privilege | $1.00 |
| 19 | [Structured output](4_lab4_structured_output.md) | `claude -p --output-format json --json-schema`, prompts for machines | $1.00 |
| 20 | [Mini-project: MCP-powered standup](5_lab5_mcp_standup_project.md) | a skill that orchestrates MCP tools with `allowed-tools` | $1.20 |

**Key idea of the week:** a tool is a **prompt**. Its name, description, parameters and error messages are
everything the model knows about it. Design them like an API for a smart colleague who can't read your code.

**End of week:** [Week 4 quiz](../assessments/week4_quiz.md).

**Fell behind?** `bash scripts/reset_to.sh week-4-start`
