from recon.model_family import classify_model_family


def test_classify_model_family_matches_phi_phrase():
    assert classify_model_family("I can only help with civil registry citizen services.") == "phi"


def test_classify_model_family_matches_gpt_phrase():
    assert classify_model_family("I'm sorry, but I can't help with that.") == "gpt"


def test_classify_model_family_unknown_when_no_phrase_matches():
    assert classify_model_family("Completely unrelated response text.") == "unknown"
