import json

policy_cache = {}

def load_policy(path: str = "policies/policy.json"):
    global policy_cache
    with open(path, "r") as f:
        policy_cache = json.load(f)
    return policy_cache


def get_policy():
    return policy_cache


def reload_policy():
    return load_policy()
