# Case-by-case semantic risk queue — live run 38500177379

**Evidence:** [live run 38500177379](https://github.com/AMMARICA1791/ai-research-agents/actions/runs/38500177379), artifact `11865338443`, generated from five archived DeepMind/Google Developers articles. The original reviewer packet and model responses are inside the workflow ZIP (retained temporarily). Do not add archived publisher excerpts to public commits.

**Status:** Assistant-authored *preliminary triage only*, **not** two independently supplied human gold reviews. No semantic-accuracy percentage is asserted. The model's first-hand cited passage—not a substitute quotation selected by a reviewer—must substantiate the answer. Mechanical quote matches are not proof of that relation.

| Case | Type | Mechanical result | Specific semantic issue requiring independent judgment |
| --- | --- | --- | --- |
| Q01 | Direct | Quote match | The answer repeats a sweeping publisher assertion about robotics capabilities; require attribution rather than independent endorsement |
| Q02 | Inference | Quote match | The answer paraphrases the publisher's claimed breakthrough without clearly separating that claim from independent proof |
| Q03 | Unanswerable | Quarantined: model URL mismatch | The model chose NOT_IN_SOURCE, but did not correctly echo the archived source URL; review absence in excerpt separately |
| Q04 | Direct | Quote match | Quotation supports the product introduction; extra claims about how watermarking works appear elsewhere, not in the model's selected quote |
| Q05 | Inference | Quote match | Physical-protein verification details are asserted while the selected quote only announces a watermarking technology |
| Q06 | Unanswerable | Quarantined: model URL mismatch | Same absence decision vs malformed provenance distinction |
| Q07 | Direct | Quote match | Model cites the broad privacy motivation instead of the article's explicit technical proposal; test entailment of cross-device memory claims |
| Q08 | Inference | Quote match | The general privacy narrative is not evidence of implementation or technical success; source framing must remain conditional |
| Q09 | Unanswerable | Quarantined: model URL mismatch | Absence decision is not equivalent to a valid citation envelope |
| Q10 | Direct | Quote match | A student-exam analogy was used to support a technical double-blind evaluation claim; the cited analogy alone cannot prove the mechanism |
| Q11 | Inference | Quote match | The same analogy is used as technical evidence for the evaluation pilot; evaluate whether the quote addresses the inference at all |
| Q12 | Unanswerable | Quarantined: nonempty model quote | Answer says NOT_IN_SOURCE but quote is an unrelated retrieval-status token; invalid absence envelope |
| Q13 | Direct | Quarantined: quote not in archived excerpt | The original selected title/author passage does not literally match the archived HTML extraction; cannot be silently replaced |
| Q14 | Inference | Quote match | Quotation describes what developers are *teaching* robots to do; the answer presents demonstrated capability in unpredictable environments |
| Q15 | Unanswerable | Valid mechanical abstention envelope | Reviewer must still verify the exact requested revenue is absent from the short excerpt |

## Mechanical facts from the archived audit

- 15 structured outputs linked to five archived sources.
- 9 answerable-case quotes exactly matched source snippets; this does **not** establish answer entailment.
- 5 cases quarantined (Q03, Q06, Q09, Q12, Q13).
- Q15 alone had a valid abstention **envelope**, even though all five negative-control answer fields chose NOT_IN_SOURCE.
- 0 independent human review records and 0 verified semantic accuracy scores.
- No output was approved for unattended publication.

## Non-negotiable review rule

A reviewer may **not** mark Q04, Q05, Q07, Q08, Q10, Q11, or any other quote-supported case as SUPPORTED just because the *overall excerpt* contains better supporting prose elsewhere. The judgment concerns the **specific model-provided citation**. Additional evidence can guide later model repair, but must not be substituted into the review of the original answer. Reviewers should classify each substantive claim and its cited passage, distinguish reported publisher claims from independent verification, and send disagreements for explicit adjudication.

This queue is a prioritization aid for two outside reviewers, not their answers.
