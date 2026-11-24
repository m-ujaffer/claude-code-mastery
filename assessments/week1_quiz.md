# Week 1 quiz: Foundations

10 questions · about 10 minutes · offline · answers in [answers/week1_answers.md](answers/week1_answers.md)

**1.** You want Claude to investigate a bug and propose a fix, but you're not ready for any files to change. Which mode fits best?
- A) Default mode
- B) Accept-edits mode
- C) Plan mode
- D) Bypass-permissions mode

**2.** Claude has edited three files in the wrong direction. What's the fastest way to restore both the code and the conversation to before the mistake?
- A) `/clear`
- B) `/compact`
- C) `git stash`
- D) `/rewind` (or Esc Esc) to a checkpoint

**3.** Which statement about `/rewind` is true?
- A) It also undoes the effects of shell commands Claude ran, such as database writes
- B) It only works in plan mode
- C) It restores files Claude edited, but not external side effects of commands
- D) It deletes the session

**4.** You need Claude to look at one specific file. Which is cheapest and most precise?
- A) "Look around the repo and find the overdue logic"
- B) `@practice-app/src/taskforge/services.py` in your prompt
- C) Paste the whole repo into the prompt
- D) Switch to Opus so it searches faster

**5.** In a test-first bug fix, why should you confirm the new test fails *before* the fix?
- A) It proves the test actually captures the bug, rather than passing trivially
- B) It makes the session cheaper
- C) Claude Code requires it
- D) So coverage goes up

**6.** Which prompt element did Day 4 show most reduces wasted turns?
- A) Concrete context and verification steps (files, acceptance criteria, which tests to run)
- B) Politeness
- C) All caps for important rules
- D) A longer prompt

**7.** Your session is at 60% context and you're mid-task. You want to continue, but cheaper. Best move?
- A) `/compact` with a focus on what to keep
- B) `/clear`
- C) Switch to Opus
- D) Start a second session and copy-paste the conversation

**8.** You're switching from a finished task to an unrelated one. Best move?
- A) `/compact`
- B) `/clear`
- C) Keep going; the context might be useful
- D) `/model haiku`

**9.** Which is the most expensive part of a typical long session, even with caching?
- A) Your typed prompts
- B) Output tokens of short answers
- C) The status line
- D) Repeated context: everything re-sent each turn (conversation, tool results, file contents)

**10.** Why does the course default to Sonnet rather than Opus?
- A) Opus can't edit files
- B) Sonnet handles everyday coding well at a lower price; Opus is reserved for problems that need it
- C) Sonnet has a larger context window
- D) Opus isn't available with API keys
