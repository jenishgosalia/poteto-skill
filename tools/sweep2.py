import re, pathlib, sys
root = pathlib.Path(sys.argv[1])
subs = [
 (r'grok-4\.7-xhigh-fast', 'sonnet-xhigh'),
 (r'claude-opus-5-5-xhigh', 'opus-xhigh'),
 (r'claude-opus-5-5-max', 'fable-max'),
 (r'grok-4\.7-medium-fast', 'sonnet-medium'),
 (r'claude-opus-5-5-medium', 'opus-medium'),
 (r'~/\.cursor/rules/pstack-models\.mdc', '~/.claude/rules/pstack-models.md'),
 (r'pstack-models\.mdc', 'pstack-models.md'),
 (r'~/\.cursor/plugins/', '~/.claude/plugins/'),
 (r'~/\.cursor/projects/', '~/.claude/projects/'),
 (r'/\.cursor/projects/', '/.claude/projects/'),
 (r'If the Task tool rejects', 'If the Agent tool rejects'),
 (r'Task tool', 'Agent tool'),
 (r'`Task` calls?', lambda m: m.group(0).replace('Task','Agent')),
 (r'Task subagent', 'Agent subagent'),
 (r'every `Task` call', 'every `Agent` call'),
 (r'Task `model`', 'Agent `model`'),
 (r'Spawn `Task` with', 'Spawn an `Agent` with'),
 (r'with the Task tool', 'with the Agent tool'),
 # family sentences
 (r' Families go by prefix: `claude-\*`, and `grok-\*` with `cursor-grok-\*` and `composer-\*`\. A refused `composer-\*` entry runs on `sonnet-xhigh`\. With no family match, use `opus-xhigh`\.', ' Families are the Claude model aliases `haiku`, `sonnet`, `opus`, and `fable`. With no family match, use `opus-xhigh`.'),
 (r' Families go by prefix: `claude-\*`, and `grok-\*` with `cursor-grok-\*` and `composer-\*`\. A refused `composer-\*` entry runs on Reviewer B\'s default\. With no family match, use Reviewer A\'s default\.', ' Families are the Claude model aliases `haiku`, `sonnet`, `opus`, and `fable`. With no family match, use Reviewer A\'s default.'),
 (r'use the closest valid slug of the same family from its error message', 'use the closest valid alias and effort from its error message'),
 (r'agent mode \(`readonly: false`\)', '`subagent_type: general-purpose`'),
 (r'`subagent_type: general-purpose`, `model` from the `reflect judgment, divergent, synthesizer` line \(default `opus-xhigh`\), `subagent_type: general-purpose`', '`subagent_type: general-purpose`, `model` from the `reflect judgment, divergent, synthesizer` line (default `opus-xhigh`)'),
 (r"- `/deslop`, `control-cli`, and `control-ui` ship in the `cursor-team-kit` plugin\.\n", ''),
 (r"- `/loop` and `/skill-creator` are Cursor built-ins\.", "- `skill-creator` ships in Anthropic's skills plugin. Scheduled wake-ups use Claude Code's `ScheduleWakeup` and `Monitor` tools."),
 (r'the slop-strip \(the \*\*unslop\*\* skill over the diff \(code and comments included\)\)', 'the slop-strip (the **unslop** skill over the diff)'),
]
changed=0
for p in root.rglob('*.md'):
    t=p.read_text(); o=t
    for a,b in subs: t=re.sub(a,b,t)
    if t!=o: p.write_text(t); changed+=1
print("files changed",changed)
