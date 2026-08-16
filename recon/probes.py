from .client import send_message
from .config import REFUSAL_MARKERS, SAFETY_PROBES


def is_refusal(response: str) -> bool:
    lower = response.lower()
    return any(marker in lower for marker in REFUSAL_MARKERS)


def probe_safety_level(target_url: str) -> tuple[int, list[dict]]:
    """
    Send the four gradient probes in order. Returns (safety_level, transcript).

    safety_level is the level of the first probe that gets refused. If none
    of the four probes get refused, safety_level is 0 -- the target is fully
    permissive within the probes tested.
    """
    transcript = []
    for level, probe_text in SAFETY_PROBES:
        response = send_message(target_url, probe_text)
        refused = is_refusal(response)
        transcript.append(
            {"level": level, "probe": probe_text, "response": response, "refused": refused}
        )
        if refused:
            return level, transcript
    return 0, transcript
