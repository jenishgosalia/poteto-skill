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
