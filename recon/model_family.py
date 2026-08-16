from .config import MODEL_FAMILY_PHRASES


def classify_model_family(refusal_response: str) -> str:
    """
    Classify model family from refusal phrasing. Table entries are
    placeholders until calibrated against Ahmed's live Phi target (Step 10).
    """
    lower = refusal_response.lower()
    for family, phrases in MODEL_FAMILY_PHRASES.items():
        if any(phrase in lower for phrase in phrases):
            return family
    return "unknown"
