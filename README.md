# LLM API with FastAPI

Small FastAPI service that sends prompts to OpenAI and returns the generated text.

## What it includes

- `POST /generate` for text generation
- `GET /` for a basic status message
- `GET /healthz` for a simple health check
- environment-based configuration with `.env`

## Requirements

- Python 3.10+
- an OpenAI API key

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the example environment file and fill in your API key:

```bash
cp .env.example .env
```

4. Run the API:

```bash
uvicorn main:app --reload
```

5. Open the docs:

```text
http://127.0.0.1:8000/docs
```

## Example request

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short welcome message for a new user.",
    "system_prompt": "You are a concise assistant."
  }'
```

## Response example

```json
{
  "response": "Welcome! We are glad you are here.",
  "model": "gpt-5.4-mini"
}
```

## Notes

- By default, the app uses `gpt-5.4-mini`.
- You can override the model with the `OPENAI_MODEL` environment variable.
- If `OPENAI_API_KEY` is missing, `/generate` returns a clear server error message instead of crashing the app on startup.
