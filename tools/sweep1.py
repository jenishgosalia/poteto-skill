import re, pathlib, sys
root = pathlib.Path(sys.argv[1])
subs = [
 (r'`subagent_type: generalPurpose`, `readonly: true`', '`subagent_type: Explore` (read-only)'),
 (r'`subagent_type: generalPurpose` and `readonly: true`', '`subagent_type: Explore` (the read-only agent)'),
 (r'`subagent_type: generalPurpose`, agent mode \(`readonly: false`\)', '`subagent_type: general-purpose`'),
 (r'`subagent_type: generalPurpose`, `model` from', '`subagent_type: general-purpose`, `model` from'),
 (r'Every spawn is `generalPurpose` with `readonly: false` \(agent mode\)\. \*\*Do not use readonly/Ask mode\.\*\* It strips MCP access, which disables', 'Every spawn is `subagent_type: general-purpose`. **Do not use the `Explore` agent here.** It is read-only and strips MCP access, which disables'),
 (r'`subagent_type: generalPurpose`', '`subagent_type: general-purpose`'),
 (r'generalPurpose', '`general-purpose`'),
 (r'Substituting ``general-purpose``', 'Substituting `general-purpose`'),
 (r'readonly: true', 'subagent_type: Explore'),
 (r'`AskQuestion`', '`AskUserQuestion`'),
 (r'\bAskQuestion\b', 'AskUserQuestion'),
 (r"Cursor's built-in `create-skill` skill", 'the `skill-creator` skill'),
 (r"Cursor's built-in `create-skill`", 'the `skill-creator` skill'),
 (r'the \*\*create-skill\*\* skill \(Cursor\'s built-in for authoring SKILL\.md files\)', 'the **skill-creator** skill (Anthropic\'s skill for authoring SKILL.md files)'),
 (r'`create-skill`', '`skill-creator`'),
 (r'create-skill', 'skill-creator'),
 (r'the `deslop` skill from the `cursor-team-kit` plugin \(`/deslop`\)', 'the **unslop** skill over the diff (code and comments included)'),
 (r'Run `/deslop` from `cursor-team-kit` over the diff before commit', 'Run the **unslop** skill over the diff before commit'),
 (r'Run `/deslop` before each commit', 'Run **unslop** over the diff before each commit'),
 (r'`interrogate`, `/deslop`, and `/no-comments`', '`interrogate`, `unslop`, and `/no-comments`'),
 (r'- Shipping UI / IDE / CLI → the matching control skill\. `cursor-team-kit` publishes `control-cli` \(CLIs and TUIs\) and `control-ui` \(browser / Electron / web UIs\)\.', '- Shipping UI / IDE / CLI → drive the real surface yourself. Web and Electron UIs through a browser-automation tool (Claude in Chrome, Playwright, or CDP), CLIs and TUIs by running them. If the project has a `verify-*` skill, use it.'),
 (r'\*\*Control skill\.\*\* Pick it by surface\. Browser, Electron, and web UIs use `control-ui` from `cursor-team-kit`\. CLIs and TUIs use `control-cli` from `cursor-team-kit`\.', '**Control surface.** Pick it by surface. Browser, Electron, and web UIs through browser automation (Claude in Chrome, Playwright, or CDP). CLIs and TUIs by running them directly.'),
 (r'Drive through `control-ui` or `control-cli` from `cursor-team-kit`\.', 'Drive it through browser automation or the CLI directly.'),
 (r'`control-ui` or `control-cli` runtime verification \(from `cursor-team-kit`\)', 'runtime verification against a local browser or CLI'),
 (r'`environment: "cloud"`', '`isolation: "worktree"`'),
 (r'environment: "cloud"', 'isolation: "worktree"'),
 (r'a Cursor restart', 'a Claude Code restart'),
 (r'After a Cursor restart', 'After a Claude Code restart'),
 (r"using Cursor's `/loop` command \(a built-in, not a pstack skill\)", 'using a scheduled wake-up (Claude Code\'s `ScheduleWakeup` or `Monitor` tool, or a watcher subagent)'),
 (r"This playbook replaces Cursor's built-in babysit skill for these requests, so do", 'This playbook owns these requests, so do'),
 (r", not Cursor's built-in babysit skill, whose description matches the same words", ''),
 (r'Bugbot or the agentic security review commented', 'A review bot (Claude Code review, GitHub Copilot review, or an agentic security scan) commented'),
 (r'\*\*Bugbot is triaged skeptically, always\.\*\*', '**Review-bot comments are triaged skeptically, always.**'),
 (r'Bugbot', 'the review bot'),
 (r'bugbot comments', 'review-bot comments'),
 (r"the cloud agent's status in the Cursor dashboard", "the agent's status via `ListAgents`"),
 (r"list the available MCPs from the Cursor environment\. Use the available-tools map when present\. Otherwise inspect the `mcps/` directory Cursor exposes for enabled MCP servers\.", 'list the available MCP servers in this session (`ListConnectors` or `ToolSearch`, or `claude mcp list`).'),
 (r'`\.cursor/skills/', '`.claude/skills/'),
 (r'\.cursor/skills/', '.claude/skills/'),
 (r'~/\.cursor/skills/', '~/.claude/skills/'),
 (r'\.cursor/worktrees/', '.claude/worktrees/'),
]
changed=0
for p in root.rglob('*.md'):
    t=p.read_text(); o=t
    for a,b in subs: t=re.sub(a,b,t)
    if t!=o: p.write_text(t); changed+=1
print("files changed",changed)
