from app.redactors.base import Redactor

class CreditCardRedactor(Redactor):

    def enabled(self, policy: dict) -> bool:
        rules = policy.get("redaction_rules", {})
        return rules.get("credit_card", False)

    def redact(self, text: str) -> str:
        """
        Replace credit card-like patterns with <CARD>.
        We consider patterns where 13-16 digits appear (with spaces or dashes allowed).
        """
        result = []
        buffer = ""

        def flush_buffer():
            nonlocal result, buffer
            digit_count = sum(c.isdigit() for c in buffer)
            # Typical credit card ranges from 13 to 16 digits
            if 13 <= digit_count <= 16:
                if result and result[-1].isalnum():
                    result.append(" ")
                result.append("<CARD>")
            else:
                result.append(buffer)
            buffer = ""

        for c in text:
            if c.isdigit() or c in "- ":
                buffer += c
            else:
                if buffer:
                    flush_buffer()
                result.append(c)

        if buffer:
            flush_buffer()

        return "".join(result)