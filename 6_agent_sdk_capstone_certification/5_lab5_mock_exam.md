# Week 6 · Day 30: Mock CCA-F exam and readiness plan

| | |
|---|---|
| **Level** | Expert |
| **CCA-F domain** | all five |
| **Time** | Mock exam: 120 minutes (do it in one sitting, outside your daily hour if needed) · Review: 60 min |
| **Budget cap** | **$0**. This day is entirely offline. |
| **Check** | `uv run labcheck w6d30` |

## 🎯 Goal

Find out, honestly, whether you're ready to book the Claude Certified Architect – Foundations exam, and if
not, exactly what to study.

## 🛠️ Steps

**1. Prepare.** Read [Guide 07: the CCA-F exam](../guides/07_cca_f_exam_overview.md). Close Claude Code. Copy the
result template:

```bash
cp notes/templates/mock-exam-result.md notes/mock-exam-result.md
```

**2. Take the mock exam** in [assessments/mock_exam_cca_f.md](../assessments/mock_exam_cca_f.md): 60 questions in
120 minutes, no notes, no Claude. Write your answers on paper or in a scratch file.

**3. Mark it** with [assessments/answers/mock_exam_answers.md](../assessments/answers/mock_exam_answers.md). Each answer has
an explanation and a lab reference. Read the explanations even for questions you got right.

**4. Fill in `notes/mock-exam-result.md`**: total `Score: NN/60`, score per domain, then:
- **Gap analysis**: your two weakest domains, and the *type* of mistake (didn't know the feature, misread the
  scenario, or picked an over-engineered answer)
- **Study plan**: the specific labs to redo, docs pages to read, and Anthropic Academy courses to take, with dates

**5. Decide.**
- **≥ 72%** with time to spare: you're ready. Ask your admin about exam access via the Claude Partner Network.
- **60–71%**: follow your study plan for 1–2 weeks, then retake the mock (the question order doesn't matter;
  re-read the explanations instead of memorising letters).
- **< 60%**: redo the labs for your weakest domains first.

**6. Run the full course check**, and celebrate. You've earned it.

```bash
uv run labcheck --all
uv run labcheck budget
```

## ✅ Checkpoint

```bash
uv run labcheck w6d30
```

## 💰 Budget & cost log

Nothing to log today. Look back over your whole cost log: which week cost the most, and what would you do differently?

## 🚀 Stretch

Write five **new** scenario questions in the exam style about the area you found hardest, with explanations. Writing
good distractors is one of the best ways to really learn a topic. Contribute them to `community_contributions/`.

## 💼 Commercial application

The certification signals to your employer and clients that you can **design, configure and govern** agentic
systems, not just prompt them. The capstone you built this week is the evidence behind the badge.

## 🤔 Reflect

1. Which domain was your weakest, and why do you think it was?
2. How many of your mistakes were "picked the more complex option"?
3. What's the first thing you'll do differently at work on Monday?

## 🎓 Congratulations

Six weeks ago you typed your first prompt. Now you can configure, extend, automate and architect with Claude
Code, and you have the receipts: 30 labs, a plugin, an MCP server, a CI workflow, an SDK agent and a capstone.
Thank you for doing the work. Please share your feedback by opening an issue on the course repo.
