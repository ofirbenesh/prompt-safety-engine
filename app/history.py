from collections import deque
from datetime import datetime

history = deque(maxlen=50)   # final size controlled by policy

def log_entry(request, result):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": request.user_id,
        "prompt": request.prompt,
        "decision": result["action"]
    }
    history.append(entry)


def get_history(limit=20):
    return list(history)[-limit:]
