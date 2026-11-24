# Week 6 · Day 27: Agentic architecture design review

| | |
|---|---|
| **Level** | Expert |
| **CCA-F domain** | 1 · Agentic architecture & orchestration (27% of the exam) |
| **Time** | 15 min read · 30 min design · 15 min review |
| **Budget cap** | $0.40 |
| **Check** | `uv run labcheck w6d27` |

## 🎯 Goal

Choose and justify an architecture for your capstone, using the patterns and trade-offs the certification
tests, *before* you write code.

## 📖 Primer: the pattern ladder (use the lowest rung that works)

| Rung | Pattern | Use when | Watch out for |
|---|---|---|---|
| 1 | **Single call** | One well-defined transformation (classify, extract, summarise) | Don't build an agent for this |
| 2 | **Prompt chain / workflow** | Fixed steps known in advance; code controls the flow | Brittle if steps vary per input |
| 3 | **Routing** | Different input types need different handling | Misroutes, so log and evaluate the router |
| 4 | **Single agent with tools** | Open-ended steps; the model decides what to do next | Cost and turn caps; tool design quality |
| 5 | **Orchestrator–workers** (subagents) | Work splits into independent parts that need isolated contexts | Coordination overhead; summaries lose detail |
| 6 | **Evaluator–optimizer** | Output quality can be judged against criteria (tests, rubric, schema) | Infinite loops, so cap iterations |

**Cross-cutting concerns** every design must address:
- **Guardrails**: permissions, hooks, allowed tools, sandboxing, schema validation
- **Human in the loop**: where a person approves (side effects, irreversible actions, low confidence)
- **Context strategy**: what each agent sees; subagents, compaction, handoff files
- **Cost**: tokens per run × runs per day; caps; model choice per component
- **Failure modes**: what happens on a tool error, a timeout, bad output, or budget exhaustion
- **Evaluation**: how you'll know it works, before and after launch

## 🛠️ Steps

**1. Read the three capstone briefs** in [3_lab3_capstone_build.md](3_lab3_capstone_build.md) and pick one.

**2. Draft the design yourself first** (10 minutes, no Claude). Create `docs/architecture/capstone-design.md` with
these sections: **Problem**, **Pattern**, **Components**, **Guardrails**, **Cost estimate**, **Failure modes**,
**Human in the loop**. Under **Pattern**, name the rung and say why the rung *below* isn't enough.

**3. Get an adversarial review.**

> Review @docs/architecture/capstone-design.md as a principal engineer who is sceptical of over-engineered
> agent systems. Challenge the pattern choice (could a simpler rung work?), find missing guardrails and failure
> modes, and sanity-check the cost estimate. Be concrete and brief. Do not rewrite the document.

**4. Revise** the document by hand. Keep a short **Decision log** at the bottom: what you changed and why.

**5. Commit** it.

## ✅ Checkpoint

```bash
uv run labcheck w6d27
```

## 💰 Budget & cost log

Cap: **$0.40**.

```bash
uv run labcheck log w6d27 0.25 "design review"
```

## 🚀 Stretch

Draw the architecture as a Mermaid diagram in the doc. Which arrows carry untrusted data?

## 💼 Commercial application

Most failed agent projects are over-built: a multi-agent system where a workflow would have done. Being the
person who can say "rung 2 is enough, and here's why", or "this genuinely needs rung 5, and here are the guardrails",
is the core skill of an agentic architect.

## 🤔 Reflect

1. Which review point changed your design the most?
2. Where exactly does a human approve something in your design, and why there?
3. How will you know, a month after launch, that it still works?

## ➡️ Next

[Day 28: Capstone day 1](3_lab3_capstone_build.md)
