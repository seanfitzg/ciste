# Dispute Investigator is invoked in-process, not over the Agent Server API

`open_dispute` invokes the compiled `dispute_investigator` graph directly inside the support agent's process. The Customer waits for the result in the same turn. We chose this over calling the deployed graph through `RemoteGraph`/the SDK because it keeps one trace tree per conversation, so `thread_id` and cost roll up to the thread (needed for Epic 7). It also lets the investigator share the same store for `/memories/` under the same per-customer auth scoping. The investigator is still registered as its own graph in `langgraph.json` so it can be run and evaluated standalone.

## Considered Options

- **Remote call via `RemoteGraph`/SDK**: closer to a microservice boundary and better Deploy practice, but it splits traces across runs and needs the caller's auth forwarded explicitly. Kept as a stretch ticket to demonstrate the trade-off.
- **Fold the investigator into the support agent as a subagent**: simplest, but loses the `create_agent` vs `create_deep_agent` contrast the exam tests.
