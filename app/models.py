from pydantic import BaseModel
from typing import Optional, Dict


class MitigateRequest(BaseModel):
    prompt: str
    user_id: str
    model: Optional[str] = None
    purpose: Optional[str] = None
    headers: Optional[Dict] = None


class MitigateResponse(BaseModel):
    action: str            # allow | redact | block
    prompt_out: str        # possibly redacted prompt
    reason: str            # human-readable explanation