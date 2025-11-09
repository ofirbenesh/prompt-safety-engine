from fastapi import FastAPI
from app.routes import router
from app.policy_loader import load_policy

app = FastAPI(
    title="Prompt Safety Engine",
    version="1.0"
)

@app.on_event("startup")
def startup_event():
    load_policy()

app.include_router(router)
