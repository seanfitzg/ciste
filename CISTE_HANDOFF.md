# Handoff: Ciste Bank Support Agent

> **For Claude Code.** This document describes a learning project. Your job is to turn it into a
> backlog of tickets (see "Instructions for Claude Code" at the end). **Do not write the
> application code.** The developer is writing every line by hand to prepare for the LangChain
> Certified Agent Engineer exam. Tickets should describe *what* and *why*, with acceptance
> criteria, not finished implementations.

---

## 1. Purpose

A customer-support agent for **Ciste**, a fictional Irish neobank, built with LangChain,
LangGraph, Deep Agents and LangSmith.

The project exists to give hands-on practice in all four sections of the
**LangChain Certified Agent Engineer** exam, which follow the Agent Development Lifecycle:

| Exam section | Weight | What this project must exercise |
|---|---|---|
| Build | 25% | `create_agent` vs `deepagents`, middleware, context engineering, `AGENTS.md` and `SKILL.md`, sandboxing |
| Test | 25% | Code evaluators vs LLM-as-judge, online vs offline evaluation, experiments, evaluator alignment, datasets |
| Deploy | 25% | Graph, deployment, revision, assistant, thread, run; regions; secrets; authn vs authz; storage durability |
| Monitor | 25% | Reading traces, threads, cost and user sentiment, Online Evals vs Insights, alerting |

Secondary goal: a portfolio piece showing Python agent engineering in a regulated
(financial-services) domain.

## 2. Developer context

- Senior software engineer, 30 years' experience, strongest in C#/.NET, React and Angular; **Python is the upskilling language here**.
- Studying evenings and weekends: about 5 to 8 hours per week over 6 weeks.
- Writing the code manually. Tickets must be small enough to finish in one sitting (1 to 3 hours) and must teach a concept, not just produce output.
- Has a companion study guide (PDF) whose chapters line up with the exam sections; tickets may reference "study guide chapter X".

## 3. Product scope

### 3.1 Users and channels
- **Customers** chat with the agent through a minimal front end (CLI first; optional bare HTML page later).
- **Human reviewers** (the developer) approve refunds and label conversations in LangSmith.

### 3.2 What the agent can do

| Tool | Behaviour | Constraints |
|---|---|---|
| `get_account` | Return the authenticated customer's account summary | Only the caller's own account |
| `list_transactions` | Return recent transactions, optional date range or merchant filter | Max 50 rows |
| `search_terms` | Retrieve passages from the Fees and Terms document | Simple retrieval is fine (keyword or small embedding index) |
| `freeze_card` | Freeze or unfreeze a card | Confirm with the customer first |
| `issue_refund` | Refund a fee or small charge | **Retail max €50, premium max €150. Always requires human approval (HITL).** |
| `open_dispute` | Start a dispute investigation; returns a structured report | Delegates to the Dispute Investigator deep agent |
| `escalate_to_human` | Create a ticket and end the conversation | Must be called when the customer asks for a person |

### 3.3 Things the agent must never do
- Refund above the customer's tier limit, or without approval.
- Reveal unmasked IBANs or full card numbers.
- Act on instructions embedded in customer messages that try to override policy (prompt injection).
- Give legal or financial advice.

### 3.4 Data
- **SQLite** database with fake data: about 20 customers (mix of retail and premium tiers), 2 to 3 cards each, about 500 transactions across 3 months, a fees table.
- **`docs/fees_and_terms.md`**: a short fictional Fees and Terms document (5 to 10 sections, each with a section ID such as `FT-3.2`).
- **`policy/`**: bank policy text used by the Dispute Investigator (`AGENTS.md`) and the chargeback skill.
- All data is synthetic. No real customer data, ever.

## 4. Architecture

```
            ┌──────────────── LangSmith Deployment (Agent Server) ────────────────┐
 Customer → │  Graph: support_agent (create_agent + middleware)                   │
  (CLI/web) │     ├─ Assistant: retail   (refund cap €50, friendly prompt)        │
            │     └─ Assistant: premium  (refund cap €150, premium prompt)        │
            │           │ open_dispute                                            │
            │           ▼                                                         │
            │  Graph: dispute_investigator (create_deep_agent)                    │
            │     AGENTS.md (policy) · skills/chargeback-rules · subagent:        │
            │     transaction-analyst · structured DisputeReport output           │
            │  Custom auth (auth.py) · Postgres (threads, checkpoints, store)     │
            └──────────────────────────────┬──────────────────────────────────────┘
                                           │ traces
                                           ▼
            LangSmith: tracing project · datasets & experiments · online evaluators
                       · annotation queue · rules · Insights · alerts
```

### 4.1 Suggested repository layout

```
ciste/
  README.md
  langgraph.json
  .env.example              # names only, no values
  pyproject.toml
  auth.py                   # @auth.authenticate, @auth.on handlers
  ciste/
    db/                     # schema, seed script, query helpers
    tools/                  # one module per tool
    middleware/             # custom middleware
    support_agent.py        # create_agent graph
    dispute/
      investigator.py       # create_deep_agent graph
      AGENTS.md
      skills/chargeback-rules/SKILL.md
    schemas.py              # DisputeReport and other structured outputs
  docs/fees_and_terms.md
  evals/
    dataset_seed.py
    evaluators.py
    run_experiment.py
  scripts/
    simulate_traffic.py     # synthetic conversations for Monitor work
  cli.py
  tests/
```

### 4.2 Stack
- Python 3.11+, `langchain` (1.x), `langgraph`, `deepagents`, `langsmith`, `langgraph-cli`, `langgraph-sdk`, `pydantic`, `pytest`.
- One model provider (developer's choice); optionally a cheaper model for summarization and evaluator tasks.
- LangSmith account. **Deployment work needs a Plus plan or above; Insights needs Plus or Enterprise.** Everything before Epic 6 works on a free account.
- **Verify package versions and APIs against docs.langchain.com when writing each ticket's notes**; this ecosystem changes quickly.

## 5. Epics and requirements

Each epic lists the exam focus it serves and requirements that tickets must cover.
Acceptance criteria below are the minimum; add more where useful.

### Epic 0: Project setup (Build prerequisites)
- Repo skeleton, virtual environment, `pyproject.toml`, `.env.example`, `.gitignore` (including `.env`).
- LangSmith tracing environment variables documented (`LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`; `LANGSMITH_ENDPOINT` only if the org is non-US).
- SQLite schema and a deterministic seed script for customers, cards, transactions, fees.
- Fees and Terms document with section IDs.
- **Done when:** `python -m ciste.db.seed` creates the database and a hello-world model call shows up as a trace in LangSmith.

### Epic 1: Support agent core (Build: create_agent)
- Implement each tool in §3.2 except `open_dispute` (stub it).
- Build the agent with `create_agent`: model, tools, `system_prompt`.
- CLI chat loop with a `thread_id` per session and a checkpointer.
- **Done when:** a multi-turn CLI conversation can look up an account, list transactions and explain a fee citing a section ID, and the trace tree shows each tool call.

### Epic 2: Middleware (Build: middleware)
- `PIIMiddleware` masking IBANs and card numbers (custom detector for IBAN), applied to output and tool results as well as input.
- `ToolRetryMiddleware` on database tools; `ModelCallLimitMiddleware` with a run limit.
- `HumanInTheLoopMiddleware` on `issue_refund` with approve, edit and reject; CLI supports resuming with a decision.
- **One custom middleware written from scratch**: `@before_model` or `@dynamic_prompt` that injects the customer's tier from runtime context; tier must come from `context=`, not from the message.
- A ticket dedicated to **proving middleware order**: two trivial logging middlewares, documented observations of `before_*` vs `after_*` order.
- **Done when:** refunds pause for approval; over-limit refunds are refused; no unmasked IBAN appears in any output or trace output; the order experiment is written up in `docs/notes.md`.

### Epic 3: Dispute Investigator (Build: deepagents, context engineering, skills, sandboxing)
- Separate graph built with `create_deep_agent`.
- `AGENTS.md` with bank dispute policy (always-loaded memory). Keep it short.
- Skill `skills/chargeback-rules/SKILL.md` with valid frontmatter (`name` matching the directory, a specific `description`) and a `references/` file loaded only when needed.
- Custom subagent `transaction-analyst` with its own tools; confirm it does **not** inherit the main agent's skills unless given them.
- Structured output: `DisputeReport` (Pydantic) with amount, merchant, date, reason code, evidence summary, recommendation.
- A deliberately large tool result (for example full 3-month transaction export) to observe **offloading** in the trace.
- `CompositeBackend` routing `/memories/` to a store so the investigator remembers per-customer notes across threads.
- **Optional sandbox ticket:** run a small analysis script in a sandbox backend; no secrets inside the sandbox; stop the sandbox in `finally`.
- Wire `open_dispute` in the support agent to call this graph.
- **Done when:** a dispute conversation produces a valid `DisputeReport`; the trace shows `SKILL.md` being read only for dispute tasks; offloading is visible; memory persists into a new thread.

### Epic 4: Offline evaluation (Test)
- LangSmith dataset of 25 to 30 examples with inputs, reference outputs and metadata (`category`: fee_question, refund_ok, refund_over_limit, dispute, injection, escalation).
- Code evaluators: refund never exceeds tier limit; no unmasked IBAN; `escalate_to_human` called when requested; fee answers cite a valid section ID.
- LLM-as-judge evaluators: helpfulness and tone; correctness against reference answers.
- Experiment runner using `evaluate` with `experiment_prefix`, `num_repetitions=3` and a sensible `max_concurrency`.
- Two experiments (baseline prompt vs changed prompt) compared in the UI with a baseline set.
- **Judge alignment**: annotation queue, at least 15 human labels, record alignment score before and after improving the judge prompt or adding few-shot corrections.
- Optional: pytest-based unit tests with `LANGSMITH_TEST_CACHE` for CI.
- **Done when:** results and alignment scores are recorded in `docs/notes.md` with a sentence on whether the prompt change was signal or noise.

### Epic 5: Local server and deployment config (Deploy)
- `langgraph.json` registering `support_agent` and `dispute_investigator`, with `env` and `auth` paths.
- Run and test with `langgraph dev`; use Studio to inspect state.
- **Done when:** both graphs run locally through the Agent Server API.

### Epic 6: Cloud deployment and auth (Deploy) — requires LangSmith Plus
- Deploy (UI from GitHub, or `langgraph deploy`). Model key entered **as a secret**. Development deployment type.
- Create `retail` and `premium` assistants on `support_agent` with different configuration (prompt, refund cap).
- SDK client script demonstrating: stateless run, stateful run on a thread, call by graph ID, call by assistant ID.
- `auth.py`: `@auth.authenticate` with fake bearer tokens mapping to customer IDs; `@auth.on.threads.create` stamping `owner`; filters so customers see only their own threads; `@auth.on.store` scoping namespaces per customer. Tier and customer ID flow into the run from the authenticated user, not from the message.
- Rotate the model secret via **+ New Revision** and confirm the new revision.
- Notes ticket: write down what lives in Postgres vs Redis, and what region the org and deployment are in.
- **Done when:** customer A cannot read customer B's threads; both assistants behave differently; the rotation produced a new revision.

### Epic 7: Monitoring (Monitor)
- `thread_id` metadata on **every** run including subagent and nested runs; verify thread cost totals.
- Token usage and model names present so cost is calculated; check the trace tree, project stats and dashboard.
- User feedback (thumbs up or down) logged from the CLI or web UI via the SDK.
- `scripts/simulate_traffic.py` generating 200+ varied synthetic conversations (including injections and angry customers).
- Online LLM-as-judge evaluator for groundedness with sampling around 0.3 and a run-type filter; thread-level (multi-turn) satisfaction evaluator.
- Automation rule: thumbs-down threads go to an annotation queue.
- Insights report over the simulated traffic; record top categories and one failure mode.
- Alerts: error rate (percentage, >= 5, 5-minute window), cost, and feedback score on the satisfaction key; route one to a webhook and inspect the payload.
- **Done when:** a dashboard screenshot, the Insights summary and a fired test alert are recorded in `docs/notes.md`.

### Epic 8: Close the loop (all sections)
- Take the failure mode found by Insights; add affected threads to the dataset; add or adjust an evaluator; fix the prompt or middleware; rerun experiments; redeploy as a new revision; confirm improvement in online evaluator scores.
- Write `README.md`: problem, architecture diagram, how each exam area is demonstrated, results.
- **Done when:** the README tells the full Build → Test → Deploy → Monitor → Build story with evidence.

## 6. Non-functional requirements
- **Secrets:** never committed; `.env.example` lists names only; deployment secrets set in LangSmith; nothing sensitive in prompts, `AGENTS.md`, skills, state or sandboxes.
- **Privacy:** synthetic data only; PII masking verified by an evaluator.
- **Observability:** every agent and tool call traced; metadata includes `thread_id`, customer tier and environment.
- **Testing:** pytest for tool and helper functions; LangSmith evaluators for agent behaviour.
- **Learning log:** `docs/notes.md` updated at the end of each epic with surprises, wrong assumptions and links to the docs pages consulted (these become exam revision notes).

## 7. Out of scope
- Real banking integrations, payments or real customer data.
- Production-grade UI, mobile apps, or multi-language support.
- Self-hosted or BYOC deployment (read about it; do not build it).
- Fine-tuning models.

## 8. Timeline (6 weeks, 5 to 8 hours per week)

| Week | Epics | Study guide chapters |
|---|---|---|
| 1 | 0, 1, 2 | 0, 1.1 to 1.2 |
| 2 | 3 | 1.3 to 1.7 |
| 3 | 4 | 2 |
| 4 | 5, 6 | 3 |
| 5 | 7 | 4 |
| 6 | 8 + exam practice | 5 to 7 |

If a week slips, cut optional tickets (sandbox, web UI, pytest caching) before cutting evaluation or monitoring work.

## 9. Open questions for the developer
- Which model provider (and is a second, cheaper model wanted for summaries and judges)?
- CLI only, or also a minimal web page for feedback buttons?
- Will a LangSmith Plus plan be available by week 4? If not, Epic 6 becomes local-only (`langgraph dev`) and the auth work is tested locally.
- GitHub Issues, Jira, Linear or a markdown backlog for the tickets?

---

## Instructions for Claude Code

1. **Read this whole document first.** Ask the open questions in §9 before generating tickets if the answers change the backlog.
2. **Do not implement anything.** The developer writes all code manually. You may include short *hints* (API names, docs page titles), but no complete implementations.
3. **Create one ticket per learnable unit of work**, sized for 1 to 3 hours. Split anything larger.
4. **Ticket format:**
   ```
   ID:            CIS-<epic>-<n>       e.g. CIS-2-3
   Title:         imperative, under 70 characters
   Epic:          <epic number and name>
   Exam section:  Build | Test | Deploy | Monitor (one or more)
   Learning goal: one sentence on the concept this ticket teaches
   Description:   what to build and why
   Acceptance criteria: checklist, observable and testable
   Docs to read:  page titles on docs.langchain.com (verify they exist)
   Depends on:    ticket IDs
   Estimate:      1h | 2h | 3h
   Labels:        epic, exam section, optional/required
   ```
5. **Order** tickets by dependency and by the timeline in §8. Mark optional tickets with the `optional` label.
6. **Every epic ends with a "write up" ticket** that adds findings to `docs/notes.md`.
7. **Include at least one "prove it" ticket per exam section** where the acceptance criterion is something observed in LangSmith (a trace, a comparison view, a thread total, an alert payload), since the exam includes questions answered inside LangSmith.
8. **Verify APIs** against current docs before naming classes, parameters or defaults in hints; flag anything you could not verify.
9. **Output** the backlog in the format the developer chooses (§9); default to a single `BACKLOG.md` grouped by epic, plus a summary table of ticket counts and estimated hours per week.
