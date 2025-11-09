import json
import os

DEFAULT_POLICY_PATH = os.getenv("POLICY_FILE_PATH", "policies/policy.example.json")
policy_cache = {}

def load_policy(path: str = None):
    global policy_cache
    path = path or DEFAULT_POLICY_PATH
    with open(path, "r") as f:
        policy_cache = json.load(f)
    return policy_cache


def get_policy():
    return policy_cache


def reload_policy():
    return load_policy()
