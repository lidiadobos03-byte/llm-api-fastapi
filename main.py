import os
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from openai import OpenAI
from openai import OpenAIError
from pydantic import BaseModel, ConfigDict, Field

load_dotenv()

DEFAULT_MODEL = "gpt-5.4-mini"

app = FastAPI(
    title="LLM API",
    version="0.1.0",
    description="Minimal FastAPI service for generating text with OpenAI.",
)


class GenerateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(..., min_length=1, max_length=8_000)
    system_prompt: str = Field(
        default="You are a helpful assistant.",
        min_length=1,
        max_length=4_000,
    )


class GenerateResponse(BaseModel):
    response: str
    model: str


@lru_cache
def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to your environment or .env file."
        )

    return OpenAI(api_key=api_key)


@app.post("/generate")
def generate_text(body: GenerateRequest) -> GenerateResponse:
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    try:
        client = get_openai_client()
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": body.system_prompt},
                {"role": "user", "content": body.prompt},
            ],
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except OpenAIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenAI API request failed: {exc}",
        ) from exc

    output_text = response.output_text.strip()
    if not output_text:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The model returned an empty response.",
        )

    return GenerateResponse(response=output_text, model=model)


@app.get("/")
def home():
    return {
        "message": "LLM API is running",
        "docs": "/docs",
        "health": "/healthz",
    }


@app.get("/healthz")
def healthcheck():
    return {
        "status": "ok",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "model": os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
    }
