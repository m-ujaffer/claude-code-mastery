# Week 4 answers

| Q | Answer | Why |
|---|---|---|
| 1 | **C** | Project scope lives in `.mcp.json`, shared through version control. |
| 2 | **B** | `${VAR}` expansion keeps secrets out of git; each person uses their own credentials. |
| 3 | **A** | Repo content shouldn't be able to run code without consent. |
| 4 | **B** | Few, task-shaped, well-described tools: less context, better choices. |
| 5 | **B** | Actionable errors let the model self-correct. (In the Python SDK, raise `ToolError`.) |
| 6 | **C** | Tools are model-controlled; resources are application- or user-controlled. |
| 7 | **D** | Tool poisoning: malicious instructions hidden in tool metadata. |
| 8 | **A** | `structured_output`, which is missing when the run doesn't produce valid output. |
| 9 | **D** | Descriptions plus a few-shot example. Shouting doesn't help. |
| 10 | **A** | `allowed-tools` pre-approves only what's needed; anything else still asks. |
