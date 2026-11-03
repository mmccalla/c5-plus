# Question validation

The viewer's questions are checked against agreed answers on every change, by `scripts/check_questions.js` (run by pre-commit and CI). The check runs `questions.js`, the same code the page uses.

## What is checked

- **Scope.** Each of the 18 questions says which elements it is about (192 question–element pairs in all). The page tells people when they ask a question about something outside its scope, and lets them ask anyway. Each question's built-in example must be in its scope.
- **Answers.** 109 agreed answers for the five most-used questions: Q3 *Who owns this?*, Q1 *What depends on this?*, Q2 *What will a change to this impact?*, Q7 *Which teams must be involved?* and Q13 *Who must act on this incident?*. For Q3, Q7 and Q13 the answer must be exactly the agreed one; for Q1 and Q2 it must include the agreed elements.

The agreed answers, with a one-line reason for each, are in `tests/expected-answers.json`. To change one, edit that file: the check then holds the viewer to the new answer.

## Decisions

1. A question asked about something outside its scope says so instead of guessing, with an option to ask anyway.
2. Business elements and governance rules are owned by a **business role**: business capabilities, services, processes and value streams, KPIs, policies, standards, procedures, controls and risks.
3. **SRE** is involved whenever a live system changes or fails: application services, infrastructure services, ML models and the data products feeding them.

## Corrections to the first draft

Fixing the model showed that some of the first draft's expected answers were wrong. Each was corrected rather than forcing the model to match:

| # | Question | Element | Correction |
|---|---|---|---|
| C1 | Q3 | application interface | Also owned by the product team when it exposes a product. |
| C2 | Q1 | business service | Expected business process, not products and services or business capability: those realise or are exposed through the service rather than depend on it. |
| C3 | Q1 | data catalog | No must-include answer: the draft expected data objects, but data is registered in the catalog rather than depending on it. |
| C4 | Q1 | technology interface | Dropped infrastructure service: it provides the interface rather than depending on it. |
| C5 | Q2, Q7 | change, change request | Removed from scope: they are process records. Ask about the specific change, for example the application change. |
| C6 | Q13 | platform failure | Product team added, consistent with incidents. |
| C7 | Q13 | model bias | SRE added: the model is a live system (decision 3). |
| C8 | Q7 | application change, application component, data object, data product, ml model | Platform team added: it owns a shared platform product the change reaches. |
| C9 | Q7 | application change, application service | Product team added: its product is built on the affected service. |
| C10 | Q7 | data object | SRE added: live services use the data (decision 3). |

## Model changes this required

- **Ownership:** 43 *owns* or *accountable for* relationships added, including the business-role ownership above, platform-team ownership of shared platform products, and stewardship of master and reference data.
- **Missing facts:** applications call application interfaces and platform interfaces; application interfaces are published through API management; infrastructure services run on nodes; a release can affect the application service; SRE supports application services, infrastructure services and ML models.
- **Impact direction:** *exposed via* now carries a change both ways: a change to what is exposed reaches the channel (service → interface), and a change to the channel reaches what it exposes (business service → capability → customer outcomes).
- **Questions:** Q3 follows ownership through what an element belongs to and gives only the nearest owner; Q1 follows the right direction for exposure, permissions, part-whole and subtypes; Q7 and Q13 stop at the first team and consider operating teams only.
