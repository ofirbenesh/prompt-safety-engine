from app.redactors.base import Redactor

class PhoneRedactor(Redactor):

    def enabled(self, policy: dict) -> bool:
        rules = policy.get("redaction_rules", {})
        return rules.get("phone", False)

    def redact(self, text: str) -> str:
        result = []
        buffer = ""

        def flush_buffer():
            nonlocal result, buffer
            digit_count = sum(c.isdigit() for c in buffer)
            # Consider phone if it contains >= 7 digits
            if digit_count >= 7:
                if result and result[-1].isalnum():
                    result.append(" ")
                result.append("<PHONE>")
            else:
                result.append(buffer)
            buffer = ""

        for c in text:
            if c.isdigit() or c in "+- ":
                buffer += c
            else:
                if buffer:
                    flush_buffer()
                result.append(c)

        if buffer:
            flush_buffer()

        return "".join(result)