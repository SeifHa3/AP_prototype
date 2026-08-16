"""
Throwaway stand-in for Ahmed's target bot so RECON can be built and tested
before his real FastAPI + Phi/Ollama service is up. Same request/response
shape as the real target: POST /chat {"message": str} -> {"response": str}.

Behaves like a bot with role_enforcement + safety_classifier style defenses,
and toggles Arabic/English phrasing based on whether it was told to answer
only in English, so all three RECON dimensions have something real to probe.
Delete this once Ahmed's target is ready.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


def generate_response(message: str) -> str:
    lower = message.lower()

    if "system prompt" in lower:
        return "I can't do that."

    if "ignore" in lower and "instruction" in lower:
        return "I can only help with civil registry citizen services."

    if "staff" in lower or "internal" in lower or "restricted" in lower:
        return (
            "Internal staff procedures aren't something I can detail here, "
            "but generally case workers follow standard verification steps."
        )

    if "respond only in english" in lower:
        return "Understood, I will respond only in English from now on."

    english_only = "respond only in english" in lower
    if english_only:
        return "You need the birth certificate and both parents' national IDs to register a birth."

    return (
        "لتسجيل مولود جديد (to register a birth) you need the birth certificate "
        "and the parents' IDs. مرحباً بكم."
    )


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return ChatResponse(response=generate_response(req.message))
