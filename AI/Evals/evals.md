# Evals

An eval measures whether an AI system works for its users, on realistic tasks and data. It is systematic measurement of quality, replacing "vibe checks".

## Why evals

- LLM output is non-deterministic, so you can't just eyeball a few runs.
- Prompt, model or retrieval changes can silently regress quality.
- Evals give a repeatable score, so you can compare changes and ship with confidence.
- They are the base for fine-tuning, because labelled examples become training data.

## Two kinds of evals

| | Model benchmark | Product eval |
|---|---|---|
| Question | How good is this model in general? | Does *my* system work for *my* users? |
| Data | Public, generic (MMLU, HumanEval, GSM8K, ...) | Your own tasks, traces and edge cases |
| Use | Choosing a base model | Deciding whether to ship, catching regressions |

Benchmarks only shortlist models. Product evals decide quality.

**Mechanisms for product evals** (cheap and fast to expensive and slow):

1. Code assertions (exact match, regex, schema or JSON validity, tool-call checks)
2. LLM-as-judge
3. Human review
4. Online experiments (A/B tests)

## Levels of evaluation

### Level 1: Unit tests (assertions)

- Write scoped tests for each feature or failure mode. Never skip this level.
- Create test cases by hand, and generate synthetic test data (use an LLM to produce varied inputs and edge cases).
- Run them regularly (on every prompt, model or code change, ideally in CI) and track pass rate over time.
- Example assertions: the output is valid JSON, it doesn't leak the system prompt, it calls the right tool, and the answer contains the expected fact.

### Level 2: Human and model evaluation

**Logging traces**
- A trace is the log of the sequence of events for one request flow. For an LLM app it covers the conversation, retrieved context, tool calls, latencies and token counts.
- LangChain integrates with LangSmith for tracing (other options: Langfuse, Phoenix, Braintrust).
- Review traces regularly and label them good or bad, with a short reason. Labelled examples help you to:
  - measure the quality of the system
  - validate automated evals (does the LLM judge agree with human labels?)
  - curate high-quality synthetic data for fine-tuning

**Automated evals with LLMs (LLM-as-judge)**
- A second LLM scores outputs against a rubric, such as correctness, helpfulness, faithfulness to context or tone.
- Prefer binary or low-scale scores with written criteria over vague 1-10 ratings.
- Calibrate against human labels, and keep checking agreement over time.
- Known biases: position bias, verbosity bias, and self-preference (a model favours its own outputs).
- For RAG, evaluate retrieval (recall@k, MRR, context precision) separately from generation (faithfulness, answer relevance). RAGAS and DeepEval implement these.

### Level 3: A/B testing

- Run variants (prompt, model, retrieval setup) on real traffic and compare product metrics.
- Metrics: task success, thumbs up or down, retention, escalation rate, cost, latency.
- It's the slowest and costliest level, so use it after Levels 1 and 2 pass.

## Feeding back into the system

- **Fine-tuning**: use labelled good and bad traces to train or preference-tune a model.
- **Data synthesis and curation**: generate synthetic data from failure cases, filter it by eval score, and add it to the test or training set.
- Improvement loop: **trace, label, find failure mode, add test, fix, re-run evals**.

## Practical checklist

1. Start with 20-50 real or realistic cases and grow from failures you find.
2. Cover happy paths, edge cases and adversarial inputs.
3. Keep a fixed regression set that never shrinks.
4. Version prompts, datasets and eval results together.
5. Track cost and latency next to quality.
6. Review failures by hand, since a score alone doesn't tell you why something failed.

## Tools

LangSmith, Langfuse, Arize Phoenix, Braintrust, promptfoo, RAGAS, DeepEval, OpenAI Evals.

## Reference

Framework of the three levels: Hamel Husain, *Your AI Product Needs Evals*.
