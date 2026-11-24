# W1D4: Vague vs precise prompts

## Vague prompt

Prompt: add validation to task titles
Cost (from /cost): $0.31
Acceptance tests passed (labcheck): 2 of 5. It didn't trim, and it didn't validate PATCH.

## Precise prompt

Prompt: (five-part prompt from the lab, plus "trimming happens before the length check")
Cost (from /cost): $0.22
Acceptance tests passed (labcheck): 5 of 5

## What I learned

The precise prompt was cheaper because Claude didn't explore or guess. Naming the files and the
verification step removed two rounds of back-and-forth. The vague version looked fine in review but
missed the PATCH and trimming criteria. Acceptance criteria belong in the prompt.
