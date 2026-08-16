# RECON Agent

Profiles a target chatbot before any attack fires. Sends benign text probes
and returns a profile dict telling the Attack Agent which techniques to
prioritize and which defense to expect.

Owner: Seif El Dein Hany. See `AgentProbe_Prototype_Tasks.docx` (section 4)
for the full spec.

## Usage

```bash
pip install -r requirements.txt
python run_recon.py --target http://localhost:8000/chat
```

Or as a library:

```python
from recon import recon

profile = recon("http://localhost:8000/chat")
```

Output — the profile dict:

```json
{
  "target_url": "http://localhost:8000/chat",
  "safety_level": 3,
  "model_family": "phi",
  "instruction_compliance": "high",
  "primary_defense": "role_enforcement"
}
```

- `safety_level` (0-4) — level of the first probe that got refused (0 if the
  target never refused any of the four gradient probes).
- `model_family` — `"phi" | "gpt" | "claude" | "unknown"`, classified from
  refusal phrasing.
- `instruction_compliance` — `"high" | "low"`, whether the target obeyed an
  out-of-scope instruction ("respond only in English") on a follow-up turn.
- `primary_defense` — `"semantic_refusal" | "keyword_filter" |
  "role_enforcement" | "safety_classifier"`, classified from the refusal
  response.

## Mock target

`mock_target/server.py` is a throwaway FastAPI stand-in for Ahmed's real
target, used to build and test RECON before his bot is ready. Same API
shape: `POST /chat {"message": str} -> {"response": str}`.

```bash
uvicorn mock_target.server:app --port 8000
```

Delete this directory once the real target is live.

## Tests

```bash
pytest tests/ -v
```

Unit tests mock `send_message`, so they don't require a running target.

## Known placeholders

The refusal-phrase tables in `recon/config.py` (`MODEL_FAMILY_PHRASES`,
`DEFENSE_SIGNALS`) are calibrated against the mock target only. They need to
be recalibrated against Ahmed's real Phi/Ollama target once it's running.
