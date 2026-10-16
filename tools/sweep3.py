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
]
for p in root.rglob('*.md'):
    t=p.read_text(); o=t
    for a,b in subs: t=re.sub(a,b,t)
    if t!=o: p.write_text(t); print("edited",p)
