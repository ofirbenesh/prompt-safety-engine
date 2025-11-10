from app.policy_loader import get_policy
from app.redactors.registry import get_all_redactors


def evaluate_prompt(request):

    policy = get_policy()
    prompt = request.prompt

    # Block
    max_chars = policy.get("max_prompt_chars")
    if max_chars is not None and len(prompt) > max_chars:
        return {
            "action": "block",
            "prompt_out": "",
            "reason": f"Prompt exceeds maximum allowed length of {max_chars} characters"
        }

    banned_keywords = policy.get("banned_keywords", [])
    for keyword in banned_keywords:
        if keyword.lower() in prompt.lower():
            return {
                "action": "block",
                "prompt_out": "",
                "reason": f"Contains banned keyword: '{keyword}'"
            }
        
    # Redact
    text = prompt
    changed = False

    for redactor in get_all_redactors():
        if redactor.enabled(policy):
            new_text = redactor.redact(text)
            if new_text != text:
                changed = True
            text = new_text

    if changed:
        return {
            "action": "redact",
            "prompt_out": text,
            "reason": "PII redacted according to policy"
        }

    # Allow
    return {
        "action": "allow",
        "prompt_out": prompt,
        "reason": "No violations"
    }