from app.policy_loader import get_policy
from app.pii_redactor import redact_pii


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
    redaction_enabled = policy.get("redaction_rules", {})
    redacted_text = redact_pii(prompt, redaction_enabled)

    if redacted_text != prompt:
        # something was changed
        return {
            "action": "redact",
            "prompt_out": redacted_text,
            "reason": "PII redacted according to policy"
        }

    # Allow
    return {
        "action": "allow",
        "prompt_out": prompt,
        "reason": "No violations"
    }
