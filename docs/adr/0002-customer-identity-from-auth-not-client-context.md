# Customer identity comes from the authenticated user, never from client-supplied context

On the Agent Server, the client chooses the `context=` it sends with a run. A caller holding one Customer's token could therefore claim another Customer's ID or a higher Tier. All tools and middleware resolve the Customer through one helper. It prefers `langgraph_auth_user` (set by `@auth.authenticate`, which the client can't forge) and ignores client context whenever an authenticated user is present. It falls back to runtime context only when there is no auth layer (local CLI, offline evals). This keeps tools runnable without a server while ensuring the Refund cap and data access can't be escalated through the request body.

## Considered Options

- **An `@auth.on` run-create handler that rewrites the run's context**: tools would keep reading `runtime.context` unchanged, but we couldn't confirm the run-create payload exposes context for rewriting.
- **Trust client context**: simplest, but it lets any authenticated Customer read other Accounts and raise their own Refund cap.
