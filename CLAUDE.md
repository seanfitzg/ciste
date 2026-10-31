# Ciste

A learning project for the LangChain Certified Agent Engineer exam. The developer writes the exam-relevant code by hand, because writing it is how they learn it.

## Who writes what

Every ticket (GitHub issue and `BACKLOG.md` entry) has exactly one ownership label:

- `by-hand`: the developer writes all of it. Never write or edit code or prose deliverables for it, even when asked to "implement" or "fix" the issue. Instead give hints, explain concepts, point to docs pages, or review what the developer wrote.
- `owner-tbd`: not exam material and not yet decided. Ask the developer before writing anything, and once they decide, swap the label to `by-hand` or `claude`.
- `claude`: Claude may do the work.

If a ticket has no ownership label, or the request doesn't map to a ticket, treat it as `by-hand` and ask.

## References

- `GLOSSARY.md`: use its terms in code, tickets and notes.
- `docs/adr/`: decisions already made; don't relitigate them silently.
- `BACKLOG.md`: tickets, labels, schedule and unverified API details.
- `docs/study_guide.pdf`: licensed study material, gitignored. Never commit it or quote it at length.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues (`seanfitzg/ciste`) via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Triage roles map to this repo's own labels (`owner-tbd`, `question`, `claude`, `by-hand`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
