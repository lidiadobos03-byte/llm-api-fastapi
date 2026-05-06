# LLM API FastAPI

A lightweight FastAPI project that exposes a simple REST API for text generation with OpenAI.

This repository is designed as a clean starter project for an LLM-powered backend. It includes request validation, environment-based configuration, a health check endpoint, and a small test suite.

## Features

- FastAPI-based REST API
- OpenAI integration through the Responses API
- Input validation with Pydantic
- `.env` configuration support
- Health check endpoint
- Simple automated tests with `pytest`
- Ready-to-extend project structure for demos or coursework

## Endpoints

### `GET /`

Returns a basic service status message.

### `GET /healthz`

Returns:

- API health status
- whether `OPENAI_API_KEY` is configured
- the active model name

### `POST /generate`

Generates a text response from a user prompt.

Example request body:

```json
{
  "prompt": "Write a short welcome message for a new user.",
  "system_prompt": "You are a concise assistant."
}
```

Example response:

```json
{
  "response": "Welcome! We are glad you are here.",
  "model": "gpt-5.4-mini"
}
```

## Tech Stack

- Python
- FastAPI
- OpenAI Python SDK
- Pydantic
- Uvicorn
- Pytest

## Project Structure

```text
llm-api-fastapi/
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── tests/
│   └── test_main.py
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/lidiadobos03-byte/llm-api-fastapi.git
cd llm-api-fastapi
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For development and testing:

```bash
pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Then set your OpenAI API key inside `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.4-mini
```

## Running the API

Start the development server:

```bash
uvicorn main:app --reload
```

Once the server is running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Running Tests

```bash
pytest -q
```

## Notes

- The API can start without an OpenAI key.
- If `OPENAI_API_KEY` is missing, the server still runs, but `POST /generate` will return an error until the key is configured.
- The default model is `gpt-5.4-mini`, but it can be changed with `OPENAI_MODEL`.

## Example cURL Request

```bash
curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short product description for a note-taking app.",
    "system_prompt": "You are a helpful assistant for marketing copy."
  }'
```

## Why This Project

This project is a good foundation for:

- learning how to build a Python API with FastAPI
- integrating an external AI service into a backend
- using environment variables securely
- preparing a simple portfolio or academic demo project

## Future Improvements

- Docker support
- rate limiting
- structured logging
- async service layer
- separate `routers/`, `services/`, and `schemas/` modules
- deployment configuration for Render, Railway, or Fly.io

## License

This project is provided for educational and portfolio use.
