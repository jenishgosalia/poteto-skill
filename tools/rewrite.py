import pathlib, re, sys
root = pathlib.Path(sys.argv[1])

# ---------- poteto-mode Subagents section ----------
p = root/'skills/poteto-mode/SKILL.md'
t = p.read_text()
start = t.index('**Use `subagent_type: "poteto-agent"`')
end = t.index('You own every subagent')
new_sub = '''**Use `subagent_type: "poteto-agent"` for any subagent you spawn inside a playbook step** (code-writing delegates, ad-hoc helpers). If the Agent tool does not resolve the bare name, use the plugin-scoped form `pstack:poteto-agent`. The chat that receives `/poteto-mode` runs the playbook. Never spawn a `poteto-agent` to run the playbook itself. Routed workflow skills (`how`, `why`, `interrogate`, `reflect`, `swarm`) set their own `subagent_type` for diverse-model review. Respect what the skill prescribes, don't override to `poteto-agent`.

**Model slugs.** pstack names a model as `<alias>-<effort>`, where the alias is a Claude Code model alias (`haiku`, `sonnet`, `opus`, `fable`) and the effort is one of `low`, `medium`, `high`, `xhigh`, `max`. The ladder of strength is `haiku` < `sonnet` < `opus` < `fable`. When you spawn, split the slug into the Agent tool's two parameters: `model: "opus"` and `effort: "xhigh"` for `opus-xhigh`. Never pass the joined slug as `model`. If the effort is not supported by that model, Claude Code falls back to the highest level it supports.

**Defaults for every `Agent` call.** `run_in_background: true`, `subagent_type: general-purpose` or `poteto-agent` when the delegate needs MCP or write access (`Explore` is read-only and strips MCP), file pointers not inlined context, explicit model per role (configurable via `/setup-pstack`. Defaults `sonnet-xhigh` for code, `opus-xhigh` for prose and judgment, `fable-max` for the hardest tasks). Code delegates tier by difficulty. The hardest changes (cross-cutting design, gnarly concurrency, subtle algorithms) go to your strongest model (`fable-max`, the `hardest tasks` line), whether the task needs judgment on vague intent or is a precisely specified sequence of steps to execute to the letter. Trivial mechanical edits (renames, moving files, applying a codemod's output) go one step down the ladder from the role's model, so `sonnet` roles run them on `haiku`. Per-role lines in the `/setup-pstack` rule override these defaults and the model choices in the routed skills (`how`, `why`, `arena`, `swarm`, `architect`, `interrogate`, `reflect`). A role with no line keeps its default, and a role line of `inherit-parent` or `auto` runs that role on the parent chat model (omit Agent `model` and `effort`). Each code playbook's configured model comes from its line (`feature, refactoring`, `bug-fix`, `perf-issue`, or `hillclimb`), and the hardest changes read `hardest tasks`. Prose and judgment read `judgment and prose`.

**Match the model to the job.** Before each spawn, start from the role's line or default and pick the effort the job needs. The `/setup-pstack` budget sets each role's starting level, xhigh by default. Raise it one step, up to max, for the hardest or subtlest work. Lower it one step for judgment and two or more steps for routine work. Verification is the exception and stays on the `swarm workers` model and effort (`sonnet-xhigh` by default). Change only the effort, and keep the alias the role names, so a diverse panel stays diverse. A role on `auto` or `inherit-parent` stays on the parent model. If the Agent tool rejects the adjusted effort, do not try another. Use the role's line or default and say so.

'''
t = t[:start] + new_sub + t[end:]
p.write_text(t)

# ---------- setup-pstack ----------
(root/'skills/setup-pstack/SKILL.md').write_text('''---
name: setup-pstack
description: Configure which Claude models pstack uses per role and at what reasoning effort. Detects the models available to the Agent tool and writes an always-loaded user rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.claude/rules/pstack-models.md`, a user-level rule with no `paths` frontmatter, so Claude Code loads it in every session and every project. It sets pstack's model per role.

## Slug grammar

A pstack model slug is `<alias>-<effort>`. The alias is a Claude Code model alias: `haiku`, `sonnet`, `opus`, or `fable`. The effort is `low`, `medium`, `high`, `xhigh`, or `max`. Examples: `sonnet-xhigh`, `opus-xhigh`, `fable-max`, `haiku-medium`. Skills split the slug into the Agent tool's `model` and `effort` parameters at spawn time. `inherit-parent` and `auto` are aliases that mean "run this role on the parent chat model" (omit `model` and `effort`).

## Steps

### 1. Detect available models

Enumerate the aliases the Agent tool's `model` parameter accepts in this session (its schema lists them; `fable` requires a plan that includes Fable). That is the dependable source. If you cannot detect any, ask the user which of `haiku`, `sonnet`, `opus`, `fable` they can use. Never write an alias you have not confirmed is available. `inherit-parent` and `auto` are always valid.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in step 5 below. If `~/.claude/rules/pstack-models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. A line whose role is not in step 5 is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer `AskUserQuestion` over free text. Offer these four options with these exact labels, and name the current budget when the rule records one. With no rule, say that `large` matches the skill defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by alias, list, or `inherit-parent`/`auto`. `unlimited`, `large`, `medium`, and `small` set the effort token of every real slug, panel entries included, to `max`, `xhigh`, `high`, or `medium`. The `hardest tasks` line always sits one step above the budget, capped at `max`. `inherit-parent` and `auto` do not change. So `unlimited` turns `opus-xhigh` into `opus-max` and `sonnet-xhigh` into `sonnet-max`. `large` keeps the defaults. `small` turns them into `opus-medium` and `sonnet-medium`, and `hardest tasks` into `fable-high`.

**(c) Show the roles and confirm.** Show every role with its model, marking any alias not in the detected set as needing a choice (a user without `fable` gets `opus` for `hardest tasks` and the `fable` panel seats become `opus`). Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected aliases plus `inherit-parent` and `auto` as the options. Prefer `AskUserQuestion` over free text. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose alias differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every alias written must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen alias is not available, stop and ask again.

### 5. Write the rule

Write `~/.claude/rules/pstack-models.md` (create the directory if needed) with a `# budget` line with the chosen label and its target effort, and one line per role, using the same labels poteto-mode uses. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# Slug is <alias>-<effort>: alias in haiku, sonnet, opus, fable. Effort in low, medium, high, xhigh, max.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Agent `model` and `effort`). Alias entries in a panel list still count toward its fan-out.
# budget: large (xhigh)
feature, refactoring: sonnet-xhigh
bug-fix: sonnet-xhigh
perf-issue: sonnet-xhigh
hillclimb: sonnet-xhigh
judgment and prose: opus-xhigh
hardest tasks: fable-max
how explorer: sonnet-xhigh
how explainer: opus-xhigh
why investigators: sonnet-xhigh
why synthesizer: opus-xhigh
reflect tooling: sonnet-xhigh
reflect judgment, divergent, synthesizer: opus-xhigh
arena runners: fable-xhigh, opus-xhigh, sonnet-xhigh
arena cross-judge pool: fable-xhigh, opus-xhigh, sonnet-xhigh
swarm workers: sonnet-xhigh
architect runners: fable-xhigh, opus-xhigh, sonnet-xhigh
interrogate reviewers: fable-xhigh, opus-xhigh, sonnet-xhigh, haiku-xhigh
```

### 6. Confirm

Tell the user the rule was written and that it applies to new sessions. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill` (resolves wherever pstack is installed: workspace, user, or plugin). On no, move on without pushing.
''')

# ---------- poteto-agent ----------
(root/'agents/poteto-agent.md').write_text('''---
name: poteto-agent
description: Delegate subagent for code-writing and helper tasks spawned during a `/poteto-mode` run. Use for delegates, not as the runner for `/poteto-mode` itself. Spawn a fresh `poteto-agent` for each new task, and resume one only in the strict cases that poteto-mode's Subagents section names. Reads the `poteto-mode` skill's `SKILL.md` in full before any work, including its inline Principles index. Substituting `general-purpose` skips that read and drifts.
model: inherit
background: true
color: yellow
---

# Poteto subagent

You are operating as poteto-mode's full agent style. The chat that receives `/poteto-mode` owns the playbook, the task list, and every Agent spawn. You are one of its delegates. Read the `poteto-mode` skill's `SKILL.md` in full before doing any work, including its inline Principles index. Use the absolute path your parent gave you. With no path, read `${CLAUDE_PLUGIN_ROOT}/skills/poteto-mode/SKILL.md`. If that path does not resolve, search `~/.claude/plugins/` for a file whose path ends in `skills/poteto-mode/SKILL.md` and use the copy under the highest version directory. Your skill catalog hides this skill, so a missing catalog entry does not mean pstack is absent. If no such file exists, stop and tell your parent. Navigate to a leaf `principle-*` skill whenever you apply that principle.
''')

# ---------- comment-sicko: strip Cursor-only frontmatter if any ----------
# ---------- poteto-help ----------
p = root/'skills/poteto-help/SKILL.md'; t = p.read_text()
t = t.replace("pstack is built for Cursor. Its skills use the Agent Skills format, so other tools can read them. But most workflow skills, including `/poteto-mode`, `/how`, `/why`, and `/teach`, spawn Cursor subagents with per-role models, and Custom Modes and `/loop` are Cursor features, so those parts may not work there.",
"This build of pstack is ported to Claude Code from the Cursor original. Its skills use the Agent Skills format, so other tools can read them. The workflow skills, including `/poteto-mode`, `/how`, `/why`, and `/teach`, spawn Claude Code subagents through the Agent tool with per-role models and effort levels. In the claude.ai chat app, the skills load but there is no subagent fan-out, so `/poteto-mode` runs its playbook inline.")
t = re.sub(r"Whether `/poteto-mode` stays on depends on how the user starts it:\n\n- Enter on.*?\n- Option\+Enter.*?\n- Cursor's docs.*?\n\nLink \[Cursor's skills docs\]\(https://cursor\.com/docs/skills\) when this comes up\. ",
"`/poteto-mode` has `disable-model-invocation: true`, so it only loads when the user invokes it. Start each new task with `/poteto-mode`, or `/pstack:poteto-mode` when a name collides. To keep it on for every turn, the user can add one line to `~/.claude/CLAUDE.md`: `Start every nontrivial task by loading the poteto-mode skill.` ", t, flags=re.S)
t = t.replace("Without `/poteto-mode`, a phrase such as \"babysit this pr\" can start Cursor's own skill for the same job instead.", "Without `/poteto-mode`, a phrase such as \"babysit this pr\" gets no playbook.")
t = t.replace("pstack has no planning skill. Cursor's Plan Mode works alongside it.", "pstack has no planning skill. Claude Code's plan mode (`EnterPlanMode`) works alongside it.")
p.write_text(t)

# ---------- reflect small fixes ----------
p = root/'skills/reflect/SKILL.md'; t = p.read_text()
t = t.replace(", and readonly strips MCPs.", ", so do not use the read-only `Explore` agent.")
t = t.replace("Reviewers return findings in the `Task` response body.", "Reviewers return findings in the Agent response body.")
t = t.replace("It spot-verifies citations through MCP, and readonly strips MCPs.", "It spot-verifies citations through MCP, so it is not an `Explore` agent.")
p.write_text(t)

# ---------- README: add a Claude Code section at top ----------
p = root/'README.md'; t = p.read_text()
t = t.replace("## install\n\n```bash\n/add-plugin pstack\n```",
'''## this build: ported to Claude Code

this copy of pstack is adapted from the Cursor original to run in Claude Code and claude.ai. what changed:

- models: Cursor's opus/grok panel became a Claude ladder (`haiku` < `sonnet` < `opus` < `fable`). slugs are `<alias>-<effort>` (e.g. `opus-xhigh`, `fable-max`) and split into the Agent tool's `model` and `effort` parameters.
- subagents: `Task` → `Agent`. `generalPurpose` → `general-purpose`, `readonly: true` → `subagent_type: Explore`, `environment: "cloud"` → `isolation: "worktree"`.
- config: `~/.cursor/rules/pstack-models.mdc` → `~/.claude/rules/pstack-models.md`. transcripts under `~/.claude/projects/`.
- removed Cursor-only dependencies: `cursor-team-kit` (`/deslop`, `control-ui`, `control-cli`), Cursor's `create-skill` (→ `skill-creator`), `/loop` (→ `ScheduleWakeup`/`Monitor`), Bugbot (→ any review bot, e.g. Claude Code review). `make-bot-ui` still targets Cursor automation webhooks and is not useful here.

## install

claude.ai (all projects): Customize → Plugins → Add → Upload plugin → `pstack.zip`.

Claude Code (all projects): add a marketplace that lists this plugin, then `claude plugin install pstack@<marketplace> --scope user`.

Then run `/setup-pstack` to pick a budget and confirm the model roles.''')
p.write_text(t)
print("ok")
