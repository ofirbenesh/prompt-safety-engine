from fastapi import APIRouter
from app.models import MitigateRequest, MitigateResponse
from app.engine import evaluate_prompt
from app.history import log_entry, get_history
from app.policy_loader import reload_policy

router = APIRouter()


@router.post("/mitigate", response_model=MitigateResponse)
def mitigate(request: MitigateRequest):
    result = evaluate_prompt(request)
    log_entry(request, result)
    return result


@router.get("/history")
def history(limit: int = 20):
    return get_history(limit)


@router.post("/reload_policy")
def reload():
    reload_policy()
    return {"status": "policy reloaded"}
