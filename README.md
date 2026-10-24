# Issue Triage

A Lemma teammate that helps open-source maintainers sort new GitHub issues.
It labels each issue, spots duplicates, drafts a kind reply asking for missing
details, and **waits for a person to approve** before anything is final.

## What's inside
| Part | Name | Job |
|---|---|---|
| Table | `issues` | Every triaged issue and the decision made |
| Agent | `triage_agent` | Category, priority, duplicate check, draft reply |
| Function | `save_issue` | Saves the result and the person's decision |
| Workflow | `triage_flow` | Form -> agent -> approval form -> save |

## Try it
```bash
lemma auth login
lemma pods create issue-triage --org <your-org>
lemma pods import . --dry-run
lemma pods import .
lemma workflows run triage_flow
```
Fill in the first form (see `payloads/sample_issue.json`), wait for the agent,
then approve or skip the reply in the second form.

## Limits (v0.1)
- Issues are pasted in by hand. Automatic intake from a GitHub webhook is a
  planned next step.
- Approved replies are saved as `READY_TO_POST`. Posting to GitHub is still done
  by a person.

## Roadmap
1. Automatic intake: start triage from a GitHub webhook when an issue is opened.
2. Post the approved reply back to GitHub through a connector.
3. Suggest labels from the repo's own label list.
