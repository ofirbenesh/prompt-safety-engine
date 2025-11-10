from app.redactors.base import Redactor

class SecretRedactor(Redactor):

    def enabled(self, policy: dict) -> bool:
        rules = policy.get("redaction_rules", {})
        return rules.get("secret", False)

    def redact(self, text: str) -> str:
        result = text
        search_token = "SECRET{"

        while True:
            start = result.find(search_token)
            if start == -1:
                break

            end = result.find("}", start)
            if end == -1:
                break

            # Add a space before tag if needed
            prefix = result[:start]
            if prefix and prefix[-1].isalnum():
                prefix += " "

            suffix = result[end+1:]
            result = prefix + "<SECRET>" + suffix

        return result