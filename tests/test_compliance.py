from recon.compliance import probe_instruction_compliance
from recon.config import COMPLIANCE_INSTRUCTION


def test_compliance_high_when_follow_up_has_no_arabic(monkeypatch):
    calls = []

    def fake_send_message(target_url, message):
        calls.append(message)
        return "Understood." if len(calls) == 1 else "You need the birth certificate and IDs."

    monkeypatch.setattr("recon.compliance.send_message", fake_send_message)

    assert probe_instruction_compliance("http://fake/chat") == "high"
    assert len(calls) == 2
    assert calls[0] == COMPLIANCE_INSTRUCTION
    assert COMPLIANCE_INSTRUCTION in calls[1]  # instruction carried into the follow-up call


def test_compliance_low_when_follow_up_still_has_arabic(monkeypatch):
    def fake_send_message(target_url, message):
        return "لتسجيل مولود جديد you need the birth certificate."

    monkeypatch.setattr("recon.compliance.send_message", fake_send_message)

    assert probe_instruction_compliance("http://fake/chat") == "low"
