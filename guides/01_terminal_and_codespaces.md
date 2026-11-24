# Guide 01: The terminal and your Codespace

You'll live in a terminal for this course. Here is the minimum you need.

## Where things are

| You see | It is |
|---|---|
| Editor (top) | VS Code running in your browser, connected to the Codespace |
| Terminal (bottom) | A bash shell **inside** the Codespace, a Linux container in the cloud |
| Explorer (left) | Your copy of the repo, at `/workspaces/<repo-name>` |

Open more terminals with the **+** in the terminal panel. A common layout is one terminal
for `claude` and one for running tests or the server yourself.

## Ten commands you'll use

```bash
pwd                      # where am I?
ls -la                   # what's here (including hidden files like .claude/)?
cd practice-app          # go into a folder;  cd ..  goes up;  cd  alone goes home
cat file.md              # print a file
less file.md             # page through a file (q to quit)
grep -rn "is_overdue" practice-app/src   # find text in files
uv run pytest            # run the tests
uv run labcheck w1d3     # check a lab (free)
git status               # what changed?
code notes/x.md          # open a file in the editor
```

## Keyboard shortcuts that save time

| Keys | Does |
|---|---|
| `Ctrl+C` | stop the running command |
| `Ctrl+R` | search your command history |
| `Tab` | autocomplete file names |
| `↑` | previous command |
| `Ctrl+L` | clear the screen |

## Inside Claude Code specifically

| Keys / input | Does |
|---|---|
| `Esc` | interrupt Claude mid-response |
| `Esc` `Esc` | open the rewind menu |
| `Shift+Tab` | cycle permission modes (default → accept edits → plan) |
| `@` | mention a file (autocompletes) |
| `!` at the start | run a shell command directly, without Claude |
| `/` | slash commands (`/help` lists them) |
| `Ctrl+D` twice, or `/exit` | quit |

## Codespace lifecycle

- **Stop** it when you're done (Codespaces menu → *Stop current codespace*). Files are kept.
- **Rebuild** (command palette → *Codespaces: Rebuild Container*) re-runs the devcontainer
  setup. Your files in `/workspaces` are kept.
- **Delete** only at the end of the course, after pushing your work.
