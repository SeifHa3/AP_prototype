import httpx


def send_message(target_url: str, message: str, timeout: float = 15.0) -> str:
    """POST a single message to the target's /chat endpoint and return its response text."""
    resp = httpx.post(target_url, json={"message": message}, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["response"]
