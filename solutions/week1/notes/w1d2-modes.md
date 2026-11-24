# W1D2: Modes and controls

- default: asks before every edit and most commands; the right choice on unfamiliar or important code.
- acceptEdits: auto-approves file edits for the session but still asks for commands; fine when git diff is my review.
- plan: read-only research and a proposed plan; use it before any multi-file change.
- @ mention: pulls a specific file into context so Claude doesn't spend tokens searching.
- ! bash: runs my own command and puts its output into the conversation.
- esc: interrupts Claude immediately so I can redirect it.
- rewind: restores code and/or conversation to a checkpoint; it does not undo side effects of commands Claude ran.
