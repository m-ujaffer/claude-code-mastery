# Week 1 answers

| Q | Answer | Why |
|---|---|---|
| 1 | **C** | Plan mode lets Claude read and propose without editing. |
| 2 | **D** | Rewind restores code and/or conversation to a checkpoint. `/clear` loses the conversation but keeps the bad edits. |
| 3 | **C** | Checkpoints track Claude's file edits. Side effects of commands (DB writes, pushes, deployments) can't be rewound. |
| 4 | **B** | An `@` mention pulls the exact file in, with no exploratory searching. |
| 5 | **A** | A test that passes before the fix doesn't test the bug. |
| 6 | **A** | Context and verification remove guessing and exploring. Caps and length don't help. |
| 7 | **A** | `/compact <focus>` keeps continuity while shrinking history. |
| 8 | **B** | Unrelated old context costs tokens every turn and can mislead. |
| 9 | **D** | Every turn re-sends the conversation; big file reads and tool outputs dominate. |
| 10 | **B** | Match model to task: Sonnet for everyday work, Opus on purpose. |
