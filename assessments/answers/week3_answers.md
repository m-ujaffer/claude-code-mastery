# Week 3 answers

| Q | Answer | Why |
|---|---|---|
| 1 | **C** | Managed settings have the highest precedence and can't be overridden. |
| 2 | **C** | Array settings like permission rules merge across scopes. |
| 3 | **B** | `Read(...)` rules govern the Read tool; shell access needs a Bash rule or a deterministic hook. An instruction is only advisory. |
| 4 | **A** | Exit code 2 blocks, and stderr is shown to Claude. Other non-zero codes are non-blocking errors. |
| 5 | **A** | "Must happen every time" means a hook. Preferences and architecture knowledge belong in memory. |
| 6 | **B** | `disable-model-invocation: true` makes the skill manual only. |
| 7 | **A** | Progressive disclosure: descriptions first, full content on use. |
| 8 | **B** | Only the manifest lives in `.claude-plugin/`. |
| 9 | **D** | `${CLAUDE_PLUGIN_ROOT}` resolves to the installed plugin's directory. |
| 10 | **D** | Plugins plus marketplaces give consistent, versioned distribution. |
