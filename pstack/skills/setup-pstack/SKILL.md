---
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
