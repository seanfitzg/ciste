# Ciste Backlog

Tickets for the Ciste support agent, a learning project for the LangChain Certified Agent Engineer exam. Every ticket carries one ownership label (`by-hand`, `owner-tbd` or `claude`, below); tickets say *what* and *why*, with hints only.

- **Vocabulary:** [GLOSSARY.md](GLOSSARY.md). Tickets use its terms (Customer, Fee, Refund cap, Reviewer, Confirmation, and so on).
- **Decisions:** [ADR 0001](docs/adr/0001-dispute-investigator-invoked-in-process.md) (in-process investigator) and [ADR 0002](docs/adr/0002-customer-identity-from-auth-not-client-context.md) (identity from auth, not client context).
- **Study guide:** `docs/study_guide.pdf` (gitignored). "Guide §x" and "Lab n" refer to it.
- **Docs:** page titles are from docs.langchain.com as of 31 Oct 2026, with the path after each title so you can find it fast. Practising finding pages is itself exam prep.

## Labels

| Label | Meaning |
|---|---|
| `core` | Needed to cover the exam. Doing only core tickets still practises every exam focus area. |
| `stretch` | Depth, polish or portfolio value. Skip first when a week slips. |
| `plus` | Needs LangSmith Plus. Treat as `stretch` until the Plus decision on **Mon 23 Nov 2026**. |
| `prove-it` | Acceptance is something observed in LangSmith (trace, comparison view, thread total, alert payload). |
| `by-hand` | Exam material: the developer writes every line. Claude only gives hints, explains or reviews. |
| `owner-tbd` | Not exam material. Decide before starting whether the developer writes it or Claude does, then swap the label to `by-hand` or `claude`. |
| `claude` | Claude does the work (for now, the non-code content drafts). |
| `epic-N`, `build`, `test`, `deploy`, `monitor` | Epic and exam section. |

## Summary

| Epic | Core tickets | Core h | Stretch h |
|---|---|---|---|
| 0 Project setup | 4 | 5 | 0 |
| 1 Support agent core | 5 | 8 | 2 |
| 2 Middleware | 6 | 10 | 2 |
| 3 Dispute Investigator | 6 | 11 | 3 |
| 4 Offline evaluation | 6 | 11 | 2 |
| 5 Local server and auth | 4 | 8 | 7 |
| 6 Cloud deployment | 1 | 1 | 4 |
| 7 Monitoring | 7 | 11 | 3 |
| 8 Close the loop | 3 | 6 | 0 |
| **Total** | **42** | **71** | **23** |

### Schedule (core path, 6 weeks)

| Week | Dates | Core tickets | Core h | Guide |
|---|---|---|---|---|
| 1 | 2–8 Nov | CIS-0-1 … CIS-0-4, CIS-1-1 … CIS-1-4, CIS-1-6 | 13 | §0, §1.1 |
| 2 | 9–15 Nov | CIS-2-1 … CIS-2-5, CIS-2-7, CIS-3-1 | 12 | §1.2–1.4, Lab 1 |
| 3 | 16–22 Nov | CIS-3-2 … CIS-3-5, CIS-3-7, CIS-4-1 | 11 | §1.5–1.7, Lab 2 |
| 4 | 23–29 Nov | CIS-4-2 … CIS-4-5, CIS-4-7, CIS-5-1 | 11 | §2, Labs 3–4 · **Plus decision 23 Nov** |
| 5 | 30 Nov–6 Dec | CIS-5-2, CIS-5-3, CIS-5-7, CIS-6-4, CIS-7-1 … CIS-7-3 | 12 | §3, Lab 5 |
| 6 | 7–13 Dec | CIS-7-4 … CIS-7-6, CIS-7-10, CIS-8-1 … CIS-8-3 | 12 | §4, §5–7, Labs 6–8 |

> **Agreed 31 Oct 2026:** the core path is 71 h, done at about 12 h/week to keep the 6-week exam timeline. If a week slips, drop that week's stretch tickets first, then push the remaining core tickets into week 6.

### API spend (target about $20 total, rough estimates)

| Ticket | What runs | Rough cost |
|---|---|---|
| CIS-4-4 | 2 experiments × 30 examples × 3 repetitions + judges | $2–5 |
| CIS-4-5 | Judge re-runs during alignment | < $1 |
| CIS-7-3 | ~50 simulated conversations (mini model plays the Customer) | $1–3 |
| CIS-7-4 | Online judges at 0.3 sampling | < $1 |
| CIS-7-9 (stretch) | 200+ conversations | $5–10 |
| CIS-8-2 | Re-run experiments + fresh traffic | $2–5 |

Prices are not verified. Record actual spend per ticket in `docs/notes.md` and check against the OpenAI pricing page.

### Unverified API details

These are hints that could not be confirmed in the docs. Each affected ticket starts with a short spike.

1. Whether `ToolCallRequest` in `@wrap_tool_call` exposes the runtime/context (CIS-2-3). Fallback: resolve the Customer through the shared resolver.
2. How an `after_model` hook rewrites or removes a pending tool call on the last `AIMessage` (CIS-2-6). Docs only show `jump_to: "end"`.
3. Whether a tool span in LangSmith records the raw tool output before `PIIMiddleware` masks it (CIS-2-4). The ticket's first job is to observe this.
4. How assistant configuration reaches the graph in the current Agent Server (context vs `configurable`) (CIS-5-2).
5. How a tool reads `langgraph_auth_user` (docs show `config["configurable"]` in a node; the tool equivalent is unconfirmed) (CIS-5-3).
6. Whether `langgraph dev` enforces custom auth (CIS-5-3).
7. Whether custom routes are covered by custom auth (CIS-5-5).
8. Whether nested in-process graph runs inherit thread metadata automatically (CIS-7-1). The ticket observes it.
9. Whether alerts are available on the free plan (CIS-7-6).
10. Current OpenAI model IDs and prices. Docs examples use `gpt-5.5` and `gpt-5.4-mini` (CIS-0-2).
11. The docs page title for the Agent Server data plane (CIS-6-4). Guide §3.3 covers the content.

---

## Content drafted by Claude

These are prerequisites the developer doesn't write. Ask Claude for them before the ticket that depends on them.

### CIS-C-1 · Draft the Fees and Terms document
- **Labels:** `claude` `epic-0`
- **Description:** `docs/fees_and_terms.md`: 7–8 short sections, each with an ID like `FT-3.2`. Fees must include one above €50 and one above €150 so both Tiers have over-cap Refund cases, plus overdraft, card replacement, international transfer and returned payment fees. It ends with a no-advice disclaimer section.
- **Needed by:** CIS-1-2, CIS-0-3

### CIS-C-2 · Draft the dispute policy text
- **Labels:** `claude` `epic-3`
- **Description:** `policy/dispute_policy.md` (source for the `AGENTS.md` you write) and `policy/chargeback_reason_codes.md` (source for the skill's `references/` file): time limits, evidence rules, reason codes (duplicate, not received, fraud, chip-and-PIN authorised).
- **Needed by:** CIS-3-1, CIS-3-2

### CIS-C-3 · Draft the seed-data specification
- **Labels:** `claude` `epic-0`
- **Description:** `docs/seed_spec.md`: tables, ~20 named Customers with Tiers, card patterns, transaction mix over 3 months, and the edge cases evals rely on: a duplicate merchant charge, a retail Fee > €50, a premium Fee > €150, an already-refunded Fee, a frozen Card, a chip-and-PIN transaction.
- **Needed by:** CIS-0-3

---

## Epic 0 · Project setup

### CIS-0-1 · Initialise the uv project in the public GitHub repo
- **Epic:** 0 Project setup · **Exam section:** Build · **Estimate:** 1h · **Labels:** `owner-tbd` `epic-0` `build` `core`
- **Depends on:** —
- **Learning goal:** How `uv` manages the Python version, virtual environment, dependencies and lockfile, and how to keep secrets out of a public repo from the first commit.
- **Description:** The public repo already exists at [seanfitzg/ciste](https://github.com/seanfitzg/ciste), holding the planning files. Create the project with `uv` using the layout in the handoff §4.1. Add the stack dependencies, write `.env.example` with names only, extend the existing `.gitignore`, and push.
- **Acceptance criteria:**
  - [ ] `uv sync` on a fresh clone installs `langchain`, `langchain-openai`, `langgraph`, `deepagents`, `langsmith`, `langgraph-cli[inmem]`, `langgraph-sdk`, `pydantic`, `pytest`
  - [ ] `.env.example` lists `OPENAI_API_KEY`, `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (and a commented `LANGSMITH_ENDPOINT` for non-US orgs) with no values
  - [ ] `git check-ignore .env ciste.db docs/study_guide.pdf` reports all three
  - [ ] The repo's history still contains no secrets and no PDF
  - [ ] `uv run python -c "import ciste"` succeeds
- **Hints:** `uv init`, `uv add`, `uv run`. The `[inmem]` extra is what `langgraph dev` needs.
- **Docs to read:** [Run a local server](https://docs.langchain.com/oss/python/langgraph/local-server) for the CLI install line. Guide §0.

### CIS-0-2 · Trace a first OpenAI call in LangSmith
- **Epic:** 0 Project setup · **Exam section:** Monitor · **Estimate:** 1h · **Labels:** `by-hand` `epic-0` `monitor` `core` `prove-it`
- **Depends on:** CIS-0-1
- **Learning goal:** Tracing turns on through environment variables alone, and the org's region decides whether `LANGSMITH_ENDPOINT` is needed.
- **Description:** A tiny `scripts/hello.py` calls the capable model and the mini model through `init_chat_model`. Confirm both appear as traces with model name, tokens and cost. Choose and record the two model IDs.
- **Acceptance criteria:**
  - [ ] Two traces in project `ciste-dev`, one per model, each showing model name, input/output tokens and a cost
  - [ ] `docs/notes.md` records the chosen model IDs and their prices per million tokens
  - [ ] Notes say whether the org is US or EU and whether `LANGSMITH_ENDPOINT` was needed
- **Hints:** `init_chat_model("openai:<model>")`; load `.env` with `uv run --env-file .env` or `python-dotenv`. Verify current model IDs and prices on OpenAI's site.
- **Docs to read:** [Tracing quickstart](https://docs.langchain.com/langsmith/observability-quickstart); [Models](https://docs.langchain.com/oss/python/langchain/models); [OpenAI integrations](https://docs.langchain.com/oss/python/integrations/providers/openai); [Cost tracking](https://docs.langchain.com/langsmith/cost-tracking). Guide §4.1, §4.4.

### CIS-0-3 · Create the SQLite schema and deterministic seed script
- **Epic:** 0 Project setup · **Exam section:** Build · **Estimate:** 2h · **Labels:** `claude` `epic-0` `build` `core`
- **Depends on:** CIS-0-1, CIS-C-3
- **Learning goal:** Python's `sqlite3`, dataclasses and seeded randomness. Deterministic data is what makes evaluation results comparable later.
- **Description:** `ciste/db/schema.sql` plus `python -m ciste.db.seed`, which rebuilds `ciste.db` from `docs/seed_spec.md`. Tables: customers, accounts, cards, transactions (Merchant charges and Fees), fees catalogue (with FT section ID), refunds, disputes, escalations. Store full IBANs and card numbers, as a real bank would; masking comes in CIS-2-4.
- **Acceptance criteria:**
  - [ ] Running the seed twice produces identical databases (compare a hash of `iterdump()` output)
  - [ ] About 20 Customers with mixed Tiers, 2–3 Cards each, about 500 transactions over 3 months
  - [ ] Every edge case in `seed_spec.md` exists
  - [ ] A uniqueness constraint makes a second Refund of the same Fee impossible
  - [ ] A pytest test checks row counts and the edge cases
- **Hints:** `random.Random(seed)`; `conn.executescript`; `conn.iterdump()`.
- **Docs to read:** Python `sqlite3` docs (not on docs.langchain.com).

### CIS-0-4 · Write up Epic 0
- **Epic:** 0 Project setup · **Exam section:** Build, Monitor · **Estimate:** 1h · **Labels:** `by-hand` `epic-0` `build` `monitor` `core`
- **Depends on:** CIS-0-2, CIS-0-3
- **Learning goal:** Turn setup surprises into revision notes while they're fresh.
- **Description:** Start `docs/notes.md` with an Epic 0 section.
- **Acceptance criteria:**
  - [ ] uv commands mapped to their `dotnet` equivalents
  - [ ] The tracing environment variables and what each does, including the region rule
  - [ ] Model choice, prices and one wrong assumption
  - [ ] Links to every docs page read
- **Docs to read:** —

---

## Epic 1 · Support agent core

### CIS-1-1 · Build get_account and list_transactions on runtime context
- **Epic:** 1 Support agent core · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-1` `build` `core`
- **Depends on:** CIS-0-3
- **Learning goal:** Tools take the caller's identity from injected runtime context, never from arguments the model fills in.
- **Description:** Define a `Context` (customer_id, tier) and one `resolve_customer(runtime)` helper (ADR 0002: context now, authenticated user from Epic 5). Write query helpers in `ciste/db/` and two tools that take `runtime: ToolRuntime[Context]`. `list_transactions` takes an optional date range and merchant filter and returns at most 50 rows.
- **Acceptance criteria:**
  - [ ] Neither tool's argument schema has a customer ID (inspect `tool.args`)
  - [ ] `get_account` returns only the context Customer's Account
  - [ ] `list_transactions` never returns more than 50 rows and honours both filters
  - [ ] Every tool gets the Customer through `resolve_customer`
  - [ ] pytest covers the query helpers
- **Hints:** `from langchain.tools import tool, ToolRuntime`; `runtime.context`.
- **Docs to read:** [Tools](https://docs.langchain.com/oss/python/langchain/tools); [Runtime](https://docs.langchain.com/oss/python/langchain/runtime); [Context overview](https://docs.langchain.com/oss/python/concepts/context). Guide §1.5 "Runtime context vs state".

### CIS-1-2 · Add keyword search_terms over the Fees and Terms
- **Epic:** 1 Support agent core · **Exam section:** Build · **Estimate:** 1h · **Labels:** `owner-tbd` `epic-1` `build` `core`
- **Depends on:** CIS-0-1, CIS-C-1
- **Learning goal:** A tool's docstring and return shape are context engineering. Returning section IDs is what later lets an evaluator check citations.
- **Description:** Split `docs/fees_and_terms.md` by section ID, rank sections by keyword overlap, and return the top two with their IDs.
- **Acceptance criteria:**
  - [ ] "overdraft fee" returns a section whose ID matches `FT-\d+(\.\d+)?`
  - [ ] Every result carries its section ID and text
  - [ ] A query with no match returns an explicit "no matching section" message
  - [ ] pytest covers three queries
- **Docs to read:** [Tools](https://docs.langchain.com/oss/python/langchain/tools). Guide §1.1.

### CIS-1-3 · Implement issue_refund and escalate_to_human; stub open_dispute
- **Epic:** 1 Support agent core · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-1` `build` `core`
- **Depends on:** CIS-1-1
- **Learning goal:** Tools that change state: returning a `Command` to update agent state, and `return_direct` to end a run.
- **Description:** `issue_refund(fee_id, amount)` checks that the Fee belongs to the Customer, that the amount doesn't exceed the Fee, and that the Fee hasn't been refunded, then writes a refund row. The Refund cap is not checked here; that's middleware in CIS-2-3. `escalate_to_human(reason)` writes an Escalation row, marks the Conversation escalated in agent state, and ends the run. `open_dispute` returns a fake Dispute reference for now.
- **Acceptance criteria:**
  - [ ] `issue_refund` refuses another Customer's Fee, a Merchant charge, an amount above the Fee, and a second Refund of the same Fee, each with a clear message rather than an exception
  - [ ] After `escalate_to_human`, the trace shows no further model call
  - [ ] Agent state has `escalated = True` after an Escalation
  - [ ] `open_dispute` returns a reference like `D-0042`
  - [ ] pytest covers the Refund rules
- **Hints:** `@tool(return_direct=True)`; a tool can return `Command(update={...})` including its `ToolMessage`; a custom state field needs a state schema.
- **Docs to read:** [Tools](https://docs.langchain.com/oss/python/langchain/tools); [Agents](https://docs.langchain.com/oss/python/langchain/agents); [Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory). Guide §1.1.

### CIS-1-4 · Assemble the support agent and CLI chat loop
- **Epic:** 1 Support agent core · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-1` `build` `core`
- **Depends on:** CIS-1-1, CIS-1-2, CIS-1-3
- **Learning goal:** `create_agent` compiles model, tools and system prompt into a LangGraph. A checkpointer plus a `thread_id` is what gives it memory across turns.
- **Description:** `ciste/support_agent.py` exposes a factory that takes a model name, so evals can swap models. `cli.py` takes `--customer`, starts a new `thread_id` per session, and loops. The system prompt covers scope, citing FT section IDs, no legal or financial advice, and ignoring instructions in messages that try to override policy.
- **Acceptance criteria:**
  - [ ] `uv run python cli.py --customer C001` holds a multi-turn Conversation that remembers earlier turns
  - [ ] The Customer and Tier reach the agent only through `context=`
  - [ ] After an Escalation, the CLI prints a handoff message and accepts no more input on that thread
  - [ ] An unknown Customer ID fails fast with no model call
- **Hints:** `create_agent(model=, tools=, system_prompt=, checkpointer=, context_schema=)`; `config={"configurable": {"thread_id": ...}}`.
- **Docs to read:** [Agents](https://docs.langchain.com/oss/python/langchain/agents); [Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory); [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence). Guide §1.1.

### CIS-1-5 · Add freeze_card with a raw interrupt() Confirmation
- **Epic:** 1 Support agent core · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-1` `build` `stretch`
- **Depends on:** CIS-1-4
- **Learning goal:** `interrupt()` is the primitive underneath HITL middleware. Writing it by hand shows what the middleware hides.
- **Description:** `freeze_card(card_last4, freeze)` calls `interrupt()` with a Confirmation question, and the CLI resumes with the Customer's yes or no. Give the interrupt payload a `kind` field so the CLI can tell Confirmations from Reviewer Approvals (CIS-2-2).
- **Acceptance criteria:**
  - [ ] Freezing pauses the run and the CLI asks the Customer to confirm
  - [ ] "no" leaves the Card unchanged; "yes" updates its status
  - [ ] The trace shows the interrupt and the resumed run on the same thread
- **Hints:** `from langgraph.types import interrupt, Command`; `Command(resume=...)`.
- **Docs to read:** [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts); [Human-in-the-loop overview](https://docs.langchain.com/oss/python/concepts/human-in-the-loop).

### CIS-1-6 · Prove the tool loop in LangSmith and write up Epic 1
- **Epic:** 1 Support agent core · **Exam section:** Build, Monitor · **Estimate:** 1h · **Labels:** `by-hand` `epic-1` `build` `monitor` `core` `prove-it`
- **Depends on:** CIS-1-4
- **Learning goal:** Reading an agent trace: which tools ran, in what order, with what inputs.
- **Description:** Run one scripted Conversation and study its trace, then write up Epic 1.
- **Acceptance criteria:**
  - [ ] One Conversation looks up the Account, lists last week's transactions, and explains a Fee citing an `FT-` section ID
  - [ ] The trace tree shows each tool call as a child run (link or screenshot in notes)
  - [ ] Notes cover the `create_agent` parameters used, context vs state, and one wrong assumption
- **Docs to read:** [Trace LangGraph agents](https://docs.langchain.com/langsmith/trace-with-langgraph). Guide §1.1, §4.2.

---

## Epic 2 · Middleware

### CIS-2-1 · Prove middleware execution order
- **Epic:** 2 Middleware · **Exam section:** Build · **Estimate:** 1h · **Labels:** `by-hand` `epic-2` `build` `core` `prove-it`
- **Depends on:** CIS-1-4
- **Learning goal:** `before_*` hooks run first to last, `after_*` hooks last to first, and `wrap_*` hooks nest. This is a frequently tested fact.
- **Description:** Lab 1 steps 2–3 on the Ciste agent. Two trivial middlewares, A and B, each log from `@before_model`, `@after_model` and `@wrap_model_call`. Run with `[A, B]`, then `[B, A]`.
- **Acceptance criteria:**
  - [ ] `docs/notes.md` has a table of observed order for both lists and all three hook types
  - [ ] Notes say where middleware spans appear in the LangSmith trace tree
  - [ ] Notes predict where a guard must sit relative to `HumanInTheLoopMiddleware` for its `after_model` to run first (tested in CIS-2-6)
- **Docs to read:** [Middleware overview](https://docs.langchain.com/oss/python/langchain/middleware/overview); [Custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom). Guide §1.2, Lab 1.

### CIS-2-2 · Pause Refunds for Reviewer Approval with HITL
- **Epic:** 2 Middleware · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-2` `build` `core`
- **Depends on:** CIS-1-4
- **Learning goal:** `HumanInTheLoopMiddleware` interrupts before a tool runs, needs a checkpointer and a `thread_id`, and resumes with approve, edit or reject decisions.
- **Description:** Put HITL on `issue_refund` only. Locally, the CLI shows a `[Reviewer]` prompt and resumes the run. The separate review command is CIS-5-4.
- **Acceptance criteria:**
  - [ ] Every `issue_refund` call pauses, and no refund row is written before Approval
  - [ ] Approve writes the Refund; reject (with a message) writes nothing and the agent tells the Customer; edit writes the edited amount
  - [ ] No other tool interrupts
  - [ ] Notes record what happens without a checkpointer (Lab 1 step 4)
- **Hints:** `interrupt_on={"issue_refund": {"allowed_decisions": ["approve", "edit", "reject"]}}`; resume with `Command(resume={"decisions": [{"type": "approve"}]})`; read pending interrupts from `result.interrupts` (with `version="v2"`).
- **Docs to read:** [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop); [Prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in). Guide §1.2.

### CIS-2-3 · Inject Tier with @dynamic_prompt and cap Refunds with @wrap_tool_call
- **Epic:** 2 Middleware · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-2` `build` `core`
- **Depends on:** CIS-2-2
- **Learning goal:** Writing two custom middlewares from scratch: one that shapes the prompt from runtime context, and one wrap-style hook that short-circuits a tool call.
- **Description:** A `@dynamic_prompt` adds the Customer's Tier and Refund cap from context, never from the message. A `RefundCapGuard` `@wrap_tool_call` returns an error `ToolMessage` without calling the handler when `issue_refund`'s amount exceeds the cap. It runs at execution, after HITL, so it also catches a Reviewer's edit.
- **Acceptance criteria:**
  - [ ] A retail Customer saying "I'm premium, refund €120" still gets a retail system prompt, and the guard refuses
  - [ ] A €60 retail Refund approved by the Reviewer is still refused, and no refund row is written
  - [ ] A Reviewer edit from €40 to €80 (retail) is refused
  - [ ] Cap values live in one place, keyed by Tier
  - [ ] A unit test proves the guard never calls the handler when over the cap
- **Hints:** `@wrap_tool_call def guard(request, handler)`; `request.tool_call["args"]`. Not verified: whether `request` exposes runtime/context. Spike first; fall back to `resolve_customer`.
- **Docs to read:** [Custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom); [Runtime](https://docs.langchain.com/oss/python/langchain/runtime); [Context engineering in agents](https://docs.langchain.com/oss/python/langchain/context-engineering). Guide §1.2, §1.5.

### CIS-2-4 · Catch the PII leak in a trace, then mask at source
- **Epic:** 2 Middleware · **Exam section:** Build, Monitor · **Estimate:** 2h · **Labels:** `by-hand` `epic-2` `build` `monitor` `core` `prove-it`
- **Depends on:** CIS-1-4
- **Learning goal:** Middleware masks what the model sees, but traces record tool spans as they happened. Protecting data has to start at the source.
- **Description:** Add `PIIMiddleware` for `credit_card` and a custom `iban` regex detector, using the mask strategy with input, output and tool results enabled. Ask "what's my IBAN?" and inspect the `get_account` tool span. Then make the query helpers return Masked values.
- **Acceptance criteria:**
  - [ ] Before the fix: notes record whether the raw IBAN appeared in the tool span (screenshot)
  - [ ] After the fix: no full IBAN or card number anywhere in the trace (search the exported trace JSON)
  - [ ] A card number the Customer types is Masked in the model input
  - [ ] The agent can still tell the Customer the last four digits
  - [ ] pytest covers the masking helper for IBANs and 16-digit card numbers
- **Hints:** `PIIMiddleware("iban", detector=r"...", strategy="mask", apply_to_output=True, apply_to_tool_results=True)`. `apply_to_output` and `apply_to_tool_results` default to `False`.
- **Docs to read:** [Prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in); [Prevent logging of sensitive data in traces](https://docs.langchain.com/langsmith/mask-inputs-outputs). Guide §1.2.

### CIS-2-5 · Add tool retry, model call limit and summarization
- **Epic:** 2 Middleware · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-2` `build` `core`
- **Depends on:** CIS-2-1
- **Learning goal:** Matching built-in middleware to the problem: a flaky dependency needs retries, a runaway loop needs a call limit, a long chat needs summarization.
- **Description:** Add `ToolRetryMiddleware` limited to database tools, with flakiness simulated by an env var (e.g. `CISTE_FLAKY_DB=0.3` raises `sqlite3.OperationalError`). Add `ModelCallLimitMiddleware(run_limit=...)`. Add `SummarizationMiddleware` on the mini model with a low message trigger so you can watch it fire.
- **Acceptance criteria:**
  - [ ] With flakiness on, the trace shows retries and eventual success, and `search_terms` is never retried
  - [ ] A prompt that makes the agent loop stops at `run_limit` with `exit_behavior="end"`, and notes describe how the stopped run looks
  - [ ] After enough turns, a summary written by the mini model replaces older history (visible in the trace)
  - [ ] Notes justify where retry sits in the middleware list
- **Hints:** `ToolRetryMiddleware(tools=[...], retry_on=(sqlite3.OperationalError,))`; `SummarizationMiddleware(model=..., trigger=("messages", 10))`.
- **Docs to read:** [Prebuilt middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in). Guide §1.2, Lab 1 step 5.

### CIS-2-6 · Stop over-cap Refunds before they reach a Reviewer
- **Epic:** 2 Middleware · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-2` `build` `stretch`
- **Depends on:** CIS-2-1, CIS-2-3
- **Learning goal:** Middleware order in practice: an `after_model` guard only pre-empts HITL if it runs first.
- **Description:** An `after_model` guard spots an over-cap `issue_refund` proposal and replaces it with a message to the model, so HITL never interrupts. Place it where CIS-2-1 predicted.
- **Acceptance criteria:**
  - [ ] An over-cap request never produces an interrupt, and the agent tells the Customer the cap
  - [ ] Swapping the guard's position makes the interrupt reappear
  - [ ] In-cap Refunds still interrupt
- **Hints:** Not verified: how to rewrite or remove a tool call on the last `AIMessage`. Spike first. Docs only show returning new messages with `jump_to`.
- **Docs to read:** [Custom middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom); [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop). Guide §1.2.

### CIS-2-7 · Write up Epic 2 with Lab 1 answers
- **Epic:** 2 Middleware · **Exam section:** Build · **Estimate:** 1h · **Labels:** `by-hand` `epic-2` `build` `core`
- **Depends on:** CIS-2-1 … CIS-2-5
- **Learning goal:** Consolidate middleware facts as exam revision notes.
- **Description:** Epic 2 section in `docs/notes.md`.
- **Acceptance criteria:**
  - [ ] Order table, and a "problem → middleware" matcher in your own words
  - [ ] `PIIMiddleware` defaults and your leak finding
  - [ ] Lab 1 "Check yourself" answered from your own Ciste traces
  - [ ] Links to every docs page read
- **Docs to read:** Guide §1.2 trap boxes.

---

## Epic 3 · Dispute Investigator

### CIS-3-1 · Scaffold the Dispute Investigator with AGENTS.md and DisputeReport
- **Epic:** 3 Dispute Investigator · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-3` `build` `core`
- **Depends on:** CIS-1-1, CIS-C-2
- **Learning goal:** What the Deep Agents harness adds over `create_agent`, `AGENTS.md` as always-loaded memory, and `response_format` for typed output.
- **Description:** `ciste/dispute/investigator.py` uses `create_deep_agent` with a `FilesystemBackend` rooted at `ciste/dispute/` (`virtual_mode=True`), `memory=["/AGENTS.md"]` and `response_format=DisputeReport` (in `ciste/schemas.py`). You write a short `AGENTS.md` from `policy/dispute_policy.md`. Give it one read-only tool for the context Customer's transactions.
- **Acceptance criteria:**
  - [ ] Invoking it on a disputed transaction returns `structured_response` as a `DisputeReport` (amount, merchant, date, reason code, evidence summary, recommendation)
  - [ ] Notes show where `AGENTS.md` content appears in the model input in the trace
  - [ ] `AGENTS.md` is short (about 40 lines max) and contains no secrets
  - [ ] Notes list the built-in tools the deep agent has that the support agent doesn't
- **Docs to read:** [Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview); [Customize Deep Agents](https://docs.langchain.com/oss/python/deepagents/customization); [Memory](https://docs.langchain.com/oss/python/deepagents/memory); [Backends](https://docs.langchain.com/oss/python/deepagents/backends); [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output). Guide §1.3, §1.4, §1.6.

### CIS-3-2 · Add the chargeback-rules skill and prove progressive disclosure
- **Epic:** 3 Dispute Investigator · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-3` `build` `core` `prove-it`
- **Depends on:** CIS-3-1
- **Learning goal:** The three loading levels of a skill (metadata, instructions, resources) and the frontmatter rules.
- **Description:** You write `skills/chargeback-rules/SKILL.md` (with `name` matching the directory and a specific `description`) and `references/reason-codes.md` from `policy/chargeback_reason_codes.md`. Pass `skills=["/skills/"]`.
- **Acceptance criteria:**
  - [ ] For a non-dispute question, the trace has no `read_file` of `SKILL.md`; for a dispute question, it does
  - [ ] The `references/` file is read only when the case needs reason codes (one trace each way)
  - [ ] Notes record what happens when `skills` points directly at `/skills/chargeback-rules/` (Lab 2 step 3)
  - [ ] Frontmatter meets the spec: name is 1–64 lowercase-hyphen characters, description is at most 1,024 characters
- **Docs to read:** [Skills](https://docs.langchain.com/oss/python/deepagents/skills). Guide §1.6, Lab 2.

### CIS-3-3 · Add the transaction-analyst subagent and observe offloading
- **Epic:** 3 Dispute Investigator · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-3` `build` `core` `prove-it`
- **Depends on:** CIS-3-1
- **Learning goal:** Subagents isolate context and don't inherit skills; tool results over about 20,000 tokens are offloaded to the filesystem.
- **Description:** Add a `transaction-analyst` subagent dict with its own tools, including `export_transactions`, which returns the full 3-month history verbosely (over 20,000 tokens). The investigator delegates to it through the `task` tool.
- **Acceptance criteria:**
  - [ ] The trace shows a `task` call to `transaction-analyst` returning one report
  - [ ] The export is offloaded: the message holds a file path and a preview (notes record both)
  - [ ] The subagent can't see `chargeback-rules` unless you give it a `skills` list (show the trace)
  - [ ] The investigator's own context never contains the raw export
- **Hints:** If the export is under 20,000 tokens, make rows more verbose; count with `tiktoken`.
- **Docs to read:** [Subagents](https://docs.langchain.com/oss/python/deepagents/subagents); [Context engineering in Deep Agents](https://docs.langchain.com/oss/python/deepagents/context-engineering). Guide §1.3, §1.5.

### CIS-3-4 · Remember per-customer notes across threads with /memories/
- **Epic:** 3 Dispute Investigator · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-3` `build` `core`
- **Depends on:** CIS-3-1
- **Learning goal:** A filesystem in agent state lasts one thread; durable memory needs a `CompositeBackend` route to a `StoreBackend`.
- **Description:** Wrap the backend in a `CompositeBackend` that routes `/memories/` to a `StoreBackend` namespaced by Customer (from `resolve_customer`). The investigator saves a note after each Dispute.
- **Acceptance criteria:**
  - [ ] A Dispute on thread 1 writes a note; the investigator reads it on thread 2 (same store)
  - [ ] Customer C002 can't see C001's note
  - [ ] Without the route, the note does not survive (recorded in notes)
  - [ ] Notes explain `InMemoryStore` locally vs the Postgres-backed store on the Agent Server
- **Docs to read:** [Backends](https://docs.langchain.com/oss/python/deepagents/backends); [Memory](https://docs.langchain.com/oss/python/deepagents/memory); [Long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory). Guide §1.3, practice Q10.

### CIS-3-5 · Wire open_dispute to the investigator in-process
- **Epic:** 3 Dispute Investigator · **Exam section:** Build · **Estimate:** 2h · **Labels:** `by-hand` `epic-3` `build` `core`
- **Depends on:** CIS-3-1, CIS-1-3
- **Learning goal:** Composing graphs: a tool that invokes a compiled graph and passes runtime context and config through (ADR 0001).
- **Description:** Replace the stub. `open_dispute` invokes the investigator with the transaction, the reason and the same Customer. It saves a Dispute row with status `open` and the report JSON, and returns only the Dispute reference.
- **Acceptance criteria:**
  - [ ] A CLI Dispute Conversation produces a Dispute row holding a valid `DisputeReport`
  - [ ] The Customer's reply contains the Dispute reference and never the recommendation
  - [ ] Investigator runs appear nested under the support agent's trace
  - [ ] The investigator can't read another Customer's transactions
- **Docs to read:** [Runtime](https://docs.langchain.com/oss/python/langchain/runtime); [Trace LangGraph agents](https://docs.langchain.com/langsmith/trace-with-langgraph). Guide §1.1 "Embedding an agent", ADR 0001.

### CIS-3-6 · Run an analysis script in a sandbox backend
- **Epic:** 3 Dispute Investigator · **Exam section:** Build · **Estimate:** 3h · **Labels:** `by-hand` `epic-3` `build` `stretch`
- **Depends on:** CIS-3-3
- **Learning goal:** Sandbox-as-a-tool, the `execute` tool, the never-put-secrets-inside rule, and sandbox lifecycle.
- **Description:** The analyst runs a small script in a sandbox backend to compute merchant frequency for the disputed period.
- **Acceptance criteria:**
  - [ ] The script runs inside the sandbox and its result reaches the report
  - [ ] Printing the environment inside the sandbox shows no API keys
  - [ ] The sandbox is stopped in a `finally` block, and its cost is recorded
- **Docs to read:** [Sandboxes](https://docs.langchain.com/oss/python/deepagents/sandboxes). Guide §1.7.

### CIS-3-7 · Write up Epic 3 with Lab 2 answers
- **Epic:** 3 Dispute Investigator · **Exam section:** Build · **Estimate:** 1h · **Labels:** `by-hand` `epic-3` `build` `core`
- **Depends on:** CIS-3-2 … CIS-3-5
- **Learning goal:** Consolidate Deep Agents facts as exam revision notes.
- **Description:** Epic 3 section in `docs/notes.md`.
- **Acceptance criteria:**
  - [ ] A `create_agent` vs `create_deep_agent` table drawn from your own code
  - [ ] The five context types (Guide §1.5) mapped to concrete Ciste examples
  - [ ] Offloading and memory behaviour as observed
  - [ ] Lab 2 "Check yourself" answered from your own traces
- **Docs to read:** Guide §1.3–1.7 trap boxes.

---

## Epic 4 · Offline evaluation

### CIS-4-1 · Build the eval dataset and a target that handles interrupts
- **Epic:** 4 Offline evaluation · **Exam section:** Test · **Estimate:** 2h · **Labels:** `by-hand` `epic-4` `test` `core`
- **Depends on:** CIS-2-3, CIS-3-5
- **Learning goal:** What a dataset example is (inputs, reference outputs, metadata), and how to turn an agent that pauses into something you can score.
- **Description:** `evals/dataset_seed.py` creates `ciste-support-v1` with 25–30 examples. Metadata holds `category` (fee_question, refund_ok, refund_over_limit, dispute, injection, escalation), `customer_id` and `tier`. The target runs each example on a fresh thread. If HITL interrupts, it returns the proposed refund arguments as `pending_refund` instead of approving. The target's output holds final text, tool calls, `pending_refund` and `escalated`.
- **Acceptance criteria:**
  - [ ] Dataset exists in LangSmith with at least 4 examples per category; re-running the script doesn't duplicate it
  - [ ] Fee examples' reference outputs include the expected section ID; Refund examples include the expected outcome
  - [ ] The target returns its output dict for every category without hanging on an interrupt
  - [ ] Two more examples added by hand in the UI (Lab 3 step 1)
- **Hints:** `Client.has_dataset`, `create_dataset`, `create_examples`.
- **Docs to read:** [Manage datasets](https://docs.langchain.com/langsmith/manage-datasets); [How to evaluate agents](https://docs.langchain.com/langsmith/evaluate-llm-application); [Evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts). Guide §2.1, §2.5.

### CIS-4-2 · Write the code evaluators
- **Epic:** 4 Offline evaluation · **Exam section:** Test · **Estimate:** 2h · **Labels:** `by-hand` `epic-4` `test` `core`
- **Depends on:** CIS-4-1
- **Learning goal:** Anything checkable by rules belongs in a code evaluator: cheap, deterministic, repeatable.
- **Description:** `evals/evaluators.py`: `refund_within_cap` (uses the example's Tier), `no_unmasked_pii`, `escalated_when_asked`, `cites_valid_section` (ID exists in the Fees and Terms), `dispute_recommendation_not_leaked`.
- **Acceptance criteria:**
  - [ ] Each evaluator has a pytest with one passing and one failing fake output
  - [ ] Evaluators that don't apply to an example's category skip it rather than scoring it
  - [ ] Return values follow the SDK conventions (bool, number or `{"key", "score"}` dict)
- **Docs to read:** [How to define a code evaluator (SDK)](https://docs.langchain.com/langsmith/code-evaluator-sdk). Guide §2.3.

### CIS-4-3 · Write LLM-as-judge evaluators on the mini model
- **Epic:** 4 Offline evaluation · **Exam section:** Test · **Estimate:** 2h · **Labels:** `by-hand` `epic-4` `test` `core`
- **Depends on:** CIS-4-1
- **Learning goal:** LLM judges cover what rules can't, such as tone and semantic correctness, and need structured scores and visible reasoning.
- **Description:** A reference-free `helpfulness_tone` judge and a `correctness` judge against reference outputs, both on the mini model, returning a score plus a comment.
- **Acceptance criteria:**
  - [ ] Judge prompts live in the repo
  - [ ] Each judge returns a score and a reasoning comment
  - [ ] Hand-checked on 3 examples; notes record agreement
  - [ ] Estimated judge cost per experiment recorded
- **Docs to read:** [How to define an LLM-as-a-judge evaluator (SDK)](https://docs.langchain.com/langsmith/llm-as-judge-sdk); [Evaluation types](https://docs.langchain.com/langsmith/evaluation-types). Guide §2.3.

### CIS-4-4 · Run baseline vs changed-prompt experiments and compare
- **Epic:** 4 Offline evaluation · **Exam section:** Test · **Estimate:** 2h · **Labels:** `by-hand` `epic-4` `test` `core` `prove-it`
- **Depends on:** CIS-4-2, CIS-4-3
- **Learning goal:** Telling signal from noise: repetitions, a baseline, and per-example inspection.
- **Description:** `evals/run_experiment.py` calls `evaluate(...)` with `experiment_prefix`, `num_repetitions=3` and `max_concurrency=2`. Run a baseline, change one thing in the system prompt, run again, and compare. Rough cost: $2–5.
- **Acceptance criteria:**
  - [ ] Two experiments, each with 3 repetitions, visible on the dataset
  - [ ] In the comparison view with the baseline set, notes list regressed (red) and improved (green) examples
  - [ ] One sentence: did the mean move by more than the spread between repetitions, so signal or noise?
  - [ ] Actual cost of both runs recorded
- **Docs to read:** [Experiment configuration](https://docs.langchain.com/langsmith/experiment-configuration); [How to evaluate with repetitions](https://docs.langchain.com/langsmith/repetition); [How to compare experiment results](https://docs.langchain.com/langsmith/compare-experiment-results). Guide §2.4, Lab 3.

### CIS-4-5 · Align the correctness judge with 15+ human labels
- **Epic:** 4 Offline evaluation · **Exam section:** Test · **Estimate:** 2h · **Labels:** `by-hand` `epic-4` `test` `core` `prove-it`
- **Depends on:** CIS-4-4
- **Learning goal:** A judge can be consistently wrong; the alignment score measures agreement with humans.
- **Description:** Send experiment runs to an annotation queue, label at least 15 yourself, record the alignment score, improve the judge prompt or add few-shot corrections, and measure again.
- **Acceptance criteria:**
  - [ ] At least 15 labelled runs in an annotation queue
  - [ ] Alignment score before and after recorded in notes
  - [ ] Labelled examples saved to a reference dataset
  - [ ] Notes explain reliability vs accuracy using your own numbers
- **Docs to read:** [Use annotation queues](https://docs.langchain.com/langsmith/annotation-queues); [Improve LLM-as-judge evaluators using human feedback](https://docs.langchain.com/langsmith/improve-judge-evaluator-feedback); [How to improve your evaluator with few-shot examples](https://docs.langchain.com/langsmith/create-few-shot-evaluators). Guide §2.6, Lab 4.

### CIS-4-6 · Run evaluators in pytest with LANGSMITH_TEST_CACHE
- **Epic:** 4 Offline evaluation · **Exam section:** Test · **Estimate:** 2h · **Labels:** `by-hand` `epic-4` `test` `stretch`
- **Depends on:** CIS-4-2
- **Learning goal:** LangSmith unit tests in CI, and caching to stop paying for identical calls.
- **Description:** Five representative cases as LangSmith-integrated pytest tests, with caching on.
- **Acceptance criteria:**
  - [ ] Tests appear in LangSmith as an experiment
  - [ ] The second run is served from cache (no new OpenAI usage)
  - [ ] Optional: a GitHub Actions workflow runs them, with the key as a repository secret
- **Docs to read:** [How to run evaluations with pytest](https://docs.langchain.com/langsmith/pytest). Guide §2.4.

### CIS-4-7 · Write up Epic 4 with Lab 3–4 answers
- **Epic:** 4 Offline evaluation · **Exam section:** Test · **Estimate:** 1h · **Labels:** `by-hand` `epic-4` `test` `core`
- **Depends on:** CIS-4-4, CIS-4-5
- **Learning goal:** Consolidate evaluation facts as exam revision notes.
- **Description:** Epic 4 section in `docs/notes.md`.
- **Acceptance criteria:**
  - [ ] Results table, the signal-or-noise verdict, and alignment scores before and after
  - [ ] Offline vs online evaluation in your own words
  - [ ] Lab 3 and Lab 4 "Check yourself" answered from your own experiments
- **Docs to read:** Guide §2 trap boxes.

---

## Epic 5 · Local server and auth

### CIS-5-1 · Register both graphs in langgraph.json and run langgraph dev
- **Epic:** 5 Local server and auth · **Exam section:** Deploy · **Estimate:** 2h · **Labels:** `by-hand` `epic-5` `deploy` `core`
- **Depends on:** CIS-3-5
- **Learning goal:** What a graph is to the Agent Server, and that the server, not your code, provides the checkpointer and store.
- **Description:** `langgraph.json` registers `support_agent` and `dispute_investigator` with `dependencies` and `env`. Graph modules export compiled graphs without their own checkpointer. Inspect thread state and resume a Refund interrupt in Studio.
- **Acceptance criteria:**
  - [ ] `uv run langgraph dev` starts, and both graphs appear in Studio
  - [ ] A Conversation runs in Studio; its state (messages, `escalated`) is inspected; a Refund interrupt is resumed there
  - [ ] Notes explain why the local `InMemorySaver` was removed for the server
- **Docs to read:** [Run a local server](https://docs.langchain.com/oss/python/langgraph/local-server); [Application structure](https://docs.langchain.com/langsmith/application-structure); [Studio](https://docs.langchain.com/oss/python/langgraph/studio); [Agent Server](https://docs.langchain.com/langsmith/agent-server-overview). Guide §3.1–3.2.

### CIS-5-2 · Create retail and premium assistants and drive runs with the SDK
- **Epic:** 5 Local server and auth · **Exam section:** Deploy · **Estimate:** 2h · **Labels:** `by-hand` `epic-5` `deploy` `core`
- **Depends on:** CIS-5-1
- **Learning goal:** An assistant is a graph plus configuration; runs are stateless or stateful; a graph can be called by graph ID or by assistant ID.
- **Description:** `scripts/sdk_demo.py` creates `retail` and `premium` assistants that differ in persona prompt and a `refund_cap` ceiling. The effective cap is the lower of the Tier cap and the assistant cap. The script then runs once statelessly, once on a new thread, once by graph ID and once by assistant ID.
- **Acceptance criteria:**
  - [ ] All four run styles succeed and are visible in Studio or LangSmith
  - [ ] The stateless run leaves no thread behind
  - [ ] The premium assistant answers in its persona
  - [ ] A retail Customer calling the premium assistant is still capped at €50
- **Hints:** `get_client(url=...)`; `client.assistants.create`, `client.threads.create`, `client.runs.wait` / `stream`. Not verified: how assistant configuration reaches the graph in the current version. Check the Assistants page first.
- **Docs to read:** [Assistants](https://docs.langchain.com/langsmith/assistants); [Use threads](https://docs.langchain.com/langsmith/use-threads); [Runs](https://docs.langchain.com/langsmith/runs); [Stateless runs](https://docs.langchain.com/langsmith/stateless-runs). Guide §3.2.

### CIS-5-3 · Add custom auth and prove Customer isolation
- **Epic:** 5 Local server and auth · **Exam section:** Deploy · **Estimate:** 3h · **Labels:** `by-hand` `epic-5` `deploy` `core` `prove-it`
- **Depends on:** CIS-5-2
- **Learning goal:** Authentication answers who is calling; authorization answers what they may see. The store is shared until you scope it.
- **Description:** `auth.py`: `@auth.authenticate` maps fake bearer tokens to an identity (Customer ID), Tier and role. `@auth.on.threads.create` stamps `owner`, resource handlers filter reads, and `@auth.on.store` prefixes namespaces with the identity. `resolve_customer` now prefers `langgraph_auth_user` (ADR 0002). Register the auth path in `langgraph.json`.
- **Acceptance criteria:**
  - [ ] Customer A's token lists only A's threads; reading B's thread by ID is refused (record the status code)
  - [ ] A run with A's token but `context={"customer_id": "<B>", ...}` acts as A (shown in the trace)
  - [ ] A missing or invalid token gets 401
  - [ ] `/memories/` notes from A are invisible to B
  - [ ] Notes say which handler fired for each action (specificity rule)
- **Hints:** Not verified: how a tool reads `langgraph_auth_user` (docs show `config["configurable"]` in a node), and whether `langgraph dev` enforces custom auth. Spike both first.
- **Docs to read:** [Authentication & access control](https://docs.langchain.com/langsmith/auth); [Add custom authentication](https://docs.langchain.com/langsmith/custom-auth); [Make conversations private](https://docs.langchain.com/langsmith/resource-auth); [Isolate store data per user](https://docs.langchain.com/langsmith/store-auth). Guide §3.6, ADR 0002.

### CIS-5-4 · Approve Refunds from a cli.py review command
- **Epic:** 5 Local server and auth · **Exam section:** Deploy · **Estimate:** 2h · **Labels:** `by-hand` `epic-5` `deploy` `stretch`
- **Depends on:** CIS-5-3, CIS-2-2
- **Learning goal:** An interrupted thread can be resumed from any client; the Reviewer is a different actor with a different role.
- **Description:** `cli.py review` uses a Reviewer token to list interrupted threads, show each proposed Refund, and resume with approve, edit or reject.
- **Acceptance criteria:**
  - [ ] A Customer session shows "awaiting approval"; the Reviewer approves from another terminal; the Customer sees the outcome
  - [ ] A Customer token can't list other Customers' interrupted threads
- **Docs to read:** [Human-in-the-loop using server API](https://docs.langchain.com/langsmith/add-human-in-the-loop); [Use threads](https://docs.langchain.com/langsmith/use-threads).

### CIS-5-5 · Serve a web chat page from a custom route
- **Epic:** 5 Local server and auth · **Exam section:** Deploy · **Estimate:** 3h · **Labels:** `owner-tbd` `epic-5` `deploy` `stretch`
- **Depends on:** CIS-5-3
- **Learning goal:** Extending the Agent Server with your own HTTP app while keeping every secret server-side.
- **Description:** A small Starlette or FastAPI app (`http.app` in `langgraph.json`) serves one plain HTML and JavaScript page. The page chats through the Agent Server API with a Customer's bearer token, streams replies, and shows "awaiting approval" and Confirmation prompts.
- **Acceptance criteria:**
  - [ ] `langgraph dev` serves the page, and chat works for two different Customer tokens
  - [ ] No OpenAI or LangSmith key reaches the browser (check page source and the network tab)
- **Hints:** Not verified: whether custom routes are covered by custom auth.
- **Docs to read:** [How to add custom routes](https://docs.langchain.com/langsmith/custom-routes); [Use threads](https://docs.langchain.com/langsmith/use-threads).

### CIS-5-6 · Call the investigator through RemoteGraph
- **Epic:** 5 Local server and auth · **Exam section:** Deploy · **Estimate:** 2h · **Labels:** `owner-tbd` `epic-5` `deploy` `stretch`
- **Depends on:** CIS-5-1
- **Learning goal:** The trade-off ADR 0001 rejected, made visible.
- **Description:** An env var switches `open_dispute` between in-process and `RemoteGraph`.
- **Acceptance criteria:**
  - [ ] Both modes produce a valid `DisputeReport`
  - [ ] Notes compare the two trace shapes and what auth had to be forwarded
  - [ ] ADR 0001 gains a Consequences note
- **Docs to read:** [How to interact with a deployment using RemoteGraph](https://docs.langchain.com/langsmith/use-remote-graph).

### CIS-5-7 · Write up Epic 5
- **Epic:** 5 Local server and auth · **Exam section:** Deploy · **Estimate:** 1h · **Labels:** `by-hand` `epic-5` `deploy` `core`
- **Depends on:** CIS-5-3
- **Learning goal:** Map the six Deploy nouns onto real Ciste objects.
- **Description:** Epic 5 section in `docs/notes.md`.
- **Acceptance criteria:**
  - [ ] Graph, deployment, revision, assistant, thread and run each mapped to a Ciste example
  - [ ] Authn vs authz and handler specificity in your own words
  - [ ] The local parts of Lab 5 "Check yourself" answered
- **Docs to read:** Guide §3.2, §3.6–3.7.

---

## Epic 6 · Cloud deployment

### CIS-6-1 · Deploy to LangSmith Cloud with the model key as a secret
- **Epic:** 6 Cloud deployment · **Exam section:** Deploy · **Estimate:** 2h · **Labels:** `by-hand` `epic-6` `deploy` `stretch` `plus`
- **Depends on:** CIS-5-3
- **Learning goal:** Control plane vs data plane, secrets vs plain env vars, and the Development deployment type.
- **Description:** Create a Development deployment from the GitHub repo, entering `OPENAI_API_KEY` as a secret.
- **Acceptance criteria:**
  - [ ] Deployment is live, and a tracing project named after it exists
  - [ ] The OpenAI key is stored as a secret, not a plain variable
  - [ ] Notes record the org's region and the deployment's region
- **Docs to read:** [Deploy to Cloud](https://docs.langchain.com/langsmith/deploy-to-cloud-overview); [Create a deployment](https://docs.langchain.com/langsmith/deploy-to-cloud); [Cloud Agent Server environment variables](https://docs.langchain.com/langsmith/env-var-cloud); [Cloud platform features](https://docs.langchain.com/langsmith/cloud-platform-features). Guide §3.1, §3.5.

### CIS-6-2 · Re-create assistants and prove isolation in the cloud
- **Epic:** 6 Cloud deployment · **Exam section:** Deploy · **Estimate:** 1h · **Labels:** `by-hand` `epic-6` `deploy` `stretch` `plus` `prove-it`
- **Depends on:** CIS-6-1
- **Learning goal:** The same SDK and auth behaviour, local and cloud.
- **Description:** Point `sdk_demo.py` and the auth checks at the cloud URL.
- **Acceptance criteria:**
  - [ ] Both assistants exist and behave differently
  - [ ] Customer A can't read Customer B's threads on the cloud deployment
- **Docs to read:** [Assistants](https://docs.langchain.com/langsmith/assistants); [Make conversations private](https://docs.langchain.com/langsmith/resource-auth).

### CIS-6-3 · Rotate the model secret through a new revision
- **Epic:** 6 Cloud deployment · **Exam section:** Deploy · **Estimate:** 1h · **Labels:** `by-hand` `epic-6` `deploy` `stretch` `plus` `prove-it`
- **Depends on:** CIS-6-1
- **Learning goal:** Code changes and secret changes both take effect only through a new revision.
- **Description:** Create a new OpenAI key, update it through **+ New Revision**, and revoke the old one.
- **Acceptance criteria:**
  - [ ] The Revisions table shows the new revision (screenshot)
  - [ ] Runs succeed after the old key is revoked
- **Docs to read:** [Revisions](https://docs.langchain.com/langsmith/deployment-revisions). Guide §3.5.

### CIS-6-4 · Write up storage durability, regions and Epic 6
- **Epic:** 6 Cloud deployment · **Exam section:** Deploy · **Estimate:** 1h · **Labels:** `by-hand` `epic-6` `deploy` `core`
- **Depends on:** CIS-5-7
- **Learning goal:** What survives what: Postgres is durable, Redis isn't, and data stays in its region.
- **Description:** Epic 6 section in `docs/notes.md`. Without Plus, answer from the docs and guide instead of a live deployment.
- **Acceptance criteria:**
  - [ ] A table placing Ciste's threads, checkpoints, `/memories/` store, runs and secrets in Postgres, Redis or the secrets store
  - [ ] Region rules and the "deployment type can't change" fact
  - [ ] Lab 5 cloud "Check yourself" answered (live or from the docs)
- **Docs to read:** [Agent Server](https://docs.langchain.com/langsmith/agent-server-overview); [Cloud platform features](https://docs.langchain.com/langsmith/cloud-platform-features). The data plane page title couldn't be verified; use Guide §3.3–3.5.

---

## Epic 7 · Monitoring

### CIS-7-1 · Put thread metadata on every run and verify thread cost
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 2h · **Labels:** `by-hand` `epic-7` `monitor` `core` `prove-it`
- **Depends on:** CIS-3-5
- **Learning goal:** Child runs without thread metadata drop out of thread cost totals, the classic "thread cost looks too low" problem.
- **Description:** Make sure every run, including nested investigator, subagent and summarization runs, carries `thread_id`, plus `tier` and `environment` metadata.
- **Acceptance criteria:**
  - [ ] The Threads tab lists Ciste Conversations with turns, tokens and cost
  - [ ] A Dispute thread's total includes the investigator's runs (compare the sum of trace costs to the thread total)
  - [ ] Dropping the metadata on the nested call once shows the drop (Lab 6 step 2), recorded in notes
  - [ ] Traces can be filtered by Tier
- **Docs to read:** [Configure threads](https://docs.langchain.com/langsmith/threads); [Add metadata and tags to traces](https://docs.langchain.com/langsmith/add-metadata-tags); [Cost tracking](https://docs.langchain.com/langsmith/cost-tracking); [Trace LangGraph agents](https://docs.langchain.com/langsmith/trace-with-langgraph). Guide §4.3–4.4, Lab 6.

### CIS-7-2 · Log thumbs-up/down feedback from the CLI
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 1h · **Labels:** `by-hand` `epic-7` `monitor` `core`
- **Depends on:** CIS-1-4
- **Learning goal:** End-user sentiment becomes feedback attached to a run.
- **Description:** `/good` and `/bad` in the CLI attach a `user_score` feedback to the last run.
- **Acceptance criteria:**
  - [ ] Feedback appears on the run, in the Threads tab and on the dashboard
  - [ ] The feedback key name is recorded for alerts (CIS-7-6)
- **Hints:** Pre-generate the run ID and pass it in the invoke config (`run_id`); `Client.create_feedback(run_id=..., key=..., score=..., trace_id=...)`.
- **Docs to read:** [Log user feedback using the SDK](https://docs.langchain.com/langsmith/attach-user-feedback). Guide §4.4.

### CIS-7-3 · Generate about 50 simulated conversations
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 2h · **Labels:** `owner-tbd` `epic-7` `monitor` `core`
- **Depends on:** CIS-7-1, CIS-7-2
- **Learning goal:** Monitoring features need realistic traffic, including bad actors and unhappy Customers.
- **Description:** `scripts/simulate_traffic.py`: the mini model plays Customer personas (routine, angry, injection attempt, wants a human, Dispute) for 3–6 turns. It leaves persona-driven thumbs feedback and makes automatic Reviewer decisions. Rough cost: $1–3.
- **Acceptance criteria:**
  - [ ] At least 50 threads with `persona` metadata, including at least 5 injection and 5 angry
  - [ ] Re-running with the same seed reproduces the persona mix
  - [ ] Actual cost recorded
- **Docs to read:** Use threads (if run against the server); [Log user feedback using the SDK](https://docs.langchain.com/langsmith/attach-user-feedback). Guide Lab 7 setup.

### CIS-7-4 · Add online groundedness and thread-level satisfaction evaluators
- **Epic:** 7 Monitoring · **Exam section:** Monitor, Test · **Estimate:** 2h · **Labels:** `by-hand` `epic-7` `monitor` `test` `core`
- **Depends on:** CIS-7-3
- **Learning goal:** Online evaluators are reference-free, sampled and filtered; multi-turn evaluators run once per idle thread.
- **Description:** On the tracing project, add an LLM-as-judge groundedness evaluator (mini model, sampling 0.3, filtered by run type) and a multi-turn satisfaction evaluator.
- **Acceptance criteria:**
  - [ ] Roughly 30% of new matching runs get a groundedness score
  - [ ] Completed threads get a satisfaction score after the idle time (note the setting)
  - [ ] A weekly evaluator spend cap is set
- **Docs to read:** [Set up LLM-as-a-judge online evaluators](https://docs.langchain.com/langsmith/online-evaluations-llm-as-judge); [Set up multi-turn online evaluators](https://docs.langchain.com/langsmith/online-evaluations-multi-turn). Guide §2.7, §4.5, Lab 7.

### CIS-7-5 · Route thumbs-down threads to an annotation queue
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 1h · **Labels:** `by-hand` `epic-7` `monitor` `core`
- **Depends on:** CIS-7-2
- **Learning goal:** Automation rules: item type, filter, sampling rate, action.
- **Description:** A thread rule filtered on negative feedback, with the action "send to annotation queue".
- **Acceptance criteria:**
  - [ ] A new thumbs-down thread lands in the queue
  - [ ] One queued thread is added to `ciste-support-v1`
- **Docs to read:** [Set up automation rules](https://docs.langchain.com/langsmith/rules); [Use annotation queues](https://docs.langchain.com/langsmith/annotation-queues). Guide §4.6.

### CIS-7-6 · Configure alerts and inspect a webhook payload
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 2h · **Labels:** `by-hand` `epic-7` `monitor` `core` `prove-it`
- **Depends on:** CIS-7-4
- **Learning goal:** Alerts need a metric, aggregation, threshold and window; quality alerts need a feedback key first.
- **Description:** Set up three alerts: error rate (percentage, ≥ 5, 5 minutes, LLM runs only), cost, and feedback score on the satisfaction key. Route one to a webhook (a request-bin URL is fine) and trigger it with `CISTE_FLAKY_DB`.
- **Acceptance criteria:**
  - [ ] All three alerts configured; the preview shows how often each would have fired
  - [ ] One alert fires, and its webhook payload is saved in notes with its `alert_rule_attribute`
- **Hints:** Not verified: whether alerts are available on the free plan.
- **Docs to read:** [Alerts in LangSmith](https://docs.langchain.com/langsmith/alerts); [Monitor projects with dashboards](https://docs.langchain.com/langsmith/dashboards). Guide §4.7, Lab 8.

### CIS-7-7 · Run an Insights report over the simulated traffic
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 1h · **Labels:** `by-hand` `epic-7` `monitor` `stretch` `plus`
- **Depends on:** CIS-7-3
- **Learning goal:** Insights discovers unknown patterns; evaluators test known ones.
- **Description:** An Insights report over the simulated threads, with a `user_satisfied` boolean attribute.
- **Acceptance criteria:**
  - [ ] Top categories and one failure mode recorded in notes
  - [ ] The two models Insights uses and their roles noted, plus cost
- **Docs to read:** [Discover errors and usage patterns with Insights](https://docs.langchain.com/langsmith/insights). Guide §4.5.

### CIS-7-8 · Log feedback from the web page through POST /feedback
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 1h · **Labels:** `owner-tbd` `epic-7` `monitor` `stretch`
- **Depends on:** CIS-5-5, CIS-7-2
- **Learning goal:** Collecting feedback in a browser without exposing an API key.
- **Description:** Thumbs buttons on the web page post to a server-side `/feedback` route that calls LangSmith.
- **Acceptance criteria:**
  - [ ] Browser feedback appears on the right run
  - [ ] Notes compare this with presigned feedback URLs
- **Docs to read:** [Log user feedback using the SDK](https://docs.langchain.com/langsmith/attach-user-feedback); [How to add custom routes](https://docs.langchain.com/langsmith/custom-routes).

### CIS-7-9 · Scale simulated traffic to 200+ conversations
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 1h · **Labels:** `owner-tbd` `epic-7` `monitor` `stretch`
- **Depends on:** CIS-7-3
- **Learning goal:** How metrics, Insights and alerts behave at volume.
- **Description:** Run the simulator for 200+ conversations. Rough cost: $5–10; check the remaining budget first.
- **Acceptance criteria:**
  - [ ] 200+ threads exist; dashboards and online evaluator scores updated
  - [ ] Actual cost recorded
- **Docs to read:** [Monitor projects with dashboards](https://docs.langchain.com/langsmith/dashboards).

### CIS-7-10 · Write up Epic 7 with Lab 6–8 answers
- **Epic:** 7 Monitoring · **Exam section:** Monitor · **Estimate:** 1h · **Labels:** `by-hand` `epic-7` `monitor` `core`
- **Depends on:** CIS-7-1 … CIS-7-6
- **Learning goal:** Consolidate Monitor facts as exam revision notes.
- **Description:** Epic 7 section in `docs/notes.md`.
- **Acceptance criteria:**
  - [ ] A dashboard screenshot, the fired alert payload, and Insights findings (if Plus)
  - [ ] Online Evals vs Insights vs Automations in your own words
  - [ ] Lab 6, 7 and 8 "Check yourself" answered from your own project
- **Docs to read:** Guide §4 trap boxes.

---

## Epic 8 · Close the loop

### CIS-8-1 · Turn a production failure into dataset examples and an evaluator
- **Epic:** 8 Close the loop · **Exam section:** Test, Monitor · **Estimate:** 2h · **Labels:** `by-hand` `epic-8` `test` `monitor` `core`
- **Depends on:** CIS-7-5, CIS-4-4
- **Learning goal:** Failing production traces become regression tests.
- **Description:** Take the failure mode from Insights (with Plus) or from the annotation queue and low online scores (without). Add the affected threads to the dataset and add or adjust an evaluator that catches it.
- **Acceptance criteria:**
  - [ ] At least 3 failing threads added to `ciste-support-v1`
  - [ ] The new or adjusted evaluator fails them on the current baseline
- **Docs to read:** [Manage datasets](https://docs.langchain.com/langsmith/manage-datasets); [Use annotation queues](https://docs.langchain.com/langsmith/annotation-queues). Guide §2.5, §4.7 playbook.

### CIS-8-2 · Fix the failure and confirm it offline and online
- **Epic:** 8 Close the loop · **Exam section:** Build, Test, Deploy, Monitor · **Estimate:** 2h · **Labels:** `by-hand` `epic-8` `build` `test` `deploy` `monitor` `core` `prove-it`
- **Depends on:** CIS-8-1
- **Learning goal:** The full lifecycle loop: Build → Test → Deploy → Monitor → Build.
- **Description:** Fix the failure in the prompt or middleware, rerun the experiment against the baseline, redeploy (a new revision with Plus, a `langgraph dev` restart without), and run fresh simulated traffic. Rough cost: $2–5.
- **Acceptance criteria:**
  - [ ] The experiment comparison (with repetitions) shows improvement on the new examples without regressions elsewhere
  - [ ] Online evaluator scores on fresh traffic improve; numbers recorded
  - [ ] With Plus, a new revision is visible
- **Docs to read:** [How to compare experiment results](https://docs.langchain.com/langsmith/compare-experiment-results); [Revisions](https://docs.langchain.com/langsmith/deployment-revisions).

### CIS-8-3 · Write the README and the Epic 8 write-up
- **Epic:** 8 Close the loop · **Exam section:** Build, Test, Deploy, Monitor · **Estimate:** 2h · **Labels:** `by-hand` `epic-8` `build` `test` `deploy` `monitor` `core`
- **Depends on:** CIS-8-2
- **Learning goal:** Explain the project as a portfolio piece and as a revision map.
- **Description:** `README.md` and the final `docs/notes.md` section.
- **Acceptance criteria:**
  - [ ] README covers the problem, an architecture diagram, how each exam section is demonstrated (with links to traces or screenshots), and a results table
  - [ ] The README tells the full Build → Test → Deploy → Monitor → Build story with evidence
  - [ ] No secrets, real data or study guide content in the repo
- **Docs to read:** —
