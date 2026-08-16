from recon.probes import is_refusal, probe_safety_level


def test_is_refusal_true_for_known_marker():
    assert is_refusal("I can only help with civil registry citizen services.")


def test_is_refusal_false_for_normal_answer():
    assert not is_refusal("You need your birth certificate and a valid photo ID.")


def test_probe_safety_level_stops_at_first_refusal(monkeypatch):
    responses = {
        1: "Sure, here are the requirements.",
        2: "Here's some general info about staff procedures.",
        3: "I can only help with civil registry citizen services.",
        4: "I can't do that.",
    }
    calls = []

    def fake_send_message(target_url, message):
        calls.append(message)
        level = len(calls)
        return responses[level]

    monkeypatch.setattr("recon.probes.send_message", fake_send_message)

    level, transcript = probe_safety_level("http://fake/chat")

    assert level == 3
    assert len(calls) == 3  # stopped after the first refusal, never sent probe 4
    assert transcript[-1]["refused"] is True
    assert transcript[0]["refused"] is False


def test_probe_safety_level_returns_zero_when_never_refused(monkeypatch):
    monkeypatch.setattr(
        "recon.probes.send_message", lambda target_url, message: "Sure, happy to help."
    )

    level, transcript = probe_safety_level("http://fake/chat")

    assert level == 0
    assert len(transcript) == 4
    assert all(not t["refused"] for t in transcript)
