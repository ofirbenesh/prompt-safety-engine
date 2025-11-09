import string

def redact_email(text: str) -> str:
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

def redact_phone(text: str) -> str:
    result = []
    buffer = ""

    def flush_buffer():
        nonlocal result, buffer
        # Decide if buffer looks like a phone number
        digit_count = sum(c.isdigit() for c in buffer)
        if digit_count >= 7:
            result.append("<PHONE>")
        else:
            result.append(buffer)
        buffer = ""

    for c in text:
        if c.isdigit() or c in "+- ":
            buffer += c
        else:
            # Close phone-like sequence
            if buffer:
                flush_buffer()
            result.append(c)

    # Flush leftover buffer
    if buffer:
        flush_buffer()

    return "".join(result)

def redact_secret(text: str) -> str:
    result = text
    search_token = "SECRET{"
    
    while True:
        start = result.find(search_token)
        if start == -1:
            break

        end = result.find("}", start)
        if end == -1:
            break

        # Replace the entire SECRET{...}
        result = result[:start] + "<SECRET>" + result[end+1:]

    return result

def redact_pii(text: str, redaction_rules: dict) -> str:
    result = text

    # EMAILS
    if redaction_rules.get("email", False):
        result = redact_email(result)

    # PHONE NUMBERS
    if redaction_rules.get("phone", False):
        result = redact_phone(result)

    # SECRET{...}
    if redaction_rules.get("secret", False):
        result = redact_secret(result)

    return result
