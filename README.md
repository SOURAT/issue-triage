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
| Workflow | `triage_flow` | Manual: form -> agent -> approval form -> save |
| Workflow | `triage_on_issue` | Automatic: new GitHub issue -> agent -> approval form -> save |

## Try it (manual)
```bash
lemma auth login
lemma orgs create <org-name>
lemma orgs select <org-name> --save-default
lemma pods create issue-triage --org <org-id>
lemma pods import . --pod <pod-id> --dry-run
lemma pods import . --pod <pod-id>
lemma workflows run triage_flow --pod <pod-id> --file payloads/sample_issue.json
```
Wait for the agent, then approve or skip the reply:
```bash
lemma workflows runs submit-form <run-id> --pod <pod-id> --file payloads/approve.json
```
(`payloads/approve.json` contains `{"approved": true}`.)

## Automatic intake
`triage_on_issue` starts by itself when a new issue is opened on a connected
GitHub repository. After importing the pod:

1. Connect GitHub in Lemma and install the Lemma GitHub App on your repository.
2. Find your connected account id: `lemma connectors accounts list --connector github`
3. Create the trigger:
   ```bash
   lemma schedules create --workflow triage_on_issue --webhook-source github --account <account-id> --pod <pod-id>
   ```
4. Open a new issue on the repository. A run appears, waiting for approval
   (`lemma workflows runs list triage_on_issue --pod <pod-id>`).

## Limits
- Approved replies are saved as `READY_TO_POST`. Posting to GitHub is still done
  by a person.
- Duplicate detection compares against issues already saved in the `issues`
  table, so it improves as more issues are triaged.

## Roadmap
1. Post the approved reply back to GitHub through a connector.
2. Suggest labels from the repo's own label list.