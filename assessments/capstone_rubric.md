# Capstone rubric (50 points, pass ≥ 35 / 70%)

Score yourself on Day 29 and record the result in `capstone/REVIEW.md`. If your cohort has an instructor or peer
reviewer, they use the same rubric.

| Criterion | 0 | 3 | 5 | 7 | 10 |
|---|---|---|---|---|---|
| **1. Architecture fit** (D1) | No rationale | Pattern named | Pattern justified against the rung below | …plus components and boundaries clear | …plus the decision log shows a real trade-off considered |
| **2. Guardrails and safety** (D2, D4) | Broad tools, no caps | Some caps | Least-privilege tools **and** turn/budget caps | …plus untrusted input handled (delimited, no tool access, or validated) | …plus a human approves every irreversible action, and that's demonstrated |
| **3. Reliability and verification** (D3, D5) | No tests | Some tests | Deterministic shell tested with no API calls | …plus output validated (schema) and failures handled explicitly | …plus a small eval or golden cases |
| **4. Cost awareness** (D5) | Unknown | Rough guess | Measured cost per run | …plus a monthly estimate at realistic usage | …plus the worst case is bounded and explained |
| **5. Communication** | No README | Run instructions | Brief, How to run, Architecture | …plus honest Limitations | …plus a review log with decisions (fix / accept / won't fix) |

**Common reasons capstones lose points**
- An agent where a workflow would do (criterion 1).
- `bypassPermissions`, or Bash without restrictions (criterion 2).
- Tests that call the model, so they're flaky and cost money (criterion 3).
- "It's cheap" with no numbers (criterion 4).
