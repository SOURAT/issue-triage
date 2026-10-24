# input_type_name: SaveIssueInput
# output_type_name: SaveIssueResult
# function_name: save_issue

from typing import Optional

from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod
from lemma_sdk.errors import LemmaAPIError


class SaveIssueInput(BaseModel):
    issue_number: int
    title: str
    body: str = ""
    author: str = ""
    category: str = "other"
    priority: str = "normal"
    duplicate_of: int = 0
    summary: str = ""
    reply: str = ""
    approved: bool = False


class SaveIssueResult(BaseModel):
    denied: bool = False
    status_code: Optional[int] = None
    error_code: Optional[str] = None
    record_id: Optional[str] = None
    status: Optional[str] = None


async def save_issue(ctx: FunctionContext, data: SaveIssueInput) -> SaveIssueResult:
    # A person decided. Approved replies are marked ready to post by hand;
    # skipped ones are kept for the record only.
    status = "READY_TO_POST" if data.approved else "SKIPPED"
    pod = Pod.from_env()
    try:
        record = pod.table("issues").create(
            {
                "issue_number": data.issue_number,
                "title": data.title,
                "body": data.body,
                "author": data.author,
                "category": data.category,
                "priority": data.priority,
                "duplicate_of": data.duplicate_of or None,
                "summary": data.summary,
                "reply": data.reply,
                "status": status,
            }
        )
    except LemmaAPIError as exc:
        return SaveIssueResult(
            denied=True, status_code=exc.status_code, error_code=exc.code
        )
    return SaveIssueResult(record_id=str(record["id"]), status=status)
