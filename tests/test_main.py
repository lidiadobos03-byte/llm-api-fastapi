from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


class DummyResponse:
    output_text = "Generated from test"


class DummyResponsesAPI:
    def create(self, **kwargs):
        assert kwargs["model"] == "test-model"
        assert kwargs["input"][1]["content"] == "Hello"
        return DummyResponse()


class DummyOpenAIClient:
    responses = DummyResponsesAPI()


def test_healthcheck_reports_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "openai_configured": False,
        "model": "test-model",
    }


def test_generate_returns_model_output(monkeypatch):
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setattr(main, "get_openai_client", lambda: DummyOpenAIClient())

    response = client.post("/generate", json={"prompt": "Hello"})

    assert response.status_code == 200
    assert response.json() == {
        "response": "Generated from test",
        "model": "test-model",
    }
