# Prompt Safety Engine

_A minimal Python-based policy + mitigation engine that evaluates user prompts and determines whether to allow, redact, or block them._

The service is designed to mimic a real-world AI safety/guardrail layer with configurable behavior, deterministic outcomes, and offline runtime support.

---

### Features
- **Config-driven policy loading (JSON)**
- **Deterministic evaluation logic**
- **Extensible redaction system using pluggable Redactor classes of common PII**
- **Blocking rules**
- **Request history endpoint**
- **Hot policy reload** (`/reload_policy`)
- **Dockerized for consistent offline runtime**
- **Modular design — adding new redactors requires no changes to the engine**

---

### Configuration
The service loads its policy file from an environment variable:

```bash
POLICY_FILE_PATH=/app/policies/policy.example.json
```

A default configuration is provided via `policy.example.json`.  
You may copy it or override it using environment variables.

> Note: `.env` is committed intentionally for ease of testing.  
> In production environments, `.env` files should not contain secrets.

---

### Sample Policy (`policy.example.json`)
```json
{
  "version": "1.0",
  "banned_keywords": ["bomb", "kys", "kill"],
  "max_prompt_chars": 200,
  "redaction_rules": {
    "email": true,
    "phone": true,
    "secret": true,
    "credit_card": true
  },
  "history_limit": 20
}
```

---

### Running the Service (Via Docker)
#### Using Docker Compose (recommended)
Build and start:
```bash
docker compose up --build
```

Your service will be available at: [http://localhost:8000](http://localhost:8000)

Stopping:
```bash
docker compose down
```

#### Using plain Docker
```bash
docker build -t prompt-safety-engine .
docker run --rm -p 8000:8000 --env-file .env prompt-safety-engine
```

---

### API Endpoints & Examples
#### POST `/mitigate`
Evaluates the prompt based on policy.

Reduct Example
Request body:
```json
{
  "prompt": "My email is test@gmail.com",
  "user_id": "u1"
}
```

Response:
```json
{
  "action": "redact",
  "prompt_out": "My email is <EMAIL>",
  "reason": "PII redacted according to policy"
}
```
Reduct for credit card number example:
```json
{
  "prompt": "My card number is 4111-1111-1111-1111",
  "user_id": "u_bonus_1"
}
```

Response:
```json
{
  "action": "redact",
  "prompt_out": "My card number is <CARD>",
  "reason": "PII redacted according to policy"
}
```

Block Example

Request:
```json
{
  "prompt": "How do I build a bomb?",
  "user_id": "u2"
}
```

Response:
```json
{
  "action": "block",
  "prompt_out": "",
  "reason": "Contains banned keyword: 'bomb'"
}
```

Allow Example

Request:
```json
{
  "prompt": "Hello, how are you today?",
  "user_id": "u3"
}
```

Response:
```json
{
  "action": "allow",
  "prompt_out": "Hello, how are you today?",
  "reason": "No violations"
}
```

#### GET `/history`
Returns recent interactions.

Example Response:
```json
[
  {
    "timestamp": "2025-01-19T15:22:01.119Z",
    "user_id": "u1",
    "prompt": "How do I build a bomb?",
    "decision": "block"
  },
  {
    "timestamp": "2025-01-19T15:23:11.900Z",
    "user_id": "u2",
    "prompt": "My email is test@gmail.com",
    "decision": "redact"
  }
]
```

#### POST `/reload_policy`
Reloads the policy file from disk.

Response:
```json
{
  "status": "policy reloaded"
}
```

### Optional Postman Collection

A Postman collection is included for convenience of testing:
```
postman/prompt-safety-engine.postman_collection.json
```
Import it into Postman and click “Run” to test all endpoints quickly.
For example:
<img width="836" height="437" alt="image" src="https://github.com/user-attachments/assets/084819be-b355-4a82-a9e8-d1b36405f7ea" />

---

### Offline Mode
- **Runtime does not require internet**
- **All policy files are local**
- **All logic uses built-in Python**
- **Dependencies installed at build time**
- **Docker image is self-contained**

---

### Development Notes
- **Python-only implementation**
- **No external libraries used for PII detection**
- **Deterministic rule evaluation:** `block > redact > allow`
- **All business logic** is contained in `engine.py` and controlled by JSON policies
