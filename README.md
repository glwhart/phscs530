# Physics 530: Computational Physics

The files you need for Physics 530 at BYU. Do all your course work inside this folder. Among other
things it holds the course instructions for AI tools, so that any AI agent you start here follows the
course AI policy. The policy itself is in the syllabus.

*Draft for Winter 2027. The final version will be posted before the first class.*

## Getting it

With git (recommended, because updates then take one command):

```
git clone https://github.com/glwhart/phscs530.git phscs530
cd phscs530
```

Without git: on this page, click **Code**, then **Download ZIP**, and unzip it where you keep your
course work.

## Keeping it up to date

The instructor will add files and may update the AI instructions during the semester. With git, run `git pull` inside the
folder. Without git, download the ZIP again and copy over `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and
`chatbot-prompt.md`.

## Using it with AI tools

**Coding agents** (Claude Code, Codex, Gemini CLI, Cursor and others): start the agent in this folder
or a folder inside it. The agent reads the instructions automatically: Codex and most others read
`AGENTS.md`, Claude Code reads `CLAUDE.md`, and Gemini CLI reads `GEMINI.md`. All three say the same
thing. To check that it works, ask your agent "What level is NE 3 under the course AI policy?" It should
answer "level 1, tutor".

**Chat tools** (ChatGPT, Gemini, Claude or Copilot in a browser): paste the text from
`chatbot-prompt.md` at the start of each conversation, or use the course's shared tutor link on max.

## What is here

| Item | What it is for |
|---|---|
| `AGENTS.md` | The instructions AI tools follow in this course |
| `CLAUDE.md`, `GEMINI.md` | Load `AGENTS.md` for Claude Code and Gemini CLI |
| `chatbot-prompt.md` | The same instructions, short, for chat tools |
| `AI-LOG.md` | A running log of AI use, for the AI-use appendix on each assignment |
| `numerical-exercises/PLAN-template.md` | Your plan, equations and prediction, written before any AI help |
| `simdd/SPEC-template.md` | The specification and predictions you write before an agent builds anything |
| `checks/` | Example checks, in Julia and Python, for handouts that list "Checks your code must pass" |
| `readings/`, `warmups/`, `numerical-exercises/`, `simdd/`, `final-project/` | Your work, one folder per assignment |

These files help you use AI within the course policy. They do not change the policy, and you are
responsible for following it whether or not you use them.
