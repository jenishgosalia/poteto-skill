# pstack-claude

A Claude Code / claude.ai port of [pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT, Lauren Tan), pinned from cursor/plugins@2f83774.

## Install in Claude Code (all projects)

```
claude plugin marketplace add <your-github-user>/pstack-claude
claude plugin install pstack@pstack-claude --scope user
cp rules/pstack-models.md ~/.claude/rules/pstack-models.md   # or run /pstack:setup-pstack
```

## Install in claude.ai (all projects)

Customize → Plugins → Add → Upload plugin → `pstack.zip` (built from `pstack/`).

Skills are namespaced: `/pstack:poteto-mode`, `/pstack:setup-pstack`, `/pstack:unslop`, …
