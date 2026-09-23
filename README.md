# Provenance first-developer pilot

A benign, public Paper plugin used to exercise the Provenance console's
first-developer onboarding flow (Plan 08 exit gate) end to end: connect the
repository, take the proposed configuration and Action workflow, submit a
test-only candidate, and inspect its matrix.

The plugin only logs a readiness marker on enable. Release mode is
`test-only`; nothing is published anywhere.

Build locally with Java 21 and Python 3:

```sh
python3 scripts/build.py
```
