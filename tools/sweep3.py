import re, pathlib, sys
root=pathlib.Path(sys.argv[1])
subs=[
 (r'a `Task` prompt naming its path', 'an `Agent` prompt naming its path'),
 (r'each a Cursor cloud agent, runs the change the way a user would with the matching control skill \(such as `control-ui` or `control-cli`[^.]*\)', 'each an `Agent` subagent in its own worktree, runs the change the way a user would (browser automation for UIs, the CLI directly for CLIs)'),
 (r"Drive a long or stubborn hunt with Cursor's `/loop` command\.", 'Drive a long or stubborn hunt with a scheduled wake-up (`ScheduleWakeup` or `Monitor`).'),
 (r'a nested spawn has the full Task schema including `environment`', 'a nested spawn has the full Agent schema including `isolation`'),
 (r'Prefer a different model family from the parent\'s\. Spawn one readonly judge subagent', "Prefer a different alias from the parent's. Spawn one `Explore` (read-only) judge subagent"),
 (r"choose from `opus-xhigh` and `sonnet-xhigh`", "choose from `fable-xhigh`, `opus-xhigh`, and `sonnet-xhigh`"),
 (r"default to one each on `opus-xhigh` and `sonnet-xhigh`", "default to one each on `fable-xhigh`, `opus-xhigh`, and `sonnet-xhigh`"),
 (r"use `opus-xhigh` and `sonnet-xhigh`\.", "use `fable-xhigh`, `opus-xhigh`, and `sonnet-xhigh`."),
 # upstream 0.15.26+ (ae5650f)
 (r'runs `/deslop` and `/no-comments`', 'runs **unslop** and `/no-comments`'),
 (r'Run workers on a new cloud VM \(`isolation: "worktree"`\) unless the work needs this machine: a `control-ui` or `control-cli` runtime check \(from `cursor-team-kit`\),', 'Run workers in a fresh worktree (`isolation: "worktree"`) unless the work needs this checkout: a runtime check against a local browser or CLI,'),
 (r'through its control skill \(such as `control-ui` or `control-cli` from `cursor-team-kit`\) or a named driver', 'through browser automation or the CLI directly, or a named driver'),
 (r" Families go by prefix: `claude-\*`, and `grok-\*` with `cursor-grok-\*` and `composer-\*`\. A refused `composer-\*` entry runs on `sonnet-xhigh`\.", ' Families are the Claude model aliases `haiku`, `sonnet`, `opus`, and `fable`.'),
 # poteto-help: upstream now describes its own Claude Code install and run-time adapter; this port rewrites names instead.
 (r"pstack is built for Cursor, and it also installs in Claude Code with `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`\. There, each command takes a `pstack:` prefix, such as `/pstack:poteto-mode`\. The \[Claude Code adapter\]\(\.\./\.\./docs/harness/claude-code\.md\) maps the Cursor names, and a step that needs a Cursor-only feature, such as (?:Bugbot|the review bot) or Automations, is skipped with a one-line note\.\n\nOther tools can read the skills, because they use the Agent Skills format\. But most workflow skills, including `/poteto-mode`, `/how`, `/why`, and `/teach`, spawn Cursor subagents with per-role models, and Custom Modes and `/loop` are Cursor features, so those parts may not work there\.",
  "This build of pstack is ported to Claude Code from the Cursor original: the Cursor names are rewritten in the skills themselves. (Upstream also publishes its own Claude Code build, `/plugin marketplace add cursor/plugins` then `/plugin install pstack@cursor-plugins`, with a [run-time adapter](https://github.com/cursor/plugins/blob/main/pstack/docs/harness/claude-code.md) that maps the names instead.) Each command takes a `pstack:` prefix, such as `/pstack:poteto-mode`. A step that needs a Cursor-only feature, such as Automations, is skipped with a one-line note.\n\nOther tools can read the skills, because they use the Agent Skills format. The workflow skills, including `/poteto-mode`, `/how`, `/why`, and `/teach`, spawn Claude Code subagents through the Agent tool with per-role models and effort levels. In the claude.ai chat app, the skills load but there is no subagent fan-out, so `/poteto-mode` runs its playbook inline."),
 (r'Spawn workers with `Task`\.', 'Spawn workers with the `Agent` tool.'),
 (r"In Claude Code, run `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`\. Claude Code prefixes plugin commands, so each command in this guide takes a `pstack:` prefix there, such as `/pstack:setup-pstack`, which writes its model rule to `~/\.claude/rules/pstack-models\.md`\. The \[Claude Code adapter\]\(\.\./harness/claude-code\.md\) covers the other differences\.",
  "This build is ported to Claude Code; install it from the `poteto-skill` marketplace (see the README). Claude Code prefixes plugin commands, so each command in this guide takes a `pstack:` prefix, such as `/pstack:setup-pstack`, which writes its model rule to `~/.claude/rules/pstack-models.md`. Upstream's own Claude Code build (`/plugin marketplace add cursor/plugins`) ships a [run-time adapter](https://github.com/cursor/plugins/blob/main/pstack/docs/harness/claude-code.md) instead."),
 (r'``general-purpose``', '`general-purpose`'),
 (r'\b([Tt]he|a) the review bot', r'\1 review bot'),
 # README: drop upstream's own "in claude code" install block (rewrite.py adds this port's) and keep one pointer to it.
 (r"(?s)in claude code:\n\n```bash\n/plugin marketplace add cursor/plugins\n/plugin install pstack@cursor-plugins\n```\n\n.*?ci fails while the generated copy is out of date\.\n\n",
  "upstream also publishes its own claude code build (`/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`), generated into [`harness/pstack/`](https://github.com/cursor/plugins/tree/main/harness/pstack) with a run-time [name adapter](https://github.com/cursor/plugins/blob/main/pstack/docs/harness/claude-code.md). this port predates it and rewrites the cursor names in the skills directly.\n\n"),
]
for p in root.rglob('*.md'):
    t=p.read_text(); o=t
    for a,b in subs: t=re.sub(a,b,t)
    if t!=o: p.write_text(t); print("edited",p)
