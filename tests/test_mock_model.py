from fastapi.testclient import TestClient

from services.mock_model.app import app


def test_healthz_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_completions_returns_openai_compatible_shape() -> None:
    client = TestClient(app)

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "mock-work-safe",
            "messages": [{"role": "user", "content": "Say hello."}],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "chatcmpl-mock"
    assert payload["object"] == "chat.completion"
    assert payload["choices"][0]["message"]["role"] == "assistant"
    assert "mock model endpoint" in payload["choices"][0]["message"]["content"]


def test_chat_completions_streams_openai_compatible_sse_chunks() -> None:
    client = TestClient(app)

    with client.stream(
        "POST",
        "/v1/chat/completions",
        json={
            "model": "mock-work-safe",
            "stream": True,
            "messages": [{"role": "user", "content": "Say hello."}],
        },
    ) as response:
        response.read()
        body = response.text

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert 'data: {"id":"chatcmpl-mock"' in body
    assert '"object":"chat.completion.chunk"' in body
    assert (
        '"delta":{"content":"This response came from the local mock model endpoint. '
        'Received: Say hello."}'
    ) in body
    assert body.endswith("data: [DONE]\n\n")


def test_models_endpoint_lists_mock_model() -> None:
    client = TestClient(app)

    response = client.get("/v1/models")

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == "mock-work-safe"
