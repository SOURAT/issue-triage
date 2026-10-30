# input_type_name: DigestInput
# output_type_name: DigestResult
# function_name: morning_digest

from datetime import date
from typing import Optional

from pydantic import BaseModel
from lemma_sdk import FunctionContext, Pod
from lemma_sdk.errors import LemmaAPIError


class DigestInput(BaseModel):
    pass


class DigestResult(BaseModel):
    denied: bool = False
    status_code: Optional[int] = None
    error_code: Optional[str] = None
    summary: Optional[str] = None


async def morning_digest(ctx: FunctionContext, data: DigestInput) -> DigestResult:
    pod = Pod.from_env()
    try:
        rows = pod.records.list("issues", limit=500).to_dict()["items"]
        rows = [r.get("data", r) for r in rows]

        total = len(rows)
        to_post = sum(1 for r in rows if r.get("status") == "READY_TO_POST")
        duplicates = sum(1 for r in rows if r.get("duplicate_of"))
        urgent_open = sum(
            1
            for r in rows
            if r.get("priority") in ("urgent", "high")
            and r.get("status") in ("READY_TO_POST", None, "")
        )

        summary = (
            f"{total} issues triaged so far. "
            f"{to_post} approved replies are waiting to be posted. "
            f"{urgent_open} urgent or high-priority issues are still open. "
            f"{duplicates} were flagged as duplicates."
        )
        pod.table("digests").create(
            {
                "day": date.today().isoformat(),
                "total": total,
                "urgent_open": urgent_open,
                "to_post": to_post,
                "duplicates": duplicates,
                "summary": summary,
            }
        )
    except LemmaAPIError as exc:
        return DigestResult(
            denied=True, status_code=exc.status_code, error_code=exc.code
        )
    return DigestResult(summary=summary)
