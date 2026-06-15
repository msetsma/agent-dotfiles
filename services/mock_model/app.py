from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette.responses import StreamingResponse


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage] = Field(min_length=1)
    stream: bool = False


app = FastAPI(title="Hermes Assistant Mock Model")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/models")
def models() -> dict[str, list[dict[str, str]]]:
    return {
        "data": [
            {
                "id": "mock-work-safe",
                "object": "model",
                "owned_by": "local",
            }
        ]
    }


@app.post("/v1/chat/completions", response_model=None)
def chat_completions(
    request: ChatCompletionRequest,
) -> dict[str, object] | StreamingResponse:
    user_messages = [
        message.content for message in request.messages if message.role == "user"
    ]
    latest = user_messages[-1] if user_messages else ""
    content = (
        "This response came from the local mock model endpoint. "
        f"Received: {latest}"
    )

    if request.stream:
        return StreamingResponse(
            stream_chat_completion(request.model, content),
            media_type="text/event-stream",
        )

    return {
        "id": "chatcmpl-mock",
        "object": "chat.completion",
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": content,
                },
            }
        ],
        "usage": {
            "prompt_tokens": 1,
            "completion_tokens": 1,
            "total_tokens": 2,
        },
    }


def stream_chat_completion(model: str, content: str) -> Iterator[str]:
    chunk = {
        "id": "chatcmpl-mock",
        "object": "chat.completion.chunk",
        "model": model,
        "choices": [
            {
                "index": 0,
                "finish_reason": None,
                "delta": {"content": content},
            }
        ],
    }
    final_chunk = {
        "id": "chatcmpl-mock",
        "object": "chat.completion.chunk",
        "model": model,
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "delta": {},
            }
        ],
    }

    yield f"data: {json.dumps(chunk, separators=(',', ':'))}\n\n"
    yield f"data: {json.dumps(final_chunk, separators=(',', ':'))}\n\n"
    yield "data: [DONE]\n\n"
