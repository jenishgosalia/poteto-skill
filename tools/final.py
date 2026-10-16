import pathlib, re, sys
root=pathlib.Path(sys.argv[1])
p=root/'skills/interrogate/SKILL.md'; t=p.read_text()
t=t.replace("| Reviewer A | `opus-xhigh` |\n| Reviewer B | `sonnet-xhigh` |","| Reviewer A | `fable-xhigh` |\n| Reviewer B | `opus-xhigh` |\n| Reviewer C | `sonnet-xhigh` |\n| Reviewer D | `haiku-xhigh` |")
t=t.replace("and `model` set to its configured entry","and `model` and `effort` set from its configured entry")
p.write_text(t)
for p in root.rglob('*.md'):
    t=p.read_text(); o=t
    t=t.replace("Pick each subagent's reasoning level and fast or standard speed for the job","Pick each subagent's effort for the job")
    t=t.replace("reasoning level and fast or standard speed","effort")
    t=t.replace('`subagent_type: "poteto-agent"`','`subagent_type: "pstack:poteto-agent"`')
    t=t.replace('If the Agent tool does not resolve the bare name, use the plugin-scoped form `pstack:poteto-agent`.','The bare name `poteto-agent` also resolves when no other plugin defines one.')
    t=t.replace('`subagent_type: "comment-sicko"`','`subagent_type: "pstack:comment-sicko"`')
    if t!=o: p.write_text(t)
for p in list(root.rglob('SKILL.md'))+list((root/'agents').glob('*.md')):
    t=p.read_text(); m=re.match(r'---\n(.*?)\n---\n',t,re.S)
    if not m: continue
    drop=('icon','is_background') if p.parent.name=='agents' else ('icon','is_background','color')
    lines=[l for l in m.group(1).split('\n') if not l.split(':')[0] in drop]
    new='---\n'+'\n'.join(lines)+'\n---\n'+t[m.end():]
    if new!=t: p.write_text(new)
