# W5D21: Subagents and context

- task given: find every place in practice-app where dates or times are created or compared
- main context before: about 46k tokens (I did the search myself and the file reads landed in the main context)
- main context after: about 22k tokens (the Explore subagent returned a 15-line list)
- what the subagent returned: file:line list covering clock.py, services.py, repository.py and legacy/report_builder.py
- when not to use a subagent: tightly coupled edits that need the full conversation (e.g. a refactor already being
  discussed), tiny tasks where the cold start costs more than it saves, and anything where I need to see the raw evidence
