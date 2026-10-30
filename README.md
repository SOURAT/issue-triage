# Issue Triage

**Who it is for:** maintainers of an open-source project who get more GitHub
issues than they can sort by hand.
**What it does:** it labels each new issue, spots duplicates, drafts a kind
reply asking for missing details, and waits for a person to approve before
anything is final.

## The people
- **Triager** (any contributor): opens the **Triage Board**, reads the agent's
  suggestion, edits the reply, and approves or skips it.
- **Maintainer** (project owner): reads the **morning digest** and keeps the
  approved-reply queue moving by marking replies as posted.

## How it works
1. A new GitHub issue is opened (or you add one by hand).
2. `triage_agent` decides the category and priority, checks for a duplicate,
   lists missing details, and drafts a reply.
3. **The run stops and waits.** A person approves or skips it on the board.
4. `save_issue` stores the result. Approved replies show under **Approved**,
   where a person copies them to GitHub and marks them as posted.
5. Every morning at 09:00 UTC, `morning_digest` writes a short report.

Nothing is ever posted to GitHub automatically.

## What's inside
| Part | Name | Job |
|---|---|---|
| App | `triage_board` | Review, approve, mark posted, read the digest |
| Agent | `triage_agent` | Category, priority, duplicate check, draft reply |
| Workflow | `triage_on_issue` | Automatic: new GitHub issue -> agent -> approval -> save |
| Workflow | `triage_flow` | Manual: paste an issue -> agent -> approval -> save |
| Workflow | `morning_digest` | Daily report |
| Schedule | `morning_digest` | Runs the digest every day at 09:00 UTC |
| Functions | `save_issue`, `morning_digest` | Plain code that saves results |
| Tables | `issues`, `digests` | The shared history |

## Run it on your machine
Set up Lemma locally first (see the Lemma README). Then:
```bash
lemma servers select local
lemma auth login
lemma pods create issue-triage
lemma pods import . --pod <pod-id>
lemma records import issues payloads/seed_issues.json --pod <pod-id>
lemma workflows run morning_digest --pod <pod-id>
lemma workflows run triage_flow --pod <pod-id> --file payloads/sample_issue.json
lemma apps open triage_board --pod <pod-id>
```
`payloads/seed_issues.json` is a month of made-up issues, so the board and the
digest are not empty. It contains no real people and no keys.

Open the Triage Board. The run from `triage_flow` is waiting under **To review**.
Approve it and it moves to **Approved**.

## Optional: automatic intake from GitHub
1. Connect GitHub in Lemma and install the Lemma GitHub App on a repository.
2. `lemma connectors accounts list --connector github`
3. ```bash
   lemma schedules create --workflow triage_on_issue --webhook-source github --account <account-id> --pod <pod-id>
   ```
4. Open an issue on that repository. A run appears under **To review**.

## Limits
- Approved replies are copied to GitHub by a person.
- The agent only compares an issue with ones already saved, so duplicate
  detection improves as more issues are triaged.

## License
MIT. See `LICENSE`.
