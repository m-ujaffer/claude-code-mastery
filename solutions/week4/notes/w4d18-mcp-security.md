# W4D18: MCP security review

- tool poisoning: a server's tool description can carry hidden instructions; in my drill Claude tried to read .env and the deny rule plus the hook blocked it. Descriptions are code, so review them.
- least privilege: read-only tools are auto-allowed and annotated readOnlyHint; write tools still ask; tokens get the narrowest scopes.
- secrets: never in .mcp.json; use ${VAR} expansion and per-engineer secrets.
- what I would review before installing a server: who maintains it, pinned version, tool descriptions, which network calls and credentials it needs, and whether its outputs include untrusted content (a prompt-injection path).
