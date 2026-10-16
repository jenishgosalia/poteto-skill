# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# Slug is <alias>-<effort>: alias in haiku, sonnet, opus, fable. Effort in low, medium, high, xhigh, max.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Agent `model` and `effort`). Alias entries in a panel list still count toward its fan-out.
# budget: medium (high)
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: opus-high
hardest tasks: fable-xhigh
how explorer: sonnet-high
how explainer: opus-high
why investigators: sonnet-high
why synthesizer: opus-high
reflect tooling: sonnet-high
reflect judgment, divergent, synthesizer: opus-high
arena runners: fable-high, opus-high, sonnet-high
arena cross-judge pool: fable-high, opus-high, sonnet-high
swarm workers: sonnet-high
architect runners: fable-high, opus-high, sonnet-high
interrogate reviewers: fable-high, opus-high, sonnet-high, haiku-high
