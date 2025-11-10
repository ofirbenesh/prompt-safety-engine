from app.redactors.base import Redactor

class EmailRedactor(Redactor):

    def enabled(self, policy: dict) -> bool:
        rules = policy.get("redaction_rules", {})
        return rules.get("email", False)

    def redact(self, text: str) -> str:
        result = text
        i = 0

        while i < len(result):
            if result[i] == "@":
                # Expand left
                start = i - 1
                while start >= 0 and (result[start].isalnum() or result[start] in "._-"):
                    start -= 1
                start += 1

                # Expand right
                end = i + 1
                while end < len(result) and (result[end].isalnum() or result[end] in "._-"):
                    end += 1

                # Replace the email substring
                result = result[:start] + "<EMAIL>" + result[end:]
                i = start + len("<EMAIL>")
            else:
                i += 1

        return result