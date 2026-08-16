from recon.agent import recon


def test_recon_assembles_full_profile_dict(monkeypatch):
    safety_responses = {
        1: "Sure, here are the requirements.",
        2: "Here's some general info about staff procedures.",
        3: "I can only help with civil registry citizen services.",
    }
    safety_calls = []

    def fake_probe_send(target_url, message):
        safety_calls.append(message)
        return safety_responses[len(safety_calls)]

    def fake_compliance_send(target_url, message):
        return "Understood." if "birth" not in message else "You need the birth certificate."

    monkeypatch.setattr("recon.probes.send_message", fake_probe_send)
    monkeypatch.setattr("recon.compliance.send_message", fake_compliance_send)

    profile = recon("http://fake/chat")

    assert profile == {
        "target_url": "http://fake/chat",
        "safety_level": 3,
        "model_family": "phi",
        "instruction_compliance": "high",
        "primary_defense": "role_enforcement",
    }


def test_recon_defaults_to_semantic_refusal_when_never_refused(monkeypatch):
    monkeypatch.setattr(
        "recon.probes.send_message", lambda target_url, message: "Sure, happy to help."
    )
    monkeypatch.setattr(
        "recon.compliance.send_message", lambda target_url, message: "Still happy to help."
    )

    profile = recon("http://fake/chat")

    assert profile["safety_level"] == 0
    assert profile["primary_defense"] == "semantic_refusal"
