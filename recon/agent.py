from .compliance import probe_instruction_compliance
from .config import DEFAULT_TARGET_URL
from .defense import classify_defense
from .model_family import classify_model_family
from .probes import probe_safety_level


def recon(target_url: str = DEFAULT_TARGET_URL) -> dict:
    """
    Profile the target across the three RECON dimensions and return the
    profile dict consumed by the Attack Agent.
    """
    safety_level, transcript = probe_safety_level(target_url)
    refused_turns = [t for t in transcript if t["refused"]]
    reference_turn = refused_turns[0] if refused_turns else transcript[-1]

    model_family = classify_model_family(reference_turn["response"])
    primary_defense = (
        classify_defense(reference_turn["probe"], reference_turn["response"])
        if refused_turns
        else "semantic_refusal"
    )
    instruction_compliance = probe_instruction_compliance(target_url)

    return {
        "target_url": target_url,
        "safety_level": safety_level,
        "model_family": model_family,
        "instruction_compliance": instruction_compliance,
        "primary_defense": primary_defense,
    }
