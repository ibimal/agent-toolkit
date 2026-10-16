# docs/sdlc/config template

`docs/sdlc/config` is TOML. Fill in what you found; leave out what does not
apply. Other skills read it: `second-opinion` reads the other-family CLIs,
`review-change` and `review-plan` read the ladder, `code-health` reads the
health command, and every writer reads the tracker.

```toml
# Workflow config. Written by setup; edit it freely.

tracker = "local"            # local, github, jira or linear
tracker_project = ""         # for example owner/repo, or a project key
health_command = "make health"
verify_command = ""          # filled in by the stack pass

# One table per device and harness. The device name is the host name.
[models.my-laptop.claude-code]
models = ["claude-opus-5-5"]                  # same-family models reachable here
effort_scale = ["low", "medium", "high", "xhigh", "max"]
other_family_clis = ["codex"]                 # CLIs second-opinion may call

[ladder]
# Rung 1: a model from another family, through second-opinion.
# Rung 2: the strongest same-family model at one effort level above the
# writer's, capped at max, in a fresh context with an adversarial prompt.
rung1 = "second-opinion"
rung2 = "same-family, effort +1, fresh context"
feature_s = "rung1"          # set to "rung2" if review slows small work
```
