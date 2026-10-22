# Day 17: ReAct (Reasoning + Acting)

## Overview

**ReAct** = **Rea**soning + **Act**ing. It is an agent pattern where the LLM alternates between *thinking* and *using tools*, and feeds each tool result back into its context so the next thought is grounded in reality.

Paper: *ReAct: Synergizing Reasoning and Acting in Language Models* — Yao et al., 2022 ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629))

Reference: [ReAct Agent Pattern Explained](https://manalisomani099.medium.com/react-agent-pattern-explained-ai-reasoning-action-c8602122a833)

---

## The Core Idea

The heart of any agent is **how it thinks, acts, and reacts**. ReAct turns that into an explicit, repeating loop:

1. **Think** — reason about what to do next
2. **Act** — call a tool with structured arguments
3. **Observe** — read the tool's result
4. **Think again** — use that result to decide the next step

```
Reason → Act → Observe → Reason → Act → Observe → ... → Final Answer
```

This loop continues until the query is resolved or a stopping condition is hit.

- **Reasoning** without acting = hallucinated answers (Chain-of-Thought alone).
- **Acting** without reasoning = blind trial and error.
- **ReAct** = reasoning grounded in real observations.

---

## Flow Engineering

*Flow engineering* is designing how the model moves between **thinking** and **doing** — where the loop starts, how many turns it may take, what stops it, and what it sees at each step.

After each step, the system must:

- **Verify progress** — is the user's query solved, or is the agent drifting in circles?
- **Enforce limits** — stop after a maximum number of steps/tool calls.

Two crucial concerns:

- **Preventing infinite loops** — a model can repeat the same failing action forever.
- **Controlling latency and cost** — every iteration is another LLM call plus tool execution, so tokens and wall-clock time grow with each turn.

### Guardrails worth adding

| Guardrail | Why |
|---|---|
| Max iterations (e.g. 5–10) | Hard stop against infinite loops |
| Per-step timeout | One slow tool must not hang the agent |
| Repeat-action detection | Same tool + same args = break the loop |
| Token/context budget | History grows every turn; stop before overflow |
| Explicit `finish` action | Lets the model end cleanly instead of guessing |
| Tool error handling | Return the error *as an observation* so the model can adapt |

---

## Who Executes What

**The LLM does not execute anything — the system does.**

```
User Query
    ↓
LLM (reason: "I need the current price of gold")
    ↓
Structured Action → get_price(asset="gold")
    ↓
YOUR APPLICATION executes the real function
    ↓
Observation → {"price": 2412.30, "currency": "USD"}
    ↓
LLM (reasons over observation → next action or final answer)
```

The model's only job is to emit **thoughts** and **structured action requests**. Execution, permissions, retries, and logging belong to your code. This separation is what makes agents safe and debuggable.

---

## Updating Context After Every Action

After each action, append the result to the conversation history and call the LLM again. The agent "learns" what happened from its own transcript and chooses the next step from there.

```
history = [system_prompt, user_query]

while not done and steps < MAX_STEPS:
    thought, action = llm(history)              # Reason
    observation     = execute(action)            # Act + Observe
    history.append(thought, action, observation) # Update context
    done = action.type == "finish"
```

Practical implications:

- **History is the agent's memory** — if a result is not in the history, the model cannot use it.
- **Truncate or summarise old steps** in long runs, or the context grows without bound.
- **Keep observations compact** — return the 3 fields that matter, not a 40 KB JSON blob.

---

## ReAct vs Chain-of-Thought (CoT)

| | Chain-of-Thought | ReAct |
|---|---|---|
| Reasoning | One-shot, up front | Continuous, interleaved with actions |
| Tool interaction | None | Core of the pattern |
| Grounding | Parametric memory only | Real observations from tools |
| Behaviour | Static | Adaptive — revises the plan on new evidence |
| Best for | Math, logic, self-contained reasoning | Lookups, APIs, multi-step tasks with unknowns |

CoT can *sound* correct while inventing facts. ReAct forces the model to check.

---

## ReAct vs Plan-and-Execute

| | ReAct | Plan-and-Execute |
|---|---|---|
| Planning | Implicit, step by step | Explicit plan first, then execution |
| Adaptability | High — replans every turn | Lower — plan may go stale |
| Cost per step | Higher (LLM call every step) | Lower (execute plan with fewer calls) |
| Predictability | Low | High |
| Weakness | Loops, drift, runaway cost | Brittle when the world changes mid-task |
| Best for | Exploratory, unknown-shaped tasks | Well-understood, repeatable workflows |

**Hybrid** (common in production): plan once, execute steps with a small ReAct loop per step, replan only when an observation invalidates the plan.

---

## Designing the Toolset

Fewer, sharper tools beat many overlapping ones:

- **Limit the number of tools** exposed at once — tool-selection accuracy drops as the list grows.
- **Descriptive names and docstrings** — the model chooses tools by reading their descriptions, nothing else.
- **Narrow, composable tools** (`search_docs`, `read_file`) beat one mega-tool with mode flags.
- **Validate arguments** before executing; return a clear error string on failure.
- **Make tools idempotent where possible** so a retry does not duplicate side effects.
- **Group tools by task** and load only the relevant subset per request.

---

## Where ReAct Works Best

- **Open-ended research** — search, read, refine the query, search again.
- **Live/volatile data** — prices, weather, inventory, anything the model was not trained on.
- **Multi-step tool workflows** — fetch an ID, then use it in a second call.
- **Debugging-style tasks** — inspect, hypothesise, test, inspect again.
- **Customer support with backends** — check order, check policy, decide refund.

Where it fits poorly:

- Purely reasoning tasks with no tools (use CoT — cheaper).
- Strictly regulated flows needing a fixed, auditable sequence (use a plan or explicit state machine).
- Latency-critical paths — each iteration adds a full model round-trip.

---

## Failure Modes to Watch For

| Failure | Symptom | Fix |
|---|---|---|
| Infinite loop | Same tool/args repeated | Repeat detection + max steps |
| Hallucinated observation | Fabricated tool result in reasoning | Always inject real output; never let the model self-report results |
| Context overflow | Errors or lost instructions late in the run | Summarise history, prune old steps |
| Tool sprawl | Wrong tool chosen | Fewer tools, better descriptions |
| Prompt injection via tool output | Model obeys text found in a web page | Treat observations as data, not instructions |
| Silent partial success | Agent stops early | Explicit success check before `finish` |

---

## Key Takeaways

1. ReAct = **interleaved reasoning and action**, grounded by real observations.
2. The LLM **proposes**; your system **executes** and **owns safety**.
3. Every loop needs a **budget**: max steps, timeouts, and a cost ceiling.
4. **History is memory** — update it after every action, but keep it trimmed.
5. ReAct is a *pattern*, not a framework — the loop, guardrails, and tool design matter more than the library.
6. Use it where the task shape is unknown; use planning or plain CoT where it isn't.
